import json
import re
from dataclasses import dataclass
from pathlib import Path

from own_knowledge_rag.filename_metadata import build_country_index, extract_filename_metadata
from own_knowledge_rag.models import ParsedDocument

SUPPORTED_SUFFIX_ORDER = (".md", ".json", ".txt")
SUPPORTED_SUFFIXES = set(SUPPORTED_SUFFIX_ORDER)
SCHEMA_VERSION = "0.5.0"
QUOTE_TOKENS_TO_PRESERVE = ('"#Nevetscorp"', '"InfoSMS"', '"Verify"', '"01"', '"#"')
QUOTE_TOKEN_FIELDS_TO_PATCH = {"value", "answer", "source_quote"}


@dataclass(slots=True)
class DocumentValidationIssue:
    code: str
    message: str
    severity: str = "error"


class DocumentValidationError(ValueError):
    def __init__(self, path: Path, issues: list[DocumentValidationIssue]) -> None:
        self.path = path
        self.issues = issues
        issue_text = "; ".join(f"{issue.code}: {issue.message}" for issue in issues)
        super().__init__(f"{path}: {issue_text}")


def parse_file(path: Path) -> ParsedDocument | None:
    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_SUFFIXES:
        return None

    raw_text, encoding_detected, encoding_confidence, encoding_fallback, parse_warnings = _read_text_with_encoding(path)
    text = raw_text
    content_type = "markdown" if suffix == ".md" else "text"
    title = _infer_title(path, raw_text)

    if suffix == ".json":
        payload, repaired, restored_tokens = _load_json_payload(raw_text)
        if repaired:
            parse_warnings.append("json_repaired:escaped_unescaped_inner_quotes")
        if restored_tokens:
            parse_warnings.append("json_normalized:restored_known_quoted_tokens")
        text = _json_to_text(payload, default_title=path.stem.replace("-", " ").replace("_", " ").title())
        content_type = "json"
        title = _infer_json_title(path, payload) or title

    if not text.strip():
        return None

    filename_meta = extract_filename_metadata(path)

    document = ParsedDocument(
        document_id=path.stem,
        title=title,
        source_path=str(path),
        content_type=content_type,
        text=text.strip(),
        country=filename_meta.country,
        iso_code=filename_meta.iso_code,
        encoding_detected=encoding_detected,
        encoding_confidence=encoding_confidence,
        encoding_fallback=encoding_fallback,
        parse_warnings=parse_warnings,
    )
    validate_parsed_document(document, path=path)
    return document


def _read_text_with_encoding(path: Path) -> tuple[str, str, float, bool, list[str]]:
    raw_bytes = path.read_bytes()
    warnings: list[str] = []
    try:
        return raw_bytes.decode("utf-8"), "utf-8", 1.0, False, warnings
    except UnicodeDecodeError:
        pass

    detected = ""
    confidence = 0.0
    try:
        from charset_normalizer import from_bytes

        match = from_bytes(raw_bytes).best()
        if match is not None and match.encoding:
            detected = match.encoding
            confidence = round(float(getattr(match, "percent_coherence", 0.0) or 0.0) / 100, 4)
            text = str(match)
            if confidence < 0.8:
                detected = "cp1252"
                confidence = 0.0
                text = raw_bytes.decode("cp1252", errors="replace")
            warnings.append(f"encoding_fallback:{detected}")
            return text, detected, confidence, True, warnings
    except Exception as exc:
        warnings.append(f"encoding_detection_failed:{type(exc).__name__}")

    text = raw_bytes.decode("utf-8", errors="replace")
    warnings.append("encoding_fallback:utf-8-replace")
    return text, detected or "utf-8-replace", confidence, True, warnings


def validate_parsed_document(document: ParsedDocument, *, path: Path | None = None) -> None:
    issues = parsed_document_validation_issues(document, path=path)
    errors = [issue for issue in issues if issue.severity == "error"]
    if errors:
        raise DocumentValidationError(path or Path(document.source_path), errors)


def parsed_document_validation_issues(
    document: ParsedDocument,
    *,
    path: Path | None = None,
) -> list[DocumentValidationIssue]:
    issues: list[DocumentValidationIssue] = []
    source_path = path or Path(document.source_path)
    text = document.text.strip()
    content_type = document.content_type.strip().lower()

    if not document.document_id.strip():
        issues.append(DocumentValidationIssue("missing_document_id", "Document id is empty."))
    if not document.title.strip():
        issues.append(DocumentValidationIssue("missing_title", "Document title is empty."))
    if not document.source_path.strip():
        issues.append(DocumentValidationIssue("missing_source_path", "Document source path is empty."))
    if content_type not in {"markdown", "text", "json"}:
        issues.append(
            DocumentValidationIssue(
                "unsupported_content_type",
                f"Content type '{document.content_type}' is not supported.",
            )
        )
    if not text:
        issues.append(DocumentValidationIssue("empty_text", "Document text is empty after parsing."))
    if "\x00" in document.text:
        issues.append(DocumentValidationIssue("binary_text", "Document text contains NUL bytes."))
    if source_path.suffix.lower() == ".md" and content_type == "markdown":
        non_empty_lines = [line.strip() for line in document.text.splitlines() if line.strip()]
        if non_empty_lines and not any(line.startswith("#") for line in non_empty_lines):
            issues.append(
                DocumentValidationIssue(
                    "markdown_missing_heading",
                    "Markdown document has content but no heading.",
                    severity="warning",
                )
            )
    if source_path.suffix.lower() == ".json" and content_type != "json":
        issues.append(
            DocumentValidationIssue(
                "json_content_type_mismatch",
                "JSON source did not produce a JSON parsed document.",
            )
        )
    return issues


def normalize_allowed_suffixes(allowed_suffixes: list[str] | tuple[str, ...] | set[str] | None) -> tuple[str, ...]:
    if not allowed_suffixes:
        return SUPPORTED_SUFFIX_ORDER
    normalized = []
    for suffix in allowed_suffixes:
        value = str(suffix).strip().lower()
        if not value:
            continue
        if not value.startswith("."):
            value = f".{value}"
        if value in SUPPORTED_SUFFIXES and value not in normalized:
            normalized.append(value)
    return tuple(suffix for suffix in SUPPORTED_SUFFIX_ORDER if suffix in normalized)


def can_parse_file(path: Path, allowed_suffixes: list[str] | tuple[str, ...] | set[str] | None = None) -> bool:
    valid_suffixes = set(normalize_allowed_suffixes(allowed_suffixes))
    return path.is_file() and path.suffix.lower() in valid_suffixes


def _infer_title(path: Path, text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("# ").strip()
        if stripped:
            return stripped[:120]
    return path.stem.replace("-", " ").replace("_", " ").title()


def _infer_json_title(path: Path, payload: object) -> str | None:
    if isinstance(payload, dict):
        for key in ("locale_name", "title", "name"):
            value = payload.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
    return path.stem.replace("-", " ").replace("_", " ").title()


def _strip_json_code_fence(raw_text: str) -> str:
    text = raw_text.strip()
    if not text.startswith("```"):
        return raw_text

    lines = text.splitlines()
    if not lines:
        return raw_text
    opening = lines[0].strip().lower()
    if opening not in {"```", "```json", "```javascript", "```js"}:
        return raw_text

    body = lines[1:]
    if body and body[-1].strip() == "```":
        body = body[:-1]
    return "\n".join(body).strip()


def _load_json_payload(raw_text: str) -> tuple[object, bool, bool]:
    text = _strip_json_code_fence(raw_text)
    repaired = False
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as original_error:
        repaired_text = repair_json_text(text)
        if repaired_text == text:
            raise
        try:
            payload = json.loads(repaired_text)
            repaired = True
        except json.JSONDecodeError:
            raise original_error
    restored_tokens = restore_known_quoted_tokens_in_payload(payload)
    return payload, repaired, restored_tokens


def repair_json_text(raw_text: str) -> str:
    return _escape_unescaped_inner_json_quotes(_strip_json_code_fence(raw_text))


def normalize_json_text_for_ingestion(raw_text: str) -> str:
    payload, _repaired, _restored_tokens = _load_json_payload(raw_text)
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def restore_known_quoted_tokens_in_payload(payload: object) -> bool:
    changed = False
    if isinstance(payload, dict):
        for key, value in list(payload.items()):
            if key in QUOTE_TOKEN_FIELDS_TO_PATCH and isinstance(value, str):
                updated = _restore_known_quoted_tokens_in_string(value)
                if updated != value:
                    payload[key] = updated
                    changed = True
                continue
            if key == "local_aliases" and isinstance(value, list):
                updated_aliases = []
                for item in value:
                    if isinstance(item, str):
                        updated = _restore_known_quoted_tokens_in_string(item)
                        changed = changed or updated != item
                        updated_aliases.append(updated)
                    else:
                        changed = restore_known_quoted_tokens_in_payload(item) or changed
                        updated_aliases.append(item)
                payload[key] = updated_aliases
                continue
            changed = restore_known_quoted_tokens_in_payload(value) or changed
    elif isinstance(payload, list):
        for item in payload:
            changed = restore_known_quoted_tokens_in_payload(item) or changed
    return changed


def _restore_known_quoted_tokens_in_string(value: str) -> str:
    updated = value
    for quoted_token in QUOTE_TOKENS_TO_PRESERVE:
        bare_token = quoted_token.strip('"')
        pattern = re.compile(rf'(?<!["\w#]){re.escape(bare_token)}(?!["\w#])')
        updated = pattern.sub(quoted_token, updated)
    return updated


def _escape_unescaped_inner_json_quotes(text: str) -> str:
    repaired: list[str] = []
    in_string = False
    escaped = False

    for index, char in enumerate(text):
        if not in_string:
            repaired.append(char)
            if char == '"':
                in_string = True
                escaped = False
            continue

        if escaped:
            repaired.append(char)
            escaped = False
            continue

        if char == "\\":
            repaired.append(char)
            escaped = True
            continue

        if char == '"':
            next_nonspace = _next_nonspace_char(text, index + 1)
            if next_nonspace in {":", ",", "}", "]"}:
                repaired.append(char)
                in_string = False
            else:
                repaired.append('\\"')
            continue

        repaired.append(char)

    return "".join(repaired)


def _next_nonspace_char(text: str, start: int) -> str:
    for char in text[start:]:
        if not char.isspace():
            return char
    return ""


def _json_to_text(payload: object, default_title: str) -> str:
    if isinstance(payload, dict):
        source_facts = payload.get("source_facts")
        tables = payload.get("tables")
        if isinstance(source_facts, list):
            return _source_facts_payload_to_text(payload, default_title)
        enriched_items = _enriched_items(payload)
        if enriched_items and any(
            isinstance(item, dict) and isinstance(item.get("enriched_text"), str)
            for item in enriched_items
        ):
            return _enriched_blocks_payload_to_text(payload, default_title)
        if isinstance(tables, list) and tables:
            return _tables_payload_to_text(payload, default_title)
        if "locales" in payload and isinstance(payload.get("locales"), list):
            return _catalog_payload_to_text(payload, default_title)
    if isinstance(payload, list):
        if _looks_like_source_fact_items(payload):
            return _source_facts_payload_to_text({"source_facts": payload}, default_title)
        if _looks_like_enriched_items(payload):
            return _enriched_blocks_payload_to_text({"results": payload}, default_title)

    lines = [f"# {default_title}", ""]
    lines.extend(_flatten_json(payload, level=2))
    return "\n".join(line for line in lines if line is not None).strip()


def _looks_like_source_fact_items(items: list[object]) -> bool:
    dict_items = [item for item in items if isinstance(item, dict)]
    if not dict_items:
        return False
    fact_markers = {"fact_id", "fact_type", "topic", "value", "structured_fields", "source_anchor"}
    return any(bool(fact_markers.intersection(item.keys())) and isinstance(item.get("value"), str) for item in dict_items)


def _looks_like_enriched_items(items: list[object]) -> bool:
    dict_items = [item for item in items if isinstance(item, dict)]
    if not dict_items:
        return False
    return any(isinstance(item.get("enriched_text"), str) for item in dict_items)


def _source_facts_payload_to_text(payload: dict[str, object], default_title: str) -> str:
    title = _infer_json_title(Path(default_title), payload) or str(payload.get("document_title") or default_title)
    lines = [f"# {title}", ""]

    content_type = payload.get("content_type")
    if isinstance(content_type, str) and content_type.strip():
        lines.append(f"Content type: {content_type.strip()}")
        lines.append("")

    source_facts = payload.get("source_facts")
    if isinstance(source_facts, list):
        lines.append("## Source Facts")
        lines.append("")
        for item in source_facts:
            if not isinstance(item, dict):
                continue
            field = str(item.get("field") or item.get("fact_type") or item.get("topic") or item.get("fact_id") or "").strip()
            value = _json_scalar(item.get("value"))
            if not field or not value:
                continue
            parts = [f"Value={value}"]
            structured_fields = item.get("structured_fields")
            if isinstance(structured_fields, dict):
                for key, raw_value in structured_fields.items():
                    text = _json_scalar(raw_value)
                    if text:
                        parts.append(f"{key}={text}")
            for key in (
                "fact_id",
                "fact_type",
                "topic",
                "unit",
                "applies_to",
                "conditions",
                "condition",
                "exceptions",
                "notes",
                "country_iso2",
                "operator_name",
                "source_anchor",
                "source_quote",
            ):
                text = _json_scalar(item.get(key))
                if text and f"{key}={text}" not in parts:
                    parts.append(f"{key}={text}")
            local_aliases = item.get("local_aliases")
            if isinstance(local_aliases, list):
                aliases = ", ".join(_json_scalar(alias) for alias in local_aliases if _json_scalar(alias))
                if aliases:
                    parts.append(f"local_aliases={aliases}")
            lines.append(f"- {field}: {'; '.join(parts)}")
        lines.append("")

    tables = payload.get("tables")
    if isinstance(tables, list) and tables:
        table_text = _tables_payload_to_text({"tables": tables, "locale_name": title}, default_title)
        lines.extend(table_text.splitlines()[2:])

    notes = payload.get("notes")
    if isinstance(notes, list) and notes:
        lines.append("## Notes")
        lines.append("")
        for note in notes:
            text = _json_scalar(note)
            if text:
                lines.append(f"- {text}")

    return "\n".join(line for line in lines if line is not None).strip()


def _enriched_blocks_payload_to_text(payload: dict[str, object], default_title: str) -> str:
    title = _infer_json_title(Path(default_title), payload) or default_title
    lines = [f"# {title}", "", "## Source Facts", ""]
    country_index = build_country_index()

    enriched_items = _enriched_items(payload)
    if not enriched_items:
        return "\n".join(lines).strip()

    for item in enriched_items:
        if not isinstance(item, dict):
            continue
        value = _json_scalar(item.get("enriched_text"))
        if not value:
            continue
        country = _json_scalar(item.get("country"))
        iso = _json_scalar(item.get("iso_code")).upper()
        if not iso and country:
            iso = country_index.get(country.lower(), "")
        regulation_topics = item.get("regulation_topics")
        fact_type = _fact_type_from_topics(regulation_topics, value)
        parts = [f"Value={value}"]
        if country:
            parts.append(f"country_name={country}")
        if iso:
            parts.append(f"country_iso2={iso}")
        for key in ("block_id", "answer_signal", "source_category"):
            text = _json_scalar(item.get(key))
            if text:
                parts.append(f"{key}={text}")
        for key in ("sender_types", "regulation_topics", "local_aliases", "hypothetical_questions"):
            text = _json_scalar(item.get(key))
            if text:
                parts.append(f"{key}={text}")
        lines.append(f"- {fact_type}: {'; '.join(parts)}")

    return "\n".join(line for line in lines if line is not None).strip()


def _enriched_items(payload: dict[str, object]) -> list[object]:
    for key in ("blocks", "results"):
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return []


def _fact_type_from_topics(topics: object, value: str = "") -> str:
    text = _json_scalar(topics).lower()
    value_text = value.lower()
    if "content restriction" in text and "sunday sending is not allowed" in value_text:
        return "content_restriction"
    if "quiet" in text or "do not disturb" in text or "dnd" in text:
        return "quiet_hours"
    if "registration" in text or "pre-registration" in text:
        return "registration"
    if "routing" in text or "route" in text:
        return "routing"
    if "restriction" in text or "prohibited" in text:
        return "content_restriction"
    if "two-way" in text or "capability" in text:
        return "sms_capability"
    return "other"


def _tables_payload_to_text(payload: dict[str, object], default_title: str) -> str:
    title = _infer_json_title(Path(default_title), payload) or default_title
    lines = [f"# {title}", ""]

    source_url = payload.get("source_url")
    locale_code = payload.get("locale_code")
    if isinstance(source_url, str) and source_url.strip():
        lines.append(f"Source: {source_url.strip()}")
    if isinstance(locale_code, str) and locale_code.strip():
        lines.append(f"Locale code: {locale_code.strip()}")
    if len(lines) > 2:
        lines.append("")

    for table in payload.get("tables", []):
        if not isinstance(table, dict):
            continue
        table_title = str(table.get("title") or "Table").strip()
        section = str(table.get("section") or "").strip()
        heading = table_title if not section else f"{table_title}: {section}"
        lines.append(f"## {heading}")
        lines.append("")

        table_type = str(table.get("type") or "").strip()
        items = table.get("items")
        if not isinstance(items, list):
            continue

        if table_type == "key_value":
            for item in items:
                if not isinstance(item, dict):
                    continue
                field = str(item.get("field") or "").strip()
                description = str(item.get("description") or "").strip()
                value = str(item.get("value") or "").strip()
                if not field or not value:
                    continue
                parts = []
                if description:
                    parts.append(f"Description={description}")
                parts.append(f"Value={value}")
                lines.append(f"- {field}: {'; '.join(parts)}")
            lines.append("")
            continue

        if table_type == "matrix":
            for item in items:
                if not isinstance(item, dict):
                    continue
                field = str(item.get("field") or "").strip()
                description = str(item.get("description") or "").strip()
                values = item.get("values")
                if not field or not isinstance(values, dict):
                    continue
                parts = []
                if description:
                    parts.append(f"Description={description}")
                for column, value in values.items():
                    column_label = str(column).strip()
                    value_text = str(value).strip()
                    if column_label and value_text:
                        parts.append(f"{column_label}={value_text}")
                if parts:
                    lines.append(f"- {field}: {'; '.join(parts)}")
            lines.append("")
            continue

        lines.extend(_flatten_json(table, level=0))
        lines.append("")

    return "\n".join(line for line in lines if line is not None).strip()


def _catalog_payload_to_text(payload: dict[str, object], default_title: str) -> str:
    title = _infer_json_title(Path(default_title), payload) or default_title
    lines = [f"# {title}", ""]

    source_url = payload.get("source_index_url")
    locale_count = payload.get("locale_count")
    if isinstance(source_url, str) and source_url.strip():
        lines.append(f"Source index: {source_url.strip()}")
    if locale_count is not None:
        lines.append(f"Locale count: {locale_count}")
    lines.append("")
    lines.append("## Locales")
    lines.append("")

    for item in payload.get("locales", []):
        if not isinstance(item, dict):
            continue
        locale_name = str(item.get("locale_name") or item.get("title") or "").strip()
        source = str(item.get("source_url") or "").strip()
        locale_code = str(item.get("locale_code") or "").strip()
        if not locale_name:
            continue
        parts = []
        if locale_code:
            parts.append(f"Locale code={locale_code}")
        if source:
            parts.append(f"Source URL={source}")
        if parts:
            lines.append(f"- {locale_name}: {'; '.join(parts)}")
        else:
            lines.append(f"- {locale_name}")

    return "\n".join(lines).strip()


def _flatten_json(payload: object, level: int) -> list[str]:
    lines: list[str] = []
    if isinstance(payload, dict):
        for key, value in payload.items():
            key_label = str(key).strip()
            heading = key_label.replace("_", " ").strip().title()
            if isinstance(value, (dict, list)):
                lines.append(f"{'#' * min(max(level, 2), 6)} {heading}")
                lines.append("")
                lines.extend(_flatten_json(value, level + 1))
                lines.append("")
            else:
                text = _json_scalar(value)
                if text:
                    lines.append(f"- {key_label}: {text}")
        return lines

    if isinstance(payload, list):
        for item in payload:
            if isinstance(item, dict):
                label = _list_item_label(item)
                if label:
                    lines.append(f"- {label}")
                else:
                    lines.extend(_flatten_json(item, level + 1))
            elif isinstance(item, list):
                lines.extend(_flatten_json(item, level + 1))
            else:
                text = _json_scalar(item)
                if text:
                    lines.append(f"- {text}")
        return lines

    text = _json_scalar(payload)
    return [f"- {text}"] if text else []


def _json_scalar(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return ", ".join(_json_scalar(item) for item in value if _json_scalar(item))
    if isinstance(value, dict):
        parts = []
        for key, raw_value in value.items():
            text = _json_scalar(raw_value)
            if text:
                parts.append(f"{key}={text}")
        return "; ".join(parts)
    text = str(value).strip()
    return text


def _list_item_label(item: dict[str, object]) -> str:
    for key in ("field", "title", "name", "locale_name"):
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""
