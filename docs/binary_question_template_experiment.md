# Binary Question Template Experiment

## Question

Can the answer layer improve binary yes/no questions by forcing each answer to decide from the relevant structured table row instead of adding a generic yes/no prefix after synthesis?

## Why This Matters

Notebook 01 showed that binary questions were the weakest major segment: `82.7%` answer correctness versus `98.8%` for capability questions. The gap was statistically significant after Bonferroni correction, so this was not random noise. The failure mechanism was also plausible: binary questions require an explicit yes/no commitment, and the extractive answer layer sometimes expressed the supporting fact without making the decision easy to evaluate.

## Intervention

The answerer now applies a structured binary template before generic answer polishing when the query is binary and the retrieved evidence has row metadata.

For structured rows, the template:

- reads `metadata.row_key` and `metadata.row_values`;
- derives the yes/no verdict from the row value only;
- keeps the answer evidence anchored to the selected `SearchHit`;
- names the row used for the decision in the answer text.

Example answer shape:

```text
No. In Afghanistan, short code sender IDs are not supported; the `Twilio supported` row says `Not Supported`.
```

This makes the answer more reviewable because the decision, country, row key, and row value are visible in one sentence.

## Results

Benchmark: `benchmarks/country_regressions.json`

| Metric | Before | After |
| --- | ---: | ---: |
| Overall answer correctness | 0.9268 | 0.9382 |
| Binary answer correctness | 0.8271 | 0.8777 |
| Capability answer correctness | 0.9884 | 0.9907 |
| Evidence hit rate | 0.9868 | 0.9868 |
| Citation accuracy | 0.8975 | 0.8975 |
| Retrieval recall@k | 0.9946 | 0.9946 |

Detailed artifact:

- `reports/tables/binary_template_experiment.json`

## Interpretation

The intervention improved binary correctness by `+5.06pp` and overall correctness by `+1.14pp` without moving retrieval, evidence hit rate, or citation accuracy. That means the gain came from answer expression, not from retrieval changes.

The original success target was binary correctness `>= 90%` without reducing citation accuracy. The experiment improved the segment substantially but stopped at `87.77%`, so it should be treated as a successful v1 intervention but not a final promotion.

## Promotion Decision

Do not declare the binary segment fixed yet.

Keep the structured binary template because it improves correctness and makes answers more auditable, but plan a v2 experiment focused on the remaining binary failures.

## Next Experiment

Split the remaining incorrect binary cases by `row_key`, country, and failure stage. If failures concentrate in a small number of rows, add row-specific templates for those rows.

Proposed next success metric:

- binary correctness `>= 90%`;
- citation accuracy unchanged or improved;
- no increase in zero-evidence or foreign-evidence cases.

## V2 Follow-Up Result

Phase 21 implemented the row-specific follow-up. The diagnostic confirmed that the remaining answer-incorrect binary cases were dominated by `Twilio supported` rows, especially generic alphanumeric support questions that could be confused with `Sender ID preserved` or dynamic-only notes.

After adding row-specific support-row selection and `Twilio supported` verdict handling:

| Metric | V1 | V2 |
| --- | ---: | ---: |
| Overall answer correctness | 0.9382 | 0.9639 |
| Binary answer correctness | 0.8777 | 0.9935 |
| Evidence hit rate | 0.9868 | 0.9875 |
| Citation accuracy | 0.8975 | 0.8975 |

Decision: promote v2. The binary segment is now above the `>=90%` target, and the remaining binary failures are retrieval/source-coverage cases.

Residual risk: binary citation accuracy remains the loose thread. The V1 report showed binary citation accuracy at `67.54%`, far below capability (`100%`) and duration (`96.59%`). V2 fixed answer correctness without materially moving global citation accuracy, so binary citation anchoring should be treated as a separate follow-up from the yes/no answer template.
