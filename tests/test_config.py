import sys
from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from own_knowledge_rag.config import CANONICAL_TERM_GROUPS, CANONICAL_TERMS, CANONICAL_TERMS_VERSION, Settings
from own_knowledge_rag.model_probe import probe_provider_models


def test_canonical_terms_are_versioned_and_expanded() -> None:
    assert CANONICAL_TERMS_VERSION
    assert len(CANONICAL_TERMS) >= 60
    assert len(CANONICAL_TERM_GROUPS) >= 2
    assert "sender_identity" in CANONICAL_TERM_GROUPS
    assert "quiet hours" in CANONICAL_TERMS


def test_default_generation_model_is_allowlisted() -> None:
    settings = Settings(OKR_GENERATION_PROVIDER="openai")

    assert settings.generation_model == "gpt-4o-mini"
    assert settings.generation_model in settings.generation_model_allowlist


def test_provider_model_probe_is_disabled_by_default() -> None:
    result = probe_provider_models(Settings())

    assert result.enabled is False
    assert result.status == "skipped"


def test_provider_model_probe_checks_openai_models(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeModels:
        @staticmethod
        def list() -> SimpleNamespace:
            return SimpleNamespace(data=[SimpleNamespace(id="gpt-4o-mini")])

    class FakeOpenAI:
        models = FakeModels()

    monkeypatch.setitem(sys.modules, "openai", SimpleNamespace(OpenAI=lambda: FakeOpenAI()))
    settings = Settings(
        OKR_PROVIDER_MODEL_PROBE_ENABLED=True,
        OKR_MAPPING_PROVIDER="noop",
        OKR_GENERATION_PROVIDER="openai",
        OKR_GENERATION_MODEL="gpt-4o-mini",
    )

    result = probe_provider_models(settings)

    assert result.enabled is True
    assert result.status == "passed"
    assert result.checked_models == {"gpt-4o-mini": "openai"}


def test_retrieval_control_defaults_are_configured() -> None:
    settings = Settings()

    assert settings.rrf_lexical_weight == 1.0
    assert settings.rrf_vector_weight == 1.0
    assert settings.arm_k_multiplier == 3
    assert settings.max_blocks_per_document == 2


def test_settings_can_be_populated_by_field_name_for_cli_overrides() -> None:
    settings = Settings(mapping_provider="noop", embedding_provider="local")

    assert settings.mapping_provider == "noop"
    assert settings.embedding_provider == "local"


def test_generation_model_must_be_allowlisted_when_provider_enabled() -> None:
    with pytest.raises(ValidationError) as exc_info:
        Settings(
            OKR_GENERATION_PROVIDER="openai",
            OKR_GENERATION_MODEL="not-a-real-model",
            OKR_GENERATION_MODEL_ALLOWLIST=["gpt-4o-mini"],
        )

    assert "OKR_GENERATION_MODEL_ALLOWLIST" in str(exc_info.value)


def test_answer_thresholds_must_be_ordered() -> None:
    with pytest.raises(ValidationError) as exc_info:
        Settings(
            OKR_MIN_ANSWER_SCORE=0.6,
            OKR_TIER2_SCORE_THRESHOLD=0.55,
            OKR_TIER0_SCORE_THRESHOLD=0.75,
        )

    assert "OKR_TIER0_SCORE_THRESHOLD > OKR_TIER2_SCORE_THRESHOLD > OKR_MIN_ANSWER_SCORE" in str(exc_info.value)
