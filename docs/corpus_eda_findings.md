# Corpus EDA & Embedding Space Findings

## Summary

Phase 11 profiles the promoted `data/work` corpus as a dataset rather than only as an index artifact.

| Measure | Value |
| --- | ---: |
| Documents | 501 |
| Blocks | 18,734 |
| Vectors | 18,734 |
| Markdown documents | 277 |
| JSON documents | 224 |
| Median block length | 94 chars |
| Mean block length | 162.43 chars |
| P90 block length | 338 chars |
| Max block length | 3,874 chars |

## Notebook Charts

Corpus charts render inline in `notebooks/02_corpus_eda.ipynb`. The embedding projection renders inline in `notebooks/03_embedding_umap.ipynb` only when real UMAP is available; otherwise the notebook records a warning and does not draw a placeholder scatterplot.

## Finding 1: The corpus is mostly structured, not free-form prose

| Block type | Count |
| --- | ---: |
| table_fact | 9,465 |
| structured_fact | 6,252 |
| narrative | 1,661 |
| policy_rule | 1,134 |
| list_item | 210 |
| faq | 12 |

`table_fact` and `structured_fact` account for `15,717` of `18,734` blocks.

## Finding 2: Enrichment coverage is uneven

| Enrichment field | Covered blocks |
| --- | ---: |
| country or ISO | 17,650 |
| sender types | 9,658 |
| regulation topics | 4,642 |
| hypothetical questions | 229 |
| summary | 0 |

Country/ISO coverage matches the Phase 10 result: `country_match_at_1=0.9950`. Hypothetical question coverage is `229` blocks. Summaries are not populated in the promoted workspace.

## Finding 3: The top vocabulary is telecom-specific and row-key heavy

| Tag | Count |
| --- | ---: |
| short code | 6,782 |
| long code | 6,588 |
| key_value | 5,492 |
| pre-registration | 3,880 |
| alphanumeric sender id | 3,707 |
| sms | 3,625 |
| matrix | 2,529 |
| provisioning time | 2,459 |
| dialing code | 1,100 |
| operator network capability | 900 |

The vocabulary contains variants worth normalizing: `sender id preserved` vs `senderid preserved`, `two-way` vs `two-way sms supported`, and extended labels like `alphanumeric sender id (business names like "bird" or "netflix" that send one-way messages)`.

## Finding 4: Low-quality and long blocks are a targeted risk

`1,255` blocks are marked `LOW_QUALITY`, while `17,479` are `ok`.

Median block length is `94` characters. `policy_rule` has the highest median and p95 length: median `233` chars, p90 `642`, p95 `944`, and max `3,680`. `structured_fact` reaches max `3,874`.

`citation` was the largest failure stage in Phase 10 with `227` cases.

The notebook writes a review queue at `reports/tables/long_block_risk.csv`. The table contains `1,123` long-block candidates with `document_id`, `block_id`, `block_type`, text length, p90/p95 flags, tags, preview text, and document-level citation/synthesis failure counts.

## Finding 5: Tag normalization is reviewable, not automatic

The raw tag vocabulary contains `758` unique tags. Fuzzy/token normalization finds two high-confidence candidate groups:

| Canonical suggestion | Variants | Total count |
| --- | ---: | ---: |
| sender id preserved | 2 | 900 |
| content restriction | 2 | 19 |

If approved, these candidates reduce the reviewed vocabulary from `758` to `756` unique tags.

Artifacts:

- `reports/tables/tag_normalization_candidates.csv`
- `reports/tables/tag_normalization_summary.json`

## Finding 6: Embedding vectors are available, but projection requires real UMAP

The promoted workspace has `18,734` vectors for `18,734` blocks.

The notebook `notebooks/03_embedding_umap.ipynb` renders a projection only when `umap-learn` is installed. If UMAP is unavailable, it writes metadata and shows a warning.

Phase 20 adds a quantitative check: cosine silhouette by `block_type` is `-0.0561` on a stratified `2,500`-block sample. The anomaly queue has `100` blocks whose local embedding neighbors mostly have another block type.

## Finding 7: Country-precision leakage is now smaller and explainable

The Phase 20 audit found a specific query-parser issue: capitalized `ID` in `sender ID` could be interpreted as Indonesia's ISO code. Fixing that collision reduced the refreshed foreign/wrong-country audit set from `17` to `14` cases.

| Metric | Before | After |
| --- | ---: | ---: |
| Retrieval recall@k | 0.9946 | 0.9957 |
| Document precision@k | 0.9946 | 0.9957 |
| Country match@1 | 0.9950 | 0.9961 |
| Foreign evidence rate | 0.0025 | 0.0014 |
| Wrong-country answer rate | 0.0050 | 0.0039 |
| Answer correctness | 0.9382 | 0.9382 |

The remaining audit cases are mostly United States benchmark/source coverage misses, plus two `quiet-hours` aggregate-document cases and two Tanzania citation-anchor cases.

## Artifacts

- Corpus EDA notebook: `notebooks/02_corpus_eda.ipynb`
- Embedding projection notebook: `notebooks/03_embedding_umap.ipynb`
- Summary table: `reports/tables/corpus_eda_summary.json`
- Long-block risk queue: `reports/tables/long_block_risk.csv`
- Tag-normalization candidates: `reports/tables/tag_normalization_candidates.csv`
- Tag-normalization summary: `reports/tables/tag_normalization_summary.json`
- Embedding sample: `reports/tables/embedding_projection_sample.json`
- Embedding cluster metrics: `reports/tables/embedding_cluster_metrics.json`
- Embedding anomaly queue: `reports/tables/embedding_anomalous_blocks.csv`
- Foreign-evidence audit: `reports/tables/foreign_evidence_audit.csv`
- Figures: rendered inline in the notebooks