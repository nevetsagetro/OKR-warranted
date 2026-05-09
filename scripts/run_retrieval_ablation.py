from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "src"))

from own_knowledge_rag.retrieval_ablation import (  # noqa: E402
    run_retrieval_ablation,
    write_retrieval_ablation_report,
)


def main() -> None:
    report = run_retrieval_ablation(
        work_dir=Path("data/work"),
        benchmark_path=Path("benchmarks/country_regressions.json"),
        output_path=Path("reports/tables/retrieval_ablation_study.json"),
    )
    write_retrieval_ablation_report(report, Path("docs/retrieval_ablation_study.md"))
    print("Wrote reports/tables/retrieval_ablation_study.json")
    print("Wrote docs/retrieval_ablation_study.md")
    print(
        "Best mode="
        f"{report['best_mode']['name']} "
        "evidence_hit_rate="
        f"{report['best_mode']['metrics']['evidence_hit_rate']}"
    )


if __name__ == "__main__":
    main()
