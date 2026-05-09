import json
from collections import Counter
from pathlib import Path


def audit_benchmark(
    benchmark_path: Path,
    *,
    min_cases: int = 10,
    allow_low_count: list[str] | tuple[str, ...] | set[str] | None = None,
) -> dict[str, object]:
    payload = json.loads(benchmark_path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("Benchmark file must contain a JSON array.")
    allowed_low_count = {item.strip() for item in (allow_low_count or []) if item.strip()}

    counters = {
        "iso_code": Counter[str](),
        "question_type": Counter[str](),
        "sender_type": Counter[str](),
        "block_type": Counter[str](),
    }
    missing_metadata = Counter[str]()
    for item in payload:
        if not isinstance(item, dict):
            continue
        iso = str(item.get("expected_iso_code") or _iso_from_documents(item.get("expected_document_ids")) or "unknown")
        counters["iso_code"][iso] += 1
        question_type = str(item.get("question_type") or "factoid")
        counters["question_type"][question_type] += 1
        sender_types = item.get("expected_sender_types") or item.get("sender_types") or []
        block_types = item.get("expected_block_types") or []
        if not sender_types and _expects_sender_metadata(item, question_type):
            missing_metadata["sender_type"] += 1
        if not block_types:
            missing_metadata["block_type"] += 1
        for value in sender_types or ["unknown"]:
            counters["sender_type"][str(value or "unknown")] += 1
        for value in block_types or ["unknown"]:
            counters["block_type"][str(value or "unknown")] += 1

    tables = {
        name: dict(sorted(counter.items(), key=lambda entry: (-entry[1], entry[0])))
        for name, counter in counters.items()
    }
    warnings = []
    allowed_low_count_findings = []
    for name, table in tables.items():
        for value, count in table.items():
            segment = f"{name}:{value}"
            if value == "unknown" or count >= min_cases:
                continue
            message = f"{segment} has {count} case(s), below minimum {min_cases}."
            if segment in allowed_low_count:
                allowed_low_count_findings.append(message)
            else:
                warnings.append(message)
    metadata_warnings = [
        f"{name} metadata is missing for {count} case(s)."
        for name, count in sorted(missing_metadata.items())
        if count
    ]
    warnings.extend(metadata_warnings)
    return {
        "benchmark_path": str(benchmark_path),
        "total_cases": len(payload),
        "min_cases": min_cases,
        "tables": tables,
        "missing_metadata": dict(sorted(missing_metadata.items())),
        "allowed_low_count": sorted(allowed_low_count),
        "allowed_low_count_findings": allowed_low_count_findings,
        "warnings": warnings,
        "adequate": not warnings,
    }


def render_benchmark_audit(report: dict[str, object]) -> str:
    lines = [
        f"Benchmark audit: {report['benchmark_path']}",
        f"Total cases: {report['total_cases']}",
        f"Minimum cases per segment: {report['min_cases']}",
        "",
    ]
    tables = report.get("tables", {})
    if isinstance(tables, dict):
        for name, table in tables.items():
            lines.append(name)
            if isinstance(table, dict):
                for value, count in table.items():
                    lines.append(f"  {value}: {count}")
            lines.append("")
    warnings = report.get("warnings", [])
    missing_metadata = report.get("missing_metadata", {})
    if isinstance(missing_metadata, dict) and missing_metadata:
        lines.append("Missing metadata:")
        for name, count in missing_metadata.items():
            lines.append(f"  {name}: {count}")
        lines.append("")
    allowed_low_count_findings = report.get("allowed_low_count_findings", [])
    if allowed_low_count_findings:
        lines.append("Allowed low-count segments:")
        for finding in allowed_low_count_findings:
            lines.append(f"- {finding}")
        lines.append("")
    lines.append("Warnings:")
    if warnings:
        lines.extend(f"- {warning}" for warning in warnings)
    else:
        lines.append("- none")
    return "\n".join(lines)


def _iso_from_documents(value: object) -> str:
    if not isinstance(value, list) or len(value) != 1:
        return ""
    document_id = str(value[0])
    if "_" not in document_id:
        return ""
    return document_id.split("_")[-1].upper()


def _expects_sender_metadata(item: dict[str, object], question_type: str) -> bool:
    if question_type.startswith("sender_type"):
        return True
    question = str(item.get("question") or "").lower()
    return any(term in question for term in ("sender id", "sender ids", "short code", "long code", "toll-free", "toll free"))
