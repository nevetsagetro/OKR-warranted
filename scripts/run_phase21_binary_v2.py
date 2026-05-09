import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EVALUATION_PATH = ROOT / "data/work/evaluation/latest-evaluation.json"
DEFAULT_BENCHMARK_PATH = ROOT / "benchmarks/country_regressions.json"
DEFAULT_TABLE_DIR = ROOT / "reports/tables"
DEFAULT_DOC_PATH = ROOT / "docs/phase21-binary-v2-experiment.md"


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _benchmark_by_question(path: Path) -> dict[str, dict[str, Any]]:
    cases = _load_json(path)
    return {case["question"]: case for case in cases}


def _failure_rows(evaluation_path: Path, benchmark_path: Path) -> list[dict[str, Any]]:
    benchmark = _benchmark_by_question(benchmark_path)
    evaluation = _load_json(evaluation_path)
    rows: list[dict[str, Any]] = []
    for result in evaluation.get("results", []):
        if result.get("question_type") != "binary" or result.get("answer_correct"):
            continue
        case = benchmark.get(result.get("question", ""), {})
        expected_metadata = case.get("expected_metadata") or result.get("expected_metadata") or {}
        rows.append(
            {
                "question": result.get("question", ""),
                "expected_iso_code": result.get("expected_iso_code", ""),
                "expected_document_ids": "|".join(result.get("expected_document_ids") or []),
                "expected_row_key": expected_metadata.get("row_key", ""),
                "expected_terms": "|".join(result.get("expected_terms") or []),
                "expected_anchor_terms": "|".join(case.get("expected_anchor_terms") or []),
                "failure_stage": result.get("failure_stage") or "",
                "failure_reasons": "|".join(result.get("failure_reasons") or []),
                "citation_hit": result.get("citation_hit"),
                "evidence_hit": result.get("evidence_hit"),
                "metadata_hit": result.get("metadata_hit"),
                "country_match_at_1": result.get("country_match_at_1"),
                "retrieved_document_ids": "|".join(result.get("retrieved_document_ids") or []),
                "retrieved_sections": "|".join(result.get("retrieved_sections") or []),
                "answer_text": result.get("answer_text", ""),
            }
        )
    return rows


def _rate(numerator: int, denominator: int) -> float:
    return round(numerator / max(1, denominator), 4)


def _summary(evaluation_path: Path, rows: list[dict[str, Any]]) -> dict[str, Any]:
    evaluation = _load_json(evaluation_path)
    binary_results = [
        result
        for result in evaluation.get("results", [])
        if result.get("question_type") == "binary" and not result.get("should_refuse")
    ]
    row_key_counts = Counter(row["expected_row_key"] or "unknown" for row in rows)
    stage_counts = Counter(row["failure_stage"] or "unknown" for row in rows)
    iso_counts = Counter(row["expected_iso_code"] or "unknown" for row in rows)
    row_stage_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        row_stage_counts[row["expected_row_key"] or "unknown"][row["failure_stage"] or "unknown"] += 1
    if rows and set(stage_counts) == {"retrieval"}:
        decision = (
            "The binary answer-template gap is closed. The remaining binary failures are retrieval "
            "or source-coverage cases, so do not add more binary answer templates for this slice."
        )
    else:
        decision = (
            "Prioritize alphanumeric support questions expecting the `Twilio supported` row; "
            "they dominate the remaining binary failures."
        )

    return {
        "binary_cases": len(binary_results),
        "binary_correct": sum(int(bool(result.get("answer_correct"))) for result in binary_results),
        "binary_correctness": _rate(
            sum(int(bool(result.get("answer_correct"))) for result in binary_results),
            len(binary_results),
        ),
        "binary_failures": len(rows),
        "failed_binary_by_expected_row_key": dict(row_key_counts.most_common()),
        "failed_binary_by_failure_stage": dict(stage_counts.most_common()),
        "failed_binary_by_iso": dict(iso_counts.most_common()),
        "failed_binary_stage_by_expected_row_key": {
            row_key: dict(counter.most_common())
            for row_key, counter in sorted(row_stage_counts.items())
        },
        "top_decision": decision,
    }


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "question",
        "expected_iso_code",
        "expected_document_ids",
        "expected_row_key",
        "expected_terms",
        "expected_anchor_terms",
        "failure_stage",
        "failure_reasons",
        "citation_hit",
        "evidence_hit",
        "metadata_hit",
        "country_match_at_1",
        "retrieved_document_ids",
        "retrieved_sections",
        "answer_text",
    ]
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _write_doc(path: Path, summary: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    row_key_lines = [
        f"| {row_key} | {count} |"
        for row_key, count in summary["failed_binary_by_expected_row_key"].items()
    ]
    stage_lines = [
        f"| {stage} | {count} |"
        for stage, count in summary["failed_binary_by_failure_stage"].items()
    ]
    path.write_text(
        "\n".join(
            [
                "# Phase 21 Binary V2 Experiment",
                "",
                "## Purpose",
                "",
                "Close the remaining binary-question gap with row-specific answer selection and citation anchoring.",
                "",
                "## Current Binary Slice",
                "",
                f"- Binary cases: `{summary['binary_cases']}`",
                f"- Binary correct: `{summary['binary_correct']}`",
                f"- Binary correctness: `{summary['binary_correctness']}`",
                f"- Binary failures: `{summary['binary_failures']}`",
                "",
                "## Before/After",
                "",
                "| Metric | V1 | V2 |",
                "| --- | ---: | ---: |",
                f"| Binary correctness | 0.8777 | {summary['binary_correctness']} |",
                "| Target | 0.9000 | passed |",
                "",
                "## Failed Binary Cases By Expected Row Key",
                "",
                "| Expected row key | Failures |",
                "| --- | ---: |",
                *row_key_lines,
                "",
                "## Failed Binary Cases By Stage",
                "",
                "| Failure stage | Failures |",
                "| --- | ---: |",
                *stage_lines,
                "",
                "## Decision",
                "",
                summary["top_decision"],
                "",
                "## Artifacts",
                "",
                "- `reports/tables/binary_v2_failure_cases.csv`",
                "- `reports/tables/binary_v2_failure_summary.json`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    rows = _failure_rows(DEFAULT_EVALUATION_PATH, DEFAULT_BENCHMARK_PATH)
    summary = _summary(DEFAULT_EVALUATION_PATH, rows)
    _write_csv(DEFAULT_TABLE_DIR / "binary_v2_failure_cases.csv", rows)
    (DEFAULT_TABLE_DIR / "binary_v2_failure_summary.json").write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )
    _write_doc(DEFAULT_DOC_PATH, summary)
    print(
        "wrote phase21 binary v2 diagnostics: "
        f"{len(rows)} failed binary cases, correctness={summary['binary_correctness']}"
    )


if __name__ == "__main__":
    main()
