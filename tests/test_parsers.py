from pathlib import Path

import pytest

from own_knowledge_rag.models import ParsedDocument
from own_knowledge_rag.parsers import DocumentValidationError, parse_file, parsed_document_validation_issues


def test_parse_json_table_payload_creates_structured_text(tmp_path: Path) -> None:
    path = tmp_path / "spain_es.json"
    path.write_text(
        """
{
  "source_url": "https://example.com/es",
  "locale_code": "es",
  "locale_name": "Spain (ES)",
  "tables": [
    {
      "title": "Phone Numbers & Sender ID",
      "section": "Alphanumeric",
      "type": "matrix",
      "items": [
        {
          "field": "Twilio supported",
          "description": "Whether supported.",
          "values": {
            "Pre-registration": "---",
            "Dynamic": "Supported"
          }
        }
      ]
    }
  ]
}
""".strip(),
        encoding="utf-8",
    )

    document = parse_file(path)

    assert document is not None
    assert document.content_type == "json"
    assert document.title == "Spain (ES)"
    assert "## Phone Numbers & Sender ID: Alphanumeric" in document.text
    assert "- Twilio supported: Description=Whether supported.; Pre-registration=---; Dynamic=Supported" in document.text


def test_parse_json_catalog_payload_creates_catalog_text(tmp_path: Path) -> None:
    path = tmp_path / "index.json"
    path.write_text(
        """
{
  "source_index_url": "https://example.com/index",
  "locale_count": 2,
  "locales": [
    {
      "locale_name": "Spain (ES)",
      "locale_code": "es",
      "source_url": "https://example.com/es"
    },
    {
      "locale_name": "Sri Lanka (LK)",
      "locale_code": "lk",
      "source_url": "https://example.com/lk"
    }
  ]
}
""".strip(),
        encoding="utf-8",
    )

    document = parse_file(path)

    assert document is not None
    assert document.content_type == "json"
    assert "## Locales" in document.text
    assert "- Spain (ES): Locale code=es; Source URL=https://example.com/es" in document.text


def test_parse_json_source_facts_payload_preserves_fact_values(tmp_path: Path) -> None:
    path = tmp_path / "global-restriction.json"
    path.write_text(
        """
{
  "document_title": "Global SMS Sender Registration Requirements",
  "content_type": "messaging_rules",
  "source_facts": [
    {
      "field": "operator_requirement",
      "value": "GrameenPhone, Robi/Axiata, TeleTalk",
      "applies_to": "Bangladesh",
      "condition": "mandatory registration",
      "source_quote": "Mandatory for GrameenPhone, Robi/Axiata, and TeleTalk networks",
      "local_aliases": ["mandatory registration"]
    }
  ],
  "tables": [],
  "notes": []
}
""".strip(),
        encoding="utf-8",
    )

    document = parse_file(path)

    assert document is not None
    assert document.content_type == "json"
    assert document.title == "Global Restriction"
    assert "## Source Facts" in document.text
    assert "- operator_requirement: Value=GrameenPhone, Robi/Axiata, TeleTalk" in document.text
    assert "applies_to=Bangladesh" in document.text
    assert "condition=mandatory registration" in document.text


def test_parse_json_source_facts_payload_supports_curated_fact_schema(tmp_path: Path) -> None:
    path = tmp_path / "bangladesh-registration.json"
    path.write_text(
        """
{
  "document_id": "bangladesh_sender_registration",
  "title": "Bangladesh Sender Registration",
  "language": "en",
  "source_type": "human_curated",
  "domain": "telecommunications",
  "source_facts": [
    {
      "fact_id": "bangladesh_grameenphone_registration_001",
      "fact_type": "registration",
      "topic": "Sender registration for GrameenPhone",
      "value": "Sender registration is mandatory for GrameenPhone in Bangladesh.",
      "structured_fields": {
        "country_iso2": "BD",
        "operator_name": "GrameenPhone",
        "registration_scope": "operator_specific"
      },
      "applies_to": ["sms"],
      "conditions": ["mandatory registration"],
      "exceptions": [],
      "source_anchor": "Bangladesh row, GrameenPhone requirement"
    }
  ]
}
""".strip(),
        encoding="utf-8",
    )

    document = parse_file(path)

    assert document is not None
    assert document.content_type == "json"
    assert "- registration: Value=Sender registration is mandatory for GrameenPhone in Bangladesh." in document.text
    assert "country_iso2=BD" in document.text
    assert "operator_name=GrameenPhone" in document.text
    assert "registration_scope=operator_specific" in document.text
    assert "source_anchor=Bangladesh row, GrameenPhone requirement" in document.text


def test_parse_json_repairs_unescaped_inner_quotes(tmp_path: Path) -> None:
    path = tmp_path / "benin-faq.json"
    path.write_text(
        """
{
  "document_title": "Benin FAQ Source Facts",
  "content_type": "faq_source_facts",
  "source_facts": [
    {
      "fact_id": "benin-number-format-change",
      "field": "FAQ answer",
      "fact_type": "provisioning",
      "topic": "number format",
      "value": "The old format changed to a new 10-digit format, for example, by adding "01" after the country code.",
      "country_iso2": "BJ",
      "applies_to": "Benin",
      "structured_fields": {
        "question": "What changed in the Benin phone number format?",
        "answer": "The old format changed to a new 10-digit format, for example, by adding "01" after the country code.",
        "question_pattern": "faq"
      },
      "source_anchor": "Benin number format",
      "source_quote": "by adding "01" after the country code"
    }
  ]
}
""".strip(),
        encoding="utf-8",
    )

    document = parse_file(path)

    assert document is not None
    assert document.content_type == "json"
    assert "json_repaired:escaped_unescaped_inner_quotes" in document.parse_warnings
    assert 'by adding "01" after the country code' in document.text


def test_parse_json_restores_known_quoted_tokens_in_source_truth_fields(tmp_path: Path) -> None:
    path = tmp_path / "sender-faq.json"
    path.write_text(
        """
{
  "document_title": "Sender FAQ Source Facts",
  "content_type": "faq_source_facts",
  "source_facts": [
    {
      "fact_id": "sender-token-preservation",
      "fact_type": "content_restriction",
      "value": "Avoid generic sender IDs such as InfoSMS or Verify and use #Nevetscorp where required.",
      "structured_fields": {
        "question": "Which sender tokens matter?",
        "answer": "Avoid InfoSMS, Verify, and #Nevetscorp."
      },
      "local_aliases": ["InfoSMS", "Verify", "#Nevetscorp"],
      "source_quote": "Use # for registry prefixes, and avoid InfoSMS or Verify."
    }
  ]
}
""".strip(),
        encoding="utf-8",
    )

    document = parse_file(path)

    assert document is not None
    assert "json_normalized:restored_known_quoted_tokens" in document.parse_warnings
    assert 'such as "InfoSMS" or "Verify"' in document.text
    assert 'use "#Nevetscorp" where required' in document.text
    assert 'answer=Avoid "InfoSMS", "Verify", and "#Nevetscorp".' in document.text
    assert 'local_aliases="InfoSMS", "Verify", "#Nevetscorp"' in document.text
    assert 'Use "#" for registry prefixes' in document.text


def test_parse_enriched_blocks_payload_creates_atomic_source_facts(tmp_path: Path) -> None:
    path = tmp_path / "telecom_sms_registration_taxonomy_enriched_blocks.json"
    path.write_text(
        """
{
  "prompt_version": "v3.0",
  "blocks": [
    {
      "block_id": "registration-taxonomy-australia-general-mandatory-registration",
      "country": "Australia",
      "iso_code": null,
      "sender_types": ["alphanumeric sender id"],
      "regulation_topics": ["pre-registration"],
      "answer_signal": "standalone_fact",
      "enriched_text": "In Australia, sender ID pre-registration is mandatory for all SMS traffic.",
      "hypothetical_questions": [
        "Does Australia require sender registration for all SMS traffic?"
      ],
      "source_category": "general mandatory registration"
    }
  ]
}
""".strip(),
        encoding="utf-8",
    )

    document = parse_file(path)

    assert document is not None
    assert "## Source Facts" in document.text
    assert "- registration: Value=In Australia, sender ID pre-registration is mandatory" in document.text
    assert "country_name=Australia" in document.text
    assert "country_iso2=AU" in document.text
    assert "Does Australia require sender registration" in document.text
    assert "prompt_version: v3.0" not in document.text


def test_parse_fenced_json_results_payload_creates_atomic_source_facts(tmp_path: Path) -> None:
    path = tmp_path / "quiet-hours.json"
    path.write_text(
        """
```json
{
  "results": [
    {
      "block_id": "brazil-time-restrictions",
      "country": "Brazil",
      "iso_code": "BR",
      "sender_types": [],
      "regulation_topics": ["quiet hours", "content restriction"],
      "answer_signal": "standalone_fact",
      "enriched_text": "In Brazil, promotional SMS is allowed Monday-Friday 8:00 AM-8:00 PM and Saturday 8:00 AM-2:00 PM. Sunday sending is not allowed.",
      "hypothetical_questions": [
        "What are the promotional SMS sending hours in Brazil?",
        "Can I send promotional SMS on Sundays in Brazil?"
      ],
      "local_aliases": [],
      "reasoning": ""
    }
  ]
}
```
""".strip(),
        encoding="utf-8",
    )

    document = parse_file(path)

    assert document is not None
    assert document.content_type == "json"
    assert "## Source Facts" in document.text
    assert "- content_restriction: Value=In Brazil, promotional SMS is allowed" in document.text
    assert "country_name=Brazil" in document.text
    assert "country_iso2=BR" in document.text
    assert "What are the promotional SMS sending hours in Brazil?" in document.text


def test_parse_top_level_source_fact_list_creates_atomic_source_facts(tmp_path: Path) -> None:
    path = tmp_path / "quiet-hours.json"
    path.write_text(
        """
[
  {
    "fact_id": "united_states_quiet_hours_001",
    "fact_type": "quiet_hours",
    "topic": "United States promotional SMS sending window",
    "value": "In United States, SMS advertising should not be sent before 8:00 AM or after 9:00 PM local time.",
    "structured_fields": {
      "country_name": "United States",
      "country_iso2": "US",
      "traffic_type": "promotional_sms"
    },
    "applies_to": ["United States"],
    "conditions": ["advertising SMS"],
    "source_anchor": "quiet_hours.united_states"
  }
]
""".strip(),
        encoding="utf-8",
    )

    document = parse_file(path)

    assert document is not None
    assert document.content_type == "json"
    assert "## Source Facts" in document.text
    assert "- quiet_hours: Value=In United States, SMS advertising should not be sent" in document.text
    assert "country_iso2=US" in document.text
    assert "traffic_type=promotional_sms" in document.text
    assert "## Structured Fields" not in document.text


def test_parse_top_level_enriched_list_creates_atomic_source_facts(tmp_path: Path) -> None:
    path = tmp_path / "quiet-hours.json"
    path.write_text(
        """
[
  {
    "block_id": "united-states-time-restrictions",
    "country": "United States",
    "iso_code": "US",
    "regulation_topics": ["quiet hours", "content restriction"],
    "answer_signal": "standalone_fact",
    "enriched_text": "In United States, SMS advertising should not be sent before 8:00 AM or after 9:00 PM local time.",
    "hypothetical_questions": [
      "What quiet hours apply to SMS advertising in United States?"
    ]
  }
]
""".strip(),
        encoding="utf-8",
    )

    document = parse_file(path)

    assert document is not None
    assert "## Source Facts" in document.text
    assert "- quiet_hours: Value=In United States, SMS advertising should not be sent" in document.text
    assert "country_name=United States" in document.text
    assert "country_iso2=US" in document.text
    assert "What quiet hours apply to SMS advertising in United States?" in document.text


def test_parse_real_corpus_json_sidecar(tmp_path: Path) -> None:
    source = Path("data/raw/spain_es.json")
    document = parse_file(source)

    assert document is not None
    assert document.title == "Spain (ES)"
    assert "Twilio supported" in document.text


def test_parse_rejects_binary_like_text(tmp_path: Path) -> None:
    path = tmp_path / "broken.md"
    path.write_text("# Broken\n\nvalid prefix\x00invalid payload\n", encoding="utf-8")

    with pytest.raises(DocumentValidationError) as exc_info:
        parse_file(path)

    assert exc_info.value.issues[0].code == "binary_text"


def test_parse_non_utf8_file_records_encoding_fallback(tmp_path: Path) -> None:
    path = tmp_path / "latin.md"
    path.write_bytes("# España\n\nRegistro de remitente requerido.\n".encode("latin-1"))

    document = parse_file(path)

    assert document is not None
    assert "España" in document.text
    assert document.encoding_fallback is True
    assert document.encoding_detected
    assert document.parse_warnings


def test_parsed_document_validation_warns_when_markdown_has_no_heading() -> None:
    document = ParsedDocument(
        document_id="notes",
        title="Notes",
        source_path="notes.md",
        content_type="markdown",
        text="A paragraph without a heading.",
    )

    issues = parsed_document_validation_issues(document)

    assert [issue.code for issue in issues] == ["markdown_missing_heading"]
    assert issues[0].severity == "warning"
