import re
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

from own_knowledge_rag.embeddings import EmbeddingModel
from own_knowledge_rag.filename_metadata import build_country_index
from own_knowledge_rag.lexical import BM25Index
from own_knowledge_rag.models import KnowledgeBlock, SearchHit
from own_knowledge_rag.query_intent import analyze_query
from own_knowledge_rag.query_router import QueryFilters, extract_query_filters
from own_knowledge_rag.reranking import Reranker
from own_knowledge_rag.text import tokenize
from own_knowledge_rag.vector_store import VectorIndex

LOW_SIGNAL_QUERY_TERMS = {
    "are",
    "can",
    "countries",
    "country",
    "count",
    "days",
    "does",
    "file",
    "files",
    "how",
    "hours",
    "is",
    "json",
    "list",
    "locales",
    "many",
    "markets",
    "months",
    "must",
    "number",
    "required",
    "should",
    "supported",
    "take",
    "what",
    "when",
    "where",
    "weeks",
    "which",
}

STRUCTURED_FACT_QUERY_PHRASES = {
    "calling code",
    "country code",
    "dialing code",
    "dialling code",
    "iso code",
    "mobile country code",
    "phone code",
}

STRUCTURED_FACT_QUERY_TERMS = {
    "dialing",
    "dialling",
    "iso",
    "iso2",
    "mcc",
    "mnc",
    "prefix",
}


class HybridRetriever:
    def __init__(
        self,
        lexical_index: BM25Index,
        vector_index: VectorIndex,
        embedding_model: EmbeddingModel,
        reranker: Reranker | None = None,
        all_blocks: list[KnowledgeBlock] | None = None,
        country_index: dict[str, str] | None = None,
        rrf_lexical_weight: float = 1.0,
        rrf_vector_weight: float = 1.0,
        arm_k_multiplier: int = 3,
        max_blocks_per_document: int = 2,
    ) -> None:
        self._lexical_index = lexical_index
        self._vector_index = vector_index
        self._embedding_model = embedding_model
        self._reranker = reranker
        # All blocks stored for pre-filtering; fall back to empty list if not provided
        self._all_blocks: list[KnowledgeBlock] = (
            all_blocks if all_blocks is not None else list(getattr(lexical_index, "_blocks", []))
        )
        # Lowercase name/ISO → uppercase ISO code for geo pre-filtering
        self._country_index: dict[str, str] = country_index or build_country_index()
        self._rrf_lexical_weight = max(0.0, rrf_lexical_weight)
        self._rrf_vector_weight = max(0.0, rrf_vector_weight)
        self._arm_k_multiplier = max(1, arm_k_multiplier)
        self._max_blocks_per_document = max(1, max_blocks_per_document)

    def search(self, question: str, top_k: int = 5) -> list[SearchHit]:
        intent = analyze_query(question)

        # ── Step 1: extract structured filters from the query (heuristic, no provider)
        filters = extract_query_filters(question, self._country_index)

        # ── Step 2: build candidate block ID set from tag-based pre-filter
        candidate_ids = self._build_candidate_ids(filters)

        # ── Step 3: run BM25 + vector search in parallel on the candidate set
        #    Multiplier reduced from 5x to 3x because the pre-filter already
        #    eliminates irrelevant blocks.
        arm_k = (
            max(top_k * max(self._arm_k_multiplier, 8), 80)
            if intent.is_aggregate
            else max(top_k * self._arm_k_multiplier, 40)
        )

        def _lex() -> list[tuple[KnowledgeBlock, float]]:
            return self._lexical_index.search(question, top_k=arm_k, candidate_ids=candidate_ids)

        def _vec() -> list[tuple[KnowledgeBlock, float]]:
            return self._vector_index.search(
                self._embedding_model, question, top_k=arm_k, candidate_ids=candidate_ids
            )

        with ThreadPoolExecutor(max_workers=2) as pool:
            lex_future = pool.submit(_lex)
            vec_future = pool.submit(_vec)
            lexical_hits = lex_future.result()
            vector_hits = vec_future.result()

        # ── Step 4: merge, heuristic rerank, optional cross-encoder rerank
        fused = self._rrf_merge(lexical_hits, vector_hits)
        fused = self._inject_target_row_candidates(question, fused, filters, candidate_ids)
        heuristic_reranked = self._rerank(question, fused, filters, aggregate=intent.is_aggregate)
        if not intent.is_aggregate:
            heuristic_reranked = self._enforce_geo_results(filters, heuristic_reranked)
        if self._reranker is not None:
            heuristic_reranked = self._reranker.rerank(question, heuristic_reranked)
        final_k = max(top_k, 20) if intent.is_aggregate else top_k
        heuristic_reranked = self._enforce_document_diversity(heuristic_reranked)
        if intent.is_aggregate:
            heuristic_reranked = self._enforce_aggregate_country_diversity(
                heuristic_reranked,
                limit=final_k,
            )
        return heuristic_reranked[:final_k]

    def _enforce_document_diversity(self, hits: list[SearchHit]) -> list[SearchHit]:
        selected: list[SearchHit] = []
        overflow: list[SearchHit] = []
        document_counts: dict[str, int] = {}

        for hit in hits:
            doc_id = hit.block.document_id
            count = document_counts.get(doc_id, 0)
            if count < self._max_blocks_per_document:
                selected.append(hit)
                document_counts[doc_id] = count + 1
            else:
                overflow.append(hit)
        selected.extend(overflow)
        return selected

    def _build_candidate_ids(self, filters: QueryFilters) -> set[str] | None:
        """Return a set of block IDs that pass the tag pre-filter.

        Returns None when no filters are active (= full-corpus search).
        """
        if not filters.has_filters:
            return None

        candidate_ids: set[str] = set()
        for block in self._all_blocks:
            meta = block.metadata

            # Geographic filter
            if filters.iso_codes:
                block_iso = self._block_iso(block)
                if block_iso and block_iso not in filters.iso_codes:
                    continue

            # Sender type filter (optional — only applied when query explicitly
            # asks about a sender type AND the block has a sender tag)
            if filters.sender_types:
                block_sender = meta.get("tag_sender_type", "")
                # Only exclude if the block has a sender tag that doesn't match.
                # Blocks without a sender tag are still included (they may be
                # general-purpose locale overview blocks).
                if block_sender and block_sender not in filters.sender_types:
                    continue

            candidate_ids.add(block.block_id)

        # Country filter: for country-explicit queries we keep the narrow candidate set.
        # For weaker non-geographic filters, fall back if the set is too small.
        if len(candidate_ids) < 5 and not filters.iso_codes:
            return None

        return candidate_ids

    def _enforce_geo_results(self, filters: QueryFilters, hits: list[SearchHit]) -> list[SearchHit]:
        if not filters.iso_codes:
            return hits
        matching_hits = [
            hit for hit in hits
            if self._block_iso(hit.block) in filters.iso_codes
        ]
        return matching_hits

    def _enforce_aggregate_country_diversity(
        self,
        hits: list[SearchHit],
        *,
        limit: int,
    ) -> list[SearchHit]:
        """Prefer broad country coverage for list-style questions.

        Aggregate questions need breadth first: one strong fact from Spain,
        India, Brazil, etc. is more useful than ten near-duplicate Spain rows.
        After the first pass, we fill any remaining slots with next-best hits.
        """
        selected: list[SearchHit] = []
        remaining: list[SearchHit] = []
        seen_countries: set[str] = set()

        for hit in hits:
            country_key = self._aggregate_country_key(hit.block)
            if country_key and country_key not in seen_countries:
                selected.append(hit)
                seen_countries.add(country_key)
                continue
            remaining.append(hit)
            if len(selected) >= limit:
                break

        if len(selected) < limit:
            selected.extend(remaining[: limit - len(selected)])
        return selected

    def _aggregate_country_key(self, block: KnowledgeBlock) -> str:
        block_iso = self._block_iso(block)
        if block_iso:
            return block_iso

        metadata = block.metadata
        row_values = metadata.get("row_values", "")
        for pattern in (
            r"(?:^|;\s*)country=([^;]+)",
            r"(?:^|;\s*)country_name=([^;]+)",
            r"(?:^|;\s*)name=([^;]+)",
        ):
            match = re.search(pattern, row_values, flags=re.IGNORECASE)
            if match:
                return match.group(1).strip().lower()

        if block.country:
            return block.country.strip().lower()
        title = block.title.strip().lower()
        if title:
            return title
        return block.document_id.strip().lower()

    def _rrf_merge(
        self,
        lexical_hits: list[tuple[KnowledgeBlock, float]],
        vector_hits: list[tuple[KnowledgeBlock, float]],
        k: int = 60,
    ) -> list[SearchHit]:
        aggregate: dict[str, SearchHit] = {}
        fused_scores: defaultdict[str, float] = defaultdict(float)

        for rank, (block, score) in enumerate(lexical_hits, start=1):
            fused_scores[block.block_id] += self._rrf_lexical_weight * (1.0 / (k + rank))
            aggregate.setdefault(
                block.block_id,
                SearchHit(block=block, score=0.0, lexical_score=score, vector_score=0.0),
            ).lexical_score = score

        for rank, (block, score) in enumerate(vector_hits, start=1):
            fused_scores[block.block_id] += self._rrf_vector_weight * (1.0 / (k + rank))
            aggregate.setdefault(
                block.block_id,
                SearchHit(block=block, score=0.0, lexical_score=0.0, vector_score=score),
            ).vector_score = score

        results: list[SearchHit] = []
        for block_id, hit in aggregate.items():
            results.append(
                SearchHit(
                    block=hit.block,
                    score=fused_scores[block_id],
                    lexical_score=hit.lexical_score,
                    vector_score=hit.vector_score,
                )
            )
        return results

    def _inject_target_row_candidates(
        self,
        question: str,
        hits: list[SearchHit],
        filters: QueryFilters,
        candidate_ids: set[str] | None,
    ) -> list[SearchHit]:
        target_rows = self._target_row_keys(question)
        if not target_rows:
            return hits
        seen = {hit.block.block_id for hit in hits}
        injected: list[SearchHit] = []
        lowered_question = question.lower()
        for block in self._all_blocks:
            if block.block_id in seen:
                continue
            if candidate_ids is not None and block.block_id not in candidate_ids:
                continue
            if filters.iso_codes and self._block_iso(block) not in filters.iso_codes:
                continue
            row_key = block.metadata.get("row_key", "").strip().lower()
            if row_key not in target_rows:
                continue
            if self._row_requires_sender_focus(row_key) and not self._section_matches_sender_focus(lowered_question, block):
                continue
            injected.append(SearchHit(block=block, score=0.001, lexical_score=0.0, vector_score=0.0))
            seen.add(block.block_id)
            if len(injected) >= 12:
                break
        return [*hits, *injected]

    @staticmethod
    def _row_requires_sender_focus(row_key: str) -> bool:
        return any(
            term in row_key
            for term in {
                "twilio supported",
                "operator network capability",
                "sender id preserved",
                "provisioning time",
                "sender provisioning",
            }
        )

    @staticmethod
    def _section_matches_sender_focus(question: str, block: KnowledgeBlock) -> bool:
        section = " > ".join(block.section_path).lower()
        row_context = " ".join(
            [
                section,
                block.text,
                block.metadata.get("row_values", ""),
            ]
        ).lower()
        if "alphanumeric" in question or "alpha sender" in question:
            return "alphanumeric" in row_context or "alpha" in row_context
        if "short code" in question or "short codes" in question:
            return "short code" in row_context or "short codes" in row_context
        if "long code" in question or "long codes" in question:
            return "long code" in row_context or "long codes" in row_context
        if "toll free" in question or "toll-free" in question:
            return "toll free" in row_context or "toll-free" in row_context or "tfn" in row_context
        return True

    def _rerank(
        self,
        question: str,
        hits: list[SearchHit],
        filters: QueryFilters,
        *,
        aggregate: bool = False,
    ) -> list[SearchHit]:
        query_tokens = tokenize(question)
        query_terms = set(query_tokens)
        reranked: list[SearchHit] = []

        # Track document counts to apply diversity penalty
        doc_counts: dict[str, int] = {}

        for hit in hits:
            support_text = self._support_text(hit)
            support_tokens = tokenize(support_text)
            block_terms = set(tokenize(hit.block.text))
            doc_terms = set(tokenize(f"{hit.block.document_id} {hit.block.title}"))
            section_terms = set(tokenize(" ".join(hit.block.section_path)))
            row_key_terms = set(tokenize(hit.block.metadata.get("row_key", "")))
            row_value_terms = set(tokenize(hit.block.metadata.get("row_values", "")))
            entity_terms = set(tokenize(hit.block.metadata.get("tag_entity", "")))
            
            overlap = len(query_terms.intersection(block_terms))
            doc_overlap = len(query_terms.intersection(doc_terms))
            section_overlap = len(query_terms.intersection(section_terms))
            row_key_overlap = len(query_terms.intersection(row_key_terms))
            row_value_overlap = len(query_terms.intersection(row_value_terms))
            entity_overlap = len(query_terms.intersection(entity_terms))
            
            specificity_bonus = (
                0.12 * doc_overlap
                + 0.14 * section_overlap
                + 0.14 * row_key_overlap
                + 0.03 * row_value_overlap
                + 0.15 * entity_overlap
                + 0.04 * overlap
            )
            block_type_bonus = 0.08 if hit.block.block_type in {"table_fact", "structured_fact", "policy_rule", "faq"} else 0.0
            metadata_bonus = self._metadata_bonus(hit)
            target_row_bonus = self._target_row_bonus(question, hit)
            table_extraction_bonus = self._table_extraction_bonus(question, hit)
            structured_fact_bonus = self._structured_fact_bonus(question, query_terms, hit)
            aggregate_bonus = self._aggregate_topic_bonus(question, query_terms, hit) if aggregate else 0.0
            alignment_bonus = self._question_alignment_bonus(
                question=question,
                query_tokens=query_tokens,
                support_text=support_text,
                support_tokens=support_tokens,
                hit=hit,
            )
            geo_bonus = self._geo_bonus(hit, filters)
            generic_penalty = self._generic_row_penalty(question, hit)
            sender_focus_penalty = self._sender_focus_penalty(question, hit)
            
            # Richness bonus: favor blocks with more detail (up to 0.1)
            richness_bonus = min(0.1, len(hit.block.text.split()) * 0.005)
            
            final_score = (
                hit.score 
                + specificity_bonus 
                + block_type_bonus 
                + metadata_bonus 
                + target_row_bonus
                + table_extraction_bonus
                + structured_fact_bonus
                + aggregate_bonus
                + alignment_bonus
                + geo_bonus
                + richness_bonus
                - generic_penalty
                - sender_focus_penalty
            )
            
            # Apply diversity penalty if document already well-represented in the stream
            # This ensures Spain__2014 isn't pushed out by 10 blocks from spain_es.
            doc_id = hit.block.document_id
            count = doc_counts.get(doc_id, 0)
            if count > 0:
                final_score -= 0.04 * count
            doc_counts[doc_id] = count + 1

            reranked.append(
                SearchHit(
                    block=hit.block,
                    score=max(0.0, final_score),
                    lexical_score=hit.lexical_score,
                    vector_score=hit.vector_score,
                )
            )

        reranked.sort(key=lambda item: item.score, reverse=True)
        return reranked

    def _geo_bonus(self, hit: SearchHit, filters: QueryFilters) -> float:
        if not filters.iso_codes:
            return 0.0
        block_iso = self._block_iso(hit.block)
        if block_iso in filters.iso_codes:
            return 0.45
        if block_iso:
            return -1.5
        return -0.18

    @staticmethod
    def _generic_row_penalty(question: str, hit: SearchHit) -> float:
        lowered_question = question.lower()
        row_key = hit.block.metadata.get("row_key", "").strip().lower()
        section = " > ".join(hit.block.section_path).strip().lower()
        text = hit.block.text.strip().lower()

        if any(term in lowered_question for term in {"sender", "registration", "two-way", "portability", "dialing code"}):
            if row_key in {"locale name", "locale summary"}:
                return 0.35
            if "locale summary" in section and row_key not in {"dialing code", "two-way sms supported", "number portability available"}:
                return 0.12

        if row_key in {"locale name"} and (text.endswith(": yes.") or text.endswith(": no.")):
            return 0.14

        if row_key in {"locale name"} and any(term in lowered_question for term in {"supported", "required", "registration"}):
            return 0.28

        return 0.0

    @classmethod
    def _sender_focus_penalty(cls, question: str, hit: SearchHit) -> float:
        row_key = hit.block.metadata.get("row_key", "").strip().lower()
        if not cls._row_requires_sender_focus(row_key):
            return 0.0
        if cls._section_matches_sender_focus(question.lower(), hit.block):
            return 0.0
        return 2.5

    def _block_iso(self, block: KnowledgeBlock) -> str:
        document_iso = re.search(r"_([a-z]{2})$", block.document_id.lower())
        title_isos = re.findall(r"\(([A-Za-z]{2})\)", block.title)
        if title_isos:
            title_iso = title_isos[-1].upper()
            if document_iso and title_iso != document_iso.group(1).upper():
                return document_iso.group(1).upper()
            return title_iso
        if document_iso:
            return document_iso.group(1).upper()
        title_key = block.title.strip().lower()
        country = block.country.strip().lower()
        title_index_iso = self._country_index.get(title_key, "")
        if title_index_iso:
            return title_index_iso
        stale_profile_country = bool(title_key and country and title_key != country)
        block_iso = (block.iso_code or block.metadata.get("tag_iso_code", "")).strip().upper()
        if block_iso and not stale_profile_country:
            return block_iso
        row_values = block.metadata.get("row_values", "")
        for pattern in (
            r"(?:^|;\s*)country_iso2=([A-Za-z]{2})(?:;|$)",
            r"(?:^|;\s*)iso2=([A-Za-z]{2})(?:;|$)",
            r"(?:^|;\s*)iso_code=([A-Za-z]{2})(?:;|$)",
        ):
            match = re.search(pattern, row_values)
            if match:
                return match.group(1).upper()
        country_match = re.search(r"(?:^|;\s*)country_name=([^;]+)", row_values)
        if country_match:
            indexed = self._country_index.get(country_match.group(1).strip().lower(), "")
            if indexed:
                return indexed
        support_iso = re.search(
            r"\(([A-Za-z]{2})\)",
            " ".join([block.metadata.get("row_key", ""), block.text[:120]]),
        )
        if support_iso:
            return support_iso.group(1).upper()
        if stale_profile_country:
            return ""
        if country and (not title_key or title_key == country):
            return self._country_index.get(country, "")
        return ""

    @staticmethod
    def _metadata_bonus(hit: SearchHit) -> float:
        metadata = hit.block.metadata
        bonus = 0.0
        if metadata.get("document_kind") == "catalog":
            bonus -= 0.18
        scope = metadata.get("document_scope")
        if scope == "aggregate":
            bonus -= 0.06
        if scope == "profile":
            bonus += 0.15
        if metadata.get("informative") == "low":
            bonus -= 0.14
        if metadata.get("informative") == "high":
            bonus += 0.05
        try:
            confidence = float(metadata.get("semantic_map_confidence", "0.0"))
        except ValueError:
            confidence = 0.0
        bonus += max(0.0, confidence - 0.5) * 0.12
        if metadata.get("semantic_map_status") in {"mapped", "cached", "heuristic"}:
            bonus += 0.02
        return bonus

    @staticmethod
    def _target_row_bonus(question: str, hit: SearchHit) -> float:
        target_rows = HybridRetriever._target_row_keys(question)
        if not target_rows:
            return 0.0
        row_key = hit.block.metadata.get("row_key", "").strip().lower()
        if row_key in target_rows:
            return 2.2
        if hit.block.block_type in {"table_fact", "structured_fact", "policy_rule"}:
            return -0.35
        return 0.0

    @staticmethod
    def _table_extraction_bonus(question: str, hit: SearchHit) -> float:
        lowered = question.lower()
        row_key = hit.block.metadata.get("row_key", "").strip().lower()
        row_values = hit.block.metadata.get("row_values", "").strip().lower()
        support_text = " ".join([row_key, row_values, hit.block.text.lower()])
        bonus = 0.0

        if not any(
            term in lowered
            for term in {
                "provisioning",
                "pre-register",
                "pre register",
                "pre-registration",
                "dynamic",
                "handset",
                "delivery receipt",
                "default sender",
                "number portability",
                "two-way",
                "two way",
                "toll-free",
                "toll free",
            }
        ):
            return 0.0

        if "provisioning" in lowered and row_key == "provisioning time":
            if HybridRetriever._row_has_non_description_value(row_values):
                bonus += 0.55
            else:
                bonus -= 2.5
        if any(term in lowered for term in {"pre-register", "pre register", "pre-registration", "registration"}):
            if row_key in {"twilio supported", "operator network capability", "sender provisioning"}:
                bonus += 0.45
            if any(term in support_text for term in {"not required", "required", "pre-registration", "pre registration"}):
                bonus += 0.28
        if "dynamic" in lowered and row_key in {"twilio supported", "operator network capability", "sender id preserved"}:
            bonus += 0.45
        if any(term in lowered for term in {"handset", "delivery receipt", "delivery receipts"}):
            if any(term in row_key for term in {"handset", "delivery receipt", "delivery receipts"}):
                bonus += 0.9
        if "default sender" in lowered or "dynamic sender is not used" in lowered:
            if any(term in support_text for term in {"verify", "info", "system", "generic sender", "sender id preserved"}):
                bonus += 0.75
        if "number portability" in lowered and "number portability" in row_key:
            bonus += 0.75
        if any(term in lowered for term in {"two-way", "two way", "2-way"}) and (
            "two-way" in row_key or "two way" in row_key
        ):
            bonus += 0.45

        return bonus

    @staticmethod
    def _row_has_non_description_value(row_values: str) -> bool:
        parts = [part.strip() for part in row_values.replace(";", ",").split(",") if part.strip()]
        for part in parts:
            lowered = part.lower()
            if "description" in lowered and (" is " in lowered or "=" in lowered or ":" in lowered):
                continue
            if any(value in lowered for value in {"n/a", "---", "-----"}):
                continue
            return True
        return False

    @staticmethod
    def _target_row_keys(question: str) -> set[str]:
        lowered = question.lower()
        targets: set[str] = set()
        if "two-way" in lowered or "two way" in lowered or "2-way" in lowered:
            targets.update({"two-way sms supported", "two-way", "two-way provisioning"})
        if "number portability" in lowered:
            targets.update({"number portability available", "number portability"})
        if "dialing code" in lowered or "dialling code" in lowered or "calling code" in lowered:
            targets.add("dialing code")
        if "sender types" in lowered or "sender availability" in lowered:
            targets.add("sender availability")
        if "preserved" in lowered or "preservation" in lowered:
            targets.add("sender id preserved")
        if any(term in lowered for term in {"default sender", "dynamic sender is not used"}):
            targets.update({"sender id preserved", "twilio supported", "operator network capability"})
        if any(term in lowered for term in {"pre-register", "pre register", "pre-registration", "registration"}):
            targets.update({"twilio supported", "operator network capability", "sender provisioning"})
        if "dynamic" in lowered:
            targets.update({"twilio supported", "operator network capability", "sender id preserved"})
        if "provisioning time" in lowered or "how long" in lowered:
            targets.update({"provisioning time", "sender provisioning", "service provisioning"})
        if "cost" in lowered and "provisioning" in lowered:
            targets.update({"twilio supported", "operator network capability", "sender provisioning"})
        if "handset" in lowered or "delivery receipt" in lowered or "delivery receipts" in lowered:
            targets.update({"handset delivery receipts", "delivery receipts", "delivery receipt support"})
        if "support" in lowered or "supported" in lowered or "supports" in lowered:
            if any(term in lowered for term in {"alphanumeric", "short code", "long code", "sender id", "sender ids"}):
                targets.add("twilio supported")
        if "compliance consideration" in lowered:
            targets.add("compliance considerations")
        if "service restriction" in lowered:
            targets.add("service restrictions")
        if "country regulation" in lowered:
            targets.add("country regulations")
        return targets

    @staticmethod
    def _structured_fact_bonus(question: str, query_terms: set[str], hit: SearchHit) -> float:
        if hit.block.block_type != "structured_fact":
            return 0.0

        lowered_question = question.lower()
        asks_for_structured_value = any(
            phrase in lowered_question for phrase in STRUCTURED_FACT_QUERY_PHRASES
        ) or bool(query_terms.intersection(STRUCTURED_FACT_QUERY_TERMS))

        metadata = hit.block.metadata
        support_terms = set(
            tokenize(
                " ".join(
                    [
                        metadata.get("row_key", ""),
                        metadata.get("row_values", ""),
                        metadata.get("structured_field", ""),
                        metadata.get("structured_value", ""),
                        hit.block.text,
                    ]
                )
            )
        )
        meaningful_query_terms = query_terms.difference(LOW_SIGNAL_QUERY_TERMS)
        exact_field_overlap = len(query_terms.intersection(support_terms))
        meaningful_overlap = len(meaningful_query_terms.intersection(support_terms))
        if not asks_for_structured_value and not meaningful_overlap:
            return 0.0

        bonus = 0.14
        if metadata.get("structured_source") == "json" or metadata.get("content_type") == "json":
            bonus += 0.18
        if asks_for_structured_value:
            bonus += 0.08
        if exact_field_overlap:
            bonus += min(0.24, exact_field_overlap * 0.08)
        if meaningful_overlap:
            bonus += min(0.24, meaningful_overlap * 0.08)
        return bonus

    @staticmethod
    def _aggregate_topic_bonus(question: str, query_terms: set[str], hit: SearchHit) -> float:
        support_text = HybridRetriever._support_text(hit).lower()
        lowered_question = question.lower()
        bonus = 0.0

        if hit.block.block_type in {"structured_fact", "table_fact", "policy_rule"}:
            bonus += 0.12

        if hit.block.metadata.get("structured_source") == "json" or hit.block.metadata.get("content_type") == "json":
            bonus += 0.12

        topic_groups = [
            (
                {"registration", "register", "pre-registration", "preregistration", "sender", "need", "needs", "needed"},
                ["registration", "register", "pre-registration", "preregistration", "mandatory", "required", "needed"],
                0.34,
            ),
            (
                {"two-way", "2-way", "twoway"},
                ["two-way", "2-way", "twoway", "mo sms", "inbound"],
                0.32,
            ),
            (
                {"support", "supported", "capability", "available"},
                ["supported", "available", "capability", "enabled"],
                0.22,
            ),
            (
                {"dialing", "dialling", "code", "prefix", "iso", "mcc", "mnc"},
                ["dialing", "dialling", "prefix", "iso", "iso2", "mcc", "mnc", "numbering"],
                0.28,
            ),
            (
                {"restriction", "restricted", "content", "prohibited", "blocked"},
                ["restriction", "restricted", "content", "prohibited", "blocked", "forbidden"],
                0.28,
            ),
        ]

        for query_markers, support_markers, value in topic_groups:
            if query_terms.intersection(query_markers) or any(marker in lowered_question for marker in query_markers):
                if any(marker in support_text for marker in support_markers):
                    bonus += value

        asks_for_required = any(
            term in lowered_question
            for term in ["need", "needs", "needed", "require", "required", "requiring", "mandatory"]
        )
        support_is_negative = any(
            phrase in support_text
            for phrase in [
                "does not require",
                "not required",
                "no registration required",
                "registration is not required",
                "not mandatory",
            ]
        )
        if asks_for_required and support_is_negative:
            bonus -= 1.1

        asks_for_support = any(
            term in lowered_question
            for term in ["available", "availability", "support", "supported", "supports"]
        )
        support_is_negative_capability = any(
            phrase in support_text
            for phrase in [
                "not supported",
                "not available",
                "no two-way",
                "two-way sms supported is: no",
                "two-way sms supported: no",
                "value=no",
                "value: no",
                "=no",
            ]
        ) or bool(re.search(r"\btwo[- ]?way\b.{0,80}\bno\b", support_text))
        if asks_for_support and support_is_negative_capability:
            bonus -= 1.1

        if any(term in lowered_question for term in ["countries with", "which countries", "what countries"]):
            if hit.block.iso_code or "country_iso2=" in support_text or "iso_code=" in support_text:
                bonus += 0.08

        return max(-1.1, min(bonus, 0.75))

    @staticmethod
    def _question_alignment_bonus(
        *,
        question: str,
        query_tokens: list[str],
        support_text: str,
        support_tokens: list[str],
        hit: SearchHit,
    ) -> float:
        lowered_question = question.lower()
        lowered_support = support_text.lower()
        bonus = 0.0
        question_profile = HybridRetriever._question_profile(lowered_question)
        support_profile = HybridRetriever._support_profile(lowered_support)
        row_key_terms = set(tokenize(hit.block.metadata.get("row_key", "")))
        query_terms = set(query_tokens)

        if question_profile["binary"]:
            if support_profile["decision"]:
                bonus += 0.22
            if support_profile["negative"] and not support_profile["requirement"]:
                bonus -= 0.06

        if question_profile["count"]:
            if support_profile["count"]:
                bonus += 0.3
            if support_profile["count_label_match"]:
                bonus += 0.16

        if question_profile["duration"]:
            if support_profile["duration"]:
                bonus += 0.28
            if support_profile["time_label"]:
                bonus += 0.12

        if question_profile["consequence"]:
            if support_profile["outcome"]:
                bonus += 0.22

        if question_profile["file_reference"] and support_profile["file_reference"]:
            bonus += 0.22

        phrase_bonus = HybridRetriever._phrase_overlap_bonus(query_tokens, support_tokens)
        bonus += phrase_bonus
        bonus += HybridRetriever._focus_coverage_bonus(query_tokens, support_tokens)
        focus_proximity_bonus = HybridRetriever._focus_proximity_bonus(question, support_text)
        bonus += focus_proximity_bonus

        if row_key_terms and not row_key_terms.intersection(query_terms) and not phrase_bonus:
            if hit.block.block_type == "table_fact":
                bonus -= 0.04

        if question_profile["binary"] and support_profile["requirement"]:
            bonus += 0.08
            if focus_proximity_bonus >= 0.24:
                bonus += 0.16
        bonus += HybridRetriever._semantic_alignment_bonus(question_profile, hit)
        return bonus

    @staticmethod
    def _support_text(hit: SearchHit) -> str:
        return " ".join(
            [
                hit.block.title,
                " ".join(hit.block.section_path),
                hit.block.metadata.get("row_key", ""),
                hit.block.metadata.get("row_values", ""),
                hit.block.metadata.get("semantic_entities", ""),
                hit.block.metadata.get("semantic_canonical_terms", ""),
                hit.block.metadata.get("semantic_synonyms", ""),
                hit.block.metadata.get("semantic_related_terms", ""),
                hit.block.metadata.get("semantic_retrieval_hints", ""),
                hit.block.metadata.get("semantic_answer_signal", ""),
                hit.block.text,
            ]
        )

    @staticmethod
    def _semantic_alignment_bonus(question_profile: dict[str, bool], hit: SearchHit) -> float:
        signal = hit.block.metadata.get("semantic_answer_signal", "")
        if not signal:
            return 0.0
        if question_profile["duration"] and signal == "duration":
            return 0.24
        if question_profile["count"] and signal == "count":
            return 0.24
        if question_profile["consequence"] and signal == "consequence":
            return 0.22
        if question_profile["binary"] and signal in {"requirement", "capability"}:
            return 0.16
        return 0.0

    @staticmethod
    def _question_profile(question: str) -> dict[str, bool]:
        return {
            "binary": question.startswith(("is ", "are ", "does ", "do ", "can ", "should ", "must ")),
            "count": "how many" in question or "count" in question or "number of" in question,
            "duration": "how long" in question or "how many weeks" in question or "how many days" in question,
            "consequence": "what happens" in question or "what occurs" in question or "what if" in question,
            "file_reference": ".json" in question or ".md" in question or "file" in question,
        }

    @staticmethod
    def _support_profile(text: str) -> dict[str, bool]:
        return {
            "decision": any(term in text for term in ["yes", "no", "supported", "available", "allowed", "required"]),
            "negative": any(term in text for term in ["not supported", "not available", "not allowed", "blocked", "forbidden", "prohibited", "no "]),
            "requirement": any(term in text for term in ["required", "mandatory", "needed", "prerequisite"]),
            "count": bool(re.search(r"\b\d+\b", text)) and any(term in text for term in ["count", "total", "number"]),
            "count_label_match": any(term in text for term in ["count", "total", "number"]),
            "duration": bool(re.search(r"\b\d+\s*(day|days|week|weeks|month|months|year|years|hour|hours)\b", text)),
            "time_label": any(term in text for term in ["time", "duration", "timeline", "period"]),
            "outcome": any(term in text for term in ["will", "overwritten", "changed", "converted", "rejected", "blocked", "preserved"]),
            "file_reference": bool(re.search(r"\.[a-z0-9]{2,5}\b", text)),
        }

    @staticmethod
    def _phrase_overlap_bonus(query_tokens: list[str], support_tokens: list[str]) -> float:
        if len(query_tokens) < 2 or len(support_tokens) < 2:
            return 0.0
        support_bigrams = {
            f"{support_tokens[index]} {support_tokens[index + 1]}"
            for index in range(len(support_tokens) - 1)
        }
        score = 0.0
        for index in range(len(query_tokens) - 1):
            phrase = f"{query_tokens[index]} {query_tokens[index + 1]}"
            if phrase in support_bigrams:
                score += 0.24
        return min(score, 0.72)

    @staticmethod
    def _focus_coverage_bonus(query_tokens: list[str], support_tokens: list[str]) -> float:
        focus_terms = [
            token for token in query_tokens
            if token not in LOW_SIGNAL_QUERY_TERMS
        ]
        if not focus_terms:
            return 0.0
        support_term_set = set(support_tokens)
        covered = sum(1 for term in focus_terms if term in support_term_set)
        coverage_ratio = covered / len(focus_terms)
        if coverage_ratio >= 0.8:
            return 0.4
        if coverage_ratio >= 0.5:
            return 0.0
        if len(focus_terms) >= 2:
            return -0.18
        return -0.06

    @staticmethod
    def _focus_proximity_bonus(question: str, support_text: str) -> float:
        question_terms = [
            token for token in HybridRetriever._rough_tokens(question)
            if token not in LOW_SIGNAL_QUERY_TERMS
        ]
        support_terms = HybridRetriever._rough_tokens(support_text)
        if len(question_terms) < 2 or len(support_terms) < 2:
            return 0.0

        positions: dict[str, list[int]] = defaultdict(list)
        for index, token in enumerate(support_terms):
            positions[token].append(index)

        score = 0.0
        for index in range(len(question_terms) - 1):
            left = question_terms[index]
            right = question_terms[index + 1]
            if left not in positions or right not in positions:
                continue
            if HybridRetriever._has_ordered_near_match(positions[left], positions[right], max_gap=2):
                score += 0.12
        return min(score, 0.36)

    @staticmethod
    def _has_ordered_near_match(left_positions: list[int], right_positions: list[int], max_gap: int) -> bool:
        for left in left_positions:
            for right in right_positions:
                if right > left and (right - left - 1) <= max_gap:
                    return True
        return False

    @staticmethod
    def _rough_tokens(text: str) -> list[str]:
        tokens: list[str] = []
        for raw in re.findall(r"[a-z0-9]+", text.lower()):
            if raw == "ids":
                tokens.append("id")
                continue
            if raw.endswith("s") and len(raw) > 3:
                raw = raw[:-1]
            tokens.append(raw)
        return tokens
