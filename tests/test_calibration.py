import json
from pathlib import Path

from own_knowledge_rag.config import Settings
from own_knowledge_rag.pipeline import KnowledgePipeline


def test_pipeline_calibrates_refusal_thresholds_and_writes_report(tmp_path: Path) -> None:
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
    (source_dir / "policy.md").write_text(
        """# Policy

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
                    "expected_terms": ["sender provisioning", "no sender registration needed"],
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

    pipeline = KnowledgePipeline(Settings(OKR_SOURCE_DIR=source_dir, OKR_WORK_DIR=work_dir))
    pipeline.build_index(allow_low_quality=True, source_dir=source_dir, work_dir=work_dir)

    report = pipeline.calibrate_refusal(
        benchmark_path=benchmark_path,
        work_dir=work_dir,
        top_k=3,
    )

    assert report.candidates
    assert report.recommended_min_score_threshold > 0
    assert report.recommended_min_overlap_ratio > 0
    assert report.recommended_tier0_score_threshold > 0
    assert report.recommended_tier2_score_threshold > 0
    assert report.total_cases == 2
    assert report.answerable_cases == 1
    assert report.refusal_cases == 1
    assert report.candidate_count == len(report.candidates)
    assert (work_dir / "evaluation" / "refusal-calibration.json").exists()
    assert (work_dir / "evaluation" / "refusal-calibration.md").exists()
