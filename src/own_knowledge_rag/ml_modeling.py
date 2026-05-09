from __future__ import annotations

import json
import math
import random
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Any


@dataclass(frozen=True)
class FailureModelDataset:
    feature_names: list[str]
    rows: list[list[float]]
    labels: list[int]


@dataclass(frozen=True)
class LogisticFailureModel:
    feature_names: list[str]
    coefficients: list[float]
    intercept: float
    means: list[float]
    scales: list[float]

    def predict_proba(self, rows: list[list[float]]) -> list[float]:
        scores: list[float] = []
        for row in rows:
            z = self.intercept
            for value, coefficient, center, scale in zip(
                row, self.coefficients, self.means, self.scales
            ):
                z += coefficient * ((value - center) / scale)
            scores.append(_sigmoid(z))
        return scores


def load_evaluation_dataset(evaluation_path: Path) -> FailureModelDataset:
    payload = json.loads(evaluation_path.read_text(encoding="utf-8"))
    return build_failure_dataset(payload.get("results", []))


def build_failure_dataset(results: list[dict[str, Any]]) -> FailureModelDataset:
    feature_names = [
        "retrieval_hit",
        "evidence_hit",
        "citation_hit",
        "section_hit",
        "block_type_hit",
        "metadata_hit",
        "country_match_at_1",
        "foreign_evidence_present",
        "document_precision_at_k",
        "expected_document_count",
        "expected_term_count",
        "expected_block_type_count",
        "expected_sender_type_count",
        "retrieved_document_count",
        "retrieved_section_count",
        "question_length",
        "answer_length",
        "question_type_binary",
        "question_type_policy_rule",
        "question_type_sender_type_policy",
        "question_type_capability",
        "tier0",
        "tier1",
        "tier2",
        "answer_cached",
    ]
    rows: list[list[float]] = []
    labels: list[int] = []
    for result in results:
        if result.get("should_refuse"):
            continue
        question_type = str(result.get("question_type") or "")
        routed_tier = str(result.get("routed_tier") or "")
        row = [
            _bool(result.get("retrieval_hit")),
            _bool(result.get("evidence_hit")),
            _bool(result.get("citation_hit")),
            _bool(result.get("section_hit")),
            _bool(result.get("block_type_hit")),
            _bool(result.get("metadata_hit")),
            _bool(result.get("country_match_at_1")),
            _bool(result.get("foreign_evidence_present")),
            _float(result.get("document_precision_at_k")),
            float(len(result.get("expected_document_ids") or [])),
            float(len(result.get("expected_terms") or [])),
            float(len(result.get("expected_block_types") or [])),
            float(len(result.get("expected_sender_types") or [])),
            float(len(result.get("retrieved_document_ids") or [])),
            float(len(result.get("retrieved_sections") or [])),
            float(len(str(result.get("question") or ""))),
            float(len(str(result.get("answer_text") or ""))),
            float(question_type == "binary"),
            float(question_type == "policy_rule"),
            float(question_type == "sender_type_policy"),
            float(question_type == "capability"),
            float(routed_tier == "tier0"),
            float(routed_tier == "tier1"),
            float(routed_tier == "tier2"),
            _bool(result.get("answer_cached")),
        ]
        rows.append(row)
        labels.append(0 if result.get("answer_correct") else 1)
    return FailureModelDataset(feature_names=feature_names, rows=rows, labels=labels)


def train_failure_model(
    dataset: FailureModelDataset,
    *,
    seed: int = 42,
    test_fraction: float = 0.25,
    iterations: int = 900,
    learning_rate: float = 0.12,
    l2: float = 0.002,
) -> dict[str, Any]:
    train_idx, test_idx = stratified_train_test_split(dataset.labels, seed, test_fraction)
    x_train = [dataset.rows[index] for index in train_idx]
    y_train = [dataset.labels[index] for index in train_idx]
    x_test = [dataset.rows[index] for index in test_idx]
    y_test = [dataset.labels[index] for index in test_idx]

    model = fit_logistic_regression(
        dataset.feature_names,
        x_train,
        y_train,
        iterations=iterations,
        learning_rate=learning_rate,
        l2=l2,
    )
    probabilities = model.predict_proba(x_test)
    baseline_scores = [_baseline_failure_score(row, dataset.feature_names) for row in x_test]

    metrics = binary_classification_metrics(y_test, probabilities)
    baseline_metrics = binary_classification_metrics(y_test, baseline_scores)
    confusion = confusion_matrix(y_test, probabilities)
    roc_points = roc_curve_points(y_test, probabilities)
    return {
        "dataset": {
            "rows": len(dataset.rows),
            "features": len(dataset.feature_names),
            "positive_failure_rate": round(sum(dataset.labels) / len(dataset.labels), 4)
            if dataset.labels
            else 0.0,
            "train_rows": len(train_idx),
            "test_rows": len(test_idx),
        },
        "metrics": metrics,
        "baseline_metrics": baseline_metrics,
        "confusion_matrix": confusion,
        "roc_curve": roc_points,
        "feature_importance": feature_importance(model),
        "model": {
            "type": "standardized_logistic_regression",
            "intercept": round(model.intercept, 6),
            "coefficients": {
                name: round(coefficient, 6)
                for name, coefficient in zip(model.feature_names, model.coefficients)
            },
        },
    }


def fit_logistic_regression(
    feature_names: list[str],
    rows: list[list[float]],
    labels: list[int],
    *,
    iterations: int = 900,
    learning_rate: float = 0.12,
    l2: float = 0.002,
) -> LogisticFailureModel:
    if not rows:
        raise ValueError("Cannot fit a model without rows.")
    if len(set(labels)) < 2:
        raise ValueError("Cannot fit a model with only one target class.")

    means = [mean(column) for column in zip(*rows)]
    scales = []
    for column, center in zip(zip(*rows), means):
        variance = mean((value - center) ** 2 for value in column)
        scales.append(math.sqrt(variance) or 1.0)

    standardized = [
        [(value - center) / scale for value, center, scale in zip(row, means, scales)]
        for row in rows
    ]
    coefficients = [0.0 for _ in feature_names]
    positive_rate = sum(labels) / len(labels)
    intercept = math.log(positive_rate / (1 - positive_rate))

    for _ in range(iterations):
        gradient = [0.0 for _ in coefficients]
        intercept_gradient = 0.0
        for row, label in zip(standardized, labels):
            prediction = _sigmoid(intercept + sum(c * x for c, x in zip(coefficients, row)))
            error = prediction - label
            intercept_gradient += error
            for index, value in enumerate(row):
                gradient[index] += error * value

        n = len(labels)
        intercept -= learning_rate * intercept_gradient / n
        for index in range(len(coefficients)):
            penalty = l2 * coefficients[index]
            coefficients[index] -= learning_rate * (gradient[index] / n + penalty)

    return LogisticFailureModel(
        feature_names=feature_names,
        coefficients=coefficients,
        intercept=intercept,
        means=means,
        scales=scales,
    )


def binary_classification_metrics(
    labels: list[int], probabilities: list[float]
) -> dict[str, float]:
    if len(labels) != len(probabilities):
        raise ValueError("labels and probabilities must have the same length.")
    predictions = [1 if probability >= 0.5 else 0 for probability in probabilities]
    tp = sum(1 for y, y_hat in zip(labels, predictions) if y == 1 and y_hat == 1)
    fp = sum(1 for y, y_hat in zip(labels, predictions) if y == 0 and y_hat == 1)
    tn = sum(1 for y, y_hat in zip(labels, predictions) if y == 0 and y_hat == 0)
    fn = sum(1 for y, y_hat in zip(labels, predictions) if y == 1 and y_hat == 0)
    accuracy = (tp + tn) / len(labels) if labels else 0.0
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "roc_auc": round(roc_auc(labels, probabilities), 4),
        "average_precision": round(average_precision(labels, probabilities), 4),
    }


def confusion_matrix(
    labels: list[int], probabilities: list[float], threshold: float = 0.5
) -> dict[str, int]:
    predictions = [1 if probability >= threshold else 0 for probability in probabilities]
    return {
        "true_negative": sum(
            1 for label, prediction in zip(labels, predictions) if label == 0 and prediction == 0
        ),
        "false_positive": sum(
            1 for label, prediction in zip(labels, predictions) if label == 0 and prediction == 1
        ),
        "false_negative": sum(
            1 for label, prediction in zip(labels, predictions) if label == 1 and prediction == 0
        ),
        "true_positive": sum(
            1 for label, prediction in zip(labels, predictions) if label == 1 and prediction == 1
        ),
    }


def roc_curve_points(labels: list[int], scores: list[float]) -> list[dict[str, float]]:
    thresholds = sorted(set(scores), reverse=True)
    points = [{"threshold": 1.01, "false_positive_rate": 0.0, "true_positive_rate": 0.0}]
    positives = sum(labels)
    negatives = len(labels) - positives
    if positives == 0 or negatives == 0:
        return points
    for threshold in thresholds:
        predictions = [1 if score >= threshold else 0 for score in scores]
        tp = sum(
            1 for label, prediction in zip(labels, predictions) if label == 1 and prediction == 1
        )
        fp = sum(
            1 for label, prediction in zip(labels, predictions) if label == 0 and prediction == 1
        )
        points.append(
            {
                "threshold": round(threshold, 6),
                "false_positive_rate": round(fp / negatives, 6),
                "true_positive_rate": round(tp / positives, 6),
            }
        )
    points.append({"threshold": -0.01, "false_positive_rate": 1.0, "true_positive_rate": 1.0})
    return points


def roc_auc(labels: list[int], scores: list[float]) -> float:
    positives = sum(labels)
    negatives = len(labels) - positives
    if positives == 0 or negatives == 0:
        return 0.0
    ranked = sorted(zip(scores, labels), key=lambda item: item[0])
    rank_sum = 0.0
    index = 0
    while index < len(ranked):
        end = index
        while end + 1 < len(ranked) and ranked[end + 1][0] == ranked[index][0]:
            end += 1
        average_rank = (index + 1 + end + 1) / 2
        rank_sum += average_rank * sum(label for _, label in ranked[index : end + 1])
        index = end + 1
    return (rank_sum - positives * (positives + 1) / 2) / (positives * negatives)


def average_precision(labels: list[int], scores: list[float]) -> float:
    positives = sum(labels)
    if positives == 0:
        return 0.0
    ranked = sorted(zip(scores, labels), key=lambda item: item[0], reverse=True)
    precision_sum = 0.0
    found = 0
    for rank, (_, label) in enumerate(ranked, start=1):
        if label:
            found += 1
            precision_sum += found / rank
    return precision_sum / positives


def feature_importance(model: LogisticFailureModel, limit: int = 12) -> list[dict[str, Any]]:
    ranked = sorted(
        zip(model.feature_names, model.coefficients),
        key=lambda item: abs(item[1]),
        reverse=True,
    )
    return [
        {
            "feature": feature,
            "coefficient": round(coefficient, 6),
            "direction": "raises_failure_risk" if coefficient > 0 else "lowers_failure_risk",
        }
        for feature, coefficient in ranked[:limit]
    ]


def stratified_train_test_split(
    labels: list[int], seed: int = 42, test_fraction: float = 0.25
) -> tuple[list[int], list[int]]:
    rng = random.Random(seed)
    by_label: dict[int, list[int]] = {}
    for index, label in enumerate(labels):
        by_label.setdefault(label, []).append(index)

    train: list[int] = []
    test: list[int] = []
    for indexes in by_label.values():
        rng.shuffle(indexes)
        test_count = max(1, round(len(indexes) * test_fraction))
        test.extend(indexes[:test_count])
        train.extend(indexes[test_count:])
    rng.shuffle(train)
    rng.shuffle(test)
    return train, test


def write_failure_model_report(result: dict[str, Any], output_path: Path) -> None:
    lines = [
        "# Answer Failure Prediction Model",
        "",
        (
            "This lightweight supervised model predicts whether a benchmark answer "
            "will fail from retrieval and query features."
        ),
        "",
        "## Dataset",
        "",
        f"- Rows: `{result['dataset']['rows']}`",
        f"- Features: `{result['dataset']['features']}`",
        f"- Failure rate: `{result['dataset']['positive_failure_rate']}`",
        (
            f"- Train/test rows: `{result['dataset']['train_rows']}` / "
            f"`{result['dataset']['test_rows']}`"
        ),
        "",
        "## Test Metrics",
        "",
        "| Model | ROC-AUC | Average precision | F1 | Recall | Precision | Accuracy |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        (
            f"| Logistic failure model | {result['metrics']['roc_auc']} | "
            f"{result['metrics']['average_precision']} | {result['metrics']['f1']} | "
            f"{result['metrics']['recall']} | {result['metrics']['precision']} | "
            f"{result['metrics']['accuracy']} |"
        ),
        (
            f"| Heuristic baseline | {result['baseline_metrics']['roc_auc']} | "
            f"{result['baseline_metrics']['average_precision']} | "
            f"{result['baseline_metrics']['f1']} | "
            f"{result['baseline_metrics']['recall']} | "
            f"{result['baseline_metrics']['precision']} | "
            f"{result['baseline_metrics']['accuracy']} |"
        ),
        "",
        "## Strongest Features",
        "",
        "| Feature | Coefficient | Direction |",
        "| --- | ---: | --- |",
    ]
    for item in result["feature_importance"]:
        lines.append(
            f"| `{item['feature']}` | {item['coefficient']} | {item['direction']} |"
        )
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _baseline_failure_score(row: list[float], feature_names: list[str]) -> float:
    values = dict(zip(feature_names, row))
    score = 0.05
    if not values.get("citation_hit"):
        score += 0.45
    if not values.get("evidence_hit"):
        score += 0.25
    if values.get("question_type_binary"):
        score += 0.12
    if values.get("foreign_evidence_present"):
        score += 0.1
    return min(score, 0.95)


def _bool(value: Any) -> float:
    return 1.0 if bool(value) else 0.0


def _float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _sigmoid(value: float) -> float:
    if value >= 0:
        z = math.exp(-value)
        return 1 / (1 + z)
    z = math.exp(value)
    return z / (1 + z)
