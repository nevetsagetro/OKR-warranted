import pytest

from own_knowledge_rag.config import Settings
from own_knowledge_rag.models import KnowledgeBlock, SearchHit
from own_knowledge_rag.reranking import CrossEncoderReranker, build_reranker


def test_build_reranker_defaults_to_noop() -> None:
    reranker = build_reranker(Settings())

    assert reranker.rerank("question", []) == []


def test_cross_encoder_reranker_reorders_top_hits(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeCrossEncoder:
        def __init__(self, model_name: str) -> None:
            assert model_name == "cross-encoder/ms-marco-MiniLM-L-6-v2"

        def predict(self, pairs):
            assert len(pairs) == 2
            return [0.1, 2.0]

    class FakeModule:
        CrossEncoder = FakeCrossEncoder

    monkeypatch.setattr(
        "own_knowledge_rag.reranking.importlib.import_module",
        lambda name: FakeModule(),
    )

    reranker = CrossEncoderReranker(
        Settings(
            OKR_RERANKER_PROVIDER="cross_encoder",
            OKR_RERANKER_MODEL="cross-encoder/ms-marco-MiniLM-L-6-v2",
            OKR_RERANKER_TOP_N=2,
        )
    )

    first = SearchHit(
        block=KnowledgeBlock(
            block_id="a",
            document_id="a",
            title="A",
            section_path=["sender"],
                section_heading="",
            block_type="table_fact",
            text="Sender provisioning: unknown.",
            source_path="a.md",
            start_anchor="Sender provisioning",
            end_anchor="unknown.",
        ),
        score=2.0,
    )
    second = SearchHit(
        block=KnowledgeBlock(
            block_id="b",
            document_id="b",
            title="B",
            section_path=["spain", "sender"],
                section_heading="",
            block_type="table_fact",
            text="Sender provisioning: No sender registration needed.",
            source_path="b.md",
            start_anchor="Sender provisioning",
            end_anchor="No sender registration needed.",
        ),
        score=1.0,
    )

    reranked = reranker.rerank("Sender in Spain?", [first, second])

    assert reranked[0].block.block_id == "b"
