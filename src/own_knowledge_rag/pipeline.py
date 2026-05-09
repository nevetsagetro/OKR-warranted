import json
import logging
import os
import shutil
import time
from collections import OrderedDict
from hashlib import sha256
from dataclasses import asdict, dataclass
from contextlib import contextmanager
from pathlib import Path
from datetime import UTC, datetime

from own_knowledge_rag.answering import ExtractiveAnswerer
from own_knowledge_rag.calibration import RefusalCalibrator
from own_knowledge_rag.config import CANONICAL_TERMS_VERSION, Settings
from own_knowledge_rag.embeddings import EmbeddingModel
from own_knowledge_rag.evaluation import Evaluator
from own_knowledge_rag.filename_metadata import augment_country_index, build_country_index
from own_knowledge_rag.generation import build_generator
from own_knowledge_rag.lexical import BM25Index
from own_knowledge_rag.models import (
    Answer,
    CalibrationReport,
    EvaluationSummary,
    KnowledgeBlock,
    ParsedDocument,
    SearchHit,
)
from own_knowledge_rag.normalizers import SCHEMA_VERSION as NORMALIZER_SCHEMA_VERSION
from own_knowledge_rag.normalizers import normalize_document
from own_knowledge_rag.parsers import SCHEMA_VERSION as PARSER_SCHEMA_VERSION
from own_knowledge_rag.parsers import can_parse_file, normalize_allowed_suffixes, parse_file
from own_knowledge_rag.query_cache import (
    deserialize_answer,
    load_query_cache,
    query_cache_key,
    save_query_cache,
    serialize_answer,
    should_cache_answer,
)
from own_knowledge_rag.retrieval import HybridRetriever
from own_knowledge_rag.query_router import extract_query_filters
from own_knowledge_rag.reranking import build_reranker
from own_knowledge_rag.enrichment import Enricher
from own_knowledge_rag.vector_store import build_vector_store, load_vector_store, vector_store_snapshot_path
from own_knowledge_rag.analytics import (
    KnowledgeAnalytics,
    generate_consistency_report,
    generate_ds_report,
    seed_review_findings,
)
from own_knowledge_rag.benchmark_generation import export_review_findings_benchmark


logger = logging.getLogger(__name__)


class BuildLockError(RuntimeError):
    def __init__(self, message: str, lock_info: dict[str, object] | None = None) -> None:
        super().__init__(message)
        self.lock_info = lock_info or {}


@dataclass
class BuildLockStatus:
    locked: bool
    path: str
    stale: bool = False
    reason: str = ""
    pid: int | None = None
    source_dir: str = ""
    work_dir: str = ""
    allowed_suffixes: list[str] | None = None
    started_at: int | None = None
    age_seconds: int | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "locked": self.locked,
            "path": self.path,
            "stale": self.stale,
            "reason": self.reason,
            "pid": self.pid,
            "source_dir": self.source_dir,
            "work_dir": self.work_dir,
            "allowed_suffixes": self.allowed_suffixes or [],
            "started_at": self.started_at,
            "age_seconds": self.age_seconds,
        }


@dataclass
class RetrieverCacheEntry:
    retriever: HybridRetriever
    loaded_at: float
    manifest_mtime: float


class KnowledgePipeline:
    STALE_LOCK_SECONDS = 24 * 60 * 60
    RETRIEVER_CACHE_SIZE = 3

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._generator = build_generator(settings)
        self._answerer = ExtractiveAnswerer(
            min_score_threshold=settings.min_answer_score,
            min_overlap_ratio=settings.min_answer_overlap_ratio,
            tier0_score_threshold=settings.tier0_score_threshold,
            tier2_score_threshold=settings.tier2_score_threshold,
            generator=self._generator,
            generation_max_evidence=settings.generation_max_evidence,
        )
        self._evaluator = Evaluator()
        self._calibrator = RefusalCalibrator(self._evaluator)
        self._enricher = Enricher(settings)
        self._reranker = build_reranker(settings)
        # Cache loaded retrievers by work_dir path to avoid re-deserializing
        # 61k blocks on every API request.
        self._retriever_cache: OrderedDict[str, RetrieverCacheEntry] = OrderedDict()

    def build_index(
        self, 
        source_dir: Path | None = None, 
        work_dir: Path | None = None,
        force_reenrich: bool = False,
        allow_low_quality: bool = False,
        allowed_suffixes: list[str] | tuple[str, ...] | set[str] | None = None,
    ) -> dict[str, object]:
        total_started_at = time.monotonic()
        source_dir = source_dir or self._settings.source_dir
        work_dir = work_dir or self._settings.work_dir
        work_dir.mkdir(parents=True, exist_ok=True)
        normalized_suffixes = list(normalize_allowed_suffixes(allowed_suffixes))
        with self._acquire_build_lock(work_dir, source_dir, normalized_suffixes):
            previous_manifest = self._load_manifest(work_dir)
            previous_documents = self._load_documents_index(work_dir)
            previous_blocks, previous_vectors = self._load_block_vector_index(work_dir)
            fingerprints, skipped_files = self._source_fingerprints(
                source_dir,
                normalized_suffixes,
                max_file_bytes=self._settings.max_file_bytes,
            )
            embedding_model = EmbeddingModel(self._settings)

            reuse_enabled = self._can_reuse_previous_index(previous_manifest, normalized_suffixes)
            documents: list[ParsedDocument] = []
            blocks: list[KnowledgeBlock] = []
            vectors: list[list[float]] = []
            rebuilt_documents = 0
            reused_documents = 0

            failed_files = []
            blocks_per_file = {}
            missing_tag_blocks = 0
            low_quality_blocks = 0
            rejected_blocks = 0
            duplicate_blocks = 0
            code_blocks_erased = 0
            code_blocks_preserved = 0
            drift_risk_blocks = 0
            encoding_fallback_files: list[dict[str, object]] = []
            duplicate_block_reasons = {}
            flagged_block_reasons = {}
            seen_block_hashes: set[str] = set()
            total_documents = len(fingerprints)
            started_at = time.monotonic()
            build_timings = {
                "parse_time": 0.0,
                "normalize_time": 0.0,
                "enrichment_time": 0.0,
                "embedding_time": 0.0,
                "vector_store_time": 0.0,
                "total_time": 0.0,
            }
            enrichment_total_before = self._enricher.total_blocks
            enrichment_cache_hits_before = self._enricher.cache_hits
            enrichment_api_calls_before = self._enricher.api_calls
            enrichment_live_blocks_before = self._enricher.live_enrichment_blocks

            for document_number, (path, fingerprint) in enumerate(fingerprints, start=1):
                document_id = path.stem
                print(
                    f"Index Progress | document={document_number}/{total_documents} | id={document_id} "
                    f"| elapsed={self._format_duration(time.monotonic() - started_at)} "
                    f"| eta={self._format_duration(self._estimate_eta_seconds(document_number - 1, total_documents, time.monotonic() - started_at))}"
                )
                can_reuse = reuse_enabled and previous_manifest.get("documents_state", {}).get(document_id) == fingerprint
                if can_reuse and not force_reenrich and document_id in previous_documents and document_id in previous_blocks:
                    documents.append(previous_documents[document_id])
                    cached_blocks = previous_blocks[document_id]
                    cached_vectors = previous_vectors.get(document_id, [])
                    reused_blocks: list[KnowledgeBlock] = []
                    reused_vectors: list[list[float]] = []
                    for block, vector in zip(cached_blocks, cached_vectors, strict=False):
                        duplicate_of = self._dedupe_duplicate_of(block, seen_block_hashes)
                        if duplicate_of:
                            duplicate_blocks += 1
                            duplicate_block_reasons[block.block_id] = duplicate_of
                            flagged_block_reasons[block.block_id] = "DUPLICATE"
                            continue
                        reused_blocks.append(block)
                        reused_vectors.append(vector)
                    blocks.extend(reused_blocks)
                    vectors.extend(reused_vectors)
                    reused_documents += 1
                    
                    blocks_per_file[document_id] = len(reused_blocks)
                    for b in reused_blocks:
                        if not b.country and not b.iso_code and not b.sender_types and not b.regulation_topics:
                            missing_tag_blocks += 1
                        if b.quality_status != "ok":
                            low_quality_blocks += 1
                            flagged_block_reasons[b.block_id] = b.quality_status
                        if b.metadata.get("drift_risk") == "true":
                            drift_risk_blocks += 1
                            flagged_block_reasons[b.block_id] = "DRIFT_RISK"
                    reused_code_preserved = self._document_code_blocks_preserved(reused_blocks)
                    code_blocks_preserved += reused_code_preserved
                    code_blocks_erased += self._document_code_blocks_erased(reused_blocks)
                    if documents[-1].encoding_fallback:
                        encoding_fallback_files.append(self._encoding_fallback_record(documents[-1]))
                    print(
                        f"Index Progress | document={document_number}/{total_documents} | id={document_id} | reused=1 | blocks={len(reused_blocks)} "
                        f"| elapsed={self._format_duration(time.monotonic() - started_at)} "
                        f"| eta={self._format_duration(self._estimate_eta_seconds(document_number, total_documents, time.monotonic() - started_at))}"
                    )
                    continue

                try:
                    stage_started = time.monotonic()
                    parsed = parse_file(path)
                    build_timings["parse_time"] += time.monotonic() - stage_started
                    if parsed is None:
                        continue
                    if parsed.encoding_fallback:
                        encoding_fallback_files.append(self._encoding_fallback_record(parsed))
                    stage_started = time.monotonic()
                    normalized_blocks = normalize_document(
                        parsed,
                        chunk_size=self._settings.chunk_size,
                        chunk_overlap=self._settings.chunk_overlap,
                    )
                    build_timings["normalize_time"] += time.monotonic() - stage_started
                    code_blocks_preserved += self._document_code_blocks_preserved(normalized_blocks)
                    code_blocks_erased += self._document_code_blocks_erased(normalized_blocks)
                    
                    stage_started = time.monotonic()
                    enriched_blocks = self._enricher.enrich_blocks(parsed, normalized_blocks, work_dir, force_reenrich=force_reenrich)
                    mapped_blocks = self._enricher.validate_blocks(enriched_blocks)
                    build_timings["enrichment_time"] += time.monotonic() - stage_started
                    
                    valid_blocks = []
                    for b in mapped_blocks:
                        if b.quality_status == "REJECTED":
                            flagged_block_reasons[b.block_id] = b.quality_status
                            rejected_blocks += 1
                            continue
                            
                        if b.quality_status == "LOW_QUALITY":
                            flagged_block_reasons[b.block_id] = b.quality_status
                            low_quality_blocks += 1
                        if b.metadata.get("drift_risk") == "true":
                            flagged_block_reasons[b.block_id] = "DRIFT_RISK"
                            drift_risk_blocks += 1
                            
                        valid_blocks.append(b)

                    deduped_blocks: list[KnowledgeBlock] = []
                    for b in valid_blocks:
                        duplicate_of = self._dedupe_duplicate_of(b, seen_block_hashes)
                        if duplicate_of:
                            flagged_block_reasons[b.block_id] = "DUPLICATE"
                            duplicate_block_reasons[b.block_id] = duplicate_of
                            duplicate_blocks += 1
                            continue
                        deduped_blocks.append(b)
                            
                    stage_started = time.monotonic()
                    document_vectors = (
                        embedding_model.encode([self._embedding_text(block) for block in deduped_blocks])
                        if deduped_blocks
                        else []
                    )
                    build_timings["embedding_time"] += time.monotonic() - stage_started
                    documents.append(parsed)
                    blocks.extend(deduped_blocks)
                    vectors.extend(document_vectors)
                    rebuilt_documents += 1
                    print(
                        f"Index Progress | document={document_number}/{total_documents} | id={document_id} | rebuilt=1 | blocks={len(deduped_blocks)} "
                        f"| elapsed={self._format_duration(time.monotonic() - started_at)} "
                        f"| eta={self._format_duration(self._estimate_eta_seconds(document_number, total_documents, time.monotonic() - started_at))}"
                    )
                    
                    blocks_per_file[document_id] = len(mapped_blocks)
                    for b in mapped_blocks:
                        if not b.country and not b.iso_code and not b.sender_types and not b.regulation_topics:
                            missing_tag_blocks += 1
                except Exception as e:
                    logger.error(f"Failed to process {path}: {type(e).__name__} - {e}")
                    failed_files.append({"file": str(path), "error": str(e), "type": type(e).__name__})
                    print(
                        f"Index Progress | document={document_number}/{total_documents} | id={document_id} | failed={type(e).__name__} "
                        f"| elapsed={self._format_duration(time.monotonic() - started_at)} "
                        f"| eta={self._format_duration(self._estimate_eta_seconds(document_number, total_documents, time.monotonic() - started_at))}"
                    )

            self._enricher.log_costs()

            zero_block_files = [k for k, v in blocks_per_file.items() if v == 0]
            total_blocks = len(blocks)
            success_rate = round(((total_blocks - missing_tag_blocks) / total_blocks * 100), 2) if total_blocks else 0
            enrichment_total_blocks = self._enricher.total_blocks - enrichment_total_before
            enrichment_cache_hits = self._enricher.cache_hits - enrichment_cache_hits_before
            enrichment_api_calls = self._enricher.api_calls - enrichment_api_calls_before
            enrichment_live_blocks = self._enricher.live_enrichment_blocks - enrichment_live_blocks_before
            cache_hit_rate = round(enrichment_cache_hits / max(1, enrichment_total_blocks), 4)
            build_timings["total_time"] = time.monotonic() - total_started_at
            rounded_timings = {
                key: round(value, 4)
                for key, value in build_timings.items()
            }
            performance = {
                **rounded_timings,
                "cache_hit_rate": cache_hit_rate,
                "enrichment_total_blocks": enrichment_total_blocks,
                "enrichment_cache_hits": enrichment_cache_hits,
                "enrichment_live_blocks": enrichment_live_blocks,
                "enrichment_api_calls": enrichment_api_calls,
                "reused_document_rate": round(reused_documents / max(1, total_documents), 4),
            }
            ingest_report = {
                "total_files_parsed": len(documents),
                "total_blocks_produced": total_blocks,
                "success_rate": success_rate,
                "performance": performance,
                **rounded_timings,
                "cache_hit_rate": cache_hit_rate,
                "enrichment_provider": self._settings.mapping_provider,
                "enrichment_model": self._settings.mapping_model,
                "canonical_terms_version": CANONICAL_TERMS_VERSION,
                "low_quality_blocks": low_quality_blocks,
                "rejected_blocks": rejected_blocks,
                "duplicate_blocks": duplicate_blocks,
                "code_blocks_erased": code_blocks_erased,
                "code_blocks_preserved": code_blocks_preserved,
                "drift_risk_blocks": drift_risk_blocks,
                "encoding_fallback_files": encoding_fallback_files,
                "failed_files": failed_files,
                "skipped_files": skipped_files,
                "zero_block_files": zero_block_files,
                "flagged_block_reasons": flagged_block_reasons,
                "duplicate_block_reasons": duplicate_block_reasons,
                "blocks_per_file": blocks_per_file,
            }
            (work_dir / "ingest_report.json").write_text(json.dumps(ingest_report, indent=2), encoding="utf-8")

            (work_dir / "documents.json").write_text(
                json.dumps([asdict(document) for document in documents], indent=2),
                encoding="utf-8",
            )
            (work_dir / "blocks.json").write_text(
                json.dumps([asdict(block) for block in blocks], indent=2),
                encoding="utf-8",
            )
            stage_started = time.monotonic()
            build_vector_store(self._settings, blocks, vectors).save(work_dir)
            build_timings["vector_store_time"] += time.monotonic() - stage_started
            build_timings["total_time"] = time.monotonic() - total_started_at
            rounded_timings = {
                key: round(value, 4)
                for key, value in build_timings.items()
            }
            performance = {
                **rounded_timings,
                "cache_hit_rate": cache_hit_rate,
                "enrichment_total_blocks": enrichment_total_blocks,
                "enrichment_cache_hits": enrichment_cache_hits,
                "enrichment_live_blocks": enrichment_live_blocks,
                "enrichment_api_calls": enrichment_api_calls,
                "reused_document_rate": round(reused_documents / max(1, total_documents), 4),
            }
            ingest_report.update(
                {
                    "performance": performance,
                    **rounded_timings,
                    "cache_hit_rate": cache_hit_rate,
                }
            )
            (work_dir / "ingest_report.json").write_text(json.dumps(ingest_report, indent=2), encoding="utf-8")

            manifest = {
                "documents": len(documents),
                "blocks": len(blocks),
                **rounded_timings,
                "cache_hit_rate": cache_hit_rate,
                "enrichment_provider": self._settings.mapping_provider,
                "enrichment_model": self._settings.mapping_model,
                "canonical_terms_version": CANONICAL_TERMS_VERSION,
                "performance": performance,
                "reused_documents": reused_documents,
                "rebuilt_documents": rebuilt_documents,
                "duplicate_blocks": duplicate_blocks,
                "code_blocks_erased": code_blocks_erased,
                "code_blocks_preserved": code_blocks_preserved,
                "drift_risk_blocks": drift_risk_blocks,
                "encoding_fallback_files": encoding_fallback_files,
                "skipped_files": skipped_files,
                "max_file_bytes": self._settings.max_file_bytes,
                "allowed_suffixes": normalized_suffixes,
                "parser_schema_version": PARSER_SCHEMA_VERSION,
                "normalizer_schema_version": NORMALIZER_SCHEMA_VERSION,
                "chunk_size": self._settings.chunk_size,
                "chunk_overlap": self._settings.chunk_overlap,
                "mapping_provider": self._settings.mapping_provider,
                "mapping_model": self._settings.mapping_model,
                "mapping_batch_size": self._settings.mapping_batch_size,
                "mapping_batch_delay_ms": self._settings.mapping_batch_delay_ms,
                "mapping_text_char_limit": self._settings.mapping_text_char_limit,
                "mapping_prompt_mode": self._settings.mapping_prompt_mode,
                "mapping_retry_missing_results": self._settings.mapping_retry_missing_results,
                "embedding_provider": self._settings.embedding_provider,
                "embedding_model": self._settings.embedding_model,
                "embedding_device": self._settings.embedding_device,
                "embedding_dimensions": self._settings.embedding_dimensions,
                "vector_backend": self._settings.vector_backend,
                "vector_collection": self._settings.vector_collection,
                "qdrant_url": self._settings.qdrant_url,
                "reranker_provider": self._settings.reranker_provider,
                "reranker_model": self._settings.reranker_model,
                "reranker_top_n": self._settings.reranker_top_n,
                "rrf_lexical_weight": self._settings.rrf_lexical_weight,
                "rrf_vector_weight": self._settings.rrf_vector_weight,
                "arm_k_multiplier": self._settings.arm_k_multiplier,
                "max_blocks_per_document": self._settings.max_blocks_per_document,
                "documents_state": {path.stem: fingerprint for path, fingerprint in fingerprints},
            }
            (work_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
            cache_key = str(work_dir.resolve())
            if cache_key in self._retriever_cache:
                del self._retriever_cache[cache_key]
            print(
                "Index Performance | "
                f"parse={rounded_timings['parse_time']}s | "
                f"normalize={rounded_timings['normalize_time']}s | "
                f"enrichment={rounded_timings['enrichment_time']}s | "
                f"embedding={rounded_timings['embedding_time']}s | "
                f"vector_store={rounded_timings['vector_store_time']}s | "
                f"total={rounded_timings['total_time']}s | "
                f"cache_hit_rate={cache_hit_rate}"
            )
            return manifest

    def build_merged_index(
        self,
        *,
        baseline_work_dir: Path,
        experiment_source_dir: Path,
        work_dir: Path,
        force_reenrich: bool = False,
        allow_low_quality: bool = False,
        allowed_suffixes: list[str] | tuple[str, ...] | set[str] | None = None,
    ) -> dict[str, object]:
        total_started_at = time.monotonic()
        normalized_suffixes = list(normalize_allowed_suffixes(allowed_suffixes))
        baseline_manifest = self._load_manifest(baseline_work_dir)
        if not baseline_manifest:
            raise ValueError(f"Baseline work_dir is missing manifest.json: {baseline_work_dir}")

        baseline_documents = self._load_documents_index(baseline_work_dir)
        baseline_blocks, baseline_vectors = self._load_block_vector_index(baseline_work_dir)
        if not baseline_documents or not baseline_blocks:
            raise ValueError(f"Baseline work_dir is missing index artifacts: {baseline_work_dir}")

        timestamp = datetime.now(UTC).strftime("%Y%m%d-%H%M%S")
        delta_work_dir = work_dir.parent / f".{work_dir.name}.delta-{timestamp}"
        if delta_work_dir.exists():
            shutil.rmtree(delta_work_dir)

        delta_manifest = self.build_index(
            source_dir=experiment_source_dir,
            work_dir=delta_work_dir,
            force_reenrich=force_reenrich,
            allow_low_quality=allow_low_quality,
            allowed_suffixes=normalized_suffixes,
        )
        delta_documents = self._load_documents_index(delta_work_dir)
        delta_blocks, delta_vectors = self._load_block_vector_index(delta_work_dir)
        delta_doc_ids = set(delta_documents)

        work_dir.mkdir(parents=True, exist_ok=True)
        with self._acquire_build_lock(work_dir, experiment_source_dir, normalized_suffixes):
            documents: list[ParsedDocument] = []
            blocks: list[KnowledgeBlock] = []
            vectors: list[list[float]] = []
            reused_baseline_documents = 0
            replaced_documents = 0

            for document_id, document in baseline_documents.items():
                if document_id in delta_doc_ids:
                    replaced_documents += 1
                    continue
                documents.append(document)
                doc_blocks = baseline_blocks.get(document_id, [])
                doc_vectors = baseline_vectors.get(document_id, [])
                blocks.extend(doc_blocks)
                vectors.extend(doc_vectors[: len(doc_blocks)])
                reused_baseline_documents += 1

            for document_id, document in delta_documents.items():
                documents.append(document)
                doc_blocks = delta_blocks.get(document_id, [])
                doc_vectors = delta_vectors.get(document_id, [])
                blocks.extend(doc_blocks)
                vectors.extend(doc_vectors[: len(doc_blocks)])

            if len(blocks) != len(vectors):
                raise ValueError(
                    f"Merged block/vector count mismatch: {len(blocks)} blocks vs {len(vectors)} vectors"
                )

            build_timings = {
                "parse_time": float(delta_manifest.get("parse_time", 0.0) or 0.0),
                "normalize_time": float(delta_manifest.get("normalize_time", 0.0) or 0.0),
                "enrichment_time": float(delta_manifest.get("enrichment_time", 0.0) or 0.0),
                "embedding_time": float(delta_manifest.get("embedding_time", 0.0) or 0.0),
                "vector_store_time": 0.0,
                "total_time": 0.0,
            }

            (work_dir / "documents.json").write_text(
                json.dumps([asdict(document) for document in documents], indent=2),
                encoding="utf-8",
            )
            (work_dir / "blocks.json").write_text(
                json.dumps([asdict(block) for block in blocks], indent=2),
                encoding="utf-8",
            )

            stage_started = time.monotonic()
            build_vector_store(self._settings, blocks, vectors).save(work_dir)
            build_timings["vector_store_time"] = time.monotonic() - stage_started
            build_timings["total_time"] = time.monotonic() - total_started_at
            rounded_timings = {key: round(value, 4) for key, value in build_timings.items()}

            baseline_state = baseline_manifest.get("documents_state", {})
            baseline_state = baseline_state if isinstance(baseline_state, dict) else {}
            delta_state = delta_manifest.get("documents_state", {})
            delta_state = delta_state if isinstance(delta_state, dict) else {}
            documents_state = {
                str(document_id): fingerprint
                for document_id, fingerprint in baseline_state.items()
                if str(document_id) not in delta_doc_ids
            }
            documents_state.update({str(document_id): fingerprint for document_id, fingerprint in delta_state.items()})

            low_quality_blocks = sum(1 for block in blocks if block.quality_status == "LOW_QUALITY")
            rejected_blocks = sum(1 for block in blocks if block.quality_status == "REJECTED")
            performance = {
                **rounded_timings,
                "cache_hit_rate": float(delta_manifest.get("cache_hit_rate", 0.0) or 0.0),
                "enrichment_total_blocks": (delta_manifest.get("performance") or {}).get("enrichment_total_blocks", 0)
                if isinstance(delta_manifest.get("performance"), dict)
                else 0,
                "enrichment_cache_hits": (delta_manifest.get("performance") or {}).get("enrichment_cache_hits", 0)
                if isinstance(delta_manifest.get("performance"), dict)
                else 0,
                "enrichment_live_blocks": (delta_manifest.get("performance") or {}).get("enrichment_live_blocks", 0)
                if isinstance(delta_manifest.get("performance"), dict)
                else 0,
                "enrichment_api_calls": (delta_manifest.get("performance") or {}).get("enrichment_api_calls", 0)
                if isinstance(delta_manifest.get("performance"), dict)
                else 0,
                "reused_document_rate": round(reused_baseline_documents / max(1, len(documents)), 4),
            }

            ingest_report = {
                "total_files_parsed": len(delta_documents),
                "total_blocks_produced": len(blocks),
                "success_rate": 100.0 if blocks else 0.0,
                "performance": performance,
                **rounded_timings,
                "cache_hit_rate": performance["cache_hit_rate"],
                "low_quality_blocks": low_quality_blocks,
                "rejected_blocks": rejected_blocks,
                "duplicate_blocks": int(delta_manifest.get("duplicate_blocks", 0) or 0),
                "failed_files": [],
                "skipped_files": delta_manifest.get("skipped_files", []),
                "zero_block_files": [],
                "flagged_block_reasons": {},
                "duplicate_block_reasons": {},
                "blocks_per_file": {
                    document_id: len(baseline_blocks.get(document_id, []))
                    for document_id in baseline_documents
                    if document_id not in delta_doc_ids
                }
                | {document_id: len(delta_blocks.get(document_id, [])) for document_id in delta_documents},
            }
            (work_dir / "ingest_report.json").write_text(json.dumps(ingest_report, indent=2), encoding="utf-8")

            self._merge_enrichment_caches(baseline_work_dir, delta_work_dir, work_dir)

            manifest = {
                "documents": len(documents),
                "blocks": len(blocks),
                **rounded_timings,
                "cache_hit_rate": performance["cache_hit_rate"],
                "performance": performance,
                "merge_strategy": "incremental_artifact_merge",
                "baseline_work_dir": str(baseline_work_dir),
                "experiment_source_dir": str(experiment_source_dir),
                "delta_work_dir": str(delta_work_dir),
                "reused_documents": reused_baseline_documents,
                "rebuilt_documents": len(delta_documents),
                "reused_baseline_documents": reused_baseline_documents,
                "replaced_documents": replaced_documents,
                "added_documents": max(0, len(delta_documents) - replaced_documents),
                "duplicate_blocks": int(delta_manifest.get("duplicate_blocks", 0) or 0),
                "skipped_files": delta_manifest.get("skipped_files", []),
                "max_file_bytes": self._settings.max_file_bytes,
                "allowed_suffixes": normalized_suffixes,
                "parser_schema_version": PARSER_SCHEMA_VERSION,
                "normalizer_schema_version": NORMALIZER_SCHEMA_VERSION,
                "chunk_size": self._settings.chunk_size,
                "chunk_overlap": self._settings.chunk_overlap,
                "mapping_provider": self._settings.mapping_provider,
                "mapping_model": self._settings.mapping_model,
                "mapping_batch_size": self._settings.mapping_batch_size,
                "mapping_batch_delay_ms": self._settings.mapping_batch_delay_ms,
                "mapping_text_char_limit": self._settings.mapping_text_char_limit,
                "mapping_prompt_mode": self._settings.mapping_prompt_mode,
                "mapping_retry_missing_results": self._settings.mapping_retry_missing_results,
                "embedding_provider": self._settings.embedding_provider,
                "embedding_model": self._settings.embedding_model,
                "embedding_device": self._settings.embedding_device,
                "embedding_dimensions": self._settings.embedding_dimensions,
                "vector_backend": self._settings.vector_backend,
                "vector_collection": self._settings.vector_collection,
                "qdrant_url": self._settings.qdrant_url,
                "reranker_provider": self._settings.reranker_provider,
                "reranker_model": self._settings.reranker_model,
                "reranker_top_n": self._settings.reranker_top_n,
                "documents_state": documents_state,
            }
            (work_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
            self._retriever_cache.pop(str(work_dir.resolve()), None)
            print(
                "Incremental Merge Performance | "
                f"baseline_reused={reused_baseline_documents} | "
                f"delta_docs={len(delta_documents)} | "
                f"replaced={replaced_documents} | "
                f"vector_store={rounded_timings['vector_store_time']}s | "
                f"total={rounded_timings['total_time']}s"
            )
            return manifest
    

    @staticmethod
    def _build_lock_path(work_dir: Path) -> Path:
        return work_dir / ".build-index.lock"

    def inspect_build_lock(self, work_dir: Path | None = None) -> BuildLockStatus:
        work_dir = work_dir or self._settings.work_dir
        return self._inspect_build_lock_path(self._build_lock_path(work_dir))

    def clear_stale_build_lock(self, work_dir: Path | None = None) -> BuildLockStatus:
        work_dir = work_dir or self._settings.work_dir
        lock_path = self._build_lock_path(work_dir)
        status = self._inspect_build_lock_path(lock_path)
        if not status.locked:
            return status
        if not status.stale:
            raise BuildLockError(
                f"Build lock for {work_dir} appears active and was not cleared.",
                status.to_dict(),
            )
        try:
            lock_path.unlink()
        except FileNotFoundError:
            pass
        cleared = status.to_dict()
        cleared["cleared"] = True
        return BuildLockStatus(
            locked=False,
            path=str(lock_path),
            stale=False,
            reason=f"Cleared stale lock: {status.reason}",
            pid=status.pid,
            source_dir=status.source_dir,
            work_dir=status.work_dir,
            allowed_suffixes=status.allowed_suffixes,
            started_at=status.started_at,
            age_seconds=status.age_seconds,
        )

    @contextmanager
    def _acquire_build_lock(
        self,
        work_dir: Path,
        source_dir: Path,
        allowed_suffixes: list[str],
    ):
        lock_path = self._build_lock_path(work_dir)
        payload = {
            "pid": os.getpid(),
            "source_dir": str(source_dir),
            "work_dir": str(work_dir),
            "allowed_suffixes": allowed_suffixes,
            "started_at": int(time.time()),
        }
        try:
            fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            status = self._inspect_build_lock_path(lock_path)
            if status.stale:
                try:
                    lock_path.unlink()
                    fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                except FileExistsError:
                    status = self._inspect_build_lock_path(lock_path)
                else:
                    logger.info("Cleared stale build lock at %s: %s", lock_path, status.reason)
                    status = BuildLockStatus(locked=False, path=str(lock_path))
            if "fd" in locals():
                pass
            else:
                detail_suffix = f" Existing lock: {json.dumps(status.to_dict(), sort_keys=True)}"
                raise BuildLockError(
                    f"Another index build is already running for {work_dir}. "
                    f"Wait for it to finish, use a different work_dir, or clear the lock if it is stale."
                    f"{detail_suffix}",
                    status.to_dict(),
                ) from None
        if "fd" not in locals():
            status = self._inspect_build_lock_path(lock_path)
            detail_suffix = f" Existing lock: {json.dumps(status.to_dict(), sort_keys=True)}"
            raise BuildLockError(
                f"Another index build is already running for {work_dir}. "
                f"Wait for it to finish, use a different work_dir, or clear the lock if it is stale."
                f"{detail_suffix}",
                status.to_dict(),
            ) from None
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(payload, handle, indent=2)
            yield
        finally:
            try:
                if lock_path.exists():
                    lock_path.unlink()
            except FileNotFoundError:
                pass

    def _inspect_build_lock_path(self, lock_path: Path) -> BuildLockStatus:
        if not lock_path.exists():
            return BuildLockStatus(locked=False, path=str(lock_path))
        try:
            payload = json.loads(lock_path.read_text(encoding="utf-8"))
        except Exception:
            return BuildLockStatus(
                locked=True,
                path=str(lock_path),
                stale=True,
                reason="lock file is unreadable",
            )
        if not isinstance(payload, dict):
            return BuildLockStatus(
                locked=True,
                path=str(lock_path),
                stale=True,
                reason="lock file payload is invalid",
            )

        pid = self._lock_pid(payload.get("pid"))
        started_at = self._lock_started_at(payload.get("started_at"))
        now = int(time.time())
        age_seconds = max(0, now - started_at) if started_at is not None else None
        allowed_suffixes = payload.get("allowed_suffixes")
        if not isinstance(allowed_suffixes, list):
            allowed_suffixes = []

        stale = False
        reason = "active build lock"
        if pid is None:
            stale = True
            reason = "lock file has no valid pid"
        elif not self._pid_is_running(pid):
            stale = True
            reason = f"pid {pid} is not running"
        elif age_seconds is not None and age_seconds > self.STALE_LOCK_SECONDS:
            stale = True
            reason = f"lock is older than {self.STALE_LOCK_SECONDS} seconds"

        return BuildLockStatus(
            locked=True,
            path=str(lock_path),
            stale=stale,
            reason=reason,
            pid=pid,
            source_dir=str(payload.get("source_dir") or ""),
            work_dir=str(payload.get("work_dir") or ""),
            allowed_suffixes=[str(item) for item in allowed_suffixes],
            started_at=started_at,
            age_seconds=age_seconds,
        )

    @staticmethod
    def _lock_pid(value: object) -> int | None:
        try:
            pid = int(value)
        except (TypeError, ValueError):
            return None
        return pid if pid > 0 else None

    @staticmethod
    def _lock_started_at(value: object) -> int | None:
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _pid_is_running(pid: int) -> bool:
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return False
        except PermissionError:
            return True
        return True

    @staticmethod
    def _estimate_eta_seconds(processed: int, total: int, elapsed_seconds: float) -> float | None:
        if processed <= 0 or total <= processed:
            return 0.0 if total <= processed and total > 0 else None
        rate = elapsed_seconds / processed
        return max(0.0, rate * (total - processed))

    @staticmethod
    def _format_duration(seconds: float | None) -> str:
        if seconds is None:
            return "?"
        rounded = int(round(seconds))
        minutes, secs = divmod(rounded, 60)
        hours, minutes = divmod(minutes, 60)
        if hours:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        return f"{minutes:02d}:{secs:02d}"

    def get_block(self, block_id: str, work_dir: Path | None = None) -> KnowledgeBlock | None:
        work_dir = work_dir or self._settings.work_dir
        retriever = self._load_retriever(work_dir)
        return next((b for b in retriever._all_blocks if b.block_id == block_id), None)

    def explain_block(self, block_id: str, work_dir: Path | None = None) -> str:
        block = self.get_block(block_id, work_dir=work_dir)
        if not block:
            return f"Block '{block_id}' not found in index."

        lines = [
            f"--- Block: {block.block_id} ---",
            f"Source: {block.source_path}",
            f"Country/ISO: {block.country} ({block.iso_code})",
            f"Reasoning: {block.reasoning}",
            f"Enrichment Provider: {block.enrichment_provider}",
            f"Enrichment Model: {block.enrichment_model}",
            f"Enriched At: {block.enriched_at}",
            f"Answer Signal: {block.answer_signal}",
            f"Tags: {', '.join(block.sender_types + block.regulation_topics)}",
            f"Local Aliases: {', '.join(block.local_aliases)}",
            "",
            "Hypothetical Questions:",
        ]
        for q in block.hypothetical_questions:
            lines.append(f"  ? {q}")
            
        lines.extend([
            "",
            "Enriched Text:",
            block.enriched_text or "(Empty)",
            "",
            "Raw Text:",
            block.text[:500] + ("..." if len(block.text) > 500 else "")
        ])
        return "\n".join(lines)

    def ask(self, question: str, work_dir: Path | None = None, top_k: int | None = None) -> str:
        answer = self.answer(question=question, work_dir=work_dir, top_k=top_k)
        return answer.answer

    @staticmethod
    def _embedding_text(block: KnowledgeBlock) -> str:
        # High-entropy retrieval targets
        structured_value = block.metadata.get("structured_value", "").strip()
        row_value = KnowledgePipeline._row_value_for_retrieval(block.metadata.get("row_values", ""))
        main_content = structured_value or row_value or block.enriched_text or block.text
        questions = " ".join(block.hypothetical_questions)
        tags = ", ".join(
            sorted(
                list(
                    set(
                        block.sender_types
                        + block.regulation_topics
                        + block.canonical_terms
                    )
                )
            )
        )
        aliases = ", ".join(block.local_aliases)
        
        # Weighted concatenation
        return f"{main_content} | Questions: {questions} | Tags: {tags} | Aliases: {aliases}"

    @staticmethod
    def _row_value_for_retrieval(row_values: str) -> str:
        for part in [item.strip() for item in row_values.split(";") if item.strip()]:
            if "=" not in part:
                continue
            label, value = [item.strip() for item in part.split("=", 1)]
            if label.lower() == "value" and value.lower() not in {"", "n/a", "---", "-----", "/", "unknown", "null"}:
                return value
        return ""

    @staticmethod
    def _dedupe_duplicate_of(block: KnowledgeBlock, seen_hashes: set[str]) -> str:
        fingerprint = KnowledgePipeline._block_dedupe_hash(block)
        if fingerprint in seen_hashes:
            return fingerprint
        seen_hashes.add(fingerprint)
        return ""

    @staticmethod
    def _document_code_blocks_preserved(blocks: list[KnowledgeBlock]) -> int:
        for block in blocks:
            value = block.metadata.get("code_blocks_preserved")
            if value:
                try:
                    return int(value)
                except ValueError:
                    return 0
        return 0

    @staticmethod
    def _document_code_blocks_erased(blocks: list[KnowledgeBlock]) -> int:
        for block in blocks:
            value = block.metadata.get("code_blocks_erased")
            if value:
                try:
                    return int(value)
                except ValueError:
                    return 0
        return 0

    @staticmethod
    def _encoding_fallback_record(document: ParsedDocument) -> dict[str, object]:
        return {
            "file": document.source_path,
            "encoding_detected": document.encoding_detected,
            "encoding_confidence": document.encoding_confidence,
            "warnings": document.parse_warnings,
        }

    @staticmethod
    def _block_dedupe_hash(block: KnowledgeBlock) -> str:
        normalized_text = " ".join(block.text.casefold().split())
        country_scope = (block.iso_code or block.country or block.metadata.get("tag_iso_code", "")).strip().casefold()
        section_scope = " > ".join(part.strip().casefold() for part in block.section_path if part.strip())
        block_type = block.block_type.strip().casefold()
        digest = sha256()
        digest.update(country_scope.encode("utf-8"))
        digest.update(b"\0")
        digest.update(section_scope.encode("utf-8"))
        digest.update(b"\0")
        digest.update(block_type.encode("utf-8"))
        digest.update(b"\0")
        digest.update(normalized_text.encode("utf-8"))
        return digest.hexdigest()

    def answer(
        self,
        question: str,
        work_dir: Path | None = None,
        top_k: int | None = None,
    ) -> Answer:
        work_dir = work_dir or self._settings.work_dir
        manifest = self._load_manifest(work_dir)
        retriever = self._load_retriever(work_dir)
        return self._answer_with_cache(
            question=question,
            work_dir=work_dir,
            retriever=retriever,
            manifest=manifest,
            top_k=top_k if top_k is not None else self._settings.top_k,
        )

    def evaluate(
        self,
        benchmark_path: Path,
        work_dir: Path | None = None,
        top_k: int | None = None,
    ) -> EvaluationSummary:
        work_dir = work_dir or self._settings.work_dir
        manifest = self._load_manifest(work_dir)
        retriever = self._load_retriever(work_dir)
        cases = self._evaluator.load_cases(benchmark_path)
        summary = self._evaluator.evaluate(
            cases,
            lambda question: self._run_case(
                question,
                work_dir,
                retriever,
                manifest,
                top_k if top_k is not None else self._settings.top_k,
            ),
        )
        output_path = work_dir / "evaluation" / "latest-evaluation.json"
        self._evaluator.save_summary(summary, output_path)
        return summary

    def calibrate_refusal(
        self,
        benchmark_path: Path,
        work_dir: Path | None = None,
        top_k: int | None = None,
    ) -> CalibrationReport:
        work_dir = work_dir or self._settings.work_dir
        retriever = self._load_retriever(work_dir)
        cases = self._evaluator.load_cases(benchmark_path)
        report = self._calibrator.calibrate(
            cases=cases,
            search=retriever.search,
            top_k=top_k if top_k is not None else self._settings.top_k,
        )
        output_path = work_dir / "evaluation" / "refusal-calibration.json"
        self._calibrator.save_report(report, output_path)
        return report

    def audit_knowledge(self, work_dir: Path | None = None) -> Path:
        work_dir = work_dir or self._settings.work_dir
        analytics = KnowledgeAnalytics(work_dir)
        metrics = analytics.audit_quality()
        report_path = generate_ds_report(metrics, work_dir)
        return report_path

    def check_consistency(self, work_dir: Path | None = None) -> Path:
        work_dir = work_dir or self._settings.work_dir
        analytics = KnowledgeAnalytics(work_dir)
        report = analytics.audit_cross_section_consistency()
        report_path = generate_consistency_report(report, work_dir)
        return report_path

    def build_review_packets(
        self,
        work_dir: Path | None = None,
        document_id: str | None = None,
    ) -> list[Path]:
        work_dir = work_dir or self._settings.work_dir
        analytics = KnowledgeAnalytics(work_dir)
        report = analytics.build_review_packets(document_id=document_id)
        return [Path(path) for path in report.packet_paths]

    def seed_review_findings(self, work_dir: Path | None = None) -> Path:
        work_dir = work_dir or self._settings.work_dir
        analytics = KnowledgeAnalytics(work_dir)
        report = analytics.audit_cross_section_consistency()
        return seed_review_findings(report, work_dir)

    def export_review_benchmark(
        self,
        review_findings_path: Path,
        output_path: Path,
    ) -> list:
        return export_review_findings_benchmark(review_findings_path, output_path)

    def _load_retriever(self, work_dir: Path) -> HybridRetriever:
        cache_key = str(work_dir.resolve())
        manifest_mtime = self._manifest_mtime(work_dir)
        cached = self._retriever_cache.get(cache_key)
        if cached is not None:
            if cached.manifest_mtime == manifest_mtime and manifest_mtime <= cached.loaded_at:
                self._retriever_cache.move_to_end(cache_key)
                return cached.retriever
            self._retriever_cache.pop(cache_key, None)

        blocks_payload = json.loads((work_dir / "blocks.json").read_text(encoding="utf-8"))
        for payload in blocks_payload:
            payload.setdefault("section_heading", "")
        blocks = [KnowledgeBlock(**payload) for payload in blocks_payload]
        lexical = BM25Index(blocks)
        retrieval_settings = self._retrieval_settings_for_index(work_dir)
        vector = load_vector_store(retrieval_settings, work_dir)
        embedding_model = EmbeddingModel(retrieval_settings)
        reranker = build_reranker(retrieval_settings)

        # Build country-name → ISO-code lookup from block tags written at index time.
        # Blocks without tag_iso_code (pre-redesign index) degrade gracefully to full search.
        country_index = build_country_index()
        for block in blocks:
            augment_country_index(
                country_index,
                block.country or block.metadata.get("tag_country", ""),
                block.iso_code or block.metadata.get("tag_iso_code", ""),
            )

        retriever = HybridRetriever(
            lexical,
            vector,
            embedding_model,
            reranker=reranker,
            all_blocks=blocks,
            country_index=country_index,
            rrf_lexical_weight=retrieval_settings.rrf_lexical_weight,
            rrf_vector_weight=retrieval_settings.rrf_vector_weight,
            arm_k_multiplier=retrieval_settings.arm_k_multiplier,
            max_blocks_per_document=retrieval_settings.max_blocks_per_document,
        )
        loaded_at = time.time()
        self._retriever_cache[cache_key] = RetrieverCacheEntry(
            retriever=retriever,
            loaded_at=loaded_at,
            manifest_mtime=manifest_mtime,
        )
        self._retriever_cache.move_to_end(cache_key)
        while len(self._retriever_cache) > self.RETRIEVER_CACHE_SIZE:
            self._retriever_cache.popitem(last=False)
        return retriever

    @staticmethod
    def _manifest_mtime(work_dir: Path) -> float:
        manifest_path = work_dir / "manifest.json"
        if not manifest_path.exists():
            return 0.0
        return manifest_path.stat().st_mtime

    def _retrieval_settings_for_index(self, work_dir: Path) -> Settings:
        manifest_path = work_dir / "manifest.json"
        if not manifest_path.exists():
            return self._settings
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        return self._settings.model_copy(
            update={
                "embedding_provider": manifest.get("embedding_provider", self._settings.embedding_provider),
                "embedding_model": manifest.get("embedding_model", self._settings.embedding_model),
                "embedding_device": manifest.get("embedding_device", self._settings.embedding_device),
                "embedding_dimensions": manifest.get("embedding_dimensions", self._settings.embedding_dimensions),
                "vector_backend": manifest.get("vector_backend", self._settings.vector_backend),
                "vector_collection": manifest.get("vector_collection", self._settings.vector_collection),
                "qdrant_url": manifest.get("qdrant_url", self._settings.qdrant_url),
                "reranker_provider": manifest.get("reranker_provider", self._settings.reranker_provider),
                "reranker_model": manifest.get("reranker_model", self._settings.reranker_model),
                "reranker_top_n": manifest.get("reranker_top_n", self._settings.reranker_top_n),
                "rrf_lexical_weight": manifest.get("rrf_lexical_weight", self._settings.rrf_lexical_weight),
                "rrf_vector_weight": manifest.get("rrf_vector_weight", self._settings.rrf_vector_weight),
                "arm_k_multiplier": manifest.get("arm_k_multiplier", self._settings.arm_k_multiplier),
                "max_blocks_per_document": manifest.get(
                    "max_blocks_per_document",
                    self._settings.max_blocks_per_document,
                ),
            }
        )

    @staticmethod
    def _load_manifest(work_dir: Path) -> dict[str, object]:
        path = work_dir / "manifest.json"
        if not path.exists():
            return {}
        payload = json.loads(path.read_text(encoding="utf-8"))
        return payload if isinstance(payload, dict) else {}

    @staticmethod
    def _load_documents_index(work_dir: Path) -> dict[str, ParsedDocument]:
        path = work_dir / "documents.json"
        if not path.exists():
            return {}
        payload = json.loads(path.read_text(encoding="utf-8"))
        return {
            item["document_id"]: ParsedDocument(**item)
            for item in payload
        }

    @staticmethod
    def _load_block_vector_index(
        work_dir: Path,
    ) -> tuple[dict[str, list[KnowledgeBlock]], dict[str, list[list[float]]]]:
        path = vector_store_snapshot_path(work_dir)
        if not path.exists():
            return {}, {}
        payload = json.loads(path.read_text(encoding="utf-8"))
        blocks_by_document: dict[str, list[KnowledgeBlock]] = {}
        vectors_by_document: dict[str, list[list[float]]] = {}
        for item, vector in zip(payload.get("blocks", []), payload.get("vectors", []), strict=False):
            item.setdefault("section_heading", "")
            block = KnowledgeBlock(**item)
            blocks_by_document.setdefault(block.document_id, []).append(block)
            vectors_by_document.setdefault(block.document_id, []).append(vector)
        return blocks_by_document, vectors_by_document

    def _can_reuse_previous_index(
        self,
        previous_manifest: dict[str, object],
        allowed_suffixes: list[str] | tuple[str, ...] | set[str] | None = None,
    ) -> bool:
        previous_suffixes = previous_manifest.get("allowed_suffixes", [])
        return (
            list(normalize_allowed_suffixes(previous_suffixes if isinstance(previous_suffixes, list) else []))
            == list(normalize_allowed_suffixes(allowed_suffixes))
            and
            previous_manifest.get("normalizer_schema_version") == NORMALIZER_SCHEMA_VERSION
            and previous_manifest.get("parser_schema_version") == PARSER_SCHEMA_VERSION
            and
            previous_manifest.get("chunk_size") == self._settings.chunk_size
            and previous_manifest.get("chunk_overlap") == self._settings.chunk_overlap
            and previous_manifest.get("mapping_provider") == self._settings.mapping_provider
            and previous_manifest.get("mapping_model") == self._settings.mapping_model
            and previous_manifest.get("mapping_batch_size") == self._settings.mapping_batch_size
            and previous_manifest.get("mapping_batch_delay_ms") == self._settings.mapping_batch_delay_ms
            and previous_manifest.get("mapping_text_char_limit") == self._settings.mapping_text_char_limit
            and previous_manifest.get("mapping_prompt_mode") == self._settings.mapping_prompt_mode
            and previous_manifest.get("mapping_retry_missing_results") == self._settings.mapping_retry_missing_results
            and previous_manifest.get("embedding_provider") == self._settings.embedding_provider
            and previous_manifest.get("embedding_model") == self._settings.embedding_model
            and previous_manifest.get("embedding_device") == self._settings.embedding_device
            and previous_manifest.get("embedding_dimensions") == self._settings.embedding_dimensions
            and previous_manifest.get("vector_backend") == self._settings.vector_backend
            and previous_manifest.get("vector_collection") == self._settings.vector_collection
            and previous_manifest.get("qdrant_url") == self._settings.qdrant_url
            and previous_manifest.get("reranker_provider") == self._settings.reranker_provider
            and previous_manifest.get("reranker_model") == self._settings.reranker_model
            and previous_manifest.get("reranker_top_n") == self._settings.reranker_top_n
            and previous_manifest.get("rrf_lexical_weight") == self._settings.rrf_lexical_weight
            and previous_manifest.get("rrf_vector_weight") == self._settings.rrf_vector_weight
            and previous_manifest.get("arm_k_multiplier") == self._settings.arm_k_multiplier
            and previous_manifest.get("max_blocks_per_document") == self._settings.max_blocks_per_document
        )

    @staticmethod
    def _merge_enrichment_caches(*work_dirs: Path) -> None:
        if len(work_dirs) < 2:
            return
        target = work_dirs[-1] / "enrichment-cache.json"
        merged: dict[str, object] = {}
        for work_dir in work_dirs[:-1]:
            path = work_dir / "enrichment-cache.json"
            if not path.exists():
                continue
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                continue
            if isinstance(payload, dict):
                merged.update(payload)
        if merged:
            target.write_text(json.dumps(merged, indent=2), encoding="utf-8")

    @staticmethod
    def _source_fingerprints(
        source_dir: Path,
        allowed_suffixes: list[str] | tuple[str, ...] | set[str] | None = None,
        max_file_bytes: int | None = None,
    ) -> tuple[list[tuple[Path, str]], list[dict[str, object]]]:
        fingerprints: list[tuple[Path, str]] = []
        skipped_files: list[dict[str, object]] = []
        for path in sorted(source_dir.rglob("*")):
            if not can_parse_file(path, allowed_suffixes):
                continue
            file_size = path.stat().st_size
            if max_file_bytes is not None and max_file_bytes > 0 and file_size > max_file_bytes:
                skipped_files.append(
                    {
                        "file": str(path),
                        "reason": "file_too_large",
                        "size_bytes": file_size,
                        "max_file_bytes": max_file_bytes,
                    }
                )
                continue
            fingerprints.append((path, KnowledgePipeline._fingerprint_file(path)))
        return fingerprints, skipped_files

    @staticmethod
    def _fingerprint_file(path: Path) -> str:
        digest = sha256()
        digest.update(path.suffix.lower().encode("utf-8"))
        digest.update(path.read_bytes())
        return digest.hexdigest()

    def _run_case(
        self,
        question: str,
        work_dir: Path,
        retriever: HybridRetriever,
        manifest: dict[str, object],
        top_k: int,
    ) -> tuple[list[SearchHit], Answer]:
        answer = self._answer_with_cache(
            question=question,
            work_dir=work_dir,
            retriever=retriever,
            manifest=manifest,
            top_k=top_k,
        )
        return answer.evidence, answer

    def _answer_with_cache(
        self,
        *,
        question: str,
        work_dir: Path,
        retriever: HybridRetriever,
        manifest: dict[str, object],
        top_k: int,
    ) -> Answer:
        cache_key = query_cache_key(
            question=question,
            top_k=top_k,
            settings=self._settings,
            manifest=manifest,
        )
        if self._settings.query_cache_enabled:
            cache = load_query_cache(work_dir)
            cached_payload = cache.get(cache_key)
            if isinstance(cached_payload, dict):
                cached_answer = deserialize_answer(cached_payload)
                if self._cached_answer_matches_index(cached_answer, retriever):
                    return cached_answer
                cache.pop(cache_key, None)
                save_query_cache(work_dir, cache)
        else:
            cache = {}

        hits = retriever.search(question, top_k=top_k)
        answer = self._answerer.answer(question, hits)
        answer = self._enforce_country_alignment(question, retriever, answer)
        if self._settings.query_cache_enabled and should_cache_answer(answer):
            cache[cache_key] = serialize_answer(answer)
            save_query_cache(work_dir, cache)
        return answer

    @staticmethod
    def _cached_answer_matches_index(answer: Answer, retriever: HybridRetriever) -> bool:
        if not answer.evidence:
            return True
        indexed_block_ids = {block.block_id for block in retriever._all_blocks}
        return all(hit.block.block_id in indexed_block_ids for hit in answer.evidence)

    def _enforce_country_alignment(
        self,
        question: str,
        retriever: HybridRetriever,
        answer: Answer,
    ) -> Answer:
        filters = extract_query_filters(question, getattr(retriever, "_country_index", {}))
        if not filters.iso_codes or not answer.evidence:
            return answer

        matching_evidence = [
            hit for hit in answer.evidence
            if (
                hit.block.iso_code
                or hit.block.metadata.get("tag_iso_code", "")
                or retriever._block_iso(hit.block)
            ).strip().upper()
            in filters.iso_codes
        ]
        if matching_evidence:
            return answer

        return Answer(
            question=answer.question,
            answer="Insufficient evidence in the indexed knowledge base for the requested country.",
            confidence="low",
            evidence=[],
            tier="refusal",
            query_intent=answer.query_intent,
            cached=answer.cached,
        )
