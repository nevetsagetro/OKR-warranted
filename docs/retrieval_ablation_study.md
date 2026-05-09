# Retrieval Ablation Study

This study compares lexical, vector, and hybrid retrieval modes on the frozen benchmark.

## Hypotheses

- Hybrid retrieval should recover expected documents as reliably as either single arm.
- Lexical-heavy fusion should perform well on structured telecom facts and row labels.
- Vector-heavy fusion may help semantic policy questions but can dilute exact evidence matches.

## Setup

- Benchmark: `benchmarks/country_regressions.json`
- Cases: `2799`
- Top-k: `5`
- Candidate arm-k: `40`
- Indexed embedding profile: `local` / `BAAI/bge-small-en-v1.5`

## Results

| Mode | Recall@k | Evidence hit | Block type hit | Metadata hit | Country@1 | MRR | Seconds |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bm25_only` | 1.0 | 0.7949 | 0.0957 | 0.6745 | 0.9996 | 0.9807 | 0.669 |
| `vector_only` | 1.0 | 0.6885 | 0.0379 | 0.4069 | 0.9993 | 0.9996 | 13.381 |
| `hybrid_balanced` | 1.0 | 0.7624 | 0.0518 | 0.6091 | 1.0 | 1.0 | 14.976 |
| `hybrid_lexical_heavy` | 1.0 | 0.8089 | 0.0604 | 0.6652 | 1.0 | 1.0 | 16.059 |
| `hybrid_vector_heavy` | 1.0 | 0.7245 | 0.0454 | 0.5309 | 1.0 | 1.0 | 14.468 |

## Decision

Best local setting: `hybrid_lexical_heavy`. Selected by evidence hit rate, then retrieval recall@k, then metadata hit rate.

## Interpretation

The local benchmark favors exact lexical structure for evidence selection. Vector-only retrieval ranks expected countries/documents well, but it is weaker on evidence terms and metadata-heavy rows. A lexical-heavy hybrid keeps the country/document reliability of hybrid search while recovering more expected terms.

## Embedding Tradeoff

This ablation reuses the promoted local vector snapshot. External embedding-model rebuilds were not run in this local pass.

This completes the local ablation layer. A true external embedding-model comparison requires rebuilding the vector snapshot for each candidate model before rerunning this study.

## Residual Risks

- This is a retrieval-only ablation; citation accuracy and answer correctness still require a full synthesis evaluation run.
- Candidate prefiltering is enabled, so these numbers evaluate retrieval arms inside the production-style filtered search space.
- The promoted vector snapshot uses the indexed local embedding representation; external embedding models were not rebuilt here.
