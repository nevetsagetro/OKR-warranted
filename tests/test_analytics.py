import json
from pathlib import Path

from own_knowledge_rag.analytics import (
    KnowledgeAnalytics,
    generate_consistency_report,
    query_reviews_path,
    record_query_review,
    seed_review_findings,
)


def test_audit_quality_falls_back_to_enrichment_cache(tmp_path: Path) -> None:
    payload = {
        "k1": {
            "block_id": "b1",
            "reasoning": "",
            "country": "Spain",
            "iso_code": "ES",
            "sender_types": ["short code"],
            "regulation_topics": ["provisioning time"],
            "answer_signal": "standalone_fact",
            "hypothetical_questions": ["How long does short code provisioning take in Spain?"],
            "enriched_text": "In Spain, short code provisioning takes 12-14 weeks.",
            "local_aliases": [],
        },
        "k2": {
            "block_id": "b2",
            "reasoning": "",
            "country": "Spain",
            "iso_code": "ES",
            "sender_types": [],
            "regulation_topics": [],
            "answer_signal": "context_dependent",
            "hypothetical_questions": [],
            "enriched_text": "Messages to landlines fail.",
            "local_aliases": [],
        },
    }
    (tmp_path / "enrichment-cache.json").write_text(json.dumps(payload), encoding="utf-8")

    metrics = KnowledgeAnalytics(tmp_path).audit_quality()

    assert metrics.source_artifact == "enrichment-cache"
    assert metrics.total_blocks == 2
    assert metrics.blocks_with_enriched_text == 2
    assert metrics.blocks_with_questions == 1
    assert metrics.blocks_with_tags == 1
    assert metrics.question_coverage == 0.5
    assert metrics.tag_coverage == 0.5


def test_audit_quality_surfaces_tag_inconsistencies(tmp_path: Path) -> None:
    payload = {
        "k1": {
            "block_id": "b1",
            "reasoning": "",
            "country": "Spain",
            "iso_code": "ES",
            "sender_types": ["Short Code"],
            "regulation_topics": ["provisioning time"],
            "answer_signal": "standalone_fact",
            "hypothetical_questions": [],
            "enriched_text": "Short code is supported.",
            "local_aliases": [],
        },
        "k2": {
            "block_id": "b2",
            "reasoning": "",
            "country": "Spain",
            "iso_code": "ES",
            "sender_types": ["short_code"],
            "regulation_topics": [],
            "answer_signal": "standalone_fact",
            "hypothetical_questions": [],
            "enriched_text": "Short code requires registration.",
            "local_aliases": [],
        },
    }
    (tmp_path / "enrichment-cache.json").write_text(json.dumps(payload), encoding="utf-8")

    metrics = KnowledgeAnalytics(tmp_path).audit_quality()

    assert metrics.inconsistent_tag_groups["short code"] == ["Short Code", "short_code"]


def test_cross_section_consistency_flags_conflicting_global_fact(tmp_path: Path) -> None:
    blocks = [
        {
            "block_id": "spain_es-block-1",
            "document_id": "spain_es",
            "title": "Spain (ES)",
            "section_path": ["Spain (ES)", "Locale Summary"],
            "section_heading": "Locale Summary",
            "block_type": "table_fact",
            "text": "For Locale Summary, the Two-way SMS supported is: Yes.",
            "source_path": "data/raw/spain_es.md",
            "start_anchor": "Two-way SMS supported",
            "end_anchor": "Yes",
            "country": "Spain",
            "iso_code": "ES",
            "metadata": {
                "document_scope": "profile",
                "row_key": "Two-way SMS supported",
                "row_values": "Value=Yes",
            },
        },
        {
            "block_id": "spain_es-block-2",
            "document_id": "spain_es",
            "title": "Spain (ES)",
            "section_path": ["Spain (ES)", "Guidelines"],
            "section_heading": "Guidelines",
            "block_type": "table_fact",
            "text": "For Guidelines, the Two-way SMS supported is: No.",
            "source_path": "data/raw/spain_es.md",
            "start_anchor": "Two-way SMS supported",
            "end_anchor": "No",
            "country": "Spain",
            "iso_code": "ES",
            "metadata": {
                "document_scope": "profile",
                "row_key": "Two-way SMS supported",
                "row_values": "Value=No",
            },
        },
    ]
    (tmp_path / "blocks.json").write_text(json.dumps(blocks), encoding="utf-8")

    report = KnowledgeAnalytics(tmp_path).audit_cross_section_consistency()

    assert report.total_findings == 1
    assert report.findings[0].normalized_key == "two way sms supported"
    assert report.findings[0].severity == "high"
    markdown_path = generate_consistency_report(report, tmp_path)
    assert markdown_path.exists()


def test_build_review_packets_writes_locale_packet(tmp_path: Path) -> None:
    blocks = [
        {
            "block_id": "spain_es-block-1",
            "document_id": "spain_es",
            "title": "Spain (ES)",
            "section_path": ["Spain (ES)", "Locale Summary"],
            "section_heading": "Locale Summary",
            "block_type": "table_fact",
            "text": "For Locale Summary, the Dialing code is: +34.",
            "source_path": "data/raw/spain_es.md",
            "start_anchor": "Dialing code",
            "end_anchor": "+34",
            "country": "Spain",
            "iso_code": "ES",
            "sender_types": ["short code"],
            "regulation_topics": ["provisioning time"],
            "canonical_terms": ["short code"],
            "answer_signal": "standalone_fact",
            "enriched_text": "Spain uses dialing code +34.",
            "quality_status": "ok",
            "metadata": {
                "document_scope": "profile",
                "row_key": "Dialing code",
                "row_values": "Value=+34",
            },
        },
        {
            "block_id": "spain_es-block-2",
            "document_id": "spain_es",
            "title": "Spain (ES)",
            "section_path": ["Spain (ES)", "Guidelines"],
            "section_heading": "Guidelines",
            "block_type": "table_fact",
            "text": "For Guidelines, the Two-way SMS supported is: Yes.",
            "source_path": "data/raw/spain_es.md",
            "start_anchor": "Two-way SMS supported",
            "end_anchor": "Yes",
            "country": "Spain",
            "iso_code": "ES",
            "sender_types": ["short code"],
            "regulation_topics": [],
            "canonical_terms": [],
            "answer_signal": "standalone_fact",
            "enriched_text": "Spain supports two-way SMS.",
            "quality_status": "LOW_QUALITY",
            "metadata": {
                "document_scope": "profile",
                "row_key": "Two-way SMS supported",
                "row_values": "Value=Yes",
            },
        },
    ]
    (tmp_path / "blocks.json").write_text(json.dumps(blocks), encoding="utf-8")

    report = KnowledgeAnalytics(tmp_path).build_review_packets(document_id="spain_es")

    assert report.total_documents == 1
    packet_path = Path(report.packet_paths[0])
    assert packet_path.exists()
    packet_text = packet_path.read_text(encoding="utf-8")
    assert "Review Packet: spain_es" in packet_text
    assert "Top Tags" in packet_text
    assert "Sample Blocks" in packet_text


def test_seed_review_findings_writes_template(tmp_path: Path) -> None:
    blocks = [
        {
            "block_id": "spain_es-block-1",
            "document_id": "spain_es",
            "title": "Spain (ES)",
            "section_path": ["Spain (ES)", "Locale Summary"],
            "section_heading": "Locale Summary",
            "block_type": "table_fact",
            "text": "For Locale Summary, the Two-way SMS supported is: Yes.",
            "source_path": "data/raw/spain_es.md",
            "start_anchor": "Two-way SMS supported",
            "end_anchor": "Yes",
            "country": "Spain",
            "iso_code": "ES",
            "metadata": {
                "document_scope": "profile",
                "row_key": "Two-way SMS supported",
                "row_values": "Value=Yes",
            },
        },
        {
            "block_id": "spain_es-block-2",
            "document_id": "spain_es",
            "title": "Spain (ES)",
            "section_path": ["Spain (ES)", "Guidelines"],
            "section_heading": "Guidelines",
            "block_type": "table_fact",
            "text": "For Guidelines, the Two-way SMS supported is: No.",
            "source_path": "data/raw/spain_es.md",
            "start_anchor": "Two-way SMS supported",
            "end_anchor": "No",
            "country": "Spain",
            "iso_code": "ES",
            "metadata": {
                "document_scope": "profile",
                "row_key": "Two-way SMS supported",
                "row_values": "Value=No",
            },
        },
    ]
    (tmp_path / "blocks.json").write_text(json.dumps(blocks), encoding="utf-8")

    consistency_report = KnowledgeAnalytics(tmp_path).audit_cross_section_consistency()
    output_path = seed_review_findings(consistency_report, tmp_path)

    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["entries"][0]["review_status"] == "pending"
    assert payload["entries"][0]["finding_id"] == "spain_es::two way sms supported"


def test_record_query_review_appends_entries(tmp_path: Path) -> None:
    output_path = record_query_review(
        tmp_path,
        {
            "question": "Sender in Colombia?",
            "answer": "For Colombia, the Sender availability is: Short Code.",
            "rating": "correct_with_foreign_evidence",
            "expected_document_id": "colombia_co",
            "expected_iso_code": "CO",
            "expected_terms": ["sender", "short code"],
            "notes": "Angola appeared in evidence.",
            "evidence_document_ids": ["colombia_co", "angola_ao"],
            "evidence_block_ids": ["colombia-block", "angola-block"],
        },
    )
    record_query_review(
        tmp_path,
        {
            "question": "Should this refuse?",
            "answer": "Insufficient evidence in the indexed knowledge base.",
            "rating": "should_refuse",
            "expected_document_id": "",
            "expected_iso_code": "",
            "expected_terms": [],
            "notes": "",
            "evidence_document_ids": [],
            "evidence_block_ids": [],
        },
    )

    assert output_path == query_reviews_path(tmp_path)
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert len(payload["entries"]) == 2
    assert payload["entries"][0]["review_id"] == "review-00001"
    assert payload["entries"][1]["review_id"] == "review-00002"
