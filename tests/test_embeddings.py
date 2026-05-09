import pytest

from own_knowledge_rag.config import Settings
from own_knowledge_rag.embeddings import EmbeddingModel


def test_openai_embeddings_encode_batch(monkeypatch: pytest.MonkeyPatch) -> None:
    requests: list[dict[str, object]] = []

    class FakeEmbedding:
        def __init__(self, embedding: list[float]) -> None:
            self.embedding = embedding

    class FakeResponse:
        def __init__(self) -> None:
            self.data = [
                FakeEmbedding([0.1, 0.2, 0.3]),
                FakeEmbedding([0.4, 0.5, 0.6]),
            ]

    class FakeEmbeddings:
        def create(self, **kwargs):
            requests.append(kwargs)
            return FakeResponse()

    class FakeClient:
        def __init__(self) -> None:
            self.embeddings = FakeEmbeddings()

    class FakeModule:
        @staticmethod
        def OpenAI() -> FakeClient:
            return FakeClient()

    monkeypatch.setattr(
        "own_knowledge_rag.embeddings.importlib.import_module",
        lambda name: FakeModule(),
    )

    model = EmbeddingModel(
        Settings(
            OKR_EMBEDDING_PROVIDER="openai",
            OKR_EMBEDDING_MODEL="text-embedding-3-small",
            OKR_EMBEDDING_DIMENSIONS=3,
        )
    )

    vectors = model.encode(["hello", "world"])

    assert requests[0]["model"] == "text-embedding-3-small"
    assert requests[0]["input"] == ["hello", "world"]
    assert requests[0]["dimensions"] == 3
    assert vectors == [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
