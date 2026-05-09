import json
import re
from dataclasses import asdict
from pathlib import Path

from own_knowledge_rag.models import EvaluationCase
from own_knowledge_rag.normalizers import normalize_document
from own_knowledge_rag.parsers import can_parse_file, parse_file


VALUE_PATTERN = re.compile(r"(?:^|;\s)Value=([^;]+)")


def generate_benchmark_cases(source_dir: Path, max_cases: int | None = None) -> list[EvaluationCase]:
    cases: list[EvaluationCase] = []

    for path in sorted(source_dir.rglob("*")):
        if not can_parse_file(path):
            continue
        parsed = parse_file(path)
        if parsed is None or parsed.content_type != "markdown":
            continue

        blocks = normalize_document(parsed)
        locale_name = _locale_name(parsed.title, blocks)
        source_path = parsed.source_path

        if parsed.document_id == "all_twilio_sms_guidelines_index":
            cases.extend(_catalog_cases(parsed.document_id, source_path, blocks))
            continue

        if any("locale summary" in " > ".join(block.section_path).lower() for block in blocks):
            cases.extend(_profile_cases(parsed.document_id, source_path, locale_name, blocks))

    cases.extend(_refusal_cases())

    deduped = _dedupe_cases(cases)
    if max_cases is not None:
        return deduped[:max_cases]
    return deduped


def save_benchmark_cases(cases: list[EvaluationCase], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps([asdict(case) for case in cases], indent=2),
        encoding="utf-8",
    )


def export_review_findings_benchmark(review_findings_path: Path, output_path: Path) -> list[EvaluationCase]:
    payload = json.loads(review_findings_path.read_text(encoding="utf-8"))
    entries = payload.get("entries", []) if isinstance(payload, dict) else []
    cases: list[EvaluationCase] = []

    for entry in entries:
        if not isinstance(entry, dict):
            continue
        review_status = str(entry.get("review_status", "")).strip().lower()
        document_id = str(entry.get("document_id", "")).strip()
        country = str(entry.get("country", "")).strip() or document_id.replace("_", " ")
        normalized_key = str(entry.get("normalized_key", "")).strip()
        if not document_id or not normalized_key:
            continue

        question = _review_question(country, normalized_key)
        if review_status == "accepted_conflict":
            cases.append(
                EvaluationCase(
                    question=question,
                    expected_document_ids=[document_id],
                    expected_iso_code=_document_iso(document_id),
                    expected_terms=[],
                    question_type="consistency_refusal",
                    should_refuse=True,
                )
            )
            continue

        if review_status == "resolved":
            resolution_value = str(entry.get("resolution_value", "")).strip()
            if not resolution_value:
                continue
            cases.append(
                EvaluationCase(
                    question=question,
                    expected_document_ids=[document_id],
                    expected_iso_code=_document_iso(document_id),
                    expected_terms=_expected_terms_for_resolution(normalized_key, resolution_value),
                    expected_anchor_terms=[resolution_value],
                    question_type="consistency_resolution",
                    should_refuse=False,
                )
            )

    deduped = _dedupe_cases(cases)
    save_benchmark_cases(deduped, output_path)
    return deduped


def export_country_regression_cases(
    benchmark_path: Path,
    output_path: Path,
    source_dir: Path | None = None,
) -> list[EvaluationCase]:
    payload = json.loads(benchmark_path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("Benchmark file must contain a JSON array of evaluation cases.")

    cases = [EvaluationCase(**item) for item in payload if isinstance(item, dict)]
    if source_dir is not None:
        cases = [*generate_benchmark_cases(source_dir), *cases]
    filtered: list[EvaluationCase] = []
    for case in cases:
        if case.should_refuse:
            continue
        if case.question_type in {"comparative", "count", "refusal", "index_fact"}:
            continue
        if len(case.expected_document_ids) != 1:
            continue
        if not _question_mentions_expected_doc(case):
            continue
        filtered.append(
            EvaluationCase(
                question=case.question,
                expected_document_ids=case.expected_document_ids,
                expected_source_paths=case.expected_source_paths,
                expected_terms=case.expected_terms,
                expected_section_terms=case.expected_section_terms,
                expected_anchor_terms=case.expected_anchor_terms,
                expected_block_types=case.expected_block_types or _fallback_block_types(case),
                expected_sender_types=case.expected_sender_types or _fallback_sender_types(case),
                expected_metadata=case.expected_metadata or _fallback_expected_metadata(case),
                expected_iso_code=case.expected_iso_code or _document_iso(case.expected_document_ids[0]),
                forbid_document_ids=case.forbid_document_ids,
                must_not_mix_documents=True,
                question_type=case.question_type,
                should_refuse=case.should_refuse,
            )
        )

    deduped = _dedupe_cases(filtered)
    save_benchmark_cases(deduped, output_path)
    return deduped


def export_query_reviews_benchmark(
    query_reviews_path: Path,
    output_path: Path,
) -> list[EvaluationCase]:
    payload = json.loads(query_reviews_path.read_text(encoding="utf-8"))
    entries = payload.get("entries", []) if isinstance(payload, dict) else []
    cases: list[EvaluationCase] = []

    for entry in entries:
        if not isinstance(entry, dict):
            continue
        question = str(entry.get("question", "")).strip()
        rating = str(entry.get("rating", "")).strip().lower()
        if not question or not rating:
            continue

        expected_document_id = str(entry.get("expected_document_id", "")).strip()
        expected_terms = entry.get("expected_terms", [])
        if not isinstance(expected_terms, list):
            expected_terms = []
        expected_terms = [str(term).strip() for term in expected_terms if str(term).strip()]
        if not expected_terms:
            expected_terms = _fallback_expected_terms(entry)

        should_refuse = rating == "should_refuse"
        question_type = "country_regression"
        if rating in {"wrong_country", "correct_with_foreign_evidence"}:
            question_type = "country_precision"
        elif rating == "should_refuse":
            question_type = "review_refusal"

        cases.append(
            EvaluationCase(
                question=question,
                expected_document_ids=[expected_document_id] if expected_document_id and not should_refuse else [],
                expected_iso_code=str(entry.get("expected_iso_code", "")).strip().upper(),
                expected_terms=[] if should_refuse else expected_terms,
                expected_section_terms=[],
                must_not_mix_documents=rating in {"correct_with_foreign_evidence", "wrong_country", "incomplete", "correct"},
                question_type=question_type,
                should_refuse=should_refuse,
            )
        )

    deduped = _dedupe_cases(cases)
    save_benchmark_cases(deduped, output_path)
    return deduped


def _profile_cases(
    document_id: str,
    source_path: str,
    locale_name: str,
    blocks,
) -> list[EvaluationCase]:
    cases: list[EvaluationCase] = []

    dialing_block, dialing_value = _find_simple_fact(blocks, row_key="Dialing code")
    if dialing_value:
        cases.append(
            EvaluationCase(
                question=f"What is the dialing code for {locale_name}?",
                expected_document_ids=[document_id],
                expected_source_paths=[source_path],
                expected_terms=["dialing code", dialing_value],
                expected_section_terms=["locale summary"],
                expected_anchor_terms=["dialing code", dialing_value],
                expected_block_types=_expected_block_types(dialing_block),
                expected_metadata={"row_key": "Dialing code"},
                expected_iso_code=_document_iso(document_id),
                must_not_mix_documents=True,
                question_type="factoid",
                should_refuse=False,
            )
        )

    two_way_block, two_way_value = _find_simple_fact(blocks, row_key="Two-way SMS supported")
    if two_way_value:
        cases.append(
            EvaluationCase(
                question=f"Does {locale_name} support two-way SMS?",
                expected_document_ids=[document_id],
                expected_source_paths=[source_path],
                expected_terms=_answer_terms_for_value(two_way_value, fallback=["two-way sms"]),
                expected_section_terms=["guidelines"],
                expected_anchor_terms=["two-way sms supported", two_way_value],
                expected_block_types=_expected_block_types(two_way_block),
                expected_metadata={"row_key": "Two-way SMS supported"},
                expected_iso_code=_document_iso(document_id),
                must_not_mix_documents=True,
                question_type="capability",
                should_refuse=False,
            )
        )

    number_portability_block, number_portability_value = _find_simple_fact(blocks, row_key="Number portability available")
    if number_portability_value:
        cases.append(
            EvaluationCase(
                question=f"Is number portability available in {locale_name}?",
                expected_document_ids=[document_id],
                expected_source_paths=[source_path],
                expected_terms=_answer_terms_for_value(number_portability_value, fallback=["number portability"]),
                expected_section_terms=["guidelines"],
                expected_anchor_terms=["number portability available", number_portability_value],
                expected_block_types=_expected_block_types(number_portability_block),
                expected_metadata={"row_key": "Number portability available"},
                expected_iso_code=_document_iso(document_id),
                must_not_mix_documents=True,
                question_type="capability",
                should_refuse=False,
            )
        )

    cases.extend(_sender_matrix_cases(document_id, source_path, locale_name, blocks))
    cases.extend(_infobip_profile_cases(document_id, source_path, locale_name, blocks))
    cases.extend(_compliance_profile_cases(document_id, source_path, locale_name, blocks))

    return cases


def _fallback_expected_terms(entry: dict[str, object]) -> list[str]:
    answer = str(entry.get("answer", "")).strip().lower()
    evidence_document_ids = entry.get("evidence_document_ids", [])
    fallback_terms: list[str] = []
    if answer:
        fallback_terms.append(answer)
    if isinstance(evidence_document_ids, list):
        expected_document_id = str(entry.get("expected_document_id", "")).strip()
        if expected_document_id:
            fallback_terms.append(expected_document_id)
    return fallback_terms[:2]


def _document_iso(document_id: str) -> str:
    if "_" not in document_id:
        return ""
    return document_id.split("_")[-1].upper()


def _catalog_cases(document_id: str, source_path: str, blocks) -> list[EvaluationCase]:
    cases: list[EvaluationCase] = []
    locale_count = _find_line_value(blocks, row_key="Locale count")
    error_count = _find_line_value(blocks, row_key="Error count")

    if locale_count:
        cases.append(
            EvaluationCase(
                question="How many locales are listed in the Twilio SMS Guidelines Index?",
                expected_document_ids=[document_id],
                expected_source_paths=[source_path],
                expected_terms=["locale count", locale_count],
                expected_section_terms=["twilio sms guidelines index"],
                expected_anchor_terms=["locale count", locale_count],
                question_type="index_fact",
                should_refuse=False,
            )
        )
    if error_count:
        cases.append(
            EvaluationCase(
                question="How many scrape errors are listed in the Twilio SMS Guidelines Index?",
                expected_document_ids=[document_id],
                expected_source_paths=[source_path],
                expected_terms=["error count", error_count],
                expected_section_terms=["twilio sms guidelines index"],
                expected_anchor_terms=["error count", error_count],
                question_type="index_fact",
                should_refuse=False,
            )
        )
    return cases


def _find_simple_value(blocks, *, row_key: str) -> str | None:
    _block, value = _find_simple_fact(blocks, row_key=row_key)
    return value


def _find_simple_fact(blocks, *, row_key: str):
    for block in blocks:
        if block.metadata.get("row_key") != row_key:
            continue
        row_values = block.metadata.get("row_values", "")
        match = VALUE_PATTERN.search(row_values)
        if match:
            return block, match.group(1).strip()
        if row_values:
            return block, row_values.strip()
    return None, None


def _expected_block_types(block) -> list[str]:
    if block is None:
        return []
    block_type = str(getattr(block, "block_type", "")).strip()
    return [block_type] if block_type else []


def _sender_matrix_cases(
    document_id: str,
    source_path: str,
    locale_name: str,
    blocks,
) -> list[EvaluationCase]:
    cases: list[EvaluationCase] = []
    cases.extend(
        _sender_row_case(
            document_id,
            source_path,
            locale_name,
            blocks,
            section_hint="alphanumeric",
            row_key="Twilio supported",
            sender_type="alphanumeric sender id",
            question=f"Does {locale_name} support alphanumeric sender IDs?",
            question_type="binary",
        )
    )
    cases.extend(
        _sender_row_case(
            document_id,
            source_path,
            locale_name,
            blocks,
            section_hint="alphanumeric",
            row_key="Sender ID preserved",
            sender_type="alphanumeric sender id",
            question=f"Are alphanumeric sender IDs preserved in {locale_name}?",
            question_type="sender_type_policy",
        )
    )
    cases.extend(
        _sender_row_case(
            document_id,
            source_path,
            locale_name,
            blocks,
            section_hint="alphanumeric",
            row_key="Provisioning time",
            sender_type="alphanumeric sender id",
            question=f"What is the provisioning time for alphanumeric sender IDs in {locale_name}?",
            question_type="duration",
        )
    )
    cases.extend(
        _sender_row_case(
            document_id,
            source_path,
            locale_name,
            blocks,
            section_hint="long codes and short codes",
            row_key="Twilio supported",
            sender_type="short code",
            question=f"Are short codes supported in {locale_name}?",
            question_type="binary",
        )
    )
    cases.extend(
        _sender_row_case(
            document_id,
            source_path,
            locale_name,
            blocks,
            section_hint="long codes and short codes",
            row_key="Twilio supported",
            sender_type="long code",
            question=f"Are long codes supported in {locale_name}?",
            question_type="binary",
        )
    )
    cases.extend(
        _sender_row_case(
            document_id,
            source_path,
            locale_name,
            blocks,
            section_hint="long codes and short codes",
            row_key="Sender ID preserved",
            sender_type="long code",
            question=f"Are long-code sender IDs preserved in {locale_name}?",
            question_type="sender_type_policy",
        )
    )
    return cases


def _sender_row_case(
    document_id: str,
    source_path: str,
    locale_name: str,
    blocks,
    *,
    section_hint: str,
    row_key: str,
    sender_type: str,
    question: str,
    question_type: str,
) -> list[EvaluationCase]:
    block = _find_block(blocks, row_key=row_key, section_hint=section_hint)
    if block is None:
        return []
    value = _case_value(block, sender_type)
    if not _usable_case_value(value):
        return []
    return [
        EvaluationCase(
            question=question,
            expected_document_ids=[document_id],
            expected_source_paths=[source_path],
            expected_terms=_answer_terms_for_value(value, fallback=[sender_type]),
            expected_section_terms=[section_hint],
            expected_anchor_terms=[row_key, value],
            expected_block_types=_expected_block_types(block),
            expected_sender_types=[sender_type],
            expected_metadata={"row_key": row_key},
            expected_iso_code=_document_iso(document_id),
            must_not_mix_documents=True,
            question_type=question_type,
            should_refuse=False,
        )
    ]


def _infobip_profile_cases(
    document_id: str,
    source_path: str,
    locale_name: str,
    blocks,
) -> list[EvaluationCase]:
    specs = [
        (
            "Sender availability",
            "sender availability",
            f"What sender types are available in {locale_name}?",
            "capability",
        ),
        (
            "Sender provisioning",
            "sender provisioning",
            f"What is the sender provisioning process in {locale_name}?",
            "procedural",
        ),
        (
            "Service restrictions",
            "service restrictions",
            f"What service restrictions apply to SMS in {locale_name}?",
            "policy_rule",
        ),
        (
            "Country regulations",
            "country regulations",
            f"What country regulations apply to SMS in {locale_name}?",
            "policy_rule",
        ),
    ]
    cases: list[EvaluationCase] = []
    for row_key, expected_term, question, question_type in specs:
        block, value = _find_simple_fact(blocks, row_key=row_key)
        if block is None or not _usable_case_value(value):
            continue
        sender_types = _sender_types_from_text(value)
        cases.append(
            EvaluationCase(
                question=question,
                expected_document_ids=[document_id],
                expected_source_paths=[source_path],
                expected_terms=_answer_terms_for_value(value, fallback=[expected_term]),
                expected_section_terms=[],
                expected_anchor_terms=[row_key, value],
                expected_block_types=_expected_block_types(block),
                expected_sender_types=sender_types,
                expected_metadata={"row_key": row_key},
                expected_iso_code=_document_iso(document_id),
                must_not_mix_documents=True,
                question_type="sender_type_capability" if row_key == "Sender availability" and sender_types else question_type,
                should_refuse=False,
            )
        )
    return cases


def _compliance_profile_cases(
    document_id: str,
    source_path: str,
    locale_name: str,
    blocks,
) -> list[EvaluationCase]:
    block, value = _find_simple_fact(blocks, row_key="Compliance considerations")
    if block is None or not _usable_case_value(value):
        return []
    return [
        EvaluationCase(
            question=f"What compliance considerations apply to SMS in {locale_name}?",
            expected_document_ids=[document_id],
            expected_source_paths=[source_path],
            expected_terms=_answer_terms_for_value(value, fallback=["compliance considerations"]),
            expected_section_terms=[],
            expected_anchor_terms=["Compliance considerations", value],
            expected_block_types=_expected_block_types(block),
            expected_sender_types=_sender_types_from_text(value),
            expected_metadata={"row_key": "Compliance considerations"},
            expected_iso_code=_document_iso(document_id),
            must_not_mix_documents=True,
            question_type="policy_rule",
            should_refuse=False,
        )
    ]


def _find_block(blocks, *, row_key: str, section_hint: str):
    lowered_hint = section_hint.lower()
    for block in blocks:
        if block.metadata.get("row_key") != row_key:
            continue
        section = " > ".join(block.section_path).lower()
        if lowered_hint in section:
            return block
    return None


def _case_value(block, sender_type: str) -> str:
    metadata = getattr(block, "metadata", {})
    candidate_keys = _sender_value_keys(sender_type)
    values = [metadata.get(key, "").strip() for key in candidate_keys if metadata.get(key, "").strip()]
    if not values:
        values = [metadata.get("row_values", "").strip()]
    return "; ".join(dict.fromkeys(value for value in values if _usable_case_value(value)))


def _answer_terms_for_value(value: str, *, fallback: list[str]) -> list[str]:
    lowered = value.lower()
    if "not supported" in lowered or "not available" in lowered:
        return ["not supported"]
    if "not required" in lowered or "no sender registration needed" in lowered:
        return ["not required"]
    if re.search(r"\bno\b", lowered):
        return ["no"]
    if re.search(r"\byes\b", lowered):
        return ["yes"]
    duration_match = re.search(r"\b\d+(?:\s*[-–]\s*\d+)?\s*(?:day|days|week|weeks|month|months)\b", lowered)
    if duration_match:
        return [duration_match.group(0)]
    if "supported" in lowered or "available" in lowered:
        return ["supported"]
    if any(term in lowered for term in {"required", "registration", "register", "provisioning"}):
        return [fallback[0]]
    words = [word for word in tokenize_for_expected_terms(lowered) if len(word) > 3]
    return words[:2] or fallback


def tokenize_for_expected_terms(text: str) -> list[str]:
    return re.findall(r"[a-z0-9][a-z0-9+-]*", text.lower())


def _sender_value_keys(sender_type: str) -> list[str]:
    if sender_type == "alphanumeric sender id":
        return [
            "tag_column_international_pre_registration",
            "tag_column_domestic_pre_registration",
            "tag_column_pre_registration",
            "tag_column_dynamic",
        ]
    if sender_type == "short code":
        return ["tag_column_short_code"]
    if sender_type == "long code":
        return ["tag_column_long_code_domestic", "tag_column_long_code_international"]
    return []


def _usable_case_value(value: str | None) -> bool:
    if value is None:
        return False
    cleaned = value.strip().lower()
    return bool(cleaned) and cleaned not in {"---", "n/a", "na", "none", "null"}


def _sender_types_from_text(text: str) -> list[str]:
    lowered = text.lower()
    sender_types: list[str] = []
    if any(term in lowered for term in ("alpha", "alphanumeric")):
        sender_types.append("alphanumeric sender id")
    if "short code" in lowered or "shortcode" in lowered:
        sender_types.append("short code")
    if "toll-free" in lowered or "toll free" in lowered:
        sender_types.append("toll-free number")
    if "long code" in lowered or "longcode" in lowered or "vln" in lowered:
        sender_types.append("long code")
    return sender_types


def _fallback_block_types(case: EvaluationCase) -> list[str]:
    if _fallback_expected_metadata(case):
        return ["table_fact"]
    if case.question_type in {"table_extraction", "policy_rule", "procedural", "binary", "duration"}:
        return ["table_fact", "structured_fact", "policy_rule"]
    return []


def _fallback_expected_metadata(case: EvaluationCase) -> dict[str, str]:
    terms = " ".join([case.question, *case.expected_terms, *case.expected_anchor_terms]).lower()
    if "dialing code" in terms:
        return {"row_key": "Dialing code"}
    if "two-way sms" in terms or "two way sms" in terms:
        return {"row_key": "Two-way SMS supported"}
    if "number portability" in terms:
        return {"row_key": "Number portability available"}
    return {}


def _fallback_sender_types(case: EvaluationCase) -> list[str]:
    terms = " ".join([case.question, *case.expected_terms, *case.expected_anchor_terms]).lower()
    sender_types: list[str] = []
    if "alphanumeric" in terms or "alpha sender" in terms:
        sender_types.append("alphanumeric sender id")
    elif "sender id" in terms:
        sender_types.append("alphanumeric sender id")
    if "short code" in terms or "shortcode" in terms:
        sender_types.append("short code")
    if "toll-free" in terms or "toll free" in terms:
        sender_types.append("toll-free number")
    if "long code" in terms or "longcode" in terms:
        sender_types.append("long code")
    return sender_types


def _find_line_value(blocks, *, row_key: str) -> str | None:
    search_key = f"{row_key.lower()}:"
    for block in blocks:
        text = " ".join(block.text.split())
        idx = text.lower().find(search_key)
        if idx != -1:
            value_part = text[idx + len(search_key):].strip()
            return value_part.split()[0] if value_part else ""
    return None


def _locale_name(title: str, blocks) -> str:
    locale_name = _find_simple_value(blocks, row_key="Locale name")
    if locale_name:
        return locale_name
    return re.sub(r"\s+\([A-Z]{2,3}\)$", "", title).strip()


def _refusal_cases() -> list[EvaluationCase]:
    return [
        EvaluationCase(
            question="Does this corpus document moon geology?",
            expected_document_ids=[],
            expected_terms=[],
            question_type="refusal",
            should_refuse=True,
        ),
        EvaluationCase(
            question="What is the capital gains tax rate for Martian imports in this corpus?",
            expected_document_ids=[],
            expected_terms=[],
            question_type="refusal",
            should_refuse=True,
        ),
        EvaluationCase(
            question="Which chapters in this corpus explain protein folding?",
            expected_document_ids=[],
            expected_terms=[],
            question_type="refusal",
            should_refuse=True,
        ),
    ]


def _dedupe_cases(cases: list[EvaluationCase]) -> list[EvaluationCase]:
    deduped: list[EvaluationCase] = []
    seen_questions: set[str] = set()
    for case in cases:
        normalized_question = case.question.strip().lower()
        if normalized_question in seen_questions:
            continue
        deduped.append(case)
        seen_questions.add(normalized_question)
    return deduped


def _review_question(country: str, normalized_key: str) -> str:
    if normalized_key == "dialing code":
        return f"What is the dialing code for {country}?"
    if normalized_key == "two way sms supported":
        return f"Does {country} support two-way SMS?"
    if normalized_key == "number portability available":
        return f"Is number portability available in {country}?"
    return f"What does the corpus say about {normalized_key} in {country}?"


def _expected_terms_for_resolution(normalized_key: str, resolution_value: str) -> list[str]:
    value = resolution_value.strip().lower()
    if normalized_key in {"dialing code", "mcc", "mnc"}:
        return [value]
    return [value]


def _question_mentions_expected_doc(case: EvaluationCase) -> bool:
    if not case.expected_document_ids:
        return False
    doc_id = case.expected_document_ids[0]
    locale_hint = doc_id.rsplit("_", 1)[0].replace("_", " ").replace("-", " ").lower()
    question = case.question.lower()
    return locale_hint in question
