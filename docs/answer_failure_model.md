# Answer Failure Prediction Model

This supervised failure model predicts whether a benchmark answer will fail from retrieval, query, citation, metadata, and routing features.

## Dataset

- Rows: `2799`
- Features: `25`
- Failure rate: `0.0618`
- Train/test rows for transparent LR: `2100` / `699`

## Sklearn Model Selection

The primary model-selection workflow uses stratified 5-fold cross-validation. The from-scratch logistic regression remains as a transparency appendix, not the primary selected model.

| Model | ROC-AUC mean | ROC-AUC std | Average precision | F1 |
| --- | --- | --- | --- | --- |
| `xgboost_balanced` | 0.9702 | 0.0075 | 0.8191 | 0.6506 |
| `random_forest_balanced` | 0.965 | 0.0138 | 0.7743 | 0.658 |
| `hist_gradient_boosting` | 0.9643 | 0.0122 | 0.8074 | 0.6888 |
| `logistic_regression` | 0.9057 | 0.0301 | 0.671 | 0.5298 |
| `logistic_regression_balanced` | 0.9015 | 0.0267 | 0.6531 | 0.4243 |

Selected model: `xgboost_balanced`.

## Threshold Selection

The selected model is evaluated on a stratified holdout for threshold selection. Because failures are rare, the report uses the F1-optimal threshold from the Precision-Recall curve instead of an undefended `0.50` cutoff.

| Model | Threshold | Precision | Recall | F1 | Average precision | ROC-AUC |
| --- | --- | --- | --- | --- | --- | --- |
| `xgboost_balanced` | 0.8972 | 0.8788 | 0.6744 | 0.7632 | 0.8287 | 0.9662 |

## Recall-Target Review Policy

For failure detection, false negatives are the most dangerous error: the model says an answer is safe, but the answer is wrong. The report therefore also evaluates a recall-target threshold for manual review.

| Policy | Threshold | Precision | Recall | F1 | False positives | False negatives |
| --- | --- | --- | --- | --- | --- | --- |
| `recall_0.90` | 0.428 | 0.4937 | 0.907 | 0.6393 | 40 | 4 |

## False-Negative Audit

False negatives are failed answers that the model would not send to manual review under a given threshold.

| Policy | Threshold | Missed failures |
| --- | --- | --- |
| `f1_optimal` | 0.897237 | 14 |
| `recall_0.90` | 0.427984 | 4 |

Detailed cases are written to `reports/tables/failure_model_false_negatives.csv`.

## Calibration

Holdout Brier score is `0.0448`.

## Proxy Feature Audit

`answer_length` is output-derived. The report compares the selected model with and without this feature using the same CV protocol.

| Audit | ROC-AUC mean | Delta vs full model | Average precision | F1 |
| --- | --- | --- | --- | --- |
| Full selected model | 0.9702 | 0.0 | 0.8191 | 0.6506 |
| Without `answer_length` | 0.9229 | 0.0473 | 0.635 | 0.4133 |

## Class Imbalance

The positive failure rate is `0.0618`. The notebook compares unweighted logistic regression with `class_weight='balanced'` and balanced tree models.

## Transparent Baseline

| Model | ROC-AUC | Average precision | F1 | Recall | Precision | Accuracy |
| --- | --- | --- | --- | --- | --- | --- |
| From-scratch logistic model | 0.871 | 0.5993 | 0.4828 | 0.3256 | 0.9333 | 0.9571 |
| Heuristic baseline | 0.7483 | 0.3873 | 0.4035 | 0.5349 | 0.3239 | 0.9027 |

## Explainability

SHAP TreeExplainer is available for the selected XGBoost model. Positive SHAP values push the prediction toward answer failure; negative values push it toward safe/correct.

### Global SHAP Importance

| Feature | Mean abs SHAP | Mean SHAP | Direction |
| --- | --- | --- | --- |
| `answer_length` | 1.700804 | -1.050445 | pushes_failure_down |
| `question_length` | 0.809457 | -0.575882 | pushes_failure_down |
| `citation_hit` | 0.621188 | -0.341758 | pushes_failure_down |
| `expected_term_count` | 0.434713 | -0.161786 | pushes_failure_down |
| `retrieved_section_count` | 0.375799 | -0.202441 | pushes_failure_down |
| `question_type_binary` | 0.239124 | -0.068537 | pushes_failure_down |
| `question_type_sender_type_policy` | 0.158354 | -0.112695 | pushes_failure_down |
| `tier0` | 0.146781 | -0.112888 | pushes_failure_down |
| `section_hit` | 0.087158 | -0.041177 | pushes_failure_down |
| `metadata_hit` | 0.069782 | -0.040216 | pushes_failure_down |
| `expected_sender_type_count` | 0.062945 | -0.030513 | pushes_failure_down |
| `evidence_hit` | 0.062902 | -0.036084 | pushes_failure_down |

### Local SHAP Examples

Local examples show why specific cases were scored as high risk or missed by a low predicted failure probability.

- `high_risk` `FR` `policy_rule` p=`0.997752`: Are there any content restrictions for SMS in France regarding marketing during nighttime?
Top SHAP contributions: `citation_hit`=1.702029; `metadata_hit`=1.422745; `tier0`=1.306869; `retrieved_section_count`=1.041375
- `high_risk` `AL` `table_extraction` p=`0.997142`: What is the default sender ID in Albania if dynamic sender is not used?
Top SHAP contributions: `citation_hit`=2.34854; `metadata_hit`=1.409745; `evidence_hit`=1.191389; `retrieved_section_count`=1.093534
- `high_risk` `IN` `procedural` p=`0.996811`: What should I do if my SMS is rejected in India?
Top SHAP contributions: `citation_hit`=2.13488; `retrieved_section_count`=1.307027; `evidence_hit`=1.058157; `metadata_hit`=0.926544
- `missed_failure` `GE` `factoid` p=`0.312884`: What is the dialing code for Georgia?
Top SHAP contributions: `answer_length`=1.427479; `question_length`=-0.870145; `expected_term_count`=-0.592749; `citation_hit`=-0.2737

### Permutation Importance Fallback

| Feature | Importance mean | Importance std |
| --- | --- | --- |
| `answer_length` | 0.144905 | 0.00438 |
| `question_length` | 0.057925 | 0.009482 |
| `expected_term_count` | 0.024569 | 0.004748 |
| `citation_hit` | 0.023219 | 0.00158 |
| `retrieved_section_count` | 0.007677 | 0.000957 |
| `question_type_sender_type_policy` | 0.005354 | 0.001415 |
| `tier0` | 0.003488 | 0.000318 |
| `question_type_binary` | 0.003066 | 0.000735 |
| `metadata_hit` | 0.000833 | 0.000135 |
| `evidence_hit` | 0.000472 | 0.000157 |
| `section_hit` | 0.000424 | 0.000115 |
| `expected_sender_type_count` | 0.000388 | 0.000152 |