import hashlib
import json
from pathlib import Path
from own_knowledge_rag.config import Settings

_TEMPLATE_PATH = Path(__file__).parent / "templates" / "gui.html"
_PROMPT_PATH = Path(__file__).parents[2] / "docs" / "internal" / "prose_source_ingestion_enrichment_prompt.md"
_FAQ_PROMPT_PATH = Path(__file__).parents[2] / "docs" / "internal" / "faq_qa_source_fact_ingestion_prompt.md"


def _index_id(manifest: dict[str, object]) -> str:
    if not manifest:
        return ""
    documents_state = manifest.get("documents_state", {})
    payload = {
        "documents": manifest.get("documents", 0),
        "blocks": manifest.get("blocks", 0),
        "documents_state": documents_state if isinstance(documents_state, dict) else {},
        "parser_schema_version": manifest.get("parser_schema_version", ""),
        "normalizer_schema_version": manifest.get("normalizer_schema_version", ""),
        "mapping_provider": manifest.get("mapping_provider", ""),
        "mapping_model": manifest.get("mapping_model", ""),
        "embedding_provider": manifest.get("embedding_provider", ""),
        "embedding_model": manifest.get("embedding_model", ""),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()[:12]


def _document_ids_sample(manifest: dict[str, object], limit: int = 5) -> list[str]:
    documents_state = manifest.get("documents_state", {})
    if not isinstance(documents_state, dict):
        return []
    return sorted(str(document_id) for document_id in documents_state.keys())[:limit]


def _workspace_options(settings: Settings) -> list[dict[str, object]]:
    root = settings.work_dir.parent
    candidates = [settings.work_dir]
    if root.exists():
        candidates.extend(
            path
            for path in root.iterdir()
            if path.is_dir()
            and not path.name.startswith(".")
            and (
                path.name.startswith("work")
                or (path / "manifest.json").exists()
            )
        )

    seen: set[str] = set()
    options: list[dict[str, object]] = []
    for path in candidates:
        key = str(path.resolve()) if path.exists() else str(path)
        if key in seen:
            continue
        seen.add(key)
        ready = all((path / name).exists() for name in ("manifest.json", "blocks.json", "documents.json"))
        manifest: dict[str, object] = {}
        if ready:
            try:
                manifest = json.loads((path / "manifest.json").read_text(encoding="utf-8"))
            except Exception:
                manifest = {}
        kind = "baseline" if path == settings.work_dir else "experiment" if path.name.startswith("work_exp_") else "backup" if "_backup_" in path.name or "_pre_rollback_" in path.name else "workspace"
        options.append(
            {
                "path": str(path),
                "name": f"{path.name} (baseline)" if path == settings.work_dir else path.name,
                "kind": kind,
                "index_ready": ready,
                "documents": int(manifest.get("documents", 0) or 0),
                "blocks": int(manifest.get("blocks", 0) or 0),
                "manifest_path": str(path / "manifest.json"),
                "manifest_modified_at": int((path / "manifest.json").stat().st_mtime) if ready else 0,
                "index_id": _index_id(manifest),
                "document_ids_sample": _document_ids_sample(manifest),
            }
        )
    return sorted(
        options,
        key=lambda item: (
            0 if item["kind"] == "baseline" else 1 if item["kind"] == "experiment" else 2,
            str(item["path"]),
        ),
    )

def render_gui(settings: Settings, mode: str = "user") -> str:
    enrichment_prompt_template = ""
    if _PROMPT_PATH.exists():
        enrichment_prompt_template = _PROMPT_PATH.read_text(encoding="utf-8")
    faq_prompt_template = ""
    if _FAQ_PROMPT_PATH.exists():
        faq_prompt_template = _FAQ_PROMPT_PATH.read_text(encoding="utf-8")
    defaults = {
        "sourceDir": str(settings.source_dir),
        "workDir": str(settings.work_dir),
        "workspaceOptions": _workspace_options(settings),
        "allowedSuffixes": [".json", ".md", ".txt"],
        "topK": settings.top_k,
        "benchmarkPath": "benchmarks/real_corpus_smoke.json",
        "experimentBenchmarkPath": "",
        "experimentBaselineWorkDir": str(settings.work_dir),
        "experimentSourceDir": str(settings.work_dir.parent / "experiment_sources" / "exp_candidate" / "raw"),
        "experimentWorkDir": str(settings.work_dir.parent / "work_experiment_candidate"),
        "chunkSize": settings.chunk_size,
        "chunkOverlap": settings.chunk_overlap,
        "mappingProvider": settings.mapping_provider,
        "mappingModel": settings.mapping_model,
        "mappingBatchSize": settings.mapping_batch_size,
        "mappingBatchDelayMs": settings.mapping_batch_delay_ms,
        "mappingTextCharLimit": settings.mapping_text_char_limit,
        "mappingPromptMode": settings.mapping_prompt_mode,
        "mappingRetryMissingResults": settings.mapping_retry_missing_results,
        "embeddingProvider": settings.embedding_provider,
        "embeddingModel": settings.embedding_model,
        "embeddingDevice": settings.embedding_device,
        "embeddingDimensions": settings.embedding_dimensions,
        "vectorBackend": settings.vector_backend,
        "vectorCollection": settings.vector_collection,
        "qdrantUrl": settings.qdrant_url,
        "rerankerProvider": settings.reranker_provider,
        "rerankerModel": settings.reranker_model,
        "rerankerTopN": settings.reranker_top_n,
        "enrichmentPromptTemplate": enrichment_prompt_template,
        "enrichmentPromptPath": str(_PROMPT_PATH),
        "faqPromptTemplate": faq_prompt_template,
        "faqPromptPath": str(_FAQ_PROMPT_PATH),
    }
    
    if not _TEMPLATE_PATH.exists():
        # Fallback if template missing
        return "<html><body>Template not found</body></html>"

    html = _TEMPLATE_PATH.read_text(encoding="utf-8")
    
    html = html.replace("{{defaults_json}}", json.dumps(defaults))
    html = html.replace("{{mode}}", mode)
    
    return html
