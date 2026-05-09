import json
from pathlib import Path

from own_knowledge_rag.config import Settings
from own_knowledge_rag.evaluation import Evaluator
from own_knowledge_rag.models import Answer, EvaluationCase, KnowledgeBlock, SearchHit
from own_knowledge_rag.pipeline import KnowledgePipeline


def test_pipeline_evaluation_writes_summary_and_scores_cases(tmp_path: Path) -> None:
    source_dir = tmp_path / "raw"
    work_dir = tmp_path / "work"
    source_dir.mkdir(parents=True, exist_ok=True)

    (source_dir / "spain_es.md").write_text(
        """# Spain (ES)

## Sender
| Key | Value |
| --- | --- |
| Sender provisioning | No sender registration needed. |
| Two-way | Supported |
""",
        encoding="utf-8",
    )
    (source_dir / "general_policy.md").write_text(
        """# General Policy

Support agents must use approved documentation.
""",
        encoding="utf-8",
    )

    benchmark_path = tmp_path / "benchmark.json"
    benchmark_path.write_text(
        json.dumps(
            [
                {
                    "question": "Sender in Spain?",
                    "expected_document_ids": ["spain_es"],
                    "expected_source_paths": [str(source_dir / "spain_es.md")],
                    "expected_terms": ["sender provisioning", "no sender registration needed"],
                    "expected_section_terms": ["sender"],
                    "expected_anchor_terms": ["sender provisioning", "no sender registration needed"],
                    "question_type": "factoid",
                    "should_refuse": False,
                },
                {
                    "question": "What is the moon made of in this corpus?",
                    "expected_document_ids": [],
                    "expected_terms": [],
                    "question_type": "refusal",
                    "should_refuse": True,
                },
            ],
            indent=2,
        ),
        encoding="utf-8",
    )

    pipeline = KnowledgePipeline(
        Settings(
            OKR_SOURCE_DIR=source_dir,
            OKR_WORK_DIR=work_dir,
        )
    )
    pipeline.build_index(allow_low_quality=True, source_dir=source_dir, work_dir=work_dir)

    summary = pipeline.evaluate(benchmark_path=benchmark_path, work_dir=work_dir, top_k=3)

    assert summary.total_cases == 2
    assert summary.retrieval_recall_at_k == 1.0
    assert summary.evidence_hit_rate == 1.0
    assert summary.citation_accuracy == 1.0
    assert summary.no_answer_precision == 1.0
    assert summary.diversity_enforcement_rate == 0.0
    assert summary.answer_cache_hit_rate == 0.0
    assert "retrieval_recall_at_k|question_type|factoid" in summary.segment_breakdown
    assert summary.tier_distribution
    assert isinstance(summary.fix_recommendations, dict)
    assert (work_dir / "evaluation" / "latest-evaluation.json").exists()
    assert (work_dir / "evaluation" / "evaluation_segments.json").exists()
    assert (work_dir / "evaluation" / "latest-evaluation.md").exists()


def test_evaluator_marks_failure_stage_when_expected_document_is_missing(tmp_path: Path) -> None:
    source_dir = tmp_path / "raw"
    work_dir = tmp_path / "work"
    source_dir.mkdir(parents=True, exist_ok=True)

    (source_dir / "policy.md").write_text("# Policy\n\nEmployees must use approved docs.\n", encoding="utf-8")
    benchmark_path = tmp_path / "benchmark.json"
    benchmark_path.write_text(
        json.dumps(
            [
                {
                    "question": "What sender is supported in Spain?",
                    "expected_document_ids": ["spain_es"],
                    "expected_terms": ["supported"],
                    "question_type": "factoid",
                    "should_refuse": False,
                }
            ],
            indent=2,
        ),
        encoding="utf-8",
    )

    pipeline = KnowledgePipeline(Settings(OKR_SOURCE_DIR=source_dir, OKR_WORK_DIR=work_dir))
    pipeline.build_index(allow_low_quality=True, source_dir=source_dir, work_dir=work_dir)
    summary = pipeline.evaluate(benchmark_path=benchmark_path, work_dir=work_dir, top_k=3)

    assert summary.results[0].failure_stage == "retrieval"
    assert summary.failure_analysis["by_stage"]["retrieval"] == 1
    assert "retrieval" in summary.fix_recommendations
    assert summary.results[0].routed_tier in {"tier0", "tier1", "tier2", "refusal"}
    assert summary.results[0].query_intent


def test_evaluation_can_validate_curated_source_fact_ingestion(tmp_path: Path) -> None:
    source_dir = tmp_path / "raw"
    work_dir = tmp_path / "work"
    source_dir.mkdir(parents=True, exist_ok=True)
    (source_dir / "global-restriction.json").write_text(
        json.dumps(
            {
                "document_title": "Global SMS Sender Registration Requirements",
                "content_type": "messaging_rules",
                "source_facts": [
                    {
                        "field": "operator_requirement",
                        "value": "GrameenPhone, Robi/Axiata, TeleTalk",
                        "applies_to": "Bangladesh",
                        "condition": "mandatory registration",
                    }
                ],
                "tables": [],
                "notes": [],
            }
        ),
        encoding="utf-8",
    )
    benchmark_path = tmp_path / "benchmark.json"
    benchmark_path.write_text(
        json.dumps(
            [
                {
                    "question": "operator_requirement Bangladesh GrameenPhone Robi Axiata TeleTalk",
                    "expected_document_ids": ["global-restriction"],
                    "expected_terms": ["GrameenPhone", "Robi/Axiata", "TeleTalk"],
                    "expected_block_types": ["structured_fact"],
                    "expected_metadata": {
                        "row_key": "operator_requirement",
                        "structured_value": "GrameenPhone, Robi/Axiata, TeleTalk",
                    },
                    "question_type": "ingestion_fact",
                    "should_refuse": False,
                }
            ],
            indent=2,
        ),
        encoding="utf-8",
    )

    pipeline = KnowledgePipeline(
        Settings(
            OKR_SOURCE_DIR=source_dir,
            OKR_WORK_DIR=work_dir,
            OKR_MAPPING_PROVIDER="noop",
        )
    )
    pipeline.build_index(allow_low_quality=True, source_dir=source_dir, work_dir=work_dir)
    summary = pipeline.evaluate(benchmark_path=benchmark_path, work_dir=work_dir, top_k=3)

    assert summary.retrieval_recall_at_k == 1.0
    assert summary.results[0].block_type_hit is True
    assert summary.results[0].metadata_hit is True
    assert summary.results[0].failure_stage is None


def test_evaluator_marks_citation_failure_when_anchor_expectation_is_not_met(tmp_path: Path) -> None:
    source_dir = tmp_path / "raw"
    work_dir = tmp_path / "work"
    source_dir.mkdir(parents=True, exist_ok=True)
    file_path = source_dir / "spain_es.md"
    file_path.write_text(
        """# Spain (ES)

## Sender
Sender provisioning: No sender registration needed.
""",
        encoding="utf-8",
    )
    benchmark_path = tmp_path / "benchmark.json"
    benchmark_path.write_text(
        json.dumps(
            [
                {
                    "question": "Sender in Spain?",
                    "expected_document_ids": ["spain_es"],
                    "expected_source_paths": [str(file_path)],
                    "expected_terms": ["sender provisioning", "no sender registration needed"],
                    "expected_section_terms": ["sender"],
                    "expected_anchor_terms": ["nonexistent anchor phrase"],
                    "question_type": "factoid",
                    "should_refuse": False,
                }
            ],
            indent=2,
        ),
        encoding="utf-8",
    )

    pipeline = KnowledgePipeline(Settings(OKR_SOURCE_DIR=source_dir, OKR_WORK_DIR=work_dir))
    pipeline.build_index(allow_low_quality=True, source_dir=source_dir, work_dir=work_dir)
    summary = pipeline.evaluate(benchmark_path=benchmark_path, work_dir=work_dir, top_k=3)

    assert summary.citation_accuracy == 0.0
    assert summary.results[0].citation_hit is False
    assert summary.results[0].failure_stage == "citation"


def test_evaluator_tracks_country_precision_metrics() -> None:
    evaluator = Evaluator()
    colombia_block = KnowledgeBlock(
        block_id="colombia-block",
        document_id="colombia_co",
        title="Colombia (CO)",
        section_path=["Colombia (CO)", "Sender"],
        section_heading="Sender",
        block_type="table_fact",
        text="For Colombia, the Sender availability is: Short Code.",
        source_path="data/raw/colombia_co.md",
        start_anchor="Sender availability",
        end_anchor="Short Code",
        country="Colombia",
        iso_code="CO",
    )
    angola_block = KnowledgeBlock(
        block_id="angola-block",
        document_id="angola_ao",
        title="Angola (AO)",
        section_path=["Angola (AO)", "Phone Numbers & Sender ID"],
        section_heading="Phone Numbers & Sender ID",
        block_type="table_fact",
        text="Regarding Phone Numbers & Sender ID, the Sender ID preserved value is: Yes.",
        source_path="data/raw/angola_ao.md",
        start_anchor="Sender ID preserved",
        end_anchor="Yes",
        country="Angola",
        iso_code="AO",
    )
    colombia_hit = SearchHit(block=colombia_block, score=0.92)
    angola_hit = SearchHit(block=angola_block, score=0.77)
    cases = [
        EvaluationCase(
            question="Sender in Colombia?",
            expected_document_ids=["colombia_co"],
            expected_terms=["sender", "short code"],
            expected_iso_code="CO",
            must_not_mix_documents=True,
            question_type="country_precision",
            should_refuse=False,
        )
    ]

    summary = evaluator.evaluate(
        cases,
        lambda _question: (
            [colombia_hit, angola_hit],
            Answer(
                question="Sender in Colombia?",
                answer="For Colombia, the Sender availability is: Short Code.",
                confidence="high",
                evidence=[colombia_hit, angola_hit],
                tier="tier0",
                query_intent="lookup",
            ),
        ),
    )

    assert summary.country_match_at_1 == 1.0
    assert summary.foreign_evidence_rate == 1.0
    assert summary.wrong_country_answer_rate == 0.0
    assert summary.results[0].failure_stage == "geo_precision"
    assert summary.results[0].foreign_evidence_present is True


def test_evaluator_matches_normalized_answer_terms() -> None:
    evaluator = Evaluator()

    assert evaluator._matches_terms(["+93"], "Afghanistan's dialing code is 93.", fallback=False)
    assert evaluator._matches_terms(["yes"], "Yes. In Afghanistan, alphanumeric sender IDs are preserved.", fallback=False)
    assert evaluator._matches_terms(["not supported"], "No. In Afghanistan, short code sender IDs are not supported.", fallback=False)
    assert evaluator._matches_terms(["7-14 days"], "Provisioning takes 1-2 weeks.", fallback=False)
    assert evaluator._matches_terms(
        ["alphanumeric sender id"],
        "In Albania, regarding Phone Numbers & Sender ID: Alphanumeric for Provisioning time.",
        fallback=False,
    )
    assert evaluator._matches_terms(
        ["not required"],
        "Yes. In Albania, alphanumeric sender IDs are supported.",
        fallback=False,
    )
