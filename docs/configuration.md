# Configuration Reference

Configuration is environment-variable driven so the same code path can run local-only or with provider-backed enrichment, embeddings, vector stores, reranking, and synthesis.

## Mapping And Enrichment

| Variable | Typical Value | Description |
| --- | --- | --- |
| `OKR_MAPPING_PROVIDER` | `local` | Selects local or provider-backed ingest enrichment. |
| `OKR_MAPPING_MODEL` | `heuristic-v1` | Mapping/enrichment model or profile. |
| `OKR_MAPPING_BATCH_SIZE` | `16` | Batch size for enrichment. |
| `OKR_PROVIDER_MODEL_PROBE_ENABLED` | `false` | When true, startup checks provider model-list APIs. |

## Embeddings

| Variable | Typical Value | Description |
| --- | --- | --- |
| `OKR_EMBEDDING_PROVIDER` | `local` | Embedding provider. |
| `OKR_EMBEDDING_MODEL` | `BAAI/bge-small-en-v1.5` | Embedding model label. |
| `OKR_EMBEDDING_DEVICE` | `cpu` | Runtime device for local embeddings. |
| `OKR_EMBEDDING_DIMENSIONS` | empty or `1536` | Dimension override when supported. |

## Vector Store

| Variable | Typical Value | Description |
| --- | --- | --- |
| `OKR_VECTOR_BACKEND` | `local` | Vector backend: local, ChromaDB, or Qdrant. |
| `OKR_VECTOR_COLLECTION` | `own-knowledge-rag` | Vector collection/index name. |
| `OKR_QDRANT_URL` | `http://localhost:6333` | Qdrant URL when using Qdrant. |
| `OKR_QDRANT_API_KEY` | empty | Optional Qdrant API key. |

## Reranking

| Variable | Typical Value | Description |
| --- | --- | --- |
| `OKR_RERANKER_PROVIDER` | `none` | Reranker provider. |
| `OKR_RERANKER_MODEL` | `cross-encoder/ms-marco-MiniLM-L-6-v2` | Cross-encoder model label. |
| `OKR_RERANKER_TOP_N` | `10` | Number of retrieved candidates reranked. |

## Answer Synthesis

| Variable | Typical Value | Description |
| --- | --- | --- |
| `OKR_GENERATION_PROVIDER` | `none` or `local` | Answer synthesis provider. |
| `OKR_GENERATION_MODEL` | `extractive-fusion-v1` | Synthesis model/profile. |
| `OKR_GENERATION_MAX_EVIDENCE` | `5` | Maximum evidence blocks used in synthesis. |

Routed `tier2` answers can use grounded multi-block synthesis with inline citations. `tier0`, `tier1`, and `refusal` remain local and extractive.

## Query Cache And Routing

| Variable | Typical Value | Description |
| --- | --- | --- |
| `OKR_QUERY_CACHE_ENABLED` | `true` | Enables persisted query caching. |
| `OKR_TIER0_SCORE_THRESHOLD` | `0.75` | Highest-confidence local-answer route threshold. |
| `OKR_TIER2_SCORE_THRESHOLD` | `0.55` | Routed synthesis threshold. |

The cache key includes normalized query text plus retrieval and synthesis provenance, so model/backend changes do not silently reuse stale answers.

## Optional Provider Examples

Local cross-encoder reranker:

```bash
pip install -e .[dev,huggingface]
export OKR_RERANKER_PROVIDER=cross_encoder
export OKR_RERANKER_MODEL=cross-encoder/ms-marco-MiniLM-L-6-v2
export OKR_RERANKER_TOP_N=10
okr build-index --source-dir data/raw --work-dir data/work
```

ChromaDB:

```bash
pip install -e .[dev,chromadb]
export OKR_VECTOR_BACKEND=chromadb
export OKR_VECTOR_COLLECTION=own-knowledge-rag
okr build-index --source-dir data/raw --work-dir data/work
```

Qdrant:

```bash
pip install -e .[dev,qdrant]
export OKR_VECTOR_BACKEND=qdrant
export OKR_VECTOR_COLLECTION=own-knowledge-rag
export OKR_QDRANT_URL=http://localhost:6333
okr build-index --source-dir data/raw --work-dir data/work
```
