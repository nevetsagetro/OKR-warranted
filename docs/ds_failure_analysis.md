# Data Science Failure Analysis

## Summary

The full country regression benchmark was rerun against the promoted workspace `data/work` with `top_k=5`.

| Metric | Value |
| --- | ---: |
| Total cases | 2,799 |
| Retrieval recall@k | 0.9946 |
| Evidence hit rate | 0.9868 |
| Document precision@k | 0.9946 |
| Citation accuracy | 0.8975 |
| Answer correctness | 0.9268 |
| Country match@1 | 0.9950 |
| Foreign evidence rate | 0.0025 |
| Wrong-country answer rate | 0.0050 |

The main finding is that the system is no longer primarily retrieval-limited. Retrieval recall, evidence hit rate, document precision, and country match are all near-perfect, but answer correctness is lower at `0.9268` and citation accuracy is lower at `0.8975`.

That makes the next DS hypothesis concrete: answer quality is now driven more by citation anchoring, answer synthesis, and specific data-quality segments than by broad retrieval recall.

## Notebook Charts

The failure-stage, question-type, and ISO-segment charts now render inline in `notebooks/01_failure_analysis.ipynb` instead of being exported as separate image files. The supporting tables are written to `reports/tables/`.

## Finding 1: Most remaining failures are citation or synthesis failures

Out of `2,799` cases, `2,402` passed and `397` had a classified failure stage.

| Failure stage | Count |
| --- | ---: |
| citation | 227 |
| answer_synthesis | 109 |
| ingestion | 33 |
| retrieval | 22 |
| grounding | 4 |
| geo_precision | 2 |

The most common failure reason was: `returned citations did not match the expected source anchor` with `227` cases. The second was: `answer did not express expected terms` with `109` cases.

**Interpretation:** the system usually retrieves the right document and evidence, but the final answer/citation contract is stricter than the current answer layer. The next improvement should target citation-anchor selection and answer templates for high-risk question types.

## Finding 2: Weakness is concentrated by question type

| Question type | Correct | Total | Answer correctness |
| --- | ---: | ---: | ---: |
| table_extraction | 1 | 10 | 0.1000 |
| binary | 507 | 613 | 0.8271 |
| policy_rule | 539 | 584 | 0.9229 |
| procedural | 175 | 189 | 0.9259 |
| sender_type_capability | 145 | 156 | 0.9295 |
| factoid | 196 | 204 | 0.9608 |
| sender_type_policy | 401 | 407 | 0.9853 |
| capability | 426 | 431 | 0.9884 |
| duration | 204 | 205 | 0.9951 |

**Interpretation:** capability and duration questions are now strong. In this original audit, the obvious weak segment was `table_extraction`, but it only had `10` cases. The more important product-scale issue was `binary`, because it had `613` cases and only `0.8271` correctness.

**Follow-up:** binary templating was promoted through V2 and reached `0.9935` binary correctness. The table slice was then expanded from `10` to `50` cases and hardened with row-aware retrieval plus table answer templates; the expanded table slice now reaches `0.88` evidence hit rate, `0.82` citation accuracy, and `0.86` answer correctness. See `docs/table_extraction_hardening.md`.

**Next experiment:** split binary questions by expected row key and sender type. If errors cluster around a few rows such as sender support or registration requirements, fix answer templates or enrichment normalization for those rows first.

## Finding 3: A small set of country segments needs targeted review

Worst ISO segments with at least 10 cases:

| ISO | Correct | Total | Answer correctness |
| --- | ---: | ---: | ---: |
| US | 8 | 17 | 0.4706 |
| IN | 10 | 15 | 0.6667 |
| AE | 9 | 13 | 0.6923 |
| SA | 12 | 17 | 0.7059 |
| LK | 10 | 14 | 0.7143 |
| TC | 10 | 14 | 0.7143 |
| CR | 11 | 14 | 0.7857 |
| CD | 11 | 14 | 0.7857 |
| DM | 11 | 14 | 0.7857 |
| IT | 11 | 14 | 0.7857 |

**Interpretation:** the weak countries are not mainly wrong-country retrieval failures. Country match@1 is `0.9950`, while wrong-country answer rate is only `0.0050`. These countries likely have harder source structure, ambiguous policy wording, or answer-template mismatches.

**Next experiment:** audit the top 5 weak ISO segments manually and compare their source structure against high-performing countries. This should become a corpus EDA task in Phase 11.

## Research Conclusion

The strongest portfolio claim from this analysis is:

> On a 2,799-case country regression benchmark, hybrid retrieval is already highly reliable (`0.9946` recall@k and `0.9950` country match@1). Remaining error is concentrated in citation anchoring, answer synthesis, binary question handling, and a small set of country segments.

That is a data science result, not only an engineering status check. It identifies what changed, what still fails, where the failures are concentrated, and which experiment should come next.

## Artifacts

- Notebook: `notebooks/01_failure_analysis.ipynb`
- Evaluation JSON: `data/work/evaluation/latest-evaluation.json`
- Evaluation markdown: `data/work/evaluation/latest-evaluation.md`
- Summary table: `reports/tables/failure_analysis_summary.json`
- Question-type table: `reports/tables/question_type_correctness.csv`
- Worst-ISO table: `reports/tables/worst_iso_correctness.csv`
- Figures: rendered inline in `notebooks/01_failure_analysis.ipynb`
