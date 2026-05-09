"""Generate Phase 20 embedding and country-precision diagnostics."""

from __future__ import annotations

import csv
import json
import random
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.neighbors import NearestNeighbors


ROOT = Path(__file__).resolve().parents[1]
WORK_DIR = ROOT / "data/work"
TABLE_DIR = ROOT / "reports/tables"
VECTOR_PATH = WORK_DIR / "vectors.json"
EVALUATION_PATH = WORK_DIR / "evaluation/latest-evaluation.json"


def main() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)

    vector_payload = _read_json(VECTOR_PATH)
    blocks = vector_payload.get("blocks", [])
    vectors = vector_payload.get("vectors", [])
    embedding_metrics, anomalous_blocks = embedding_diagnostics(blocks, vectors)

    (TABLE_DIR / "embedding_cluster_metrics.json").write_text(
        json.dumps(embedding_metrics, indent=2),
        encoding="utf-8",
    )
    _write_csv(TABLE_DIR / "embedding_anomalous_blocks.csv", anomalous_blocks)

    evaluation_payload = _read_json(EVALUATION_PATH)
    foreign_evidence_rows, foreign_summary = foreign_evidence_audit(evaluation_payload)
    _write_csv(TABLE_DIR / "foreign_evidence_audit.csv", foreign_evidence_rows)
    (TABLE_DIR / "foreign_evidence_audit_summary.json").write_text(
        json.dumps(foreign_summary, indent=2),
        encoding="utf-8",
    )

    print(
        "Phase 20 diagnostics complete: "
        f"silhouette={embedding_metrics['global_silhouette_score']}, "
        f"anomalous_blocks={len(anomalous_blocks)}, "
        f"country_precision_cases={len(foreign_evidence_rows)}"
    )


def embedding_diagnostics(
    blocks: list[dict[str, Any]],
    vectors: list[list[float]],
    *,
    sample_size: int = 2500,
    neighbor_count: int = 12,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    paired_count = min(len(blocks), len(vectors))
    if paired_count == 0:
        return (
            {
                "vector_count": len(vectors),
                "block_count": len(blocks),
                "sample_size": 0,
                "global_silhouette_score": None,
                "warning": "No paired blocks/vectors available.",
            },
            [],
        )

    indices = _stratified_sample_indices(blocks[:paired_count], sample_size=sample_size)
    sample_blocks = [blocks[index] for index in indices]
    sample_vectors = np.array([vectors[index] for index in indices], dtype=float)
    labels = [block.get("block_type") or "unknown" for block in sample_blocks]

    label_counts = Counter(labels)
    usable_positions = [
        position
        for position, label in enumerate(labels)
        if label_counts[label] >= 2
    ]
    if len({labels[position] for position in usable_positions}) < 2:
        global_score = None
        by_block_type: dict[str, dict[str, Any]] = {}
        warning = "Need at least two labels with at least two samples each for silhouette."
    else:
        usable_vectors = sample_vectors[usable_positions]
        usable_labels = [labels[position] for position in usable_positions]
        sample_scores = silhouette_samples(usable_vectors, usable_labels, metric="cosine")
        global_score = round(
            float(silhouette_score(usable_vectors, usable_labels, metric="cosine")),
            4,
        )
        by_block_type = {}
        score_by_label: dict[str, list[float]] = {}
        for label, score in zip(usable_labels, sample_scores, strict=True):
            score_by_label.setdefault(label, []).append(float(score))
        for label, scores in sorted(score_by_label.items()):
            by_block_type[label] = {
                "sample_count": len(scores),
                "mean_silhouette": round(float(np.mean(scores)), 4),
                "median_silhouette": round(float(np.median(scores)), 4),
            }
        warning = ""

    anomalous_blocks = _embedding_anomalies(
        blocks=blocks,
        vectors=vectors,
        paired_count=paired_count,
        neighbor_count=neighbor_count,
    )

    metrics = {
        "vector_count": len(vectors),
        "block_count": len(blocks),
        "paired_count": paired_count,
        "sample_size": len(indices),
        "random_seed": 42,
        "label": "block_type",
        "metric": "cosine",
        "global_silhouette_score": global_score,
        "by_block_type": by_block_type,
        "block_type_counts_in_sample": dict(sorted(label_counts.items())),
        "anomalous_block_count": len(anomalous_blocks),
        "anomalous_block_artifact": "reports/tables/embedding_anomalous_blocks.csv",
        "warning": warning,
    }
    return metrics, anomalous_blocks


def _stratified_sample_indices(
    blocks: list[dict[str, Any]],
    *,
    sample_size: int,
) -> list[int]:
    rng = random.Random(42)
    grouped: dict[str, list[int]] = {}
    for index, block in enumerate(blocks):
        grouped.setdefault(block.get("block_type") or "unknown", []).append(index)
    target_size = min(sample_size, len(blocks))
    selected: set[int] = set()
    for group_indices in grouped.values():
        selected.update(rng.sample(group_indices, min(2, len(group_indices))))
    remaining_slots = max(0, target_size - len(selected))
    remaining = [index for index in range(len(blocks)) if index not in selected]
    if remaining_slots:
        selected.update(rng.sample(remaining, min(remaining_slots, len(remaining))))
    return sorted(selected)


def _embedding_anomalies(
    *,
    blocks: list[dict[str, Any]],
    vectors: list[list[float]],
    paired_count: int,
    neighbor_count: int,
    max_rows: int = 100,
) -> list[dict[str, Any]]:
    matrix = np.array(vectors[:paired_count], dtype=float)
    labels = [blocks[index].get("block_type") or "unknown" for index in range(paired_count)]
    n_neighbors = min(neighbor_count + 1, paired_count)
    if n_neighbors <= 2:
        return []

    neighbors = NearestNeighbors(n_neighbors=n_neighbors, metric="cosine")
    neighbors.fit(matrix)
    distances, indices = neighbors.kneighbors(matrix, return_distance=True)

    rows: list[dict[str, Any]] = []
    for row_index, (neighbor_indices, neighbor_distances) in enumerate(zip(indices, distances, strict=True)):
        local_indices = [
            int(index)
            for index in neighbor_indices
            if int(index) != row_index
        ][:neighbor_count]
        if not local_indices:
            continue
        neighbor_labels = [labels[index] for index in local_indices]
        majority_label, majority_count = Counter(neighbor_labels).most_common(1)[0]
        own_label = labels[row_index]
        majority_share = majority_count / len(local_indices)
        if majority_label == own_label or majority_share < 0.6:
            continue
        block = blocks[row_index]
        nearest_distance = next(
            float(distance)
            for index, distance in zip(neighbor_indices, neighbor_distances, strict=True)
            if int(index) != row_index
        )
        metadata = block.get("metadata") or {}
        rows.append(
            {
                "block_id": block.get("block_id", ""),
                "document_id": block.get("document_id", ""),
                "source_path": block.get("source_path", ""),
                "block_type": own_label,
                "neighbor_majority_block_type": majority_label,
                "neighbor_majority_share": round(majority_share, 4),
                "nearest_neighbor_distance": round(nearest_distance, 4),
                "row_key": metadata.get("row_key", ""),
                "quality_status": block.get("quality_status", ""),
                "text_preview": _preview(block.get("text", "")),
            }
        )

    rows.sort(
        key=lambda row: (
            -float(row["neighbor_majority_share"]),
            float(row["nearest_neighbor_distance"]),
            row["document_id"],
            row["block_id"],
        )
    )
    return rows[:max_rows]


def foreign_evidence_audit(
    evaluation_payload: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for result in evaluation_payload.get("results", []):
        expected_iso = result.get("expected_iso_code") or ""
        is_country_case = bool(expected_iso)
        foreign_evidence = bool(result.get("foreign_evidence_present"))
        wrong_country = is_country_case and not bool(result.get("country_match_at_1"))
        if not (foreign_evidence or wrong_country):
            continue
        retrieved_documents = result.get("retrieved_document_ids") or []
        expected_documents = result.get("expected_document_ids") or []
        expected_prefix = expected_iso.lower()
        top_document = retrieved_documents[0] if retrieved_documents else ""
        rows.append(
            {
                "question": result.get("question", ""),
                "question_type": result.get("question_type", ""),
                "expected_iso_code": expected_iso,
                "expected_document_ids": ";".join(expected_documents),
                "top_document_id": top_document,
                "retrieved_document_ids": ";".join(retrieved_documents),
                "country_match_at_1": result.get("country_match_at_1"),
                "foreign_evidence_present": foreign_evidence,
                "answer_correct": result.get("answer_correct"),
                "citation_hit": result.get("citation_hit"),
                "evidence_hit": result.get("evidence_hit"),
                "failure_stage": result.get("failure_stage") or "",
                "failure_reasons": ";".join(result.get("failure_reasons") or []),
                "likely_cause": _country_precision_cause(
                    expected_iso=expected_prefix,
                    top_document=top_document,
                    retrieved_documents=retrieved_documents,
                    expected_documents=expected_documents,
                    foreign_evidence=foreign_evidence,
                    answer_correct=bool(result.get("answer_correct")),
                ),
                "answer_text": result.get("answer_text", ""),
            }
        )

    rows.sort(
        key=lambda row: (
            row["expected_iso_code"],
            row["question_type"],
            row["question"],
        )
    )
    causes = Counter(row["likely_cause"] for row in rows)
    summary = {
        "total_cases": evaluation_payload.get("total_cases", 0),
        "audited_case_count": len(rows),
        "foreign_evidence_case_count": sum(int(row["foreign_evidence_present"]) for row in rows),
        "wrong_country_case_count": sum(not bool(row["country_match_at_1"]) for row in rows),
        "answer_correct_count": sum(int(bool(row["answer_correct"])) for row in rows),
        "likely_cause_counts": dict(sorted(causes.items())),
        "artifact": "reports/tables/foreign_evidence_audit.csv",
    }
    return rows, summary


def _country_precision_cause(
    *,
    expected_iso: str,
    top_document: str,
    retrieved_documents: list[str],
    expected_documents: list[str],
    foreign_evidence: bool,
    answer_correct: bool,
) -> str:
    if top_document in expected_documents and foreign_evidence:
        return "citation_or_evidence_anchor_mixed_country"
    if top_document not in expected_documents and any(doc in expected_documents for doc in retrieved_documents):
        return "reranking_put_foreign_or_ambiguous_result_first"
    if expected_iso and top_document and expected_iso not in top_document.lower():
        return "metadata_filter_or_country_alias_leakage"
    if answer_correct and foreign_evidence:
        return "correct_answer_with_foreign_evidence"
    return "needs_manual_review"


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _preview(text: str, limit: int = 180) -> str:
    cleaned = " ".join(text.split())
    return cleaned[: limit - 1] + "..." if len(cleaned) > limit else cleaned


if __name__ == "__main__":
    main()
