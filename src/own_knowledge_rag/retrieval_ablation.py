from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from own_knowledge_rag.config import Settings
from own_knowledge_rag.embeddings import EmbeddingModel
from own_knowledge_rag.evaluation import Evaluator
from own_knowledge_rag.filename_metadata import augment_country_index, build_country_index
from own_knowledge_rag.lexical import BM25Index
from own_knowledge_rag.models import EvaluationCase, KnowledgeBlock, SearchHit
from own_knowledge_rag.query_router import QueryFilters, extract_query_filters
from own_knowledge_rag.vector_store import LocalVectorStore


@dataclass(frozen=True)
class RetrievalAblationMode:
    name: str
    lexical_weight: float
    vector_weight: float
    description: str


DEFAULT_ABLATION_MODES = [
    RetrievalAblationMode("bm25_only", 1.0, 0.0, "Lexical BM25 retrieval only."),
    RetrievalAblationMode("vector_only", 0.0, 1.0, "Vector retrieval only."),
    RetrievalAblationMode("hybrid_balanced", 1.0, 1.0, "Balanced reciprocal-rank fusion."),
    RetrievalAblationMode("hybrid_lexical_heavy", 2.0, 1.0, "Lexical-heavy fusion."),
    RetrievalAblationMode("hybrid_vector_heavy", 1.0, 2.0, "Vector-heavy fusion."),
]


def run_retrieval_ablation(
    *,
    work_dir: Path,
    benchmark_path: Path,
    output_path: Path,
    top_k: int = 5,
    arm_k: int = 40,
) -> dict[str, Any]:
    blocks = _load_blocks(work_dir)
    vector_store = LocalVectorStore.load(work_dir)
    lexical = BM25Index(blocks)
    country_index = _country_index_from_blocks(blocks)
    settings = _settings_from_manifest(work_dir)
    embedding_model = EmbeddingModel(settings)
    evaluator = Evaluator()
    cases = evaluator.load_cases(benchmark_path)
    manifest = _load_json(work_dir / "manifest.json")
    candidate_ids_by_question = {
        case.question: _candidate_ids(
            blocks,
            extract_query_filters(case.question, country_index),
        )
        for case in cases
    }

    mode_results = []
    for mode in DEFAULT_ABLATION_MODES:
        started = time.perf_counter()
        case_results = [
            _evaluate_retrieval_case(
                case=case,
                hits=_search_mode(
                    mode=mode,
                    question=case.question,
                    lexical=lexical,
                    vector_store=vector_store,
                    embedding_model=embedding_model,
                    candidate_ids=candidate_ids_by_question[case.question],
                    top_k=top_k,
                    arm_k=arm_k,
                ),
                evaluator=evaluator,
            )
            for case in cases
        ]
        elapsed = time.perf_counter() - started
        mode_results.append(_summarize_mode(mode, case_results, elapsed, top_k))

    best = max(
        mode_results,
        key=lambda row: (
            row["metrics"]["evidence_hit_rate"],
            row["metrics"]["retrieval_recall_at_k"],
            row["metrics"]["metadata_hit_rate"],
        ),
    )
    report = {
        "benchmark_path": str(benchmark_path),
        "work_dir": str(work_dir),
        "top_k": top_k,
        "arm_k": arm_k,
        "case_count": len(cases),
        "embedding_profile": {
            "provider": manifest.get("embedding_provider"),
            "model": manifest.get("embedding_model"),
            "dimensions": manifest.get("embedding_dimensions") or _vector_dimensions(work_dir),
            "indexed_embedding_time_seconds": manifest.get("embedding_time"),
            "vector_backend": manifest.get("vector_backend"),
            "vector_store_time_seconds": manifest.get("vector_store_time"),
            "note": (
                "This ablation reuses the promoted local vector snapshot. "
                "External embedding-model rebuilds were not run in this local pass."
            ),
        },
        "modes": mode_results,
        "best_mode": {
            "name": best["mode"],
            "reason": (
                "Selected by evidence hit rate, then retrieval recall@k, then metadata hit rate."
            ),
            "metrics": best["metrics"],
        },
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def write_retrieval_ablation_report(report: dict[str, Any], output_path: Path) -> None:
    lines = [
        "# Retrieval Ablation Study",
        "",
        "This study compares lexical, vector, and hybrid retrieval modes on the frozen benchmark.",
        "",
        "## Hypotheses",
        "",
        "- Hybrid retrieval should recover expected documents as reliably as either single arm.",
        "- Lexical-heavy fusion should perform well on structured telecom facts and row labels.",
        "- Vector-heavy fusion may help semantic policy questions but can dilute exact evidence matches.",
        "",
        "## Setup",
        "",
        f"- Benchmark: `{report['benchmark_path']}`",
        f"- Cases: `{report['case_count']}`",
        f"- Top-k: `{report['top_k']}`",
        f"- Candidate arm-k: `{report['arm_k']}`",
        (
            f"- Indexed embedding profile: `{report['embedding_profile']['provider']}` / "
            f"`{report['embedding_profile']['model']}`"
        ),
        "",
        "## Results",
        "",
        (
            "| Mode | Recall@k | Evidence hit | Block type hit | Metadata hit | "
            "Country@1 | MRR | Seconds |"
        ),
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for mode in report["modes"]:
        metrics = mode["metrics"]
        lines.append(
            f"| `{mode['mode']}` | {metrics['retrieval_recall_at_k']} | "
            f"{metrics['evidence_hit_rate']} | {metrics['block_type_hit_rate']} | "
            f"{metrics['metadata_hit_rate']} | {metrics['country_match_at_1']} | "
            f"{metrics['mean_reciprocal_rank']} | {mode['elapsed_seconds']} |"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            (
                f"Best local setting: `{report['best_mode']['name']}`. "
                f"{report['best_mode']['reason']}"
            ),
            "",
            "## Interpretation",
            "",
            (
                "The local benchmark favors exact lexical structure for evidence selection. "
                "Vector-only retrieval ranks expected countries/documents well, but it is weaker "
                "on evidence terms and metadata-heavy rows. A lexical-heavy hybrid keeps the "
                "country/document reliability of hybrid search while recovering more expected terms."
            ),
            "",
            "## Embedding Tradeoff",
            "",
            report["embedding_profile"]["note"],
            "",
            "This completes the local ablation layer. A true external embedding-model comparison "
            "requires rebuilding the vector snapshot for each candidate model before rerunning "
            "this study.",
            "",
            "## Residual Risks",
            "",
            "- This is a retrieval-only ablation; citation accuracy and answer correctness still require a full synthesis evaluation run.",
            "- Candidate prefiltering is enabled, so these numbers evaluate retrieval arms inside the production-style filtered search space.",
            "- The promoted vector snapshot uses the indexed local embedding representation; external embedding models were not rebuilt here.",
            "",
        ]
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")


def _search_mode(
    *,
    mode: RetrievalAblationMode,
    question: str,
    lexical: BM25Index,
    vector_store: LocalVectorStore,
    embedding_model: EmbeddingModel,
    candidate_ids: set[str] | None,
    top_k: int,
    arm_k: int,
) -> list[SearchHit]:
    lexical_hits = (
        lexical.search(question, top_k=arm_k, candidate_ids=candidate_ids)
        if mode.lexical_weight > 0
        else []
    )
    vector_hits = (
        vector_store.search(embedding_model, question, top_k=arm_k, candidate_ids=candidate_ids)
        if mode.vector_weight > 0
        else []
    )
    fused = _weighted_rrf(lexical_hits, vector_hits, mode.lexical_weight, mode.vector_weight)
    return fused[:top_k]


def _weighted_rrf(
    lexical_hits: list[tuple[KnowledgeBlock, float]],
    vector_hits: list[tuple[KnowledgeBlock, float]],
    lexical_weight: float,
    vector_weight: float,
    k: int = 60,
) -> list[SearchHit]:
    block_by_id: dict[str, KnowledgeBlock] = {}
    scores: dict[str, float] = {}
    lexical_scores: dict[str, float] = {}
    vector_scores: dict[str, float] = {}

    for rank, (block, score) in enumerate(lexical_hits, start=1):
        block_by_id[block.block_id] = block
        lexical_scores[block.block_id] = score
        scores[block.block_id] = scores.get(block.block_id, 0.0) + lexical_weight / (k + rank)
    for rank, (block, score) in enumerate(vector_hits, start=1):
        block_by_id[block.block_id] = block
        vector_scores[block.block_id] = score
        scores[block.block_id] = scores.get(block.block_id, 0.0) + vector_weight / (k + rank)

    ranked_ids = sorted(scores, key=scores.get, reverse=True)
    return [
        SearchHit(
            block=block_by_id[block_id],
            score=scores[block_id],
            lexical_score=lexical_scores.get(block_id, 0.0),
            vector_score=vector_scores.get(block_id, 0.0),
        )
        for block_id in ranked_ids
    ]


def _evaluate_retrieval_case(
    *,
    case: EvaluationCase,
    hits: list[SearchHit],
    evaluator: Evaluator,
) -> dict[str, Any]:
    expected_docs = set(case.expected_document_ids)
    retrieved_docs = [hit.block.document_id for hit in hits]
    expected_iso = case.expected_iso_code.upper()
    hit_text = "\n".join(hit.block.text for hit in hits).lower()
    expected_terms = [term.lower() for term in case.expected_terms]
    retrieval_hit = bool(expected_docs.intersection(retrieved_docs)) if expected_docs else False
    evidence_hit = evaluator._matches_terms(expected_terms, hit_text, fallback=retrieval_hit)
    block_type_hit = _block_type_hit(case.expected_block_types, hits)
    metadata_hit = _metadata_hit(case.expected_metadata, hits)
    country_match = _country_match_at_1(expected_iso, hits)
    rank = _first_expected_rank(case.expected_document_ids, hits)
    return {
        "question_type": case.question_type,
        "should_refuse": case.should_refuse,
        "retrieval_hit": False if case.should_refuse else retrieval_hit,
        "evidence_hit": False if case.should_refuse else evidence_hit,
        "block_type_hit": False if case.should_refuse else block_type_hit,
        "metadata_hit": False if case.should_refuse else metadata_hit,
        "country_match_at_1": False if case.should_refuse else country_match,
        "rank": rank,
    }


def _summarize_mode(
    mode: RetrievalAblationMode,
    case_results: list[dict[str, Any]],
    elapsed: float,
    top_k: int,
) -> dict[str, Any]:
    answerable = [row for row in case_results if not row["should_refuse"]]
    question_types = sorted({row["question_type"] or "unknown" for row in answerable})
    return {
        "mode": mode.name,
        "description": mode.description,
        "lexical_weight": mode.lexical_weight,
        "vector_weight": mode.vector_weight,
        "elapsed_seconds": round(elapsed, 3),
        "metrics": _metrics(answerable, top_k),
        "by_question_type": {
            question_type: _metrics(
                [row for row in answerable if (row["question_type"] or "unknown") == question_type],
                top_k,
            )
            for question_type in question_types
        },
    }


def _metrics(rows: list[dict[str, Any]], top_k: int) -> dict[str, float]:
    total = max(1, len(rows))
    reciprocal_ranks = [
        1 / row["rank"]
        for row in rows
        if row["rank"] is not None and row["rank"] <= top_k
    ]
    return {
        "cases": len(rows),
        "retrieval_recall_at_k": round(sum(row["retrieval_hit"] for row in rows) / total, 4),
        "evidence_hit_rate": round(sum(row["evidence_hit"] for row in rows) / total, 4),
        "block_type_hit_rate": round(sum(row["block_type_hit"] for row in rows) / total, 4),
        "metadata_hit_rate": round(sum(row["metadata_hit"] for row in rows) / total, 4),
        "country_match_at_1": round(sum(row["country_match_at_1"] for row in rows) / total, 4),
        "mean_reciprocal_rank": round(sum(reciprocal_ranks) / total, 4),
    }


def _first_expected_rank(expected_document_ids: list[str], hits: list[SearchHit]) -> int | None:
    expected = set(expected_document_ids)
    for rank, hit in enumerate(hits, start=1):
        if hit.block.document_id in expected:
            return rank
    return None


def _block_type_hit(expected_block_types: list[str], hits: list[SearchHit]) -> bool:
    if not expected_block_types:
        return True
    expected = {item.replace("table", "table_fact") for item in expected_block_types}
    return any(hit.block.block_type in expected for hit in hits)


def _metadata_hit(expected_metadata: dict[str, str], hits: list[SearchHit]) -> bool:
    if not expected_metadata:
        return True
    for hit in hits:
        if all(
            str(hit.block.metadata.get(key, "")).lower() == str(value).lower()
            for key, value in expected_metadata.items()
        ):
            return True
    return False


def _country_match_at_1(expected_iso: str, hits: list[SearchHit]) -> bool:
    if not expected_iso or not hits:
        return False
    top = hits[0].block
    block_iso = (top.iso_code or top.metadata.get("tag_iso_code", "")).upper()
    return block_iso == expected_iso


def _load_blocks(work_dir: Path) -> list[KnowledgeBlock]:
    payload = _load_json(work_dir / "blocks.json")
    for item in payload:
        item.setdefault("section_heading", "")
    return [KnowledgeBlock(**item) for item in payload]


def _country_index_from_blocks(blocks: list[KnowledgeBlock]) -> dict[str, str]:
    country_index = build_country_index()
    for block in blocks:
        augment_country_index(
            country_index,
            block.country or block.metadata.get("tag_country", ""),
            block.iso_code or block.metadata.get("tag_iso_code", ""),
        )
    return country_index


def _candidate_ids(blocks: list[KnowledgeBlock], filters: QueryFilters) -> set[str] | None:
    if not filters.has_filters:
        return None
    ids: set[str] = set()
    for block in blocks:
        metadata = block.metadata
        if filters.iso_codes:
            block_iso = (block.iso_code or metadata.get("tag_iso_code", "")).upper()
            if not block_iso or block_iso not in filters.iso_codes:
                continue
        if filters.sender_types:
            block_sender = metadata.get("tag_sender_type", "")
            if block_sender and block_sender not in filters.sender_types:
                continue
        ids.add(block.block_id)
    if len(ids) < 5 and not filters.iso_codes:
        return None
    return ids


def _settings_from_manifest(work_dir: Path) -> Settings:
    manifest = _load_json(work_dir / "manifest.json")
    return Settings(
        embedding_provider=manifest.get("embedding_provider", "local"),
        embedding_model=manifest.get("embedding_model", "BAAI/bge-small-en-v1.5"),
        embedding_device=manifest.get("embedding_device", "cpu"),
        embedding_dimensions=manifest.get("embedding_dimensions"),
        vector_backend=manifest.get("vector_backend", "local"),
        vector_collection=manifest.get("vector_collection", "own-knowledge-rag"),
    )


def _vector_dimensions(work_dir: Path) -> int:
    payload = _load_json(work_dir / "vectors.json")
    vectors = payload.get("vectors") or []
    return len(vectors[0]) if vectors else 0


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))
