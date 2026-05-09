import re

from own_knowledge_rag.generation import GroundedGenerator
from own_knowledge_rag.models import Answer, SearchHit
from own_knowledge_rag.query_intent import analyze_query
from own_knowledge_rag.text import tokenize


class ExtractiveAnswerer:
    def __init__(
        self,
        min_score_threshold: float = 0.18,
        min_overlap_ratio: float = 0.2,
        tier0_score_threshold: float = 0.75,
        tier2_score_threshold: float = 0.55,
        generator: GroundedGenerator | None = None,
        generation_max_evidence: int = 5,
    ) -> None:
        self._min_score_threshold = min_score_threshold
        self._min_overlap_ratio = min_overlap_ratio
        self._tier0_score_threshold = tier0_score_threshold
        self._tier2_score_threshold = tier2_score_threshold
        self._generator = generator
        self._generation_max_evidence = generation_max_evidence

    def answer(self, question: str, hits: list[SearchHit]) -> Answer:
        intent = analyze_query(question)
        if not hits or self._should_refuse(question, hits):
            return Answer(
                question=question,
                answer="Insufficient evidence in the indexed knowledge base.",
                confidence="low",
                evidence=[],
                tier="refusal",
                query_intent=intent.primary,
            )

        best = self._best_informative_hit(question, hits)
        coherent_hits = self._coherent_hits(intent, hits, best)
        coherent_hits = self._prioritize_best_hit(best, coherent_hits)
        confidence = self._confidence(question, coherent_hits)
        tier = self._route_tier(intent, best, coherent_hits, confidence)
        direct = self._answer_body(question, best, coherent_hits, tier)
        evidence_limit = 10 if intent.is_aggregate else 3
        evidence_hits = self._answer_evidence_hits(question, intent, coherent_hits)
        return Answer(
            question=question,
            answer=direct,
            confidence=confidence,
            evidence=evidence_hits[:evidence_limit],
            tier=tier,
            query_intent=intent.primary,
        )

    def _answer_body(self, question: str, best: SearchHit, hits: list[SearchHit], tier: str) -> str:
        intent = analyze_query(question)
        if intent.is_aggregate:
            aggregate = self._aggregate_answer(question, hits)
            if aggregate:
                return aggregate

        if tier == "tier2" and self._generator is not None:
            generated = self._generator.generate(question, hits[: self._generation_max_evidence])
            if generated:
                return generated
        
        # Multi-source synthesis for extractive answers
        # If we have multiple hits from DIFFERENT documents with very high scores,
        # we concatenate them to ensure no "Spain" document is forgotten.
        relevant_hits = [hits[0]]
        primary_doc = hits[0].block.document_id

        for hit in hits[1:3]:
            # If hit is from a different doc but has a very similar score (within 15%)
            if hit.block.document_id != primary_doc and hit.score >= (hits[0].score * 0.85):
                # Ensure it's not a near-duplicate of the best text
                if hit.block.text[:50].lower() not in relevant_hits[0].block.text.lower():
                    relevant_hits.append(hit)
        
        if len(relevant_hits) > 1:
            parts = []
            for i, hit in enumerate(relevant_hits):
                parts.append(self._direct_answer(question, hit))
            return "\n\n---\n\n".join(parts)

        return self._direct_answer(question, best)

    def _coherent_hits(self, intent, hits: list[SearchHit], best: SearchHit) -> list[SearchHit]:
        if intent.is_aggregate:
            return self._aggregate_coherent_hits(hits)
        if intent.is_comparative:
            return hits
        primary_doc = best.block.document_id
        same_doc_hits = [hit for hit in hits if hit.block.document_id == primary_doc]
        return same_doc_hits or hits

    @staticmethod
    def _prioritize_best_hit(best: SearchHit, hits: list[SearchHit]) -> list[SearchHit]:
        if not hits:
            return hits
        return [best] + [hit for hit in hits if hit is not best]

    def _aggregate_coherent_hits(self, hits: list[SearchHit]) -> list[SearchHit]:
        selected: list[SearchHit] = []
        seen_countries: set[str] = set()

        for hit in hits:
            country_key = self._country_key(hit)
            if country_key and country_key in seen_countries:
                continue
            if country_key:
                seen_countries.add(country_key)
            selected.append(hit)
            if len(selected) >= 12:
                break

        return selected or hits

    def _answer_evidence_hits(self, question: str, intent, hits: list[SearchHit]) -> list[SearchHit]:
        if not intent.is_aggregate:
            return hits
        if self._asks_for_required(question):
            positive_hits = [hit for hit in hits if not self._is_negative_requirement(hit)]
            return positive_hits or hits
        if self._asks_for_support(question):
            positive_hits = [hit for hit in hits if self._is_positive_support(hit)]
            return positive_hits or hits
        return hits

    def _aggregate_answer(self, question: str, hits: list[SearchHit]) -> str:
        selected: list[tuple[str, str]] = []
        asks_for_required = self._asks_for_required(question)
        asks_for_support = self._asks_for_support(question)

        for hit in hits:
            if asks_for_required and self._is_negative_requirement(hit):
                continue
            if asks_for_support and not self._is_positive_support(hit):
                continue
            country = self._country_label(question, hit)
            if not country:
                continue
            detail = self._aggregate_detail(question, hit)
            if detail:
                selected.append((country, detail))
            if len(selected) >= 12:
                break

        if not selected:
            return ""

        lines = [f"- {country}: {detail}" for country, detail in selected]
        return "Countries found:\n" + "\n".join(lines)

    def _aggregate_detail(self, question: str, hit: SearchHit) -> str:
        block_text = self._trim(hit.block.enriched_text or hit.block.text)
        country = self._country_label(question, hit)
        if block_text and self._looks_like_standalone_fact(block_text):
            if country and block_text.lower().startswith(country.lower()):
                _, _, remainder = block_text.partition(" ")
                return self._trim(remainder)
            return block_text

        polished = self._polished_structured_answer(question, hit)
        if polished:
            if country and polished.lower().startswith(country.lower()):
                _, _, remainder = polished.partition(" ")
                return self._trim(remainder)
            return self._trim(polished)

        structured = self._structured_answer(hit)
        if structured:
            return self._trim(structured)
        return block_text

    def _best_informative_hit(self, question: str, hits: list[SearchHit]) -> SearchHit:
        query_terms = set(tokenize(question))
        best_hit = hits[0]
        best_score = float("-inf")

        for hit in hits[:8]:
            text = hit.block.text
            text_terms = set(tokenize(text))
            overlap = len(query_terms.intersection(text_terms))
            penalty = 0.0
            lowered = text.lower()
            if "best practices" in lowered:
                penalty += 0.18
            if self._looks_placeholder_heavy(text):
                penalty += 0.24
            if self._looks_like_question_only(hit):
                penalty += 0.55
            if self._is_description_only_provisioning_row(question, hit):
                penalty += 0.85
            row_key = hit.block.metadata.get("row_key", "").strip().lower()
            lowered_question = question.lower()
            if "number portability" in lowered_question and "number portability" not in row_key:
                penalty += 1.25
            if any(term in lowered_question for term in {"two-way", "two way", "2-way"}) and "two-way" not in row_key:
                penalty += 0.8
            if self._requested_sender_labels(question) and not self._row_mentions_requested_sender(question, hit):
                penalty += 0.45
            alignment_bonus = self._question_alignment_bonus(question, hit)
            scope_bonus = 0.1 if hit.block.metadata.get("document_scope") == "profile" else 0.0
            count_bonus = self._count_alignment_bonus(question, hit)
            informativeness = hit.score + (overlap * 0.08) + alignment_bonus + scope_bonus + count_bonus - penalty
            if informativeness > best_score:
                best_score = informativeness
                best_hit = hit

        return best_hit

    def _direct_answer(self, question: str, hit: SearchHit) -> str:
        structured = self._structured_answer(hit)
        if structured:
            binary_answer = self._binary_structured_answer(question, hit)
            if binary_answer:
                return self._anchor_country(question, hit, binary_answer)
            polished = self._polished_structured_answer(question, hit)
            if polished:
                answer = self._apply_binary_verdict(question, polished)
                return self._anchor_country(question, hit, answer)
            answer = self._apply_binary_verdict(question, structured)
            return self._anchor_country(question, hit, answer)

        text = hit.block.text
        # If the block text is already a semantic sentence from our normalizer, use it.
        if text.startswith(("For ", "Regarding ", "The ")) and ":" in text:
            answer = self._apply_binary_verdict(question, text)
            return self._anchor_country(question, hit, answer)

        cleaned = " ".join(text.strip().split())
        if len(cleaned) > 260:
            cleaned = cleaned[:257].rstrip() + "..."
        answer = self._apply_binary_verdict(question, cleaned)
        return self._anchor_country(question, hit, answer)

    @staticmethod
    def _looks_placeholder_heavy(text: str) -> bool:
        lowered = text.lower()
        placeholder_count = sum(lowered.count(marker) for marker in ["n/a", "---", "-----"])
        return placeholder_count >= 2

    @staticmethod
    def _looks_like_question_only(hit: SearchHit) -> bool:
        text = " ".join(hit.block.text.strip().lstrip("-* ").split())
        if len(text) > 180 or not text.endswith("?"):
            return False
        lowered = text.lower()
        if hit.block.block_type == "faq":
            return True
        return lowered.startswith(
            ("what ", "which ", "who ", "where ", "when ", "why ", "how ", "can ", "does ", "do ", "is ", "are ")
        )

    def _confidence(self, question: str, hits: list[SearchHit]) -> str:
        if not hits:
            return "low"
        query_terms = set(tokenize(question))
        top_terms = set()
        for hit in hits[:3]:
            top_terms.update(self._answer_support_terms(hit))
        overlap_ratio = len(query_terms.intersection(top_terms)) / max(1, len(query_terms))
        if hits[0].score >= 0.55 and overlap_ratio >= 0.6:
            return "high"
        if hits[0].score >= 0.3 and overlap_ratio >= 0.35:
            return "medium"
        if self._has_relevant_two_way_evidence(question, hits[0]):
            return "medium"
        return "low"

    def _should_refuse(self, question: str, hits: list[SearchHit]) -> bool:
        if not hits:
            return True
        if all(self._looks_like_question_only(hit) for hit in hits[:3]):
            return True
        if self._confidence(question, hits) == "low":
            return True
        if hits[0].score < self._min_score_threshold:
            return True
        query_terms = set(tokenize(question))
        if not query_terms:
            return True
        top_terms = set()
        for hit in hits[:3]:
            top_terms.update(self._answer_support_terms(hit))
        overlap_ratio = len(query_terms.intersection(top_terms)) / max(1, len(query_terms))
        return overlap_ratio < self._min_overlap_ratio

    @staticmethod
    def _has_relevant_two_way_evidence(question: str, hit: SearchHit) -> bool:
        lowered_question = question.lower()
        if "two-way" not in lowered_question and "two way" not in lowered_question:
            return False
        support_text = ExtractiveAnswerer._support_polarity_text(hit)
        if "two-way" not in support_text and "two way" not in support_text:
            return False
        return hit.score >= 0.3

    def _route_tier(self, intent, best: SearchHit, hits: list[SearchHit], confidence: str) -> str:
        if not hits:
            return "refusal"
        if confidence == "low":
            return "refusal"

        doc_count = len({hit.block.document_id for hit in hits[:3]})

        # ── Corpus-first: high-confidence single-block answers go straight to Tier 0.
        # table_fact is added here because most factoid queries (country/sender/
        # regulation lookups) are already verbatim in a table row.
        if (
            confidence in {"high", "medium"}
            and best.score >= self._tier0_score_threshold
            and best.block.block_type in {"faq", "policy_rule", "procedure_step", "table_fact", "structured_fact"}
        ):
            return "tier0"

        # ── Only escalate to provider (Tier 2) when the corpus genuinely cannot answer:
        #   - comparative / multi-document synthesis questions, OR
        #   - evidence spans multiple documents AND no single block is highly confident.
        # We never call the provider when the corpus already has a high-confidence answer.
        corpus_can_answer = confidence == "high" or best.score >= self._tier2_score_threshold
        if not corpus_can_answer and (intent.is_comparative or doc_count > 1):
            return "tier2"

        if intent.is_procedural or best.block.block_type in {"narrative", "table_fact", "structured_fact"}:
            return "tier1"
        return "tier1"

    def _answer_support_terms(self, hit: SearchHit) -> set[str]:
        support_text = " ".join(
            [
                hit.block.title,
                " ".join(hit.block.section_path),
                hit.block.metadata.get("row_key", ""),
                hit.block.metadata.get("row_values", ""),
                hit.block.text,
            ]
        )
        return set(tokenize(support_text))

    def _question_alignment_bonus(self, question: str, hit: SearchHit) -> float:
        lowered_question = question.lower()
        lowered_text = " ".join(
            [
                hit.block.text.lower(),
                " ".join(part.lower() for part in hit.block.section_path),
                hit.block.metadata.get("row_key", "").lower(),
                hit.block.metadata.get("row_values", "").lower(),
            ]
        )
        bonus = 0.0

        if self._is_binary_question(lowered_question):
            if any(token in lowered_question for token in {"required", "require", "necessary", "need"}):
                if any(token in lowered_text for token in {"required", "mandatory", "needed", "prerequisite"}):
                    bonus += 0.35
                if "not required" in lowered_text or "no sender registration needed" in lowered_text:
                    bonus += 0.12
                if "supported" in lowered_text and not any(
                    token in lowered_text for token in {"required", "mandatory", "needed"}
                ):
                    bonus -= 0.1
            if any(token in lowered_question for token in {"support", "supports", "supported", "available", "allowed"}):
                if any(token in lowered_text for token in {"supported", "available", "allowed"}):
                    bonus += 0.22
                if any(token in lowered_text for token in {"not supported", "forbidden", "prohibited", "blocked"}):
                    bonus += 0.08
                row_key = hit.block.metadata.get("row_key", "").strip().lower()
                if "twilio supported" in row_key:
                    bonus += 1.05
                if (
                    any(token in lowered_question for token in {"sender id", "sender ids", "alphanumeric"})
                    and "sender id preserved" in row_key
                    and not self._asks_about_preservation(question)
                ):
                    bonus -= 0.85
                if any(term in row_key for term in {"best practices", "use case restrictions"}):
                    bonus -= 0.18
                if "provisioning time" in row_key and "provisioning" not in lowered_question:
                    bonus -= 0.22

        row_key = hit.block.metadata.get("row_key", "").lower()
        if any(token in lowered_question for token in {"registration", "required", "require"}):
            if any(token in row_key for token in {"service restrictions", "sender provisioning", "use case restrictions"}):
                bonus += 0.15
            if "preregistration=required" in lowered_text or "pre-register" in lowered_text:
                bonus += 0.22
        if "how long" in lowered_question:
            if any(token in lowered_text for token in {"provisioning time", "3 weeks", "2 weeks", "weeks", "months", "days"}):
                bonus += 0.28
        if "sender" in lowered_question:
            if any(token in lowered_text for token in {"sender provisioning", "twilio supported", "sender id", "short code"}):
                bonus += 0.12
            if any(token in lowered_text for token in {"locale summary", "locale name", "dialing code"}) and "sender" not in lowered_text:
                bonus -= 0.18
        if "sender provisioning" in lowered_question or "provisioning process" in lowered_question:
            row_key = hit.block.metadata.get("row_key", "").strip().lower()
            if row_key == "sender provisioning":
                bonus += 1.65
            if row_key == "provisioning time" and self._row_has_non_description_value(hit.block.metadata.get("row_values", "")):
                bonus += 0.08
        return bonus

    @staticmethod
    def _asks_about_preservation(question: str) -> bool:
        lowered = question.lower()
        return any(term in lowered for term in {"preserved", "preserve", "overwritten", "overwrite", "changed"})

    @staticmethod
    def _asks_for_required(question: str) -> bool:
        lowered = question.lower()
        return any(term in lowered for term in ["need", "needs", "needed", "require", "required", "requiring", "mandatory"])

    @staticmethod
    def _asks_for_support(question: str) -> bool:
        lowered = question.lower()
        return any(term in lowered for term in ["available", "availability", "support", "supported", "supports"])

    @staticmethod
    def _is_negative_requirement(hit: SearchHit) -> bool:
        support_text = " ".join(
            [
                hit.block.text,
                hit.block.metadata.get("row_key", ""),
                hit.block.metadata.get("row_values", ""),
                hit.block.enriched_text,
            ]
        ).lower()
        return any(
            phrase in support_text
            for phrase in [
                "does not require",
                "not required",
                "no registration required",
                "no sender registration needed",
                "registration is not required",
                "not mandatory",
            ]
        )

    @staticmethod
    def _is_negative_support(hit: SearchHit) -> bool:
        support_text = ExtractiveAnswerer._support_polarity_text(hit)
        return any(
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

    @staticmethod
    def _is_positive_support(hit: SearchHit) -> bool:
        support_text = ExtractiveAnswerer._support_polarity_text(hit)
        if ExtractiveAnswerer._is_negative_support(hit):
            return False
        return any(
            phrase in support_text
            for phrase in [
                "is supported",
                "supported in",
                "supported learn more",
                "is available",
                "available for",
                "value=yes",
                "value: yes",
                "=yes",
            ]
        ) or bool(re.search(r"\btwo[- ]?way\b.{0,80}\byes\b", support_text))

    @staticmethod
    def _support_polarity_text(hit: SearchHit) -> str:
        return " ".join(
            [
                hit.block.text,
                hit.block.metadata.get("row_key", ""),
                hit.block.metadata.get("row_values", ""),
                hit.block.enriched_text,
            ]
        ).lower()

    @staticmethod
    def _looks_like_standalone_fact(text: str) -> bool:
        lowered = text.lower()
        if not text or "=" in text[:80] or lowered.startswith(("-", "value=", "country_name=", "country_iso2=")):
            return False
        return any(
            marker in lowered
            for marker in [
                "requires",
                "require",
                "needed",
                "mandatory",
                "supported",
                "not supported",
                "not required",
                "does not require",
                "allowed",
                "not allowed",
                "can only",
                "only be sent",
            ]
        )

    @staticmethod
    def _count_alignment_bonus(question: str, hit: SearchHit) -> float:
        lowered_question = question.lower()
        lowered_text = " ".join(
            [
                hit.block.text.lower(),
                hit.block.metadata.get("row_key", "").lower(),
                hit.block.metadata.get("row_values", "").lower(),
            ]
        )
        if "how many" in lowered_question or "count" in lowered_question or "number of" in lowered_question:
            if "locale" in lowered_question and "locale count" in lowered_text:
                return 0.42
            if "locale count" in lowered_text or "count: " in lowered_text:
                return 0.35
            if "error count" in lowered_text and "error" not in lowered_question:
                return -0.12
            if "source index" in lowered_text:
                return -0.08
        return 0.0

    @staticmethod
    def _is_binary_question(question: str) -> bool:
        stripped = question.strip().lower()
        return stripped.startswith(("is ", "are ", "does ", "do ", "can ", "should ", "must "))

    def _apply_binary_verdict(self, question: str, statement: str) -> str:
        if not self._is_binary_question(question.lower()):
            return statement
        verdict = self._binary_verdict(statement)
        if verdict == "yes" and not statement.lower().startswith("yes"):
            return f"Yes. {statement}"
        if verdict == "no" and not statement.lower().startswith("no"):
            return f"No. {statement}"
        return statement

    @staticmethod
    def _binary_verdict(statement: str) -> str | None:
        lowered = statement.lower()
        explicit_negative_patterns = [
            " is: no",
            " is no.",
            " value=no",
            " value: no",
            " = no",
        ]
        explicit_positive_patterns = [
            " is: yes",
            " is yes.",
            " value=yes",
            " value: yes",
            " = yes",
        ]
        positive_markers = [
            " is required",
            " are required",
            "mandatory",
            "needed",
            "supported",
            "available",
            "allowed",
            "can be used",
        ]
        negative_markers = [
            "not required",
            "not supported",
            "not available",
            "not allowed",
            "forbidden",
            "prohibited",
            "blocked",
            "rejected",
            "no sender registration needed",
        ]
        if any(marker in lowered for marker in explicit_negative_patterns):
            return "no"
        if any(marker in lowered for marker in explicit_positive_patterns):
            return "yes"
        if any(marker in lowered for marker in negative_markers):
            return "no"
        if any(marker in lowered for marker in positive_markers):
            return "yes"
        return None

    def _binary_structured_answer(self, question: str, hit: SearchHit) -> str:
        if not self._is_binary_question(question):
            return ""

        row_key, row_values, _ = self._flatten_structured_row(hit)
        if not row_key or not row_values:
            return ""

        rendered_value = self._render_row_values(row_values) or row_values.strip()
        requested_value = self._requested_sender_value(question, row_key.lower(), row_values)
        decision_value = requested_value or rendered_value
        verdict = (
            self._row_specific_binary_verdict(question, row_key, decision_value, row_values)
            or self._binary_verdict(decision_value)
            or self._binary_verdict(f"{row_key} is: {decision_value}")
        )
        if verdict not in {"yes", "no"}:
            return ""
        sender_label = self._requested_sender_label(question)
        if (
            "twilio supported" in row_key.lower()
            and sender_label == "alphanumeric"
            and "not supported" in row_values.lower()
        ):
            decision_value = rendered_value

        country = self._country_label(question, hit)
        subject = country or "this market"
        row_label = row_key.strip()
        evidence_value = self._trim(decision_value, max_chars=140)
        lowered_row_key = row_label.lower()

        if "twilio supported" in lowered_row_key:
            feature = f"{sender_label} sender IDs" if sender_label else "this sender type"
            support_phrase = "are supported" if verdict == "yes" else "are not supported"
            return (
                f"{verdict.title()}. In {subject}, {feature} {support_phrase}; "
                f"the `{row_label}` row says `{evidence_value}`."
            )

        if "sender id preserved" in lowered_row_key:
            feature = f"{sender_label} sender IDs" if sender_label else "sender IDs"
            support_phrase = "are preserved" if verdict == "yes" else "are not preserved"
            return (
                f"{verdict.title()}. In {subject}, {feature} {support_phrase}; "
                f"the `{row_label}` row says `{evidence_value}`."
            )

        if "number portability" in lowered_row_key:
            support_phrase = "is available" if verdict == "yes" else "is not available"
            return (
                f"{verdict.title()}. Number portability {support_phrase} in {subject}; "
                f"the `{row_label}` row says `{evidence_value}`."
            )

        if "two-way" in lowered_row_key:
            support_phrase = "is supported" if verdict == "yes" else "is not supported"
            return (
                f"{verdict.title()}. Two-way messaging {support_phrase} in {subject}; "
                f"the `{row_label}` row says `{evidence_value}`."
            )

        if any(term in lowered_row_key for term in {"sender provisioning", "sender registration", "service restrictions"}):
            support_phrase = "requires sender registration" if verdict == "yes" else "does not require sender registration"
            return (
                f"{verdict.title()}. {subject} {support_phrase}; "
                f"the `{row_label}` row says `{evidence_value}`."
            )

        return (
            f"{verdict.title()}. In {subject}, the `{row_label}` row says `{evidence_value}`."
        )

    @staticmethod
    def _row_specific_binary_verdict(
        question: str,
        row_key: str,
        value: str,
        row_values: str,
    ) -> str | None:
        lowered_row_key = row_key.lower()
        lowered_value = value.lower()
        if "twilio supported" in lowered_row_key:
            if ExtractiveAnswerer._requested_sender_label(question) == "alphanumeric":
                lowered_row_values = row_values.lower()
                if "not supported" in lowered_row_values or "not available" in lowered_row_values:
                    return "no"
            if "not supported" in lowered_value or "not available" in lowered_value:
                return "no"
            if "supported" in lowered_value or "available" in lowered_value:
                return "yes"
        return None

    def _structured_answer(self, hit: SearchHit) -> str:
        row_key, row_values, extra_context = self._flatten_structured_row(hit)
        if not row_key or not row_values:
            return ""

        rendered_value = self._render_row_values(row_values)
        if not rendered_value:
            return ""

        context = self._context_label(hit)
        if extra_context and extra_context.lower() not in context.lower():
            context = f"{context} ({extra_context})" if context else extra_context
        
        if context:
            answer = f"In {context}, the {row_key} is: {rendered_value}"
        else:
            answer = f"The {row_key} is: {rendered_value}"

        return self._trim(answer)

    def _polished_structured_answer(self, question: str, hit: SearchHit) -> str:
        raw_row_key_lower = hit.block.metadata.get("row_key", "").strip().lower()
        if raw_row_key_lower in {"enriched_text", "value"} or any(
            term in raw_row_key_lower
            for term in {"content_restriction", "quiet hours", "quiet_hours", "do not disturb", "dnd", "promotional"}
        ):
            direct_value = hit.block.metadata.get("structured_value", "").strip() or hit.block.metadata.get("row_values", "").strip()
            direct_value = re.sub(r"^[-*\s]*(?:enriched_text|value):\s*", "", direct_value, flags=re.I).strip()
            if direct_value:
                return self._trim(direct_value)

        row_key, row_values, extra_context = self._flatten_structured_row(hit)
        row_key_lower = row_key.lower()
        value = self._render_row_values(row_values) or row_values.strip()
        value_lower = value.lower()
        country = self._country_label(question, hit)
        structured_value = hit.block.metadata.get("structured_value", "").strip()

        if row_key_lower in {"exceptions", "conditions", "applies to", "notes"} and self._looks_like_standalone_fact(value):
            return self._trim(value)

        code_label = self._code_fact_label(row_key_lower)
        if code_label:
            direct_value = structured_value or value
            direct_value = re.sub(r"^value:\s*", "", direct_value, flags=re.I).strip()
            if direct_value:
                if code_label == "dialing code":
                    direct_value = self._format_dialing_code(direct_value)
                if country:
                    return f"{country}'s {code_label} is {direct_value}."
                return f"The {code_label} is {direct_value}."

        requested_value = self._requested_sender_value(question, row_key_lower, row_values)
        if requested_value:
            sender_label = self._requested_sender_label(question)
            subject = country or "this market"
            if "twilio supported" in row_key_lower or "operator network capability" in row_key_lower:
                return self._support_answer(subject, sender_label, requested_value)
            if "sender id preserved" in row_key_lower:
                return self._preservation_answer(subject, sender_label, requested_value)
            if "provisioning time" in row_key_lower:
                sender_phrase = f" for {sender_label} sender IDs" if sender_label else ""
                return f"In {subject}, the provisioning time{sender_phrase} is {requested_value}."
            if any(term in row_key_lower for term in {"sender availability", "sender provisioning"}):
                sender_phrase = f" for {sender_label} sender IDs" if sender_label else ""
                return f"In {subject}, the {row_key} value{sender_phrase} is {requested_value}."

        if "number portability" in row_key_lower:
            subject = country or "this market"
            if self._positive_value(value):
                return f"Number portability is available in {subject}."
            if self._negative_value(value):
                return f"Number portability is not available in {subject}."
            return f"In {subject}, number portability is: {value}."

        if any(term in row_key_lower for term in {"handset delivery", "delivery receipt", "delivery receipts"}):
            subject = country or "this market"
            if self._positive_value(value) or "supported" in value_lower:
                return f"Handset delivery receipts are supported in {subject}."
            if self._negative_value(value) or "not supported" in value_lower:
                return f"Handset delivery receipts are not supported in {subject}."
            return f"In {subject}, handset delivery receipt support is: {value}."

        if "default sender" in question.lower() or "dynamic sender is not used" in question.lower():
            default_senders = self._default_sender_values(value)
            if default_senders:
                subject = country or "this market"
                return f"In {subject}, the default sender IDs are {default_senders}."

        if any(term in row_key_lower for term in {"sender provisioning", "sender registration", "service restrictions"}):
            if "no sender registration needed" in value_lower or "not required" in value_lower:
                subject = country or "This market"
                return f"{subject} does not require sender registration."
            if any(term in value_lower for term in {"registration required", "is required", "required for", "mandatory"}):
                subject = country or "This market"
                detail = value.rstrip(".")
                if detail.lower().startswith("sender registration"):
                    return f"{subject} requires {detail[0].lower()}{detail[1:]}."
                return f"{subject} requires sender registration: {detail}."

        if "two-way" in row_key_lower:
            subject = f" in {country}" if country else ""
            if "sms" in question.lower() and "whatsapp" in value_lower and "sms" not in value_lower:
                market = country or "this market"
                return f"Two-way SMS is not supported in {market}; the available two-way conversation channel is WhatsApp."
            if any(term in value_lower for term in {"not supported", "not available", "no"}):
                return f"Two-way messaging is not supported{subject}."
            if any(term in value_lower for term in {"supported", "available", "yes"}):
                return f"Two-way messaging is supported{subject}."

        if "twilio supported" in row_key_lower and "supported" in value_lower:
            context = extra_context or self._context_label(hit)
            feature_label = self._specific_context_label(context)
            feature = f"{feature_label} sender IDs" if feature_label else "This feature"
            subject = f" in {country}" if country else ""
            return f"{feature} are supported{subject}."

        enriched = hit.block.enriched_text.strip()
        if enriched and self._enrichment_matches_value(enriched, value):
            return self._trim(enriched)

        return ""

    def _evidence_text(self, hit: SearchHit) -> str:
        structured = self._structured_answer(hit)
        return structured or self._trim(" ".join(hit.block.text.split()))

    def _flatten_structured_row(self, hit: SearchHit) -> tuple[str, str, str]:
        metadata = hit.block.metadata
        row_key = metadata.get("row_key", "").strip()
        row_values = metadata.get("row_values", "").strip()
        if not row_values:
            return row_key, row_values, ""

        prefix_labels, remainder = self._extract_prefix_labels(row_values)
        if not prefix_labels:
            return row_key, row_values, ""

        extra_context = ""
        nested_key = row_key
        if len(prefix_labels) == 1:
            extra_context = prefix_labels[0]
        else:
            extra_context = prefix_labels[0]
            nested_key = prefix_labels[-1]

        nested_candidate, nested_remainder = self._extract_nested_key(remainder)
        if nested_candidate:
            nested_key = nested_candidate
            remainder = nested_remainder

        return nested_key, remainder, extra_context

    def _context_label(self, hit: SearchHit) -> str:
        if not hit.block.section_path:
            return ""
        title = hit.block.title.strip().lower()
        current = hit.block.section_path[-1].strip()
        if current and current.lower() != title:
            return current
        return hit.block.title.strip()

    def _country_label(self, question: str, hit: SearchHit) -> str:
        title_country = self._country_from_title(hit.block.title)
        title = hit.block.title.strip()
        if not title_country and self._normalized_label(title) == hit.block.document_id.strip().lower():
            title_country = title
        document_country = self._country_from_document_id(hit.block.document_id)
        document_iso = self._iso_from_document_id(hit.block.document_id)
        block_iso = hit.block.iso_code.strip().upper()

        if title_country and self._country_metadata_conflicts(hit.block.country, block_iso, document_iso):
            return title_country
        if document_country and self._country_metadata_conflicts(hit.block.country, block_iso, document_iso):
            return document_country
        if title_country:
            return title_country

        if hit.block.country.strip():
            return hit.block.country.strip()

        if document_country:
            return document_country

        lowered_question = question.lower()
        for candidate in hit.block.section_path:
            normalized = self._humanize_label(candidate)
            if normalized and normalized.lower() in lowered_question:
                return normalized
        return ""

    def _country_key(self, hit: SearchHit) -> str:
        title_iso = self._iso_from_title(hit.block.title)
        if title_iso:
            return title_iso
        document_iso = self._iso_from_document_id(hit.block.document_id)
        if document_iso:
            return document_iso
        if hit.block.iso_code.strip():
            return hit.block.iso_code.strip().upper()
        country = self._country_label("", hit)
        if country:
            return country.lower()
        row_values = hit.block.metadata.get("row_values", "")
        for pattern in (
            r"(?:^|;\s*)country_iso2=([A-Za-z]{2})(?:;|$)",
            r"(?:^|;\s*)iso2=([A-Za-z]{2})(?:;|$)",
            r"(?:^|;\s*)iso_code=([A-Za-z]{2})(?:;|$)",
            r"(?:^|;\s*)country_name=([^;]+)",
            r"(?:^|;\s*)country=([^;]+)",
        ):
            match = re.search(pattern, row_values, flags=re.IGNORECASE)
            if match:
                return match.group(1).strip().lower()
        return hit.block.document_id.strip().lower()

    @staticmethod
    def _country_from_title(title: str) -> str:
        title = title.strip()
        if title and "(" in title:
            return title.split("(", 1)[0].strip()
        return ""

    @staticmethod
    def _normalized_label(value: str) -> str:
        return re.sub(r"[^a-z0-9]+", "_", value.strip().lower()).strip("_")

    @staticmethod
    def _iso_from_title(title: str) -> str:
        match = re.search(r"\(([A-Za-z]{2})\)", title)
        return match.group(1).upper() if match else ""

    @staticmethod
    def _country_from_document_id(document_id: str) -> str:
        if "_" not in document_id:
            return ""
        stem = "_".join(document_id.split("_")[:-1])
        return ExtractiveAnswerer._humanize_label(stem)

    @staticmethod
    def _iso_from_document_id(document_id: str) -> str:
        match = re.search(r"_([a-z]{2})$", document_id.lower())
        return match.group(1).upper() if match else ""

    @staticmethod
    def _country_metadata_conflicts(country: str, block_iso: str, document_iso: str) -> bool:
        if document_iso and block_iso and block_iso != document_iso:
            return True
        return bool(country.strip())

    def _render_row_values(self, row_values: str) -> str:
        parts = [part.strip() for part in row_values.split(";") if part.strip()]
        if not parts:
            return self._trim(row_values)

        keyed_values = {
            label.strip().lower(): value.strip()
            for part in parts
            if "=" in part
            for label, value in [part.split("=", 1)]
        }
        direct_value = keyed_values.get("value") or keyed_values.get("structured_value")
        if direct_value and direct_value.lower() not in {"n/a", "---", "-----", "/", "unknown", "null"}:
            return self._trim(direct_value)

        informative_parts: list[str] = []
        dynamic_part = ""
        metadata_labels = {
            "answer_signal",
            "block_id",
            "country",
            "country_iso2",
            "country_name",
            "fact_id",
            "fact_type",
            "hypothetical_questions",
            "iso_code",
            "local_aliases",
            "regulation_topics",
            "source_anchor",
            "sender_types",
            "topic",
        }
        for part in parts:
            if "=" not in part:
                informative_parts.append(part)
                continue
            label, value = [item.strip() for item in part.split("=", 1)]
            if not value or value.lower() in {"n/a", "---", "-----", "/"}:
                continue
            if label.lower() == "description":
                continue
            if label.lower() in metadata_labels:
                continue
            if label.lower() == "dynamic":
                dynamic_part = f"Dynamic={value}"
                continue
            informative_parts.append(f"{label}: {value}")

        if dynamic_part:
            return self._trim(dynamic_part)
        if informative_parts:
            return self._trim("; ".join(informative_parts))

        filtered = []
        for part in parts:
            if "=" not in part:
                filtered.append(part)
                continue
            label, value = [item.strip() for item in part.split("=", 1)]
            if label.lower() == "description" and value:
                filtered.append(value)
        if filtered:
            return self._trim("; ".join(filtered))
        return ""

    @staticmethod
    def _format_dialing_code(value: str) -> str:
        cleaned = value.strip()
        if re.fullmatch(r"\d{1,4}", cleaned):
            return f"+{cleaned}"
        return cleaned

    def _requested_sender_value(self, question: str, row_key_lower: str, row_values: str) -> str:
        if not any(
            term in row_key_lower
            for term in {
                "twilio supported",
                "operator network capability",
                "sender id preserved",
                "provisioning time",
                "sender availability",
                "sender provisioning",
                "handset delivery",
                "delivery receipt",
                "delivery receipts",
            }
        ):
            return ""

        requested_labels = self._requested_sender_labels(question)
        if not requested_labels:
            return ""

        keyed_values = self._extract_row_value_map(row_values)
        if not keyed_values:
            return ""

        candidates: list[str] = []
        for label, value in keyed_values.items():
            if label == "description" or not value:
                continue
            if any(requested in label for requested in requested_labels):
                candidates.append(value)

        if not candidates and "alphanumeric" in requested_labels:
            candidates = [
                value
                for label, value in keyed_values.items()
                if "pre-registration" in label or "preregistration" in label or label == "dynamic"
            ]

        return self._select_sender_value(row_key_lower, candidates)

    def _row_mentions_requested_sender(self, question: str, hit: SearchHit) -> bool:
        row_key = hit.block.metadata.get("row_key", "").strip().lower()
        if not any(
            term in row_key
            for term in {
                "twilio supported",
                "sender id preserved",
                "provisioning time",
                "sender availability",
                "sender provisioning",
            }
        ):
            return True
        support_text = " ".join(
            [
                hit.block.text,
                hit.block.metadata.get("row_values", ""),
                " ".join(hit.block.section_path),
            ]
        ).lower()
        return any(label in support_text for label in self._requested_sender_labels(question))

    @classmethod
    def _is_description_only_provisioning_row(cls, question: str, hit: SearchHit) -> bool:
        lowered_question = question.lower()
        if "provisioning" not in lowered_question:
            return False
        if hit.block.metadata.get("row_key", "").strip().lower() != "provisioning time":
            return False
        return not cls._row_has_non_description_value(hit.block.metadata.get("row_values", ""))

    @classmethod
    def _row_has_non_description_value(cls, row_values: str) -> bool:
        values = cls._extract_row_value_map(row_values)
        return any(label != "description" and value.strip() for label, value in values.items())

    @staticmethod
    def _extract_row_value_map(row_values: str) -> dict[str, str]:
        normalized = row_values.replace(";", ",")
        pattern = re.compile(
            r"(?:^|,\s*)(?:the\s+)?(?P<label>[A-Za-z][A-Za-z0-9 /&'()_-]{1,80}?)\s+"
            r"(?:is|=|:)\s+"
            r"(?P<value>.*?)(?=,\s*(?:the\s+)?[A-Za-z][A-Za-z0-9 /&'()_-]{1,80}?\s+(?:is|=|:)\s+|$)",
            flags=re.IGNORECASE,
        )
        values: dict[str, str] = {}
        for match in pattern.finditer(normalized):
            label = re.sub(r"\s+", " ", match.group("label").strip()).lower()
            value = re.sub(r"\s+", " ", match.group("value").strip(" ."))
            if label and value:
                values[label] = value
        return values

    @staticmethod
    def _requested_sender_labels(question: str) -> list[str]:
        lowered = question.lower()
        normalized = lowered.replace("-", " ")
        labels: list[str] = []
        if "short code" in normalized or "short codes" in normalized:
            labels.append("short code")
        if "long code" in normalized or "long codes" in normalized:
            labels.extend(["long code domestic", "long code international", "long code"])
        if "toll free" in normalized:
            labels.extend(["toll-free", "toll free"])
        if "alphanumeric" in lowered or (
            ("sender id" in lowered or "sender ids" in lowered)
            and not any(labels)
        ):
            labels.append("alphanumeric")
        return labels

    @staticmethod
    def _requested_sender_label(question: str) -> str:
        lowered = question.lower().replace("-", " ")
        if "short code" in lowered or "short codes" in lowered:
            return "short code"
        if "long code" in lowered or "long codes" in lowered:
            return "long code"
        if "toll free" in lowered:
            return "toll-free"
        if "alphanumeric" in lowered or "sender id" in lowered or "sender ids" in lowered:
            return "alphanumeric"
        return ""

    def _select_sender_value(self, row_key_lower: str, candidates: list[str]) -> str:
        cleaned = [candidate.strip() for candidate in candidates if candidate.strip()]
        if not cleaned:
            return ""
        lowered = [candidate.lower() for candidate in cleaned]
        if "provisioning time" in row_key_lower:
            for candidate, lowered_candidate in zip(cleaned, lowered, strict=True):
                if any(char.isdigit() for char in candidate) or any(
                    unit in lowered_candidate for unit in {"day", "week", "month", "hour"}
                ):
                    return candidate
        if "twilio supported" in row_key_lower or "operator network capability" in row_key_lower:
            if any(self._negative_value(candidate) for candidate in cleaned):
                return next(candidate for candidate in cleaned if self._negative_value(candidate))
            if any(self._positive_value(candidate) for candidate in cleaned):
                return next(candidate for candidate in cleaned if self._positive_value(candidate))
        if "sender id preserved" in row_key_lower:
            if all(self._positive_value(candidate) for candidate in cleaned):
                return "Yes"
            if any(self._negative_value(candidate) for candidate in cleaned):
                return next(candidate for candidate in cleaned if self._negative_value(candidate))
        return "; ".join(dict.fromkeys(cleaned))

    @staticmethod
    def _default_sender_values(value: str) -> str:
        found: list[str] = []
        for label in ("Verify", "Info", "System"):
            if re.search(rf"\b{re.escape(label)}\b", value, flags=re.IGNORECASE):
                found.append(label)
        if not found:
            return ""
        if len(found) == 1:
            return found[0]
        return ", ".join(found[:-1]) + f", and {found[-1]}"

    @staticmethod
    def _support_answer(subject: str, sender_label: str, value: str) -> str:
        feature = f"{sender_label} sender IDs" if sender_label else "This sender type"
        lowered = value.lower()
        if ExtractiveAnswerer._negative_value(value):
            return f"No. In {subject}, {feature} are not supported."
        if ExtractiveAnswerer._positive_value(value) or "supported" in lowered:
            return f"Yes. In {subject}, {feature} are supported."
        return f"In {subject}, {feature} support is: {value}."

    @staticmethod
    def _preservation_answer(subject: str, sender_label: str, value: str) -> str:
        feature = f"{sender_label} sender IDs" if sender_label else "Sender IDs"
        if ExtractiveAnswerer._negative_value(value):
            return f"No. In {subject}, {feature} are not preserved."
        if ExtractiveAnswerer._positive_value(value):
            return f"Yes. In {subject}, {feature} are preserved."
        return f"In {subject}, {feature} preservation is: {value}."

    @staticmethod
    def _positive_value(value: str) -> bool:
        lowered = value.strip().lower()
        return lowered in {"yes", "supported", "available", "required"} or lowered.startswith("supported")

    @staticmethod
    def _negative_value(value: str) -> bool:
        lowered = value.strip().lower()
        return lowered in {"no", "not supported", "not available", "n/a"} or lowered.startswith("not supported")

    @staticmethod
    def _humanize_label(value: str) -> str:
        cleaned = value.strip().replace("_", " ").replace("-", " ")
        cleaned = re.sub(r"\s+", " ", cleaned)
        if not cleaned:
            return ""
        return " ".join(part.capitalize() for part in cleaned.split())

    @staticmethod
    def _specific_context_label(value: str) -> str:
        cleaned = value.strip()
        if ":" in cleaned:
            cleaned = cleaned.split(":")[-1].strip()
        return cleaned

    @staticmethod
    def _code_fact_label(row_key_lower: str) -> str:
        if "dialing code" in row_key_lower or "dialling code" in row_key_lower or "calling code" in row_key_lower:
            return "dialing code"
        if row_key_lower in {"iso2", "iso 2"} or "iso2" in row_key_lower:
            return "ISO2 code"
        if "iso code" in row_key_lower:
            return "ISO code"
        if "mcc" in row_key_lower or "mobile country code" in row_key_lower:
            return "MCC"
        if "prefix" in row_key_lower:
            return "prefix"
        return ""

    @staticmethod
    def _enrichment_matches_value(enriched: str, value: str) -> bool:
        value_terms = {term for term in tokenize(value) if len(term) > 3}
        enriched_terms = set(tokenize(enriched))
        if not value_terms:
            return False
        return len(value_terms.intersection(enriched_terms)) / len(value_terms) >= 0.5

    @staticmethod
    def _anchor_country(question: str, hit: SearchHit, answer: str) -> str:
        country = (hit.block.country or "").strip()
        if not country:
            return answer
        lowered_answer = answer.lower()
        if country.lower() in lowered_answer:
            return answer
        if country.lower() not in question.lower():
            return answer
        if answer.startswith(("Yes.", "No.")):
            verdict, _, remainder = answer.partition(". ")
            if remainder:
                return f"{verdict}. In {country}, {remainder[0].lower()}{remainder[1:]}"
            return f"{verdict}. In {country}."
        return f"In {country}, {answer[0].lower()}{answer[1:]}"

    def _extract_prefix_labels(self, row_values: str) -> tuple[list[str], str]:
        labels: list[str] = []
        remainder = row_values

        while ":" in remainder:
            candidate, tail = remainder.split(":", 1)
            candidate = candidate.strip()
            tail = tail.strip()
            if not self._looks_like_prefix_label(candidate) or "=" in candidate:
                break
            if tail.startswith("="):
                break
            labels.append(candidate)
            remainder = tail
            if "=" in candidate:
                break
            if "=" in remainder.split(";", 1)[0]:
                break

        if not labels:
            return [], row_values
        return labels, remainder

    def _extract_nested_key(self, remainder: str) -> tuple[str, str]:
        if ":" not in remainder:
            return "", remainder
        candidate, tail = remainder.split(":", 1)
        candidate = candidate.strip()
        tail = tail.strip()
        if not self._looks_like_prefix_label(candidate) or "=" in candidate:
            return "", remainder
        if "=" not in tail:
            return "", remainder
        return candidate, tail

    @staticmethod
    def _looks_like_prefix_label(candidate: str) -> bool:
        if not candidate or len(candidate) > 64:
            return False
        if any(char in candidate for char in {",", ".", "?", "!"}):
            return False
        if re.search(r"\b\d{1,2}$", candidate):
            return False
        return bool(re.match(r"^[A-Za-z][A-Za-z0-9 ()&/'_-]*$", candidate))

    @staticmethod
    def _trim(text: str, max_chars: int = 260) -> str:
        cleaned = " ".join(text.split())
        if len(cleaned) > max_chars:
            return cleaned[: max_chars - 3].rstrip() + "..."
        return cleaned
