import importlib
from typing import Any

from own_knowledge_rag.config import Settings
from own_knowledge_rag.models import SearchHit


class Reranker:
    def rerank(self, question: str, hits: list[SearchHit]) -> list[SearchHit]:
        raise NotImplementedError


class NoOpReranker(Reranker):
    def rerank(self, question: str, hits: list[SearchHit]) -> list[SearchHit]:
        return hits


class CrossEncoderReranker(Reranker):
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._model: Any | None = None

    def rerank(self, question: str, hits: list[SearchHit]) -> list[SearchHit]:
        if not hits:
            return hits
        top_n = max(1, min(self._settings.reranker_top_n, len(hits)))
        head = hits[:top_n]
        tail = hits[top_n:]
        pairs = [(question, _support_text(hit)) for hit in head]
        scores = self._get_model().predict(pairs)
        rescored = [
            SearchHit(
                block=hit.block,
                score=hit.score + float(score),
                lexical_score=hit.lexical_score,
                vector_score=hit.vector_score,
            )
            for hit, score in zip(head, scores, strict=False)
        ]
        rescored.sort(key=lambda item: item.score, reverse=True)
        return rescored + tail

    def _get_model(self) -> Any:
        if self._model is not None:
            return self._model
        try:
            module = importlib.import_module("sentence_transformers")
        except ImportError as exc:
            raise ValueError(
                "Cross-encoder reranking requires sentence-transformers. "
                "Install with `pip install -e .[huggingface]`."
            ) from exc
        self._model = module.CrossEncoder(self._settings.reranker_model)
        return self._model


def build_reranker(settings: Settings) -> Reranker:
    provider = settings.reranker_provider.strip().lower()
    if provider in {"", "none", "disabled"}:
        return NoOpReranker()
    if provider in {"cross_encoder", "cross-encoder", "local"}:
        return CrossEncoderReranker(settings)
    raise ValueError(f"Unsupported reranker provider: {settings.reranker_provider}")


def _support_text(hit: SearchHit) -> str:
    return " ".join(
        [
            hit.block.title,
            " ".join(hit.block.section_path),
            hit.block.metadata.get("row_key", ""),
            hit.block.metadata.get("row_values", ""),
            hit.block.text,
        ]
    )
