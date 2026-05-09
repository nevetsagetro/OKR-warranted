import json
from dataclasses import asdict
from hashlib import sha256
from pathlib import Path
from typing import Any

from own_knowledge_rag.config import Settings
from own_knowledge_rag.models import Answer, KnowledgeBlock, SearchHit
from own_knowledge_rag.text import tokenize


def load_query_cache(work_dir: Path) -> dict[str, dict[str, Any]]:
    path = query_cache_path(work_dir)
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        return {}
    entries = payload.get("entries", {})
    return entries if isinstance(entries, dict) else {}


def save_query_cache(work_dir: Path, cache: dict[str, dict[str, Any]]) -> None:
    payload = {"entries": cache}
    query_cache_path(work_dir).write_text(json.dumps(payload, indent=2), encoding="utf-8")


def query_cache_path(work_dir: Path) -> Path:
    return work_dir / "query-cache.json"


def query_cache_key(
    *,
    question: str,
    top_k: int,
    settings: Settings,
    manifest: dict[str, Any],
) -> str:
    payload = {
        "query_cache_version": 4,
        "normalized_question": " ".join(tokenize(question)),
        "top_k": top_k,
        "parser_schema_version": manifest.get("parser_schema_version"),
        "normalizer_schema_version": manifest.get("normalizer_schema_version"),
        "mapping_provider": manifest.get("mapping_provider"),
        "mapping_model": manifest.get("mapping_model"),
        "mapping_batch_size": manifest.get("mapping_batch_size"),
        "embedding_provider": manifest.get("embedding_provider"),
        "embedding_model": manifest.get("embedding_model"),
        "embedding_device": manifest.get("embedding_device"),
        "embedding_dimensions": manifest.get("embedding_dimensions"),
        "vector_backend": manifest.get("vector_backend"),
        "vector_collection": manifest.get("vector_collection"),
        "qdrant_url": manifest.get("qdrant_url"),
        "reranker_provider": manifest.get("reranker_provider"),
        "reranker_model": manifest.get("reranker_model"),
        "reranker_top_n": manifest.get("reranker_top_n"),
        "documents_state": manifest.get("documents_state", {}),
        "generation_provider": settings.generation_provider,
        "generation_model": settings.generation_model,
        "generation_max_evidence": settings.generation_max_evidence,
        "min_answer_score": settings.min_answer_score,
        "min_answer_overlap_ratio": settings.min_answer_overlap_ratio,
        "tier0_score_threshold": settings.tier0_score_threshold,
        "tier2_score_threshold": settings.tier2_score_threshold,
    }
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=True).encode("utf-8")
    return sha256(encoded).hexdigest()


def serialize_answer(answer: Answer) -> dict[str, Any]:
    return {
        "question": answer.question,
        "answer": answer.answer,
        "confidence": answer.confidence,
        "tier": answer.tier,
        "query_intent": answer.query_intent,
        "cached": True,
        "evidence": [_serialize_hit(hit) for hit in answer.evidence],
    }


def deserialize_answer(payload: dict[str, Any]) -> Answer:
    return Answer(
        question=str(payload["question"]),
        answer=str(payload["answer"]),
        confidence=str(payload["confidence"]),
        evidence=[_deserialize_hit(item) for item in payload.get("evidence", [])],
        tier=str(payload.get("tier", "refusal")),
        query_intent=str(payload.get("query_intent", "lookup")),
        cached=bool(payload.get("cached", True)),
    )


def should_cache_answer(answer: Answer) -> bool:
    return answer.tier in {"tier1", "tier2"}


def _serialize_hit(hit: SearchHit) -> dict[str, Any]:
    return {
        "block": asdict(hit.block),
        "score": hit.score,
        "lexical_score": hit.lexical_score,
        "vector_score": hit.vector_score,
    }


def _deserialize_hit(payload: dict[str, Any]) -> SearchHit:
    return SearchHit(
        block=KnowledgeBlock(**payload["block"]),
        score=float(payload.get("score", 0.0)),
        lexical_score=float(payload.get("lexical_score", 0.0)),
        vector_score=float(payload.get("vector_score", 0.0)),
    )
