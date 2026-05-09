import hashlib
import json
import shutil
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from own_knowledge_rag.config import Settings
from own_knowledge_rag.benchmark_audit import audit_benchmark
from own_knowledge_rag.benchmark_generation import export_query_reviews_benchmark, export_review_findings_benchmark
from own_knowledge_rag.filename_metadata import build_country_index
from own_knowledge_rag.pipeline import BuildLockError, KnowledgePipeline
from own_knowledge_rag.gui import render_gui
from own_knowledge_rag.analytics import query_reviews_path, record_query_review
from own_knowledge_rag.model_probe import ModelProbeResult, probe_provider_models
from own_knowledge_rag.experiments import (
    compare_experiments,
    clear_experiments_registry,
    experiment_sources_alignment,
    experiments_registry_path,
    load_experiments_registry,
    promote_experiment_workspace,
    promote_experiment_sources,
    rollback_baseline_workspace,
    save_experiment_record,
    stage_experiment_files,
    suggest_experiment_layout,
)
from own_knowledge_rag.parsers import can_parse_file, normalize_allowed_suffixes, normalize_json_text_for_ingestion
from own_knowledge_rag.query_router import extract_query_filters

_PROSE_SOURCE_INGESTION_PROMPT_PATH = Path(__file__).parents[2] / "docs" / "internal" / "prose_source_ingestion_enrichment_prompt.md"
_FAQ_QA_SOURCE_FACT_INGESTION_PROMPT_PATH = Path(__file__).parents[2] / "docs" / "internal" / "faq_qa_source_fact_ingestion_prompt.md"
_SOURCE_FACT_TEMPLATE_PATH = Path(__file__).parents[2] / "data" / "raw" / "_templates" / "source_fact_template.json"
_QA_SEED_TEMPLATE_PATH = Path(__file__).parents[2] / "data" / "raw" / "_templates" / "qa_seed_template.json"
_QA_SEED_GENERATION_PROMPT_PATH = Path(__file__).parents[2] / "docs" / "internal" / "qa_seed_generation_prompt.md"
_QA_SEED_GENERATION_PROMPT_FALLBACK = """# QA Seed Generation Prompt

Use the REVIEWED Q/A TEXT FILE and SOURCE FACT JSON to draft benchmark-ready Q&A seeds.

Return only RECOMMENDED_QA_SEED_JSON with accepted seeds that preserve source fact IDs,
expected document IDs, expected metadata, expected terms, and review status.
"""
_STATIC_DIR = Path(__file__).parent / "static"


class HealthResponse(BaseModel):
    status: str
    app: str


class BuildIndexRequest(BaseModel):
    source_dir: str | None = None
    work_dir: str | None = None
    allowed_suffixes: list[str] | None = None
    allow_low_quality: bool = False
    force_reenrich: bool = False
    chunk_size: int | None = Field(default=None, ge=100)
    chunk_overlap: int | None = Field(default=None, ge=0)
    mapping_provider: str | None = None
    mapping_model: str | None = None
    mapping_batch_size: int | None = Field(default=None, ge=1)
    mapping_batch_delay_ms: int | None = Field(default=None, ge=0)
    mapping_text_char_limit: int | None = Field(default=None, ge=100)
    mapping_prompt_mode: str | None = None
    mapping_retry_missing_results: bool | None = None
    embedding_provider: str | None = None
    embedding_model: str | None = None
    embedding_device: str | None = None
    embedding_dimensions: int | None = Field(default=None, ge=1)
    vector_backend: str | None = None
    vector_collection: str | None = None
    qdrant_url: str | None = None
    reranker_provider: str | None = None
    reranker_model: str | None = None
    reranker_top_n: int | None = Field(default=None, ge=1)


class BuildIndexResponse(BaseModel):
    documents: int
    blocks: int
    total_time: float = 0
    reused_documents: int
    rebuilt_documents: int
    reused_baseline_documents: int = 0
    replaced_documents: int = 0
    added_documents: int = 0
    allowed_suffixes: list[str]
    chunk_size: int
    chunk_overlap: int
    mapping_provider: str
    mapping_model: str
    mapping_batch_size: int
    mapping_batch_delay_ms: int
    mapping_text_char_limit: int
    mapping_prompt_mode: str
    mapping_retry_missing_results: bool
    embedding_provider: str
    embedding_model: str
    embedding_device: str
    embedding_dimensions: int | None = None
    vector_backend: str
    vector_collection: str
    qdrant_url: str
    reranker_provider: str
    reranker_model: str
    reranker_top_n: int


class BuildLockRequest(BaseModel):
    work_dir: str | None = None


class BuildLockResponse(BaseModel):
    locked: bool
    path: str
    stale: bool = False
    reason: str = ""
    pid: int | None = None
    source_dir: str = ""
    work_dir: str = ""
    allowed_suffixes: list[str] = Field(default_factory=list)
    started_at: int | None = None
    age_seconds: int | None = None


class AnswerRequest(BaseModel):
    question: str = Field(min_length=3)
    work_dir: str | None = None
    top_k: int | None = Field(default=None, ge=0, le=10)


class EvidenceResponse(BaseModel):
    block_id: str
    document_id: str
    title: str
    section_path: list[str]
    block_type: str
    source_path: str
    start_anchor: str
    end_anchor: str
    text: str
    enriched_text: str
    score: float
    lexical_score: float
    vector_score: float


class AnswerResponse(BaseModel):
    question: str
    answer: str
    confidence: str
    tier: str
    query_intent: str
    cached: bool
    work_dir: str
    evidence: list[EvidenceResponse]


class QueryReviewRequest(BaseModel):
    work_dir: str | None = None
    question: str = Field(min_length=3)
    answer: str = Field(min_length=1)
    confidence: str = ""
    tier: str = ""
    query_intent: str = ""
    cached: bool = False
    rating: str = Field(min_length=3)
    expected_document_id: str = ""
    expected_iso_code: str = ""
    expected_terms: list[str] = Field(default_factory=list)
    notes: str = ""
    evidence_document_ids: list[str] = Field(default_factory=list)
    evidence_block_ids: list[str] = Field(default_factory=list)


class QueryReviewResponse(BaseModel):
    saved: bool
    path: str
    review_count: int


class HumanReviewReadinessCheck(BaseModel):
    name: str
    value: int
    target: int
    status: str


class HumanReviewQualityWarning(BaseModel):
    review_id: str
    severity: str
    message: str


class HumanReviewCollectionPrompt(BaseModel):
    target: str
    label: str
    question: str
    rating_hint: str
    notes: str = ""


class HumanReviewReadinessResponse(BaseModel):
    work_dir: str
    query_reviews_path: str
    review_findings_path: str
    query_reviews_found: bool
    review_findings_found: bool
    total_query_reviews: int
    rating_counts: dict[str, int] = Field(default_factory=dict)
    should_refuse_count: int
    foreign_or_wrong_country_count: int
    multi_fact_or_comparison_count: int
    review_findings_count: int
    accepted_review_findings_count: int
    quality_warnings: list[HumanReviewQualityWarning] = Field(default_factory=list)
    thresholds: dict[str, int] = Field(default_factory=dict)
    checks: list[HumanReviewReadinessCheck] = Field(default_factory=list)
    missing_targets: list[str] = Field(default_factory=list)
    collection_prompts: list[HumanReviewCollectionPrompt] = Field(default_factory=list)
    ready_for_export: bool
    gate_mode: str
    proposed_outputs: list[str] = Field(default_factory=list)
    message: str


class HumanReviewExportRequest(BaseModel):
    work_dir: str | None = None
    output_dir: str = "benchmarks"
    allow_undercovered: bool = False


class HumanReviewExportResponse(BaseModel):
    exported: bool
    query_review_benchmark_path: str = ""
    query_review_cases: int = 0
    review_findings_benchmark_path: str = ""
    review_findings_cases: int = 0
    readiness: HumanReviewReadinessResponse
    message: str


class EvaluateRequest(BaseModel):
    benchmark_path: str
    work_dir: str | None = None
    top_k: int | None = Field(default=None, ge=0, le=10)


class GateRunRequest(BaseModel):
    benchmark_path: str
    work_dir: str | None = None
    top_k: int | None = Field(default=None, ge=0, le=10)
    min_cases: int = Field(default=10, ge=1)
    allow_low_count: list[str] = Field(default_factory=lambda: ["sender_type:toll-free number"])
    disable_query_cache: bool = True


class CalibrateRequest(BaseModel):
    benchmark_path: str
    work_dir: str | None = None
    top_k: int | None = Field(default=None, ge=0, le=10)


class RuntimeDefaultsResponse(BaseModel):
    source_dir: str
    work_dir: str
    allowed_suffixes: list[str]
    top_k: int
    query_cache_enabled: bool
    api_host: str
    api_port: int
    chunk_size: int
    chunk_overlap: int
    mapping_provider: str
    mapping_model: str
    mapping_batch_size: int
    mapping_batch_delay_ms: int
    mapping_text_char_limit: int
    mapping_prompt_mode: str
    mapping_retry_missing_results: bool
    embedding_provider: str
    embedding_model: str
    embedding_device: str
    embedding_dimensions: int | None = None
    vector_backend: str
    vector_collection: str
    qdrant_url: str
    reranker_provider: str
    reranker_model: str
    reranker_top_n: int


class BenchmarkPresetResponse(BaseModel):
    name: str
    path: str
    cases: int
    description: str


class RuntimeTestingResponse(BaseModel):
    source_dir_exists: bool
    work_dir_exists: bool
    index_available: bool
    latest_evaluation_available: bool
    latest_calibration_available: bool
    benchmark_presets: list[BenchmarkPresetResponse]
    sample_questions: list[str]


class ModelProbeResponse(BaseModel):
    enabled: bool
    status: str
    checked_models: dict[str, str] = Field(default_factory=dict)
    available_models: list[str] = Field(default_factory=list)
    message: str = ""


class BaselineStatusResponse(BaseModel):
    baseline_work_dir: str
    promoted_baseline: bool
    exists: bool
    index_ready: bool
    documents: int = 0
    blocks: int = 0
    modified_at: int = 0
    rollback_backup_count: int = 0
    latest_rollback_backup: dict[str, object] | None = None


class IndexedCorpusResponse(BaseModel):
    available: bool
    documents: int = 0
    blocks: int = 0
    manifest_path: str = ""
    manifest_modified_at: int = 0
    index_id: str = ""
    document_ids_sample: list[str] = Field(default_factory=list)
    reused_documents: int = 0
    rebuilt_documents: int = 0
    allowed_suffixes: list[str] = Field(default_factory=list)
    mapping_provider: str = ""
    mapping_model: str = ""
    mapping_batch_size: int = 0
    mapping_batch_delay_ms: int = 0
    mapping_text_char_limit: int = 0
    mapping_prompt_mode: str = ""
    mapping_retry_missing_results: bool = False
    embedding_provider: str = ""
    embedding_model: str = ""
    embedding_device: str = ""
    embedding_dimensions: int | None = None
    vector_backend: str = ""
    vector_collection: str = ""
    qdrant_url: str = ""
    reranker_provider: str = ""
    reranker_model: str = ""
    reranker_top_n: int = 0
    chunk_size: int = 0
    chunk_overlap: int = 0
    generation_provider: str = ""
    generation_model: str = ""
    tier0_score_threshold: float = 0.0
    tier2_score_threshold: float = 0.0
    semantic_status_counts: dict[str, int] = Field(default_factory=dict)
    semantic_intent_counts: dict[str, int] = Field(default_factory=dict)


class ExplainBlockRequest(BaseModel):
    block_id: str
    work_dir: str | None = None


class ExplainBlockResponse(BaseModel):
    block_id: str
    document_id: str
    title: str
    section_path: list[str]
    block_type: str
    text: str
    enriched_text: str
    enrichment_provider: str
    enrichment_model: str
    enriched_at: str
    hypothetical_questions: list[str]
    local_aliases: list[str]
    reasoning: str
    answer_signal: str
    quality_status: str
    canonical_terms: list[str]
    metadata: dict[str, str]


class LowQualityBlocksRequest(BaseModel):
    work_dir: str | None = None
    limit: int = Field(default=50, ge=1, le=250)
    include_accepted: bool = False


class ExperimentClearRegistryRequest(BaseModel):
    delete_workspaces: bool = False


class ExperimentCreateRequest(BaseModel):
    source_dir: str | None = None
    experiment_source_dir: str | None = None
    experiment_work_dir: str | None = None
    baseline_work_dir: str | None = None
    benchmark_path: str | None = None
    content_type: str = "documents"
    hypothesis: str = ""
    notes: str = ""


class ExperimentCreateResponse(BaseModel):
    experiment_id: str
    registry_path: str
    experiment_source_dir: str
    experiment_work_dir: str
    baseline_work_dir: str
    benchmark_path: str
    status: str


class ExperimentBuildRequest(BuildIndexRequest):
    source_dir: str | None = None
    experiment_source_dir: str | None = None
    experiment_work_dir: str | None = None
    baseline_work_dir: str | None = None
    benchmark_path: str | None = None
    merge_with_baseline: bool = False
    content_type: str = "documents"
    hypothesis: str = ""
    notes: str = ""


class ExperimentEvaluateRequest(BaseModel):
    experiment_work_dir: str = Field(min_length=3)
    baseline_work_dir: str | None = None
    benchmark_path: str | None = None
    top_k: int | None = Field(default=None, ge=0, le=10)
    content_type: str = "documents"
    hypothesis: str = ""
    notes: str = ""


class ExperimentCompareRequest(BaseModel):
    experiment_work_dir: str = Field(min_length=3)
    baseline_work_dir: str | None = None
    benchmark_path: str | None = None
    top_k: int | None = Field(default=None, ge=0, le=10)
    content_type: str = "documents"
    hypothesis: str = ""
    notes: str = ""


class ExperimentPromoteRequest(BaseModel):
    experiment_work_dir: str = Field(min_length=3)
    baseline_work_dir: str
    experiment_source_dir: str | None = None
    source_dir: str | None = None
    force_promote_without_sources: bool = False
    benchmark_path: str | None = None
    content_type: str = "documents"
    hypothesis: str = ""
    notes: str = ""


class ExperimentPromoteSourcesRequest(BaseModel):
    experiment_source_dir: str = Field(min_length=3)
    source_dir: str | None = None
    experiment_work_dir: str | None = None
    baseline_work_dir: str | None = None
    benchmark_path: str | None = None
    content_type: str = "documents"
    hypothesis: str = ""
    notes: str = ""


class ExperimentRollbackRequest(BaseModel):
    baseline_work_dir: str = Field(min_length=3)
    backup_work_dir: str = Field(min_length=3)
    experiment_work_dir: str | None = None
    content_type: str = "documents"
    hypothesis: str = ""
    notes: str = ""


class ExperimentSuggestRequest(BaseModel):
    hypothesis: str = ""


class ExperimentUploadFile(BaseModel):
    name: str = Field(min_length=1)
    content: str = ""


class ExperimentUploadRequest(BaseModel):
    experiment_source_dir: str | None = None
    hypothesis: str = ""
    files: list[ExperimentUploadFile] = Field(default_factory=list)


def _repair_upload_file_if_needed(file: ExperimentUploadFile) -> dict[str, str]:
    content = file.content
    if Path(file.name).suffix.lower() == ".json":
        content = normalize_json_text_for_ingestion(content)
    return {"name": file.name, "content": content}


class KnowledgeTemplateResponse(BaseModel):
    source_fact_template: str
    qa_seed_template: str
    qa_seed_generation_prompt: str
    source_fact_template_path: str
    qa_seed_template_path: str
    qa_seed_generation_prompt_path: str


class KnowledgeQaSeedExportRequest(BaseModel):
    qa_seed_content: str = Field(min_length=2)
    source_fact_content: str = ""
    output_path: str = "benchmarks/qa_seed_regressions.json"
    allow_pending: bool = True


class KnowledgeQaSeedExportResponse(BaseModel):
    exported: bool
    output_path: str
    case_count: int
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    source_fact_ids: list[str] = Field(default_factory=list)
    cases: list[dict[str, object]] = Field(default_factory=list)


class RuntimeResponse(BaseModel):
    defaults: RuntimeDefaultsResponse
    indexed: IndexedCorpusResponse
    testing: RuntimeTestingResponse
    model_probe: ModelProbeResponse


def _load_manifest(work_dir: Path) -> dict[str, object]:
    path = work_dir / "manifest.json"
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def _load_blocks_payload(work_dir: Path) -> list[dict[str, object]]:
    path = work_dir / "blocks.json"
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        return []
    return [item for item in payload if isinstance(item, dict)]


def _manifest_modified_at(work_dir: Path) -> int:
    path = work_dir / "manifest.json"
    return int(path.stat().st_mtime) if path.exists() else 0


def _manifest_index_id(manifest: dict[str, object]) -> str:
    if not manifest:
        return ""
    documents_state = manifest.get("documents_state", {})
    payload = {
        "documents": manifest.get("documents", 0),
        "blocks": manifest.get("blocks", 0),
        "documents_state": documents_state if isinstance(documents_state, dict) else {},
        "parser_schema_version": manifest.get("parser_schema_version", ""),
        "normalizer_schema_version": manifest.get("normalizer_schema_version", ""),
        "mapping_provider": manifest.get("mapping_provider", ""),
        "mapping_model": manifest.get("mapping_model", ""),
        "embedding_provider": manifest.get("embedding_provider", ""),
        "embedding_model": manifest.get("embedding_model", ""),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()[:12]


def _manifest_document_ids_sample(manifest: dict[str, object], limit: int = 5) -> list[str]:
    documents_state = manifest.get("documents_state", {})
    if not isinstance(documents_state, dict):
        return []
    return sorted(str(document_id) for document_id in documents_state.keys())[:limit]


def _count_benchmark_cases(path: Path) -> int:
    if not path.exists():
        return 0
    payload = json.loads(path.read_text(encoding="utf-8"))
    return len(payload) if isinstance(payload, list) else 0


def _json_from_text(raw: str, *, label: str) -> object:
    try:
        return json.loads(raw)
    except json.JSONDecodeError as error:
        raise HTTPException(status_code=400, detail=f"{label} is not valid JSON: {error}") from error


def _source_fact_ids_from_payload(payload: object) -> set[str]:
    if not isinstance(payload, dict):
        return set()
    source_facts = payload.get("source_facts")
    if not isinstance(source_facts, list):
        return set()
    fact_ids: set[str] = set()
    for item in source_facts:
        if not isinstance(item, dict):
            continue
        fact_id = str(item.get("fact_id", "")).strip()
        if fact_id:
            fact_ids.add(fact_id)
    return fact_ids


def _qa_seed_items(payload: object) -> list[dict[str, object]]:
    if isinstance(payload, dict):
        seeds = payload.get("qa_seeds")
        if isinstance(seeds, list):
            return [item for item in seeds if isinstance(item, dict)]
        if {"question", "expected_terms"}.intersection(payload.keys()):
            return [payload]
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    return []


def _list_of_strings(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        return [item.strip() for item in value.split("|") if item.strip()]
    return []


def _qa_seed_cases_from_payload(
    *,
    qa_seed_payload: object,
    source_fact_ids: set[str],
    allow_pending: bool,
) -> tuple[list[dict[str, object]], list[str], list[str]]:
    seeds = _qa_seed_items(qa_seed_payload)
    warnings: list[str] = []
    errors: list[str] = []
    cases: list[dict[str, object]] = []
    if not seeds:
        errors.append("No qa_seeds were found.")
        return cases, warnings, errors

    for index, seed in enumerate(seeds, start=1):
        seed_id = str(seed.get("seed_id") or f"qa-seed-{index:03d}").strip()
        review_status = str(seed.get("review_status") or "").strip().lower()
        if review_status in {"rejected", "reject"}:
            warnings.append(f"{seed_id}: skipped rejected seed.")
            continue
        if review_status in {"pending", ""} and not allow_pending:
            warnings.append(f"{seed_id}: skipped pending seed because allow_pending=false.")
            continue

        question = str(seed.get("question", "")).strip()
        expected_document_ids = _list_of_strings(seed.get("expected_document_ids"))
        expected_terms = _list_of_strings(seed.get("expected_terms"))
        expected_anchor_terms = _list_of_strings(seed.get("expected_anchor_terms"))
        expected_metadata = seed.get("expected_metadata") if isinstance(seed.get("expected_metadata"), dict) else {}
        source_fact_id = str(seed.get("source_fact_id", "")).strip()

        if not question:
            errors.append(f"{seed_id}: question is required.")
        if not expected_document_ids and not seed.get("should_refuse"):
            errors.append(f"{seed_id}: expected_document_ids is required for answerable seeds.")
        if not expected_terms and not seed.get("should_refuse"):
            errors.append(f"{seed_id}: expected_terms is required for answerable seeds.")
        if source_fact_id and source_fact_ids and source_fact_id not in source_fact_ids:
            errors.append(f"{seed_id}: source_fact_id {source_fact_id!r} is not present in source_facts.")
        if not source_fact_id:
            warnings.append(f"{seed_id}: no source_fact_id is linked.")
        if not expected_anchor_terms and not seed.get("should_refuse"):
            warnings.append(f"{seed_id}: no expected_anchor_terms were provided.")
        if not expected_metadata and not seed.get("should_refuse"):
            warnings.append(f"{seed_id}: no expected_metadata was provided.")

        cases.append(
            {
                "question": question,
                "expected_document_ids": expected_document_ids,
                "expected_terms": expected_terms,
                "expected_metadata": {str(key): str(value) for key, value in expected_metadata.items()},
                "expected_anchor_terms": expected_anchor_terms,
                "expected_source_paths": _list_of_strings(seed.get("expected_source_paths")),
                "expected_section_terms": _list_of_strings(seed.get("expected_section_terms")),
                "expected_block_types": _list_of_strings(seed.get("expected_block_types")),
                "expected_sender_types": _list_of_strings(seed.get("expected_sender_types")),
                "expected_iso_code": str(seed.get("expected_iso_code", "")).strip(),
                "question_type": str(seed.get("question_type") or "factoid").strip(),
                "should_refuse": bool(seed.get("should_refuse")),
            }
        )

    if errors:
        return [], warnings, errors
    return cases, warnings, errors


def _semantic_summary(work_dir: Path) -> tuple[dict[str, int], dict[str, int]]:
    path = work_dir / "blocks.json"
    if not path.exists():
        return {}, {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        return {}, {}
    status_counts: dict[str, int] = {}
    intent_counts: dict[str, int] = {}
    for item in payload:
        if not isinstance(item, dict):
            continue
        metadata = item.get("metadata", {})
        if not isinstance(metadata, dict):
            continue
        status = str(metadata.get("semantic_map_status", "")).strip()
        intent = str(metadata.get("semantic_intent", "")).strip()
        if status:
            status_counts[status] = status_counts.get(status, 0) + 1
        if intent:
            intent_counts[intent] = intent_counts.get(intent, 0) + 1
    return status_counts, intent_counts


def _load_json_dict(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def _entries_from_payload(payload: dict[str, object]) -> list[dict[str, object]]:
    entries = payload.get("entries", [])
    if not isinstance(entries, list):
        return []
    return [entry for entry in entries if isinstance(entry, dict)]


def _is_multi_fact_or_comparison_review(entry: dict[str, object]) -> bool:
    question = str(entry.get("question", "")).lower()
    markers = [
        " compare ",
        " comparison ",
        " difference ",
        " differences ",
        " vs ",
        " versus ",
        " both ",
        " and ",
        " across ",
    ]
    padded = f" {question} "
    return any(marker in padded for marker in markers)


def _human_review_collection_prompts(
    *,
    total_reviews: int,
    rating_counts: dict[str, int],
    foreign_or_wrong_country_count: int,
    multi_fact_or_comparison_count: int,
    thresholds: dict[str, int],
) -> list[HumanReviewCollectionPrompt]:
    prompts: list[HumanReviewCollectionPrompt] = []
    if total_reviews < thresholds["total_query_reviews"]:
        prompts.append(
            HumanReviewCollectionPrompt(
                target="total_query_reviews",
                label="General factual review",
                question="What is the dialing code for Kuwait?",
                rating_hint="correct",
                notes="Use this for ordinary answer/evidence correctness review.",
            )
        )
    if rating_counts.get("should_refuse", 0) < thresholds["should_refuse"]:
        prompts.append(
            HumanReviewCollectionPrompt(
                target="should_refuse",
                label="Should-refuse review",
                question="Does Atlantis support two-way SMS?",
                rating_hint="should_refuse",
                notes="Use an out-of-corpus country or unsupported request and verify the answer refuses.",
            )
        )
    if foreign_or_wrong_country_count < thresholds["foreign_or_wrong_country"]:
        prompts.append(
            HumanReviewCollectionPrompt(
                target="foreign_or_wrong_country",
                label="Country evidence trap",
                question="Does Colombia support two-way SMS?",
                rating_hint="wrong_country",
                notes="Inspect whether the answer uses Colombia evidence or leaks another country.",
            )
        )
    if multi_fact_or_comparison_count < thresholds["multi_fact_or_comparison"]:
        prompts.append(
            HumanReviewCollectionPrompt(
                target="multi_fact_or_comparison",
                label="Multi-fact comparison",
                question="Compare two-way SMS support and sender registration in Colombia and Kuwait.",
                rating_hint="incomplete",
                notes="Rate as correct only if all requested facts are grounded in the right sources.",
            )
        )
    return prompts


def _document_iso_from_id(document_id: str) -> str:
    parts = document_id.lower().rsplit("_", 1)
    if len(parts) == 2 and len(parts[1]) == 2 and parts[1].isalpha():
        return parts[1].upper()
    return ""


def _human_review_quality_warnings(review_entries: list[dict[str, object]]) -> list[HumanReviewQualityWarning]:
    country_index = build_country_index()
    warnings: list[HumanReviewQualityWarning] = []
    negative_note_markers = ["not correct", "incorrect", "wrong", "bad evidence", "foreign evidence"]
    for index, entry in enumerate(review_entries, start=1):
        review_id = str(entry.get("review_id") or f"review-{index:05d}")
        question = str(entry.get("question", ""))
        rating = str(entry.get("rating", "")).strip().lower()
        notes = str(entry.get("notes", "")).strip().lower()
        expected_iso = str(entry.get("expected_iso_code", "")).strip().upper()
        evidence_document_ids = entry.get("evidence_document_ids", [])
        if not isinstance(evidence_document_ids, list):
            evidence_document_ids = []
        filters = extract_query_filters(question, country_index)

        if rating == "correct" and any(marker in notes for marker in negative_note_markers):
            warnings.append(
                HumanReviewQualityWarning(
                    review_id=review_id,
                    severity="high",
                    message="Review is rated correct, but notes indicate the answer was not correct.",
                )
            )

        if filters.iso_codes and expected_iso and expected_iso not in filters.iso_codes:
            warnings.append(
                HumanReviewQualityWarning(
                    review_id=review_id,
                    severity="high",
                    message=f"Expected ISO {expected_iso} does not match requested country ISO {', '.join(filters.iso_codes)}.",
                )
            )

        evidence_isos = {
            iso
            for iso in (_document_iso_from_id(str(document_id)) for document_id in evidence_document_ids)
            if iso
        }
        if (
            filters.iso_codes
            and evidence_isos
            and not evidence_isos.intersection(filters.iso_codes)
            and rating not in {"wrong_country", "correct_with_foreign_evidence"}
        ):
            warnings.append(
                HumanReviewQualityWarning(
                    review_id=review_id,
                    severity="high",
                    message=(
                        "Saved evidence appears to come from a different country "
                        f"({', '.join(sorted(evidence_isos))}) than requested ({', '.join(filters.iso_codes)})."
                    ),
                )
            )
    return warnings


def _human_review_readiness_payload(work_dir: Path) -> HumanReviewReadinessResponse:
    reviews_path = query_reviews_path(work_dir)
    findings_path = work_dir / "analytics" / "review_findings.json"
    review_entries = _entries_from_payload(_load_json_dict(reviews_path))
    finding_entries = _entries_from_payload(_load_json_dict(findings_path))

    rating_counts: dict[str, int] = {}
    for entry in review_entries:
        rating = str(entry.get("rating", "")).strip().lower() or "unrated"
        rating_counts[rating] = rating_counts.get(rating, 0) + 1

    accepted_statuses = {"accepted", "approved", "accepted_conflict", "resolved"}
    accepted_findings = [
        entry
        for entry in finding_entries
        if str(entry.get("status", "")).strip().lower() in accepted_statuses
    ]
    quality_warnings = _human_review_quality_warnings(review_entries)
    thresholds = {
        "total_query_reviews": 100,
        "should_refuse": 20,
        "foreign_or_wrong_country": 20,
        "multi_fact_or_comparison": 20,
        "category_stability": 10,
    }
    foreign_or_wrong_country_count = (
        rating_counts.get("correct_with_foreign_evidence", 0)
        + rating_counts.get("wrong_country", 0)
    )
    multi_fact_or_comparison_count = sum(
        1 for entry in review_entries if _is_multi_fact_or_comparison_review(entry)
    )
    checks = [
        HumanReviewReadinessCheck(
            name="Total human-reviewed queries",
            value=len(review_entries),
            target=thresholds["total_query_reviews"],
            status="pass" if len(review_entries) >= thresholds["total_query_reviews"] else "fail",
        ),
        HumanReviewReadinessCheck(
            name="Should-refuse cases",
            value=rating_counts.get("should_refuse", 0),
            target=thresholds["should_refuse"],
            status="pass" if rating_counts.get("should_refuse", 0) >= thresholds["should_refuse"] else "fail",
        ),
        HumanReviewReadinessCheck(
            name="Foreign-evidence or wrong-country cases",
            value=foreign_or_wrong_country_count,
            target=thresholds["foreign_or_wrong_country"],
            status="pass" if foreign_or_wrong_country_count >= thresholds["foreign_or_wrong_country"] else "fail",
        ),
        HumanReviewReadinessCheck(
            name="Multi-fact or comparison cases",
            value=multi_fact_or_comparison_count,
            target=thresholds["multi_fact_or_comparison"],
            status=(
                "pass"
                if multi_fact_or_comparison_count >= thresholds["multi_fact_or_comparison"]
                else "fail"
            ),
        ),
    ]
    stable_categories = sum(
        1 for count in rating_counts.values() if count >= thresholds["category_stability"]
    )
    if rating_counts:
        checks.append(
            HumanReviewReadinessCheck(
                name="Stable review categories",
                value=stable_categories,
                target=1,
                status="pass" if stable_categories else "fail",
            )
        )
    missing_targets = [
        f"{check.name}: need {max(0, check.target - check.value)} more"
        for check in checks
        if check.status != "pass" and check.target > check.value
    ]
    collection_prompts = _human_review_collection_prompts(
        total_reviews=len(review_entries),
        rating_counts=rating_counts,
        foreign_or_wrong_country_count=foreign_or_wrong_country_count,
        multi_fact_or_comparison_count=multi_fact_or_comparison_count,
        thresholds=thresholds,
    )
    ready_for_export = all(check.status == "pass" for check in checks)
    return HumanReviewReadinessResponse(
        work_dir=str(work_dir),
        query_reviews_path=str(reviews_path),
        review_findings_path=str(findings_path),
        query_reviews_found=reviews_path.exists(),
        review_findings_found=findings_path.exists(),
        total_query_reviews=len(review_entries),
        rating_counts=rating_counts,
        should_refuse_count=rating_counts.get("should_refuse", 0),
        foreign_or_wrong_country_count=foreign_or_wrong_country_count,
        multi_fact_or_comparison_count=multi_fact_or_comparison_count,
        review_findings_count=len(finding_entries),
        accepted_review_findings_count=len(accepted_findings),
        quality_warnings=quality_warnings,
        thresholds=thresholds,
        checks=checks,
        missing_targets=missing_targets,
        collection_prompts=collection_prompts,
        ready_for_export=ready_for_export,
        gate_mode="candidate_hard_gate" if ready_for_export else "advisory",
        proposed_outputs=[
            "benchmarks/query_review_regressions.json",
            "benchmarks/review_findings.json",
            "benchmarks/phase9_human_reviewed_regressions.json",
        ],
        message=(
            "Ready to export the human-reviewed regression benchmark."
            if ready_for_export
            else "Keep collecting human reviews before exporting this as a benchmark gate."
        ),
    )


def _benchmark_presets() -> list[BenchmarkPresetResponse]:
    presets = [
        (
            "Smoke",
            Path("benchmarks/real_corpus_smoke.json"),
            "Smallest real-corpus smoke pass for quick validation.",
        ),
        (
            "Core",
            Path("benchmarks/real_corpus_core.json"),
            "Broader real-corpus benchmark for regular regression checks.",
        ),
        (
            "Expanded",
            Path("benchmarks/real_corpus_expanded.json"),
            "Generated large benchmark for deeper evaluation and backend comparisons.",
        ),
        (
            "Aggregate Retrieval",
            Path("benchmarks/aggregate_retrieval.json"),
            "Focused checks for multi-country registration, capability, MCC, and restriction queries.",
        ),
    ]
    return [
        BenchmarkPresetResponse(
            name=name,
            path=str(path),
            cases=_count_benchmark_cases(path),
            description=description,
        )
        for name, path, description in presets
        if path.exists()
    ]


def _sample_questions() -> list[str]:
    return [
        "Sender in Spain?",
        "Does Sri Lanka support two-way SMS?",
        "What is the dialing code for Nepal?",
        "Compare sender provisioning and two-way support in Spain.",
    ]


def _index_artifacts_ready(work_dir: Path) -> bool:
    required = [
        work_dir / "manifest.json",
        work_dir / "blocks.json",
        work_dir / "documents.json",
    ]
    return all(path.exists() for path in required)


def _experiment_entry_with_artifact_status(entry: dict[str, object]) -> dict[str, object]:
    work_dir_value = entry.get("experiment_work_dir")
    work_dir = Path(str(work_dir_value)) if work_dir_value else None
    index_exists = bool(work_dir and work_dir.exists())
    index_ready = bool(work_dir and _index_artifacts_ready(work_dir))
    manifest = _load_manifest(work_dir) if index_ready and work_dir is not None else {}
    documents = int(manifest.get("documents", 0) or 0) if manifest else 0
    blocks = int(manifest.get("blocks", 0) or 0) if manifest else 0
    index_nonempty = index_ready and documents > 0 and blocks > 0
    if not work_dir_value:
        artifact_status = "missing_work_dir"
    elif not index_exists:
        artifact_status = "missing_index"
    elif not index_ready:
        artifact_status = "missing_artifacts"
    elif not index_nonempty:
        artifact_status = "empty_index"
    else:
        artifact_status = "ready"
    return {
        **entry,
        "index_exists": index_exists,
        "index_ready": index_ready,
        "index_nonempty": index_nonempty,
        "index_documents": documents,
        "index_blocks": blocks,
        "artifact_status": artifact_status,
    }


def _runtime_payload(settings: Settings, model_probe: ModelProbeResult | None = None) -> RuntimeResponse:
    manifest = _load_manifest(settings.work_dir)
    semantic_status_counts, semantic_intent_counts = _semantic_summary(settings.work_dir)
    indexed_payload = {
        "available": bool(manifest),
        "documents": int(manifest.get("documents", 0) or 0),
        "blocks": int(manifest.get("blocks", 0) or 0),
        "manifest_path": str(settings.work_dir / "manifest.json"),
        "manifest_modified_at": _manifest_modified_at(settings.work_dir),
        "index_id": _manifest_index_id(manifest),
        "document_ids_sample": _manifest_document_ids_sample(manifest),
        "reused_documents": int(manifest.get("reused_documents", 0) or 0),
        "rebuilt_documents": int(manifest.get("rebuilt_documents", 0) or 0),
        "allowed_suffixes": list(manifest.get("allowed_suffixes", []) or []),
        "mapping_provider": str(manifest.get("mapping_provider", "")),
        "mapping_model": str(manifest.get("mapping_model", "")),
        "mapping_batch_size": int(manifest.get("mapping_batch_size", 0) or 0),
        "mapping_batch_delay_ms": int(manifest.get("mapping_batch_delay_ms", 0) or 0),
        "mapping_text_char_limit": int(manifest.get("mapping_text_char_limit", 0) or 0),
        "mapping_prompt_mode": str(manifest.get("mapping_prompt_mode", "")),
        "mapping_retry_missing_results": bool(manifest.get("mapping_retry_missing_results", False)),
        "embedding_provider": str(manifest.get("embedding_provider", "")),
        "embedding_model": str(manifest.get("embedding_model", "")),
        "embedding_device": str(manifest.get("embedding_device", "")),
        "embedding_dimensions": manifest.get("embedding_dimensions"),
        "vector_backend": str(manifest.get("vector_backend", "")),
        "vector_collection": str(manifest.get("vector_collection", "")),
        "qdrant_url": str(manifest.get("qdrant_url", "")),
        "reranker_provider": str(manifest.get("reranker_provider", "")),
        "reranker_model": str(manifest.get("reranker_model", "")),
        "reranker_top_n": int(manifest.get("reranker_top_n", 0) or 0),
        "chunk_size": int(manifest.get("chunk_size", 0) or 0),
        "chunk_overlap": int(manifest.get("chunk_overlap", 0) or 0),
        "generation_provider": settings.generation_provider,
        "generation_model": settings.generation_model,
        "tier0_score_threshold": settings.tier0_score_threshold,
        "tier2_score_threshold": settings.tier2_score_threshold,
        "semantic_status_counts": semantic_status_counts,
        "semantic_intent_counts": semantic_intent_counts,
    }
    return RuntimeResponse(
        defaults=RuntimeDefaultsResponse(
            source_dir=str(settings.source_dir),
            work_dir=str(settings.work_dir),
            allowed_suffixes=list(normalize_allowed_suffixes(None)),
            top_k=settings.top_k,
            query_cache_enabled=settings.query_cache_enabled,
            api_host=settings.api_host,
            api_port=settings.api_port,
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            mapping_provider=settings.mapping_provider,
            mapping_model=settings.mapping_model,
            mapping_batch_size=settings.mapping_batch_size,
            mapping_batch_delay_ms=settings.mapping_batch_delay_ms,
            mapping_text_char_limit=settings.mapping_text_char_limit,
            mapping_prompt_mode=settings.mapping_prompt_mode,
            mapping_retry_missing_results=settings.mapping_retry_missing_results,
            embedding_provider=settings.embedding_provider,
            embedding_model=settings.embedding_model,
            embedding_device=settings.embedding_device,
            embedding_dimensions=settings.embedding_dimensions,
            vector_backend=settings.vector_backend,
            vector_collection=settings.vector_collection,
            qdrant_url=settings.qdrant_url,
            reranker_provider=settings.reranker_provider,
            reranker_model=settings.reranker_model,
            reranker_top_n=settings.reranker_top_n,
        ),
        indexed=IndexedCorpusResponse(**indexed_payload),
        testing=RuntimeTestingResponse(
            source_dir_exists=settings.source_dir.exists(),
            work_dir_exists=settings.work_dir.exists(),
            index_available=_index_artifacts_ready(settings.work_dir),
            latest_evaluation_available=(settings.work_dir / "evaluation" / "latest-evaluation.json").exists(),
            latest_calibration_available=(settings.work_dir / "evaluation" / "refusal-calibration.json").exists(),
            benchmark_presets=_benchmark_presets(),
            sample_questions=_sample_questions(),
        ),
        model_probe=ModelProbeResponse(**(model_probe or probe_provider_models(settings)).as_dict()),
    )


def _resolve_work_dir(raw_work_dir: str | None, settings: Settings) -> Path:
    return Path(raw_work_dir) if raw_work_dir else settings.work_dir


def _experiments_root(settings: Settings) -> Path:
    return settings.work_dir.parent


def _resolved_experiment_layout(
    settings: Settings,
    hypothesis: str,
    experiment_source_dir: str | None,
    experiment_work_dir: str | None,
) -> dict[str, str]:
    layout = suggest_experiment_layout(_experiments_root(settings), hypothesis)
    if experiment_source_dir:
        layout["experiment_source_dir"] = str(Path(experiment_source_dir))
    if experiment_work_dir:
        layout["experiment_work_dir"] = str(Path(experiment_work_dir))
    return layout


def _ensure_source_dir(raw_source_dir: str | None, settings: Settings) -> Path:
    source_dir = Path(raw_source_dir) if raw_source_dir else settings.source_dir
    if not source_dir.exists():
        raise HTTPException(status_code=400, detail=f"Source directory does not exist: {source_dir}")
    if not source_dir.is_dir():
        raise HTTPException(status_code=400, detail=f"Source directory is not a folder: {source_dir}")
    return source_dir


def _ensure_benchmark_path(raw_benchmark_path: str) -> Path:
    benchmark_path = Path(raw_benchmark_path)
    if not benchmark_path.exists():
        raise HTTPException(status_code=400, detail=f"Benchmark file does not exist: {benchmark_path}")
    if not benchmark_path.is_file():
        raise HTTPException(status_code=400, detail=f"Benchmark path is not a file: {benchmark_path}")
    return benchmark_path


def _ensure_index_ready(work_dir: Path) -> None:
    if not _index_artifacts_ready(work_dir):
        raise HTTPException(
            status_code=400,
            detail=(
                f"Index artifacts are missing in {work_dir}. "
                "Build the index before asking questions, evaluating, or calibrating."
            ),
        )


def _source_dir_for_experiment(
    settings: Settings,
    source_dir: str | None,
    experiment_source_dir: str | None,
) -> Path:
    if experiment_source_dir:
        resolved = Path(experiment_source_dir)
        if resolved.exists():
            return _ensure_source_dir(str(resolved), settings)
    return _ensure_source_dir(source_dir, settings)


def _strict_experiment_source_dir(experiment_source_dir: str | None, settings: Settings) -> Path:
    if not experiment_source_dir:
        raise HTTPException(
            status_code=400,
            detail="Experiment Source Dir is required for experiment builds.",
        )
    source_dir = Path(experiment_source_dir)
    if not source_dir.exists():
        raise HTTPException(
            status_code=400,
            detail=(
                f"Experiment Source Dir does not exist: {source_dir}. "
                "Upload files to the experiment source or set it to an existing folder."
            ),
        )
    if not source_dir.is_dir():
        raise HTTPException(status_code=400, detail=f"Experiment Source Dir is not a folder: {source_dir}")
    return source_dir


def _ensure_experiment_source_has_files(source_dir: Path, allowed_suffixes: list[str] | None) -> None:
    files = [
        path
        for path in source_dir.rglob("*")
        if can_parse_file(path, allowed_suffixes)
    ]
    if not files:
        allowed = ", ".join(normalize_allowed_suffixes(allowed_suffixes))
        raise HTTPException(
            status_code=400,
            detail=(
                f"Experiment Source Dir has no supported files: {source_dir}. "
                f"Upload .md, .json, or .txt files first, or change Experiment File Types. "
                f"Currently allowed: {allowed}."
            ),
        )


def _copy_source_tree(source_dir: Path, target_dir: Path, allowed_suffixes: list[str] | None) -> int:
    copied = 0
    for path in source_dir.rglob("*"):
        if not can_parse_file(path, allowed_suffixes):
            continue
        relative = path.relative_to(source_dir)
        destination = target_dir / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)
        copied += 1
    return copied


def _overlay_experiment_source_dir(
    *,
    baseline_source_dir: Path,
    experiment_source_dir: Path,
    experiment_work_dir: Path,
    allowed_suffixes: list[str] | None,
) -> Path:
    overlay_dir = Path(f"{experiment_work_dir}_overlay_source")
    if overlay_dir.exists():
        shutil.rmtree(overlay_dir)
    overlay_dir.mkdir(parents=True, exist_ok=True)
    baseline_count = _copy_source_tree(baseline_source_dir, overlay_dir, allowed_suffixes)
    experiment_count = _copy_source_tree(experiment_source_dir, overlay_dir, allowed_suffixes)
    if baseline_count <= 0:
        raise HTTPException(
            status_code=400,
            detail=f"Baseline Source Dir has no supported files to merge: {baseline_source_dir}.",
        )
    if experiment_count <= 0:
        raise HTTPException(
            status_code=400,
            detail=f"Experiment Source Dir has no supported files to merge: {experiment_source_dir}.",
        )
    return overlay_dir


def _experiment_build_suffixes(allowed_suffixes: list[str] | None, *, merge_with_baseline: bool) -> list[str] | None:
    if not merge_with_baseline or not allowed_suffixes:
        return allowed_suffixes
    normalized = normalize_allowed_suffixes(allowed_suffixes)
    if normalized == (".md",):
        return [".md", ".json", ".txt"]
    return allowed_suffixes


def _metric_bundle(summary) -> dict[str, float | int]:
    return {
        "total_cases": summary.total_cases,
        "retrieval_recall_at_k": summary.retrieval_recall_at_k,
        "evidence_hit_rate": summary.evidence_hit_rate,
        "citation_accuracy": summary.citation_accuracy,
        "document_precision_at_k": summary.document_precision_at_k,
        "no_answer_precision": summary.no_answer_precision,
        "answer_correctness": summary.answer_correctness,
        "country_match_at_1": summary.country_match_at_1,
        "foreign_evidence_rate": summary.foreign_evidence_rate,
        "wrong_country_answer_rate": summary.wrong_country_answer_rate,
        "diversity_enforcement_rate": summary.diversity_enforcement_rate,
        "answer_cache_hit_rate": summary.answer_cache_hit_rate,
    }


def _ingestion_health(work_dir: Path) -> dict[str, object]:
    manifest = _load_manifest(work_dir)
    ingest_report_path = work_dir / "ingest_report.json"
    blocks_path = work_dir / "blocks.json"
    vectors_path = work_dir / "vectors.json"
    ingest_report = {}
    blocks_payload: list[dict[str, object]] = []
    vectors_payload: list[object] = []

    if ingest_report_path.exists():
        try:
            ingest_report = json.loads(ingest_report_path.read_text(encoding="utf-8"))
        except Exception:
            ingest_report = {}
    if blocks_path.exists():
        try:
            blocks_payload = _load_blocks_payload(work_dir)
        except Exception:
            blocks_payload = []
    if vectors_path.exists():
        try:
            raw_vectors = json.loads(vectors_path.read_text(encoding="utf-8"))
            vectors = raw_vectors.get("vectors", []) if isinstance(raw_vectors, dict) else []
            vectors_payload = vectors if isinstance(vectors, list) else []
        except Exception:
            vectors_payload = []

    documents = int(manifest.get("documents", 0) or 0)
    blocks = int(manifest.get("blocks", len(blocks_payload)) or 0)
    failed_files = ingest_report.get("failed_files", [])
    skipped_files = ingest_report.get("skipped_files", [])
    zero_block_files = ingest_report.get("zero_block_files", [])
    rejected_blocks = int(ingest_report.get("rejected_blocks", 0) or 0)
    stored_low_quality_blocks = int(ingest_report.get("low_quality_blocks", 0) or 0)
    effective_statuses = [_effective_quality_status(block) for block in blocks_payload]
    raw_low_quality_blocks = (
        sum(1 for block in blocks_payload if str(block.get("quality_status") or "ok") == "LOW_QUALITY")
        if blocks_payload
        else stored_low_quality_blocks
    )
    low_quality_blocks = (
        sum(1 for status in effective_statuses if status == "LOW_QUALITY")
        if blocks_payload
        else stored_low_quality_blocks
    )
    effectively_ok_blocks = (
        sum(
            1
            for block, status in zip(blocks_payload, effective_statuses, strict=False)
            if block.get("quality_status") == "LOW_QUALITY" and status == "ok"
        )
        if blocks_payload
        else 0
    )
    duplicate_blocks = int(ingest_report.get("duplicate_blocks", 0) or 0)
    structured_fact_blocks = sum(1 for block in blocks_payload if block.get("block_type") == "structured_fact")
    json_blocks = sum(
        1
        for block in blocks_payload
        if isinstance(block.get("metadata"), dict)
        and str(block.get("metadata", {}).get("content_type", "")).lower() == "json"
    )
    title_only_blocks = sum(1 for block in blocks_payload if str(block.get("text", "")).strip().startswith("# ") and len(str(block.get("text", "")).split()) <= 4)
    vector_count = len(vectors_payload)
    vector_count_matches = blocks == vector_count
    low_quality_rate = round(low_quality_blocks / max(1, blocks), 4)

    warnings: list[str] = []
    if documents <= 0:
        warnings.append("No documents were indexed.")
    if blocks <= 0:
        warnings.append("No blocks were produced.")
    if failed_files:
        warnings.append("Some source files failed during ingest.")
    if zero_block_files:
        warnings.append("Some source files produced zero blocks.")
    if rejected_blocks:
        warnings.append("Some blocks were rejected by quality validation.")
    if not vector_count_matches:
        warnings.append("Vector count does not match block count.")
    if json_blocks and structured_fact_blocks <= 0:
        warnings.append("JSON sources produced no structured_fact blocks.")
    if title_only_blocks:
        warnings.append("Some blocks look title-only; useful source facts may not have been parsed.")
    if low_quality_rate > 0.5:
        warnings.append("More than half of blocks are marked low quality.")

    healthy = not warnings
    return {
        "healthy": healthy,
        "documents": documents,
        "blocks": blocks,
        "vector_count": vector_count,
        "vector_count_matches": vector_count_matches,
        "json_blocks": json_blocks,
        "structured_fact_blocks": structured_fact_blocks,
        "raw_low_quality_blocks": raw_low_quality_blocks,
        "low_quality_blocks": low_quality_blocks,
        "low_quality_rate": low_quality_rate,
        "effectively_ok_blocks": effectively_ok_blocks,
        "rejected_blocks": rejected_blocks,
        "duplicate_blocks": duplicate_blocks,
        "failed_file_count": len(failed_files) if isinstance(failed_files, list) else 0,
        "skipped_file_count": len(skipped_files) if isinstance(skipped_files, list) else 0,
        "zero_block_file_count": len(zero_block_files) if isinstance(zero_block_files, list) else 0,
        "title_only_blocks": title_only_blocks,
        "warnings": warnings,
        "suggested_actions": _ingestion_health_actions(warnings),
    }


def _ingestion_health_actions(warnings: list[str]) -> list[str]:
    actions: list[str] = []
    joined = " ".join(warnings).lower()
    if "title-only" in joined:
        actions.append("Rebuild the experiment workspace after the JSON source_facts parser fix.")
    if "no documents" in joined or "no blocks" in joined:
        actions.append("Verify the experiment source directory and allowed suffixes before rebuilding.")
    if "vector count" in joined:
        actions.append("Rebuild vectors for the experiment workspace.")
    if "json sources produced no structured_fact" in joined:
        actions.append("Rebuild after converting curated JSON facts into source_facts with fact_type/topic/value fields.")
    if "failed" in joined or "zero blocks" in joined:
        actions.append("Inspect ingest_report.json and fix source parsing issues.")
    if "low quality" in joined:
        actions.append("Inspect blocks.json to confirm curated facts are split into structured_fact blocks.")
    return actions or ["The experiment index is structurally healthy."]


def _effective_quality_status(block: dict[str, object]) -> str:
    status = str(block.get("quality_status") or "ok")
    if status != "LOW_QUALITY":
        return status
    block_type = str(block.get("block_type") or "")
    if block_type not in {"structured_fact", "table_fact", "list_item", "policy_rule"}:
        return status
    text = str(block.get("text") or "")
    metadata = block.get("metadata") if isinstance(block.get("metadata"), dict) else {}
    if len(text.strip()) < 15:
        return status
    if block_type == "structured_fact" and not _structured_fact_has_retrieval_signal(block, metadata):
        return status
    if block_type in {"table_fact", "list_item", "policy_rule"} and not _short_fact_has_retrieval_signal(block, metadata):
        return status
    return "ok"


def _low_quality_review_reasons(block: dict[str, object]) -> list[str]:
    if str(block.get("quality_status") or "ok") != "LOW_QUALITY":
        return []
    if _effective_quality_status(block) == "ok":
        return ["Accepted as curated structured fact"]

    block_type = str(block.get("block_type") or "")
    text = str(block.get("text") or "").strip()
    metadata = block.get("metadata") if isinstance(block.get("metadata"), dict) else {}
    row_values = str(metadata.get("row_values") or "")
    structured_field = str(metadata.get("structured_field") or "")
    structured_value = str(metadata.get("structured_value") or "")
    signal_text = f"{text}; {row_values}; {structured_field}; {structured_value}".lower()
    reasons: list[str] = []

    if len(text) < 15:
        reasons.append("Too short to stand alone")
    keyed_value = _extract_keyed_value(signal_text, "value")
    if (structured_value or keyed_value) and _is_placeholder_value(structured_value or keyed_value):
        reasons.append("Placeholder or unknown value")
    if text.startswith("# ") and len(text.split()) <= 4:
        reasons.append("Title-only block")

    has_entity_anchor = any(
        str(value or "").strip()
        for value in (
            block.get("country"),
            block.get("iso_code"),
            metadata.get("country"),
            metadata.get("country_iso2"),
            metadata.get("iso_code"),
            metadata.get("operator_name"),
        )
    ) or any(
        term in signal_text
        for term in ("country=", "country_name=", "country_iso2=", "iso_code=", "iso2=", "operator_name=", "applies_to=")
    )
    has_topic_anchor = bool(structured_field.strip()) or any(
        term in signal_text
        for term in ("fact_type=", "topic=", "regulation_topics=", "source_anchor=", "registration_scope=", "sender_types=")
    )
    if block_type == "structured_fact" and not has_entity_anchor:
        reasons.append("Missing country/operator anchor")
    if block_type == "structured_fact" and not has_topic_anchor:
        reasons.append("Missing topic/fact_type anchor")
    if block_type == "structured_fact" and not _structured_fact_has_retrieval_signal(block, metadata):
        reasons.append("No strong retrieval signal")
    if block_type not in {"structured_fact", "table_fact", "list_item", "policy_rule"}:
        reasons.append(f"Block type '{block_type or 'unknown'}' is not trusted for short facts")

    return list(dict.fromkeys(reasons)) or ["Needs manual review"]


def _delete_registered_experiment_workspaces(
    entries: list[object],
    *,
    default_work_dir: Path,
) -> dict[str, object]:
    baseline_paths: set[Path] = {default_work_dir.resolve()}
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        baseline = entry.get("baseline_work_dir")
        if baseline:
            baseline_paths.add(Path(str(baseline)).resolve())

    deleted: list[str] = []
    skipped: list[dict[str, str]] = []
    seen: set[Path] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        raw_work_dir = str(entry.get("experiment_work_dir") or "").strip()
        if not raw_work_dir:
            continue
        work_dir = Path(raw_work_dir)
        resolved = work_dir.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        if resolved in baseline_paths:
            skipped.append({"path": str(work_dir), "reason": "matches baseline work_dir"})
            continue
        if not work_dir.exists():
            skipped.append({"path": str(work_dir), "reason": "workspace does not exist"})
            continue
        if not work_dir.is_dir():
            skipped.append({"path": str(work_dir), "reason": "workspace path is not a directory"})
            continue
        if not _index_artifacts_ready(work_dir):
            skipped.append({"path": str(work_dir), "reason": "missing index artifacts"})
            continue
        shutil.rmtree(work_dir)
        deleted.append(str(work_dir))

    return {
        "deleted_workspaces": deleted,
        "deleted_workspace_count": len(deleted),
        "skipped_workspaces": skipped,
        "skipped_workspace_count": len(skipped),
    }


def _structured_fact_has_retrieval_signal(block: dict[str, object], metadata: dict[str, object]) -> bool:
    text = str(block.get("text") or "")
    row_values = str(metadata.get("row_values") or "")
    structured_field = str(metadata.get("structured_field") or "")
    structured_value = str(metadata.get("structured_value") or "")
    signal_text = f"{text}; {row_values}; {structured_field}; {structured_value}".lower()
    keyed_value = _extract_keyed_value(signal_text, "value")
    value = structured_value or keyed_value
    if (structured_value or keyed_value) and _is_placeholder_value(value):
        return False

    has_entity_anchor = any(
        str(value or "").strip()
        for value in (
            block.get("country"),
            block.get("iso_code"),
            metadata.get("country"),
            metadata.get("country_iso2"),
            metadata.get("iso_code"),
            metadata.get("operator_name"),
        )
    ) or any(
        term in signal_text
        for term in (
            "country=",
            "country_name=",
            "country_iso2=",
            "iso_code=",
            "iso2=",
            "operator_name=",
            "applies_to=",
        )
    )
    has_topic_anchor = bool(structured_field.strip()) or any(
        term in signal_text
        for term in (
            "fact_type=",
            "topic=",
            "regulation_topics=",
            "source_anchor=",
            "registration_scope=",
            "sender_types=",
            "hypothetical_questions=",
        )
    )
    structured_signal_terms = (
        "value=",
        "mcc=",
        "mnc=",
        "dialing_code=",
        "prefix=",
        "two-way",
        "two_way",
        "sender availability",
        "sender_id",
        "registration",
        "quiet hours",
        "promotional sms",
        "content restriction",
        "opt-in",
        "opt_out",
        "throughput",
        "delivery receipt",
        "unicode",
        "encoding",
        "pricing",
        "fee",
        "route",
    )
    if metadata.get("informative") == "high" and (metadata.get("structured_field") or metadata.get("structured_value")):
        return True
    return has_entity_anchor and has_topic_anchor and any(term in signal_text for term in structured_signal_terms)


def _short_fact_has_retrieval_signal(block: dict[str, object], metadata: dict[str, object]) -> bool:
    text = str(block.get("text") or "")
    metadata_text = " ".join(str(value) for value in metadata.values())
    signal_text = f"{text}; {metadata_text}".lower()
    keyed_value = _extract_keyed_value(signal_text, "value")
    if keyed_value and _is_placeholder_value(keyed_value):
        return False
    return any(
        term in signal_text
        for term in (
            "yes",
            "no",
            "supported",
            "not supported",
            "required",
            "mandatory",
            "allowed",
            "not allowed",
            "country",
            "iso",
            "mcc",
            "mnc",
            "dialing",
            "registration",
            "sender",
            "sms",
        )
    )


def _extract_keyed_value(signal_text: str, key: str) -> str:
    marker = f"{key.lower()}="
    if marker not in signal_text:
        return ""
    remainder = signal_text.split(marker, 1)[1]
    return remainder.split(";", 1)[0].strip()


def _is_placeholder_value(value: str) -> bool:
    normalized = value.strip().lower()
    return normalized in {"", "-", "--", "---", "n/a", "na", "none", "null", "unknown", "not specified", "not available"}


def _list_baseline_backups(baseline_work_dir: Path) -> list[dict[str, object]]:
    parent = baseline_work_dir.parent
    if not parent.exists():
        return []
    prefixes = (
        f"{baseline_work_dir.name}_backup_",
        f"{baseline_work_dir.name}_pre_rollback_",
    )
    backups: list[dict[str, object]] = []
    for candidate in parent.iterdir():
        if not candidate.is_dir():
            continue
        if not any(candidate.name.startswith(prefix) for prefix in prefixes):
            continue
        missing = [
            name
            for name in ("manifest.json", "blocks.json", "documents.json")
            if not (candidate / name).exists()
        ]
        stat = candidate.stat()
        backups.append(
            {
                "path": str(candidate),
                "name": candidate.name,
                "valid": not missing,
                "missing": missing,
                "modified_at": int(stat.st_mtime),
            }
        )
    return sorted(backups, key=lambda item: int(item["modified_at"]), reverse=True)


def _baseline_status_payload(baseline_work_dir: Path) -> BaselineStatusResponse:
    exists = baseline_work_dir.exists()
    index_ready = _index_artifacts_ready(baseline_work_dir)
    manifest = _load_manifest(baseline_work_dir) if index_ready else {}
    backups = _list_baseline_backups(baseline_work_dir)
    latest_valid_backup = next((backup for backup in backups if backup.get("valid")), None)
    return BaselineStatusResponse(
        baseline_work_dir=str(baseline_work_dir),
        promoted_baseline=baseline_work_dir.name == "work",
        exists=exists,
        index_ready=index_ready,
        documents=int(manifest.get("documents", 0) or 0),
        blocks=int(manifest.get("blocks", 0) or 0),
        modified_at=int(baseline_work_dir.stat().st_mtime) if exists else 0,
        rollback_backup_count=len(backups),
        latest_rollback_backup=latest_valid_backup,
    )


def _workspace_option(path: Path, *, label: str = "", kind: str = "workspace") -> dict[str, object]:
    exists = path.exists()
    ready = _index_artifacts_ready(path)
    manifest = _load_manifest(path) if ready else {}
    modified_at = int(path.stat().st_mtime) if exists else 0
    return {
        "path": str(path),
        "name": label or path.name,
        "kind": kind,
        "exists": exists,
        "index_ready": ready,
        "documents": int(manifest.get("documents", 0) or 0),
        "blocks": int(manifest.get("blocks", 0) or 0),
        "modified_at": modified_at,
    }


def _list_workspaces(settings: Settings) -> list[dict[str, object]]:
    seen: set[str] = set()
    options: list[dict[str, object]] = []

    def add(path: Path, *, label: str = "", kind: str = "workspace") -> None:
        key = str(path.resolve()) if path.exists() else str(path)
        if key in seen:
            return
        seen.add(key)
        options.append(_workspace_option(path, label=label, kind=kind))

    add(settings.work_dir, label=f"{settings.work_dir.name} (baseline)", kind="baseline")

    root = settings.work_dir.parent
    if root.exists():
        for candidate in root.iterdir():
            if not candidate.is_dir():
                continue
            if candidate.name.startswith("."):
                continue
            if candidate.name.startswith("work_exp_"):
                add(candidate, kind="experiment")
            elif candidate.name.startswith(f"{settings.work_dir.name}_backup_") or candidate.name.startswith(
                f"{settings.work_dir.name}_pre_rollback_"
            ):
                add(candidate, kind="backup")
            elif _index_artifacts_ready(candidate):
                add(candidate, kind="workspace")

    registry = load_experiments_registry(_experiments_root(settings))
    entries = registry.get("entries", [])
    if isinstance(entries, list):
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            work_dir = entry.get("experiment_work_dir")
            if work_dir:
                add(Path(str(work_dir)), kind="experiment")
            baseline_work_dir = entry.get("baseline_work_dir")
            if baseline_work_dir:
                add(Path(str(baseline_work_dir)), kind="baseline")
            promotion = entry.get("promotion")
            if isinstance(promotion, dict) and promotion.get("backup_work_dir"):
                add(Path(str(promotion["backup_work_dir"])), kind="backup")

    return sorted(
        options,
        key=lambda item: (
            0 if item["kind"] == "baseline" else 1 if item["kind"] == "experiment" else 2,
            -int(item["modified_at"]),
            str(item["path"]),
        ),
    )


def _comparison_payload(
    baseline_summary,
    experiment_summary,
    benchmark_path: Path | None = None,
    baseline_work_dir: Path | None = None,
    experiment_work_dir: Path | None = None,
) -> dict[str, object]:
    baseline_metrics = _metric_bundle(baseline_summary)
    experiment_metrics = _metric_bundle(experiment_summary)
    delta_metrics = {
        key: round(float(experiment_metrics[key]) - float(baseline_metrics[key]), 4)
        for key in baseline_metrics
        if key != "total_cases"
    }
    benchmark_profile = _benchmark_profile(
        benchmark_path=benchmark_path,
        baseline_work_dir=baseline_work_dir,
        experiment_work_dir=experiment_work_dir,
    )
    decision_checks = [
        (
            delta_metrics["answer_correctness"] >= -0.03,
            "Answer correctness did not regress beyond the 3-point tolerance.",
        ),
        (
            delta_metrics["citation_accuracy"] >= -0.03,
            "Citation accuracy did not regress beyond the 3-point tolerance.",
        ),
        (
            delta_metrics["country_match_at_1"] >= -0.02,
            "Country match at 1 did not regress beyond the 2-point tolerance.",
        ),
        (
            delta_metrics["foreign_evidence_rate"] <= 0.02,
            "Foreign evidence rate did not increase beyond the 2-point tolerance.",
        ),
        (
            delta_metrics["wrong_country_answer_rate"] <= 0.02,
            "Wrong-country answer rate did not increase beyond the 2-point tolerance.",
        ),
    ]
    improved = [
        delta_metrics["answer_correctness"] > 0.01,
        delta_metrics["citation_accuracy"] > 0.01,
        delta_metrics["country_match_at_1"] > 0.01,
        delta_metrics["foreign_evidence_rate"] < -0.01,
        delta_metrics["wrong_country_answer_rate"] < -0.01,
    ]
    benchmark_is_adequate = bool(benchmark_profile.get("adequate"))
    has_critical_regression = not all(ok for ok, _ in decision_checks)
    has_improvement = any(improved)
    promotion_recommended = benchmark_is_adequate and not has_critical_regression and has_improvement
    if promotion_recommended:
        promotion_decision = "promote"
    elif not benchmark_is_adequate:
        promotion_decision = "needs_benchmark"
    elif has_critical_regression:
        promotion_decision = "reject"
    else:
        promotion_decision = "neutral"
    return {
        "baseline_metrics": baseline_metrics,
        "experiment_metrics": experiment_metrics,
        "delta_metrics": delta_metrics,
        "promotion_recommended": promotion_recommended,
        "promotion_decision": promotion_decision,
        "benchmark_profile": benchmark_profile,
        "decision_checks": [
            {"passed": passed, "message": message}
            for passed, message in decision_checks
        ],
        "recommendation_notes": _promotion_notes(
            promotion_decision=promotion_decision,
            benchmark_profile=benchmark_profile,
            has_critical_regression=has_critical_regression,
            has_improvement=has_improvement,
        ),
    }


def _benchmark_profile(
    *,
    benchmark_path: Path | None,
    baseline_work_dir: Path | None,
    experiment_work_dir: Path | None,
) -> dict[str, object]:
    if benchmark_path is None or not benchmark_path.exists():
        return {
            "adequate": False,
            "warnings": ["Benchmark profile unavailable."],
            "suggested_actions": ["Run comparison with a benchmark_path so promotion can assess coverage."],
        }

    try:
        payload = json.loads(benchmark_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {
            "adequate": False,
            "warnings": [f"Benchmark could not be read: {type(exc).__name__}."],
            "suggested_actions": ["Fix benchmark JSON before trusting promotion decisions."],
        }

    cases = payload if isinstance(payload, list) else []
    total_cases = len(cases)
    question_type_counts: dict[str, int] = {}
    expected_docs: set[str] = set()
    expected_terms_cases = 0
    country_cases = 0
    for case in cases:
        if not isinstance(case, dict):
            continue
        qtype = str(case.get("question_type") or "unknown")
        question_type_counts[qtype] = question_type_counts.get(qtype, 0) + 1
        docs = case.get("expected_document_ids")
        if isinstance(docs, list):
            expected_docs.update(str(item) for item in docs if str(item).strip())
        terms = case.get("expected_terms")
        if isinstance(terms, list) and terms:
            expected_terms_cases += 1
        if case.get("expected_iso_code") or (isinstance(docs, list) and len(docs) == 1):
            country_cases += 1

    baseline_docs = _manifest_document_ids(baseline_work_dir)
    experiment_docs = _manifest_document_ids(experiment_work_dir)
    new_experiment_docs = sorted(experiment_docs - baseline_docs)
    benchmark_docs_in_experiment = sorted(expected_docs.intersection(experiment_docs))
    new_docs_covered = sorted(expected_docs.intersection(new_experiment_docs))

    warnings: list[str] = []
    suggested_actions: list[str] = []
    if total_cases < 10:
        warnings.append("Benchmark has fewer than 10 cases; promotion signal is weak.")
        suggested_actions.append("Add at least 10 focused cases for this experiment before promotion.")
    if expected_terms_cases / max(1, total_cases) < 0.8:
        warnings.append("Many cases do not specify expected_terms, so answer correctness may fall back to retrieval hit.")
        suggested_actions.append("Add expected_terms for each benchmark case.")
    if country_cases == 0:
        warnings.append("Benchmark has no country/ISO-specific cases.")
        suggested_actions.append("Add expected_iso_code to country-sensitive benchmark cases.")
    if new_experiment_docs and not new_docs_covered:
        warnings.append("Experiment adds documents that the benchmark does not explicitly cover.")
        suggested_actions.append("Add benchmark cases targeting the new experiment documents.")
    if expected_docs and experiment_docs and not benchmark_docs_in_experiment:
        warnings.append("Benchmark expected_document_ids do not match documents in the experiment index.")
        suggested_actions.append("Use a benchmark aligned with this experiment workspace.")

    return {
        "adequate": not warnings,
        "total_cases": total_cases,
        "country_cases": country_cases,
        "expected_terms_cases": expected_terms_cases,
        "question_type_counts": question_type_counts,
        "expected_document_count": len(expected_docs),
        "experiment_document_count": len(experiment_docs),
        "new_experiment_document_count": len(new_experiment_docs),
        "new_experiment_documents_covered": len(new_docs_covered),
        "warnings": warnings,
        "suggested_actions": suggested_actions,
    }


def _manifest_document_ids(work_dir: Path | None) -> set[str]:
    if work_dir is None:
        return set()
    manifest_path = work_dir / "manifest.json"
    if not manifest_path.exists():
        return set()
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception:
        return set()
    state = manifest.get("documents_state")
    if isinstance(state, dict):
        return {str(key) for key in state}
    return set()


def _promotion_notes(
    *,
    promotion_decision: str,
    benchmark_profile: dict[str, object],
    has_critical_regression: bool,
    has_improvement: bool,
) -> list[str]:
    if promotion_decision == "promote":
        return ["Benchmark is adequate and the experiment improves at least one primary metric without critical regressions."]
    if promotion_decision == "needs_benchmark":
        notes = ["Do not promote yet; the benchmark is not strong enough to judge this experiment."]
        notes.extend(str(item) for item in benchmark_profile.get("suggested_actions", []))
        if has_critical_regression:
            notes.append("Current metrics show regressions, but first confirm the benchmark covers the experiment correctly.")
        return notes
    if promotion_decision == "reject":
        return ["Do not promote; benchmark coverage is adequate and one or more critical metrics regressed."]
    if not has_improvement:
        return ["Do not promote yet; no primary metric improved beyond the practical threshold."]
    return ["Review manually before promotion."]


def _build_settings_for_request(request: BuildIndexRequest, settings: Settings) -> Settings:
    payload = request.model_dump(exclude_none=True)
    for key in {
        "source_dir",
        "work_dir",
        "allowed_suffixes",
        "allow_low_quality",
        "force_reenrich",
        "experiment_source_dir",
        "experiment_work_dir",
        "baseline_work_dir",
        "benchmark_path",
        "merge_with_baseline",
        "hypothesis",
        "notes",
    }:
        payload.pop(key, None)
    return settings.model_copy(update=payload)


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()
    model_probe = probe_provider_models(settings)
    pipeline = KnowledgePipeline(settings)
    app = FastAPI(
        title="Own Knowledge RAG API",
        version="0.1.0",
        description="Thin API layer over the local-first Own Knowledge RAG core.",
    )
    app.mount("/static", StaticFiles(directory=_STATIC_DIR), name="static")

    @app.get("/", response_class=HTMLResponse)
    async def gui() -> HTMLResponse:
        return HTMLResponse(render_gui(settings, mode="user"))

    @app.get("/tech", response_class=HTMLResponse)
    async def tech_gui() -> HTMLResponse:
        return HTMLResponse(render_gui(settings, mode="tech"))

    @app.get("/health", response_model=HealthResponse)
    async def health() -> HealthResponse:
        return HealthResponse(status="ok", app="own-knowledge-rag")

    @app.get("/runtime", response_model=RuntimeResponse)
    async def runtime() -> RuntimeResponse:
        return _runtime_payload(settings, model_probe)

    @app.get("/workspaces")
    async def list_workspaces() -> dict[str, object]:
        return {
            "default_work_dir": str(settings.work_dir),
            "workspaces": _list_workspaces(settings),
        }

    @app.get("/baseline/status", response_model=BaselineStatusResponse)
    async def baseline_status(baseline_work_dir: str | None = None) -> BaselineStatusResponse:
        baseline = Path(baseline_work_dir) if baseline_work_dir else settings.work_dir
        return _baseline_status_payload(baseline)

    @app.get("/human-review/readiness", response_model=HumanReviewReadinessResponse)
    async def human_review_readiness(work_dir: str | None = None) -> HumanReviewReadinessResponse:
        resolved_work_dir = _resolve_work_dir(work_dir, settings)
        return _human_review_readiness_payload(resolved_work_dir)

    @app.post("/human-review/export-benchmark", response_model=HumanReviewExportResponse)
    async def export_human_review_benchmark(request: HumanReviewExportRequest) -> HumanReviewExportResponse:
        work_dir = _resolve_work_dir(request.work_dir, settings)
        readiness = _human_review_readiness_payload(work_dir)
        if not readiness.ready_for_export and not request.allow_undercovered:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": readiness.message,
                    "readiness": readiness.model_dump(),
                },
            )
        if not readiness.query_reviews_found:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": f"No query review file found at {readiness.query_reviews_path}.",
                    "readiness": readiness.model_dump(),
                },
            )
        output_dir = Path(request.output_dir)
        query_output_path = output_dir / "query_review_regressions.json"
        query_cases = export_query_reviews_benchmark(Path(readiness.query_reviews_path), query_output_path)
        review_output_path = output_dir / "review_findings.json"
        review_cases = []
        if readiness.review_findings_found and readiness.accepted_review_findings_count:
            review_cases = export_review_findings_benchmark(Path(readiness.review_findings_path), review_output_path)
        return HumanReviewExportResponse(
            exported=True,
            query_review_benchmark_path=str(query_output_path),
            query_review_cases=len(query_cases),
            review_findings_benchmark_path=str(review_output_path) if review_cases else "",
            review_findings_cases=len(review_cases),
            readiness=readiness,
            message=(
                "Exported human-reviewed benchmark artifacts."
                if readiness.ready_for_export
                else "Exported under-covered benchmark artifacts as advisory only."
            ),
        )

    def _prompt_payload(path: Path) -> dict[str, object]:
        if not path.exists():
            return {"path": str(path), "template": ""}
        return {
            "path": str(path),
            "template": path.read_text(encoding="utf-8"),
        }

    @app.get("/library/prose-source-ingestion-enrichment-prompt")
    async def library_prose_source_ingestion_enrichment_prompt() -> dict[str, object]:
        return _prompt_payload(_PROSE_SOURCE_INGESTION_PROMPT_PATH)

    @app.get("/library/faq-qa-source-fact-ingestion-prompt")
    async def library_faq_qa_source_fact_ingestion_prompt() -> dict[str, object]:
        return _prompt_payload(_FAQ_QA_SOURCE_FACT_INGESTION_PROMPT_PATH)

    @app.get("/library/enrichment-prompt")
    async def library_enrichment_prompt() -> dict[str, object]:
        return _prompt_payload(_PROSE_SOURCE_INGESTION_PROMPT_PATH)

    @app.get("/library/faq-source-fact-prompt")
    async def library_faq_source_fact_prompt() -> dict[str, object]:
        return _prompt_payload(_FAQ_QA_SOURCE_FACT_INGESTION_PROMPT_PATH)

    @app.get("/knowledge/templates", response_model=KnowledgeTemplateResponse)
    async def knowledge_templates() -> KnowledgeTemplateResponse:
        return KnowledgeTemplateResponse(
            source_fact_template=(
                _SOURCE_FACT_TEMPLATE_PATH.read_text(encoding="utf-8")
                if _SOURCE_FACT_TEMPLATE_PATH.exists()
                else "{}"
            ),
            qa_seed_template=(
                _QA_SEED_TEMPLATE_PATH.read_text(encoding="utf-8")
                if _QA_SEED_TEMPLATE_PATH.exists()
                else "{}"
            ),
            qa_seed_generation_prompt=(
                _QA_SEED_GENERATION_PROMPT_PATH.read_text(encoding="utf-8")
                if _QA_SEED_GENERATION_PROMPT_PATH.exists()
                else _QA_SEED_GENERATION_PROMPT_FALLBACK
            ),
            source_fact_template_path=str(_SOURCE_FACT_TEMPLATE_PATH),
            qa_seed_template_path=str(_QA_SEED_TEMPLATE_PATH),
            qa_seed_generation_prompt_path=str(_QA_SEED_GENERATION_PROMPT_PATH),
        )

    @app.post("/knowledge/qa-seeds/export", response_model=KnowledgeQaSeedExportResponse)
    async def export_qa_seed_benchmark(
        request: KnowledgeQaSeedExportRequest,
    ) -> KnowledgeQaSeedExportResponse:
        qa_seed_payload = _json_from_text(request.qa_seed_content, label="Q&A seed content")
        source_fact_ids = (
            _source_fact_ids_from_payload(_json_from_text(request.source_fact_content, label="Source fact content"))
            if request.source_fact_content.strip()
            else set()
        )
        cases, warnings, errors = _qa_seed_cases_from_payload(
            qa_seed_payload=qa_seed_payload,
            source_fact_ids=source_fact_ids,
            allow_pending=request.allow_pending,
        )
        output_path = Path(request.output_path)
        if errors:
            return KnowledgeQaSeedExportResponse(
                exported=False,
                output_path=str(output_path),
                case_count=0,
                warnings=warnings,
                errors=errors,
                source_fact_ids=sorted(source_fact_ids),
                cases=[],
            )
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(cases, indent=2), encoding="utf-8")
        return KnowledgeQaSeedExportResponse(
            exported=True,
            output_path=str(output_path),
            case_count=len(cases),
            warnings=warnings,
            errors=[],
            source_fact_ids=sorted(source_fact_ids),
            cases=cases,
        )

    @app.post("/build-index", response_model=BuildIndexResponse)
    async def build_index(request: BuildIndexRequest) -> BuildIndexResponse:
        source_dir = _ensure_source_dir(request.source_dir, settings)
        work_dir = _resolve_work_dir(request.work_dir, settings)
        build_settings = _build_settings_for_request(request, settings)
        build_pipeline = KnowledgePipeline(build_settings)
        try:
            manifest = build_pipeline.build_index(
                source_dir=source_dir, 
                work_dir=work_dir, 
                allow_low_quality=request.allow_low_quality,
                force_reenrich=request.force_reenrich,
                allowed_suffixes=request.allowed_suffixes,
            )
        except BuildLockError as error:
            raise HTTPException(
                status_code=409,
                detail={
                    "message": str(error),
                    "lock": error.lock_info,
                },
            ) from error
        pipeline._retriever_cache.pop(str(work_dir.resolve()), None)
        return BuildIndexResponse(**manifest)

    @app.post("/build-index/clear-stale-lock", response_model=BuildLockResponse)
    async def clear_stale_build_lock(request: BuildLockRequest) -> BuildLockResponse:
        work_dir = _resolve_work_dir(request.work_dir, settings)
        try:
            status = KnowledgePipeline(settings).clear_stale_build_lock(work_dir)
        except BuildLockError as error:
            raise HTTPException(
                status_code=409,
                detail={
                    "message": str(error),
                    "lock": error.lock_info,
                },
            ) from error
        return BuildLockResponse(**status.to_dict())

    @app.get("/experiments")
    async def list_experiments() -> dict[str, object]:
        registry = load_experiments_registry(_experiments_root(settings))
        entries = registry.get("entries", [])
        if not isinstance(entries, list):
            entries = []
        return {
            "registry_path": str(experiments_registry_path(_experiments_root(settings))),
            "entries": [
                _experiment_entry_with_artifact_status(entry)
                for entry in entries
                if isinstance(entry, dict)
            ],
        }

    @app.post("/experiments/clear-registry")
    async def clear_experiment_registry(request: ExperimentClearRegistryRequest) -> dict[str, object]:
        registry = load_experiments_registry(_experiments_root(settings))
        entries = registry.get("entries", [])
        entries = entries if isinstance(entries, list) else []
        workspace_result = (
            _delete_registered_experiment_workspaces(entries, default_work_dir=settings.work_dir)
            if request.delete_workspaces
            else {
                "deleted_workspaces": [],
                "deleted_workspace_count": 0,
                "skipped_workspaces": [],
                "skipped_workspace_count": 0,
            }
        )
        registry_path, cleared_count = clear_experiments_registry(_experiments_root(settings))
        return {
            "status": "cleared",
            "registry_path": str(registry_path),
            "cleared_count": cleared_count,
            "entries": [],
            **workspace_result,
            "note": (
                "Experiment registry records were cleared and registered experiment workspaces were deleted. "
                "Baseline data and staged source files were not deleted."
                if request.delete_workspaces
                else "Experiment registry records were cleared. Workspaces and staged source files were not deleted."
            ),
        }

    @app.get("/experiments/backups")
    async def list_experiment_backups(baseline_work_dir: str | None = None) -> dict[str, object]:
        baseline = Path(baseline_work_dir) if baseline_work_dir else settings.work_dir
        return {
            "baseline_work_dir": str(baseline),
            "backups": _list_baseline_backups(baseline),
        }

    @app.post("/experiments/suggest")
    async def suggest_experiment(request: ExperimentSuggestRequest) -> dict[str, str]:
        return _resolved_experiment_layout(
            settings=settings,
            hypothesis=request.hypothesis,
            experiment_source_dir=None,
            experiment_work_dir=None,
        )

    @app.post("/experiments/upload-files")
    async def upload_experiment_files(request: ExperimentUploadRequest) -> dict[str, object]:
        layout = _resolved_experiment_layout(
            settings=settings,
            hypothesis=request.hypothesis,
            experiment_source_dir=request.experiment_source_dir,
            experiment_work_dir=None,
        )
        saved = stage_experiment_files(
            Path(layout["experiment_source_dir"]),
            [_repair_upload_file_if_needed(item) for item in request.files],
        )
        return {
            "experiment_id": layout["experiment_id"],
            "experiment_source_dir": layout["experiment_source_dir"],
            **saved,
        }

    @app.post("/experiments/create", response_model=ExperimentCreateResponse)
    async def create_experiment(request: ExperimentCreateRequest) -> ExperimentCreateResponse:
        layout = _resolved_experiment_layout(
            settings=settings,
            hypothesis=request.hypothesis,
            experiment_source_dir=request.experiment_source_dir,
            experiment_work_dir=request.experiment_work_dir,
        )
        source_dir = Path(layout["experiment_source_dir"])
        source_dir.mkdir(parents=True, exist_ok=True)
        experiment_work_dir = Path(layout["experiment_work_dir"])
        baseline_work_dir = _resolve_work_dir(request.baseline_work_dir, settings)
        benchmark_path = str(Path(request.benchmark_path)) if request.benchmark_path else ""
        registry_path, stored = save_experiment_record(
            _experiments_root(settings),
            {
                "experiment_id": layout["experiment_id"],
                "source_dir": str(source_dir),
                "experiment_source_dir": layout["experiment_source_dir"],
                "experiment_work_dir": str(experiment_work_dir),
                "baseline_work_dir": str(baseline_work_dir),
                "benchmark_path": benchmark_path,
                "content_type": request.content_type.strip() or "documents",
                "hypothesis": request.hypothesis.strip(),
                "notes": request.notes.strip(),
                "status": "draft",
            },
        )
        return ExperimentCreateResponse(
            experiment_id=str(stored["experiment_id"]),
            registry_path=str(registry_path),
            experiment_source_dir=str(layout["experiment_source_dir"]),
            experiment_work_dir=str(experiment_work_dir),
            baseline_work_dir=str(baseline_work_dir),
            benchmark_path=benchmark_path,
            status=str(stored.get("status", "draft")),
        )

    @app.post("/experiments/build")
    async def build_experiment(request: ExperimentBuildRequest) -> dict[str, object]:
        layout = _resolved_experiment_layout(
            settings=settings,
            hypothesis=request.hypothesis,
            experiment_source_dir=request.experiment_source_dir,
            experiment_work_dir=request.experiment_work_dir,
        )
        allowed_suffixes = _experiment_build_suffixes(
            request.allowed_suffixes,
            merge_with_baseline=request.merge_with_baseline,
        )
        source_dir = _strict_experiment_source_dir(layout["experiment_source_dir"], settings)
        _ensure_experiment_source_has_files(source_dir, allowed_suffixes)
        experiment_work_dir = Path(layout["experiment_work_dir"])
        baseline_work_dir = _resolve_work_dir(request.baseline_work_dir, settings)
        build_settings = _build_settings_for_request(request, settings)
        build_pipeline = KnowledgePipeline(build_settings)
        try:
            manifest = (
                build_pipeline.build_merged_index(
                    baseline_work_dir=baseline_work_dir,
                    experiment_source_dir=source_dir,
                    work_dir=experiment_work_dir,
                    allow_low_quality=request.allow_low_quality,
                    force_reenrich=request.force_reenrich,
                    allowed_suffixes=allowed_suffixes,
                )
                if request.merge_with_baseline
                else build_pipeline.build_index(
                    source_dir=source_dir,
                    work_dir=experiment_work_dir,
                    allow_low_quality=request.allow_low_quality,
                    force_reenrich=request.force_reenrich,
                    allowed_suffixes=allowed_suffixes,
                )
            )
        except BuildLockError as error:
            raise HTTPException(status_code=409, detail=str(error)) from error
        except ValueError as error:
            raise HTTPException(status_code=400, detail=str(error)) from error
        build_source_dir = source_dir
        registry_path, stored = save_experiment_record(
            _experiments_root(settings),
            {
                "experiment_id": layout["experiment_id"],
                "source_dir": str(source_dir),
                "experiment_source_dir": layout["experiment_source_dir"],
                "experiment_work_dir": str(experiment_work_dir),
                "baseline_work_dir": str(baseline_work_dir),
                "build_source_dir": str(build_source_dir),
                "merge_with_baseline": request.merge_with_baseline,
                "merge_strategy": manifest.get("merge_strategy", "isolated_build"),
                "benchmark_path": request.benchmark_path or "",
                "content_type": request.content_type.strip() or "documents",
                "hypothesis": request.hypothesis.strip(),
                "notes": request.notes.strip(),
                "status": "built",
                "build_manifest": manifest,
            },
        )
        pipeline._retriever_cache.pop(str(experiment_work_dir.resolve()), None)
        return {
            "experiment_id": stored["experiment_id"],
            "registry_path": str(registry_path),
            "experiment_source_dir": layout["experiment_source_dir"],
            "build_source_dir": str(build_source_dir),
            "merge_with_baseline": request.merge_with_baseline,
            "merge_strategy": manifest.get("merge_strategy", "isolated_build"),
            "status": stored["status"],
            "build": BuildIndexResponse(**manifest).model_dump(),
        }

    @app.post("/experiments/evaluate")
    async def evaluate_experiment(request: ExperimentEvaluateRequest) -> dict[str, object]:
        experiment_work_dir = Path(request.experiment_work_dir)
        _ensure_index_ready(experiment_work_dir)
        ingestion_health = _ingestion_health(experiment_work_dir)
        benchmark_path = _ensure_benchmark_path(request.benchmark_path) if request.benchmark_path else None
        summary = (
            pipeline.evaluate(
                benchmark_path=benchmark_path,
                work_dir=experiment_work_dir,
                top_k=request.top_k,
            )
            if benchmark_path is not None
            else None
        )
        registry_path, stored = save_experiment_record(
            _experiments_root(settings),
            {
                "source_dir": str(settings.source_dir),
                "experiment_work_dir": str(experiment_work_dir),
                "baseline_work_dir": str(_resolve_work_dir(request.baseline_work_dir, settings)),
                "benchmark_path": str(benchmark_path) if benchmark_path else "",
                "content_type": request.content_type.strip() or "documents",
                "hypothesis": request.hypothesis.strip(),
                "notes": request.notes.strip(),
                "status": "evaluated",
                "ingestion_health": ingestion_health,
                "evaluation_summary": _metric_bundle(summary) if summary is not None else {},
            },
        )
        return {
            "experiment_id": stored["experiment_id"],
            "registry_path": str(registry_path),
            "status": stored["status"],
            "summary": _metric_bundle(summary) if summary is not None else {},
            "ingestion_health": ingestion_health,
            "benchmark_used": str(benchmark_path) if benchmark_path else "",
        }

    @app.post("/experiments/compare")
    async def compare_experiment(request: ExperimentCompareRequest) -> dict[str, object]:
        baseline_work_dir = Path(request.baseline_work_dir or settings.work_dir)
        experiment_work_dir = Path(request.experiment_work_dir)
        _ensure_index_ready(baseline_work_dir)
        _ensure_index_ready(experiment_work_dir)
        benchmark_path = _ensure_benchmark_path(request.benchmark_path) if request.benchmark_path else None
        baseline_health = _ingestion_health(baseline_work_dir)
        experiment_health = _ingestion_health(experiment_work_dir)
        if benchmark_path is not None:
            baseline_summary = pipeline.evaluate(
                benchmark_path=benchmark_path,
                work_dir=baseline_work_dir,
                top_k=request.top_k,
            )
            experiment_summary = pipeline.evaluate(
                benchmark_path=benchmark_path,
                work_dir=experiment_work_dir,
                top_k=request.top_k,
            )
            comparison = _comparison_payload(
                baseline_summary,
                experiment_summary,
                benchmark_path=benchmark_path,
                baseline_work_dir=baseline_work_dir,
                experiment_work_dir=experiment_work_dir,
            )
            comparison["statistical_comparison"] = compare_experiments(
                baseline_summary,
                experiment_summary,
                experiment_work_dir / "evaluation" / "comparison_report.json",
            )
        else:
            comparison = {
                "baseline_metrics": {},
                "experiment_metrics": {},
                "delta_metrics": {},
                "promotion_recommended": bool(experiment_health["healthy"]),
                "promotion_decision": "ingest_healthy" if experiment_health["healthy"] else "fix_ingestion",
                "benchmark_profile": {
                    "adequate": False,
                    "warnings": ["No benchmark was supplied; comparison is based on agnostic ingestion health only."],
                    "suggested_actions": ["Use a focused benchmark later if you want retrieval/answer regression evidence."],
                },
                "decision_checks": [
                    {
                        "passed": bool(experiment_health["healthy"]),
                        "message": "Experiment index passed agnostic ingestion health checks.",
                    }
                ],
                "recommendation_notes": list(experiment_health.get("suggested_actions", [])),
            }
        comparison["baseline_ingestion_health"] = baseline_health
        comparison["experiment_ingestion_health"] = experiment_health
        registry_path, stored = save_experiment_record(
            _experiments_root(settings),
            {
                "source_dir": str(settings.source_dir),
                "experiment_work_dir": str(experiment_work_dir),
                "baseline_work_dir": str(baseline_work_dir),
                "benchmark_path": str(benchmark_path) if benchmark_path else "",
                "content_type": request.content_type.strip() or "documents",
                "hypothesis": request.hypothesis.strip(),
                "notes": request.notes.strip(),
                "status": "compared",
                "comparison": comparison,
            },
        )
        return {
            "experiment_id": stored["experiment_id"],
            "registry_path": str(registry_path),
            "status": stored["status"],
            **comparison,
        }

    @app.post("/experiments/promote")
    async def promote_experiment(request: ExperimentPromoteRequest) -> dict[str, object]:
        baseline_work_dir = Path(request.baseline_work_dir)
        experiment_work_dir = Path(request.experiment_work_dir)
        source_alignment: dict[str, object] = {
            "accepted": True,
            "checked_files": 0,
            "missing_files": [],
            "changed_files": [],
            "override_used": False,
        }
        if request.experiment_source_dir:
            experiment_source_dir = _strict_experiment_source_dir(request.experiment_source_dir, settings)
            baseline_source_dir = _ensure_source_dir(request.source_dir, settings)
            try:
                source_alignment = experiment_sources_alignment(
                    experiment_source_dir=experiment_source_dir,
                    baseline_source_dir=baseline_source_dir,
                )
            except ValueError as error:
                raise HTTPException(status_code=400, detail=str(error)) from error
            source_alignment["override_used"] = False
            if not source_alignment["accepted"]:
                if not request.force_promote_without_sources:
                    raise HTTPException(
                        status_code=409,
                        detail={
                            "message": (
                                "Promotion is blocked because experiment source files have not been accepted "
                                "into the baseline source library."
                            ),
                            "source_alignment": source_alignment,
                            "suggested_action": (
                                "Use Accept Sources Into Library first, or retry promotion with "
                                "force_promote_without_sources=true."
                            ),
                        },
                    )
                source_alignment["override_used"] = True
        baseline_lock = KnowledgePipeline._build_lock_path(baseline_work_dir)
        experiment_lock = KnowledgePipeline._build_lock_path(experiment_work_dir)
        if baseline_lock.exists() or experiment_lock.exists():
            raise HTTPException(
                status_code=409,
                detail=(
                    "Promotion is blocked because a build lock exists for the baseline or experiment work_dir. "
                    "Wait for indexing to finish before promoting."
                ),
            )
        try:
            promotion = promote_experiment_workspace(
                experiment_work_dir=experiment_work_dir,
                baseline_work_dir=baseline_work_dir,
            )
        except ValueError as error:
            raise HTTPException(status_code=400, detail=str(error)) from error
        registry_path, stored = save_experiment_record(
            _experiments_root(settings),
            {
                "source_dir": str(settings.source_dir),
                "experiment_work_dir": str(experiment_work_dir),
                "baseline_work_dir": str(baseline_work_dir),
                "benchmark_path": request.benchmark_path or "",
                "content_type": request.content_type.strip() or "documents",
                "hypothesis": request.hypothesis.strip(),
                "notes": request.notes.strip(),
                "status": "promoted",
                "promotion": promotion,
                "source_alignment": source_alignment,
            },
        )
        pipeline._retriever_cache.pop(str(baseline_work_dir.resolve()), None)
        return {
            "experiment_id": stored["experiment_id"],
            "registry_path": str(registry_path),
            "status": stored["status"],
            "source_alignment": source_alignment,
            **promotion,
        }

    @app.post("/experiments/promote-sources")
    async def promote_sources(request: ExperimentPromoteSourcesRequest) -> dict[str, object]:
        experiment_source_dir = _strict_experiment_source_dir(request.experiment_source_dir, settings)
        baseline_source_dir = _ensure_source_dir(request.source_dir, settings)
        try:
            promotion = promote_experiment_sources(
                experiment_source_dir=experiment_source_dir,
                baseline_source_dir=baseline_source_dir,
            )
        except ValueError as error:
            raise HTTPException(status_code=400, detail=str(error)) from error
        experiment_work_dir = Path(request.experiment_work_dir) if request.experiment_work_dir else settings.work_dir
        baseline_work_dir = _resolve_work_dir(request.baseline_work_dir, settings)
        registry_path, stored = save_experiment_record(
            _experiments_root(settings),
            {
                "source_dir": str(baseline_source_dir),
                "experiment_source_dir": str(experiment_source_dir),
                "experiment_work_dir": str(experiment_work_dir),
                "baseline_work_dir": str(baseline_work_dir),
                "benchmark_path": request.benchmark_path or "",
                "content_type": request.content_type.strip() or "documents",
                "hypothesis": request.hypothesis.strip(),
                "notes": request.notes.strip(),
                "status": "sources_promoted",
                "source_promotion": promotion,
            },
        )
        return {
            "experiment_id": stored["experiment_id"],
            "registry_path": str(registry_path),
            "status": stored["status"],
            **promotion,
        }

    @app.post("/experiments/rollback")
    async def rollback_experiment_promotion(request: ExperimentRollbackRequest) -> dict[str, object]:
        baseline_work_dir = Path(request.baseline_work_dir)
        backup_work_dir = Path(request.backup_work_dir)
        baseline_lock = KnowledgePipeline._build_lock_path(baseline_work_dir)
        if baseline_lock.exists():
            raise HTTPException(
                status_code=409,
                detail=(
                    "Rollback is blocked because a build lock exists for the baseline work_dir. "
                    "Wait for indexing to finish before rolling back."
                ),
            )
        try:
            rollback = rollback_baseline_workspace(
                baseline_work_dir=baseline_work_dir,
                backup_work_dir=backup_work_dir,
            )
        except ValueError as error:
            raise HTTPException(status_code=400, detail=str(error)) from error
        experiment_work_dir = Path(request.experiment_work_dir) if request.experiment_work_dir else backup_work_dir
        registry_path, stored = save_experiment_record(
            _experiments_root(settings),
            {
                "source_dir": str(settings.source_dir),
                "experiment_work_dir": str(experiment_work_dir),
                "baseline_work_dir": str(baseline_work_dir),
                "benchmark_path": "",
                "content_type": request.content_type.strip() or "documents",
                "hypothesis": request.hypothesis.strip(),
                "notes": request.notes.strip(),
                "status": "rolled_back",
                "rollback": rollback,
            },
        )
        pipeline._retriever_cache.pop(str(baseline_work_dir.resolve()), None)
        return {
            "experiment_id": stored["experiment_id"],
            "registry_path": str(registry_path),
            "status": stored["status"],
            **rollback,
        }

    @app.post("/answer", response_model=AnswerResponse)
    async def answer(request: AnswerRequest) -> AnswerResponse:
        work_dir = _resolve_work_dir(request.work_dir, settings)
        _ensure_index_ready(work_dir)
        result = pipeline.answer(
            question=request.question,
            work_dir=work_dir,
            top_k=request.top_k,
        )
        evidence = [
            EvidenceResponse(
                block_id=hit.block.block_id,
                document_id=hit.block.document_id,
                title=hit.block.title,
                section_path=hit.block.section_path,
                block_type=hit.block.block_type,
                source_path=hit.block.source_path,
                start_anchor=hit.block.start_anchor,
                end_anchor=hit.block.end_anchor,
                text=hit.block.text,
                enriched_text=hit.block.enriched_text,
                score=round(hit.score, 4),
                lexical_score=round(hit.lexical_score, 4),
                vector_score=round(hit.vector_score, 4),
            )
            for hit in result.evidence
        ]
        return AnswerResponse(
            question=result.question,
            answer=result.answer,
            confidence=result.confidence,
            tier=result.tier,
            query_intent=result.query_intent,
            cached=result.cached,
            work_dir=str(work_dir),
            evidence=evidence,
        )

    @app.post("/review-answer", response_model=QueryReviewResponse)
    async def review_answer(request: QueryReviewRequest) -> QueryReviewResponse:
        work_dir = _resolve_work_dir(request.work_dir, settings)
        review_path = record_query_review(
            work_dir,
            {
                "question": request.question,
                "answer": request.answer,
                "confidence": request.confidence,
                "tier": request.tier,
                "query_intent": request.query_intent,
                "cached": request.cached,
                "rating": request.rating,
                "expected_document_id": request.expected_document_id,
                "expected_iso_code": request.expected_iso_code,
                "expected_terms": request.expected_terms,
                "notes": request.notes,
                "evidence_document_ids": request.evidence_document_ids,
                "evidence_block_ids": request.evidence_block_ids,
            },
        )
        payload = json.loads(review_path.read_text(encoding="utf-8"))
        entries = payload.get("entries", []) if isinstance(payload, dict) else []
        return QueryReviewResponse(
            saved=True,
            path=str(review_path),
            review_count=len(entries) if isinstance(entries, list) else 0,
        )

    @app.post("/evaluate")
    async def evaluate(request: EvaluateRequest) -> dict[str, object]:
        benchmark_path = _ensure_benchmark_path(request.benchmark_path)
        work_dir = _resolve_work_dir(request.work_dir, settings)
        _ensure_index_ready(work_dir)
        summary = pipeline.evaluate(
            benchmark_path=benchmark_path,
            work_dir=work_dir,
            top_k=request.top_k,
        )
        return {
            "total_cases": summary.total_cases,
            "retrieval_recall_at_k": summary.retrieval_recall_at_k,
            "evidence_hit_rate": summary.evidence_hit_rate,
            "citation_accuracy": summary.citation_accuracy,
            "document_precision_at_k": summary.document_precision_at_k,
            "no_answer_precision": summary.no_answer_precision,
            "answer_correctness": summary.answer_correctness,
            "country_match_at_1": summary.country_match_at_1,
            "foreign_evidence_rate": summary.foreign_evidence_rate,
            "wrong_country_answer_rate": summary.wrong_country_answer_rate,
            "diversity_enforcement_rate": summary.diversity_enforcement_rate,
            "answer_cache_hit_rate": summary.answer_cache_hit_rate,
            "cached_answer_count": summary.cached_answer_count,
            "tier_distribution": summary.tier_distribution,
            "failure_analysis": summary.failure_analysis,
            "fix_recommendations": summary.fix_recommendations,
            "results": [
                {
                    "question": result.question,
                    "question_type": result.question_type,
                    "query_intent": result.query_intent,
                    "routed_tier": result.routed_tier,
                    "answer_cached": result.answer_cached,
                    "retrieved_document_ids": result.retrieved_document_ids,
                    "retrieved_sections": result.retrieved_sections,
                    "citation_hit": result.citation_hit,
                    "failure_stage": result.failure_stage,
                    "failure_reasons": result.failure_reasons,
                    "answer_confidence": result.answer_confidence,
                    "country_match_at_1": result.country_match_at_1,
                    "foreign_evidence_present": result.foreign_evidence_present,
                    "forbidden_document_present": result.forbidden_document_present,
                    "mixed_document_violation": result.mixed_document_violation,
                }
                for result in summary.results
            ],
        }

    @app.post("/gate/run")
    async def run_gate(request: GateRunRequest) -> dict[str, object]:
        benchmark_path = _ensure_benchmark_path(request.benchmark_path)
        work_dir = _resolve_work_dir(request.work_dir, settings)
        _ensure_index_ready(work_dir)
        audit = audit_benchmark(
            benchmark_path,
            min_cases=request.min_cases,
            allow_low_count=request.allow_low_count,
        )
        gate_pipeline = pipeline
        if request.disable_query_cache:
            gate_pipeline = KnowledgePipeline(settings.model_copy(update={"query_cache_enabled": False}))
        summary = gate_pipeline.evaluate(
            benchmark_path=benchmark_path,
            work_dir=work_dir,
            top_k=request.top_k,
        )
        checks = [
            {
                "name": "Benchmark audit",
                "status": "pass" if audit["adequate"] else "fail",
                "value": len(audit.get("warnings", [])),
                "target": 0,
            },
            {
                "name": "Recall@k",
                "status": "pass" if summary.retrieval_recall_at_k >= 0.90 else "fail",
                "value": summary.retrieval_recall_at_k,
                "target": 0.90,
            },
            {
                "name": "Evidence hit rate",
                "status": "pass" if summary.evidence_hit_rate >= 0.90 else "fail",
                "value": summary.evidence_hit_rate,
                "target": 0.90,
            },
            {
                "name": "Answer correctness",
                "status": "pass" if summary.answer_correctness >= 0.90 else "fail",
                "value": summary.answer_correctness,
                "target": 0.90,
            },
        ]
        gate_passed = all(check["status"] == "pass" for check in checks)
        return {
            "status": "pass" if gate_passed else "fail",
            "work_dir": str(work_dir),
            "benchmark_path": str(benchmark_path),
            "evaluation_path": str(work_dir / "evaluation" / "latest-evaluation.json"),
            "audit": {
                "adequate": audit["adequate"],
                "total_cases": audit["total_cases"],
                "min_cases": audit["min_cases"],
                "warnings": audit.get("warnings", []),
                "allowed_low_count": audit.get("allowed_low_count", []),
                "allowed_low_count_findings": audit.get("allowed_low_count_findings", []),
            },
            "metrics": {
                "total_cases": summary.total_cases,
                "retrieval_recall_at_k": summary.retrieval_recall_at_k,
                "evidence_hit_rate": summary.evidence_hit_rate,
                "citation_accuracy": summary.citation_accuracy,
                "document_precision_at_k": summary.document_precision_at_k,
                "no_answer_precision": summary.no_answer_precision,
                "answer_correctness": summary.answer_correctness,
                "answer_cache_hit_rate": summary.answer_cache_hit_rate,
                "cached_answer_count": summary.cached_answer_count,
            },
            "checks": checks,
        }

    @app.post("/calibrate-refusal")
    async def calibrate_refusal(request: CalibrateRequest) -> dict[str, object]:
        benchmark_path = _ensure_benchmark_path(request.benchmark_path)
        work_dir = _resolve_work_dir(request.work_dir, settings)
        _ensure_index_ready(work_dir)
        report = pipeline.calibrate_refusal(
            benchmark_path=benchmark_path,
            work_dir=work_dir,
            top_k=request.top_k,
        )
        return {
            "recommended_min_score_threshold": report.recommended_min_score_threshold,
            "recommended_min_overlap_ratio": report.recommended_min_overlap_ratio,
            "recommended_tier0_score_threshold": report.recommended_tier0_score_threshold,
            "recommended_tier2_score_threshold": report.recommended_tier2_score_threshold,
            "total_cases": report.total_cases,
            "answerable_cases": report.answerable_cases,
            "refusal_cases": report.refusal_cases,
            "candidate_count": report.candidate_count,
            "recommended_no_answer_precision": report.recommended_no_answer_precision,
            "recommended_answer_correctness": report.recommended_answer_correctness,
            "recommended_evidence_hit_rate": report.recommended_evidence_hit_rate,
            "recommended_retrieval_recall_at_k": report.recommended_retrieval_recall_at_k,
            "recommended_tier0_1_share": report.recommended_tier0_1_share,
            "recommended_tier2_share": report.recommended_tier2_share,
            "recommended_refusal_share": report.recommended_refusal_share,
            "meets_query_mix_target": report.meets_query_mix_target,
            "candidates": [
                {
                    "min_score_threshold": candidate.min_score_threshold,
                    "min_overlap_ratio": candidate.min_overlap_ratio,
                    "tier0_score_threshold": candidate.tier0_score_threshold,
                    "tier2_score_threshold": candidate.tier2_score_threshold,
                    "no_answer_precision": candidate.no_answer_precision,
                    "answer_correctness": candidate.answer_correctness,
                    "evidence_hit_rate": candidate.evidence_hit_rate,
                    "retrieval_recall_at_k": candidate.retrieval_recall_at_k,
                    "tier0_1_share": candidate.tier0_1_share,
                    "tier2_share": candidate.tier2_share,
                    "refusal_share": candidate.refusal_share,
                }
                for candidate in report.candidates
            ],
        }

    @app.post("/explain-block", response_model=ExplainBlockResponse)
    async def explain_block(request: ExplainBlockRequest) -> ExplainBlockResponse:
        work_dir = _resolve_work_dir(request.work_dir, settings)
        _ensure_index_ready(work_dir)
        block = pipeline.get_block(request.block_id, work_dir=work_dir)
        if block is None:
            raise HTTPException(status_code=404, detail=f"Block not found: {request.block_id}")

        return ExplainBlockResponse(
            block_id=block.block_id,
            document_id=block.document_id,
            title=block.title,
            section_path=block.section_path,
            block_type=block.block_type,
            text=block.text,
            enriched_text=block.enriched_text,
            enrichment_provider=block.enrichment_provider,
            enrichment_model=block.enrichment_model,
            enriched_at=block.enriched_at,
            hypothetical_questions=block.hypothetical_questions,
            local_aliases=block.local_aliases,
            reasoning=block.reasoning,
            answer_signal=block.answer_signal,
            quality_status=block.quality_status,
            canonical_terms=block.canonical_terms,
            metadata=block.metadata,
        )

    @app.post("/low-quality-blocks")
    async def low_quality_blocks(request: LowQualityBlocksRequest) -> dict[str, object]:
        work_dir = _resolve_work_dir(request.work_dir, settings)
        _ensure_index_ready(work_dir)
        blocks_payload = _load_blocks_payload(work_dir)
        raw_low_quality = [
            block
            for block in blocks_payload
            if str(block.get("quality_status") or "ok") == "LOW_QUALITY"
        ]
        accepted = [
            block
            for block in raw_low_quality
            if _effective_quality_status(block) == "ok"
        ]
        review_needed = [
            block
            for block in raw_low_quality
            if _effective_quality_status(block) == "LOW_QUALITY"
        ]
        selected = raw_low_quality if request.include_accepted else review_needed
        items = []
        for block in selected[: request.limit]:
            metadata = block.get("metadata") if isinstance(block.get("metadata"), dict) else {}
            items.append(
                {
                    "block_id": block.get("block_id", ""),
                    "document_id": block.get("document_id", ""),
                    "title": block.get("title", ""),
                    "source_path": block.get("source_path", ""),
                    "section_path": block.get("section_path", []),
                    "block_type": block.get("block_type", ""),
                    "quality_status": block.get("quality_status", ""),
                    "effective_quality_status": _effective_quality_status(block),
                    "reasons": _low_quality_review_reasons(block),
                    "text": block.get("text", ""),
                    "enriched_text": block.get("enriched_text", ""),
                    "country": block.get("country", ""),
                    "iso_code": block.get("iso_code", ""),
                    "metadata": {
                        "structured_field": metadata.get("structured_field", ""),
                        "structured_value": metadata.get("structured_value", ""),
                        "row_values": metadata.get("row_values", ""),
                        "content_type": metadata.get("content_type", ""),
                    },
                }
            )
        return {
            "work_dir": str(work_dir),
            "raw_low_quality_blocks": len(raw_low_quality),
            "effectively_ok_blocks": len(accepted),
            "review_needed_blocks": len(review_needed),
            "returned_blocks": len(items),
            "limit": request.limit,
            "include_accepted": request.include_accepted,
            "blocks": items,
        }

    return app
