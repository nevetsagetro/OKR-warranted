from __future__ import annotations

import importlib
from dataclasses import dataclass, field
from typing import Any

from own_knowledge_rag.config import Settings


@dataclass
class ModelProbeResult:
    enabled: bool
    status: str
    checked_models: dict[str, str] = field(default_factory=dict)
    available_models: list[str] = field(default_factory=list)
    message: str = ""

    def as_dict(self) -> dict[str, object]:
        return {
            "enabled": self.enabled,
            "status": self.status,
            "checked_models": self.checked_models,
            "available_models": self.available_models,
            "message": self.message,
        }


def probe_provider_models(settings: Settings) -> ModelProbeResult:
    if not settings.provider_model_probe_enabled:
        return ModelProbeResult(
            enabled=False,
            status="skipped",
            message="Provider model-list probing is disabled. Set OKR_PROVIDER_MODEL_PROBE_ENABLED=true to probe configured providers at startup.",
        )

    checked = _configured_provider_models(settings)
    if not checked:
        return ModelProbeResult(
            enabled=True,
            status="skipped",
            message="No provider-backed model is configured for startup probing.",
        )

    unavailable: list[str] = []
    available_models: list[str] = []
    errors: list[str] = []

    if any(provider == "openai" for provider in checked.values()):
        try:
            openai_models = _list_openai_models()
            available_models.extend(openai_models)
            openai_set = set(openai_models)
            unavailable.extend(model for model, provider in checked.items() if provider == "openai" and model not in openai_set)
        except Exception as error:  # pragma: no cover - defensive around optional provider SDKs.
            errors.append(f"OpenAI model probe failed: {error}")

    gemini_models = [model for model, provider in checked.items() if provider == "gemini"]
    if gemini_models:
        try:
            listed_gemini_models = _list_gemini_models()
            available_models.extend(listed_gemini_models)
            gemini_set = set(listed_gemini_models)
            unavailable.extend(
                model
                for model in gemini_models
                if model not in gemini_set and f"models/{model}" not in gemini_set
            )
        except Exception as error:  # pragma: no cover - defensive around optional provider SDKs.
            errors.append(f"Gemini model probe failed: {error}")

    if errors:
        return ModelProbeResult(
            enabled=True,
            status="error",
            checked_models=checked,
            available_models=sorted(set(available_models)),
            message=" ".join(errors),
        )
    if unavailable:
        return ModelProbeResult(
            enabled=True,
            status="failed",
            checked_models=checked,
            available_models=sorted(set(available_models)),
            message=f"Configured provider models were not found: {', '.join(sorted(unavailable))}.",
        )
    return ModelProbeResult(
        enabled=True,
        status="passed",
        checked_models=checked,
        available_models=sorted(set(available_models)),
        message="Configured provider-backed models were found in provider model lists.",
    )


def _configured_provider_models(settings: Settings) -> dict[str, str]:
    checked: dict[str, str] = {}
    if settings.generation_provider.strip().lower() == "openai":
        checked[settings.generation_model] = "openai"
    if settings.embedding_provider.strip().lower() == "openai":
        checked[settings.embedding_model] = "openai"
    if settings.mapping_provider.strip().lower() in {"openai", "gemini"}:
        checked[settings.mapping_model] = settings.mapping_provider.strip().lower()
    return checked


def _list_openai_models() -> list[str]:
    module = importlib.import_module("openai")
    client = module.OpenAI()
    response = client.models.list()
    data: Any = getattr(response, "data", response)
    model_ids: list[str] = []
    for item in data:
        model_id = getattr(item, "id", None)
        if model_id is None and isinstance(item, dict):
            model_id = item.get("id")
        if model_id:
            model_ids.append(str(model_id))
    return model_ids


def _list_gemini_models() -> list[str]:
    module = importlib.import_module("google.genai")
    client = module.Client()
    models = client.models.list()
    model_ids: list[str] = []
    for item in models:
        model_id = getattr(item, "name", None) or getattr(item, "id", None)
        if model_id is None and isinstance(item, dict):
            model_id = item.get("name") or item.get("id")
        if model_id:
            model_ids.append(str(model_id))
    return model_ids
