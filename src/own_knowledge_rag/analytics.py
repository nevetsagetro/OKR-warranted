import json
import logging
from collections import Counter
from pathlib import Path
from dataclasses import dataclass, field

from own_knowledge_rag.enrichment import EnrichmentResult
from own_knowledge_rag.models import KnowledgeBlock

logger = logging.getLogger(__name__)

GLOBAL_CONSISTENCY_KEYS = {
    "locale name",
    "dialing code",
    "country code",
    "mcc",
    "mnc",
    "two way sms supported",
    "number portability available",
}

SECTION_SCOPED_KEYS = {
    "twilio supported",
    "sender id preserved",
    "provisioning time",
    "best practices",
    "use case restrictions",
    "service restrictions",
}

@dataclass
class QualityMetrics:
    source_artifact: str = "blocks"
    total_blocks: int = 0
    blocks_with_enriched_text: int = 0
    blocks_with_questions: int = 0
    blocks_with_tags: int = 0
    avg_questions_per_block: float = 0.0
    tag_distribution: dict[str, int] = field(default_factory=dict)
    block_type_distribution: dict[str, int] = field(default_factory=dict)
    answer_signal_distribution: dict[str, int] = field(default_factory=dict)
    average_reasoning_length: float = 0.0
    quality_status_counts: dict[str, int] = field(default_factory=dict)
    avg_enriched_text_length: float = 0.0
    question_coverage: float = 0.0
    tag_coverage: float = 0.0
    low_quality_blocks: int = 0
    low_quality_rate: float = 0.0
    inconsistent_tag_groups: dict[str, list[str]] = field(default_factory=dict)


@dataclass
class ConsistencyFinding:
    document_id: str
    country: str
    iso_code: str
    normalized_key: str
    sections: list[str]
    normalized_values: list[str]
    block_ids: list[str]
    severity: str


@dataclass
class ConsistencyReport:
    total_documents: int = 0
    documents_with_findings: int = 0
    total_findings: int = 0
    findings: list[ConsistencyFinding] = field(default_factory=list)


@dataclass
class ReviewPacket:
    document_id: str
    title: str
    country: str
    iso_code: str
    total_blocks: int
    low_quality_blocks: int
    rejected_blocks: int
    sections: list[str] = field(default_factory=list)
    top_tags: list[tuple[str, int]] = field(default_factory=list)
    top_block_types: list[tuple[str, int]] = field(default_factory=list)
    consistency_findings: list[ConsistencyFinding] = field(default_factory=list)
    sample_blocks: list[KnowledgeBlock] = field(default_factory=list)


@dataclass
class ReviewPacketReport:
    total_documents: int = 0
    packet_paths: list[str] = field(default_factory=list)

class KnowledgeAnalytics:
    def __init__(self, work_dir: Path):
        self.work_dir = work_dir
        self.blocks_path = work_dir / "blocks.json"
        self.enrichment_cache_path = work_dir / "enrichment-cache.json"

    def audit_quality(self) -> QualityMetrics:
        """Performs a statistical audit of the indexed knowledge base."""
        if self.blocks_path.exists():
            blocks_raw = json.loads(self.blocks_path.read_text(encoding="utf-8"))
            blocks = [KnowledgeBlock(**b) for b in blocks_raw]
            return self._audit_blocks(blocks)
        if self.enrichment_cache_path.exists():
            payload = json.loads(self.enrichment_cache_path.read_text(encoding="utf-8"))
            cache_results = [EnrichmentResult.model_validate(item) for item in payload.values()]
            return self._audit_cache_results(cache_results)
        raise FileNotFoundError(
            f"Neither blocks nor enrichment cache found in {self.work_dir}"
        )

    def audit_cross_section_consistency(self) -> ConsistencyReport:
        if not self.blocks_path.exists():
            raise FileNotFoundError(f"Indexed blocks not found in {self.work_dir}")

        blocks_raw = json.loads(self.blocks_path.read_text(encoding="utf-8"))
        blocks = [KnowledgeBlock(**b) for b in blocks_raw]
        profile_blocks = [
            block
            for block in blocks
            if block.metadata.get("document_scope") == "profile" and block.metadata.get("row_key")
        ]
        by_document: dict[str, list[KnowledgeBlock]] = {}
        for block in profile_blocks:
            by_document.setdefault(block.document_id, []).append(block)

        findings: list[ConsistencyFinding] = []
        for document_id, document_blocks in by_document.items():
            findings.extend(self._document_consistency_findings(document_id, document_blocks))

        return ConsistencyReport(
            total_documents=len(by_document),
            documents_with_findings=len({finding.document_id for finding in findings}),
            total_findings=len(findings),
            findings=findings,
        )

    def build_review_packets(self, document_id: str | None = None) -> ReviewPacketReport:
        if not self.blocks_path.exists():
            raise FileNotFoundError(f"Indexed blocks not found in {self.work_dir}")

        blocks_raw = json.loads(self.blocks_path.read_text(encoding="utf-8"))
        blocks = [KnowledgeBlock(**b) for b in blocks_raw]
        by_document: dict[str, list[KnowledgeBlock]] = {}
        for block in blocks:
            by_document.setdefault(block.document_id, []).append(block)

        consistency_report = self.audit_cross_section_consistency()
        findings_by_document: dict[str, list[ConsistencyFinding]] = {}
        for finding in consistency_report.findings:
            findings_by_document.setdefault(finding.document_id, []).append(finding)

        output_dir = self.work_dir / "analytics" / "review_packets"
        output_dir.mkdir(parents=True, exist_ok=True)

        packet_paths: list[str] = []
        selected_documents = [document_id] if document_id else sorted(by_document)
        for current_document_id in selected_documents:
            document_blocks = by_document.get(current_document_id, [])
            if not document_blocks:
                continue
            packet = self._build_review_packet(
                current_document_id,
                document_blocks,
                findings_by_document.get(current_document_id, []),
            )
            packet_path = output_dir / f"{current_document_id}.md"
            packet_path.write_text(self._review_packet_markdown(packet), encoding="utf-8")
            packet_paths.append(str(packet_path))

        index_path = output_dir / "index.json"
        index_path.write_text(json.dumps({"packet_paths": packet_paths}, indent=2), encoding="utf-8")
        return ReviewPacketReport(total_documents=len(packet_paths), packet_paths=packet_paths)

    def _audit_blocks(self, blocks: list[KnowledgeBlock]) -> QualityMetrics:
        metrics = QualityMetrics(total_blocks=len(blocks), source_artifact="blocks")
        return self._populate_metrics(
            metrics=metrics,
            items=blocks,
            get_tags=lambda b: b.sender_types + b.regulation_topics + b.canonical_terms,
            get_quality_status=lambda b: b.quality_status,
            get_block_type=lambda b: b.block_type,
            get_answer_signal=lambda b: b.answer_signal or "none",
            get_enriched_text=lambda b: b.enriched_text,
            get_questions=lambda b: b.hypothetical_questions,
            get_reasoning=lambda b: b.reasoning,
        )

    def _audit_cache_results(self, items: list[EnrichmentResult]) -> QualityMetrics:
        metrics = QualityMetrics(total_blocks=len(items), source_artifact="enrichment-cache")
        return self._populate_metrics(
            metrics=metrics,
            items=items,
            get_tags=lambda r: r.sender_types + r.regulation_topics,
            get_quality_status=lambda _r: "unknown",
            get_block_type=lambda _r: "unknown",
            get_answer_signal=lambda r: r.answer_signal or "none",
            get_enriched_text=lambda r: r.enriched_text,
            get_questions=lambda r: r.hypothetical_questions,
            get_reasoning=lambda r: r.reasoning,
        )

    @staticmethod
    def _populate_metrics(
        *,
        metrics: QualityMetrics,
        items: list,
        get_tags,
        get_quality_status,
        get_block_type,
        get_answer_signal,
        get_enriched_text,
        get_questions,
        get_reasoning,
    ) -> QualityMetrics:
        tag_counts = Counter()
        type_counts = Counter()
        signal_counts = Counter()
        status_counts = Counter()

        total_questions = 0
        total_reasoning_len = 0
        total_enriched_len = 0
        normalized_tag_variants: dict[str, Counter] = {}

        for item in items:
            type_counts[get_block_type(item)] += 1
            status_counts[get_quality_status(item)] += 1
            signal_counts[get_answer_signal(item)] += 1

            enriched_text = get_enriched_text(item)
            if enriched_text:
                metrics.blocks_with_enriched_text += 1
                total_enriched_len += len(enriched_text)

            questions = get_questions(item)
            if questions:
                metrics.blocks_with_questions += 1
                total_questions += len(questions)

            all_tags = get_tags(item)
            if all_tags:
                metrics.blocks_with_tags += 1
                for tag in all_tags:
                    tag_counts[tag] += 1
                    normalized = KnowledgeAnalytics._normalize_tag(tag)
                    variants = normalized_tag_variants.setdefault(normalized, Counter())
                    variants[tag] += 1

            reasoning = get_reasoning(item)
            if reasoning:
                total_reasoning_len += len(reasoning)

        metrics.avg_questions_per_block = round(total_questions / max(1, len(items)), 2)
        metrics.average_reasoning_length = round(total_reasoning_len / max(1, len(items)), 2)
        metrics.avg_enriched_text_length = round(total_enriched_len / max(1, len(items)), 2)
        metrics.question_coverage = round(metrics.blocks_with_questions / max(1, len(items)), 4)
        metrics.tag_coverage = round(metrics.blocks_with_tags / max(1, len(items)), 4)
        metrics.tag_distribution = dict(tag_counts.most_common(20))
        metrics.block_type_distribution = dict(type_counts)
        metrics.answer_signal_distribution = dict(signal_counts)
        metrics.quality_status_counts = dict(status_counts)
        metrics.low_quality_blocks = status_counts.get("LOW_QUALITY", 0) + status_counts.get("low_quality", 0)
        metrics.low_quality_rate = round(metrics.low_quality_blocks / max(1, len(items)), 4)
        metrics.inconsistent_tag_groups = {
            normalized: [variant for variant, _count in variants.most_common()]
            for normalized, variants in sorted(
                normalized_tag_variants.items(),
                key=lambda entry: sum(entry[1].values()),
                reverse=True,
            )
            if len(variants) > 1
        }
        return metrics

    @staticmethod
    def _normalize_tag(tag: str) -> str:
        return " ".join(tag.replace("_", " ").replace("-", " ").lower().split())

    def _build_review_packet(
        self,
        document_id: str,
        blocks: list[KnowledgeBlock],
        consistency_findings: list[ConsistencyFinding],
    ) -> ReviewPacket:
        first = blocks[0]
        tag_counter: Counter = Counter()
        block_type_counter: Counter = Counter()
        sections: set[str] = set()
        low_quality_blocks = 0
        rejected_blocks = 0

        for block in blocks:
            sections.add(" > ".join(block.section_path) or "(root)")
            block_type_counter[block.block_type] += 1
            for tag in block.sender_types + block.regulation_topics + block.canonical_terms:
                tag_counter[tag] += 1
            if block.quality_status == "LOW_QUALITY":
                low_quality_blocks += 1
            if block.quality_status == "REJECTED":
                rejected_blocks += 1

        sample_blocks = sorted(
            blocks,
            key=lambda block: (
                block.quality_status != "ok",
                block.block_type != "table_fact",
                -len(block.enriched_text or block.text),
            ),
        )[:5]

        return ReviewPacket(
            document_id=document_id,
            title=first.title,
            country=first.country,
            iso_code=first.iso_code,
            total_blocks=len(blocks),
            low_quality_blocks=low_quality_blocks,
            rejected_blocks=rejected_blocks,
            sections=sorted(sections),
            top_tags=tag_counter.most_common(10),
            top_block_types=block_type_counter.most_common(10),
            consistency_findings=consistency_findings,
            sample_blocks=sample_blocks,
        )

    def _review_packet_markdown(self, packet: ReviewPacket) -> str:
        lines = [
            f"# Review Packet: {packet.document_id}",
            "",
            "## Summary",
            f"- Title: {packet.title}",
            f"- Country: {packet.country or '(unknown)'}",
            f"- ISO code: {packet.iso_code or '(unknown)'}",
            f"- Total blocks: {packet.total_blocks}",
            f"- Low-quality blocks: {packet.low_quality_blocks}",
            f"- Rejected blocks: {packet.rejected_blocks}",
            f"- Sections: {len(packet.sections)}",
            "",
            "## Top Block Types",
        ]
        for block_type, count in packet.top_block_types:
            lines.append(f"- {block_type}: {count}")

        lines.extend(["", "## Top Tags"])
        if packet.top_tags:
            for tag, count in packet.top_tags:
                lines.append(f"- {tag}: {count}")
        else:
            lines.append("- No dominant tags recorded.")

        lines.extend(["", "## Consistency Findings"])
        if packet.consistency_findings:
            for finding in packet.consistency_findings:
                lines.append(
                    f"- [{finding.severity}] `{finding.normalized_key}` across "
                    f"{'; '.join(finding.sections)} -> {', '.join(finding.normalized_values)}"
                )
        else:
            lines.append("- No cross-section conflicts detected for this document.")

        lines.extend(["", "## Sample Blocks"])
        for block in packet.sample_blocks:
            lines.extend(
                [
                    f"### {block.block_id}",
                    f"- Section: {' > '.join(block.section_path) or '(root)'}",
                    f"- Type: {block.block_type}",
                    f"- Quality: {block.quality_status}",
                    f"- Answer signal: {block.answer_signal or '(none)'}",
                    f"- Enriched text: {block.enriched_text or '(empty)'}",
                    f"- Raw text: {block.text}",
                    "",
                ]
            )

        return "\n".join(lines).rstrip() + "\n"

    def _document_consistency_findings(
        self,
        document_id: str,
        blocks: list[KnowledgeBlock],
    ) -> list[ConsistencyFinding]:
        grouped: dict[str, list[KnowledgeBlock]] = {}
        for block in blocks:
            normalized_key = self._normalize_tag(block.metadata.get("row_key", ""))
            if not normalized_key:
                continue
            grouped.setdefault(normalized_key, []).append(block)

        findings: list[ConsistencyFinding] = []
        for normalized_key, candidate_blocks in grouped.items():
            sections = {
                " > ".join(block.section_path) or "(root)"
                for block in candidate_blocks
            }
            if len(sections) < 2:
                continue
            if normalized_key in SECTION_SCOPED_KEYS:
                continue

            value_map: dict[str, list[KnowledgeBlock]] = {}
            for block in candidate_blocks:
                normalized_value = self._normalized_consistency_value(block)
                if not normalized_value:
                    continue
                value_map.setdefault(normalized_value, []).append(block)

            if len(value_map) < 2:
                continue
            if not self._is_global_conflict_candidate(normalized_key, value_map):
                continue

            sample_block = candidate_blocks[0]
            findings.append(
                ConsistencyFinding(
                    document_id=document_id,
                    country=sample_block.country,
                    iso_code=sample_block.iso_code,
                    normalized_key=normalized_key,
                    sections=sorted(sections),
                    normalized_values=sorted(value_map.keys()),
                    block_ids=[block.block_id for block in candidate_blocks],
                    severity="high" if normalized_key in GLOBAL_CONSISTENCY_KEYS else "medium",
                )
            )
        return findings

    def _normalized_consistency_value(self, block: KnowledgeBlock) -> str:
        raw_value = block.metadata.get("row_values", "") or block.text
        lower_raw = raw_value.lower()

        structured_bits: list[str] = []
        for part in raw_value.split(";"):
            cleaned = part.strip()
            if not cleaned:
                continue
            if "=" in cleaned:
                key, value = cleaned.split("=", 1)
            elif ":" in cleaned:
                key, value = cleaned.split(":", 1)
            else:
                key, value = "_value", cleaned
            normalized_key = self._normalize_tag(key)
            normalized_value = self._normalize_value_token(value)
            if not normalized_value or normalized_key == "description":
                continue
            structured_bits.append(f"{normalized_key}={normalized_value}")

        if structured_bits:
            return " | ".join(sorted(set(structured_bits)))

        return self._normalize_value_token(lower_raw)

    def _is_global_conflict_candidate(
        self,
        normalized_key: str,
        value_map: dict[str, list[KnowledgeBlock]],
    ) -> bool:
        if normalized_key in GLOBAL_CONSISTENCY_KEYS:
            return True
        boolish_values = {
            value
            for value in value_map
            if any(token in value for token in ("yes", "no", "supported", "not supported", "required", "not required"))
        }
        return len(boolish_values) >= 2

    def _normalize_value_token(self, value: str) -> str:
        normalized = self._normalize_tag(value)
        replacements = {
            "supported learn more": "supported",
            "not supported learn more": "not supported",
            "n a": "",
            "na": "",
            "---": "",
        }
        normalized = replacements.get(normalized, normalized)
        for source, target in {
            "true": "yes",
            "false": "no",
            "not available": "not supported",
            "unsupported": "not supported",
            "not supported": "not supported",
            "support": "supported",
        }.items():
            if normalized == source:
                normalized = target
        return normalized.strip()

    def analyze_retrieval_baseline(self, retriever, queries: list[str], top_k: int = 5) -> dict:
        """
        Runs a baseline comparison of retrieval modes.
        Useful for a Data Scientist to prove why Hybrid is better than BM25.
        """
        results = {
            "lexical_only": [],
            "vector_only": [],
            "hybrid": []
        }
        
        for q in queries:
            # Simulate different modes if the retriever supports it, 
            # or just use the scores from a single hybrid hit list.
            hits = retriever.search(q, top_k=top_k)
            
            lexical_scores = [h.lexical_score for h in hits]
            vector_scores = [h.vector_score for h in hits]
            hybrid_scores = [h.score for h in hits]
            
            results["lexical_only"].append(sum(lexical_scores) / max(1, len(lexical_scores)))
            results["vector_only"].append(sum(vector_scores) / max(1, len(vector_scores)))
            results["hybrid"].append(sum(hybrid_scores) / max(1, len(hybrid_scores)))
            
        return {
            "avg_score_boost": {
                "hybrid_vs_lexical": round(sum(results["hybrid"]) / max(1, sum(results["lexical_only"])) - 1, 3),
                "hybrid_vs_vector": round(sum(results["hybrid"]) / max(1, sum(results["vector_only"])) - 1, 3),
            },
            "raw_samples": results
        }

def generate_ds_report(metrics: QualityMetrics, work_dir: Path):
    report_path = work_dir / "analytics" / "knowledge_quality_report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    lines = [
        "# Data Science Knowledge Audit",
        f"Generated from: {work_dir}",
        f"Source artifact: {metrics.source_artifact}",
        "",
        "## Corpus Statistics",
        f"- **Total Blocks**: {metrics.total_blocks}",
        f"- **Enrichment Coverage**: {round(metrics.blocks_with_enriched_text / max(1, metrics.total_blocks) * 100, 1)}%",
        f"- **Question Coverage**: {round(metrics.question_coverage * 100, 1)}%",
        f"- **Tag Coverage**: {round(metrics.tag_coverage * 100, 1)}%",
        f"- **Question Density**: {metrics.avg_questions_per_block} questions/block",
        f"- **Avg enriched text length**: {metrics.avg_enriched_text_length} chars",
        f"- **Avg reasoning depth**: {metrics.average_reasoning_length} chars",
    ]
    if metrics.low_quality_blocks:
        lines.append(
            f"- **Low-quality blocks**: {metrics.low_quality_blocks} ({round(metrics.low_quality_rate * 100, 1)}%)"
        )
    lines.extend([
        "",
        "## Semantic Distribution",
        "### Block Types",
    ])
    for k, v in metrics.block_type_distribution.items():
        lines.append(f"- {k}: {v}")
    
    lines.extend([
        "",
        "### Top Canonical Tags",
    ])
    for k, v in metrics.tag_distribution.items():
        lines.append(f"- {k}: {v}")
        
    lines.extend([
        "",
        "### Answer Signals",
    ])
    for k, v in metrics.answer_signal_distribution.items():
        lines.append(f"- {k}: {v}")

    if metrics.inconsistent_tag_groups:
        lines.extend([
            "",
            "## Tag Consistency Watchlist",
        ])
        for normalized, variants in list(metrics.inconsistent_tag_groups.items())[:10]:
            lines.append(f"- {normalized}: {', '.join(variants)}")

    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def generate_consistency_report(report: ConsistencyReport, work_dir: Path) -> Path:
    output_dir = work_dir / "analytics"
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "cross_section_consistency_report.json"
    json_path.write_text(
        json.dumps(
            {
                "total_documents": report.total_documents,
                "documents_with_findings": report.documents_with_findings,
                "total_findings": report.total_findings,
                "findings": [
                    {
                        "document_id": finding.document_id,
                        "country": finding.country,
                        "iso_code": finding.iso_code,
                        "normalized_key": finding.normalized_key,
                        "sections": finding.sections,
                        "normalized_values": finding.normalized_values,
                        "block_ids": finding.block_ids,
                        "severity": finding.severity,
                    }
                    for finding in report.findings
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    markdown_path = output_dir / "cross_section_consistency_report.md"
    lines = [
        "# Cross-Section Consistency Report",
        f"Generated from: {work_dir}",
        "",
        "## Summary",
        f"- Documents analyzed: {report.total_documents}",
        f"- Documents with findings: {report.documents_with_findings}",
        f"- Total findings: {report.total_findings}",
    ]
    if not report.findings:
        lines.extend(["", "No conflicting repeated facts were detected across locale sections."])
    else:
        lines.extend(["", "## Findings"])
        for finding in report.findings:
            sections = "; ".join(finding.sections)
            values = "; ".join(finding.normalized_values)
            lines.append(
                f"- [{finding.severity}] {finding.document_id} `{finding.normalized_key}` "
                f"appears inconsistent across sections: {sections}. Values: {values}"
            )

    markdown_path.write_text("\n".join(lines), encoding="utf-8")
    return markdown_path


def seed_review_findings(report: ConsistencyReport, work_dir: Path) -> Path:
    output_dir = work_dir / "analytics"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "review_findings.json"
    payload = {
        "generated_from": str(output_dir / "cross_section_consistency_report.json"),
        "entries": [
            {
                "finding_id": f"{finding.document_id}::{finding.normalized_key}",
                "document_id": finding.document_id,
                "country": finding.country,
                "iso_code": finding.iso_code,
                "normalized_key": finding.normalized_key,
                "sections": finding.sections,
                "observed_values": finding.normalized_values,
                "severity": finding.severity,
                "review_status": "pending",
                "resolution_value": "",
                "notes": "",
            }
            for finding in report.findings
        ],
    }
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return output_path


def query_reviews_path(work_dir: Path) -> Path:
    return work_dir / "analytics" / "query_reviews.json"


def record_query_review(work_dir: Path, entry: dict[str, object]) -> Path:
    output_path = query_reviews_path(work_dir)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.exists():
        payload = json.loads(output_path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            payload = {}
    else:
        payload = {}

    reviews = payload.get("entries", [])
    if not isinstance(reviews, list):
        reviews = []

    review_id = f"review-{len(reviews) + 1:05d}"
    stored_entry = {"review_id": review_id, **entry}
    reviews.append(stored_entry)
    payload["entries"] = reviews
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return output_path
