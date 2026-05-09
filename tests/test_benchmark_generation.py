import json
from pathlib import Path

from own_knowledge_rag.benchmark_generation import (
    export_country_regression_cases,
    export_query_reviews_benchmark,
    export_review_findings_benchmark,
    generate_benchmark_cases,
    save_benchmark_cases,
)


def test_generate_benchmark_cases_builds_profile_and_refusal_cases(tmp_path: Path) -> None:
    source_dir = tmp_path / "raw"
    source_dir.mkdir(parents=True, exist_ok=True)
    (source_dir / "spain_es.md").write_text(
        """# Spain (ES)

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Spain |
| Dialing code | --- | +34 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | --- | Yes |
| Number portability available | --- | No |
| Compliance considerations | --- | Get opt-in consent before sending marketing messages. |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Twilio supported | Whether Twilio supports the feature. | Supported | Supported |
| Sender ID preserved | Whether the sender is preserved. | Yes | Yes |
| Provisioning time | Approval time. | 1 week | N/A |

## Phone Numbers & Sender ID: Long codes and short codes

| Field | Description | Long code domestic | Long code international | Short code |
| --- | --- | --- | --- | --- |
| Twilio supported | Whether Twilio supports the feature. | Supported | Supported | Not Supported |
| Sender ID preserved | Whether the sender is preserved. | Yes | No | --- |

## spain

| Key | Value |
| --- | --- |
| Sender availability | Alpha and Short Code. |
| Sender provisioning | Registration takes 1 week. |
""",
        encoding="utf-8",
    )
    (source_dir / "all_twilio_sms_guidelines_index.md").write_text(
        """# Twilio SMS Guidelines Index

Locale count: 1

Error count: 0
""",
        encoding="utf-8",
    )

    cases = generate_benchmark_cases(source_dir)
    questions = {case.question for case in cases}

    assert "What is the dialing code for Spain?" in questions
    assert "Does Spain support two-way SMS?" in questions
    assert "Is number portability available in Spain?" in questions
    assert "Does Spain support alphanumeric sender IDs?" in questions
    assert "What sender types are available in Spain?" in questions
    assert "What compliance considerations apply to SMS in Spain?" in questions
    assert "How many locales are listed in the Twilio SMS Guidelines Index?" in questions
    assert any(case.should_refuse for case in cases)
    dialing_case = next(case for case in cases if case.question == "What is the dialing code for Spain?")
    assert dialing_case.expected_block_types
    assert dialing_case.expected_metadata == {"row_key": "Dialing code"}
    alpha_case = next(case for case in cases if case.question == "Does Spain support alphanumeric sender IDs?")
    assert alpha_case.expected_sender_types == ["alphanumeric sender id"]
    assert alpha_case.expected_metadata == {"row_key": "Twilio supported"}


def test_save_benchmark_cases_writes_json(tmp_path: Path) -> None:
    source_dir = tmp_path / "raw"
    source_dir.mkdir(parents=True, exist_ok=True)
    (source_dir / "spain_es.md").write_text(
        """# Spain (ES)

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Spain |
| Dialing code | --- | +34 |

## Guidelines

| Field | Description | Value |
| --- | --- | --- |
| Two-way SMS supported | --- | Yes |
""",
        encoding="utf-8",
    )
    cases = generate_benchmark_cases(source_dir)
    output_path = tmp_path / "generated.json"

    save_benchmark_cases(cases, output_path)

    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert isinstance(payload, list)
    assert payload


def test_checked_in_expanded_benchmark_has_phase5_scale() -> None:
    payload = json.loads(Path("benchmarks/real_corpus_expanded.json").read_text(encoding="utf-8"))
    assert len(payload) >= 200


def test_export_review_findings_benchmark_writes_cases(tmp_path: Path) -> None:
    review_findings_path = tmp_path / "review_findings.json"
    review_findings_path.write_text(
        json.dumps(
            {
                "entries": [
                    {
                        "finding_id": "spain_es::two way sms supported",
                        "document_id": "spain_es",
                        "country": "Spain",
                        "normalized_key": "two way sms supported",
                        "review_status": "accepted_conflict",
                        "resolution_value": "",
                    },
                    {
                        "finding_id": "spain_es::dialing code",
                        "document_id": "spain_es",
                        "country": "Spain",
                        "normalized_key": "dialing code",
                        "review_status": "resolved",
                        "resolution_value": "+34",
                    },
                ]
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    output_path = tmp_path / "review_benchmark.json"

    cases = export_review_findings_benchmark(review_findings_path, output_path)

    assert output_path.exists()
    assert len(cases) == 2
    questions = {case.question for case in cases}
    assert "Does Spain support two-way SMS?" in questions
    assert "What is the dialing code for Spain?" in questions


def test_export_country_regression_cases_filters_to_single_country_queries(tmp_path: Path) -> None:
    benchmark_path = tmp_path / "expanded.json"
    benchmark_path.write_text(
        json.dumps(
            [
                {
                    "question": "Does Colombia support two-way SMS?",
                    "expected_document_ids": ["colombia_co"],
                    "expected_terms": ["two-way sms supported", "no"],
                    "expected_block_types": ["table_fact"],
                    "expected_metadata": {"row_key": "Two-way SMS supported"},
                    "question_type": "capability",
                    "should_refuse": False,
                },
                {
                    "question": "Compare sender provisioning and two-way support in Spain.",
                    "expected_document_ids": ["spain_es"],
                    "expected_terms": ["supported"],
                    "question_type": "comparative",
                    "should_refuse": False,
                },
                {
                    "question": "What is the dialing code for Peru?",
                    "expected_document_ids": ["peru_pe"],
                    "expected_terms": ["dialing code", "+51"],
                    "question_type": "factoid",
                    "should_refuse": False,
                },
            ],
            indent=2,
        ),
        encoding="utf-8",
    )
    output_path = tmp_path / "country_regressions.json"

    cases = export_country_regression_cases(benchmark_path, output_path)

    assert output_path.exists()
    assert len(cases) == 2
    questions = {case.question for case in cases}
    assert "Does Colombia support two-way SMS?" in questions
    assert "What is the dialing code for Peru?" in questions
    assert all(case.must_not_mix_documents for case in cases)
    assert {case.expected_iso_code for case in cases} == {"CO", "PE"}
    colombia_case = next(case for case in cases if case.expected_iso_code == "CO")
    assert colombia_case.expected_block_types == ["table_fact"]
    assert colombia_case.expected_metadata == {"row_key": "Two-way SMS supported"}


def test_export_country_regression_cases_can_augment_from_source_dir(tmp_path: Path) -> None:
    benchmark_path = tmp_path / "expanded.json"
    benchmark_path.write_text(
        json.dumps(
            [
                {
                    "question": "What is the dialing code for Peru?",
                    "expected_document_ids": ["peru_pe"],
                    "expected_terms": ["dialing code", "+51"],
                    "question_type": "factoid",
                    "should_refuse": False,
                }
            ],
            indent=2,
        ),
        encoding="utf-8",
    )
    source_dir = tmp_path / "raw"
    source_dir.mkdir(parents=True)
    (source_dir / "spain_es.md").write_text(
        """# Spain (ES)

## Locale Summary

| Field | Description | Value |
| --- | --- | --- |
| Locale name | --- | Spain |
| Dialing code | --- | +34 |

## Phone Numbers & Sender ID: Alphanumeric

| Field | Description | Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Twilio supported | Whether Twilio supports the feature. | Supported | Supported |
""",
        encoding="utf-8",
    )
    output_path = tmp_path / "country_regressions.json"

    cases = export_country_regression_cases(benchmark_path, output_path, source_dir=source_dir)

    assert "Does Spain support alphanumeric sender IDs?" in {case.question for case in cases}
    assert {case.expected_iso_code for case in cases} == {"ES", "PE"}


def test_export_query_reviews_benchmark_writes_cases(tmp_path: Path) -> None:
    query_reviews_path = tmp_path / "query_reviews.json"
    query_reviews_path.write_text(
        json.dumps(
            {
                "entries": [
                    {
                        "review_id": "review-00001",
                        "question": "Sender in Colombia?",
                        "answer": "For Colombia, the Sender availability is: Short Code.",
                        "rating": "correct_with_foreign_evidence",
                        "expected_document_id": "colombia_co",
                        "expected_iso_code": "CO",
                        "expected_terms": ["sender", "short code"],
                        "evidence_document_ids": ["colombia_co", "angola_ao"],
                    },
                    {
                        "review_id": "review-00002",
                        "question": "Is there any moon policy in this corpus?",
                        "answer": "Insufficient evidence in the indexed knowledge base.",
                        "rating": "should_refuse",
                        "expected_document_id": "",
                        "expected_iso_code": "",
                        "expected_terms": [],
                        "evidence_document_ids": [],
                    },
                ]
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    output_path = tmp_path / "query_review_benchmark.json"

    cases = export_query_reviews_benchmark(query_reviews_path, output_path)

    assert output_path.exists()
    assert len(cases) == 2
    colombia_case = next(case for case in cases if case.question == "Sender in Colombia?")
    assert colombia_case.expected_document_ids == ["colombia_co"]
    assert colombia_case.expected_iso_code == "CO"
    assert colombia_case.must_not_mix_documents is True
    assert colombia_case.should_refuse is False
    refusal_case = next(case for case in cases if case.question == "Is there any moon policy in this corpus?")
    assert refusal_case.should_refuse is True
