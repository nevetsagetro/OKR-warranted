import json
import shutil
import math
import random
from hashlib import sha1
from datetime import UTC, datetime
from pathlib import Path

from own_knowledge_rag.models import EvaluationSummary


def experiments_registry_path(root_dir: Path) -> Path:
    return root_dir / "experiments" / "registry.json"


def suggest_experiment_layout(root_dir: Path, hypothesis: str) -> dict[str, str]:
    timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    slug = _slugify(hypothesis)
    digest = sha1(hypothesis.strip().encode("utf-8")).hexdigest()[:8] if hypothesis.strip() else "00000000"
    experiment_token = f"{slug}_{timestamp}_{digest}"
    experiment_id = f"exp_{experiment_token}"
    experiment_root = root_dir / "experiment_sources" / experiment_id
    source_dir = experiment_root / "raw"
    work_dir = root_dir / f"work_exp_{experiment_token}"
    return {
        "experiment_id": experiment_id,
        "experiment_root_dir": str(experiment_root),
        "experiment_source_dir": str(source_dir),
        "experiment_work_dir": str(work_dir),
        "slug": slug,
        "timestamp": timestamp,
        "hypothesis_hash": digest,
    }


def stage_experiment_files(
    experiment_source_dir: Path,
    files: list[dict[str, str]],
) -> dict[str, object]:
    experiment_source_dir.mkdir(parents=True, exist_ok=True)
    saved_files: list[str] = []
    for entry in files:
        name = Path(str(entry.get("name", "")).strip()).name
        content = str(entry.get("content", ""))
        if not name:
            continue
        target = experiment_source_dir / name
        target.write_text(content, encoding="utf-8")
        saved_files.append(str(target))
    return {
        "source_dir": str(experiment_source_dir),
        "file_count": len(saved_files),
        "files": saved_files,
    }


def load_experiments_registry(root_dir: Path) -> dict[str, object]:
    path = experiments_registry_path(root_dir)
    if not path.exists():
        return {"entries": []}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {"entries": []}


def clear_experiments_registry(root_dir: Path) -> tuple[Path, int]:
    path = experiments_registry_path(root_dir)
    payload = load_experiments_registry(root_dir)
    entries = payload.get("entries", [])
    cleared_count = len(entries) if isinstance(entries, list) else 0
    path.parent.mkdir(parents=True, exist_ok=True)
    payload["entries"] = []
    payload["cleared_at"] = _utc_timestamp()
    payload["cleared_count"] = cleared_count
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path, cleared_count


def save_experiment_record(root_dir: Path, entry: dict[str, object]) -> tuple[Path, dict[str, object]]:
    path = experiments_registry_path(root_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = load_experiments_registry(root_dir)
    entries = payload.get("entries", [])
    if not isinstance(entries, list):
        entries = []

    normalized_work_dir = str(Path(str(entry["experiment_work_dir"])).resolve())
    now = _utc_timestamp()
    existing = next(
        (
            item
            for item in entries
            if isinstance(item, dict)
            and str(Path(str(item.get("experiment_work_dir", ""))).resolve()) == normalized_work_dir
        ),
        None,
    )

    if existing is None:
        experiment_id = str(entry.get("experiment_id") or f"exp-{len(entries) + 1:04d}")
        stored = {"experiment_id": experiment_id, "created_at": now, **entry, "updated_at": now}
        entries.append(stored)
    else:
        existing.update(entry)
        existing["updated_at"] = now
        stored = existing

    payload["entries"] = entries
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path, stored


def promote_experiment_workspace(
    experiment_work_dir: Path,
    baseline_work_dir: Path,
) -> dict[str, str]:
    if experiment_work_dir.resolve() == baseline_work_dir.resolve():
        raise ValueError("Experiment and baseline work_dir must be different for promotion.")
    if not experiment_work_dir.exists():
        raise ValueError(f"Experiment work_dir does not exist: {experiment_work_dir}")
    required = ["manifest.json", "blocks.json", "documents.json"]
    missing = [name for name in required if not (experiment_work_dir / name).exists()]
    if missing:
        raise ValueError(
            f"Experiment work_dir is missing index artifacts: {', '.join(missing)}"
        )

    timestamp = datetime.now(UTC).strftime("%Y%m%d-%H%M%S")
    backup_dir = baseline_work_dir.parent / f"{baseline_work_dir.name}_backup_{timestamp}"
    temp_dir = baseline_work_dir.parent / f".{baseline_work_dir.name}.promoting-{timestamp}"

    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    shutil.copytree(experiment_work_dir, temp_dir)

    if baseline_work_dir.exists():
        shutil.copytree(baseline_work_dir, backup_dir)
        shutil.rmtree(baseline_work_dir)
    temp_dir.replace(baseline_work_dir)

    return {
        "baseline_work_dir": str(baseline_work_dir),
        "backup_work_dir": str(backup_dir) if backup_dir.exists() else "",
        "experiment_work_dir": str(experiment_work_dir),
        "promoted_at": _utc_timestamp(),
    }


def promote_experiment_sources(
    *,
    experiment_source_dir: Path,
    baseline_source_dir: Path,
) -> dict[str, object]:
    if experiment_source_dir.resolve() == baseline_source_dir.resolve():
        raise ValueError("Experiment source_dir and baseline source_dir must be different.")
    if not experiment_source_dir.exists():
        raise ValueError(f"Experiment source_dir does not exist: {experiment_source_dir}")
    if not experiment_source_dir.is_dir():
        raise ValueError(f"Experiment source_dir is not a folder: {experiment_source_dir}")

    source_files = [path for path in experiment_source_dir.rglob("*") if path.is_file()]
    if not source_files:
        raise ValueError(f"Experiment source_dir has no files to promote: {experiment_source_dir}")

    timestamp = datetime.now(UTC).strftime("%Y%m%d-%H%M%S")
    backup_dir = baseline_source_dir.parent / f"{baseline_source_dir.name}_source_backup_{timestamp}"
    copied: list[str] = []
    overwritten: list[str] = []
    unchanged: list[str] = []
    backed_up: list[str] = []

    baseline_source_dir.mkdir(parents=True, exist_ok=True)
    for source_file in source_files:
        relative = source_file.relative_to(experiment_source_dir)
        destination = baseline_source_dir / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            source_bytes = source_file.read_bytes()
            destination_bytes = destination.read_bytes()
            if source_bytes == destination_bytes:
                unchanged.append(str(destination))
                continue
            backup_target = backup_dir / relative
            backup_target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(destination, backup_target)
            shutil.copy2(source_file, destination)
            overwritten.append(str(destination))
            backed_up.append(str(backup_target))
        else:
            shutil.copy2(source_file, destination)
            copied.append(str(destination))

    return {
        "experiment_source_dir": str(experiment_source_dir),
        "baseline_source_dir": str(baseline_source_dir),
        "backup_source_dir": str(backup_dir) if backup_dir.exists() else "",
        "copied_files": copied,
        "overwritten_files": overwritten,
        "unchanged_files": unchanged,
        "backed_up_files": backed_up,
        "promoted_source_count": len(copied) + len(overwritten),
        "unchanged_count": len(unchanged),
        "promoted_sources_at": _utc_timestamp(),
    }


def experiment_sources_alignment(
    *,
    experiment_source_dir: Path,
    baseline_source_dir: Path,
) -> dict[str, object]:
    if not experiment_source_dir.exists():
        raise ValueError(f"Experiment source_dir does not exist: {experiment_source_dir}")
    if not experiment_source_dir.is_dir():
        raise ValueError(f"Experiment source_dir is not a folder: {experiment_source_dir}")
    if not baseline_source_dir.exists():
        raise ValueError(f"Baseline source_dir does not exist: {baseline_source_dir}")
    if not baseline_source_dir.is_dir():
        raise ValueError(f"Baseline source_dir is not a folder: {baseline_source_dir}")

    missing_files: list[str] = []
    changed_files: list[str] = []
    checked_files = 0
    for source_file in sorted(path for path in experiment_source_dir.rglob("*") if path.is_file()):
        checked_files += 1
        relative = source_file.relative_to(experiment_source_dir)
        baseline_file = baseline_source_dir / relative
        if not baseline_file.exists():
            missing_files.append(str(relative))
            continue
        if source_file.read_bytes() != baseline_file.read_bytes():
            changed_files.append(str(relative))

    return {
        "accepted": not missing_files and not changed_files,
        "checked_files": checked_files,
        "missing_files": missing_files,
        "changed_files": changed_files,
    }


def compare_experiments(
    baseline: EvaluationSummary,
    experiment: EvaluationSummary,
    output_path: Path | None = None,
    *,
    resamples: int = 2000,
    alpha: float = 0.05,
) -> dict[str, object]:
    metrics = ["retrieval_hit", "evidence_hit", "answer_correct"]
    reports = []
    for result_metric in metrics:
        baseline_values = _result_metric_values(baseline, result_metric)
        experiment_values = _result_metric_values(experiment, result_metric)
        pair_count = min(len(baseline_values), len(experiment_values))
        if pair_count == 0:
            continue
        baseline_values = baseline_values[:pair_count]
        experiment_values = experiment_values[:pair_count]
        deltas = [experiment_values[index] - baseline_values[index] for index in range(pair_count)]
        ci_low, ci_high = _bootstrap_ci(deltas, resamples=resamples, alpha=alpha)
        delta = round(sum(deltas) / pair_count, 4)
        p_value = _paired_sign_test_p_value(deltas)
        reports.append(
            {
                "metric": _summary_metric_name(result_metric),
                "baseline": round(sum(baseline_values) / pair_count, 4),
                "experiment": round(sum(experiment_values) / pair_count, 4),
                "delta": delta,
                "ci_low": ci_low,
                "ci_high": ci_high,
                "p_value": p_value,
                "significant": p_value < alpha and not (ci_low <= 0 <= ci_high),
            }
        )
    payload = {
        "alpha": alpha,
        "resamples": resamples,
        "paired_cases": min(len(baseline.results), len(experiment.results)),
        "metrics": reports,
    }
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def rollback_baseline_workspace(
    *,
    baseline_work_dir: Path,
    backup_work_dir: Path,
) -> dict[str, str]:
    if backup_work_dir.resolve() == baseline_work_dir.resolve():
        raise ValueError("Backup and baseline work_dir must be different for rollback.")
    if not backup_work_dir.exists():
        raise ValueError(f"Backup work_dir does not exist: {backup_work_dir}")
    required = ["manifest.json", "blocks.json", "documents.json"]
    missing = [name for name in required if not (backup_work_dir / name).exists()]
    if missing:
        raise ValueError(f"Backup work_dir is missing index artifacts: {', '.join(missing)}")

    timestamp = datetime.now(UTC).strftime("%Y%m%d-%H%M%S")
    current_backup_dir = baseline_work_dir.parent / f"{baseline_work_dir.name}_pre_rollback_{timestamp}"
    temp_dir = baseline_work_dir.parent / f".{baseline_work_dir.name}.rollback-{timestamp}"

    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    shutil.copytree(backup_work_dir, temp_dir)

    if baseline_work_dir.exists():
        shutil.copytree(baseline_work_dir, current_backup_dir)
        shutil.rmtree(baseline_work_dir)
    temp_dir.replace(baseline_work_dir)

    return {
        "baseline_work_dir": str(baseline_work_dir),
        "restored_backup_work_dir": str(backup_work_dir),
        "current_baseline_backup_work_dir": str(current_backup_dir)
        if current_backup_dir.exists()
        else "",
        "rolled_back_at": _utc_timestamp(),
    }


def _utc_timestamp() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _slugify(value: str) -> str:
    slug = "".join(ch.lower() if ch.isalnum() else "_" for ch in value.strip())
    slug = "_".join(part for part in slug.split("_") if part)
    return (slug[:48] or "candidate").strip("_")


def _result_metric_values(summary: EvaluationSummary, metric: str) -> list[int]:
    return [int(bool(getattr(result, metric))) for result in summary.results if not result.should_refuse]


def _summary_metric_name(result_metric: str) -> str:
    return {
        "retrieval_hit": "retrieval_recall_at_k",
        "evidence_hit": "evidence_hit_rate",
        "answer_correct": "answer_correctness",
    }[result_metric]


def _bootstrap_ci(deltas: list[int], *, resamples: int, alpha: float) -> tuple[float, float]:
    if not deltas:
        return 0.0, 0.0
    rng = random.Random(13)
    means = []
    for _ in range(max(1, resamples)):
        sample = [deltas[rng.randrange(len(deltas))] for _ in deltas]
        means.append(sum(sample) / len(sample))
    means.sort()
    low_index = int((alpha / 2) * (len(means) - 1))
    high_index = int((1 - alpha / 2) * (len(means) - 1))
    return round(means[low_index], 4), round(means[high_index], 4)


def _paired_sign_test_p_value(deltas: list[int]) -> float:
    wins = sum(1 for delta in deltas if delta > 0)
    losses = sum(1 for delta in deltas if delta < 0)
    trials = wins + losses
    if trials == 0:
        return 1.0
    observed = min(wins, losses)
    probability = sum(math.comb(trials, k) for k in range(observed + 1)) / (2**trials)
    return round(min(1.0, 2 * probability), 4)
