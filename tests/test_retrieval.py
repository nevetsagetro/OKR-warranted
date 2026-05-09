from own_knowledge_rag.answering import ExtractiveAnswerer
from own_knowledge_rag.config import Settings
from own_knowledge_rag.embeddings import EmbeddingModel
from own_knowledge_rag.lexical import BM25Index
from own_knowledge_rag.models import KnowledgeBlock, SearchHit
from own_knowledge_rag.query_router import extract_query_filters
from own_knowledge_rag.retrieval import HybridRetriever
from own_knowledge_rag.vector_store import VectorIndex


def test_hybrid_retrieval_prefers_specific_country_document() -> None:
    blocks = [
        KnowledgeBlock(
            block_id="aggregate-1",
            document_id="scraping-infobip",
            title="Scraping Infobip",
            section_path=["spain"],
                section_heading="",
            block_type="table_fact",
            text="spain: Sender provisioning: No sender registration needed.",
            source_path="data/raw/scraping-infobip.md",
            start_anchor="spain: Sender provisioning",
            end_anchor="No sender registration needed.",
        ),
        KnowledgeBlock(
            block_id="country-1",
            document_id="spain_es",
            title="Spain (ES)",
            section_path=["Phone Numbers & Sender ID", "Alphanumeric"],
                section_heading="",
            block_type="table_fact",
            text="Sender provisioning: No sender registration needed.",
            source_path="data/raw/spain_es.md",
            start_anchor="Sender provisioning",
            end_anchor="No sender registration needed.",
        ),
    ]
    model = EmbeddingModel(Settings())
    lexical = BM25Index(blocks)
    vector = VectorIndex(blocks, model.encode([block.text for block in blocks]))
    retriever = HybridRetriever(lexical, vector, model)

    hits = retriever.search("Sender in Spain?", top_k=2)

    assert hits[0].block.document_id == "spain_es"


def test_answerer_returns_grounded_markdown() -> None:
    answer = ExtractiveAnswerer().answer(
        "Sender in Spain?",
        [],
    )

    assert "Insufficient evidence" in answer.answer


def test_answerer_uses_structured_row_metadata_for_direct_answer() -> None:
    block = KnowledgeBlock(
        block_id="spain-supported",
        document_id="spain_es",
        title="Spain (ES)",
        section_path=["Phone Numbers & Sender ID", "Alphanumeric"],
                section_heading="",
        block_type="table_fact",
        text="Twilio supported: Description=Whether Twilio supports the feature for the given country.; Pre-registration=---; Dynamic=Supported Learn more",
        source_path="data/raw/spain_es.md",
        start_anchor="Twilio supported",
        end_anchor="Supported Learn more",
        metadata={
            "document_kind": "knowledge",
            "informative": "high",
            "row_key": "Twilio supported",
            "row_values": "Description=Whether Twilio supports the feature for the given country.; Pre-registration=---; Dynamic=Supported Learn more",
        },
    )
    hit = type("Hit", (), {"block": block, "score": 0.9})()
    answer = ExtractiveAnswerer().answer("Sender in Spain?", [hit])

    assert "Alphanumeric sender IDs are supported in Spain" in answer.answer


def test_answerer_polishes_sender_provisioning_fact_without_hardcoded_country() -> None:
    block = KnowledgeBlock(
        block_id="spain-sender",
        document_id="spain_es",
        title="Spain (ES)",
        section_path=["spain"],
        section_heading="",
        block_type="table_fact",
        text="For spain, the Sender provisioning is: No sender registration needed.",
        source_path="data/raw/spain_es.md",
        start_anchor="Sender provisioning",
        end_anchor="No sender registration needed.",
        metadata={
            "document_kind": "knowledge",
            "informative": "high",
            "row_key": "Sender provisioning",
            "row_values": "No sender registration needed.",
        },
    )
    hit = type("Hit", (), {"block": block, "score": 0.9})()

    answer = ExtractiveAnswerer().answer("Sender in Spain?", [hit])

    assert answer.answer == "Spain does not require sender registration."
    assert "For spain" not in answer.answer


def test_answerer_prefers_yes_no_style_for_policy_rule_when_evidence_is_explicit() -> None:
    block = KnowledgeBlock(
        block_id="sri-lanka-rule",
        document_id="scraping-infobip",
        title="SMS coverage and connectivity",
        section_path=["sri-lanka"],
                section_heading="",
        block_type="table_fact",
        text="sri-lanka: Service restrictions: Sender registration is required for domestic and international traffic.",
        source_path="data/raw/scraping-infobip.md",
        start_anchor="Service restrictions",
        end_anchor="international traffic.",
        metadata={
            "document_kind": "knowledge",
            "informative": "high",
            "row_key": "Service restrictions",
            "row_values": "Sender registration is required for domestic and international traffic.",
        },
    )
    hit = type("Hit", (), {"block": block, "score": 0.9})()
    answer = ExtractiveAnswerer().answer("Is sender registration required in Sri Lanka?", [hit])

    assert "Yes. Sri Lanka requires sender registration" in answer.answer


def test_answerer_prefers_required_evidence_over_generic_supported_evidence() -> None:
    required_block = KnowledgeBlock(
        block_id="required",
        document_id="scraping-infobip",
        title="SMS coverage and connectivity",
        section_path=["sri-lanka"],
                section_heading="",
        block_type="table_fact",
        text="sri-lanka: Service restrictions: Sender registration is required for domestic and international traffic.",
        source_path="data/raw/scraping-infobip.md",
        start_anchor="Service restrictions",
        end_anchor="international traffic.",
        metadata={
            "document_kind": "knowledge",
            "informative": "high",
            "row_key": "Service restrictions",
            "row_values": "Sender registration is required for domestic and international traffic.",
        },
    )
    supported_block = KnowledgeBlock(
        block_id="supported",
        document_id="sri_lanka_lk",
        title="Sri Lanka (LK)",
        section_path=["Phone Numbers & Sender ID: Alphanumeric"],
                section_heading="",
        block_type="table_fact",
        text="Phone Numbers & Sender ID: Alphanumeric: Twilio supported: Description=Whether Twilio supports the feature for the given country.; International Pre-registration=Supported; Domestic Pre-registration=Supported; Dynamic=Supported",
        source_path="data/raw/sri_lanka_lk.md",
        start_anchor="Twilio supported",
        end_anchor="Dynamic=Supported",
        metadata={
            "document_kind": "knowledge",
            "informative": "high",
            "row_key": "Phone Numbers & Sender ID",
            "row_values": "Alphanumeric: Twilio supported: Description=Whether Twilio supports the feature for the given country.; International Pre-registration=Supported; Domestic Pre-registration=Supported; Dynamic=Supported",
        },
    )
    hit_required = type("Hit", (), {"block": required_block, "score": 0.82})()
    hit_supported = type("Hit", (), {"block": supported_block, "score": 0.9})()

    answer = ExtractiveAnswerer().answer(
        "Is sender registration required in Sri Lanka?",
        [hit_supported, hit_required],
    )

    assert "Yes. Sri Lanka requires sender registration" in answer.answer


def test_hybrid_retrieval_penalizes_catalog_entries() -> None:
    blocks = [
        KnowledgeBlock(
            block_id="catalog-1",
            document_id="all_twilio_sms_guidelines_index",
            title="Twilio SMS Guidelines Index",
            section_path=["Index"],
                section_heading="",
            block_type="catalog_entry",
            text="Spain (ES): Source URL=https://www.twilio.com/en-us/guidelines/es/sms; Markdown=spain_es.md",
            source_path="data/raw/all_twilio_sms_guidelines_index.md",
            start_anchor="Spain (ES)",
            end_anchor="spain_es.md",
            metadata={"document_kind": "catalog", "row_key": "Spain (ES)", "row_values": "spain_es.md"},
        ),
        KnowledgeBlock(
            block_id="country-1",
            document_id="spain_es",
            title="Spain (ES)",
            section_path=["Phone Numbers & Sender ID", "Alphanumeric"],
                section_heading="",
            block_type="table_fact",
            text="Sender provisioning: Description=Provisioning is the process of getting the sender ID approved.; Pre-registration=N/A; Dynamic=N/A",
            source_path="data/raw/spain_es.md",
            start_anchor="Sender provisioning",
            end_anchor="Dynamic=N/A",
            metadata={
                "document_kind": "knowledge",
                "informative": "low",
                "row_key": "Sender provisioning",
                "row_values": "Description=Provisioning is the process of getting the sender ID approved.; Pre-registration=N/A; Dynamic=N/A",
            },
        ),
        KnowledgeBlock(
            block_id="country-2",
            document_id="spain_es",
            title="Spain (ES)",
            section_path=["Phone Numbers & Sender ID", "Alphanumeric"],
                section_heading="",
            block_type="table_fact",
            text="Twilio supported: Description=Whether Twilio supports the feature for the given country.; Pre-registration=---; Dynamic=Supported Learn more",
            source_path="data/raw/spain_es.md",
            start_anchor="Twilio supported",
            end_anchor="Supported Learn more",
            metadata={
                "document_kind": "knowledge",
                "informative": "high",
                "row_key": "Twilio supported",
                "row_values": "Description=Whether Twilio supports the feature for the given country.; Pre-registration=---; Dynamic=Supported Learn more",
            },
        ),
    ]
    model = EmbeddingModel(Settings())
    lexical = BM25Index(blocks)
    vector = VectorIndex(blocks, model.encode([block.text for block in blocks]))
    retriever = HybridRetriever(lexical, vector, model)

    hits = retriever.search("Sender in Spain?", top_k=3)

    assert hits[0].block.document_id == "spain_es"
    assert hits[-1].block.block_type == "catalog_entry"


def test_hybrid_retrieval_prefers_informative_row_keys_over_placeholder_rows() -> None:
    blocks = [
        KnowledgeBlock(
            block_id="spain-best-practice",
            document_id="spain_es",
            title="Spain (ES)",
            section_path=["Phone Numbers & Sender ID", "Alphanumeric"],
                section_heading="",
            block_type="table_fact",
            text="Best practices: Description=---; Pre-registration=N/A; Dynamic=N/A",
            source_path="data/raw/spain_es.md",
            start_anchor="Best practices",
            end_anchor="Dynamic=N/A",
            metadata={
                "document_kind": "knowledge",
                "informative": "low",
                "row_key": "Best practices",
                "row_values": "Description=---; Pre-registration=N/A; Dynamic=N/A",
            },
        ),
        KnowledgeBlock(
            block_id="spain-supported",
            document_id="spain_es",
            title="Spain (ES)",
            section_path=["Phone Numbers & Sender ID", "Alphanumeric"],
                section_heading="",
            block_type="table_fact",
            text="Twilio supported: Description=Whether Twilio supports the feature for the given country.; Pre-registration=---; Dynamic=Supported Learn more",
            source_path="data/raw/spain_es.md",
            start_anchor="Twilio supported",
            end_anchor="Supported Learn more",
            metadata={
                "document_kind": "knowledge",
                "informative": "high",
                "row_key": "Twilio supported",
                "row_values": "Description=Whether Twilio supports the feature for the given country.; Pre-registration=---; Dynamic=Supported Learn more",
            },
        ),
    ]
    model = EmbeddingModel(Settings())
    lexical = BM25Index(blocks)
    vector = VectorIndex(blocks, model.encode([block.text for block in blocks]))
    retriever = HybridRetriever(lexical, vector, model)

    hits = retriever.search("Sender in Spain?", top_k=2)

    assert hits[0].block.block_id == "spain-supported"


def test_hybrid_retrieval_prioritizes_json_structured_facts_for_code_queries() -> None:
    blocks = [
        KnowledgeBlock(
            block_id="markdown-dialing",
            document_id="spain_markdown",
            title="Spain (ES)",
            section_path=["Locale Summary"],
            section_heading="",
            block_type="table_fact",
            text="Dialing code: Value=+34",
            source_path="data/raw/spain_es.md",
            start_anchor="Dialing code",
            end_anchor="+34",
            country="Spain",
            iso_code="ES",
            metadata={
                "content_type": "markdown",
                "document_kind": "knowledge",
                "document_scope": "profile",
                "informative": "high",
                "row_key": "Dialing code",
                "row_values": "Value=+34",
            },
        ),
        KnowledgeBlock(
            block_id="json-dialing",
            document_id="spain_json",
            title="Spain (ES)",
            section_path=["Locale Summary"],
            section_heading="",
            block_type="structured_fact",
            text="- Dialing code: Description=Country calling code.; Value=+34",
            source_path="data/raw/spain_es.json",
            start_anchor="Dialing code",
            end_anchor="+34",
            country="Spain",
            iso_code="ES",
            metadata={
                "content_type": "json",
                "document_kind": "knowledge",
                "document_scope": "profile",
                "informative": "high",
                "row_key": "Dialing code",
                "row_values": "Description=Country calling code.; Value=+34",
                "structured_field": "Dialing code",
                "structured_value": "+34",
                "structured_source": "json",
            },
        ),
    ]
    model = EmbeddingModel(Settings())
    lexical = BM25Index(blocks)
    vector = VectorIndex(blocks, model.encode([block.text for block in blocks]))
    retriever = HybridRetriever(lexical, vector, model)

    hits = retriever.search("What is the dialing code for Spain?", top_k=2)

    assert hits[0].block.block_id == "json-dialing"


def test_hybrid_retrieval_refuses_foreign_country_when_requested_country_absent() -> None:
    blocks = [
        KnowledgeBlock(
            block_id="australia-registration",
            document_id="global_restrictions",
            title="Global Restrictions",
            section_path=["Source Facts"],
            section_heading="",
            block_type="structured_fact",
            text="- registration: Value=In Australia, SMS sender registration is required.; country_name=Australia; country_iso2=AU",
            source_path="data/raw/global.json",
            start_anchor="registration",
            end_anchor="AU",
            metadata={
                "content_type": "json",
                "document_kind": "knowledge",
                "row_key": "registration",
                "row_values": "Value=In Australia, SMS sender registration is required.; country_name=Australia; country_iso2=AU",
                "structured_source": "json",
            },
        )
    ]
    model = EmbeddingModel(Settings())
    lexical = BM25Index(blocks)
    vector = VectorIndex(blocks, model.encode([block.text for block in blocks]))
    retriever = HybridRetriever(lexical, vector, model)

    hits = retriever.search("Does Spain support two-way SMS?", top_k=3)

    assert hits == []


def test_hybrid_retrieval_prioritizes_target_row_key_for_sender_support() -> None:
    blocks = [
        KnowledgeBlock(
            block_id="af-ucs",
            document_id="afghanistan_af",
            title="Afghanistan (AF)",
            section_path=["Afghanistan (AF)", "Phone Numbers & Sender ID: Alphanumeric"],
            section_heading="",
            block_type="table_fact",
            text="Regarding Phone Numbers & Sender ID: Alphanumeric for UCS-2 support: the Global Pre-registration is Supported, the Dynamic is Supported.",
            source_path="data/raw/afghanistan_af.md",
            start_anchor="UCS-2 support",
            end_anchor="Supported",
            country="Afghanistan",
            iso_code="AF",
            metadata={
                "document_kind": "knowledge",
                "document_scope": "profile",
                "informative": "high",
                "row_key": "UCS-2 support",
                "row_values": "Global Pre-registration=Supported; Dynamic=Supported",
            },
        ),
        KnowledgeBlock(
            block_id="af-supported",
            document_id="afghanistan_af",
            title="Afghanistan (AF)",
            section_path=["Afghanistan (AF)", "Phone Numbers & Sender ID: Alphanumeric"],
            section_heading="",
            block_type="table_fact",
            text="Regarding Phone Numbers & Sender ID: Alphanumeric for Twilio supported: the Global Pre-registration is Supported; Dynamic is Supported.",
            source_path="data/raw/afghanistan_af.md",
            start_anchor="Twilio supported",
            end_anchor="Supported",
            country="Afghanistan",
            iso_code="AF",
            metadata={
                "document_kind": "knowledge",
                "document_scope": "profile",
                "informative": "high",
                "row_key": "Twilio supported",
                "row_values": "Global Pre-registration=Supported; Dynamic=Supported",
            },
        ),
    ]
    model = EmbeddingModel(Settings())
    lexical = BM25Index(blocks)
    vector = VectorIndex(blocks, model.encode([block.text for block in blocks]))
    retriever = HybridRetriever(lexical, vector, model)

    hits = retriever.search("Does Afghanistan support alphanumeric sender IDs?", top_k=2)

    assert hits[0].block.block_id == "af-supported"


def test_hybrid_retrieval_prioritizes_target_row_key_for_two_way_support() -> None:
    blocks = [
        KnowledgeBlock(
            block_id="al-two-way-provisioning",
            document_id="albania_al",
            title="Albania (AL)",
            section_path=["Albania (AL)", "albania"],
            section_heading="",
            block_type="table_fact",
            text="For albania, the Two-way provisioning is: Up to 15 days for VLN.",
            source_path="data/raw/albania_al.md",
            start_anchor="Two-way provisioning",
            end_anchor="15 days",
            country="Albania",
            iso_code="AL",
            metadata={
                "document_kind": "knowledge",
                "document_scope": "profile",
                "informative": "high",
                "row_key": "Two-way provisioning",
                "row_values": "Up to 15 days for VLN.",
            },
        ),
        KnowledgeBlock(
            block_id="al-two-way-supported",
            document_id="albania_al",
            title="Albania (AL)",
            section_path=["Albania (AL)", "Guidelines"],
            section_heading="",
            block_type="table_fact",
            text="For Guidelines, the Two-way SMS supported is: No.",
            source_path="data/raw/albania_al.md",
            start_anchor="Two-way SMS supported",
            end_anchor="No",
            country="Albania",
            iso_code="AL",
            metadata={
                "document_kind": "knowledge",
                "document_scope": "profile",
                "informative": "high",
                "row_key": "Two-way SMS supported",
                "row_values": "No",
            },
        ),
    ]
    model = EmbeddingModel(Settings())
    lexical = BM25Index(blocks)
    vector = VectorIndex(blocks, model.encode([block.text for block in blocks]))
    retriever = HybridRetriever(lexical, vector, model)

    hits = retriever.search("Does Albania support two-way SMS?", top_k=2)

    assert hits[0].block.block_id == "al-two-way-supported"


def test_hybrid_retrieval_prefers_title_iso_over_stale_block_iso() -> None:
    stale_foreign = KnowledgeBlock(
        block_id="myanmar-stale",
        document_id="myanmar_mm",
        title="Myanmar (MM)",
        section_path=["Myanmar (MM)", "Phone Numbers & Sender ID: Alphanumeric"],
        section_heading="",
        block_type="table_fact",
        text="Regarding Phone Numbers & Sender ID: Alphanumeric for Twilio supported: Supported.",
        source_path="data/raw/myanmar_mm.md",
        start_anchor="Twilio supported",
        end_anchor="Supported",
        country="Afghanistan",
        iso_code="AF",
        metadata={
            "document_kind": "knowledge",
            "document_scope": "profile",
            "informative": "high",
            "row_key": "Twilio supported",
            "row_values": "Supported",
        },
    )
    afghanistan = KnowledgeBlock(
        block_id="af-supported",
        document_id="afghanistan_af",
        title="Afghanistan (AF)",
        section_path=["Afghanistan (AF)", "Phone Numbers & Sender ID: Alphanumeric"],
        section_heading="",
        block_type="table_fact",
        text="Regarding Phone Numbers & Sender ID: Alphanumeric for Twilio supported: Supported.",
        source_path="data/raw/afghanistan_af.md",
        start_anchor="Twilio supported",
        end_anchor="Supported",
        country="Afghanistan",
        iso_code="AF",
        metadata={
            "document_kind": "knowledge",
            "document_scope": "profile",
            "informative": "high",
            "row_key": "Twilio supported",
            "row_values": "Supported",
        },
    )
    model = EmbeddingModel(Settings())
    lexical = BM25Index([stale_foreign, afghanistan])
    vector = VectorIndex([stale_foreign, afghanistan], model.encode([stale_foreign.text, afghanistan.text]))
    retriever = HybridRetriever(
        lexical,
        vector,
        model,
        all_blocks=[stale_foreign, afghanistan],
        country_index={"afghanistan": "AF", "myanmar": "MM"},
    )

    hits = retriever.search("Does Afghanistan support alphanumeric sender IDs?", top_k=2)

    assert [hit.block.block_id for hit in hits] == ["af-supported"]


def test_query_filter_does_not_treat_sender_id_as_indonesia_iso() -> None:
    filters = extract_query_filters(
        "What is the default sender ID in Albania if dynamic sender is not used?",
        {"albania": "AL", "id": "ID", "indonesia": "ID"},
    )

    assert filters.iso_codes == ["AL"]
    assert filters.sender_types == ["alphanumeric"]


def test_answerer_renders_json_structured_code_fact_directly() -> None:
    block = KnowledgeBlock(
        block_id="json-dialing",
        document_id="spain_json",
        title="Spain (ES)",
        section_path=["Locale Summary"],
        section_heading="",
        block_type="structured_fact",
        text="- Dialing code: Description=Country calling code.; Value=+34",
        source_path="data/raw/spain_es.json",
        start_anchor="Dialing code",
        end_anchor="+34",
        country="Spain",
        iso_code="ES",
        metadata={
            "content_type": "json",
            "document_kind": "knowledge",
            "document_scope": "profile",
            "informative": "high",
            "row_key": "Dialing code",
            "row_values": "Description=Country calling code.; Value=+34",
            "structured_field": "Dialing code",
            "structured_value": "+34",
            "structured_source": "json",
        },
    )
    hit = type("Hit", (), {"block": block, "score": 0.9})()

    answer = ExtractiveAnswerer().answer("What is the dialing code for Spain?", [hit])

    assert answer.answer == "Spain's dialing code is +34."


def test_hybrid_retrieval_prefers_requirement_row_for_required_question() -> None:
    blocks = [
        KnowledgeBlock(
            block_id="operator-capability",
            document_id="sri_lanka_lk",
            title="Sri Lanka (LK)",
            section_path=["Phone Numbers & Sender ID: Alphanumeric"],
                section_heading="",
            block_type="table_fact",
            text="Phone Numbers & Sender ID: Alphanumeric: Operator network capability: Description=Whether mobile operators support the feature.; International Pre-registration=Required; Domestic Pre-registration=Required; Dynamic=Not Supported",
            source_path="data/raw/sri_lanka_lk.md",
            start_anchor="Operator network capability",
            end_anchor="Dynamic=Not Supported",
            metadata={
                "document_kind": "knowledge",
                "informative": "high",
                "row_key": "Phone Numbers & Sender ID",
                "row_values": "Alphanumeric: Operator network capability: Description=Whether mobile operators support the feature.; International Pre-registration=Required; Domestic Pre-registration=Required; Dynamic=Not Supported",
            },
        ),
        KnowledgeBlock(
            block_id="service-restrictions",
            document_id="scraping-infobip",
            title="SMS coverage and connectivity",
            section_path=["sri-lanka"],
                section_heading="",
            block_type="table_fact",
            text="sri-lanka: Service restrictions: Sender registration is required for domestic and international traffic.",
            source_path="data/raw/scraping-infobip.md",
            start_anchor="Service restrictions",
            end_anchor="international traffic.",
            metadata={
                "document_kind": "knowledge",
                "informative": "high",
                "row_key": "Service restrictions",
                "row_values": "Sender registration is required for domestic and international traffic.",
            },
        ),
    ]
    model = EmbeddingModel(Settings())
    lexical = BM25Index(blocks)
    vector = VectorIndex(blocks, model.encode([block.text for block in blocks]))
    retriever = HybridRetriever(lexical, vector, model)

    hits = retriever.search("Is sender registration required in Sri Lanka?", top_k=2)

    assert hits[0].block.block_id == "service-restrictions"


def test_hybrid_retrieval_prefers_count_fact_over_catalog_entries() -> None:
    blocks = [
        KnowledgeBlock(
            block_id="catalog-source",
            document_id="all_twilio_sms_guidelines_index",
            title="Twilio SMS Guidelines Index",
            section_path=["Twilio SMS Guidelines Index"],
                section_heading="",
            block_type="table_fact",
            text="Source index: https://www.twilio.com/en-us/guidelines/sms",
            source_path="data/raw/all_twilio_sms_guidelines_index.md",
            start_anchor="Source index",
            end_anchor="/guidelines/sms",
            metadata={"document_kind": "catalog", "document_scope": "catalog", "row_key": "Source index", "row_values": "https://www.twilio.com/en-us/guidelines/sms"},
        ),
        KnowledgeBlock(
            block_id="catalog-count",
            document_id="all_twilio_sms_guidelines_index",
            title="Twilio SMS Guidelines Index",
            section_path=["Twilio SMS Guidelines Index"],
                section_heading="",
            block_type="table_fact",
            text="Locale count: 222",
            source_path="data/raw/all_twilio_sms_guidelines_index.md",
            start_anchor="Locale count",
            end_anchor="222",
            metadata={"document_kind": "catalog", "document_scope": "catalog", "row_key": "Locale count", "row_values": "222"},
        ),
        KnowledgeBlock(
            block_id="catalog-entry",
            document_id="all_twilio_sms_guidelines_index",
            title="Twilio SMS Guidelines Index",
            section_path=["Twilio SMS Guidelines Index"],
                section_heading="",
            block_type="catalog_entry",
            text="- Austria (AT): Source URL=https://www.twilio.com/en-us/guidelines/at/sms; JSON=austria_at.json; Markdown=austria_at.md",
            source_path="data/raw/all_twilio_sms_guidelines_index.md",
            start_anchor="Austria (AT)",
            end_anchor="austria_at.md",
            metadata={"document_kind": "catalog", "document_scope": "catalog", "row_key": "Austria (AT)", "row_values": "JSON=austria_at.json"},
        ),
    ]
    model = EmbeddingModel(Settings())
    lexical = BM25Index(blocks)
    vector = VectorIndex(blocks, model.encode([block.text for block in blocks]))
    retriever = HybridRetriever(lexical, vector, model)

    hits = retriever.search("How many locales are listed in the Twilio SMS Guidelines Index?", top_k=3)

    assert hits[0].block.block_id == "catalog-count"


def test_hybrid_retrieval_prefers_consequence_row_for_numeric_sender_question() -> None:
    blocks = [
        KnowledgeBlock(
            block_id="sender-preserved",
            document_id="nepal_np",
            title="Nepal (NP)",
            section_path=["Phone Numbers & Sender ID: Alphanumeric"],
                section_heading="",
            block_type="table_fact",
            text="Sender ID preserved: Description=Sender IDs may be changed for compliance reasons.; Global Pre-registration=Yes; Dynamic=No",
            source_path="data/raw/nepal_np.md",
            start_anchor="Sender ID preserved",
            end_anchor="Dynamic=No",
            metadata={
                "document_kind": "knowledge",
                "document_scope": "profile",
                "informative": "high",
                "row_key": "Sender ID preserved",
                "row_values": "Description=Sender IDs may be changed for compliance reasons.; Global Pre-registration=Yes; Dynamic=No",
            },
        ),
        KnowledgeBlock(
            block_id="use-case-restrictions",
            document_id="nepal_np",
            title="Nepal (NP)",
            section_path=["Phone Numbers & Sender ID: Long codes and short codes"],
                section_heading="",
            block_type="table_fact",
            text="Use case restrictions: Description=---; Long code international=Mobile networks in Nepal do not support numeric sender ID. Numeric sender ID will be overwritten with generic alphanumeric sender ID outside the Twilio platform and will be delivered at best effort basis.; Short code=N/A",
            source_path="data/raw/nepal_np.md",
            start_anchor="Use case restrictions",
            end_anchor="best effort basis.",
            metadata={
                "document_kind": "knowledge",
                "document_scope": "profile",
                "informative": "high",
                "row_key": "Use case restrictions",
                "row_values": "Long code international=Mobile networks in Nepal do not support numeric sender ID. Numeric sender ID will be overwritten with generic alphanumeric sender ID outside the Twilio platform and will be delivered at best effort basis.",
            },
        ),
    ]
    model = EmbeddingModel(Settings())
    lexical = BM25Index(blocks)
    vector = VectorIndex(blocks, model.encode([block.text for block in blocks]))
    retriever = HybridRetriever(lexical, vector, model)

    hits = retriever.search("What happens to numeric sender IDs in Nepal?", top_k=2)

    assert hits[0].block.block_id == "use-case-restrictions"


def test_answerer_prefers_sender_row_over_locale_summary_for_sender_question() -> None:
    locale_block = KnowledgeBlock(
        block_id="locale-name",
        document_id="spain_es",
        title="Spain (ES)",
        section_path=["Spain (ES)", "Locale Summary"],
                section_heading="",
        block_type="table_fact",
        text="Locale name: Value=Spain",
        source_path="data/raw/spain_es.md",
        start_anchor="Locale name",
        end_anchor="Spain",
        metadata={
            "document_kind": "knowledge",
            "document_scope": "profile",
            "informative": "high",
            "row_key": "Locale name",
            "row_values": "Value=Spain",
        },
    )
    sender_block = KnowledgeBlock(
        block_id="sender-supported",
        document_id="spain_es",
        title="Spain (ES)",
        section_path=["Spain (ES)", "Phone Numbers & Sender ID: Alphanumeric"],
                section_heading="",
        block_type="table_fact",
        text="Twilio supported: Description=Whether Twilio supports the feature for the given country.; Dynamic=Supported Learn more",
        source_path="data/raw/spain_es.md",
        start_anchor="Twilio supported",
        end_anchor="Supported Learn more",
        metadata={
            "document_kind": "knowledge",
            "document_scope": "profile",
            "informative": "high",
            "row_key": "Twilio supported",
            "row_values": "Description=Whether Twilio supports the feature for the given country.; Dynamic=Supported Learn more",
        },
    )
    locale_hit = type("Hit", (), {"block": locale_block, "score": 0.55})()
    sender_hit = type("Hit", (), {"block": sender_block, "score": 0.53})()

    answer = ExtractiveAnswerer().answer("Sender in Spain?", [locale_hit, sender_hit])

    assert "Alphanumeric sender IDs are supported in Spain" in answer.answer


def test_hybrid_retrieval_prefers_duration_row_for_how_long_question() -> None:
    blocks = [
        KnowledgeBlock(
            block_id="best-practice",
            document_id="sri_lanka_lk",
            title="Sri Lanka (LK)",
            section_path=["Phone Numbers & Sender ID: Alphanumeric"],
                section_heading="",
            block_type="table_fact",
            text="Best practices: Dynamic=Twilio suggests using a pre-registered Alphanumeric Sender ID in Sri Lanka.",
            source_path="data/raw/sri_lanka_lk.md",
            start_anchor="Best practices",
            end_anchor="Sri Lanka.",
            metadata={
                "document_kind": "knowledge",
                "document_scope": "profile",
                "informative": "high",
                "row_key": "Best practices",
                "row_values": "Dynamic=Twilio suggests using a pre-registered Alphanumeric Sender ID in Sri Lanka.",
            },
        ),
        KnowledgeBlock(
            block_id="provisioning-time",
            document_id="sri_lanka_lk",
            title="Sri Lanka (LK)",
            section_path=["Phone Numbers & Sender ID: Alphanumeric"],
                section_heading="",
            block_type="table_fact",
            text="Provisioning time: International Pre-registration=3 weeks; Domestic Pre-registration=3 weeks; Dynamic=N/A",
            source_path="data/raw/sri_lanka_lk.md",
            start_anchor="Provisioning time",
            end_anchor="Dynamic=N/A",
            metadata={
                "document_kind": "knowledge",
                "document_scope": "profile",
                "informative": "high",
                "row_key": "Provisioning time",
                "row_values": "International Pre-registration=3 weeks; Domestic Pre-registration=3 weeks; Dynamic=N/A",
            },
        ),
    ]
    model = EmbeddingModel(Settings())
    lexical = BM25Index(blocks)
    vector = VectorIndex(blocks, model.encode([block.text for block in blocks]))
    retriever = HybridRetriever(lexical, vector, model)

    hits = retriever.search("How long does international pre-registration take in Sri Lanka?", top_k=2)

    assert hits[0].block.block_id == "provisioning-time"


def test_hybrid_retrieval_country_filter_excludes_other_country_hits() -> None:
    blocks = [
        KnowledgeBlock(
            block_id="colombia-two-way",
            document_id="colombia_co",
            title="Colombia (CO)",
            section_path=["Colombia (CO)", "Guidelines"],
            section_heading="Guidelines",
            block_type="table_fact",
            text="For Guidelines, the Two-way SMS supported is: No.",
            source_path="data/raw/colombia_co.md",
            start_anchor="Two-way SMS supported",
            end_anchor="No",
            country="Colombia",
            iso_code="CO",
            metadata={
                "document_kind": "knowledge",
                "document_scope": "profile",
                "row_key": "Two-way SMS supported",
                "row_values": "Value=No",
                "informative": "high",
            },
        ),
        KnowledgeBlock(
            block_id="germany-two-way",
            document_id="germany_de",
            title="Germany (DE)",
            section_path=["Germany (DE)", "Guidelines"],
            section_heading="Guidelines",
            block_type="table_fact",
            text="For Guidelines, the Two-way SMS supported is: Yes.",
            source_path="data/raw/germany_de.md",
            start_anchor="Two-way SMS supported",
            end_anchor="Yes",
            country="Germany",
            iso_code="DE",
            metadata={
                "document_kind": "knowledge",
                "document_scope": "profile",
                "row_key": "Two-way SMS supported",
                "row_values": "Value=Yes",
                "informative": "high",
            },
        ),
    ]
    model = EmbeddingModel(Settings())
    lexical = BM25Index(blocks)
    vector = VectorIndex(blocks, model.encode([block.text for block in blocks]))
    retriever = HybridRetriever(
        lexical,
        vector,
        model,
        all_blocks=blocks,
        country_index={"colombia": "CO", "co": "CO", "germany": "DE", "de": "DE"},
    )

    hits = retriever.search("Does Colombia support two-way SMS?", top_k=2)

    assert hits
    assert hits[0].block.document_id == "colombia_co"
    assert all(hit.block.document_id != "germany_de" for hit in hits)


def test_hybrid_retrieval_diversifies_aggregate_country_queries() -> None:
    blocks = [
        KnowledgeBlock(
            block_id="india-registration",
            document_id="india_in",
            title="India (IN)",
            section_path=["India", "Registration"],
            section_heading="Registration",
            block_type="structured_fact",
            text="India requires sender registration for SMS traffic.",
            source_path="data/raw/registration.json",
            start_anchor="india",
            end_anchor="registration",
            country="India",
            iso_code="IN",
            metadata={
                "content_type": "json",
                "document_kind": "knowledge",
                "row_key": "registration",
                "row_values": "country_name=India; country_iso2=IN; Value=Sender registration is required.",
                "structured_source": "json",
                "informative": "high",
            },
        ),
        KnowledgeBlock(
            block_id="india-registration-duplicate",
            document_id="india_in",
            title="India (IN)",
            section_path=["India", "Sender ID"],
            section_heading="Sender ID",
            block_type="structured_fact",
            text="India requires pre-registration before sending alphanumeric sender ID traffic.",
            source_path="data/raw/registration.json",
            start_anchor="india-sender",
            end_anchor="registration",
            country="India",
            iso_code="IN",
            metadata={
                "content_type": "json",
                "document_kind": "knowledge",
                "row_key": "registration",
                "row_values": "country_name=India; country_iso2=IN; Value=Pre-registration is required.",
                "structured_source": "json",
                "informative": "high",
            },
        ),
        KnowledgeBlock(
            block_id="spain-registration",
            document_id="spain_es",
            title="Spain (ES)",
            section_path=["Spain", "Registration"],
            section_heading="Registration",
            block_type="structured_fact",
            text="Spain does not require sender registration for standard SMS traffic.",
            source_path="data/raw/registration.json",
            start_anchor="spain",
            end_anchor="registration",
            country="Spain",
            iso_code="ES",
            metadata={
                "content_type": "json",
                "document_kind": "knowledge",
                "row_key": "registration",
                "row_values": "country_name=Spain; country_iso2=ES; Value=Sender registration is not required.",
                "structured_source": "json",
                "informative": "high",
            },
        ),
        KnowledgeBlock(
            block_id="bangladesh-registration",
            document_id="bangladesh_bd",
            title="Bangladesh (BD)",
            section_path=["Bangladesh", "Registration"],
            section_heading="Registration",
            block_type="structured_fact",
            text="Bangladesh requires sender registration for SMS traffic.",
            source_path="data/raw/registration.json",
            start_anchor="bangladesh",
            end_anchor="registration",
            country="Bangladesh",
            iso_code="BD",
            metadata={
                "content_type": "json",
                "document_kind": "knowledge",
                "row_key": "registration",
                "row_values": "country_name=Bangladesh; country_iso2=BD; Value=Sender registration is required.",
                "structured_source": "json",
                "informative": "high",
            },
        ),
    ]
    model = EmbeddingModel(Settings())
    lexical = BM25Index(blocks)
    vector = VectorIndex(blocks, model.encode([block.text for block in blocks]))
    retriever = HybridRetriever(
        lexical,
        vector,
        model,
        all_blocks=blocks,
        country_index={
            "bangladesh": "BD",
            "bd": "BD",
            "india": "IN",
            "in": "IN",
            "spain": "ES",
            "es": "ES",
        },
    )

    hits = retriever.search("Which countries require sender registration?", top_k=2)
    first_two_isos = [hit.block.iso_code for hit in hits[:2]]

    assert len(set(first_two_isos)) == 2
    assert {"BD", "IN"} == set(first_two_isos)


def test_answerer_renders_aggregate_country_answers_as_list() -> None:
    kenya_block = KnowledgeBlock(
        block_id="kenya-registration",
        document_id="kenya_ke",
        title="Kenya (KE)",
        section_path=["Kenya", "Registration"],
        section_heading="Registration",
        block_type="structured_fact",
        text="Kenya requires local traffic registration on all networks.",
        source_path="data/raw/registration.json",
        start_anchor="kenya",
        end_anchor="registration",
        country="Kenya",
        iso_code="KE",
        metadata={
            "content_type": "json",
            "row_key": "registration",
            "row_values": "country_name=Kenya; country_iso2=KE; Value=Kenya requires local traffic registration on all networks.",
            "structured_source": "json",
        },
    )
    india_block = KnowledgeBlock(
        block_id="india-registration",
        document_id="india_in",
        title="India (IN)",
        section_path=["India", "Registration"],
        section_heading="Registration",
        block_type="structured_fact",
        text="India requires sender registration for SMS traffic.",
        source_path="data/raw/registration.json",
        start_anchor="india",
        end_anchor="registration",
        country="India",
        iso_code="IN",
        metadata={
            "content_type": "json",
            "row_key": "registration",
            "row_values": "country_name=India; country_iso2=IN; Value=India requires sender registration for SMS traffic.",
            "structured_source": "json",
        },
    )
    spain_block = KnowledgeBlock(
        block_id="spain-registration",
        document_id="spain_es",
        title="Spain (ES)",
        section_path=["Spain", "Registration"],
        section_heading="Registration",
        block_type="structured_fact",
        text="Spain does not require sender registration.",
        source_path="data/raw/registration.json",
        start_anchor="spain",
        end_anchor="registration",
        country="Spain",
        iso_code="ES",
        metadata={
            "content_type": "json",
            "row_key": "registration",
            "row_values": "country_name=Spain; country_iso2=ES; Value=Spain does not require sender registration.",
            "structured_source": "json",
        },
    )
    hits = [
        type("Hit", (), {"block": kenya_block, "score": 1.2})(),
        type("Hit", (), {"block": india_block, "score": 1.1})(),
        type("Hit", (), {"block": spain_block, "score": 1.0})(),
    ]

    answer = ExtractiveAnswerer().answer("Which countries need sender registration?", hits)

    assert answer.query_intent == "aggregate"
    assert answer.answer.startswith("Countries found:")
    assert "- Kenya:" in answer.answer
    assert "- India:" in answer.answer
    assert "Spain" not in answer.answer
    assert len(answer.evidence) == 2
    assert all(hit.block.iso_code in {"KE", "IN"} for hit in answer.evidence)


def test_answerer_filters_negative_support_from_aggregate_support_answers() -> None:
    afghanistan_block = KnowledgeBlock(
        block_id="afghanistan-two-way",
        document_id="afghanistan_af",
        title="Afghanistan (AF)",
        section_path=["Afghanistan", "Locale Summary"],
        section_heading="Locale Summary",
        block_type="table_fact",
        text="Two-way SMS supported: Value=No",
        source_path="data/raw/afghanistan_af.md",
        start_anchor="Two-way SMS supported",
        end_anchor="No",
        country="Afghanistan",
        iso_code="AF",
        metadata={
            "row_key": "Two-way SMS supported",
            "row_values": "Value=No",
        },
    )
    colombia_block = KnowledgeBlock(
        block_id="colombia-two-way",
        document_id="colombia_co",
        title="Colombia (CO)",
        section_path=["Colombia", "Locale Summary"],
        section_heading="Locale Summary",
        block_type="table_fact",
        text="Two-way SMS supported: Value=Yes",
        source_path="data/raw/colombia_co.md",
        start_anchor="Two-way SMS supported",
        end_anchor="Yes",
        country="Colombia",
        iso_code="CO",
        metadata={
            "row_key": "Two-way SMS supported",
            "row_values": "Value=Yes",
        },
    )
    belgium_block = KnowledgeBlock(
        block_id="belgium-two-way",
        document_id="belgium_be",
        title="Belgium (BE)",
        section_path=["Belgium", "Locale Summary"],
        section_heading="Locale Summary",
        block_type="table_fact",
        text="Two-way messaging is supported in Belgium.",
        source_path="data/raw/belgium_be.md",
        start_anchor="Two-way messaging",
        end_anchor="Belgium.",
        country="Belgium",
        iso_code="BE",
        metadata={
            "row_key": "Two-way SMS supported",
            "row_values": "Value=Yes",
        },
    )
    hits = [
        type("Hit", (), {"block": afghanistan_block, "score": 1.3})(),
        type("Hit", (), {"block": colombia_block, "score": 1.2})(),
        type("Hit", (), {"block": belgium_block, "score": 1.1})(),
    ]

    answer = ExtractiveAnswerer().answer("Which countries support two-way SMS?", hits)

    assert answer.query_intent == "aggregate"
    assert "Afghanistan" not in answer.answer
    assert "Colombia" in answer.answer
    assert "Belgium" in answer.answer
    assert [hit.block.iso_code for hit in answer.evidence] == ["CO", "BE"]


def test_answerer_does_not_mix_documents_for_non_comparative_question() -> None:
    colombia_block = KnowledgeBlock(
        block_id="colombia-two-way",
        document_id="colombia_co",
        title="Colombia (CO)",
        section_path=["Colombia (CO)", "Guidelines"],
        section_heading="Guidelines",
        block_type="table_fact",
        text="For Guidelines, the Two-way SMS supported is: No.",
        source_path="data/raw/colombia_co.md",
        start_anchor="Two-way SMS supported",
        end_anchor="No",
        country="Colombia",
        iso_code="CO",
        metadata={"row_key": "Two-way SMS supported", "row_values": "Value=No"},
    )
    germany_block = KnowledgeBlock(
        block_id="germany-two-way",
        document_id="germany_de",
        title="Germany (DE)",
        section_path=["Germany (DE)", "Guidelines"],
        section_heading="Guidelines",
        block_type="table_fact",
        text="For Guidelines, the Two-way SMS supported is: Yes.",
        source_path="data/raw/germany_de.md",
        start_anchor="Two-way SMS supported",
        end_anchor="Yes",
        country="Germany",
        iso_code="DE",
        metadata={"row_key": "Two-way SMS supported", "row_values": "Value=Yes"},
    )
    colombia_hit = type("Hit", (), {"block": colombia_block, "score": 0.92})()
    germany_hit = type("Hit", (), {"block": germany_block, "score": 0.9})()

    answer = ExtractiveAnswerer().answer(
        "Does Colombia support two-way SMS?",
        [colombia_hit, germany_hit],
    )

    assert "Colombia" in answer.answer
    assert "Germany" not in answer.answer
    assert all(hit.block.document_id == "colombia_co" for hit in answer.evidence)


def test_answerer_prefers_fact_over_matching_hypothetical_question() -> None:
    question_block = KnowledgeBlock(
        block_id="colombia-question",
        document_id="quiet_hours",
        title="Quiet Hours",
        section_path=["Quiet Hours", "Source Facts"],
        section_heading="Source Facts",
        block_type="faq",
        text="- What are the promotional SMS sending hours in Colombia?",
        source_path="data/raw/quiet-hours.json",
        start_anchor="What are the promotional SMS sending hours",
        end_anchor="Colombia?",
        country="Colombia",
        iso_code="CO",
    )
    fact_block = KnowledgeBlock(
        block_id="colombia-fact",
        document_id="quiet_hours",
        title="Quiet Hours",
        section_path=["Quiet Hours", "Source Facts"],
        section_heading="Source Facts",
        block_type="structured_fact",
        text="- enriched_text: In Colombia, promotional and debt collection SMS can only be sent from 8:00 AM to 9:00 PM.",
        source_path="data/raw/quiet-hours.json",
        start_anchor="In Colombia, promotional",
        end_anchor="9:00 PM.",
        country="Colombia",
        iso_code="CO",
        metadata={
            "row_key": "enriched_text",
            "structured_field": "enriched_text",
            "row_values": "In Colombia, promotional and debt collection SMS can only be sent from 8:00 AM to 9:00 PM.",
            "structured_value": "In Colombia, promotional and debt collection SMS can only be sent from 8:00 AM to 9:00 PM.",
        },
    )
    question_hit = type("Hit", (), {"block": question_block, "score": 0.95})()
    fact_hit = type("Hit", (), {"block": fact_block, "score": 0.7})()

    answer = ExtractiveAnswerer().answer(
        "What are the promotional SMS sending hours in Colombia?",
        [question_hit, fact_hit],
    )

    assert "8:00 AM to 9:00 PM" in answer.answer
    assert "What are the promotional SMS sending hours" not in answer.answer
    assert answer.evidence[0].block.block_id == "colombia-fact"


def test_answerer_hides_structured_metadata_when_rendering_value_rows() -> None:
    block = KnowledgeBlock(
        block_id="colombia-content-restriction",
        document_id="quiet_hours",
        title="Quiet Hours",
        section_path=["Quiet Hours", "Source Facts"],
        section_heading="Source Facts",
        block_type="structured_fact",
        text="- content_restriction: Value=In Colombia, promotional and debt collection SMS can only be sent from 8:00 AM to 9:00 PM.; country_name=Colombia; country_iso2=CO; block_id=colombia-time-restrictions; answer_signal=standalone_fact; regulation_topics=quiet hours, content restriction",
        source_path="data/raw/quiet-hours.json",
        start_anchor="content_restriction",
        end_anchor="content restriction",
        country="Colombia",
        iso_code="CO",
        metadata={
            "row_key": "content_restriction",
            "row_values": "Value=In Colombia, promotional and debt collection SMS can only be sent from 8:00 AM to 9:00 PM.; country_name=Colombia; country_iso2=CO; block_id=colombia-time-restrictions; answer_signal=standalone_fact; regulation_topics=quiet hours, content restriction",
            "structured_value": "In Colombia, promotional and debt collection SMS can only be sent from 8:00 AM to 9:00 PM.",
        },
    )
    hit = type("Hit", (), {"block": block, "score": 0.9})()

    answer = ExtractiveAnswerer().answer("What are the promotional SMS sending hours in Colombia?", [hit])

    assert answer.answer == "In Colombia, promotional and debt collection SMS can only be sent from 8:00 AM to 9:00 PM."
    assert "country_iso2" not in answer.answer
    assert "answer_signal" not in answer.answer


def test_answerer_uses_requested_sender_column_for_support_rows() -> None:
    block = KnowledgeBlock(
        block_id="afghanistan-short-code",
        document_id="afghanistan_af",
        title="Afghanistan (AF)",
        section_path=["Afghanistan (AF)", "Phone Numbers & Sender ID"],
        section_heading="Phone Numbers & Sender ID",
        block_type="table_fact",
        text=(
            "Regarding Phone Numbers & Sender ID: Long codes and short codes for Twilio supported: "
            "the Description is Whether Twilio supports the feature for the given country., "
            "the Long code domestic is Not Supported, the Long code international is Supported, "
            "the Short code is Not Supported"
        ),
        source_path="data/raw/afghanistan_af.md",
        start_anchor="Twilio supported",
        end_anchor="Short code is Not Supported",
        country="Afghanistan",
        iso_code="AF",
        metadata={
            "row_key": "Twilio supported",
            "row_values": (
                "the Description is Whether Twilio supports the feature for the given country., "
                "the Long code domestic is Not Supported, the Long code international is Supported, "
                "the Short code is Not Supported"
            ),
        },
    )
    hit = type("Hit", (), {"block": block, "score": 0.95})()

    answer = ExtractiveAnswerer().answer("Are short codes supported in Afghanistan?", [hit])

    assert answer.answer == (
        "No. In Afghanistan, short code sender IDs are not supported; "
        "the `Twilio supported` row says `Not Supported`."
    )
    assert answer.evidence[0].block.block_id == "afghanistan-short-code"


def test_answerer_does_not_let_sender_id_phrase_override_long_code_column() -> None:
    alpha_block = KnowledgeBlock(
        block_id="afghanistan-alpha-preserved",
        document_id="afghanistan_af",
        title="Afghanistan (AF)",
        section_path=["Afghanistan (AF)", "Phone Numbers & Sender ID"],
        section_heading="Phone Numbers & Sender ID",
        block_type="table_fact",
        text="Alphanumeric Sender ID preserved: Global Pre-registration=Yes; Dynamic=Yes",
        source_path="data/raw/afghanistan_af.md",
        start_anchor="Sender ID preserved",
        end_anchor="Dynamic=Yes",
        country="Afghanistan",
        iso_code="AF",
        metadata={
            "row_key": "Sender ID preserved",
            "row_values": "the Global Pre-registration is Yes, the Dynamic is Yes",
        },
    )
    long_code_block = KnowledgeBlock(
        block_id="afghanistan-long-code-preserved",
        document_id="afghanistan_af",
        title="Afghanistan (AF)",
        section_path=["Afghanistan (AF)", "Phone Numbers & Sender ID"],
        section_heading="Phone Numbers & Sender ID",
        block_type="table_fact",
        text="Long codes and short codes Sender ID preserved: Long code domestic=No; Long code international=No",
        source_path="data/raw/afghanistan_af.md",
        start_anchor="Sender ID preserved",
        end_anchor="Long code international=No",
        country="Afghanistan",
        iso_code="AF",
        metadata={
            "row_key": "Sender ID preserved",
            "row_values": "the Long code domestic is No, the Long code international is No",
        },
    )
    alpha_hit = type("Hit", (), {"block": alpha_block, "score": 0.96})()
    long_code_hit = type("Hit", (), {"block": long_code_block, "score": 0.95})()

    answer = ExtractiveAnswerer().answer(
        "Are long-code sender IDs preserved in Afghanistan?",
        [alpha_hit, long_code_hit],
    )

    assert answer.answer == (
        "No. In Afghanistan, long code sender IDs are not preserved; "
        "the `Sender ID preserved` row says `No`."
    )
    assert answer.evidence[0].block.block_id == "afghanistan-long-code-preserved"


def test_answerer_prefers_twilio_supported_for_alphanumeric_support_question() -> None:
    preserved_block = KnowledgeBlock(
        block_id="bahamas-alpha-preserved",
        document_id="bahamas_bs",
        title="Bahamas (BS)",
        section_path=["Bahamas (BS)", "Phone Numbers & Sender ID: Alphanumeric"],
        section_heading="Alphanumeric",
        block_type="table_fact",
        text="Alphanumeric Sender ID preserved: Global Pre-registration=Yes; Dynamic=Yes",
        source_path="data/raw/bahamas_bs.md",
        start_anchor="Sender ID preserved",
        end_anchor="Dynamic=Yes",
        country="Bahamas",
        iso_code="BS",
        metadata={
            "row_key": "Sender ID preserved",
            "row_values": "the Global Pre-registration is Yes, the Dynamic is Yes",
        },
    )
    supported_block = KnowledgeBlock(
        block_id="bahamas-alpha-supported",
        document_id="bahamas_bs",
        title="Bahamas (BS)",
        section_path=["Bahamas (BS)", "Phone Numbers & Sender ID: Alphanumeric"],
        section_heading="Alphanumeric",
        block_type="table_fact",
        text="Alphanumeric Twilio supported: Global Pre-registration=Not Required; Supported Learn more",
        source_path="data/raw/bahamas_bs.md",
        start_anchor="Twilio supported",
        end_anchor="Supported Learn more",
        country="Bahamas",
        iso_code="BS",
        metadata={
            "row_key": "Twilio supported",
            "row_values": "the Global Pre-registration is Not Required; Supported Learn more",
        },
    )
    preserved_hit = SearchHit(block=preserved_block, score=0.96)
    supported_hit = SearchHit(block=supported_block, score=0.72)

    answer = ExtractiveAnswerer().answer(
        "Does Bahamas support alphanumeric sender IDs?",
        [preserved_hit, supported_hit],
    )

    assert answer.answer == (
        "Yes. In Bahamas, alphanumeric sender IDs are supported; "
        "the `Twilio supported` row says `Not Required, Supported Learn more`."
    )
    assert answer.evidence[0].block.block_id == "bahamas-alpha-supported"


def test_answerer_uses_full_twilio_supported_row_for_generic_alphanumeric_support() -> None:
    block = KnowledgeBlock(
        block_id="algeria-alpha-supported",
        document_id="algeria_dz",
        title="Algeria (DZ)",
        section_path=["Algeria (DZ)", "Phone Numbers & Sender ID: Alphanumeric"],
        section_heading="Alphanumeric",
        block_type="table_fact",
        text=(
            "Alphanumeric Twilio supported: Domestic Pre-registration=Not Supported; "
            "Dynamic=Supported Learn more"
        ),
        source_path="data/raw/algeria_dz.md",
        start_anchor="Twilio supported",
        end_anchor="Supported Learn more",
        country="Algeria",
        iso_code="DZ",
        metadata={
            "row_key": "Twilio supported",
            "row_values": (
                "the Domestic Pre-registration is Not Supported; "
                "the Dynamic is Supported Learn more"
            ),
        },
    )
    hit = SearchHit(block=block, score=0.95)

    answer = ExtractiveAnswerer().answer("Does Algeria support alphanumeric sender IDs?", [hit])

    assert answer.answer == (
        "No. In Algeria, alphanumeric sender IDs are not supported; "
        "the `Twilio supported` row says "
        "`the Domestic Pre-registration is Not Supported; the Dynamic is Supported Learn more`."
    )


def test_answerer_prefers_title_country_over_stale_block_country() -> None:
    block = KnowledgeBlock(
        block_id="colombia-two-way",
        document_id="colombia_co",
        title="Colombia (CO)",
        section_path=["Colombia (CO)", "Guidelines"],
        section_heading="Guidelines",
        block_type="table_fact",
        text="For Guidelines, the Two-way SMS supported is: Yes.",
        source_path="data/raw/colombia_co.md",
        start_anchor="Two-way SMS supported",
        end_anchor="Yes",
        country="Argentina",
        iso_code="AR",
        metadata={"row_key": "Two-way SMS supported", "row_values": "Yes"},
    )
    hit = type("Hit", (), {"block": block, "score": 0.95})()

    answer = ExtractiveAnswerer().answer("Does Colombia support two-way SMS?", [hit])

    assert answer.answer == (
        "Yes. Two-way messaging is supported in Colombia; "
        "the `Two-way SMS supported` row says `Yes`."
    )


def test_answerer_uses_requested_sender_column_for_provisioning_time() -> None:
    block = KnowledgeBlock(
        block_id="afghanistan-alpha-provisioning",
        document_id="afghanistan_af",
        title="Afghanistan (AF)",
        section_path=["Afghanistan (AF)", "Phone Numbers & Sender ID"],
        section_heading="Phone Numbers & Sender ID",
        block_type="table_fact",
        text=(
            "Regarding Phone Numbers & Sender ID: Alphanumeric for Provisioning time: "
            "the Description is Provisioning is the process, the Global Pre-registration is 1 week"
        ),
        source_path="data/raw/afghanistan_af.md",
        start_anchor="Provisioning time",
        end_anchor="1 week",
        country="Afghanistan",
        iso_code="AF",
        metadata={
            "row_key": "Provisioning time",
            "row_values": (
                "the Description is Provisioning is the process, "
                "the Global Pre-registration is 1 week"
            ),
        },
    )
    hit = type("Hit", (), {"block": block, "score": 0.95})()

    answer = ExtractiveAnswerer().answer(
        "What is the provisioning time for alphanumeric sender IDs in Afghanistan?",
        [hit],
    )

    assert answer.answer == "In Afghanistan, the provisioning time for alphanumeric sender IDs is 1 week."


def test_answerer_prefers_sender_provisioning_process_over_description_only_time_row() -> None:
    description_block = KnowledgeBlock(
        block_id="afghanistan-provisioning-description",
        document_id="afghanistan_af",
        title="Afghanistan (AF)",
        section_path=["Afghanistan (AF)", "Phone Numbers & Sender ID"],
        section_heading="Phone Numbers & Sender ID",
        block_type="table_fact",
        text="Provisioning time: Description=Provisioning is the approval process.",
        source_path="data/raw/afghanistan_af.md",
        start_anchor="Provisioning time",
        end_anchor="approval process",
        country="Afghanistan",
        iso_code="AF",
        metadata={
            "row_key": "Provisioning time",
            "row_values": "the Description is Provisioning is the approval process.",
        },
    )
    process_block = KnowledgeBlock(
        block_id="afghanistan-sender-provisioning",
        document_id="afghanistan_af",
        title="Afghanistan (AF)",
        section_path=["Afghanistan (AF)", "Guidelines"],
        section_heading="Guidelines",
        block_type="table_fact",
        text="Sender provisioning: Alpha sender, immediately. Numeric senders 7-14 days.",
        source_path="data/raw/afghanistan_af.md",
        start_anchor="Sender provisioning",
        end_anchor="7-14 days",
        country="Afghanistan",
        iso_code="AF",
        metadata={
            "row_key": "Sender provisioning",
            "row_values": "Alpha sender, immediately. Numeric senders 7-14 days.",
        },
    )
    description_hit = type("Hit", (), {"block": description_block, "score": 0.96})()
    process_hit = type("Hit", (), {"block": process_block, "score": 0.72})()

    answer = ExtractiveAnswerer().answer(
        "What is the sender provisioning process in Afghanistan?",
        [description_hit, process_hit],
    )

    assert "7-14 days" in answer.answer
    assert "approval process" not in answer.answer


def test_answerer_uses_any_preregistration_column_for_alphanumeric_duration() -> None:
    block = KnowledgeBlock(
        block_id="algeria-alpha-provisioning",
        document_id="algeria_dz",
        title="Algeria (DZ)",
        section_path=["Algeria (DZ)", "Phone Numbers & Sender ID"],
        section_heading="Phone Numbers & Sender ID",
        block_type="table_fact",
        text=(
            "Regarding Phone Numbers & Sender ID: Alphanumeric for Provisioning time: "
            "the Description is Provisioning is the process, the Domestic Pre-registration is 2 weeks"
        ),
        source_path="data/raw/algeria_dz.md",
        start_anchor="Provisioning time",
        end_anchor="2 weeks",
        country="Algeria",
        iso_code="DZ",
        metadata={
            "row_key": "Provisioning time",
            "row_values": (
                "the Description is Provisioning is the process, "
                "the Domestic Pre-registration is 2 weeks"
            ),
        },
    )
    hit = type("Hit", (), {"block": block, "score": 0.95})()

    answer = ExtractiveAnswerer().answer(
        "What is the provisioning time for alphanumeric sender IDs in Algeria?",
        [hit],
    )

    assert answer.answer == "In Algeria, the provisioning time for alphanumeric sender IDs is 2 weeks."


def test_table_extraction_row_aliases_cover_registration_receipts_and_defaults() -> None:
    assert "operator network capability" in HybridRetriever._target_row_keys(
        "For France, do I need to pre-register alphanumeric sender IDs and are dynamic senders supported?"
    )
    assert "handset delivery receipts" in HybridRetriever._target_row_keys(
        "Does Japan support handset delivery receipts for alphanumeric sender IDs?"
    )
    assert "sender id preserved" in HybridRetriever._target_row_keys(
        "What default sender ID is used in Albania if dynamic sender is not used?"
    )


def test_table_extraction_bonus_penalizes_description_only_provisioning_rows() -> None:
    description_block = KnowledgeBlock(
        block_id="uk-alpha-provisioning-description",
        document_id="united_kingdom_gb",
        title="United Kingdom (GB)",
        section_path=["United Kingdom (GB)", "Phone Numbers & Sender ID: Alphanumeric"],
        section_heading="Alphanumeric",
        block_type="table_fact",
        text="Provisioning time: Description=Provisioning is the approval process.",
        source_path="data/raw/united_kingdom_gb.md",
        start_anchor="Provisioning time",
        end_anchor="approval process",
        country="United Kingdom",
        iso_code="GB",
        metadata={
            "row_key": "Provisioning time",
            "row_values": "the Description is Provisioning is the approval process.",
        },
    )
    value_block = KnowledgeBlock(
        block_id="uk-alpha-network-capability",
        document_id="united_kingdom_gb",
        title="United Kingdom (GB)",
        section_path=["United Kingdom (GB)", "Phone Numbers & Sender ID: Alphanumeric"],
        section_heading="Alphanumeric",
        block_type="table_fact",
        text="Operator network capability: Pre-registration=Not Required; Dynamic=Supported",
        source_path="data/raw/united_kingdom_gb.md",
        start_anchor="Operator network capability",
        end_anchor="Dynamic=Supported",
        country="United Kingdom",
        iso_code="GB",
        metadata={
            "row_key": "Operator network capability",
            "row_values": "the Pre-registration is Not Required, the Dynamic is Supported",
        },
    )

    question = "What are the provisioning cost and pre-registration status for alphanumeric sender IDs in the UK?"

    assert HybridRetriever._table_extraction_bonus(question, SearchHit(block=value_block, score=0.1)) > 0
    assert HybridRetriever._table_extraction_bonus(question, SearchHit(block=description_block, score=0.1)) < 0


def test_block_iso_uses_document_suffix_for_nested_us_territory_titles() -> None:
    block = KnowledgeBlock(
        block_id="usvi-number-portability",
        document_id="united_states_virgin_islands_us_vi",
        title="United States Virgin Islands (US) (VI)",
        section_path=["United States Virgin Islands (US) (VI)", "Guidelines"],
        section_heading="Guidelines",
        block_type="table_fact",
        text="For Guidelines, the Number portability available is: No.",
        source_path="data/raw/united_states_virgin_islands_us_vi.md",
        start_anchor="Number portability available",
        end_anchor="No",
        country="United States Virgin Islands",
        iso_code="VI",
        metadata={"row_key": "Number portability available", "row_values": "No"},
    )
    retriever = HybridRetriever.__new__(HybridRetriever)
    retriever._country_index = {}

    assert retriever._block_iso(block) == "VI"


def test_answerer_formats_table_extraction_number_portability() -> None:
    block = KnowledgeBlock(
        block_id="us-number-portability",
        document_id="united_states_us",
        title="United States (US)",
        section_path=["United States (US)", "Guidelines"],
        section_heading="Guidelines",
        block_type="table_fact",
        text="For Guidelines, the Number portability available is: Yes.",
        source_path="data/raw/united_states_us.md",
        start_anchor="Number portability available",
        end_anchor="Yes",
        country="United States",
        iso_code="US",
        metadata={"row_key": "Number portability available", "row_values": "Yes"},
    )

    answer = ExtractiveAnswerer().answer(
        "Is number portability available for short codes in the United States?",
        [SearchHit(block=block, score=0.95)],
    )

    assert answer.answer == (
        "Yes. Number portability is available in United States; "
        "the `Number portability available` row says `Yes`."
    )


def test_answerer_formats_default_sender_values_from_table_row() -> None:
    block = KnowledgeBlock(
        block_id="albania-best-practices",
        document_id="albania_al",
        title="Albania (AL)",
        section_path=["Albania (AL)", "Phone Numbers & Sender ID: Alphanumeric"],
        section_heading="Alphanumeric",
        block_type="table_fact",
        text="Best practices: default sender IDs include Verify, Info, and System.",
        source_path="data/raw/albania_al.md",
        start_anchor="Best practices",
        end_anchor="System",
        country="Albania",
        iso_code="AL",
        metadata={
            "row_key": "Best practices",
            "row_values": "Default sender IDs include Verify, Info, and System.",
        },
    )

    answer = ExtractiveAnswerer().answer(
        "What default sender ID is used in Albania if dynamic sender is not used?",
        [SearchHit(block=block, score=0.95)],
    )

    assert answer.answer == "In Albania, the default sender IDs are Verify, Info, and System."


def test_answerer_does_not_treat_time_colons_as_nested_keys() -> None:
    block = KnowledgeBlock(
        block_id="colombia-exception-time",
        document_id="quiet_hours",
        title="Quiet Hours",
        section_path=["Quiet Hours", "Structured Fields", "Exceptions"],
        section_heading="Exceptions",
        block_type="structured_fact",
        text="- Exceptions: In Colombia, promotional and debt collection SMS can only be sent from 8:00 AM to 9:00 PM.",
        source_path="data/raw/quiet-hours.json",
        start_anchor="Exceptions",
        end_anchor="9:00 PM.",
        country="Colombia",
        iso_code="CO",
        metadata={
            "row_key": "Exceptions",
            "row_values": "In Colombia, promotional and debt collection SMS can only be sent from 8:00 AM to 9:00 PM.",
            "structured_value": "In Colombia, promotional and debt collection SMS can only be sent from 8:00 AM to 9:00 PM.",
        },
    )
    hit = type("Hit", (), {"block": block, "score": 0.9})()

    answer = ExtractiveAnswerer().answer("Promotional in Colombia?", [hit])

    assert answer.answer == "In Colombia, promotional and debt collection SMS can only be sent from 8:00 AM to 9:00 PM."
    assert "the 00 AM to 9 is" not in answer.answer


def test_rrf_merge_uses_configured_arm_weights() -> None:
    lexical_block = KnowledgeBlock(
        block_id="lexical",
        document_id="lexical_doc",
        title="Lexical",
        section_path=[],
        section_heading="",
        block_type="narrative",
        text="Exact sender registration wording.",
        source_path="data/raw/lexical.md",
        start_anchor="",
        end_anchor="",
    )
    vector_block = KnowledgeBlock(
        block_id="vector",
        document_id="vector_doc",
        title="Vector",
        section_path=[],
        section_heading="",
        block_type="narrative",
        text="Semantic sender onboarding wording.",
        source_path="data/raw/vector.md",
        start_anchor="",
        end_anchor="",
    )
    model = EmbeddingModel(Settings())
    retriever = HybridRetriever(
        BM25Index([lexical_block, vector_block]),
        VectorIndex([lexical_block, vector_block], model.encode([lexical_block.text, vector_block.text])),
        model,
        rrf_lexical_weight=3.0,
        rrf_vector_weight=0.5,
    )

    hits = retriever._rrf_merge(
        lexical_hits=[(lexical_block, 1.0)],
        vector_hits=[(vector_block, 1.0)],
    )
    scores = {hit.block.block_id: hit.score for hit in hits}

    assert scores["lexical"] > scores["vector"]


def test_document_diversity_moves_overflow_after_other_documents() -> None:
    blocks = [
        KnowledgeBlock(
            block_id=f"spain-{index}",
            document_id="spain_es",
            title="Spain",
            section_path=[],
            section_heading="",
            block_type="narrative",
            text=f"Spain fact {index}.",
            source_path="data/raw/spain_es.md",
            start_anchor="",
            end_anchor="",
        )
        for index in range(3)
    ]
    blocks.append(
        KnowledgeBlock(
            block_id="france-1",
            document_id="france_fr",
            title="France",
            section_path=[],
            section_heading="",
            block_type="narrative",
            text="France fact.",
            source_path="data/raw/france_fr.md",
            start_anchor="",
            end_anchor="",
        )
    )
    model = EmbeddingModel(Settings())
    retriever = HybridRetriever(
        BM25Index(blocks),
        VectorIndex(blocks, model.encode([block.text for block in blocks])),
        model,
        max_blocks_per_document=2,
    )

    hits = [SearchHit(block=block, score=1.0) for block in blocks]
    diverse = retriever._enforce_document_diversity(hits)

    assert [hit.block.block_id for hit in diverse] == ["spain-0", "spain-1", "france-1", "spain-2"]
