# Architecture

## Design

The system is split into five layers:

1. parsing
2. normalization
3. semantic mapping
4. indexing
5. retrieval
6. answering

The architecture and roadmap documents are intentionally included in
`data/raw/docs/` as a self-referential demo of the system answering questions
about itself.

## Flow

`raw documents -> parsed document -> knowledge blocks -> semantic mapping -> lexical/vector indexes -> hybrid retrieval -> grounded answer`

On rebuild, unchanged source documents can be reused from the persisted index state so
the system skips re-parsing, re-normalizing, re-mapping, and re-embedding for those files.

Parsing records detected source encoding and fallback warnings on each `ParsedDocument`.
Markdown fenced code blocks are preserved as `code_sample` blocks rather than removed.
Build manifests report encoding fallback files plus preserved/erased code-block counts.

## Canonical Unit

The primary retrieval unit is a `KnowledgeBlock`, not a raw chunk.

Each block contains:

- `block_id`
- `document_id`
- `title`
- `section_path`
- `block_type`
- `text`
- `source_path`
- `anchors`
- `metadata`

The metadata layer is where semantic mapping enrichments live:

- parser/normalizer provenance
- mapping provider + mapping model
- semantic intent
- row and section hints used by retrieval
- block-level channel tags detected from block text and section path
- section-derived character offsets for source anchoring
- enrichment provider, model, and timestamp on each block

Enrichment cache keys are content-based and include template/provider/model
provenance plus the canonical terms ontology version. Legacy block-id cache keys
remain readable during rebuilds and are migrated into the current cache key when
encountered.

The canonical ontology is grouped by telecom concept family, including sender
identity, numbering, messaging capabilities, registration and compliance,
policy and consent, and operations. Post-enrichment validation flags possible
drift when enriched text drops too many source numbers, ISO codes, or proper
nouns; flagged blocks remain searchable but are counted in build manifests as
`drift_risk_blocks`.

## Retrieval Strategy

Retrieval is hybrid:

- BM25-style lexical scoring for exact terminology
- vector scoring for semantic similarity
- vector backend selected through config, with `local`, `ChromaDB`, and `Qdrant` implemented
- reciprocal rank fusion for candidate merging
- rule-based reranking for document and section specificity
- embedding provider/model selected through config or CLI flags
- RRF arm weights are configurable with `OKR_RRF_LEXICAL_WEIGHT` and
  `OKR_RRF_VECTOR_WEIGHT`, both defaulting to `1.0` so lexical and vector arms
  have equal influence unless an experiment says otherwise
- retrieval arm breadth is configurable with `OKR_ARM_K_MULTIPLIER`, defaulting
  to `3` for normal queries while aggregate queries still widen enough to
  gather cross-country candidates
- final results enforce `OKR_MAX_BLOCKS_PER_DOCUMENT`, defaulting to `2`, after
  reranking and before slicing so one document cannot crowd out all other
  evidence

## Model Selection

Mapping and retrieval models are selected through configuration rather than code edits.

- semantic mapper: `OKR_MAPPING_PROVIDER`, `OKR_MAPPING_MODEL`
- semantic mapper batch size: `OKR_MAPPING_BATCH_SIZE`
- embedding model: `OKR_EMBEDDING_PROVIDER`, `OKR_EMBEDDING_MODEL`, `OKR_EMBEDDING_DEVICE`
- embedding dimensions: `OKR_EMBEDDING_DIMENSIONS`
- vector backend: `OKR_VECTOR_BACKEND`, `OKR_VECTOR_COLLECTION`
- Qdrant connection: `OKR_QDRANT_URL`, `OKR_QDRANT_API_KEY`
- reranker: `OKR_RERANKER_PROVIDER`, `OKR_RERANKER_MODEL`, `OKR_RERANKER_TOP_N`
- Tier 2 synthesis: `OKR_GENERATION_PROVIDER`, `OKR_GENERATION_MODEL`, `OKR_GENERATION_MAX_EVIDENCE`
- query cache: `OKR_QUERY_CACHE_ENABLED`
- build manifests record the selected models so re-indexing and query behavior stay traceable

## Answer Strategy

The answer layer is grounded and tiered:

- choose the best evidence blocks
- use direct/extractive answers for `tier0` and `tier1`
- optionally use a grounded generator for `tier2`
- list supporting evidence and source anchors
- refuse when support is weak

The current pipeline also records:

- detected query intent
- routed tier (`tier0`, `tier1`, `tier2`, `refusal`)
- citation accuracy in evaluation artifacts
- tier distribution in evaluation artifacts

Routing is now threshold-driven as well as heuristic-driven:

- refusal thresholds: score and overlap
- Tier 0 threshold: high-confidence direct return
- Tier 2 threshold: escalation for lower-confidence multi-document cases

Tier 2 can synthesize across multiple blocks while still being constrained to
retrieved evidence and citation-aware templates.

Tier 1 and Tier 2 answers can also be cached on disk by normalized query plus
retrieval/synthesis provenance. Cached answers preserve evidence blocks so API
responses remain inspectable.

The evaluation layer now separates:

- retrieval recall
- evidence hit rate
- citation accuracy
- answer correctness
- segment metrics by block type, question type, and ISO code
- statistical experiment comparison with bootstrap confidence intervals and a
  paired sign test over per-case metric deltas
- benchmark distribution audits for ISO code, question type, sender type, and
  block type

This makes it easier to see whether failures come from ranking, grounding, citation selection,
or synthesis.

Experiment workflows can create isolated candidate workspaces, compare them
against the promoted workspace, and record local experiment state in
`data/experiments/registry.json` when the UI/API experiment flow is used.

Loaded retrievers are cached per `work_dir` in a three-entry LRU cache. Cached
retrievers are invalidated when the workspace manifest is newer than the cached
load time, so long-running API processes pick up rebuilt indexes without
unbounded memory growth.
