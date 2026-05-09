# CLI Reference

This page keeps the detailed command examples out of the README so the repository front page stays readable.

## Core Workflow

Build the index:

```bash
okr build-index --source-dir data/raw --work-dir data/work
```

Run the local API and browser UI:

```bash
okr serve-api --host 127.0.0.1 --port 8000
```

Ask a question:

```bash
okr ask --work-dir data/work --question "Sender in Spain?"
```

Run evaluation:

```bash
okr evaluate --work-dir data/work --benchmark-path benchmarks/country_regressions.json
```

## Benchmark And Review Commands

Run a smoke benchmark:

```bash
okr evaluate --work-dir data/work --benchmark-path benchmarks/real_corpus_smoke.json
```

Run a broader real-corpus benchmark:

```bash
okr evaluate --work-dir data/work --benchmark-path benchmarks/real_corpus_core.json
```

Generate an expanded benchmark from the current corpus:

```bash
okr generate-benchmark \
  --source-dir data/raw \
  --output-path benchmarks/real_corpus_expanded.json
```

Generate country regressions:

```bash
okr generate-country-regressions \
  --benchmark-path benchmarks/real_corpus_expanded.json \
  --output-path benchmarks/country_regressions.json
```

Run consistency checks:

```bash
okr check-consistency --work-dir data/work
```

Build reviewer packets:

```bash
okr build-review-packets --work-dir data/work
okr build-review-packets --work-dir data/work --document-id spain_es
```

Seed reviewed findings and export a review benchmark:

```bash
okr seed-review-findings --work-dir data/work
okr export-review-benchmark \
  --review-findings-path data/work/analytics/review_findings.json \
  --output-path benchmarks/review_findings.json
```

Export user-rated query reviews:

```bash
okr export-query-review-benchmark \
  --query-reviews-path data/work/analytics/query_reviews.json \
  --output-path benchmarks/query_review_regressions.json
```

Calibrate refusal thresholds:

```bash
okr calibrate-refusal --work-dir data/work --benchmark-path benchmarks/minimal.json
```

## Experiment Examples

Build only Markdown sources from a mixed corpus:

```bash
okr build-index \
  --source-dir data/raw \
  --work-dir data/work_md_only \
  --allowed-suffixes .md
```

Build with explicit local mapping and Hugging Face embeddings:

```bash
okr build-index \
  --source-dir data/raw \
  --work-dir data/work \
  --mapping-provider local \
  --mapping-model heuristic-v1 \
  --embedding-provider huggingface \
  --embedding-model BAAI/bge-small-en-v1.5 \
  --vector-backend local
```

Force a full re-enrichment by bypassing the enrichment cache:

```bash
okr build-index --force-reenrich
```

## Evaluation Fields

Country-sensitive benchmark cases can include:

- `expected_iso_code`
- `forbid_document_ids`
- `must_not_mix_documents`

Evaluation output reports:

- `retrieval_recall_at_k`
- `evidence_hit_rate`
- `citation_accuracy`
- `answer_correctness`
- `country_match_at_1`
- `foreign_evidence_rate`
- `wrong_country_answer_rate`
