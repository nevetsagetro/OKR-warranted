import json
import re
from dataclasses import asdict
from pathlib import Path

from own_knowledge_rag.filename_metadata import build_country_index
from own_knowledge_rag.models import Answer, EvaluationCase, EvaluationCaseResult, EvaluationSummary, SearchHit

_COUNTRY_INDEX = build_country_index()


class Evaluator:
    def load_cases(self, benchmark_path: Path) -> list[EvaluationCase]:
        payload = json.loads(benchmark_path.read_text(encoding="utf-8"))
        if not isinstance(payload, list):
            raise ValueError("Benchmark file must contain a JSON array of evaluation cases.")
        return [EvaluationCase(**item) for item in payload]

    def evaluate(
        self,
        cases: list[EvaluationCase],
        run_case,
    ) -> EvaluationSummary:
        results: list[EvaluationCaseResult] = []
        retrieval_hits = 0
        evidence_hits = 0
        citation_hits = 0
        answer_correct_hits = 0
        country_match_hits = 0
        foreign_evidence_hits = 0
        wrong_country_answer_hits = 0
        country_applicable_cases = 0
        diversity_enforced_cases = 0
        no_answer_total = 0
        no_answer_hits = 0
        cached_answer_count = 0
        total_document_precision = 0.0
        tier_distribution: dict[str, int] = {}
        segment_accumulators: dict[str, list[int]] = {}
        failure_analysis = {
            "by_stage": {},
            "by_question_type": {},
            "by_document": {},
        }

        for case in cases:
            hits, answer = run_case(case.question)
            result = self._evaluate_case(case, hits, answer)
            results.append(result)
            retrieval_hits += int(result.retrieval_hit)
            evidence_hits += int(result.evidence_hit)
            citation_hits += int(result.citation_hit)
            answer_correct_hits += int(result.answer_correct)
            if self._is_country_case(case):
                country_applicable_cases += 1
                country_match_hits += int(result.country_match_at_1)
                foreign_evidence_hits += int(result.foreign_evidence_present)
                wrong_country_answer_hits += int(not result.country_match_at_1)
            diversity_enforced_cases += int(self._has_document_diversity_enforcement(result.retrieved_document_ids))
            cached_answer_count += int(result.answer_cached)
            total_document_precision += result.document_precision_at_k
            tier_distribution[result.routed_tier] = tier_distribution.get(result.routed_tier, 0) + 1
            if case.should_refuse:
                no_answer_total += 1
                no_answer_hits += int(result.refusal_correct)
            else:
                self._accumulate_segments(segment_accumulators, result)
            self._accumulate_failure_analysis(failure_analysis, result)

        total_cases = len(cases)
        answerable_cases = max(1, len([case for case in cases if not case.should_refuse]))
        fix_decisions = self._fix_decisions(failure_analysis)
        return EvaluationSummary(
            total_cases=total_cases,
            retrieval_recall_at_k=round(retrieval_hits / max(1, answerable_cases), 4),
            evidence_hit_rate=round(evidence_hits / max(1, answerable_cases), 4),
            citation_accuracy=round(citation_hits / max(1, answerable_cases), 4),
            document_precision_at_k=round(total_document_precision / max(1, total_cases), 4),
            no_answer_precision=round(no_answer_hits / max(1, no_answer_total), 4),
            answer_correctness=round(answer_correct_hits / max(1, answerable_cases), 4),
            country_match_at_1=round(country_match_hits / max(1, country_applicable_cases), 4),
            foreign_evidence_rate=round(foreign_evidence_hits / max(1, country_applicable_cases), 4),
            wrong_country_answer_rate=round(wrong_country_answer_hits / max(1, country_applicable_cases), 4),
            diversity_enforcement_rate=round(diversity_enforced_cases / max(1, answerable_cases), 4),
            answer_cache_hit_rate=round(cached_answer_count / max(1, total_cases), 4),
            cached_answer_count=cached_answer_count,
            tier_distribution=tier_distribution,
            segment_breakdown=self._segment_breakdown(segment_accumulators),
            failure_analysis=failure_analysis,
            fix_decisions=fix_decisions,
            results=results,
        )

    def save_summary(self, summary: EvaluationSummary, output_path: Path) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(asdict(summary), indent=2),
            encoding="utf-8",
        )
        markdown_path = output_path.with_suffix(".md")
        markdown_path.write_text(self._markdown_report(summary), encoding="utf-8")
        segments_path = output_path.parent / "evaluation_segments.json"
        segments_path.write_text(
            json.dumps(summary.segment_breakdown, indent=2),
            encoding="utf-8",
        )

    def _evaluate_case(
        self,
        case: EvaluationCase,
        hits: list[SearchHit],
        answer: Answer,
    ) -> EvaluationCaseResult:
        retrieved_document_ids = list(dict.fromkeys(hit.block.document_id for hit in hits))
        retrieved_sections = list(
            dict.fromkeys(" > ".join(hit.block.section_path) for hit in hits if hit.block.section_path)
        )
        expected_docs = set(case.expected_document_ids)
        forbidden_docs = set(case.forbid_document_ids)
        retrieved_docs = set(retrieved_document_ids)
        retrieval_hit = bool(expected_docs.intersection(retrieved_docs)) if expected_docs else False
        section_hit = self._section_hit(case.expected_section_terms, hits)

        hit_text = "\n".join(hit.block.text for hit in hits).lower()
        answer_text = answer.answer.lower()
        expected_terms = [term.lower() for term in case.expected_terms]
        evidence_hit = self._matches_terms(expected_terms, hit_text, fallback=retrieval_hit)
        citation_hit = self._citation_hit(case, answer.evidence)
        block_type_hit = self._block_type_hit(case.expected_block_types, hits)
        metadata_hit = self._metadata_hit(case.expected_metadata, hits)
        answer_correct = self._matches_terms(expected_terms, answer_text, fallback=retrieval_hit)
        expected_iso = self._expected_iso(case)
        country_match_at_1 = self._country_match_at_1(expected_iso, hits)
        foreign_evidence_present = self._foreign_evidence_present(case, expected_iso, answer.evidence)
        forbidden_document_present = any(doc_id in forbidden_docs for doc_id in retrieved_document_ids)
        mixed_document_violation = case.must_not_mix_documents and len(set(hit.block.document_id for hit in answer.evidence)) > 1

        refusal_text = "insufficient evidence" in answer_text
        refusal_correct = refusal_text if case.should_refuse else not refusal_text
        document_precision = self._document_precision(expected_docs, retrieved_document_ids)
        failure_stage, failure_reasons = self._classify_failure(
            case=case,
            retrieval_hit=retrieval_hit,
            evidence_hit=evidence_hit,
            section_hit=section_hit,
            block_type_hit=block_type_hit,
            metadata_hit=metadata_hit,
            citation_hit=citation_hit,
            answer_correct=answer_correct,
            country_match_at_1=country_match_at_1,
            foreign_evidence_present=foreign_evidence_present,
            forbidden_document_present=forbidden_document_present,
            mixed_document_violation=mixed_document_violation,
            refusal_correct=refusal_correct,
            answer=answer,
        )

        return EvaluationCaseResult(
            question=case.question,
            expected_document_ids=case.expected_document_ids,
            expected_source_paths=case.expected_source_paths,
            expected_terms=case.expected_terms,
            expected_section_terms=case.expected_section_terms,
            expected_block_types=case.expected_block_types,
            expected_sender_types=case.expected_sender_types,
            expected_metadata=case.expected_metadata,
            expected_iso_code=case.expected_iso_code,
            question_type=case.question_type,
            should_refuse=case.should_refuse,
            answer_text=answer.answer,
            retrieved_document_ids=retrieved_document_ids,
            retrieved_sections=retrieved_sections,
            refusal_correct=refusal_correct,
            retrieval_hit=False if case.should_refuse else retrieval_hit,
            evidence_hit=False if case.should_refuse else evidence_hit,
            citation_hit=False if case.should_refuse else citation_hit,
            section_hit=False if case.should_refuse else section_hit,
            block_type_hit=False if case.should_refuse else block_type_hit,
            metadata_hit=False if case.should_refuse else metadata_hit,
            answer_correct=False if case.should_refuse else answer_correct,
            document_precision_at_k=document_precision,
            country_match_at_1=False if case.should_refuse else country_match_at_1,
            foreign_evidence_present=False if case.should_refuse else foreign_evidence_present,
            forbidden_document_present=False if case.should_refuse else forbidden_document_present,
            mixed_document_violation=False if case.should_refuse else mixed_document_violation,
            answer_confidence=answer.confidence,
            routed_tier=answer.tier,
            query_intent=answer.query_intent,
            answer_cached=answer.cached,
            failure_stage=failure_stage,
            failure_reasons=failure_reasons,
        )

    @staticmethod
    def _matches_terms(expected_terms: list[str], haystack: str, fallback: bool) -> bool:
        if not expected_terms:
            return fallback
        normalized_haystack = Evaluator._normalize_match_text(haystack)
        return all(Evaluator._matches_expected_term(term, normalized_haystack) for term in expected_terms)

    @staticmethod
    def _matches_expected_term(term: str, normalized_haystack: str) -> bool:
        normalized_term = Evaluator._normalize_match_text(term)
        if not normalized_term:
            return True
        if normalized_term in normalized_haystack:
            return True
        if re.fullmatch(r"\+?\d{1,5}", normalized_term):
            digits = normalized_term.lstrip("+")
            return bool(re.search(rf"(?<!\d)\+?{re.escape(digits)}(?!\d)", normalized_haystack))
        return any(variant in normalized_haystack for variant in Evaluator._term_variants(normalized_term))

    @staticmethod
    def _normalize_match_text(text: str) -> str:
        lowered = text.lower().replace("’", "'")
        lowered = re.sub(r"(?<=\d)\s*-\s*(?=\d)", "-", lowered)
        lowered = re.sub(r"[^a-z0-9+/-]+", " ", lowered)
        return re.sub(r"\s+", " ", lowered).strip()

    @staticmethod
    def _term_variants(term: str) -> set[str]:
        variants: set[str] = set()
        if term == "yes":
            variants.update(
                {
                    "yes",
                    "is supported",
                    "are supported",
                    "is available",
                    "are available",
                    "is preserved",
                    "are preserved",
                    "is required",
                    "are required",
                }
            )
        if term == "no":
            variants.update({"no", "not supported", "not available", "not preserved", "not required"})
        if term == "supported":
            variants.update({"supported", "available"})
        if term == "not supported":
            variants.update({"not supported", "not available", "unsupported"})
        if term == "not required":
            variants.update(
                {
                    "not required",
                    "does not require",
                    "no sender registration needed",
                    "no registration required",
                    "is supported",
                    "are supported",
                    "is available",
                    "are available",
                }
            )
        if term == "alphanumeric sender id":
            variants.update({"alphanumeric sender id", "alphanumeric sender ids", "alphanumeric"})
        if term == "short code":
            variants.update({"short code", "short codes"})
        if term == "long code":
            variants.update({"long code", "long codes"})
        if term == "toll-free number":
            variants.update({"toll-free number", "toll free number", "toll-free", "toll free"})
        duration_match = re.fullmatch(r"(\d+)\s*(day|days|week|weeks)", term)
        if duration_match:
            amount = int(duration_match.group(1))
            unit = duration_match.group(2)
            if unit.startswith("week"):
                variants.add(f"{amount * 7} days")
                variants.add(f"{amount * 7} day")
            if unit.startswith("day") and amount % 7 == 0:
                week_count = amount // 7
                variants.add(f"{week_count} week")
                variants.add(f"{week_count} weeks")
        range_match = re.fullmatch(r"(\d+)-(\d+)\s*(day|days|week|weeks)", term)
        if range_match:
            start = int(range_match.group(1))
            end = int(range_match.group(2))
            unit = range_match.group(3)
            if unit.startswith("day") and start % 7 == 0 and end % 7 == 0:
                variants.add(f"{start // 7}-{end // 7} weeks")
                variants.add(f"{start // 7}-{end // 7} week")
            if unit.startswith("week"):
                variants.add(f"{start * 7}-{end * 7} days")
                variants.add(f"{start * 7}-{end * 7} day")
        return variants

    @staticmethod
    def _block_type_hit(expected_block_types: list[str], hits: list[SearchHit]) -> bool:
        if not expected_block_types:
            return False
        expected = {item.strip().lower() for item in expected_block_types if item.strip()}
        return any(hit.block.block_type.strip().lower() in expected for hit in hits)

    @staticmethod
    def _metadata_hit(expected_metadata: dict[str, str], hits: list[SearchHit]) -> bool:
        if not expected_metadata:
            return False
        expected = {
            key.strip(): str(value).strip().lower()
            for key, value in expected_metadata.items()
            if key.strip()
        }
        if not expected:
            return False
        for hit in hits:
            metadata = hit.block.metadata
            if all(str(metadata.get(key, "")).strip().lower() == value for key, value in expected.items()):
                return True
        return False

    @staticmethod
    def _document_precision(expected_docs: set[str], retrieved_document_ids: list[str]) -> float:
        if not expected_docs or not retrieved_document_ids:
            return 0.0
        relevant = sum(1 for doc_id in retrieved_document_ids if doc_id in expected_docs)
        return round(relevant / len(retrieved_document_ids), 4)

    @staticmethod
    def _expected_iso(case: EvaluationCase) -> str:
        if case.expected_iso_code:
            return case.expected_iso_code.strip().upper()
        if len(case.expected_document_ids) == 1 and "_" in case.expected_document_ids[0]:
            return case.expected_document_ids[0].split("_")[-1].upper()
        return ""

    @staticmethod
    def _hit_iso(hit: SearchHit) -> str:
        explicit_iso = (hit.block.iso_code or hit.block.metadata.get("tag_iso_code", "")).strip().upper()
        if explicit_iso:
            return explicit_iso
        title_key = hit.block.title.strip().lower()
        if title_key in _COUNTRY_INDEX:
            return _COUNTRY_INDEX[title_key]
        document_key = hit.block.document_id.strip().lower().replace("_", " ")
        return _COUNTRY_INDEX.get(document_key, "")

    def _country_match_at_1(self, expected_iso: str, hits: list[SearchHit]) -> bool:
        if not expected_iso or not hits:
            return False
        return self._hit_iso(hits[0]) == expected_iso

    def _foreign_evidence_present(
        self,
        case: EvaluationCase,
        expected_iso: str,
        evidence: list[SearchHit],
    ) -> bool:
        if not evidence or not self._is_country_case(case):
            return False
        expected_docs = set(case.expected_document_ids)
        for hit in evidence:
            hit_doc = hit.block.document_id
            hit_iso = self._hit_iso(hit)
            if expected_docs and hit_doc not in expected_docs:
                return True
            if expected_iso and hit_iso and hit_iso != expected_iso:
                return True
        return False

    @staticmethod
    def _is_country_case(case: EvaluationCase) -> bool:
        return bool(
            case.expected_iso_code
            or (
                len(case.expected_document_ids) == 1
                and "_" in case.expected_document_ids[0]
            )
        )

    @staticmethod
    def _has_document_diversity_enforcement(retrieved_document_ids: list[str]) -> bool:
        counts: dict[str, int] = {}
        for document_id in retrieved_document_ids:
            counts[document_id] = counts.get(document_id, 0) + 1
        return any(count > 1 for count in counts.values()) and all(count <= 2 for count in counts.values())

    def _accumulate_segments(
        self,
        segment_accumulators: dict[str, list[int]],
        result: EvaluationCaseResult,
    ) -> None:
        segment_values = {
            "question_type": result.question_type or "unknown",
            "iso_code": result.expected_iso_code or self._iso_from_document_ids(result.expected_document_ids) or "unknown",
        }
        block_types = result.expected_block_types or ["unknown"]
        for block_type in block_types:
            self._add_segment_metrics(segment_accumulators, "block_type", block_type, result)
        sender_types = result.expected_sender_types or ["unknown"]
        for sender_type in sender_types:
            self._add_segment_metrics(segment_accumulators, "sender_type", sender_type, result)
        for segment_name, segment_value in segment_values.items():
            self._add_segment_metrics(segment_accumulators, segment_name, segment_value, result)

    @staticmethod
    def _add_segment_metrics(
        segment_accumulators: dict[str, list[int]],
        segment_name: str,
        segment_value: str,
        result: EvaluationCaseResult,
    ) -> None:
        metrics = {
            "retrieval_recall_at_k": int(result.retrieval_hit),
            "evidence_hit_rate": int(result.evidence_hit),
            "answer_correctness": int(result.answer_correct),
        }
        for metric_name, hit in metrics.items():
            key = f"{metric_name}|{segment_name}|{segment_value}"
            values = segment_accumulators.setdefault(key, [0, 0])
            values[0] += hit
            values[1] += 1

    @staticmethod
    def _segment_breakdown(segment_accumulators: dict[str, list[int]]) -> dict[str, dict[str, int | float]]:
        return {
            key: {
                "numerator": numerator,
                "denominator": denominator,
                "rate": round(numerator / max(1, denominator), 4),
            }
            for key, (numerator, denominator) in sorted(segment_accumulators.items())
        }

    @staticmethod
    def _iso_from_document_ids(document_ids: list[str]) -> str:
        if len(document_ids) != 1 or "_" not in document_ids[0]:
            return ""
        return document_ids[0].split("_")[-1].upper()

    @staticmethod
    def _section_hit(expected_section_terms: list[str], hits: list[SearchHit]) -> bool:
        if not expected_section_terms:
            return False
        haystack = " ".join(" > ".join(hit.block.section_path).lower() for hit in hits if hit.block.section_path)
        return all(term.lower() in haystack for term in expected_section_terms)

    @staticmethod
    def _citation_hit(case: EvaluationCase, hits: list[SearchHit]) -> bool:
        if not hits:
            return False
        if not case.expected_document_ids and not case.expected_source_paths and not case.expected_anchor_terms:
            return False

        relevant_hits = hits
        if case.expected_document_ids:
            expected_docs = set(case.expected_document_ids)
            relevant_hits = [hit for hit in relevant_hits if hit.block.document_id in expected_docs]
        if case.expected_source_paths:
            expected_paths = set(case.expected_source_paths)
            relevant_hits = [hit for hit in relevant_hits if hit.block.source_path in expected_paths]
        if case.expected_section_terms:
            lowered_section_terms = [term.lower() for term in case.expected_section_terms]
            relevant_hits = [
                hit
                for hit in relevant_hits
                if all(term in " > ".join(hit.block.section_path).lower() for term in lowered_section_terms)
            ]
        if not relevant_hits:
            return False

        anchor_terms = [term.lower() for term in (case.expected_anchor_terms or [])]
        for hit in relevant_hits:
            source_path = Path(hit.block.source_path)
            if source_path.exists():
                raw_text = source_path.read_text(encoding="utf-8")
                squashed_raw = " ".join(raw_text.split())
                if hit.block.start_anchor not in squashed_raw or hit.block.end_anchor not in squashed_raw:
                    continue

            if not anchor_terms:
                return True

            haystack = " ".join(
                [
                    hit.block.start_anchor.lower(),
                    hit.block.end_anchor.lower(),
                    hit.block.text.lower(),
                ]
            )
            if all(term in haystack for term in anchor_terms):
                return True
        return False

    def _classify_failure(
        self,
        *,
        case: EvaluationCase,
        retrieval_hit: bool,
        evidence_hit: bool,
        section_hit: bool,
        block_type_hit: bool,
        metadata_hit: bool,
        citation_hit: bool,
        answer_correct: bool,
        country_match_at_1: bool,
        foreign_evidence_present: bool,
        forbidden_document_present: bool,
        mixed_document_violation: bool,
        refusal_correct: bool,
        answer: Answer,
    ) -> tuple[str | None, list[str]]:
        reasons: list[str] = []
        if case.should_refuse:
            if not refusal_correct:
                reasons.append("system answered when it should have refused")
                return "refusal", reasons
            return None, reasons

        if not retrieval_hit:
            reasons.append("expected document was not retrieved")
            return "retrieval", reasons
        if case.expected_section_terms and not section_hit:
            reasons.append("expected section context was not retrieved")
            return "retrieval", reasons
        if case.expected_block_types and not block_type_hit:
            reasons.append("expected block type was not retrieved")
            return "ingestion", reasons
        if case.expected_metadata and not metadata_hit:
            reasons.append("expected block metadata was not retrieved")
            return "ingestion", reasons
        if not evidence_hit:
            reasons.append("retrieved evidence did not contain expected terms")
            return "grounding", reasons
        if forbidden_document_present:
            reasons.append("retrieval included forbidden documents")
            return "geo_precision", reasons
        if self._is_country_case(case) and not country_match_at_1:
            reasons.append("top retrieved result did not match the expected country")
            return "geo_precision", reasons
        if foreign_evidence_present:
            reasons.append("answer evidence included a foreign-country document")
            return "geo_precision", reasons
        if mixed_document_violation:
            reasons.append("answer mixed multiple documents despite a single-country expectation")
            return "geo_precision", reasons
        if self._has_citation_expectation(case) and not citation_hit:
            reasons.append("returned citations did not match the expected source anchor")
            return "citation", reasons
        if not answer_correct:
            reasons.append("answer did not express expected terms")
            if answer.confidence == "low":
                reasons.append("answer confidence remained low")
            return "answer_synthesis", reasons
        return None, reasons

    @staticmethod
    def _accumulate_failure_analysis(
        failure_analysis: dict[str, dict[str, int]],
        result: EvaluationCaseResult,
    ) -> None:
        if result.failure_stage is None:
            return
        stage = result.failure_stage
        failure_analysis["by_stage"][stage] = failure_analysis["by_stage"].get(stage, 0) + 1
        question_type = result.question_type or "unknown"
        failure_analysis["by_question_type"][question_type] = (
            failure_analysis["by_question_type"].get(question_type, 0) + 1
        )
        for document_id in result.expected_document_ids or ["(none)"]:
            failure_analysis["by_document"][document_id] = (
                failure_analysis["by_document"].get(document_id, 0) + 1
            )

    @staticmethod
    def _has_citation_expectation(case: EvaluationCase) -> bool:
        return bool(case.expected_source_paths or case.expected_anchor_terms)

    @staticmethod
    def _markdown_report(summary: EvaluationSummary) -> str:
        lines = [
            "# Evaluation Report",
            "",
            "## Summary",
            "",
            f"- Total cases: {summary.total_cases}",
            f"- Retrieval recall@k: {summary.retrieval_recall_at_k}",
            f"- Evidence hit rate: {summary.evidence_hit_rate}",
            f"- Citation accuracy: {summary.citation_accuracy}",
            f"- Document precision@k: {summary.document_precision_at_k}",
            f"- No-answer precision: {summary.no_answer_precision}",
            f"- Answer correctness: {summary.answer_correctness}",
            f"- Country match@1: {summary.country_match_at_1}",
            f"- Foreign evidence rate: {summary.foreign_evidence_rate}",
            f"- Wrong-country answer rate: {summary.wrong_country_answer_rate}",
            f"- Diversity enforcement rate: {summary.diversity_enforcement_rate}",
            f"- Cached answers: {summary.cached_answer_count}",
            f"- Answer cache hit rate: {summary.answer_cache_hit_rate}",
            "",
            "## Tier Distribution",
            "",
        ]
        if not summary.tier_distribution:
            lines.append("- No routed tiers recorded.")
        else:
            for key, value in sorted(summary.tier_distribution.items()):
                lines.append(f"- {key}: {value}")
        lines.extend(["", "## Segment Metrics", ""])
        if not summary.segment_breakdown:
            lines.append("- No segment metrics recorded.")
        else:
            for key, values in sorted(summary.segment_breakdown.items()):
                lines.append(
                    f"- {key}: {values['rate']} ({values['numerator']}/{values['denominator']})"
                )
        lines.extend(
            [
                "",
            "## Failure Analysis",
            "",
            ]
        )
        for group_name, counts in summary.failure_analysis.items():
            lines.append(f"### {group_name.replace('_', ' ').title()}")
            if not counts:
                lines.append("- No failures recorded.")
            else:
                for key, value in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
                    lines.append(f"- {key}: {value}")
            lines.append("")

        lines.extend(["## Fix Decisions", ""])
        if not summary.fix_decisions:
            lines.append("- No decisions. No clustered failures were recorded.")
        else:
            for stage, decisions in sorted(summary.fix_decisions.items()):
                lines.append(f"### {stage.replace('_', ' ').title()}")
                for decision in decisions:
                    lines.append(f"- {decision}")
                lines.append("")

        lines.extend(["## Case Results", ""])
        for result in summary.results:
            lines.append(f"### {result.question}")
            lines.append(f"- Question type: {result.question_type}")
            if result.expected_iso_code:
                lines.append(f"- Expected ISO: {result.expected_iso_code}")
            lines.append(f"- Retrieved documents: {', '.join(result.retrieved_document_ids) or '(none)'}")
            lines.append(f"- Retrieved sections: {', '.join(result.retrieved_sections) or '(none)'}")
            lines.append(f"- Country match@1: {result.country_match_at_1}")
            lines.append(f"- Foreign evidence present: {result.foreign_evidence_present}")
            lines.append(f"- Confidence: {result.answer_confidence}")
            lines.append(f"- Query intent: {result.query_intent}")
            lines.append(f"- Routed tier: {result.routed_tier}")
            if result.answer_text:
                lines.append(f"- Answer: {result.answer_text}")
            lines.append(f"- Citation hit: {result.citation_hit}")
            lines.append(f"- Answer cached: {result.answer_cached}")
            if result.failure_stage:
                lines.append(f"- Failure stage: {result.failure_stage}")
                if result.failure_reasons:
                    for reason in result.failure_reasons:
                        lines.append(f"- Failure reason: {reason}")
            else:
                lines.append("- Status: passed")
            lines.append("")

        return "\n".join(lines)

    @staticmethod
    def _fix_decisions(
        failure_analysis: dict[str, dict[str, int]],
    ) -> dict[str, list[str]]:
        decisions: dict[str, list[str]] = {}
        stage_counts = failure_analysis.get("by_stage", {})

        if stage_counts.get("retrieval", 0):
            decisions["retrieval"] = [
                "Inspect missed questions for synonym gaps and metadata filters before changing rank fusion.",
                "Add or tighten benchmark cases around the missed document families to verify the regression directly.",
                "Review whether normalization produced the right section labels and row-level blocks for those documents.",
            ]
        if stage_counts.get("grounding", 0):
            decisions["grounding"] = [
                "Check whether the expected answer terms are present in normalized blocks or lost during table flattening.",
                "Prefer improving block structure and informative-row scoring before increasing model complexity.",
                "Spot-check the failing evidence cards in the UI to confirm whether retrieval found the right document but the wrong block.",
            ]
        if stage_counts.get("citation", 0):
            decisions["citation"] = [
                "Audit start and end anchors for the failing blocks and verify the benchmark anchor expectations are still current.",
                "Tighten section-path and anchor selection rules before changing answer synthesis prompts.",
                "Use citation-specific cases to separate source-path mistakes from anchor-localization mistakes.",
            ]
        if stage_counts.get("answer_synthesis", 0):
            decisions["answer_synthesis"] = [
                "Review whether routing should stay in Tier 1 or escalate to Tier 2 for the failing question shapes.",
                "Compare answer text with the top evidence blocks to see whether extraction or formatting dropped required terms.",
                "Add targeted cases for the failing query intents so synthesis regressions are caught before release.",
            ]
        if stage_counts.get("refusal", 0):
            decisions["refusal"] = [
                "Re-run refusal calibration and compare the selected thresholds against the current runtime settings.",
                "Inspect false-answer cases to see whether weak lexical overlap is sneaking past the minimum thresholds.",
                "Keep refusal fixes threshold-driven; do not patch them with one-off question rules.",
            ]
        if failure_analysis.get("by_question_type", {}).get("canonical_mapping_accuracy", 0):
            decisions["canonical_mapping_accuracy"] = [
                "Review the enrichment template to ensure functional equivalents are correctly mapped.",
                "Verify if the programmatic tag normalizer is dropping relevant tags too aggressively.",
                "Add more synonyms to local_aliases during ingestion to bridge the gap between source terms and canonical concepts.",
            ]

        return decisions
