import re
from dataclasses import dataclass

from own_knowledge_rag.models import KnowledgeBlock, ParsedDocument

SCHEMA_VERSION = "0.4.0"
SHORT_FACT_BLOCK_TYPES = {"table_fact", "list_item", "structured_fact", "policy_rule"}


@dataclass(slots=True)
class SectionUnit:
    text: str
    original_text: str
    metadata: dict[str, str]
    relative_offset: int


@dataclass(slots=True)
class SectionSpan:
    path: list[str]
    body: str
    start_offset: int


def normalize_document(
    document: ParsedDocument,
    chunk_size: int = 800,
    chunk_overlap: int = 120,
) -> list[KnowledgeBlock]:
    text = document.text
    code_block_count = 0
    if document.content_type == "markdown":
        text, code_block_count = _normalize_markdown(text)

    document_kind = _classify_document_kind(document.title, text)
    sections = _split_sections(text)
    document_scope = _classify_document_scope(document.title, text, document_kind)
    blocks: list[KnowledgeBlock] = []
    block_index = 0

    for section in sections:
        section_path = section.path
        heading_context = section_path[-1] if section_path else None
        for unit in _split_units(section.body, heading_context, chunk_size, chunk_overlap):
            clean_unit = unit.text.strip()
            clean_original = unit.original_text.strip()
            if not clean_unit:
                continue
            block_type = _infer_block_type(
                clean_unit,
                document_kind=document_kind,
                content_type=document.content_type,
            )
            if unit.metadata.get("code_language") is not None:
                block_type = "code_sample"
            metadata = _block_metadata(
                document,
                section_path,
                clean_unit,
                block_type,
                document_kind,
                document_scope,
                unit.metadata,
            )
            if code_block_count:
                metadata["code_blocks_preserved"] = str(code_block_count)
                metadata["code_blocks_erased"] = "0"
            
            channels = _detect_channels(clean_unit, section_path)
            
            quality_status = _initial_quality_status(clean_unit, block_type)
                
            block_index += 1
            char_offset = max(0, section.start_offset + unit.relative_offset)

            blocks.append(
                KnowledgeBlock(
                    block_id=f"{document.document_id}-block-{block_index}",
                    document_id=document.document_id,
                    title=document.title,
                    section_path=section_path,
                    section_heading=heading_context or "",
                    block_type=block_type,
                    text=clean_unit,
                    source_path=document.source_path,
                    start_anchor=_anchor(clean_original, True),
                    end_anchor=_anchor(clean_original, False),
                    block_index=block_index,
                    char_offset=char_offset,
                    country=document.country,
                    iso_code=document.iso_code,
                    channels=channels,
                    quality_status=quality_status,
                    metadata=metadata,
                )
            )

    return blocks


def _initial_quality_status(text: str, block_type: str) -> str:
    if block_type == "code_sample":
        return "ok" if len(text.strip()) >= 15 else "LOW_QUALITY"
    if block_type in SHORT_FACT_BLOCK_TYPES:
        return "LOW_QUALITY" if len(text.strip()) < 15 else "ok"
    return "LOW_QUALITY" if len(text.strip()) < 50 else "ok"


def _normalize_markdown(text: str) -> tuple[str, int]:
    code_blocks = re.findall(r"(?ms)^```.*?^```[\t ]*(?:\n|$)", text)
    return text, len(code_blocks)


def _split_sections(text: str) -> list[SectionSpan]:
    lines = text.splitlines(keepends=True)
    stack: list[str] = []
    body_parts: list[tuple[str, int]] = []
    sections: list[SectionSpan] = []

    def flush() -> None:
        if not body_parts:
            return
        raw_body = "".join(part for part, _ in body_parts)
        leading_trim = len(raw_body) - len(raw_body.lstrip())
        body = raw_body.strip()
        if body:
            sections.append(SectionSpan(stack.copy(), body, body_parts[0][1] + leading_trim))

    cursor = 0
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            flush()
            body_parts = []
            heading = stripped.lstrip("# ").strip()
            level = len(stripped) - len(stripped.lstrip("#"))
            stack[:] = stack[: max(level - 1, 0)]
            stack.append(heading)
            cursor += len(line)
            continue
        body_parts.append((line, cursor))
        cursor += len(line)

    flush()
    return sections or [SectionSpan([], text, 0)]


def _split_units(body: str, heading_context: str | None, chunk_size: int, chunk_overlap: int) -> list[SectionUnit]:
    units: list[SectionUnit] = []
    for paragraph, paragraph_offset in _paragraph_spans(body):
        lines = paragraph.splitlines()
        if _looks_like_fenced_code_block(paragraph):
            units.append(_code_block_to_unit(paragraph, paragraph_offset))
            continue
        if len(lines) >= 3 and _looks_like_table_header(lines, 0):
            units.extend(_table_to_units(lines, heading_context, paragraph_offset))
            continue

        bullet_lines = [line.strip() for line in lines if line.strip().startswith("- ")]
        if bullet_lines and len(bullet_lines) == len([line for line in lines if line.strip()]):
            for index, raw_line in enumerate(lines):
                line = raw_line.strip()
                if line:
                    units.append(SectionUnit(line, line, {}, paragraph_offset + _line_offset(lines, index)))
        else:
            if len(paragraph) > chunk_size:
                units.extend(_sentence_chunk_units(paragraph, paragraph_offset, heading_context, chunk_size, chunk_overlap))
            else:
                chunk_text = paragraph
                if heading_context:
                    chunk_text = f"[{heading_context}] {chunk_text}"
                units.append(SectionUnit(chunk_text, paragraph, {}, paragraph_offset))
    return units


def _infer_block_type(text: str, *, document_kind: str, content_type: str = "") -> str:
    lowered = text.lower()
    if document_kind == "catalog" and (text.startswith("- ") or text.startswith("Regarding ") or text.startswith("For ") or text.startswith("The ")):
        return "catalog_entry"
    if content_type == "json" and _looks_like_structured_json_fact(text):
        return "structured_fact"
    if lowered.startswith("- faq:") or lowered.endswith("?"):
        return "faq"
    
    # Procedure detection
    if re.match(r"^\s*(step\s+\d+|[0-9]+\.)\s+", lowered) or \
       lowered.startswith("how to") or lowered.startswith("to start") or \
       " follow these " in lowered or " steps to " in lowered:
        return "procedure_step"

    # Policy Rule detection
    if " must " in f" {lowered} " or " should " in f" {lowered} " or \
       " required" in lowered or " mandatory" in lowered or \
       " restricted" in lowered or " prohibited" in lowered:
        return "policy_rule"

    if re.match(r"^\s*[-*]\s+", text):
        return "table_fact" if ":" in text[:120] else "list_item"
    if text.startswith("Regarding ") or text.startswith("For ") or (text.startswith("The ") and " is: " in text):
        return "table_fact"
    if _looks_like_key_value_fact(text):
        return "table_fact"
    
    return "narrative"


def _paragraph_spans(body: str) -> list[tuple[str, int]]:
    spans: list[tuple[str, int]] = []
    for match in re.finditer(r"(?s)(.*?)(?:\n\s*\n|$)", body):
        raw = match.group(1)
        if not raw.strip():
            continue
        leading_trim = len(raw) - len(raw.lstrip())
        spans.append((raw.strip(), match.start(1) + leading_trim))
        if match.end() >= len(body):
            break
    return spans


def _looks_like_fenced_code_block(paragraph: str) -> bool:
    stripped = paragraph.strip()
    return stripped.startswith("```") and stripped.endswith("```") and len(stripped.splitlines()) >= 2


def _code_block_to_unit(paragraph: str, paragraph_offset: int) -> SectionUnit:
    lines = paragraph.strip().splitlines()
    opening = lines[0].strip()
    language = opening.removeprefix("```").strip().lower()
    body_lines = lines[1:]
    if body_lines and body_lines[-1].strip() == "```":
        body_lines = body_lines[:-1]
    code = "\n".join(body_lines).strip()
    text = f"Code sample ({language or 'plain text'}):\n{code}" if code else f"Code sample ({language or 'plain text'})."
    return SectionUnit(
        text=text,
        original_text=paragraph,
        metadata={"code_language": language, "code_block_preserved": "true"},
        relative_offset=paragraph_offset,
    )


def _sentence_chunk_units(
    paragraph: str,
    paragraph_offset: int,
    heading_context: str | None,
    chunk_size: int,
    chunk_overlap: int,
) -> list[SectionUnit]:
    sentence_spans = _sentence_spans(paragraph)
    if len(sentence_spans) <= 1:
        return _character_chunk_units(paragraph, paragraph_offset, heading_context, chunk_size, chunk_overlap)

    units: list[SectionUnit] = []
    start_index = 0
    min_size = max(1, int(chunk_size * 0.9))
    max_size = max(min_size, int(chunk_size * 1.1))
    while start_index < len(sentence_spans):
        chunk_start = sentence_spans[start_index][0]
        end_index = start_index
        while end_index < len(sentence_spans):
            chunk_end = sentence_spans[end_index][1]
            current_len = chunk_end - chunk_start
            if current_len >= min_size:
                if current_len <= max_size or end_index == start_index:
                    end_index += 1
                break
            end_index += 1
        if end_index <= start_index:
            end_index = start_index + 1
        chunk_end = sentence_spans[end_index - 1][1]
        original = paragraph[chunk_start:chunk_end].strip()
        text = f"[{heading_context}] {original}" if heading_context else original
        units.append(SectionUnit(text, original, {}, paragraph_offset + chunk_start))

        if end_index >= len(sentence_spans):
            break
        overlap_start = end_index
        overlap_len = 0
        while overlap_start > start_index:
            candidate_start = sentence_spans[overlap_start - 1][0]
            overlap_len = chunk_end - candidate_start
            if overlap_len > chunk_overlap and overlap_start < end_index:
                break
            if overlap_len > chunk_overlap:
                break
            overlap_start -= 1
        start_index = max(overlap_start, start_index + 1)
    return units


def _sentence_spans(text: str) -> list[tuple[int, int]]:
    try:
        import pysbd

        segmenter = pysbd.Segmenter(language="en", clean=False)
        sentences = segmenter.segment(text)
        spans: list[tuple[int, int]] = []
        cursor = 0
        for sentence in sentences:
            start = text.find(sentence, cursor)
            if start == -1:
                continue
            end = start + len(sentence)
            spans.append((start, end))
            cursor = end
        if spans:
            return spans
    except Exception:
        pass

    spans = []
    start = 0
    for match in re.finditer(r"(?<=[.!?])\s+(?=[A-Z0-9])", text):
        end = match.start()
        if text[start:end].strip():
            spans.append((start, end))
        start = match.end()
    if text[start:].strip():
        spans.append((start, len(text)))
    return spans


def _character_chunk_units(
    paragraph: str,
    paragraph_offset: int,
    heading_context: str | None,
    chunk_size: int,
    chunk_overlap: int,
) -> list[SectionUnit]:
    units: list[SectionUnit] = []
    start = 0
    step = max(1, chunk_size - max(0, chunk_overlap))
    while start < len(paragraph):
        end = min(len(paragraph), start + chunk_size)
        if end < len(paragraph):
            whitespace = paragraph.rfind(" ", start, end)
            if whitespace > start + int(chunk_size * 0.5):
                end = whitespace
        original = paragraph[start:end].strip()
        if original:
            text = f"[{heading_context}] {original}" if heading_context else original
            units.append(SectionUnit(text, original, {}, paragraph_offset + start))
        if end >= len(paragraph):
            break
        start = max(start + step, end - chunk_overlap)
    return units


def _anchor(text: str, from_start: bool) -> str:
    normalized = " ".join(text.split())
    if len(normalized) <= 80:
        return normalized
    return normalized[:80] if from_start else normalized[-80:]


def _looks_like_table_header(lines: list[str], index: int) -> bool:
    if index + 1 >= len(lines):
        return False
    first = lines[index].strip()
    second = lines[index + 1].strip()
    return first.startswith("|") and second.startswith("|") and "-" in second


def _table_to_units(lines: list[str], heading_context: str | None, paragraph_offset: int = 0) -> list[SectionUnit]:
    rows = [_parse_table_row(line) for line in lines]
    if len(rows) < 3 or len(rows[0]) < 2:
        return [SectionUnit(line, line, {}, paragraph_offset) for line in lines]

    headers = [_clean_cell(cell) for cell in rows[0]]
    units: list[SectionUnit] = []
    
    is_kv = False
    if len(headers) >= 2:
        h1 = headers[0].lower()
        if h1 in ("key", "field", "property", "attribute", "name"):
            # Check if any subsequent header implies a value column
            if any(h.lower() in ("value", "details") for h in headers[1:]):
                is_kv = True
            elif len(headers) == 2 and headers[1].lower() in ("description",):
                is_kv = True

    # Build a compact string of the full row's col→val mapping for semantic mapper context.
    # Format: "Col1: val1 | Col2: val2 | …" (plain string; metadata values must be str).
    raw_headers_str = " | ".join(headers)

    for i, row in enumerate(rows[2:], start=2):
        original_line = lines[i]
        if len(row) < 2:
            continue
        key = _clean_cell(row[0])
        values = [_clean_cell(cell) for cell in row[1:]]
        if not key or not any(values):
            continue
            
        tags = {}
        # Build compact row-dict string: "Field: val | Description: val | …"
        raw_row_parts = []
        for h, v in zip(headers, [_clean_cell(c) for c in row], strict=False):
            if h and v:
                raw_row_parts.append(f"{h}: {v}")
        tags["raw_table_headers"] = raw_headers_str
        tags["raw_table_row_dict"] = " | ".join(raw_row_parts)
        if is_kv or (len(headers) <= 2 and len(values) == 1):
            # For KV tables with more than 2 columns (e.g. Field | Description | Value), 
            # usually the last column or the one named 'Value' contains the actual value.
            # We'll just extract the last non-empty value, or the specific 'Value' column.
            val_idx = -1
            for idx, h in enumerate(headers[1:]):
                if h.lower() == "value":
                    val_idx = idx
            
            if val_idx >= 0 and val_idx < len(values):
                value = values[val_idx]
            else:
                value = values[-1] if values else ""
                
            if not value:
                continue
            
            if heading_context:
                nl_text = f"For {heading_context}, the {key} is: {value}."
            else:
                nl_text = f"The {key} is: {value}."
            
            tags["tag_attribute"] = key
            tags["row_key"] = key
            tags["row_values"] = value
            tags["tag_table_type"] = "key_value"
            units.append(SectionUnit(nl_text, original_line, tags, paragraph_offset + _line_offset(lines, i)))
        else:
            entity = key
            tags["tag_entity"] = entity
            tags["row_key"] = entity
            tags["tag_table_type"] = "matrix"
            
            parts = []
            for header, value in zip(headers[1:], values, strict=False):
                if value and header and value.lower() not in ("n/a", "---", "none"):
                    clean_tag_name = "tag_column_" + re.sub(r'[^a-z0-9]+', '_', header.lower()).strip('_')
                    tags[clean_tag_name] = value
                    # Improve phrasing for matrix rows
                    parts.append(f"the {header} is {value}")
            
            if not parts:
                continue
                
            parts_str = ", ".join(parts)
            if heading_context:
                nl_text = f"Regarding {heading_context} for {entity}: {parts_str}."
            else:
                nl_text = f"For {entity}: {parts_str}."
                
            tags["row_values"] = parts_str
            units.append(SectionUnit(nl_text, original_line, tags, paragraph_offset + _line_offset(lines, i)))
        
    return units


def _line_offset(lines: list[str], index: int) -> int:
    return sum(len(line) + 1 for line in lines[:index])


def _parse_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _clean_cell(value: str) -> str:
    value = re.sub(r"\[(.*?)\]\((.*?)\)", r"\1", value)
    return " ".join(value.split())


def _classify_document_kind(title: str, text: str) -> str:
    lowered_title = title.lower()
    lowered_text = text.lower()
    if "index" in lowered_title:
        return "catalog"
    if "source index:" in lowered_text and "locale count:" in lowered_text:
        return "catalog"
    return "knowledge"


def _classify_document_scope(title: str, text: str, document_kind: str) -> str:
    lowered_title = title.lower()
    if document_kind == "catalog":
        return "catalog"
    if re.search(r"\([A-Z]{2,3}\)", title) or re.search(r"__[0-9]{3,4}$", title):
        return "profile"
    if "country information guide" in lowered_title or "coverage and connectivity" in lowered_title:
        return "aggregate"
    if len(re.findall(r"^###\s+", text, flags=re.M)) >= 8:
        return "profile" # High heading density usually implies a detailed profile
    return "general"


def _detect_channels(text: str, section_path: list[str]) -> list[str]:
    haystack = " ".join([text, *section_path]).lower()
    patterns = {
        "sms": r"\bsms\b|short message service",
        "mms": r"\bmms\b|multimedia message service",
        "rcs": r"\brcs\b|rich communication services?",
        "whatsapp": r"\bwhatsapp\b",
        "voice": r"\bvoice\b|phone call|calling",
    }
    return sorted(channel for channel, pattern in patterns.items() if re.search(pattern, haystack))


def _block_metadata(
    document: ParsedDocument,
    section_path: list[str],
    text: str,
    block_type: str,
    document_kind: str,
    document_scope: str,
    table_tags: dict[str, str] | None = None,
) -> dict[str, str]:
    metadata: dict[str, str] = {
        "schema_version": SCHEMA_VERSION,
        "content_type": document.content_type,
        "document_kind": document_kind,
        "document_scope": document_scope,
        "section_path": " > ".join(section_path),
    }

    if block_type in {"table_fact", "catalog_entry", "structured_fact"}:
        key, values = _extract_key_value_metadata(text, section_path)
        if key:
            metadata["row_key"] = key
            if block_type == "structured_fact":
                metadata["structured_field"] = key
        if values:
            metadata["row_values"] = values
            structured_value = _extract_structured_value(values)
            if block_type == "structured_fact" and structured_value:
                metadata["structured_value"] = structured_value
        if _looks_placeholder_heavy(text):
            metadata["informative"] = "low"
        else:
            metadata["informative"] = "high"
        if block_type == "structured_fact":
            metadata["structured_source"] = document.content_type

    if table_tags:
        for k, v in table_tags.items():
            metadata[k] = v

    return metadata


def _extract_key_value_metadata(text: str, section_path: list[str]) -> tuple[str, str]:
    stripped = text.lstrip("- ").strip()
    if ":" not in stripped:
        return "", ""
    key, remainder = stripped.split(":", 1)
    key = key.strip()
    remainder = remainder.strip()

    current_section = section_path[-1].strip().lower() if section_path else ""
    if current_section and key.lower() == current_section and ":" in remainder:
        nested_key, nested_remainder = remainder.split(":", 1)
        return nested_key.strip(), nested_remainder.strip()

    return key, remainder


def _looks_placeholder_heavy(text: str) -> bool:
    lowered = text.lower()
    placeholder_count = sum(lowered.count(marker) for marker in ["n/a", "---", "-----", "/"])
    return placeholder_count >= 2


def _looks_like_key_value_fact(text: str) -> bool:
    if "\n" in text:
        return False
    stripped = text.strip()
    if stripped.startswith(("- ", "* ")):
        return False
    if ":" not in stripped:
        return False
    key, remainder = stripped.split(":", 1)
    key = key.strip()
    remainder = remainder.strip()
    if not key or not remainder:
        return False
    if len(key) > 80:
        return False
    return bool(re.match(r"^[A-Za-z0-9][A-Za-z0-9 ()&/'_-]*$", key))


def _looks_like_structured_json_fact(text: str) -> bool:
    stripped = text.lstrip("-* ").strip()
    if ":" not in stripped:
        return False
    key, remainder = stripped.split(":", 1)
    key = key.strip()
    remainder = remainder.strip()
    return bool(key and remainder and len(key) <= 120)


def _extract_structured_value(values: str) -> str:
    for pattern in (r"(?:^|;\s*)Value=([^;]+)", r"(?:^|;\s*)value=([^;]+)"):
        match = re.search(pattern, values)
        if match:
            return match.group(1).strip()
    return values.strip()
