import json
from dataclasses import asdict
from pathlib import Path

from own_knowledge_rag.answering import ExtractiveAnswerer
from own_knowledge_rag.evaluation import Evaluator
from own_knowledge_rag.models import CalibrationCandidate, CalibrationReport, SearchHit


class RefusalCalibrator:
    TARGET_TIER0_1_SHARE = 0.7
    TARGET_TIER2_SHARE = 0.3

    def __init__(self, evaluator: Evaluator) -> None:
        self._evaluator = evaluator

    def calibrate(
        self,
        *,
        cases,
        search,
        top_k: int,
        score_thresholds: list[float] | None = None,
        overlap_thresholds: list[float] | None = None,
        tier0_thresholds: list[float] | None = None,
        tier2_thresholds: list[float] | None = None,
    ) -> CalibrationReport:
        score_thresholds = score_thresholds or [0.12, 0.16, 0.18, 0.22, 0.26, 0.3]
        overlap_thresholds = overlap_thresholds or [0.12, 0.18, 0.24, 0.3, 0.36]
        tier0_thresholds = tier0_thresholds or [0.65, 0.75, 0.85]
        tier2_thresholds = tier2_thresholds or [0.45, 0.55, 0.65]
        candidates: list[CalibrationCandidate] = []

        cached_hits: dict[tuple[str, int], list[SearchHit]] = {}

        for min_score in score_thresholds:
            for min_overlap in overlap_thresholds:
                for tier0_score in tier0_thresholds:
                    for tier2_score in tier2_thresholds:
                        answerer = ExtractiveAnswerer(
                            min_score_threshold=min_score,
                            min_overlap_ratio=min_overlap,
                            tier0_score_threshold=tier0_score,
                            tier2_score_threshold=tier2_score,
                        )

                        def run_case(question: str):
                            cache_key = (question, top_k)
                            hits = cached_hits.get(cache_key)
                            if hits is None:
                                hits = search(question, top_k=top_k)
                                cached_hits[cache_key] = hits
                            answer = answerer.answer(question, hits)
                            return hits, answer

                        summary = self._evaluator.evaluate(cases, run_case)
                        tier0_1_share = self._tier0_1_share(summary.tier_distribution)
                        tier2_share = self._tier_share(summary.tier_distribution, "tier2")
                        refusal_share = self._tier_share(summary.tier_distribution, "refusal")
                        candidates.append(
                            CalibrationCandidate(
                                min_score_threshold=min_score,
                                min_overlap_ratio=min_overlap,
                                tier0_score_threshold=tier0_score,
                                tier2_score_threshold=tier2_score,
                                no_answer_precision=summary.no_answer_precision,
                                answer_correctness=summary.answer_correctness,
                                evidence_hit_rate=summary.evidence_hit_rate,
                                retrieval_recall_at_k=summary.retrieval_recall_at_k,
                                tier0_1_share=tier0_1_share,
                                tier2_share=tier2_share,
                                refusal_share=refusal_share,
                            )
                        )

        ranked = sorted(
            candidates,
            key=lambda item: (
                item.no_answer_precision,
                item.answer_correctness,
                item.evidence_hit_rate,
                item.retrieval_recall_at_k,
                item.tier0_1_share,
                -abs(item.tier0_1_share - 0.7),
                -item.min_overlap_ratio,
                -item.min_score_threshold,
            ),
            reverse=True,
        )
        recommended = ranked[0]
        answerable_cases = len([case for case in cases if not case.should_refuse])
        refusal_cases = len(cases) - answerable_cases
        return CalibrationReport(
            recommended_min_score_threshold=recommended.min_score_threshold,
            recommended_min_overlap_ratio=recommended.min_overlap_ratio,
            recommended_tier0_score_threshold=recommended.tier0_score_threshold,
            recommended_tier2_score_threshold=recommended.tier2_score_threshold,
            total_cases=len(cases),
            answerable_cases=answerable_cases,
            refusal_cases=refusal_cases,
            candidate_count=len(ranked),
            recommended_no_answer_precision=recommended.no_answer_precision,
            recommended_answer_correctness=recommended.answer_correctness,
            recommended_evidence_hit_rate=recommended.evidence_hit_rate,
            recommended_retrieval_recall_at_k=recommended.retrieval_recall_at_k,
            recommended_tier0_1_share=recommended.tier0_1_share,
            recommended_tier2_share=recommended.tier2_share,
            recommended_refusal_share=recommended.refusal_share,
            meets_query_mix_target=(
                recommended.tier0_1_share >= self.TARGET_TIER0_1_SHARE
                and recommended.tier2_share <= self.TARGET_TIER2_SHARE
            ),
            candidates=ranked,
        )

    def save_report(self, report: CalibrationReport, output_path: Path) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(asdict(report), indent=2), encoding="utf-8")
        output_path.with_suffix(".md").write_text(self._markdown_report(report), encoding="utf-8")

    @staticmethod
    def _markdown_report(report: CalibrationReport) -> str:
        query_mix_status = "meets target" if report.meets_query_mix_target else "needs follow-up"
        lines = [
            "# Refusal Calibration Report",
            "",
            "## Phase 5 Readout",
            "",
            f"- Cases evaluated: {report.total_cases}",
            f"- Answerable cases: {report.answerable_cases}",
            f"- Refusal cases: {report.refusal_cases}",
            f"- Candidate combinations swept: {report.candidate_count}",
            f"- Query mix status: {query_mix_status}",
            "",
            "## Selected Thresholds",
            "",
            f"- Selected min score threshold: {report.recommended_min_score_threshold}",
            f"- Selected min overlap ratio: {report.recommended_min_overlap_ratio}",
            f"- Selected tier0 score threshold: {report.recommended_tier0_score_threshold}",
            f"- Selected tier2 score threshold: {report.recommended_tier2_score_threshold}",
            "",
            "## Selected Candidate Metrics",
            "",
            f"- No-answer precision: {report.recommended_no_answer_precision}",
            f"- Answer correctness: {report.recommended_answer_correctness}",
            f"- Evidence hit rate: {report.recommended_evidence_hit_rate}",
            f"- Retrieval recall@k: {report.recommended_retrieval_recall_at_k}",
            f"- Tier0/1 share: {report.recommended_tier0_1_share}",
            f"- Tier2 share: {report.recommended_tier2_share}",
            f"- Refusal share: {report.recommended_refusal_share}",
            "",
            "## Candidates",
            "",
            "| Min score | Min overlap | Tier0 score | Tier2 score | No-answer precision | Answer correctness | Evidence hit rate | Recall@k | Tier0/1 share | Tier2 share | Refusal share |",
            "|---|---|---|---|---|---|---|---|---|---|---|",
        ]
        for candidate in report.candidates:
            lines.append(
                "| "
                f"{candidate.min_score_threshold} | "
                f"{candidate.min_overlap_ratio} | "
                f"{candidate.tier0_score_threshold} | "
                f"{candidate.tier2_score_threshold} | "
                f"{candidate.no_answer_precision} | "
                f"{candidate.answer_correctness} | "
                f"{candidate.evidence_hit_rate} | "
                f"{candidate.retrieval_recall_at_k} | "
                f"{candidate.tier0_1_share} | "
                f"{candidate.tier2_share} | "
                f"{candidate.refusal_share} |"
            )
        return "\n".join(lines)

    @staticmethod
    def _tier0_1_share(tier_distribution: dict[str, int]) -> float:
        total = sum(tier_distribution.values())
        if total <= 0:
            return 0.0
        return round((tier_distribution.get("tier0", 0) + tier_distribution.get("tier1", 0)) / total, 4)

    @staticmethod
    def _tier_share(tier_distribution: dict[str, int], tier: str) -> float:
        total = sum(tier_distribution.values())
        if total <= 0:
            return 0.0
        return round(tier_distribution.get(tier, 0) / total, 4)
