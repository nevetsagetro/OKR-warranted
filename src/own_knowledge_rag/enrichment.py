import importlib
import json
import logging
import re
import time
from dataclasses import replace
from datetime import UTC, datetime
from difflib import get_close_matches
from hashlib import sha256
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field

from own_knowledge_rag.config import CANONICAL_TERMS, CANONICAL_TERMS_VERSION, Settings
from own_knowledge_rag.models import KnowledgeBlock, ParsedDocument

logger = logging.getLogger(__name__)

# --- Pydantic Schema for provider Structured Output ---

class EnrichmentResult(BaseModel):
    block_id: str
    reasoning: str = "" # English only
    country: str = ""
    iso_code: str = ""
    sender_types: list[str] = Field(default_factory=list) # Canonical English
    regulation_topics: list[str] = Field(default_factory=list) # Canonical English
    answer_signal: Literal["standalone_fact", "context_dependent"] = "context_dependent"
    hypothetical_questions: list[str] = Field(default_factory=list, max_length=5) # English only
    enriched_text: str = "" # English narrative of tables/JSON
    local_aliases: list[str] = Field(default_factory=list) # Original local terms (for BM25)

class BatchedEnrichmentResponse(BaseModel):
    results: list[EnrichmentResult]


# --- Fallback logic ---

def _fallback_enrichment(block: KnowledgeBlock, document: ParsedDocument) -> EnrichmentResult:
    # Rule-based fallback if provider fails
    text = block.text.lower()
    heading_text = " ".join(block.section_path).lower()
    combined = f"{heading_text} {text}"
    structured = _structured_fact_fields(block)
    
    sender_types = []
    if "alphanumeric" in combined:
        sender_types.append("alphanumeric")
    if "short code" in combined:
        sender_types.append("short_code")
    if "toll free" in combined or "toll-free" in combined:
        sender_types.append("toll_free")
    if "long code" in combined:
        sender_types.append("long_code")
    
    regulation_topics = []
    if "regist" in combined:
        regulation_topics.append("pre_registration")
    if "opt-out" in combined or "opt out" in combined:
        regulation_topics.append("opt_out")
    if "provisioning" in combined:
        regulation_topics.append("provisioning_time")
    
    enriched_text = structured.get("value", "")
    if not enriched_text and len(block.text) > 0:
        enriched_text = block.text if len(block.text) < 500 else block.text[:497] + "..."

    country = (
        structured.get("country")
        or _first_csv_value(structured.get("applies_to", ""))
        or document.country
    )
    iso_code = (
        structured.get("country_iso2")
        or structured.get("iso_code")
        or structured.get("iso2")
        or document.iso_code
    )
    hypothetical_questions = _split_question_list(structured.get("hypothetical_questions", ""))
    aliases = _structured_aliases(structured)

    return EnrichmentResult(
        block_id=block.block_id,
        reasoning="Fallback heuristic based on keywords and structured fields.",
        country=country,
        iso_code=iso_code,
        sender_types=sender_types,
        regulation_topics=regulation_topics,
        answer_signal="standalone_fact" if block.block_type in {"table_fact", "list_item", "structured_fact", "policy_rule"} else "context_dependent",
        hypothetical_questions=hypothetical_questions,
        enriched_text=enriched_text,
        local_aliases=aliases,
    )


def _structured_fact_fields(block: KnowledgeBlock) -> dict[str, str]:
    if block.block_type != "structured_fact":
        return {}
    source = block.metadata.get("row_values") or block.text
    if not source:
        return {}
    if source.lstrip().lower().startswith("value="):
        body = source
    else:
        body = source.lstrip("- ").strip()
        if ":" in body:
            body = body.split(":", 1)[1].strip()
    fields: dict[str, str] = {}
    for part in re.split(r";\s+", body):
        if "=" not in part:
            continue
        key, value = part.split("=", 1)
        key = key.strip().lower()
        value = value.strip()
        if key and value and key not in fields:
            fields[key] = value
    return fields


def _first_csv_value(value: str) -> str:
    return value.split(",", 1)[0].strip() if value else ""


def _split_question_list(value: str) -> list[str]:
    if not value:
        return []
    questions = [match.strip(" ,;") for match in re.findall(r"[^?]+\?", value)]
    if questions:
        return questions[:5]
    return [item.strip() for item in re.split(r"\s*\|\s*|\s*,\s*", value) if item.strip()][:5]


def _structured_aliases(fields: dict[str, str]) -> list[str]:
    aliases: list[str] = []
    for key in (
        "country",
        "country_iso2",
        "iso_code",
        "iso2",
        "mcc",
        "mnc",
        "dialing_code",
        "prefix",
        "operator_name",
        "fact_type",
        "topic",
    ):
        value = fields.get(key, "")
        if not value:
            continue
        aliases.extend(item.strip() for item in re.split(r"\s*,\s*", value) if item.strip())
    seen: set[str] = set()
    deduped: list[str] = []
    for alias in aliases:
        key = alias.lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(alias)
    return deduped[:20]


# --- Enricher ---

class Enricher:
    PROMPT_VERSION = "v2.2"
    CACHE_COMPAT_VERSIONS = ("v2.2", "v2.1")
    
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client = None
        self.total_blocks = 0
        self.api_calls = 0
        self.cache_hits = 0
        self.estimated_tokens = 0
        self.live_enrichment_blocks = 0
        
    def _get_client(self) -> Any:
        if self.client is not None:
            return self.client
        if self.settings.mapping_provider in {"noop", "local"}:
            return None
        if self.settings.mapping_provider == "gemini":
            try:
                import os
                module = importlib.import_module("google.genai")
                api_key = os.environ.get("GEMINI_API_KEY")
                self.client = module.Client(api_key=api_key) if api_key else module.Client()
            except Exception as e:
                logger.warning(f"Failed to init Gemini client: {e}. Enrichment will fallback to rules.")
        else:
            try:
                module = importlib.import_module("openai")
                self.client = module.OpenAI()
            except Exception as e:
                logger.warning(f"Failed to init OpenAI client: {e}. Enrichment will fallback to rules.")
        return self.client

    def _cache_path(self, work_dir: Path) -> Path:
        return work_dir / "enrichment-cache.json"

    def _load_cache(self, work_dir: Path) -> dict[str, dict[str, Any]]:
        path = self._cache_path(work_dir)
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                return {}
        return {}
        
    def _save_cache(self, work_dir: Path, cache: dict[str, dict[str, Any]]) -> None:
        path = self._cache_path(work_dir)
        path.write_text(json.dumps(cache, indent=2), encoding="utf-8")

    def _cache_key(self, block: KnowledgeBlock, prompt_version: str | None = None) -> str:
        key_content = "\0".join(
            [
                block.text,
                prompt_version or self.PROMPT_VERSION,
                self.settings.mapping_provider,
                self.settings.mapping_model,
                self.settings.mapping_prompt_mode,
                CANONICAL_TERMS_VERSION,
            ]
        )
        return sha256(key_content.encode("utf-8")).hexdigest()

    def _cache_keys(self, block: KnowledgeBlock) -> list[str]:
        seen: list[str] = []
        for version in self.CACHE_COMPAT_VERSIONS:
            key = self._cache_key(block, prompt_version=version)
            if key not in seen:
                seen.append(key)
            legacy_key = self._legacy_cache_key(block, prompt_version=version)
            if legacy_key not in seen:
                seen.append(legacy_key)
        return seen

    @staticmethod
    def _legacy_cache_key(block: KnowledgeBlock, prompt_version: str) -> str:
        key_content = f"{block.block_id}:{block.text}:{prompt_version}"
        return sha256(key_content.encode("utf-8")).hexdigest()

    def enrich_blocks(
        self, 
        document: ParsedDocument, 
        blocks: list[KnowledgeBlock], 
        work_dir: Path, 
        force_reenrich: bool = False
    ) -> list[KnowledgeBlock]:
        cache = self._load_cache(work_dir)
        started_at = time.monotonic()
        
        enriched_blocks = []
        to_enrich = []
        cache_migrated = False
        cache_hits_before = self.cache_hits
        live_blocks_before = self.live_enrichment_blocks
        
        for block in blocks:
            self.total_blocks += 1
            cache_keys = self._cache_keys(block)
            ckey = cache_keys[0]
            
            if not force_reenrich:
                cached_payload = None
                for cache_key in cache_keys:
                    if cache_key in cache:
                        cached_payload = cache[cache_key]
                        break
                if cached_payload is not None:
                    self.cache_hits += 1
                    try:
                        result = EnrichmentResult.model_validate(cached_payload)
                        if cache_key != ckey:
                            cache[ckey] = result.model_dump()
                            cache_migrated = True
                        enriched_blocks.append(self._apply_result(block, result))
                        continue
                    except Exception:
                        pass # Invalid cache entry, re-enrich
            
            to_enrich.append((block, ckey))

        total_doc_blocks = len(blocks)
        cached_doc_blocks = self.cache_hits - cache_hits_before
        live_doc_blocks = len(to_enrich)
        total_batches = (live_doc_blocks + max(1, self.settings.mapping_batch_size) - 1) // max(1, self.settings.mapping_batch_size)
        self._print_document_progress(
            document=document,
            processed_doc_blocks=cached_doc_blocks,
            total_doc_blocks=total_doc_blocks,
            cached_doc_blocks=cached_doc_blocks,
            live_doc_blocks=live_doc_blocks,
            completed_batches=0,
            total_batches=total_batches,
            status="start",
            started_at=started_at,
        )
            
        if to_enrich:
            batch_size = max(1, self.settings.mapping_batch_size)
            for i in range(0, len(to_enrich), batch_size):
                batch = to_enrich[i:i+batch_size]
                batch_blocks = [b for b, _ in batch]
                
                results = self._call_llm(document, batch_blocks)
                self.live_enrichment_blocks += len(batch_blocks)
                if self.settings.mapping_batch_delay_ms > 0 and i + batch_size < len(to_enrich):
                    time.sleep(self.settings.mapping_batch_delay_ms / 1000)
                completed_batches = (i // batch_size) + 1
                
                # Map results
                res_map = {r.block_id: r for r in results}
                if self.settings.mapping_retry_missing_results:
                    res_map.update(self._retry_missing_results(document, batch_blocks, res_map))
                
                for block, ckey in batch:
                    res = res_map.get(block.block_id)
                    if not res:
                        logger.warning(f"No result for block {block.block_id}, using fallback.")
                        res = _fallback_enrichment(block, document)
                    
                    cache[ckey] = res.model_dump()
                    enriched_blocks.append(self._apply_result(block, res))
                self._save_cache(work_dir, cache)
                self._print_document_progress(
                    document=document,
                    processed_doc_blocks=cached_doc_blocks + min((completed_batches * batch_size), live_doc_blocks),
                    total_doc_blocks=total_doc_blocks,
                    cached_doc_blocks=cached_doc_blocks,
                    live_doc_blocks=live_doc_blocks,
                    completed_batches=completed_batches,
                    total_batches=total_batches,
                    status="batch",
                    started_at=started_at,
                    batch_sent=len(batch_blocks),
                    batch_received=len(results),
                )
                    
        elif total_doc_blocks > 0:
            self._print_document_progress(
                document=document,
                processed_doc_blocks=total_doc_blocks,
                total_doc_blocks=total_doc_blocks,
                cached_doc_blocks=cached_doc_blocks,
                live_doc_blocks=live_doc_blocks,
                completed_batches=0,
                total_batches=0,
                status="complete",
                started_at=started_at,
            )
            if cache_migrated:
                self._save_cache(work_dir, cache)
            
        # Sort back to original order
        block_order = {b.block_id: idx for idx, b in enumerate(blocks)}
        enriched_blocks.sort(key=lambda b: block_order[b.block_id])

        if total_doc_blocks > 0 and to_enrich:
            self._print_document_progress(
                document=document,
                processed_doc_blocks=total_doc_blocks,
                total_doc_blocks=total_doc_blocks,
                cached_doc_blocks=self.cache_hits - cache_hits_before,
                live_doc_blocks=self.live_enrichment_blocks - live_blocks_before,
                completed_batches=total_batches,
                total_batches=total_batches,
                status="complete",
                started_at=started_at,
            )
        
        return enriched_blocks
        
    def _apply_result(self, block: KnowledgeBlock, res: EnrichmentResult) -> KnowledgeBlock:
        # Normalize tags to strict CANONICAL_TERMS
        normalized_sender = self._normalize_tags(res.sender_types)
        normalized_topics = self._normalize_tags(res.regulation_topics)
        country, iso_code = self._safe_country_identity(block, res)
        
        return replace(
            block,
            country=country,
            iso_code=iso_code,
            reasoning=res.reasoning,
            sender_types=normalized_sender,
            regulation_topics=normalized_topics,
            answer_signal=res.answer_signal,
            hypothetical_questions=res.hypothetical_questions,
            enriched_text=res.enriched_text,
            local_aliases=res.local_aliases,
            enrichment_provider=self.settings.mapping_provider,
            enrichment_model=self.settings.mapping_model,
            enriched_at=datetime.now(UTC).isoformat(),
        )

    @staticmethod
    def _safe_country_identity(block: KnowledgeBlock, res: EnrichmentResult) -> tuple[str, str]:
        country = (res.country or block.country).strip()
        iso_code = (res.iso_code or block.iso_code).strip().upper()
        if not res.country and not res.iso_code:
            return block.country, block.iso_code

        support_text = " ".join(
            [
                block.title,
                " ".join(block.section_path),
                block.document_id.replace("_", " "),
                block.metadata.get("row_values", ""),
                block.text[:400],
            ]
        ).lower()

        if iso_code and re.search(rf"\b{re.escape(iso_code.lower())}\b", support_text):
            return country, iso_code
        if country and re.search(rf"\b{re.escape(country.lower())}\b", support_text):
            return country, iso_code
        if block.metadata.get("structured_source") == "json" and country:
            row_values = block.metadata.get("row_values", "").lower()
            if country.lower() in row_values:
                return country, iso_code

        return block.country, block.iso_code

    def _normalize_tags(self, tags: list[str]) -> list[str]:
        if not tags:
            return []
        normalized = []
        for tag in tags:
            # Try exact match first
            tag_clean = tag.strip().lower()
            if tag_clean in CANONICAL_TERMS:
                normalized.append(tag_clean)
                continue
            
            # Fuzzy match
            matches = get_close_matches(tag_clean, CANONICAL_TERMS, n=1, cutoff=0.7)
            if matches:
                normalized.append(matches[0])
            # If no match, we drop it (as per "strict CANONICAL_TERMS list" requirement)
        
        return sorted(list(set(normalized)))

    def _call_llm(self, document: ParsedDocument, blocks: list[KnowledgeBlock]) -> list[EnrichmentResult]:
        if self.settings.mapping_provider in {"noop", "local"}:
            return [_fallback_enrichment(b, document) for b in blocks]
        client = self._get_client()
        if not client:
            return [_fallback_enrichment(b, document) for b in blocks]
            
        system_prompt = self._system_prompt()
        
        lines = [
            f"Document ID: {document.document_id}",
            f"Document Title: {document.title}",
            f"Document Country: {document.country}",
            "",
            "Extract structured enrichment for these blocks.",
            ""
        ]
        
        for b in blocks:
            lines.extend(self._block_prompt_lines(b))
            
        user_prompt = "\n".join(lines)
        
        self.api_calls += 1
        self.estimated_tokens += (len(system_prompt) + len(user_prompt)) // 4
        
        try:
            if self.settings.mapping_provider == "gemini":
                model_name = self.settings.mapping_model
                if not model_name.startswith("models/"):
                    model_name = f"models/{model_name}"
                    
                response = client.models.generate_content(
                    model=model_name,
                    contents=system_prompt + "\n\n" + user_prompt,
                    config={
                        "response_mime_type": "application/json",
                        "response_schema": BatchedEnrichmentResponse,
                    }
                )
                text = response.text
                if "```" in text:
                    text = re.sub(r"```(?:json)?\n?|```", "", text).strip()
                
                parsed = BatchedEnrichmentResponse.model_validate_json(text)
                if parsed:
                    return parsed.results

            else:
                response = client.beta.chat.completions.parse(
                    model=self.settings.mapping_model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    response_format=BatchedEnrichmentResponse
                )
                parsed = response.choices[0].message.parsed
                if parsed:
                    return parsed.results
        except Exception as e:
            import traceback
            logger.error(f"provider Enrichment Failed: {e}\n{traceback.format_exc()}")
            try:
                if 'response' in locals() and hasattr(response, 'text'):
                    logger.error(f"Raw Response: {response.text}")
            except Exception:
                pass
            
        return [_fallback_enrichment(b, document) for b in blocks]

    def _retry_missing_results(
        self,
        document: ParsedDocument,
        batch_blocks: list[KnowledgeBlock],
        res_map: dict[str, EnrichmentResult],
    ) -> dict[str, EnrichmentResult]:
        missing_blocks = [block for block in batch_blocks if block.block_id not in res_map]
        if not missing_blocks:
            return {}

        recovered: dict[str, EnrichmentResult] = {}
        retry_batch_size = 2 if len(missing_blocks) > 1 else 1
        for start in range(0, len(missing_blocks), retry_batch_size):
            retry_blocks = missing_blocks[start:start + retry_batch_size]
            logger.warning(
                "Retrying missing enrichment results for %s block(s): %s",
                len(retry_blocks),
                ", ".join(block.block_id for block in retry_blocks),
            )
            retry_results = self._call_llm(document, retry_blocks)
            for result in retry_results:
                recovered[result.block_id] = result
        return recovered

    def _system_prompt(self) -> str:
        allowed_tags = ", ".join(CANONICAL_TERMS)
        if self.settings.mapping_prompt_mode == "pass1":
            return (
                "You are a telecom SMS regulatory tagger building a compact English retrieval index.\n"
                "Return only valid JSON.\n"
                "Domain: SMS regulations per country.\n"
                f"Allowed sender/regulation tags only: {allowed_tags}.\n"
                "For each block:\n"
                "- Keep all output in English.\n"
                "- Write enriched_text as 1-2 concrete sentences and never leave it empty.\n"
                "- Lead with the country name and topic when possible.\n"
                "- State absences explicitly, for example: 'Country X does not support Y.'\n"
                "- Never use generic phrases like 'This block', 'This text', or 'It states'.\n"
                "- Generate 1-2 specific hypothetical_questions only when the block contains a clear retrievable claim.\n"
                "- Leave reasoning empty unless a short clarification is necessary.\n"
                "- Use answer_signal=standalone_fact only for direct retrievable claims; otherwise context_dependent.\n"
                "- Keep sender_types and regulation_topics aligned to the allowed telecom tags only."
            )
        return (
            "You are a telecommunications domain expert building an English retrieval index.\n"
            "Return JSON only.\n"
            "For each block:\n"
            "- Keep all output in English.\n"
            "- Translate local terms into functional English equivalents when useful.\n"
            f"- Use only these exact telecom tags when a sender or regulation tag applies: {allowed_tags}.\n"
            "- Generate 3-5 specific hypothetical_questions.\n"
            "- Write enriched_text as concise factual English sentences.\n"
            "- Use answer_signal=standalone_fact only when the block can answer directly; otherwise context_dependent.\n"
            "- Keep sender_types and regulation_topics aligned to telecom concepts."
        )

    def _block_prompt_lines(self, block: KnowledgeBlock) -> list[str]:
        lines = [
            f"--- BLOCK: {block.block_id} ---",
            f"Section: {' > '.join(block.section_path)}",
            f"Type: {block.block_type}",
        ]
        table_row = block.metadata.get("raw_table_row_dict")
        if table_row:
            lines.append(f"Table Row: {self._trim_prompt_value(table_row)}")
        else:
            row_key = block.metadata.get("row_key")
            row_values = block.metadata.get("row_values")
            if row_key:
                lines.append(f"Row Key: {self._trim_prompt_value(row_key)}")
            if row_values:
                lines.append(f"Row Values: {self._trim_prompt_value(row_values)}")
        lines.append(f"Text: {self._trim_prompt_value(block.text)}")
        lines.append("")
        return lines

    def _trim_prompt_value(self, value: Any) -> str:
        if isinstance(value, str):
            text = value
        else:
            text = json.dumps(value, ensure_ascii=True, separators=(",", ":"))
        compact = re.sub(r"\s+", " ", text).strip()
        limit = max(120, self.settings.mapping_text_char_limit)
        if len(compact) <= limit:
            return compact
        return compact[: limit - 3].rstrip() + "..."

    def _print_document_progress(
        self,
        *,
        document: ParsedDocument,
        processed_doc_blocks: int,
        total_doc_blocks: int,
        cached_doc_blocks: int,
        live_doc_blocks: int,
        completed_batches: int,
        total_batches: int,
        status: str,
        started_at: float,
        batch_sent: int = 0,
        batch_received: int = 0,
    ) -> None:
        label = {
            "start": "Enrichment Start",
            "batch": "Enrichment Progress",
            "complete": "Enrichment Complete",
        }.get(status, "Enrichment Progress")
        progress = f"{processed_doc_blocks}/{total_doc_blocks}"
        batch_progress = f"{completed_batches}/{total_batches}" if total_batches else "0/0"
        elapsed_seconds = max(0.0, time.monotonic() - started_at)
        eta_seconds = self._estimate_eta_seconds(processed_doc_blocks, total_doc_blocks, elapsed_seconds)
        remaining_blocks = max(0, total_doc_blocks - processed_doc_blocks)
        percent_complete = round((processed_doc_blocks / max(1, total_doc_blocks)) * 100, 1)
        global_processed_blocks = self.cache_hits + self.live_enrichment_blocks
        global_cached_rate = round((self.cache_hits / max(1, global_processed_blocks)) * 100, 1)
        parts = [
            label,
            f"doc={document.document_id}",
            f"blocks={progress}",
            f"remaining_blocks={remaining_blocks}",
            f"percent_complete={percent_complete}%",
            f"batches={batch_progress}",
            f"elapsed={self._format_duration(elapsed_seconds)}",
            f"eta={self._format_duration(eta_seconds)}",
            f"cached={cached_doc_blocks}",
            f"live={live_doc_blocks}",
            f"api_calls={self.api_calls}",
            f"cache_hits_total={self.cache_hits}",
            f"global_cached_rate={global_cached_rate}%",
        ]
        if status == "batch":
            parts.append(f"batch_sent={batch_sent}")
            parts.append(f"batch_received={batch_received}")
        print(" | ".join(parts))

    @staticmethod
    def _estimate_eta_seconds(processed: int, total: int, elapsed_seconds: float) -> float | None:
        if processed <= 0 or total <= processed:
            return 0.0 if total <= processed and total > 0 else None
        rate = elapsed_seconds / processed
        remaining = total - processed
        return max(0.0, rate * remaining)

    @staticmethod
    def _format_duration(seconds: float | None) -> str:
        if seconds is None:
            return "?"
        rounded = int(round(seconds))
        minutes, secs = divmod(rounded, 60)
        hours, minutes = divmod(minutes, 60)
        if hours:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        return f"{minutes:02d}:{secs:02d}"

    def validate_blocks(self, blocks: list[KnowledgeBlock]) -> list[KnowledgeBlock]:
        validated = []
        for b in blocks:
            # Check what tags are present
            structured_fields = _structured_fact_fields(b)
            has_structured_signal = b.block_type == "structured_fact" and bool(
                structured_fields.get("value")
                or structured_fields.get("country")
                or structured_fields.get("country_iso2")
                or structured_fields.get("iso_code")
                or structured_fields.get("iso2")
                or structured_fields.get("mcc")
                or structured_fields.get("dialing_code")
                or structured_fields.get("operator_name")
                or b.metadata.get("structured_value")
                or b.metadata.get("informative") == "high"
            )
            has_any_tag = bool(
                b.country
                or b.iso_code
                or b.sender_types
                or b.regulation_topics
                or b.hypothetical_questions
                or b.local_aliases
                or has_structured_signal
            )
            
            # Identify generic enriched text
            is_generic = False
            if b.enriched_text:
                lowered_text = b.enriched_text.lower()
                generic_phrases = ["this block", "this text", "this section", "it explains", "it states", "it contains"]
                if any(phrase in lowered_text for phrase in generic_phrases):
                    is_generic = True
            
            status = b.quality_status
            
            # Calibration Logic
            if has_structured_signal and not is_generic:
                status = "ok"
            elif not has_any_tag and not b.enriched_text:
                status = "REJECTED"
            elif (b.enriched_text and not has_any_tag) or (has_any_tag and is_generic):
                status = "LOW_QUALITY"
            else:
                if status not in ("LOW_QUALITY", "REJECTED"):
                    status = "ok"

            metadata = dict(b.metadata)
            drift = self._drift_assessment(b)
            if drift["drift_risk"]:
                metadata["drift_risk"] = "true"
                metadata["drift_missing_values"] = ", ".join(drift["missing_values"])
                metadata["drift_missing_ratio"] = str(drift["missing_ratio"])
            else:
                metadata.pop("drift_risk", None)
                metadata.pop("drift_missing_values", None)
                metadata.pop("drift_missing_ratio", None)

            b_val = replace(b, quality_status=status, metadata=metadata)
            validated.append(b_val)
            
        return validated

    @staticmethod
    def _drift_assessment(block: KnowledgeBlock) -> dict[str, object]:
        source_values = _drift_values(_drift_source_text(block))
        if not source_values or not block.enriched_text:
            return {"drift_risk": False, "missing_values": [], "missing_ratio": 0.0}

        enriched = block.enriched_text.casefold()
        missing = [value for value in source_values if value.casefold() not in enriched]
        missing_ratio = round(len(missing) / max(1, len(source_values)), 4)
        return {
            "drift_risk": missing_ratio > 0.2,
            "missing_values": missing,
            "missing_ratio": missing_ratio,
        }

    def log_costs(self):
        logger.info(f"Enrichment Complete | Blocks: {self.total_blocks} | Hits: {self.cache_hits} | API Calls: {self.api_calls} | Est. Tokens: {self.estimated_tokens}")


def _drift_values(text: str) -> list[str]:
    values: list[str] = []
    values.extend(re.findall(r"\b[A-Z]{2}\b", text))
    values.extend(re.findall(r"(?<!\w)\+?\d[\d:./-]*(?:\s?(?:AM|PM|am|pm))?(?!\w)", text))
    values.extend(
        match.strip()
        for match in re.findall(r"\b[A-Z][a-z]+(?:[ -][A-Z][a-z]+){0,3}\b", text)
        if match.lower() not in {"value", "description", "sender", "sms", "mms", "rcs"}
    )

    deduped: list[str] = []
    seen: set[str] = set()
    for value in values:
        normalized = value.strip(" .,:;()[]{}")
        if len(normalized) < 2:
            continue
        key = normalized.casefold()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(normalized)
    return deduped[:30]


def _drift_source_text(block: KnowledgeBlock) -> str:
    if block.block_type != "structured_fact":
        return block.text
    structured_value = str(block.metadata.get("structured_value") or "").strip()
    if structured_value and not _is_placeholder_drift_value(structured_value):
        return structured_value
    value_from_text = _extract_structured_value(block.text)
    if value_from_text and not _is_placeholder_drift_value(value_from_text):
        return value_from_text
    row_values = str(block.metadata.get("row_values") or "").strip()
    value_from_row = _extract_structured_value(row_values)
    if value_from_row and not _is_placeholder_drift_value(value_from_row):
        return value_from_row
    return _strip_metadata_only_fields(block.text)


def _extract_structured_value(text: str) -> str:
    match = re.search(r"(?:^|[;:\-\s])Value\s*=\s*([^;]+)", text, flags=re.IGNORECASE)
    return match.group(1).strip() if match else ""


def _strip_metadata_only_fields(text: str) -> str:
    pieces = []
    for part in text.split(";"):
        key = part.split("=", 1)[0].strip().casefold() if "=" in part else ""
        if key in {
            "country_iso2",
            "iso_code",
            "iso2",
            "topic",
            "regulation_topics",
            "structured_field",
            "source_anchor",
            "block_id",
            "hypothetical_questions",
            "description",
        }:
            continue
        pieces.append(part)
    return "; ".join(pieces)


def _is_placeholder_drift_value(value: str) -> bool:
    return value.strip().casefold() in {"", "-", "--", "---", "n/a", "na", "none", "null", "unknown"}
