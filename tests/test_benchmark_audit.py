import json
from pathlib import Path

from own_knowledge_rag.benchmark_audit import audit_benchmark, render_benchmark_audit


def test_benchmark_audit_counts_core_segments(tmp_path: Path) -> None:
    path = tmp_path / "benchmark.json"
    path.write_text(
        json.dumps(
            [
                {
                    "question": "Sender ID in Spain?",
                    "expected_document_ids": ["spain_es"],
                    "expected_iso_code": "ES",
                    "expected_block_types": ["table_fact"],
                    "question_type": "factoid",
                },
                {
                    "question": "Sender in France?",
                    "expected_document_ids": ["france_fr"],
                    "expected_block_types": ["structured_fact"],
                    "question_type": "factoid",
                },
            ]
        ),
        encoding="utf-8",
    )

    report = audit_benchmark(path, min_cases=2)
    rendered = render_benchmark_audit(report)

    assert report["total_cases"] == 2
    assert report["tables"]["iso_code"]["ES"] == 1
    assert report["tables"]["iso_code"]["FR"] == 1
    assert report["tables"]["block_type"]["table_fact"] == 1
    assert report["missing_metadata"]["sender_type"] == 1
    assert report["warnings"]
    assert "sender_type metadata is missing for 1 case(s)." in report["warnings"]
    assert "Benchmark audit" in rendered
    assert "Missing metadata" in rendered


def test_benchmark_audit_allows_documented_low_count_segments(tmp_path: Path) -> None:
    path = tmp_path / "benchmark.json"
    path.write_text(
        json.dumps(
            [
                {
                    "question": "Is two-way SMS supported for toll-free numbers in Canada?",
                    "expected_document_ids": ["canada_ca"],
                    "expected_iso_code": "CA",
                    "expected_block_types": ["table_fact"],
                    "expected_sender_types": ["toll-free number"],
                    "question_type": "sender_type_capability",
                }
            ]
        ),
        encoding="utf-8",
    )

    report = audit_benchmark(
        path,
        min_cases=10,
        allow_low_count=["sender_type:toll-free number"],
    )
    rendered = render_benchmark_audit(report)

    assert report["adequate"] is False
    assert "sender_type:toll-free number has 1 case(s), below minimum 10." not in report["warnings"]
    assert "sender_type:toll-free number has 1 case(s), below minimum 10." in report["allowed_low_count_findings"]
    assert "Allowed low-count segments" in rendered
