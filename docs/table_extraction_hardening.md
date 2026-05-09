# Table Extraction Hardening

## Hypothesis

Table-style questions were failing because the retriever and answer layer did not consistently map user wording to the exact row and requested cell. Row-aware retrieval aliases plus cell-aware extractive templates should improve evidence hit rate and citation accuracy without requiring model fine-tuning.

## Benchmark Expansion

The `table_extraction` slice was expanded from `10` to `50` cases in:

- `benchmarks/country_regressions.json`
- `benchmarks/real_corpus_expanded.json`

The original `10` hard cases remain in the benchmark. The added cases are deterministic row-level checks generated from existing indexed table rows, covering:

- `Two-way SMS supported`
- `Number portability available`
- `Twilio supported`
- `Provisioning time`

## Implementation

- Added table-intent row aliases in retrieval for portability, two-way SMS, support rows, registration, dynamic senders, delivery receipts, default sender IDs, and provisioning-time questions.
- Added table-specific reranking bonuses and penalties for exact row matches, description-only provisioning rows, and sender-type focus mismatches.
- Fixed nested US territory ISO parsing so `United States Virgin Islands (US) (VI)` does not satisfy United States `US` queries.
- Added extractive answer templates for number portability, delivery receipts, default sender values, and operator-network support rows.

## Results

Expanded `table_extraction` slice, `n=50`:

| Metric | Result |
| --- | ---: |
| Retrieval recall@k | 0.98 |
| Evidence hit rate | 0.88 |
| Citation accuracy | 0.82 |
| Answer correctness | 0.86 |

Full expanded benchmark, `n=2,839`:

| Metric | Result |
| --- | ---: |
| Retrieval recall@k | 0.9979 |
| Evidence hit rate | 0.9912 |
| Citation accuracy | 0.9024 |
| Answer correctness | 0.9222 |

## Residual Risk

The remaining table failures are mostly multi-intent questions and source-coverage gaps:

- support plus provisioning-time questions where the expected answer requires two table rows,
- handset delivery receipt expectations that are not exposed as a direct normalized row in the indexed source,
- default sender ID expectations that need more precise source anchoring,
- exact duration mismatches, especially where source families disagree.
