from types import SimpleNamespace

import pytest

from own_knowledge_rag.config import Settings
from own_knowledge_rag.generation import build_generator
from own_knowledge_rag.models import KnowledgeBlock, SearchHit


def _sample_hits() -> list[SearchHit]:
    return [
        SearchHit(
            block=KnowledgeBlock(
                block_id="spain-1",
                document_id="spain_es",
                title="Spain (ES)",
                section_path=["Sender"],
                section_heading="",
                block_type="table_fact",
                text="Sender provisioning is not required.",
                source_path="data/raw/spain_es.md",
                start_anchor="sender",
                end_anchor="sender",
                metadata={},
            ),
            score=0.7,
        ),
        SearchHit(
            block=KnowledgeBlock(
                block_id="spain-2",
                document_id="spain_es",
                title="Spain (ES)",
                section_path=["Capabilities"],
                section_heading="",
                block_type="table_fact",
                text="Two-way messaging is supported.",
                source_path="data/raw/spain_es.md",
                start_anchor="capabilities",
                end_anchor="capabilities",
                metadata={},
            ),
            score=0.62,
        ),
    ]


def test_build_generator_returns_none_when_disabled() -> None:
    settings = Settings(OKR_GENERATION_PROVIDER="none")
    assert build_generator(settings) is None


def test_local_generator_returns_grounded_citations() -> None:
    settings = Settings(
        OKR_GENERATION_PROVIDER="local",
        OKR_GENERATION_MODEL="extractive-fusion-v1",
    )
    generator = build_generator(settings)
    answer = generator.generate("Compare sender provisioning and two-way support in Spain.", _sample_hits()) if generator else None

    assert answer
    assert "Sender provisioning is not required" in answer
    assert "Two-way messaging is supported" in answer
    assert "[1]" in answer
    assert "[2]" in answer


def test_openai_generator_returns_output_text(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, object] = {}

    class FakeResponses:
        def create(self, **kwargs: object) -> object:
            captured.update(kwargs)
            return SimpleNamespace(output_text="Spain supports two-way messaging and does not require sender provisioning. [1][2]")

    class FakeClient:
        def __init__(self) -> None:
            self.responses = FakeResponses()

    class FakeModule:
        @staticmethod
        def OpenAI() -> FakeClient:
            return FakeClient()

    monkeypatch.setattr(
        "own_knowledge_rag.generation.importlib.import_module",
        lambda name: FakeModule(),
    )

    settings = Settings(
        OKR_GENERATION_PROVIDER="openai",
        OKR_GENERATION_MODEL="gpt-4.1-mini",
    )
    generator = build_generator(settings)
    answer = generator.generate("Can I use a sender in Spain?", _sample_hits()) if generator else None

    assert answer
    assert "[1][2]" in answer
    assert captured["model"] == "gpt-4.1-mini"
    assert "Question: Can I use a sender in Spain?" in captured["input"][1]["content"]
