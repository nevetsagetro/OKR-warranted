from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "src"))

from own_knowledge_rag.ml_modeling import (  # noqa: E402
    load_evaluation_dataset,
    train_failure_model,
    write_failure_model_report,
)


def main() -> None:
    evaluation_path = Path("data/work/evaluation/latest-evaluation.json")
    output_dir = Path("reports/tables")
    docs_dir = Path("docs")
    output_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)

    evaluation_payload = json.loads(evaluation_path.read_text(encoding="utf-8"))
    answerable_results = [
        row for row in evaluation_payload.get("results", []) if not row.get("should_refuse")
    ]
    country_lookup = load_country_lookup(Path("data/work/documents.json"))
    dataset = load_evaluation_dataset(evaluation_path)
    result = train_failure_model(dataset)

    metrics_path = output_dir / "answer_failure_model.json"
    selection_path = output_dir / "answer_failure_model_selection.json"
    report_path = docs_dir / "answer_failure_model.md"
    metrics_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    selection_result = run_sklearn_model_selection(
        dataset,
        answerable_results=answerable_results,
        country_lookup=country_lookup,
    )
    if selection_result is None:
        write_failure_model_report(result, report_path)
    else:
        selection_path.write_text(json.dumps(selection_result, indent=2), encoding="utf-8")
        false_negative_path = output_dir / "failure_model_false_negatives.csv"
        write_false_negative_table(selection_result, false_negative_path)
        write_combined_report(result, selection_result, report_path)

    print(f"Wrote metrics to {metrics_path}")
    if selection_result is not None:
        print(f"Wrote sklearn selection metrics to {selection_path}")
        print(f"Wrote false-negative table to {false_negative_path}")
    print(f"Wrote report to {report_path}")
    print(
        "Model ROC-AUC="
        f"{result['metrics']['roc_auc']} "
        "baseline ROC-AUC="
        f"{result['baseline_metrics']['roc_auc']}"
    )


def run_sklearn_model_selection(dataset, answerable_results=None, country_lookup=None):
    try:
        import numpy as np
        from sklearn.base import clone
        from sklearn.calibration import calibration_curve
        from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
        from sklearn.inspection import permutation_importance
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import (
            average_precision_score,
            brier_score_loss,
            confusion_matrix,
            f1_score,
            make_scorer,
            precision_recall_curve,
            precision_score,
            recall_score,
            roc_auc_score,
        )
        from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
        from sklearn.pipeline import make_pipeline
        from sklearn.preprocessing import StandardScaler
    except ImportError:
        return None

    x = dataset.rows
    y = dataset.labels
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scoring = {
        "roc_auc": "roc_auc",
        "average_precision": "average_precision",
        "f1": make_scorer(f1_score, zero_division=0),
    }
    models = {
        "logistic_regression": make_pipeline(
            StandardScaler(),
            LogisticRegression(max_iter=2000, random_state=42),
        ),
        "logistic_regression_balanced": make_pipeline(
            StandardScaler(),
            LogisticRegression(max_iter=2000, class_weight="balanced", random_state=42),
        ),
        "random_forest_balanced": RandomForestClassifier(
            n_estimators=240,
            class_weight="balanced",
            min_samples_leaf=3,
            random_state=42,
            n_jobs=-1,
        ),
        "hist_gradient_boosting": HistGradientBoostingClassifier(
            max_iter=180,
            learning_rate=0.05,
            max_leaf_nodes=15,
            random_state=42,
        ),
    }
    positive_count = sum(y)
    negative_count = len(y) - positive_count
    if positive_count:
        try:
            from xgboost import XGBClassifier

            models["xgboost_balanced"] = XGBClassifier(
                n_estimators=220,
                max_depth=3,
                learning_rate=0.05,
                subsample=0.9,
                colsample_bytree=0.9,
                eval_metric="logloss",
                scale_pos_weight=negative_count / positive_count,
                tree_method="hist",
                random_state=42,
                n_jobs=1,
            )
        except ImportError:
            pass

    result = {
        "positive_failure_rate": sum(y) / len(y) if y else 0.0,
        "models": [],
        "selected_model": None,
        "permutation_importance": [],
        "shap_explainability": {},
        "proxy_feature_audit": {},
        "threshold_analysis": {},
        "precision_recall_curve": [],
        "calibration": {},
        "false_negative_analysis": {},
    }
    for name, estimator in models.items():
        scores = cross_validate(estimator, x, y, cv=cv, scoring=scoring, n_jobs=-1)
        result["models"].append(
            {
                "model": name,
                "roc_auc_mean": round(float(scores["test_roc_auc"].mean()), 4),
                "roc_auc_std": round(float(scores["test_roc_auc"].std()), 4),
                "average_precision_mean": round(
                    float(scores["test_average_precision"].mean()), 4
                ),
                "average_precision_std": round(float(scores["test_average_precision"].std()), 4),
                "f1_mean": round(float(scores["test_f1"].mean()), 4),
                "f1_std": round(float(scores["test_f1"].std()), 4),
            }
        )
    result["models"].sort(key=lambda row: row["roc_auc_mean"], reverse=True)
    selected_name = result["models"][0]["model"]
    selected_estimator = models[selected_name]
    selected_estimator.fit(x, y)
    result["selected_model"] = selected_name
    result["shap_explainability"] = build_shap_explainability(
        estimator=selected_estimator,
        rows=x,
        labels=y,
        feature_names=dataset.feature_names,
        answerable_results=answerable_results or [],
        country_lookup=country_lookup or {},
    )

    importance = permutation_importance(
        selected_estimator,
        x,
        y,
        scoring="roc_auc",
        n_repeats=10,
        random_state=42,
        n_jobs=-1,
    )
    ranked = sorted(
        zip(dataset.feature_names, importance.importances_mean, importance.importances_std),
        key=lambda item: abs(item[1]),
        reverse=True,
    )[:12]
    result["permutation_importance"] = [
        {
            "feature": feature,
            "importance_mean": round(float(mean_value), 6),
            "importance_std": round(float(std_value), 6),
        }
        for feature, mean_value, std_value in ranked
    ]
    if "answer_length" in dataset.feature_names:
        answer_length_index = dataset.feature_names.index("answer_length")
        reduced_feature_names = [
            feature
            for index, feature in enumerate(dataset.feature_names)
            if index != answer_length_index
        ]
        reduced_x = [
            [value for index, value in enumerate(row) if index != answer_length_index]
            for row in x
        ]
        reduced_estimator = clone(models[selected_name])
        reduced_scores = cross_validate(
            reduced_estimator,
            reduced_x,
            y,
            cv=cv,
            scoring=scoring,
            n_jobs=-1,
        )
        selected_row = next(row for row in result["models"] if row["model"] == selected_name)
        reduced_roc_auc = round(float(reduced_scores["test_roc_auc"].mean()), 4)
        roc_auc_delta = round(selected_row["roc_auc_mean"] - reduced_roc_auc, 4)
        result["proxy_feature_audit"] = {
            "audited_feature": "answer_length",
            "reason": (
                "answer_length is an output-derived proxy. It may change when the "
                "answer synthesizer changes, so production use should prefer causal "
                "or pre-answer features when performance is comparable."
            ),
            "selected_model": selected_name,
            "full_feature_count": len(dataset.feature_names),
            "reduced_feature_count": len(reduced_feature_names),
            "full_roc_auc_mean": selected_row["roc_auc_mean"],
            "without_answer_length_roc_auc_mean": reduced_roc_auc,
            "roc_auc_delta": roc_auc_delta,
            "without_answer_length_average_precision_mean": round(
                float(reduced_scores["test_average_precision"].mean()), 4
            ),
            "without_answer_length_f1_mean": round(float(reduced_scores["test_f1"].mean()), 4),
            "interpretation": (
                "Large drops above 0.02-0.03 suggest worrying proxy dependence; "
                "small drops below 0.01 suggest the model is not overly dependent on "
                "answer_length."
            ),
        }

    indices = list(range(len(y)))
    x_train, x_test, y_train, y_test, _, test_indices = train_test_split(
        x,
        y,
        indices,
        test_size=0.25,
        stratify=y,
        random_state=43,
    )
    holdout_estimator = clone(models[selected_name])
    holdout_estimator.fit(x_train, y_train)
    y_proba = holdout_estimator.predict_proba(x_test)[:, 1]
    precision, recall, thresholds = precision_recall_curve(y_test, y_proba)
    f1_values = 2 * precision[:-1] * recall[:-1] / np.maximum(
        precision[:-1] + recall[:-1],
        1e-12,
    )
    best_index = int(np.nanargmax(f1_values))
    best_threshold = float(thresholds[best_index])
    y_pred = (y_proba >= best_threshold).astype(int)
    matrix = confusion_matrix(y_test, y_pred)
    fraction_positive, mean_predicted = calibration_curve(
        y_test,
        y_proba,
        n_bins=8,
        strategy="quantile",
    )
    result["threshold_analysis"] = {
        "model": selected_name,
        "holdout_rows": len(y_test),
        "positive_rate": round(float(np.mean(y_test)), 4),
        "average_precision": round(float(average_precision_score(y_test, y_proba)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, y_proba)), 4),
        "f1_optimal_threshold": round(best_threshold, 4),
        "precision_at_threshold": round(
            float(precision_score(y_test, y_pred, zero_division=0)),
            4,
        ),
        "recall_at_threshold": round(float(recall_score(y_test, y_pred, zero_division=0)), 4),
        "f1_at_threshold": round(float(f1_score(y_test, y_pred, zero_division=0)), 4),
        "confusion_matrix": matrix.astype(int).tolist(),
    }
    recall_targets = {}
    recall_target_threshold_values = {}
    for target_recall in (0.9,):
        candidate_indices = [
            index for index, recall_value in enumerate(recall[:-1]) if recall_value >= target_recall
        ]
        if not candidate_indices:
            continue
        best_target_index = max(
            candidate_indices,
            key=lambda index: (precision[index], thresholds[index]),
        )
        target_threshold = float(thresholds[best_target_index])
        recall_target_threshold_values[f"recall_{target_recall:.2f}"] = target_threshold
        target_pred = (y_proba >= target_threshold).astype(int)
        target_matrix = confusion_matrix(y_test, target_pred)
        recall_targets[f"recall_{target_recall:.2f}"] = {
            "target_recall": target_recall,
            "threshold": round(target_threshold, 4),
            "precision": round(
                float(precision_score(y_test, target_pred, zero_division=0)),
                4,
            ),
            "recall": round(float(recall_score(y_test, target_pred, zero_division=0)), 4),
            "f1": round(float(f1_score(y_test, target_pred, zero_division=0)), 4),
            "false_positives": int(target_matrix[0][1]),
            "false_negatives": int(target_matrix[1][0]),
            "confusion_matrix": target_matrix.astype(int).tolist(),
        }
    result["recall_target_thresholds"] = recall_targets
    policies = {"f1_optimal": best_threshold}
    policies.update(recall_target_threshold_values)
    result["false_negative_analysis"] = build_false_negative_analysis(
        policies=policies,
        y_test=y_test,
        y_proba=y_proba,
        test_indices=test_indices,
        answerable_results=answerable_results or [],
        country_lookup=country_lookup or {},
    )
    result["precision_recall_curve"] = [
        {
            "threshold": round(float(threshold), 6),
            "precision": round(float(precision_value), 6),
            "recall": round(float(recall_value), 6),
            "f1": round(float(f1_value), 6),
        }
        for threshold, precision_value, recall_value, f1_value in zip(
            thresholds,
            precision[:-1],
            recall[:-1],
            f1_values,
        )
    ]
    result["calibration"] = {
        "model": selected_name,
        "brier_score": round(float(brier_score_loss(y_test, y_proba)), 4),
        "mean_predicted_probability": [round(float(value), 6) for value in mean_predicted],
        "fraction_positive": [round(float(value), 6) for value in fraction_positive],
        "interpretation": "Use probabilities for ranking until calibration is validated on a cleaner holdout.",
    }
    return result


def build_false_negative_analysis(
    *,
    policies,
    y_test,
    y_proba,
    test_indices,
    answerable_results,
    country_lookup,
) -> dict:
    rows = []
    summary = {}
    for policy, threshold in policies.items():
        policy_false_negatives = 0
        for holdout_row, (label, probability, source_index) in enumerate(
            zip(y_test, y_proba, test_indices, strict=True)
        ):
            predicted_failure = int(probability >= threshold)
            if int(label) != 1 or predicted_failure != 0:
                continue
            policy_false_negatives += 1
            source = (
                answerable_results[int(source_index)]
                if int(source_index) < len(answerable_results)
                else {}
            )
            iso_code = source.get("iso_code") or source.get("expected_iso_code") or "unknown"
            rows.append(
                {
                    "policy": policy,
                    "threshold": round(float(threshold), 6),
                    "holdout_row": holdout_row,
                    "source_index": int(source_index),
                    "predicted_failure_probability": round(float(probability), 6),
                    "question_type": source.get("question_type") or "unknown",
                    "iso_code": iso_code,
                    "country": source.get("country") or country_lookup.get(iso_code) or "unknown",
                    "failure_stage": source.get("failure_stage") or "unknown",
                    "failure_reasons": " | ".join(source.get("failure_reasons") or []),
                    "retrieval_hit": bool(source.get("retrieval_hit")),
                    "evidence_hit": bool(source.get("evidence_hit")),
                    "citation_hit": bool(source.get("citation_hit")),
                    "answer_correct": bool(source.get("answer_correct")),
                    "question": source.get("question") or "",
                    "answer_preview": _trim_csv_text(source.get("answer_text") or ""),
                }
            )
        summary[policy] = {
            "threshold": round(float(threshold), 6),
            "false_negatives": policy_false_negatives,
        }
    return {"summary": summary, "rows": rows}


def load_country_lookup(documents_path: Path) -> dict[str, str]:
    if not documents_path.exists():
        return {}
    documents = json.loads(documents_path.read_text(encoding="utf-8"))
    lookup: dict[str, str] = {}
    for document in documents:
        iso_code = str(document.get("iso_code") or "").strip().upper()
        country = str(document.get("country") or "").strip()
        if not iso_code:
            document_id = str(document.get("document_id") or "").strip().lower()
            if "_" in document_id and len(document_id.rsplit("_", 1)[-1]) == 2:
                iso_code = document_id.rsplit("_", 1)[-1].upper()
        if not country:
            title = str(document.get("title") or "").strip()
            if "(" in title:
                country = title.split("(", 1)[0].strip().title()
        if iso_code and country and iso_code not in lookup:
            lookup[iso_code] = country
    return lookup


def build_shap_explainability(
    *,
    estimator,
    rows,
    labels,
    feature_names,
    answerable_results,
    country_lookup,
) -> dict:
    try:
        import numpy as np
        import shap
    except ImportError as exc:
        return {
            "available": False,
            "error": f"{type(exc).__name__}: {exc}",
            "fallback": "permutation_importance",
        }

    try:
        row_array = np.asarray(rows, dtype=float)
        explainer = shap.TreeExplainer(estimator)
        shap_values = explainer.shap_values(row_array)
        if isinstance(shap_values, list):
            shap_values = shap_values[-1]
        shap_values = np.asarray(shap_values, dtype=float)
        if shap_values.ndim == 3:
            shap_values = shap_values[:, :, -1]

        mean_abs = np.mean(np.abs(shap_values), axis=0)
        mean_signed = np.mean(shap_values, axis=0)
        feature_means = np.mean(row_array, axis=0)
        ranked_indices = list(np.argsort(-mean_abs))[:15]
        probabilities = estimator.predict_proba(row_array)[:, 1]

        high_risk_indices = list(np.argsort(-probabilities))[:3]
        missed_failure_indices = [
            index
            for index, (label, probability) in enumerate(zip(labels, probabilities, strict=True))
            if int(label) == 1 and probability < 0.5
        ][:3]
        local_indices = []
        for index in [*high_risk_indices, *missed_failure_indices]:
            if index not in local_indices:
                local_indices.append(index)
        sample_size = min(500, len(row_array))
        sample_indices = list(np.linspace(0, len(row_array) - 1, sample_size, dtype=int)) if sample_size else []

        return {
            "available": True,
            "library": "shap",
            "explainer": "TreeExplainer",
            "value_space": "model margin/log-odds",
            "global_importance": [
                {
                    "feature": feature_names[index],
                    "mean_abs_shap": round(float(mean_abs[index]), 6),
                    "mean_shap": round(float(mean_signed[index]), 6),
                    "feature_mean": round(float(feature_means[index]), 6),
                    "direction": "pushes_failure_up"
                    if mean_signed[index] > 0
                    else (
                        "pushes_failure_down"
                        if mean_signed[index] < 0
                        else "mixed_or_neutral"
                    ),
                }
                for index in ranked_indices
            ],
            "local_explanations": [
                build_local_shap_explanation(
                    index=index,
                    probability=float(probabilities[index]),
                    label=int(labels[index]),
                    shap_row=shap_values[index],
                    feature_row=row_array[index],
                    feature_names=feature_names,
                    answerable_results=answerable_results,
                    country_lookup=country_lookup,
                )
                for index in local_indices
            ],
            "plot_sample": {
                "feature_names": feature_names,
                "shap_values": [
                    [round(float(value), 6) for value in shap_values[index]]
                    for index in sample_indices
                ],
                "feature_values": [
                    [round(float(value), 6) for value in row_array[index]]
                    for index in sample_indices
                ],
            },
        }
    except Exception as exc:  # pragma: no cover - dependency-specific fallback
        return {
            "available": False,
            "error": f"{type(exc).__name__}: {exc}",
            "fallback": "permutation_importance",
        }


def build_local_shap_explanation(
    *,
    index,
    probability,
    label,
    shap_row,
    feature_row,
    feature_names,
    answerable_results,
    country_lookup,
) -> dict:
    index = int(index)
    label = int(label)
    probability = float(probability)
    ranked = sorted(
        range(len(feature_names)),
        key=lambda feature_index: abs(float(shap_row[feature_index])),
        reverse=True,
    )[:8]
    source = answerable_results[index] if index < len(answerable_results) else {}
    iso_code = source.get("iso_code") or source.get("expected_iso_code") or "unknown"
    return {
        "source_index": index,
        "example_type": "missed_failure" if label == 1 and probability < 0.5 else "high_risk",
        "actual_failure": bool(label),
        "predicted_failure_probability": round(probability, 6),
        "question_type": source.get("question_type") or "unknown",
        "iso_code": iso_code,
        "country": source.get("country") or country_lookup.get(iso_code) or "unknown",
        "failure_stage": source.get("failure_stage") or "pass",
        "question": source.get("question") or "",
        "top_contributions": [
            {
                "feature": feature_names[feature_index],
                "feature_value": round(float(feature_row[feature_index]), 6),
                "shap_value": round(float(shap_row[feature_index]), 6),
                "direction": "pushes_failure_up"
                if float(shap_row[feature_index]) > 0
                else "pushes_failure_down",
            }
            for feature_index in ranked
        ],
    }


def write_false_negative_table(selection: dict, output_path: Path) -> None:
    rows = selection.get("false_negative_analysis", {}).get("rows", [])
    fieldnames = [
        "policy",
        "threshold",
        "holdout_row",
        "source_index",
        "predicted_failure_probability",
        "question_type",
        "iso_code",
        "country",
        "failure_stage",
        "failure_reasons",
        "retrieval_hit",
        "evidence_hit",
        "citation_hit",
        "answer_correct",
        "question",
        "answer_preview",
    ]
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _trim_csv_text(value: str, max_chars: int = 220) -> str:
    cleaned = " ".join(str(value).split())
    if len(cleaned) <= max_chars:
        return cleaned
    return cleaned[: max_chars - 3].rstrip() + "..."


def write_combined_report(result: dict, selection: dict, output_path: Path) -> None:
    lines = [
        "# Answer Failure Prediction Model",
        "",
        (
            "This supervised ML layer predicts whether a benchmark answer will fail "
            "from retrieval, query, citation, metadata, and routing features."
        ),
        "",
        "## Dataset",
        "",
        f"- Rows: `{result['dataset']['rows']}`",
        f"- Features: `{result['dataset']['features']}`",
        f"- Failure rate: `{result['dataset']['positive_failure_rate']}`",
        (
            f"- Train/test rows for transparent LR: `{result['dataset']['train_rows']}` / "
            f"`{result['dataset']['test_rows']}`"
        ),
        "",
        "## Sklearn Model Selection",
        "",
        (
            "The primary model-selection workflow uses stratified 5-fold cross-validation. "
            "The from-scratch logistic regression remains as a transparency appendix, "
            "not the primary selected model."
        ),
        "",
        "| Model | ROC-AUC mean | ROC-AUC std | Average precision | F1 |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for row in selection.get("models", []):
        lines.append(
            f"| `{row['model']}` | {row['roc_auc_mean']} | {row['roc_auc_std']} | "
            f"{row['average_precision_mean']} | {row['f1_mean']} |"
        )
    lines.extend(
        [
            "",
            f"Selected model: `{selection.get('selected_model')}`.",
            "",
            "## Threshold Selection",
            "",
        ]
    )
    threshold = selection.get("threshold_analysis", {})
    if threshold:
        lines.extend(
            [
                (
                    "The selected model is evaluated on a stratified holdout for threshold "
                    "selection. Because failures are rare, the report uses the F1-optimal "
                    "threshold from the Precision-Recall curve instead of an undefended "
                    "`0.50` cutoff."
                ),
                "",
                "| Model | Threshold | Precision | Recall | F1 | Average precision | ROC-AUC |",
                "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
                (
                    f"| `{threshold['model']}` | {threshold['f1_optimal_threshold']} | "
                    f"{threshold['precision_at_threshold']} | "
                    f"{threshold['recall_at_threshold']} | {threshold['f1_at_threshold']} | "
                    f"{threshold['average_precision']} | {threshold['roc_auc']} |"
                ),
                "",
            ]
        )
    recall_targets = selection.get("recall_target_thresholds", {})
    if recall_targets:
        lines.extend(
            [
                "## Recall-Target Review Policy",
                "",
                (
                    "For failure detection, false negatives are the most dangerous error: "
                    "the model says an answer is safe, but the answer is wrong. The report "
                    "therefore also evaluates a recall-target threshold for manual review."
                ),
                "",
                "| Policy | Threshold | Precision | Recall | F1 | False positives | False negatives |",
                "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
            ]
        )
        for policy, values in recall_targets.items():
            lines.append(
                f"| `{policy}` | {values['threshold']} | {values['precision']} | "
                f"{values['recall']} | {values['f1']} | {values['false_positives']} | "
                f"{values['false_negatives']} |"
            )
        lines.append("")
    false_negative_analysis = selection.get("false_negative_analysis", {})
    false_negative_summary = false_negative_analysis.get("summary", {})
    if false_negative_summary:
        lines.extend(
            [
                "## False-Negative Audit",
                "",
                (
                    "False negatives are failed answers that the model would not send to "
                    "manual review under a given threshold. These are the riskiest cases for "
                    "an operational failure detector."
                ),
                "",
                "| Policy | Threshold | Missed failures |",
                "| --- | ---: | ---: |",
            ]
        )
        for policy, values in false_negative_summary.items():
            lines.append(
                f"| `{policy}` | {values['threshold']} | {values['false_negatives']} |"
            )
        lines.extend(
            [
                "",
                "Detailed cases are written to `reports/tables/failure_model_false_negatives.csv`.",
                "",
            ]
        )
    calibration = selection.get("calibration", {})
    if calibration:
        lines.extend(
            [
                "## Calibration",
                "",
                (
                    f"Holdout Brier score is `{calibration['brier_score']}`. "
                    "The model is strong for risk ranking, but the probabilities should "
                    "not be treated as operationally calibrated until validated on a cleaner "
                    "holdout or calibrated with a dedicated calibration step."
                ),
                "",
            ]
        )
    proxy_audit = selection.get("proxy_feature_audit", {})
    if proxy_audit:
        proxy_delta = proxy_audit["roc_auc_delta"]
        proxy_interpretation = (
            "`answer_length` has low proxy risk under this CV check."
            if proxy_delta < 0.01
            else (
                "`answer_length` has moderate proxy risk and should be monitored."
                if proxy_delta < 0.03
                else (
                    "`answer_length` has high proxy risk. The current model is useful "
                    "for post-answer triage, but a production pre-answer risk model "
                    "should remove it or report a separate no-answer-length model."
                )
            )
        )
        lines.extend(
            [
                "## Proxy Feature Audit",
                "",
                (
                    "`answer_length` is output-derived, so it can be a fragile proxy for "
                    "question complexity or synthesizer behavior. The report compares the "
                    "selected model with and without this feature using the same CV protocol."
                ),
                "",
                "| Audit | ROC-AUC mean | Delta vs full model | Average precision | F1 |",
                "| --- | ---: | ---: | ---: | ---: |",
                (
                    f"| Full selected model | {proxy_audit['full_roc_auc_mean']} | 0.0 | "
                    f"{next(row for row in selection.get('models', []) if row['model'] == proxy_audit['selected_model'])['average_precision_mean']} | "
                    f"{next(row for row in selection.get('models', []) if row['model'] == proxy_audit['selected_model'])['f1_mean']} |"
                ),
                (
                    f"| Without `answer_length` | "
                    f"{proxy_audit['without_answer_length_roc_auc_mean']} | "
                    f"{proxy_audit['roc_auc_delta']} | "
                    f"{proxy_audit['without_answer_length_average_precision_mean']} | "
                    f"{proxy_audit['without_answer_length_f1_mean']} |"
                ),
                "",
                proxy_interpretation,
                "",
                (
                    "`expected_term_count` is different: it is known before answer synthesis, "
                    "so it is a more defensible complexity feature than `answer_length`."
                ),
                "",
            ]
        )
    lines.extend(
        [
            "## Class Imbalance",
            "",
            (
                f"The positive failure rate is `{selection.get('positive_failure_rate', 0):.4f}`. "
                "The notebook compares unweighted logistic regression with "
                "`class_weight='balanced'` "
                "and balanced tree models."
            ),
            "",
            "## Transparent Baseline",
            "",
            "| Model | ROC-AUC | Average precision | F1 | Recall | Precision | Accuracy |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
            (
                f"| From-scratch logistic model | {result['metrics']['roc_auc']} | "
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
            "## Explainability",
            "",
        ]
    )
    shap_explainability = selection.get("shap_explainability", {})
    if shap_explainability.get("available"):
        lines.extend(
            [
                (
                    "SHAP TreeExplainer is available for the selected XGBoost model. "
                    "Positive SHAP values push the prediction toward answer failure; "
                    "negative values push it toward safe/correct."
                ),
                "",
                "### Global SHAP Importance",
                "",
                "| Feature | Mean abs SHAP | Mean SHAP | Direction |",
                "| --- | ---: | ---: | --- |",
            ]
        )
        for item in shap_explainability.get("global_importance", [])[:12]:
            lines.append(
                f"| `{item['feature']}` | {item['mean_abs_shap']} | "
                f"{item['mean_shap']} | {item['direction']} |"
            )
        lines.extend(
            [
                "",
                "### Local SHAP Examples",
                "",
                (
                    "Local examples show why specific cases were scored as high risk or "
                    "missed by a low predicted failure probability."
                ),
                "",
            ]
        )
        for example in shap_explainability.get("local_explanations", [])[:4]:
            lines.extend(
                [
                    (
                        f"- `{example['example_type']}` `{example['iso_code']}` "
                        f"`{example['question_type']}` p="
                        f"`{example['predicted_failure_probability']}`: "
                        f"{example['question']}"
                    ),
                    "  Top SHAP contributions: "
                    + "; ".join(
                        f"`{item['feature']}`={item['shap_value']}"
                        for item in example.get("top_contributions", [])[:4]
                    ),
                ]
            )
        lines.extend(["", "### Permutation Importance Fallback", ""])
    else:
        lines.extend(
            [
                (
                    "SHAP was unavailable, so the report uses permutation importance for "
                    "the selected sklearn model as the fallback explainability path."
                ),
                "",
            ]
        )
        if shap_explainability.get("error"):
            lines.extend([f"SHAP error: `{shap_explainability['error']}`.", ""])
    lines.extend(
        [
            "",
            "| Feature | Importance mean | Importance std |",
            "| --- | ---: | ---: |",
        ]
    )
    for item in selection.get("permutation_importance", [])[:12]:
        lines.append(
            f"| `{item['feature']}` | {item['importance_mean']} | {item['importance_std']} |"
        )
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
