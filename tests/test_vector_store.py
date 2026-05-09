from pathlib import Path

import pytest

from own_knowledge_rag.config import Settings
from own_knowledge_rag.embeddings import EmbeddingModel
from own_knowledge_rag.models import KnowledgeBlock
from own_knowledge_rag.vector_store import build_vector_store, load_vector_store


def test_chromadb_vector_store_matches_local_search_contract(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    storage: dict[str, dict[str, object]] = {}

    class FakeCollection:
        def __init__(self, bucket: dict[str, object]) -> None:
            self._bucket = bucket

        def upsert(self, ids, documents, metadatas, embeddings) -> None:
            self._bucket["entries"] = [
                {
                    "id": entry_id,
                    "document": document,
                    "metadata": metadata,
                    "embedding": embedding,
                }
                for entry_id, document, metadata, embedding in zip(ids, documents, metadatas, embeddings, strict=False)
            ]

        def query(self, query_embeddings, n_results, include) -> dict[str, list[list[object]]]:
            query_vector = query_embeddings[0]
            entries = self._bucket.get("entries", [])
            scored = []
            for entry in entries:
                embedding = entry["embedding"]
                similarity = sum(left * right for left, right in zip(query_vector, embedding, strict=False))
                scored.append((entry["metadata"], 1.0 - similarity))
            scored.sort(key=lambda item: item[1])
            metadatas = [item[0] for item in scored[:n_results]]
            distances = [item[1] for item in scored[:n_results]]
            return {"metadatas": [metadatas], "distances": [distances]}

    class FakePersistentClient:
        def __init__(self, path: str) -> None:
            self._path = path
            storage.setdefault(path, {})

        def get_or_create_collection(self, name: str, metadata=None) -> FakeCollection:
            bucket = storage[self._path].setdefault(name, {})
            return FakeCollection(bucket)

        def delete_collection(self, name: str) -> None:
            storage[self._path].pop(name, None)

    class FakeModule:
        @staticmethod
        def PersistentClient(path: str) -> FakePersistentClient:
            return FakePersistentClient(path)

    monkeypatch.setattr(
        "own_knowledge_rag.vector_store.importlib.import_module",
        lambda name: FakeModule(),
    )

    blocks = [
        KnowledgeBlock(
            block_id="spain-1",
            document_id="spain_es",
            title="Spain (ES)",
            section_path=["Sender"],
                section_heading="",
            block_type="table_fact",
            text="Sender provisioning: No sender registration needed.",
            source_path="data/raw/spain_es.md",
            start_anchor="Sender provisioning",
            end_anchor="No sender registration needed.",
        ),
        KnowledgeBlock(
            block_id="france-1",
            document_id="france_fr",
            title="France (FR)",
            section_path=["Sender"],
                section_heading="",
            block_type="table_fact",
            text="Sender provisioning: Registration required.",
            source_path="data/raw/france_fr.md",
            start_anchor="Sender provisioning",
            end_anchor="Registration required.",
        ),
    ]
    settings = Settings(
        OKR_VECTOR_BACKEND="chromadb",
        OKR_VECTOR_COLLECTION="test-collection",
    )
    model = EmbeddingModel(Settings())
    vectors = model.encode([block.text for block in blocks])

    build_vector_store(settings, blocks, vectors).save(tmp_path)
    loaded = load_vector_store(settings, tmp_path)

    hits = loaded.search(model, "Sender in Spain?", top_k=2)

    assert hits[0][0].document_id == "spain_es"


def test_qdrant_vector_store_matches_local_search_contract(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    storage: dict[str, dict[str, object]] = {}

    class FakePoint:
        def __init__(self, payload: dict[str, object], score: float) -> None:
            self.payload = payload
            self.score = score

    class FakeQueryResponse:
        def __init__(self, points: list[FakePoint]) -> None:
            self.points = points

    class FakeQdrantClient:
        def __init__(self, url: str, api_key: str | None = None) -> None:
            self._url = url
            self._api_key = api_key
            storage.setdefault(url, {})

        def delete_collection(self, collection_name: str) -> None:
            storage[self._url].pop(collection_name, None)

        def create_collection(self, collection_name: str, vectors_config) -> None:
            storage[self._url][collection_name] = {"points": [], "vectors_config": vectors_config}

        def upsert(self, collection_name: str, points) -> None:
            storage[self._url][collection_name]["points"] = points

        def query_points(self, collection_name: str, query, limit: int, with_payload: bool) -> FakeQueryResponse:
            points = storage[self._url][collection_name]["points"]
            scored: list[FakePoint] = []
            for point in points:
                vector = point.vector
                similarity = sum(left * right for left, right in zip(query, vector, strict=False))
                scored.append(FakePoint(point.payload, similarity))
            scored.sort(key=lambda item: item.score, reverse=True)
            return FakeQueryResponse(scored[:limit])

    class FakeVectorParams:
        def __init__(self, size: int, distance) -> None:
            self.size = size
            self.distance = distance

    class FakePointStruct:
        def __init__(self, id: str, vector: list[float], payload: dict[str, object]) -> None:
            self.id = id
            self.vector = vector
            self.payload = payload

    class FakeDistance:
        COSINE = "cosine"

    class FakeClientModule:
        @staticmethod
        def QdrantClient(url: str, api_key: str | None = None) -> FakeQdrantClient:
            return FakeQdrantClient(url=url, api_key=api_key)

    class FakeModelsModule:
        VectorParams = FakeVectorParams
        PointStruct = FakePointStruct
        Distance = FakeDistance

    def fake_import(name: str):
        if name == "qdrant_client":
            return FakeClientModule()
        if name == "qdrant_client.models":
            return FakeModelsModule()
        raise AssertionError(name)

    monkeypatch.setattr(
        "own_knowledge_rag.vector_store.importlib.import_module",
        fake_import,
    )

    blocks = [
        KnowledgeBlock(
            block_id="spain-1",
            document_id="spain_es",
            title="Spain (ES)",
            section_path=["Sender"],
                section_heading="",
            block_type="table_fact",
            text="Sender provisioning: No sender registration needed.",
            source_path="data/raw/spain_es.md",
            start_anchor="Sender provisioning",
            end_anchor="No sender registration needed.",
        ),
        KnowledgeBlock(
            block_id="france-1",
            document_id="france_fr",
            title="France (FR)",
            section_path=["Sender"],
                section_heading="",
            block_type="table_fact",
            text="Sender provisioning: Registration required.",
            source_path="data/raw/france_fr.md",
            start_anchor="Sender provisioning",
            end_anchor="Registration required.",
        ),
    ]
    settings = Settings(
        OKR_VECTOR_BACKEND="qdrant",
        OKR_VECTOR_COLLECTION="test-collection",
        OKR_QDRANT_URL="http://localhost:6333",
    )
    model = EmbeddingModel(Settings())
    vectors = model.encode([block.text for block in blocks])

    build_vector_store(settings, blocks, vectors).save(tmp_path)
    loaded = load_vector_store(settings, tmp_path)

    hits = loaded.search(model, "Sender in Spain?", top_k=2)

    assert hits[0][0].document_id == "spain_es"
