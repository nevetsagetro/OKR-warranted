from pathlib import Path

from own_knowledge_rag.config import Settings
from own_knowledge_rag.enrichment import Enricher, EnrichmentResult
from own_knowledge_rag.models import KnowledgeBlock, ParsedDocument


def _make_block(index: int, **kwargs) -> KnowledgeBlock:
    defaults = dict(
        block_id=f"block-{index}",
        document_id="finland_fi",
        title="Finland (FI)",
        section_path=["Finland (FI)", "Guidelines"],
        section_heading="Guidelines",
        block_type="table_fact",
        text=f"Block {index} text",
        source_path="data/raw/finland_fi.md",
        start_anchor="",
        end_anchor="",
        metadata={},
    )
    defaults.update(kwargs)
    return KnowledgeBlock(**defaults)


def test_enricher_uses_configured_batch_size_without_default_sleep(monkeypatch, tmp_path: Path, capsys) -> None:
    settings = Settings(OKR_MAPPING_BATCH_SIZE=2, OKR_MAPPING_BATCH_DELAY_MS=0)
    enricher = Enricher(settings)
    document = ParsedDocument(
        document_id="finland_fi",
        title="Finland (FI)",
        source_path="data/raw/finland_fi.md",
        content_type="markdown",
        text="",
        country="Finland",
        iso_code="FI",
    )
    blocks = [_make_block(1), _make_block(2), _make_block(3)]

    call_sizes: list[int] = []
    sleep_calls: list[float] = []

    def fake_call_llm(doc: ParsedDocument, batch_blocks: list[KnowledgeBlock]) -> list[EnrichmentResult]:
        call_sizes.append(len(batch_blocks))
        return [
            EnrichmentResult(
                block_id=block.block_id,
                country="Finland",
                iso_code="FI",
                answer_signal="standalone_fact",
                hypothetical_questions=[f"What does {block.block_id} say?"],
                enriched_text=block.text,
            )
            for block in batch_blocks
        ]

    monkeypatch.setattr(enricher, "_call_llm", fake_call_llm)
    monkeypatch.setattr("own_knowledge_rag.enrichment.time.sleep", lambda seconds: sleep_calls.append(seconds))

    enriched = enricher.enrich_blocks(document, blocks, tmp_path, force_reenrich=True)
    output = capsys.readouterr().out

    assert len(enriched) == 3
    assert call_sizes == [2, 1]
    assert sleep_calls == []
    assert "Enrichment Start | doc=finland_fi | blocks=0/3 | remaining_blocks=3 | percent_complete=0.0% | batches=0/2 | elapsed=" in output
    assert " | eta=? | cached=0 | live=3 | api_calls=0 | cache_hits_total=0 | global_cached_rate=0.0%" in output
    assert "Enrichment Progress | doc=finland_fi | blocks=2/3 | remaining_blocks=1 | percent_complete=66.7% | batches=1/2 | elapsed=" in output
    assert " | eta=" in output
    assert "batch_sent=2 | batch_received=2" in output
    assert "Enrichment Complete | doc=finland_fi | blocks=3/3 | remaining_blocks=0 | percent_complete=100.0% | batches=2/2 | elapsed=" in output


def test_block_prompt_lines_prefer_compact_table_payload() -> None:
    settings = Settings(OKR_MAPPING_TEXT_CHAR_LIMIT=80)
    enricher = Enricher(settings)
    block = _make_block(
        1,
        text=(
            "This is a very long descriptive block text that should still be trimmed down before being sent "
            "to the model because it includes extra explanatory context that is not needed for enrichment."
        ),
        metadata={
            "raw_table_row_dict": {
                "Field": "Two-way SMS supported",
                "Description": "Whether Twilio supports two-way SMS in the given locale.",
                "Value": "Yes",
            },
            "row_key": "Two-way SMS supported",
            "row_values": "Yes",
        },
    )

    lines = enricher._block_prompt_lines(block)
    rendered = "\n".join(lines)

    assert "Table Row:" in rendered
    assert "Row Key:" not in rendered
    assert "Row Values:" not in rendered
    assert "Type: table_fact" in rendered
    text_line = next(line for line in lines if line.startswith("Text: "))
    assert text_line.endswith("...")
    assert len(text_line) < len(f"Text: {block.text}")


def test_pass1_prompt_uses_stripped_instructions() -> None:
    settings = Settings(OKR_MAPPING_PROMPT_MODE="pass1")
    enricher = Enricher(settings)

    prompt = enricher._system_prompt()

    assert "Generate 1-2 specific hypothetical_questions" in prompt
    assert "Leave reasoning empty unless a short clarification is necessary." in prompt


def test_noop_mapping_never_initializes_external_client(monkeypatch) -> None:
    settings = Settings(OKR_MAPPING_PROVIDER="noop")
    enricher = Enricher(settings)
    document = ParsedDocument(
        document_id="finland_fi",
        title="Finland (FI)",
        source_path="data/raw/finland_fi.md",
        content_type="markdown",
        text="",
        country="Finland",
        iso_code="FI",
    )
    blocks = [_make_block(1)]
    imports: list[str] = []

    def fake_import(name: str):
        imports.append(name)
        raise AssertionError(f"noop mapping should not import provider module: {name}")

    monkeypatch.setattr("own_knowledge_rag.enrichment.importlib.import_module", fake_import)

    results = enricher._call_llm(document, blocks)

    assert imports == []
    assert results[0].block_id == "block-1"
    assert results[0].enriched_text == "Block 1 text"


def test_noop_mapping_promotes_structured_fact_fields() -> None:
    settings = Settings(OKR_MAPPING_PROVIDER="noop")
    enricher = Enricher(settings)
    document = ParsedDocument(
        document_id="country_numbering_codes_enriched",
        title="Country Numbering Codes",
        source_path="data/raw/country_numbering_codes.json",
        content_type="json",
        text="",
    )
    block = _make_block(
        1,
        document_id="country_numbering_codes_enriched",
        title="Country Numbering Codes",
        block_type="structured_fact",
        text=(
            "- country_numbering_codes: Value=Afghanistan has ISO code AF, MCC 412, and dialing codes +93, 93.; "
            "country=Afghanistan; country_iso2=AF; mcc=412; dialing_code=+93, 93; "
            "hypothetical_questions=What is the dialing code for Afghanistan?, What is the MCC for Afghanistan?, What is Afghanistan's ISO code?; "
            "fact_id=afghanistan_af_numbering_codes_001; fact_type=country_numbering_codes; "
            "topic=Afghanistan dialing code and MCC; applies_to=Afghanistan; source_anchor=country_numbering_codes.afghanistan"
        ),
        metadata={
            "content_type": "json",
            "structured_source": "json",
            "structured_field": "country_numbering_codes",
            "row_values": (
                "Value=Afghanistan has ISO code AF, MCC 412, and dialing codes +93, 93.; "
                "country=Afghanistan; country_iso2=AF; mcc=412; dialing_code=+93, 93; "
                "hypothetical_questions=What is the dialing code for Afghanistan?, What is the MCC for Afghanistan?, What is Afghanistan's ISO code?"
            ),
            "informative": "high",
        },
    )

    result = enricher._call_llm(document, [block])[0]
    enriched = enricher._apply_result(block, result)
    validated = enricher.validate_blocks([enriched])[0]

    assert enriched.country == "Afghanistan"
    assert enriched.iso_code == "AF"
    assert enriched.enriched_text == "Afghanistan has ISO code AF, MCC 412, and dialing codes +93, 93."
    assert "What is the MCC for Afghanistan?" in enriched.hypothetical_questions
    assert "412" in enriched.local_aliases
    assert validated.quality_status == "ok"


def test_apply_result_rejects_country_identity_that_conflicts_with_block_context() -> None:
    enricher = Enricher(Settings(OKR_MAPPING_PROVIDER="noop"))
    block = _make_block(
        1,
        document_id="bermuda__350",
        title="bermuda",
        section_path=["bermuda", "Bermuda"],
        text="- Generic Sender ID: No",
        country="",
        iso_code="",
        metadata={"row_key": "Generic Sender ID", "row_values": "No"},
    )
    result = EnrichmentResult(
        block_id=block.block_id,
        country="Afghanistan",
        iso_code="AF",
        enriched_text="Bermuda generic sender IDs are not supported.",
    )

    enriched = enricher._apply_result(block, result)

    assert enriched.country == ""
    assert enriched.iso_code == ""


def test_apply_result_accepts_country_identity_present_in_structured_row_values() -> None:
    enricher = Enricher(Settings(OKR_MAPPING_PROVIDER="noop"))
    block = _make_block(
        1,
        document_id="country_numbering_codes_enriched",
        title="Country Numbering Codes",
        section_path=["Country MCC and Dialing Codes"],
        text="- country_numbering_codes: Value=Afghanistan has ISO code AF.",
        country="",
        iso_code="",
        metadata={
            "structured_source": "json",
            "row_values": "Value=Afghanistan has ISO code AF.; country=Afghanistan; country_iso2=AF",
        },
    )
    result = EnrichmentResult(
        block_id=block.block_id,
        country="Afghanistan",
        iso_code="AF",
        enriched_text="Afghanistan has ISO code AF.",
    )

    enriched = enricher._apply_result(block, result)

    assert enriched.country == "Afghanistan"
    assert enriched.iso_code == "AF"


def test_validate_blocks_accepts_informative_structured_fact_without_llm_tags() -> None:
    enricher = Enricher(Settings(OKR_MAPPING_PROVIDER="noop"))
    block = _make_block(
        1,
        block_type="structured_fact",
        text="- prefix: Value=Ukraine uses dialing code +380.; country=Ukraine; country_iso2=UA; dialing_code=+380",
        enriched_text="Ukraine uses dialing code +380.",
        metadata={"row_values": "Value=Ukraine uses dialing code +380.; country=Ukraine; country_iso2=UA; dialing_code=+380"},
        quality_status="LOW_QUALITY",
    )

    validated = enricher.validate_blocks([block])[0]

    assert validated.quality_status == "ok"


def test_validate_blocks_flags_enrichment_drift_without_rejecting_block() -> None:
    enricher = Enricher(Settings(OKR_MAPPING_PROVIDER="noop"))
    block = _make_block(
        1,
        text="Spain ES requires sender registration for prefix +34 and MCC 214.",
        enriched_text="Spain requires sender registration.",
        country="Spain",
        iso_code="ES",
        regulation_topics=["sender registration"],
    )

    validated = enricher.validate_blocks([block])[0]

    assert validated.quality_status == "ok"
    assert validated.metadata["drift_risk"] == "true"
    assert "+34" in validated.metadata["drift_missing_values"]
    assert "214" in validated.metadata["drift_missing_values"]


def test_retry_missing_results_recovers_missing_blocks(monkeypatch, tmp_path: Path) -> None:
    settings = Settings(OKR_MAPPING_BATCH_SIZE=2, OKR_MAPPING_RETRY_MISSING_RESULTS=True)
    enricher = Enricher(settings)
    document = ParsedDocument(
        document_id="finland_fi",
        title="Finland (FI)",
        source_path="data/raw/finland_fi.md",
        content_type="markdown",
        text="",
        country="Finland",
        iso_code="FI",
    )
    blocks = [_make_block(1), _make_block(2)]
    call_log: list[list[str]] = []

    def fake_call_llm(doc: ParsedDocument, batch_blocks: list[KnowledgeBlock]) -> list[EnrichmentResult]:
        block_ids = [block.block_id for block in batch_blocks]
        call_log.append(block_ids)
        if block_ids == ["block-1", "block-2"]:
            return [
                EnrichmentResult(
                    block_id="block-1",
                    country="Finland",
                    iso_code="FI",
                    answer_signal="standalone_fact",
                    hypothetical_questions=["What does block-1 say?"],
                    enriched_text="Block 1",
                )
            ]
        return [
            EnrichmentResult(
                block_id="block-2",
                country="Finland",
                iso_code="FI",
                answer_signal="standalone_fact",
                hypothetical_questions=["What does block-2 say?"],
                enriched_text="Block 2",
            )
        ]

    monkeypatch.setattr(enricher, "_call_llm", fake_call_llm)

    enriched = enricher.enrich_blocks(document, blocks, tmp_path, force_reenrich=True)

    assert [block.block_id for block in enriched] == ["block-1", "block-2"]
    assert enriched[1].hypothetical_questions == ["What does block-2 say?"]
    assert call_log == [["block-1", "block-2"], ["block-2"]]


def test_enricher_cache_key_is_content_based_across_block_ids(tmp_path: Path) -> None:
    settings = Settings(OKR_MAPPING_PROVIDER="noop", OKR_MAPPING_MODEL="fallback")
    enricher = Enricher(settings)
    document = ParsedDocument(
        document_id="finland_fi",
        title="Finland (FI)",
        source_path="data/raw/finland_fi.md",
        content_type="markdown",
        text="",
        country="Finland",
        iso_code="FI",
    )
    first_block = _make_block(1, text="Same retrievable fact.")
    second_block = _make_block(2, text="Same retrievable fact.")

    first = enricher.enrich_blocks(document, [first_block], tmp_path, force_reenrich=False)
    second = enricher.enrich_blocks(document, [second_block], tmp_path, force_reenrich=False)

    assert first[0].enrichment_provider == "noop"
    assert first[0].enrichment_model == "fallback"
    assert first[0].enriched_at
    assert second[0].enriched_text == first[0].enriched_text
    assert enricher.cache_hits == 1


def test_enricher_reuses_legacy_cache_version(tmp_path: Path) -> None:
    settings = Settings()
    enricher = Enricher(settings)
    document = ParsedDocument(
        document_id="finland_fi",
        title="Finland (FI)",
        source_path="data/raw/finland_fi.md",
        content_type="markdown",
        text="",
        country="Finland",
        iso_code="FI",
    )
    block = _make_block(1)
    legacy_key = enricher._legacy_cache_key(block, prompt_version="v2.1")
    current_key = enricher._cache_key(block)
    (tmp_path / "enrichment-cache.json").write_text(
        '{"%s": {"block_id": "block-1", "country": "Finland", "iso_code": "FI", "sender_types": [], "regulation_topics": [], "answer_signal": "standalone_fact", "hypothetical_questions": ["Legacy cache hit"], "enriched_text": "Legacy text", "local_aliases": [], "reasoning": ""}}'
        % legacy_key,
        encoding="utf-8",
    )

    enriched = enricher.enrich_blocks(document, [block], tmp_path, force_reenrich=False)

    assert len(enriched) == 1
    assert enriched[0].hypothetical_questions == ["Legacy cache hit"]
    assert enricher.cache_hits == 1
    migrated_cache = enricher._load_cache(tmp_path)
    assert current_key in migrated_cache
