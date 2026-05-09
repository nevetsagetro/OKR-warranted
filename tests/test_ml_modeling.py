from __future__ import annotations

from own_knowledge_rag.ml_modeling import (
    average_precision,
    build_failure_dataset,
    confusion_matrix,
    roc_auc,
    roc_curve_points,
    train_failure_model,
)


def test_build_failure_dataset_extracts_labels_and_features() -> None:
    dataset = build_failure_dataset(
        [
            {
                "question": "Does Spain support two-way SMS?",
                "answer_text": "Yes.",
                "question_type": "binary",
                "routed_tier": "tier0",
                "expected_document_ids": ["spain_es"],
                "expected_terms": ["two-way"],
                "expected_block_types": ["table_fact"],
                "expected_sender_types": ["short code"],
                "retrieved_document_ids": ["spain_es"],
                "retrieved_sections": ["Spain > SMS"],
                "retrieval_hit": True,
                "evidence_hit": True,
                "citation_hit": False,
                "section_hit": True,
                "block_type_hit": True,
                "metadata_hit": True,
                "country_match_at_1": True,
                "foreign_evidence_present": False,
                "document_precision_at_k": 1.0,
                "answer_cached": False,
                "answer_correct": False,
            },
            {
                "question": "No-answer case",
                "should_refuse": True,
                "answer_correct": True,
            },
        ]
    )

    assert dataset.labels == [1]
    row = dict(zip(dataset.feature_names, dataset.rows[0]))
    assert row["question_type_binary"] == 1.0
    assert row["citation_hit"] == 0.0
    assert row["expected_sender_type_count"] == 1.0


def test_ranking_metrics_handle_separable_scores() -> None:
    labels = [0, 0, 1, 1]
    scores = [0.1, 0.2, 0.8, 0.9]

    assert roc_auc(labels, scores) == 1.0
    assert average_precision(labels, scores) == 1.0
    assert confusion_matrix(labels, scores, threshold=0.5) == {
        "true_negative": 2,
        "false_positive": 0,
        "false_negative": 0,
        "true_positive": 2,
    }
    points = roc_curve_points(labels, scores)
    assert points[0]["false_positive_rate"] == 0.0
    assert points[-1]["true_positive_rate"] == 1.0


def test_train_failure_model_returns_metrics_and_importance() -> None:
    results = []
    for index in range(30):
        is_failure = index % 3 == 0
        results.append(
            {
                "question": f"Question {index}",
                "answer_text": "answer",
                "question_type": "binary" if is_failure else "factoid",
                "routed_tier": "tier0",
                "expected_document_ids": ["doc"],
                "expected_terms": ["term"],
                "expected_block_types": ["table_fact"],
                "retrieved_document_ids": ["doc"],
                "retrieved_sections": ["section"],
                "retrieval_hit": True,
                "evidence_hit": not is_failure,
                "citation_hit": not is_failure,
                "section_hit": True,
                "block_type_hit": True,
                "metadata_hit": True,
                "country_match_at_1": True,
                "foreign_evidence_present": False,
                "document_precision_at_k": 1.0,
                "answer_cached": False,
                "answer_correct": not is_failure,
            }
        )

    result = train_failure_model(build_failure_dataset(results), iterations=120)

    assert result["dataset"]["rows"] == 30
    assert result["metrics"]["roc_auc"] >= 0.9
    assert result["confusion_matrix"]["true_positive"] > 0
    assert result["roc_curve"]
    assert result["feature_importance"]
