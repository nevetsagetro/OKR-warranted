from pathlib import Path

from own_knowledge_rag.experiments import compare_experiments
from own_knowledge_rag.models import EvaluationCaseResult, EvaluationSummary


def _result(question: str, *, retrieval: bool, evidence: bool, answer: bool) -> EvaluationCaseResult:
    return EvaluationCaseResult(
        question=question,
        expected_document_ids=["spain_es"],
        expected_source_paths=[],
        expected_terms=[],
        expected_section_terms=[],
        expected_block_types=[],
        expected_sender_types=[],
        expected_metadata={},
        expected_iso_code="ES",
        question_type="factoid",
        should_refuse=False,
        retrieved_document_ids=["spain_es"] if retrieval else [],
        retrieved_sections=[],
        refusal_correct=True,
        retrieval_hit=retrieval,
        evidence_hit=evidence,
        citation_hit=False,
        section_hit=False,
        answer_correct=answer,
        document_precision_at_k=1.0 if retrieval else 0.0,
        answer_confidence="high",
    )


def test_compare_experiments_outputs_statistical_report(tmp_path: Path) -> None:
    baseline = EvaluationSummary(
        total_cases=2,
        retrieval_recall_at_k=0.5,
        evidence_hit_rate=0.5,
        citation_accuracy=0.0,
        document_precision_at_k=0.5,
        no_answer_precision=0.0,
        answer_correctness=0.5,
        results=[
            _result("q1", retrieval=True, evidence=True, answer=True),
            _result("q2", retrieval=False, evidence=False, answer=False),
        ],
    )
    experiment = EvaluationSummary(
        total_cases=2,
        retrieval_recall_at_k=1.0,
        evidence_hit_rate=1.0,
        citation_accuracy=0.0,
        document_precision_at_k=1.0,
        no_answer_precision=0.0,
        answer_correctness=1.0,
        results=[
            _result("q1", retrieval=True, evidence=True, answer=True),
            _result("q2", retrieval=True, evidence=True, answer=True),
        ],
    )
    output_path = tmp_path / "comparison_report.json"

    report = compare_experiments(baseline, experiment, output_path, resamples=100)

    assert output_path.exists()
    assert report["paired_cases"] == 2
    assert {item["metric"] for item in report["metrics"]} == {
        "retrieval_recall_at_k",
        "evidence_hit_rate",
        "answer_correctness",
    }
    assert any(item["delta"] > 0 for item in report["metrics"])
