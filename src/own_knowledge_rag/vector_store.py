import importlib
import json
from dataclasses import asdict
from itertools import batched
from pathlib import Path

from own_knowledge_rag.config import Settings
from own_knowledge_rag.embeddings import EmbeddingModel, cosine_similarity
from own_knowledge_rag.models import KnowledgeBlock


class VectorStore:
    def search(
        self,
        model: EmbeddingModel,
        query: str,
        top_k: int = 20,
        candidate_ids: set[str] | None = None,
    ) -> list[tuple[KnowledgeBlock, float]]:
        raise NotImplementedError

    def save(self, work_dir: Path) -> None:
        raise NotImplementedError


class LocalVectorStore(VectorStore):
    def __init__(self, blocks: list[KnowledgeBlock], vectors: list[list[float]]) -> None:
        self._blocks = blocks
        self._vectors = vectors

    def search(
        self,
        model: EmbeddingModel,
        query: str,
        top_k: int = 20,
        candidate_ids: set[str] | None = None,
    ) -> list[tuple[KnowledgeBlock, float]]:
        query_vector = model.encode_query(query)
        scored: list[tuple[KnowledgeBlock, float]] = []
        for block, vector in zip(self._blocks, self._vectors, strict=False):
            if candidate_ids is not None and block.block_id not in candidate_ids:
                continue
            scored.append((block, cosine_similarity(query_vector, vector)))
        scored.sort(key=lambda item: item[1], reverse=True)
        return scored[:top_k]

    def save(self, work_dir: Path) -> None:
        path = vector_store_snapshot_path(work_dir)
        payload = {
            "blocks": [asdict(block) for block in self._blocks],
            "vectors": self._vectors,
        }
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, work_dir: Path) -> "LocalVectorStore":
        path = vector_store_snapshot_path(work_dir)
        payload = json.loads(path.read_text(encoding="utf-8"))
        for item in payload["blocks"]:
            item.setdefault("section_heading", "")
        blocks = [KnowledgeBlock(**item) for item in payload["blocks"]]
        vectors = payload["vectors"]
        return cls(blocks, vectors)


class ChromaDBVectorStore(VectorStore):
    def __init__(
        self,
        settings: Settings,
        blocks: list[KnowledgeBlock],
        vectors: list[list[float]],
    ) -> None:
        self._settings = settings
        self._blocks = blocks
        self._vectors = vectors
        self._client = None
        self._collection = None

    def search(self, model: EmbeddingModel, query: str, top_k: int = 20) -> list[tuple[KnowledgeBlock, float]]:
        if not self._blocks:
            return []
        try:
            collection = self._get_collection()
            query_vector = model.encode_query(query)
            results = collection.query(
                query_embeddings=[query_vector],
                n_results=top_k,
                include=["metadatas", "distances"],
            )
        except Exception as exc:
            raise ConnectionError(f"Failed to search ChromaDB: {exc}") from exc
        metadatas = results.get("metadatas", [[]])
        distances = results.get("distances", [[]])
        scored: list[tuple[KnowledgeBlock, float]] = []
        for metadata, distance in zip(metadatas[0], distances[0], strict=False):
            block = _block_from_collection_metadata(metadata)
            score = 1.0 - float(distance)
            scored.append((block, score))
        return scored

    def save(self, work_dir: Path) -> None:
        LocalVectorStore(self._blocks, self._vectors).save(work_dir)
        try:
            client = self._get_client(work_dir)
            _reset_collection(client, self._settings.vector_collection)
            collection = client.get_or_create_collection(
                name=self._settings.vector_collection,
                metadata={"hnsw:space": "cosine"},
            )
            for batch in batched(zip(self._blocks, self._vectors, strict=False), 500):
                batch_blocks, batch_vectors = zip(*batch, strict=False)
                collection.upsert(
                    ids=[block.block_id for block in batch_blocks],
                    documents=[block.text for block in batch_blocks],
                    metadatas=[_collection_metadata(block) for block in batch_blocks],
                    embeddings=list(batch_vectors),
                )
            self._client = client
            self._collection = collection
        except Exception as exc:
            raise ConnectionError(f"Failed to connect or save to ChromaDB: {exc}") from exc

    @classmethod
    def load(cls, settings: Settings, work_dir: Path) -> "ChromaDBVectorStore":
        snapshot = LocalVectorStore.load(work_dir)
        store = cls(settings, snapshot._blocks, snapshot._vectors)
        store._client = store._get_client(work_dir)
        store._collection = store._client.get_or_create_collection(name=settings.vector_collection)
        return store

    def _get_client(self, work_dir: Path):
        if self._client is not None:
            return self._client
        try:
            module = importlib.import_module("chromadb")
        except ImportError as exc:
            raise ValueError(
                "ChromaDB vector backend requires the `chromadb` package. "
                "Install it with `pip install -e .[chromadb]`."
            ) from exc
        self._client = module.PersistentClient(path=str(chromadb_path(work_dir)))
        return self._client

    def _get_collection(self):
        if self._collection is not None:
            return self._collection
        if self._client is None:
            raise ValueError("ChromaDB collection requested before client initialization.")
        self._collection = self._client.get_or_create_collection(name=self._settings.vector_collection)
        return self._collection


class QdrantVectorStore(VectorStore):
    def __init__(
        self,
        settings: Settings,
        blocks: list[KnowledgeBlock],
        vectors: list[list[float]],
    ) -> None:
        self._settings = settings
        self._blocks = blocks
        self._vectors = vectors
        self._client = None

    def search(self, model: EmbeddingModel, query: str, top_k: int = 20) -> list[tuple[KnowledgeBlock, float]]:
        if not self._blocks:
            return []
        try:
            client = self._get_client()
            query_vector = model.encode_query(query)
            response = client.query_points(
                collection_name=self._settings.vector_collection,
                query=query_vector,
                limit=top_k,
                with_payload=True,
            )
        except Exception as exc:
            raise ConnectionError(f"Failed to search Qdrant: {exc}") from exc
        points = getattr(response, "points", response)
        scored: list[tuple[KnowledgeBlock, float]] = []
        for point in points:
            payload = getattr(point, "payload", None) or {}
            score = float(getattr(point, "score", 0.0))
            block = _block_from_collection_metadata(payload)
            scored.append((block, score))
        return scored

    def save(self, work_dir: Path) -> None:
        LocalVectorStore(self._blocks, self._vectors).save(work_dir)
        try:
            client = self._get_client()
            models = self._get_models()
            dimension = self._settings.embedding_dimensions
            if not dimension:
                dimension = len(self._vectors[0]) if self._vectors else 0
            if not dimension:
                raise ValueError("Embedding dimensions are required for Qdrant collection creation.")
                
            _reset_qdrant_collection(client, self._settings.vector_collection)
            client.create_collection(
                collection_name=self._settings.vector_collection,
                vectors_config=models.VectorParams(size=dimension, distance=models.Distance.COSINE),
            )
            for batch in batched(zip(self._blocks, self._vectors, strict=False), 500):
                points = [
                    models.PointStruct(
                        id=block.block_id,
                        vector=vector,
                        payload=_collection_metadata(block),
                    )
                    for block, vector in batch
                ]
                client.upsert(
                    collection_name=self._settings.vector_collection,
                    points=points,
                )
        except Exception as exc:
            if isinstance(exc, ValueError) and "Embedding dimensions" in str(exc):
                raise
            raise ConnectionError(f"Failed to connect or save to Qdrant: {exc}") from exc

    @classmethod
    def load(cls, settings: Settings, work_dir: Path) -> "QdrantVectorStore":
        snapshot = LocalVectorStore.load(work_dir)
        return cls(settings, snapshot._blocks, snapshot._vectors)

    def _get_client(self):
        if self._client is not None:
            return self._client
        try:
            module = importlib.import_module("qdrant_client")
        except ImportError as exc:
            raise ValueError(
                "Qdrant vector backend requires the `qdrant-client` package. "
                "Install it with `pip install -e .[qdrant]`."
            ) from exc
        self._client = module.QdrantClient(
            url=self._settings.qdrant_url,
            api_key=self._settings.qdrant_api_key,
        )
        return self._client

    @staticmethod
    def _get_models():
        try:
            return importlib.import_module("qdrant_client.models")
        except ImportError as exc:
            raise ValueError(
                "Qdrant vector backend requires qdrant client models. "
                "Install it with `pip install -e .[qdrant]`."
            ) from exc


def build_vector_store(
    settings: Settings,
    blocks: list[KnowledgeBlock],
    vectors: list[list[float]],
) -> VectorStore:
    backend = settings.vector_backend.strip().lower()
    if backend == "local":
        return LocalVectorStore(blocks, vectors)
    if backend == "chromadb":
        return ChromaDBVectorStore(settings, blocks, vectors)
    if backend == "qdrant":
        return QdrantVectorStore(settings, blocks, vectors)
    raise ValueError(f"Unsupported vector backend: {settings.vector_backend}")


def load_vector_store(settings: Settings, work_dir: Path) -> VectorStore:
    backend = settings.vector_backend.strip().lower()
    if backend == "local":
        return LocalVectorStore.load(work_dir)
    if backend == "chromadb":
        return ChromaDBVectorStore.load(settings, work_dir)
    if backend == "qdrant":
        return QdrantVectorStore.load(settings, work_dir)
    raise ValueError(f"Unsupported vector backend: {settings.vector_backend}")


def vector_store_snapshot_path(work_dir: Path) -> Path:
    return work_dir / "vectors.json"


def chromadb_path(work_dir: Path) -> Path:
    return work_dir / "chromadb"


def _collection_metadata(block: KnowledgeBlock) -> dict[str, str]:
    return {
        "block_id": block.block_id,
        "document_id": block.document_id,
        "block_payload": json.dumps(asdict(block), sort_keys=True),
    }


def _block_from_collection_metadata(metadata: dict[str, object]) -> KnowledgeBlock:
    payload = metadata.get("block_payload")
    if not isinstance(payload, str):
        raise ValueError("Missing block_payload in vector collection metadata.")
    return KnowledgeBlock(**json.loads(payload))


def _reset_collection(client, collection_name: str) -> None:
    try:
        client.delete_collection(name=collection_name)
    except Exception:
        pass


def _reset_qdrant_collection(client, collection_name: str) -> None:
    try:
        client.delete_collection(collection_name=collection_name)
    except Exception:
        pass


# Backwards-compatible alias for existing code/tests.
VectorIndex = LocalVectorStore
