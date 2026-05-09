import argparse
import subprocess
import sys
from pathlib import Path

from own_knowledge_rag.benchmark_generation import (
    export_review_findings_benchmark,
    export_country_regression_cases,
    export_query_reviews_benchmark,
    generate_benchmark_cases,
    save_benchmark_cases,
)
from own_knowledge_rag.config import Settings
from own_knowledge_rag.benchmark_audit import audit_benchmark, render_benchmark_audit
from own_knowledge_rag.pipeline import KnowledgePipeline


def main() -> None:
    parser = argparse.ArgumentParser(prog="okr", description="Own Knowledge RAG CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser("build-index", help="Parse and index the raw corpus")
    build_parser.add_argument("--source-dir", type=Path, default=None)
    build_parser.add_argument("--work-dir", type=Path, default=None)
    build_parser.add_argument("--allowed-suffixes", nargs="+", default=None, help="Limit ingest to specific file suffixes such as .md or .json")
    build_parser.add_argument("--allow-low-quality", action="store_true", help="Allow indexing blocks that fail quality gates")
    build_parser.add_argument("--force-reenrich", action="store_true", help="Force provider enrichment even if cached")
    build_parser.add_argument("--mapping-provider", default=None)
    build_parser.add_argument("--mapping-model", default=None)
    build_parser.add_argument("--embedding-provider", default=None)
    build_parser.add_argument("--embedding-model", default=None)
    build_parser.add_argument("--embedding-device", default=None)
    build_parser.add_argument("--vector-backend", default=None)
    build_parser.add_argument("--vector-collection", default=None)
    build_parser.add_argument("--qdrant-url", default=None)
    build_parser.add_argument("--qdrant-api-key", default=None)

    ask_parser = subparsers.add_parser("ask", help="Ask a grounded question")
    ask_parser.add_argument("--work-dir", type=Path, default=None)
    ask_parser.add_argument("--question", required=True)
    ask_parser.add_argument("--top-k", type=int, default=None)

    eval_parser = subparsers.add_parser("evaluate", help="Run the minimal eval harness")
    eval_parser.add_argument("--work-dir", type=Path, default=None)
    eval_parser.add_argument("--benchmark-path", type=Path, required=True)
    eval_parser.add_argument("--top-k", type=int, default=None)

    benchmark_parser = subparsers.add_parser(
        "generate-benchmark",
        help="Generate a reproducible real-corpus benchmark from the current source corpus",
    )
    benchmark_parser.add_argument("--source-dir", type=Path, default=None)
    benchmark_parser.add_argument("--output-path", type=Path, required=True)
    benchmark_parser.add_argument("--max-cases", type=int, default=None)

    calibrate_parser = subparsers.add_parser(
        "calibrate-refusal",
        help="Sweep refusal thresholds against a benchmark",
    )
    calibrate_parser.add_argument("--work-dir", type=Path, default=None)
    calibrate_parser.add_argument("--benchmark-path", type=Path, required=True)
    calibrate_parser.add_argument("--top-k", type=int, default=None)

    serve_parser = subparsers.add_parser("serve-api", help="Run the thin local API")
    serve_parser.add_argument("--host", default=None)
    serve_parser.add_argument("--port", type=int, default=None)

    explain_parser = subparsers.add_parser("explain-block", help="Show enriched metadata for a specific block")
    explain_parser.add_argument("--block-id", required=True)
    explain_parser.add_argument("--work-dir", type=Path, default=None)

    audit_parser = subparsers.add_parser("audit", help="Generate a knowledge quality audit report (Data Science)")
    audit_parser.add_argument("--work-dir", type=Path, default=None)

    consistency_parser = subparsers.add_parser(
        "check-consistency",
        help="Generate a cross-section consistency report for locale profiles",
    )
    consistency_parser.add_argument("--work-dir", type=Path, default=None)

    review_packet_parser = subparsers.add_parser(
        "build-review-packets",
        help="Generate reviewer-friendly locale packets with quality and consistency context",
    )
    review_packet_parser.add_argument("--work-dir", type=Path, default=None)
    review_packet_parser.add_argument("--document-id", default=None)

    seed_review_parser = subparsers.add_parser(
        "seed-review-findings",
        help="Create a review_findings.json template from the current consistency report",
    )
    seed_review_parser.add_argument("--work-dir", type=Path, default=None)

    export_review_benchmark_parser = subparsers.add_parser(
        "export-review-benchmark",
        help="Export benchmark cases from reviewed findings decisions",
    )
    export_review_benchmark_parser.add_argument("--review-findings-path", type=Path, required=True)
    export_review_benchmark_parser.add_argument("--output-path", type=Path, required=True)

    country_regression_parser = subparsers.add_parser(
        "generate-country-regressions",
        help="Extract a country-locked regression suite from an existing benchmark file",
    )
    country_regression_parser.add_argument("--benchmark-path", type=Path, required=True)
    country_regression_parser.add_argument("--output-path", type=Path, required=True)
    country_regression_parser.add_argument(
        "--source-dir",
        type=Path,
        default=None,
        help="Optionally augment country regressions with generated single-country cases from the raw corpus",
    )

    query_review_benchmark_parser = subparsers.add_parser(
        "export-query-review-benchmark",
        help="Export benchmark cases from user-rated query reviews",
    )
    query_review_benchmark_parser.add_argument("--query-reviews-path", type=Path, required=True)
    query_review_benchmark_parser.add_argument("--output-path", type=Path, required=True)

    benchmark_audit_parser = subparsers.add_parser(
        "benchmark-audit",
        help="Audit benchmark segment distribution",
    )
    benchmark_audit_parser.add_argument("--benchmark-path", type=Path, required=True)
    benchmark_audit_parser.add_argument("--min-cases", type=int, default=10)
    benchmark_audit_parser.add_argument(
        "--allow-low-count",
        action="append",
        default=[],
        help="Allow a documented low-count segment such as 'sender_type:toll-free number'.",
    )

    gate_parser = subparsers.add_parser(
        "gate-run",
        help="Run the production gate: lint, tests, benchmark audit, and evaluation",
    )
    gate_parser.add_argument("--work-dir", type=Path, default=Path("data/work"))
    gate_parser.add_argument("--benchmark-path", type=Path, default=Path("benchmarks/country_regressions.json"))
    gate_parser.add_argument("--top-k", type=int, default=None)
    gate_parser.add_argument("--min-cases", type=int, default=10)
    gate_parser.add_argument(
        "--allow-low-count",
        action="append",
        default=["sender_type:toll-free number"],
        help="Allow a documented low-count segment such as 'sender_type:toll-free number'.",
    )
    gate_parser.add_argument("--min-recall", type=float, default=0.90)
    gate_parser.add_argument("--min-evidence-hit-rate", type=float, default=0.90)
    gate_parser.add_argument("--min-answer-correctness", type=float, default=0.90)
    gate_parser.add_argument("--skip-lint", action="store_true")
    gate_parser.add_argument("--skip-tests", action="store_true")



    args = parser.parse_args()
    settings_overrides: dict[str, object] = {}
    for field_name, arg_name in [
        ("mapping_provider", "mapping_provider"),
        ("mapping_model", "mapping_model"),
        ("embedding_provider", "embedding_provider"),
        ("embedding_model", "embedding_model"),
        ("embedding_device", "embedding_device"),
        ("vector_backend", "vector_backend"),
        ("vector_collection", "vector_collection"),
        ("qdrant_url", "qdrant_url"),
        ("qdrant_api_key", "qdrant_api_key"),
    ]:
        value = getattr(args, arg_name, None)
        if value is not None:
            settings_overrides[field_name] = value

    settings = Settings(**settings_overrides)
    pipeline = KnowledgePipeline(settings)

    if args.command == "build-index":
        manifest = pipeline.build_index(
            source_dir=args.source_dir, 
            work_dir=args.work_dir,
            allowed_suffixes=args.allowed_suffixes,
            allow_low_quality=args.allow_low_quality,
            force_reenrich=args.force_reenrich
        )
        print(f"Indexed {manifest['documents']} documents into {manifest['blocks']} knowledge blocks.")
        return

    if args.command == "ask":
        print(pipeline.ask(question=args.question, work_dir=args.work_dir, top_k=args.top_k))
        return

    if args.command == "evaluate":
        summary = pipeline.evaluate(
            benchmark_path=args.benchmark_path,
            work_dir=args.work_dir,
            top_k=args.top_k,
        )
        print(
            "Evaluation complete: "
            f"recall@k={summary.retrieval_recall_at_k} "
            f"evidence_hit_rate={summary.evidence_hit_rate} "
            f"document_precision@k={summary.document_precision_at_k} "
            f"no_answer_precision={summary.no_answer_precision} "
            f"answer_correctness={summary.answer_correctness}"
        )
        return

    if args.command == "gate-run":
        gate_failed = False
        if not args.skip_lint:
            lint = subprocess.run([sys.executable, "-m", "ruff", "check", "."], check=False)
            gate_failed = gate_failed or lint.returncode != 0
        if not args.skip_tests:
            tests = subprocess.run([sys.executable, "-m", "pytest"], check=False)
            gate_failed = gate_failed or tests.returncode != 0
        audit = audit_benchmark(
            args.benchmark_path,
            min_cases=args.min_cases,
            allow_low_count=args.allow_low_count,
        )
        print(render_benchmark_audit(audit))
        gate_failed = gate_failed or not bool(audit["adequate"])
        gate_pipeline = KnowledgePipeline(settings.model_copy(update={"query_cache_enabled": False}))
        summary = gate_pipeline.evaluate(
            benchmark_path=args.benchmark_path,
            work_dir=args.work_dir,
            top_k=args.top_k,
        )
        checks = [
            ("recall@k", summary.retrieval_recall_at_k, args.min_recall),
            ("evidence_hit_rate", summary.evidence_hit_rate, args.min_evidence_hit_rate),
            ("answer_correctness", summary.answer_correctness, args.min_answer_correctness),
        ]
        for name, value, minimum in checks:
            status = "PASS" if value >= minimum else "FAIL"
            print(f"{status} {name}: {value} >= {minimum}")
            gate_failed = gate_failed or value < minimum
        if gate_failed:
            raise SystemExit(1)
        print("Production gate: PASS")
        return

    if args.command == "generate-benchmark":
        cases = generate_benchmark_cases(
            source_dir=args.source_dir or settings.source_dir,
            max_cases=args.max_cases,
        )
        save_benchmark_cases(cases, args.output_path)
        print(f"Wrote {len(cases)} benchmark cases to {args.output_path}.")
        return

    if args.command == "calibrate-refusal":
        report = pipeline.calibrate_refusal(
            benchmark_path=args.benchmark_path,
            work_dir=args.work_dir,
            top_k=args.top_k,
        )
        print(
            "Refusal calibration complete: "
            f"min_score={report.recommended_min_score_threshold} "
            f"min_overlap={report.recommended_min_overlap_ratio} "
            f"tier0={report.recommended_tier0_score_threshold} "
            f"tier2={report.recommended_tier2_score_threshold} "
            f"answer_correctness={report.recommended_answer_correctness} "
            f"tier0_1_share={report.recommended_tier0_1_share}"
        )
        return

    if args.command == "serve-api":
        import uvicorn

        from own_knowledge_rag.api import create_app

        app = create_app(settings)
        uvicorn.run(
            app,
            host=args.host or settings.api_host,
            port=args.port or settings.api_port,
        )
        return

    if args.command == "explain-block":
        print(pipeline.explain_block(block_id=args.block_id, work_dir=args.work_dir))
        return

    if args.command == "audit":
        report_path = pipeline.audit_knowledge(work_dir=args.work_dir)
        print("Knowledge quality audit complete.")
        print(f"Report generated at: {report_path}")
        return

    if args.command == "check-consistency":
        report_path = pipeline.check_consistency(work_dir=args.work_dir)
        print("Cross-section consistency check complete.")
        print(f"Report generated at: {report_path}")
        return

    if args.command == "build-review-packets":
        packet_paths = pipeline.build_review_packets(
            work_dir=args.work_dir,
            document_id=args.document_id,
        )
        print(f"Review packet generation complete: {len(packet_paths)} packet(s).")
        for path in packet_paths:
            print(path)
        return

    if args.command == "seed-review-findings":
        output_path = pipeline.seed_review_findings(work_dir=args.work_dir)
        print("Review findings template generated.")
        print(output_path)
        return

    if args.command == "export-review-benchmark":
        cases = export_review_findings_benchmark(args.review_findings_path, args.output_path)
        print(f"Exported {len(cases)} review-derived benchmark case(s).")
        print(args.output_path)
        return

    if args.command == "generate-country-regressions":
        cases = export_country_regression_cases(args.benchmark_path, args.output_path, source_dir=args.source_dir)
        print(f"Exported {len(cases)} country regression case(s).")
        print(args.output_path)
        return

    if args.command == "export-query-review-benchmark":
        cases = export_query_reviews_benchmark(args.query_reviews_path, args.output_path)
        print(f"Exported {len(cases)} query-review benchmark case(s).")
        print(args.output_path)
        return

    if args.command == "benchmark-audit":
        print(
            render_benchmark_audit(
                audit_benchmark(
                    args.benchmark_path,
                    min_cases=args.min_cases,
                    allow_low_count=args.allow_low_count,
                )
            )
        )
        return


if __name__ == "__main__":
    main()
