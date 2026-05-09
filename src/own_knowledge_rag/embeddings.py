import hashlib
import importlib
from collections import Counter
from math import sqrt
from typing import Any

from own_knowledge_rag.config import Settings
from own_knowledge_rag.text import tokenize


class EmbeddingModel:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._hf_model: Any | None = None
        self._openai_client: Any | None = None

    def encode(self, texts: list[str]) -> list[list[float]]:
        if self._settings.embedding_provider == "huggingface":
            return self._encode_huggingface(texts)
        if self._settings.embedding_provider == "openai":
            return self._encode_openai(texts)
        return [self._encode_local(text) for text in texts]

    def encode_query(self, text: str) -> list[float]:
        return self.encode([text])[0]

    @staticmethod
    def _encode_local(text: str, dimensions: int = 256) -> list[float]:
        buckets = [0.0] * dimensions
        counts = Counter(tokenize(text))
        for token, count in counts.items():
            feature = f"tok:{token}"
            digest = hashlib.sha256(feature.encode("utf-8")).digest()
            index = int.from_bytes(digest[:2], "big") % dimensions
            sign = 1.0 if digest[2] % 2 == 0 else -1.0
            buckets[index] += sign * (1.0 + min(2.0, count * 0.25))
        norm = sqrt(sum(value * value for value in buckets)) or 1.0
        return [value / norm for value in buckets]

    def _encode_huggingface(self, texts: list[str]) -> list[list[float]]:
        model = self._get_hf_model()
        vectors = model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=False,
            show_progress_bar=False,
        )
        return [[float(value) for value in vector] for vector in vectors]

    def _get_hf_model(self) -> Any:
        if self._hf_model is not None:
            return self._hf_model
        try:
            module = importlib.import_module("sentence_transformers")
        except ImportError as exc:
            raise ValueError(
                "Hugging Face embeddings require sentence-transformers. "
                "Install with `pip install -e .[huggingface]`."
            ) from exc
        self._hf_model = module.SentenceTransformer(
            self._settings.embedding_model,
            device=self._settings.embedding_device,
        )
        return self._hf_model

    def _encode_openai(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        client = self._get_openai_client()
        request: dict[str, Any] = {
            "model": self._settings.embedding_model,
            "input": texts,
            "encoding_format": "float",
        }
        if self._settings.embedding_dimensions is not None:
            request["dimensions"] = self._settings.embedding_dimensions
        response = client.embeddings.create(**request)
        return [[float(value) for value in item.embedding] for item in response.data]

    def _get_openai_client(self) -> Any:
        if self._openai_client is not None:
            return self._openai_client
        try:
            module = importlib.import_module("openai")
        except ImportError as exc:
            raise ValueError(
                "OpenAI embeddings require the `openai` package. "
                "Install with `pip install -e .[openai]`."
            ) from exc
        self._openai_client = module.OpenAI()
        return self._openai_client


def cosine_similarity(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right, strict=False))
