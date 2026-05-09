import importlib
import re
from typing import Any

from own_knowledge_rag.config import Settings
from own_knowledge_rag.models import SearchHit
from own_knowledge_rag.text import tokenize


class GroundedGenerator:
    def generate(self, question: str, hits: list[SearchHit]) -> str | None:
        raise NotImplementedError


class NoOpGroundedGenerator(GroundedGenerator):
    def generate(self, question: str, hits: list[SearchHit]) -> str | None:
        return None


class OpenAIGroundedGenerator(GroundedGenerator):
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._client: Any | None = None

    def generate(self, question: str, hits: list[SearchHit]) -> str | None:
        if not hits:
            return None
        client = self._get_client()
        response = client.responses.create(
            model=self._settings.generation_model,
            input=[
                {"role": "system", "content": _generation_system_prompt()},
                {"role": "user", "content": _generation_user_prompt(question, hits)},
            ],
        )
        output_text = getattr(response, "output_text", None)
        if isinstance(output_text, str):
            cleaned = output_text.strip()
            return cleaned or None
        return _extract_response_text(response)

    def _get_client(self) -> Any:
        if self._client is not None:
            return self._client
        try:
            module = importlib.import_module("openai")
        except ImportError as exc:
            raise ValueError(
                "OpenAI Tier 2 generation requires the `openai` package. "
                "Install it with `pip install -e .[openai]`."
            ) from exc
        self._client = module.OpenAI()
        return self._client


class LocalGroundedGenerator(GroundedGenerator):
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def generate(self, question: str, hits: list[SearchHit]) -> str | None:
        if not hits:
            return None

        claims: list[tuple[str, int]] = []
        seen_claims: set[str] = set()
        for index, hit in enumerate(hits, start=1):
            claim = self._best_claim(question, hit)
            normalized_claim = self._normalize_claim_key(claim)
            if not normalized_claim or normalized_claim in seen_claims:
                continue
            claims.append((claim, index))
            seen_claims.add(normalized_claim)

        if not claims:
            return None

        top_claims = claims[: max(1, min(self._settings.generation_max_evidence, len(claims)))]
        parts = [f"{claim} [{index}]" for claim, index in top_claims]
        return " ".join(parts)

    def _best_claim(self, question: str, hit: SearchHit) -> str:
        query_terms = list(tokenize(question))
        query_term_set = set(query_terms)
        candidates = self._claim_candidates(hit.block.text)
        if not candidates:
            return ""
        
        best_text = candidates[0]
        best_score = float("-inf")
        
        for candidate in candidates:
            candidate_terms = set(tokenize(candidate))
            overlap = len(query_term_set.intersection(candidate_terms))
            score = overlap * 2.5
            
            candidate_lower = candidate.lower()
            
            for term in query_terms:
                if len(term) > 4 and term in candidate_lower:
                    score += 1.0
                    
            doc_id_clean = hit.block.document_id.replace("_", " ")[:40].lower()
            if doc_id_clean and doc_id_clean in candidate_lower:
                score += 2.0
                
            length = len(candidate)
            if 40 <= length <= 180:
                score += 1.5
            elif length > 280:
                score -= 1.5
            elif length < 20:
                score -= 2.0
                
            if candidate.endswith(":"):
                score -= 1.5
                
            if score > best_score:
                best_score = score
                best_text = candidate

        return self._clean_claim(best_text)

    @staticmethod
    def _claim_candidates(text: str) -> list[str]:
        cleaned = " ".join(text.replace("\n", " ").split())
        if not cleaned:
            return [""]
        pieces = re.split(r"(?<=[.!?])\s+|(?<=;)\s+", cleaned)
        candidates = [piece.strip(" -") for piece in pieces if piece.strip(" -")]
        return candidates or [cleaned]

    @staticmethod
    def _clean_claim(text: str) -> str:
        cleaned = text.strip()
        if cleaned.startswith("- "):
            cleaned = cleaned[2:].strip()
        cleaned = re.sub(r"\s+", " ", cleaned)
        if len(cleaned) > 280:
            cleaned = cleaned[:277].rstrip() + "..."
        return cleaned

    @staticmethod
    def _normalize_claim_key(text: str) -> str:
        return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def build_generator(settings: Settings) -> GroundedGenerator | None:
    provider = settings.generation_provider.strip().lower()
    if provider in {"", "none", "noop", "disabled"}:
        return None
    if provider == "local":
        return LocalGroundedGenerator(settings)
    if provider == "openai":
        return OpenAIGroundedGenerator(settings)
    raise ValueError(f"Unsupported generation provider: {settings.generation_provider}")


def _generation_system_prompt() -> str:
    return (
        "You answer questions only from the provided evidence blocks. "
        "All output (reasoning, answers, syntheses) MUST be in English. "
        "Synthesize across blocks when needed, but do not invent facts. "
        "Use inline citations like [1] or [1][2] for every factual claim. "
        "Return only the answer body, not a preamble."
    )


def _generation_user_prompt(question: str, hits: list[SearchHit]) -> str:
    lines = [
        f"Question: {question}",
        "",
        "Evidence blocks:",
        "",
    ]
    for index, hit in enumerate(hits, start=1):
        section = " > ".join(hit.block.section_path) if hit.block.section_path else "(root)"

        lines.extend(
            [
                f"[{index}] Document: {hit.block.document_id}",
                f"[{index}] Section: {section}",
                f"[{index}] Text: {hit.block.text}",
                f"[{index}] Enriched Context: {hit.block.enriched_text}",
                f"[{index}] Relevant Questions: {', '.join(hit.block.hypothetical_questions)}",
                f"[{index}] Answer Signal: {hit.block.answer_signal}",
                "",
            ]
        )
    lines.extend(
        [
            "Write a concise grounded answer using only this evidence.",
            "If the evidence does not fully answer the question, say what is missing.",
        ]
    )
    return "\n".join(lines)


def _extract_response_text(response: Any) -> str | None:
    outputs = getattr(response, "output", None)
    if not isinstance(outputs, list):
        return None
    parts: list[str] = []
    for item in outputs:
        if getattr(item, "type", None) != "message":
            continue
        content = getattr(item, "content", None)
        if not isinstance(content, list):
            continue
        for block in content:
            text = getattr(block, "text", None)
            if isinstance(text, str) and text.strip():
                parts.append(text.strip())
    if not parts:
        return None
    return "\n".join(parts)
