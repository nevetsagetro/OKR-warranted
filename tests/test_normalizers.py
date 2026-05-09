import pytest
from pathlib import Path

from own_knowledge_rag.models import ParsedDocument
from own_knowledge_rag.normalizers import normalize_document


def test_markdown_tables_become_row_level_blocks() -> None:
    document = ParsedDocument(
        document_id="spain_es",
        title="Spain",
        source_path="data/raw/spain_es.md",
        content_type="markdown",
        text="""# Spain

## Sender
| Key | Value |
| --- | --- |
| Sender provisioning | No sender registration needed. |
| Two-way | Supported |
""",
    )

    blocks = normalize_document(document)

    assert any("For Sender, the Sender provisioning is: No sender registration needed." in block.text for block in blocks)
    assert any("For Sender, the Two-way is: Supported." in block.text for block in blocks)


def test_markdown_multi_column_tables_matrix_rows_drop_placeholders() -> None:
    """Matrix tables should drop placeholder-only columns and produce 'Regarding … for …' blocks."""
    document = ParsedDocument(
        document_id="spain_es",
        title="Spain",
        source_path="data/raw/spain_es.md",
        content_type="markdown",
        text="""# Spain

## Phone Numbers & Sender ID
| Field | Description | Pre-registration | Dynamic |
| --- | --- | --- | --- |
| Twilio supported | Whether Twilio supports the feature. | --- | Supported |
| Sender ID preserved | Whether the sender is preserved. | --- | Yes |
""",
    )

    blocks = normalize_document(document)
    texts = [b.text for b in blocks]

    # Matrix table: entity is first column, columns = attributes; placeholders dropped
    assert any("Twilio supported" in t and "Supported" in t for t in texts)
    assert any("Sender ID preserved" in t and "Yes" in t for t in texts)
    # Placeholder columns (---) should NOT appear in the block text
    assert not any("Pre-registration is ---" in t for t in texts)


def test_short_table_facts_are_not_low_quality() -> None:
    document = ParsedDocument(
        document_id="spain_es",
        title="Spain",
        source_path="data/raw/spain_es.md",
        content_type="markdown",
        text="""# Spain

## Sender
| Key | Value |
| --- | --- |
| Pre-registration | Yes |
""",
    )

    blocks = normalize_document(document)

    assert len(blocks) == 1
    assert blocks[0].block_type == "table_fact"
    assert blocks[0].quality_status == "ok"


def test_json_key_value_rows_become_structured_facts() -> None:
    document = ParsedDocument(
        document_id="spain_es",
        title="Spain (ES)",
        source_path="data/raw/spain_es.json",
        content_type="json",
        text="""# Spain (ES)

## Locale Summary

- Dialing code: Description=Country calling code.; Value=+34
- iso2: ES
""",
        country="Spain",
        iso_code="ES",
    )

    blocks = normalize_document(document)
    dialing_block = next(block for block in blocks if block.metadata.get("row_key") == "Dialing code")
    iso_block = next(block for block in blocks if block.metadata.get("row_key") == "iso2")

    assert dialing_block.block_type == "structured_fact"
    assert dialing_block.metadata["structured_source"] == "json"
    assert dialing_block.metadata["structured_field"] == "Dialing code"
    assert dialing_block.metadata["structured_value"] == "+34"
    assert dialing_block.quality_status == "ok"
    assert iso_block.block_type == "structured_fact"


def test_curated_source_fact_schema_rows_become_structured_facts() -> None:
    document = ParsedDocument(
        document_id="bangladesh_registration",
        title="Bangladesh Sender Registration",
        source_path="data/raw/bangladesh_registration.json",
        content_type="json",
        text="""# Bangladesh Sender Registration

## Source Facts

- registration: Value=Sender registration is mandatory for GrameenPhone in Bangladesh.; country_iso2=BD; operator_name=GrameenPhone; registration_scope=operator_specific; source_anchor=Bangladesh row, GrameenPhone requirement
""",
        country="Bangladesh",
        iso_code="BD",
    )

    blocks = normalize_document(document)

    assert len(blocks) == 1
    assert blocks[0].block_type == "structured_fact"
    assert blocks[0].quality_status == "ok"
    assert blocks[0].metadata["structured_field"] == "registration"
    assert blocks[0].metadata["structured_value"] == "Sender registration is mandatory for GrameenPhone in Bangladesh."


def test_short_narrative_blocks_remain_low_quality() -> None:
    document = ParsedDocument(
        document_id="notes",
        title="Notes",
        source_path="data/raw/notes.md",
        content_type="markdown",
        text="# Notes\n\nTiny note.",
    )

    blocks = normalize_document(document)

    assert len(blocks) == 1
    assert blocks[0].block_type == "narrative"
    assert blocks[0].quality_status == "LOW_QUALITY"


def test_markdown_fenced_code_blocks_are_preserved_as_code_samples() -> None:
    document = ParsedDocument(
        document_id="payloads",
        title="Payloads",
        source_path="data/raw/payloads.md",
        content_type="markdown",
        text="""# Payloads

```json
{"sender_id": "ACME", "requires_registration": true}
```
""",
    )

    blocks = normalize_document(document)

    assert len(blocks) == 1
    assert blocks[0].block_type == "code_sample"
    assert "requires_registration" in blocks[0].text
    assert blocks[0].metadata["code_block_preserved"] == "true"
    assert blocks[0].metadata["code_blocks_erased"] == "0"
    assert blocks[0].metadata["code_blocks_preserved"] == "1"


def test_block_level_channel_detection_uses_text_and_section_path() -> None:
    document = ParsedDocument(
        document_id="channels",
        title="Messaging",
        source_path="data/raw/channels.md",
        content_type="markdown",
        text="""# Messaging

## MMS support
Media messages are supported.

## Rules
Two-way SMS requires registration.
""",
    )

    blocks = normalize_document(document)

    assert "mms" in blocks[0].channels
    assert "sms" in blocks[1].channels


def test_char_offsets_come_from_section_spans_not_repeated_text_find() -> None:
    document = ParsedDocument(
        document_id="offsets",
        title="Offsets",
        source_path="data/raw/offsets.md",
        content_type="markdown",
        text="# Offsets\n\nRepeated fact.\n\nRepeated fact.\n",
    )

    blocks = normalize_document(document)

    assert [block.char_offset for block in blocks] == [11, 27]


def test_long_paragraph_chunks_on_sentence_boundaries() -> None:
    paragraph = "First sentence is short. Second sentence carries the relevant detail. Third sentence closes the block."
    document = ParsedDocument(
        document_id="chunking",
        title="Chunking",
        source_path="data/raw/chunking.md",
        content_type="markdown",
        text=f"# Chunking\n\n{paragraph}",
    )

    blocks = normalize_document(document, chunk_size=55, chunk_overlap=0)

    assert len(blocks) >= 2
    assert all(block.text.rstrip().endswith((".", "!", "?")) for block in blocks)
    assert not any("Second sentence carries the relevant" in block.text and not block.text.endswith(".") for block in blocks)


@pytest.mark.skip(reason="spain__214.md removed from corpus during raw data update; re-evaluate when corpus is restabilised")
def test_real_corpus_spain_kv_file_produces_country_tagged_blocks() -> None:
    """spain__214.md is a KV-table file; every block should carry tag_iso_code=ES."""
    path = Path("data/raw/spain__214.md")
    document = ParsedDocument(
        document_id=path.stem,
        title="Spain",
        source_path=str(path),
        content_type="markdown",
        text=path.read_text(encoding="utf-8"),
        country="Spain",
        iso_code="ES",
    )

    blocks = normalize_document(document)
    table_blocks = [b for b in blocks if b.metadata.get("tag_table_type") == "key_value"]

    assert table_blocks, "Expected KV table blocks from spain__214.md"
    assert all(b.iso_code == "ES" for b in table_blocks)
    # Sender block should carry the value
    sender_blocks = [b for b in table_blocks if b.metadata.get("row_key") == "Sender availability"]
    assert sender_blocks, "Expected a 'Sender availability' block"
    assert "Dynamic alpha" in sender_blocks[0].text or "Dynamic" in sender_blocks[0].text


@pytest.mark.skip(reason="all_twilio_sms_guidelines_index.md removed from corpus during raw data update; re-evaluate when corpus is restabilised")
def test_real_corpus_index_document_is_classified_as_catalog() -> None:
    path = Path("data/raw/all_twilio_sms_guidelines_index.md")
    document = ParsedDocument(
        document_id=path.stem,
        title="Twilio SMS Guidelines Index",
        source_path=str(path),
        content_type="markdown",
        text=path.read_text(encoding="utf-8"),
    )

    blocks = normalize_document(document)

    assert blocks
    assert all(block.metadata.get("document_kind") == "catalog" for block in blocks[:10])
    assert any(block.block_type == "catalog_entry" for block in blocks)
