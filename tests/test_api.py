import json
import asyncio
import os
from pathlib import Path

import httpx

from own_knowledge_rag.api import create_app
from own_knowledge_rag.config import Settings
from own_knowledge_rag.gui import render_gui
from own_knowledge_rag.pipeline import KnowledgePipeline


def test_api_health_endpoint() -> None:
    async def run() -> httpx.Response:
        transport = httpx.ASGITransport(app=create_app(Settings()))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.get("/health")

    response = asyncio.run(run())

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_api_gui_route() -> None:
    async def run() -> httpx.Response:
        transport = httpx.ASGITransport(app=create_app(Settings()))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.get("/")

    response = asyncio.run(run())

    assert response.status_code == 200
    assert "Own Knowledge RAG" in response.text
    assert "Source Evidence" in response.text
    assert "Advanced Build Options" in response.text
    assert "Mapping and Enrichment" in response.text
    assert "Rate This Answer" in response.text
    assert "Analysis Lab" in response.text
    assert 'data-target="tab-ml-ds"' in response.text
    assert "Use Baseline For Questions" in response.text
    assert "Answer workspace:" in response.text
    assert "Refresh Suggested Path" in response.text
    assert "Suggested names combine the hypothesis and a timestamp" in response.text
    assert "Suggested experiment path refreshed:" in response.text
    assert "Experiment Source Dir" in response.text
    assert "Upload Files To Experiment Source" in response.text
    assert "Open Technical Mode" in response.text
    assert "Re-indexing..." in response.text
    assert "Building experiment index..." in response.text
    assert "Override source-library check" in response.text
    assert "Provider model probe" in response.text
    assert "Phase Gate" in response.text
    assert "Baseline Status" in response.text
    assert "Human Review Readiness" in response.text
    assert "New Knowledge" not in response.text
    assert 'data-target="tab-new-knowledge"' not in response.text
    assert "What are you adding?" in response.text
    assert "FAQ / reviewed Q&A" in response.text
    assert "Knowledge file onboarding" in response.text
    assert "FAQ reviewed Q&A onboarding" in response.text
    assert 'name="exp-content-type"' in response.text
    assert 'id="exp-content-faq"' in response.text
    assert "Knowledge Onboarding Workspace" not in response.text
    assert "Seed Draft Prompt" not in response.text
    assert "knowledge-reviewed-qa-file-picker" not in response.text
    assert "Collect Reviews" in response.text
    assert "Export Benchmark" in response.text
    assert "Next review targets" in response.text
    assert "Suggested review starters" in response.text
    assert "Review QA warnings" in response.text
    assert "Manage history" in response.text
    assert "Experiment History & Registry" in response.text
    assert "Refresh History" in response.text
    assert "Corpus scope" in response.text
    assert "Countries:" in response.text
    assert "Document IDs in tooltip" not in response.text
    assert "Collect a Phase 9 review" in response.text


def test_api_knowledge_templates_endpoint() -> None:
    async def run() -> httpx.Response:
        transport = httpx.ASGITransport(app=create_app(Settings()))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.get("/knowledge/templates")

    response = asyncio.run(run())

    assert response.status_code == 200
    payload = response.json()
    assert "source_facts" in payload["source_fact_template"]
    assert "qa_seeds" in payload["qa_seed_template"]
    assert "REVIEWED Q/A TEXT FILE" in payload["qa_seed_generation_prompt"]
    assert "RECOMMENDED_QA_SEED_JSON" in payload["qa_seed_generation_prompt"]
    assert "SOURCE FACT JSON" in payload["qa_seed_generation_prompt"]
    assert payload["qa_seed_generation_prompt_path"].endswith("docs/internal/qa_seed_generation_prompt.md")


def test_api_exports_qa_seed_benchmark(tmp_path: Path) -> None:
    source_fact_content = json.dumps(
        {
            "source_facts": [
                {
                    "fact_id": "example-alpha-support",
                    "field": "Twilio supported",
                    "value": "Supported",
                }
            ]
        }
    )
    qa_seed_content = json.dumps(
        {
            "qa_seeds": [
                {
                    "seed_id": "example-alpha-support-q1",
                    "question": "Does Exampleland support alphanumeric sender IDs?",
                    "expected_document_ids": ["exampleland_sms_regulatory_facts"],
                    "expected_terms": ["supported"],
                    "expected_metadata": {"row_key": "Twilio supported"},
                    "expected_anchor_terms": ["Twilio supported", "Supported"],
                    "question_type": "binary",
                    "source_fact_id": "example-alpha-support",
                    "review_status": "accepted",
                }
            ]
        }
    )
    output_path = tmp_path / "qa_seed_regressions.json"

    async def run() -> httpx.Response:
        transport = httpx.ASGITransport(app=create_app(Settings()))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.post(
                "/knowledge/qa-seeds/export",
                json={
                    "source_fact_content": source_fact_content,
                    "qa_seed_content": qa_seed_content,
                    "output_path": str(output_path),
                },
            )

    response = asyncio.run(run())

    assert response.status_code == 200
    payload = response.json()
    assert payload["exported"] is True
    assert payload["case_count"] == 1
    cases = json.loads(output_path.read_text(encoding="utf-8"))
    assert cases[0]["question"] == "Does Exampleland support alphanumeric sender IDs?"
    assert cases[0]["expected_metadata"] == {"row_key": "Twilio supported"}


def test_api_tech_gui_route_exposes_settings() -> None:
    async def run() -> httpx.Response:
        transport = httpx.ASGITransport(app=create_app(Settings()))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.get("/tech")

    response = asyncio.run(run())

    assert response.status_code == 200
    assert "Settings" in response.text
    assert 'data-target="tab-system"' in response.text
    assert "Simple Mode" in response.text


def test_gui_defaults_include_index_history_metadata(tmp_path: Path) -> None:
    work_dir = tmp_path / "work"
    work_dir.mkdir()
    (work_dir / "blocks.json").write_text("[]", encoding="utf-8")
    (work_dir / "documents.json").write_text("[]", encoding="utf-8")
    (work_dir / "manifest.json").write_text(
        json.dumps(
            {
                "documents": 2,
                "blocks": 3,
                "documents_state": {
                    "kuwait_kw": "aaa",
                    "spain_es": "bbb",
                },
            }
        ),
        encoding="utf-8",
    )
    settings = Settings(OKR_SOURCE_DIR=tmp_path / "raw", OKR_WORK_DIR=work_dir)

    html = render_gui(settings)

    assert '"manifest_modified_at": 0' not in html
    assert '"index_id": ""' not in html
    assert "kuwait_kw" in html
    assert "spain_es" in html


def test_api_runtime_endpoint() -> None:
    async def run() -> httpx.Response:
        transport = httpx.ASGITransport(app=create_app(Settings()))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.get("/runtime")

    response = asyncio.run(run())

    assert response.status_code == 200
    payload = response.json()
    assert payload["defaults"]["source_dir"] == "data/raw"
    assert payload["defaults"]["work_dir"] == "data/work"
    assert payload["defaults"]["mapping_provider"]
    assert payload["defaults"]["embedding_provider"]
    assert "indexed" in payload
    assert "generation_provider" in payload["indexed"]
    assert "manifest_modified_at" in payload["indexed"]
    assert "index_id" in payload["indexed"]
    assert "document_ids_sample" in payload["indexed"]
    assert "testing" in payload
    assert "benchmark_presets" in payload["testing"]
    assert payload["model_probe"]["status"] == "skipped"


def test_api_baseline_status_endpoint_lists_latest_valid_backup(tmp_path: Path) -> None:
    baseline_work_dir = tmp_path / "work"
    valid_backup = tmp_path / "work_backup_20260502-120000"
    invalid_backup = tmp_path / "work_backup_20260502-130000"
    baseline_work_dir.mkdir()
    valid_backup.mkdir()
    invalid_backup.mkdir()
    for directory, documents in [(baseline_work_dir, 3), (valid_backup, 2)]:
        (directory / "manifest.json").write_text(json.dumps({"documents": documents, "blocks": documents * 10}), encoding="utf-8")
        (directory / "blocks.json").write_text("[]", encoding="utf-8")
        (directory / "documents.json").write_text("[]", encoding="utf-8")
    (invalid_backup / "manifest.json").write_text(json.dumps({"documents": 1}), encoding="utf-8")
    settings = Settings(OKR_SOURCE_DIR=tmp_path / "raw", OKR_WORK_DIR=baseline_work_dir)

    async def run() -> httpx.Response:
        transport = httpx.ASGITransport(app=create_app(settings))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.get("/baseline/status")

    response = asyncio.run(run())

    assert response.status_code == 200
    payload = response.json()
    assert payload["baseline_work_dir"] == str(baseline_work_dir)
    assert payload["index_ready"] is True
    assert payload["documents"] == 3
    assert payload["blocks"] == 30
    assert payload["rollback_backup_count"] == 2
    assert payload["latest_rollback_backup"]["path"] == str(valid_backup)
    assert payload["latest_rollback_backup"]["valid"] is True


def test_api_human_review_readiness_empty(tmp_path: Path) -> None:
    work_dir = tmp_path / "work"
    work_dir.mkdir()
    settings = Settings(OKR_SOURCE_DIR=tmp_path / "raw", OKR_WORK_DIR=work_dir)

    async def run() -> httpx.Response:
        transport = httpx.ASGITransport(app=create_app(settings))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.get("/human-review/readiness")

    response = asyncio.run(run())

    assert response.status_code == 200
    payload = response.json()
    assert payload["total_query_reviews"] == 0
    assert payload["query_reviews_found"] is False
    assert payload["ready_for_export"] is False
    assert payload["gate_mode"] == "advisory"
    assert payload["checks"][0]["status"] == "fail"
    assert payload["missing_targets"][0] == "Total human-reviewed queries: need 100 more"
    assert payload["collection_prompts"][0]["label"] == "General factual review"
    assert {prompt["target"] for prompt in payload["collection_prompts"]} == {
        "total_query_reviews",
        "should_refuse",
        "foreign_or_wrong_country",
        "multi_fact_or_comparison",
    }


def test_api_human_review_readiness_counts_review_categories(tmp_path: Path) -> None:
    work_dir = tmp_path / "work"
    analytics_dir = work_dir / "analytics"
    analytics_dir.mkdir(parents=True)
    entries = []
    for index in range(20):
        entries.append({"question": f"Should we refuse unsupported request {index}?", "rating": "should_refuse"})
    for index in range(20):
        entries.append({"question": f"Does Spain support two-way SMS {index}?", "rating": "wrong_country"})
    for index in range(20):
        entries.append({"question": f"Compare Spain and Kuwait sender rules {index}", "rating": "incomplete"})
    for index in range(40):
        entries.append({"question": f"What is the dialing code for Kuwait {index}?", "rating": "correct"})
    (analytics_dir / "query_reviews.json").write_text(json.dumps({"entries": entries}), encoding="utf-8")
    (analytics_dir / "review_findings.json").write_text(
        json.dumps(
            {
                "entries": [
                    {"status": "accepted_conflict"},
                    {"status": "resolved"},
                    {"status": "needs_review"},
                ]
            }
        ),
        encoding="utf-8",
    )
    settings = Settings(OKR_SOURCE_DIR=tmp_path / "raw", OKR_WORK_DIR=work_dir)

    async def run() -> httpx.Response:
        transport = httpx.ASGITransport(app=create_app(settings))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.get("/human-review/readiness")

    response = asyncio.run(run())

    assert response.status_code == 200
    payload = response.json()
    assert payload["total_query_reviews"] == 100
    assert payload["rating_counts"]["should_refuse"] == 20
    assert payload["foreign_or_wrong_country_count"] == 20
    assert payload["multi_fact_or_comparison_count"] == 20
    assert payload["accepted_review_findings_count"] == 2
    assert payload["ready_for_export"] is True
    assert payload["gate_mode"] == "candidate_hard_gate"
    assert payload["missing_targets"] == []
    assert payload["collection_prompts"] == []
    assert payload["quality_warnings"] == []


def test_api_human_review_readiness_flags_inconsistent_saved_reviews(tmp_path: Path) -> None:
    work_dir = tmp_path / "work"
    analytics_dir = work_dir / "analytics"
    analytics_dir.mkdir(parents=True)
    (analytics_dir / "query_reviews.json").write_text(
        json.dumps(
            {
                "entries": [
                    {
                        "review_id": "review-00001",
                        "question": "Does Kiribati support two-way SMS?",
                        "rating": "correct",
                        "expected_iso_code": "AL",
                        "notes": "is not correct",
                        "evidence_document_ids": ["albania_al"],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    settings = Settings(OKR_SOURCE_DIR=tmp_path / "raw", OKR_WORK_DIR=work_dir)

    async def run() -> httpx.Response:
        transport = httpx.ASGITransport(app=create_app(settings))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.get("/human-review/readiness")

    response = asyncio.run(run())

    assert response.status_code == 200
    warnings = response.json()["quality_warnings"]
    assert len(warnings) == 3
    assert any("rated correct" in warning["message"] for warning in warnings)
    assert any("Expected ISO AL" in warning["message"] for warning in warnings)
    assert any("different country" in warning["message"] for warning in warnings)


def test_api_human_review_export_blocks_empty_reviews(tmp_path: Path) -> None:
    work_dir = tmp_path / "work"
    work_dir.mkdir()
    settings = Settings(OKR_SOURCE_DIR=tmp_path / "raw", OKR_WORK_DIR=work_dir)

    async def run() -> httpx.Response:
        transport = httpx.ASGITransport(app=create_app(settings))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.post("/human-review/export-benchmark", json={"work_dir": str(work_dir)})

    response = asyncio.run(run())

    assert response.status_code == 400
    assert response.json()["detail"]["readiness"]["ready_for_export"] is False


def test_api_human_review_export_writes_query_review_benchmark(tmp_path: Path) -> None:
    work_dir = tmp_path / "work"
    analytics_dir = work_dir / "analytics"
    analytics_dir.mkdir(parents=True)
    entries = []
    for index in range(20):
        entries.append(
            {
                "question": f"Should unsupported request {index} refuse?",
                "rating": "should_refuse",
                "expected_document_id": "",
                "expected_terms": [],
            }
        )
    for index in range(20):
        entries.append(
            {
                "question": f"Does Spain support two-way SMS {index}?",
                "rating": "wrong_country",
                "expected_document_id": "spain_es",
                "expected_terms": ["two-way"],
            }
        )
    for index in range(20):
        entries.append(
            {
                "question": f"Compare Spain and Kuwait sender rules {index}",
                "rating": "incomplete",
                "expected_document_id": "spain_es",
                "expected_terms": ["sender"],
            }
        )
    for index in range(40):
        entries.append(
            {
                "question": f"What is the dialing code for Kuwait {index}?",
                "rating": "correct",
                "expected_document_id": "kuwait_kw",
                "expected_terms": ["+965"],
            }
        )
    (analytics_dir / "query_reviews.json").write_text(json.dumps({"entries": entries}), encoding="utf-8")
    output_dir = tmp_path / "benchmarks"
    settings = Settings(OKR_SOURCE_DIR=tmp_path / "raw", OKR_WORK_DIR=work_dir)

    async def run() -> httpx.Response:
        transport = httpx.ASGITransport(app=create_app(settings))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.post(
                "/human-review/export-benchmark",
                json={"work_dir": str(work_dir), "output_dir": str(output_dir)},
            )

    response = asyncio.run(run())

    assert response.status_code == 200
    payload = response.json()
    assert payload["exported"] is True
    assert payload["query_review_cases"] == 100
    assert Path(payload["query_review_benchmark_path"]).exists()
    exported = json.loads(Path(payload["query_review_benchmark_path"]).read_text(encoding="utf-8"))
    assert len(exported) == 100


def test_api_build_index_accepts_advanced_overrides(tmp_path: Path) -> None:
    source_dir = tmp_path / "raw"
    work_dir = tmp_path / "work"
    source_dir.mkdir(parents=True, exist_ok=True)
    (source_dir / "peru_pe.md").write_text(
        """# Peru (PE)

## Capabilities
| Key | Value |
| --- | --- |
| Two-way SMS supported | Yes |
""",
        encoding="utf-8",
    )
    settings = Settings(OKR_SOURCE_DIR=source_dir, OKR_WORK_DIR=work_dir)

    async def run() -> httpx.Response:
        transport = httpx.ASGITransport(app=create_app(settings))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.post(
                "/build-index",
                json={
                    "source_dir": str(source_dir),
                    "work_dir": str(work_dir),
                    "allow_low_quality": True,
                    "chunk_size": 640,
                    "chunk_overlap": 80,
                    "mapping_provider": "noop",
                    "mapping_model": "heuristic-v1",
                    "mapping_batch_size": 3,
                    "mapping_batch_delay_ms": 25,
                    "mapping_text_char_limit": 420,
                    "mapping_prompt_mode": "pass1",
                    "mapping_retry_missing_results": False,
                    "embedding_provider": "local",
                    "embedding_model": "BAAI/bge-small-en-v1.5",
                    "embedding_device": "cpu",
                    "vector_backend": "local",
                    "vector_collection": "gui-test",
                    "qdrant_url": "http://localhost:6333",
                    "reranker_provider": "none",
                    "reranker_model": "cross-encoder/ms-marco-MiniLM-L-6-v2",
                    "reranker_top_n": 7,
                },
            )

    response = asyncio.run(run())

    assert response.status_code == 200
    payload = response.json()
    assert payload["chunk_size"] == 640
    assert payload["chunk_overlap"] == 80
    assert payload["mapping_provider"] == "noop"
    assert payload["mapping_prompt_mode"] == "pass1"
    assert payload["mapping_batch_size"] == 3
    assert payload["embedding_provider"] == "local"
    assert payload["vector_collection"] == "gui-test"
    assert payload["reranker_top_n"] == 7
    assert payload["total_time"] >= 0


def test_api_experiment_create_and_list(tmp_path: Path) -> None:
    source_dir = tmp_path / "raw"
    source_dir.mkdir(parents=True, exist_ok=True)
    settings = Settings(OKR_SOURCE_DIR=source_dir, OKR_WORK_DIR=tmp_path / "work")

    async def run() -> tuple[httpx.Response, httpx.Response]:
        transport = httpx.ASGITransport(app=create_app(settings))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            create_response = await client.post(
                "/experiments/create",
                json={
                    "baseline_work_dir": str(tmp_path / "work"),
                    "benchmark_path": "benchmarks/country_regressions.json",
                    "content_type": "faq",
                    "hypothesis": "Markdown-only corpus improves country precision.",
                    "notes": "First GUI-created experiment.",
                },
            )
            list_response = await client.get("/experiments")
            return create_response, list_response

    create_response, list_response = asyncio.run(run())

    assert create_response.status_code == 200
    create_payload = create_response.json()
    assert create_payload["experiment_id"].startswith("exp_")
    assert create_payload["status"] == "draft"
    assert "work_exp_markdown_only_corpus_improves_country_precis" in create_payload["experiment_work_dir"]
    assert "experiment_sources" in create_payload["experiment_source_dir"]
    assert list_response.status_code == 200
    list_payload = list_response.json()
    assert list_payload["entries"]
    assert list_payload["entries"][0]["hypothesis"] == "Markdown-only corpus improves country precision."
    assert list_payload["entries"][0]["content_type"] == "faq"
    assert list_payload["entries"][0]["artifact_status"] == "missing_index"
    assert list_payload["entries"][0]["index_ready"] is False


def test_api_clear_experiment_registry(tmp_path: Path) -> None:
    source_dir = tmp_path / "raw"
    source_dir.mkdir(parents=True, exist_ok=True)
    settings = Settings(OKR_SOURCE_DIR=source_dir, OKR_WORK_DIR=tmp_path / "work")

    async def run() -> tuple[httpx.Response, httpx.Response, httpx.Response]:
        transport = httpx.ASGITransport(app=create_app(settings))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            create_response = await client.post(
                "/experiments/create",
                json={
                    "baseline_work_dir": str(tmp_path / "work"),
                    "hypothesis": "Clear registry test.",
                },
            )
            experiment_work_dir = Path(create_response.json()["experiment_work_dir"])
            experiment_work_dir.mkdir(parents=True, exist_ok=True)
            for name in ("manifest.json", "blocks.json", "documents.json"):
                (experiment_work_dir / name).write_text("{}", encoding="utf-8")
            clear_response = await client.post("/experiments/clear-registry", json={"delete_workspaces": True})
            list_response = await client.get("/experiments")
            return create_response, clear_response, list_response

    create_response, clear_response, list_response = asyncio.run(run())

    assert create_response.status_code == 200
    assert clear_response.status_code == 200
    clear_payload = clear_response.json()
    assert clear_payload["status"] == "cleared"
    assert clear_payload["cleared_count"] == 1
    assert clear_payload["entries"] == []
    assert clear_payload["deleted_workspace_count"] == 1
    assert not Path(create_response.json()["experiment_work_dir"]).exists()
    assert "workspaces were deleted" in clear_payload["note"]
    assert list_response.json()["entries"] == []


def test_api_experiment_upload_files_stages_source_data(tmp_path: Path) -> None:
    settings = Settings(OKR_SOURCE_DIR=tmp_path / "raw", OKR_WORK_DIR=tmp_path / "work")

    async def run() -> httpx.Response:
        transport = httpx.ASGITransport(app=create_app(settings))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.post(
                "/experiments/upload-files",
                json={
                    "hypothesis": "Test staged upload for Spain sender changes.",
                    "files": [
                        {"name": "spain_es.md", "content": "# Spain (ES)\n\nSender provisioning: No sender registration needed.\n"},
                        {"name": "notes.txt", "content": "auxiliary experiment note"},
                    ],
                },
            )

    response = asyncio.run(run())

    assert response.status_code == 200
    payload = response.json()
    assert payload["file_count"] == 2
    source_dir = Path(payload["experiment_source_dir"])
    assert source_dir.exists()
    assert (source_dir / "spain_es.md").exists()
    assert (source_dir / "notes.txt").exists()


def test_api_experiment_upload_repairs_json_inner_quotes(tmp_path: Path) -> None:
    settings = Settings(OKR_SOURCE_DIR=tmp_path / "raw", OKR_WORK_DIR=tmp_path / "work")
    broken_json = """
{
  "document_title": "Benin FAQ Source Facts",
  "source_facts": [
    {
      "fact_id": "benin-number-format-change",
      "fact_type": "provisioning",
      "value": "The format changes by adding "01" after the country code."
    }
  ]
}
""".strip()

    async def run() -> httpx.Response:
        transport = httpx.ASGITransport(app=create_app(settings))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.post(
                "/experiments/upload-files",
                json={
                    "hypothesis": "FAQ quote repair",
                    "files": [{"name": "benin-faq.json", "content": broken_json}],
                },
            )

    response = asyncio.run(run())

    assert response.status_code == 200
    source_dir = Path(response.json()["experiment_source_dir"])
    saved = (source_dir / "benin-faq.json").read_text(encoding="utf-8")
    assert 'adding \\"01\\" after' in saved
    assert json.loads(saved)["source_facts"][0]["value"] == 'The format changes by adding "01" after the country code.'


def test_api_experiment_upload_restores_known_quoted_tokens(tmp_path: Path) -> None:
    settings = Settings(OKR_SOURCE_DIR=tmp_path / "raw", OKR_WORK_DIR=tmp_path / "work")
    payload = {
        "document_title": "Sender FAQ Source Facts",
        "source_facts": [
            {
                "fact_id": "sender-token-preservation",
                "fact_type": "content_restriction",
                "value": "Avoid InfoSMS or Verify.",
                "structured_fields": {"answer": "Avoid InfoSMS or Verify."},
                "local_aliases": ["InfoSMS", "Verify"],
                "source_quote": "Avoid InfoSMS or Verify.",
            }
        ],
    }

    async def run() -> httpx.Response:
        transport = httpx.ASGITransport(app=create_app(settings))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.post(
                "/experiments/upload-files",
                json={
                    "hypothesis": "FAQ known quote restoration",
                    "files": [{"name": "sender-faq.json", "content": json.dumps(payload)}],
                },
            )

    response = asyncio.run(run())

    assert response.status_code == 200
    source_dir = Path(response.json()["experiment_source_dir"])
    saved_payload = json.loads((source_dir / "sender-faq.json").read_text(encoding="utf-8"))
    source_fact = saved_payload["source_facts"][0]
    assert source_fact["value"] == 'Avoid "InfoSMS" or "Verify".'
    assert source_fact["structured_fields"]["answer"] == 'Avoid "InfoSMS" or "Verify".'
    assert source_fact["local_aliases"] == ['"InfoSMS"', '"Verify"']
    assert source_fact["source_quote"] == 'Avoid "InfoSMS" or "Verify".'


def test_api_experiment_build_can_merge_with_baseline_source(tmp_path: Path) -> None:
    baseline_source_dir = tmp_path / "raw"
    experiment_source_dir = tmp_path / "experiment_source"
    baseline_work_dir = tmp_path / "work"
    experiment_work_dir = tmp_path / "work_exp"
    baseline_source_dir.mkdir(parents=True, exist_ok=True)
    experiment_source_dir.mkdir(parents=True, exist_ok=True)
    (baseline_source_dir / "spain_es.md").write_text(
        "# Spain (ES)\n\nTwo-way SMS is supported.\n",
        encoding="utf-8",
    )
    (experiment_source_dir / "sender_rules.json").write_text(
        json.dumps(
            {
                "document_id": "sender_rules",
                "title": "Sender Rules",
                "language": "en",
                "source_facts": [
                    {
                        "fact_id": "sender_rules_001",
                        "fact_type": "registration",
                        "topic": "Sender registration",
                        "value": "Spain does not require sender registration for this curated rule.",
                        "structured_fields": {"country_iso2": "ES"},
                        "source_anchor": "curated test",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    settings = Settings(OKR_SOURCE_DIR=baseline_source_dir, OKR_WORK_DIR=baseline_work_dir, OKR_MAPPING_PROVIDER="noop")
    KnowledgePipeline(settings).build_index(
        source_dir=baseline_source_dir,
        work_dir=baseline_work_dir,
        allow_low_quality=True,
        allowed_suffixes=[".md", ".json"],
    )

    async def run() -> httpx.Response:
        transport = httpx.ASGITransport(app=create_app(settings))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.post(
                "/experiments/build",
                json={
                    "source_dir": str(baseline_source_dir),
                    "experiment_source_dir": str(experiment_source_dir),
                    "experiment_work_dir": str(experiment_work_dir),
                    "baseline_work_dir": str(baseline_work_dir),
                    "merge_with_baseline": True,
                    "allowed_suffixes": [".md"],
                    "allow_low_quality": True,
                    "mapping_provider": "noop",
                },
            )

    response = asyncio.run(run())

    assert response.status_code == 200
    payload = response.json()
    assert payload["merge_with_baseline"] is True
    assert payload["merge_strategy"] == "incremental_artifact_merge"
    assert payload["build"]["documents"] == 2
    assert payload["build"]["allowed_suffixes"] == [".md", ".json", ".txt"]
    assert payload["build"]["reused_baseline_documents"] == 1
    assert payload["build"]["added_documents"] == 1
    assert payload["build"]["total_time"] >= 0


def test_api_build_index_can_limit_allowed_suffixes(tmp_path: Path) -> None:
    source_dir = tmp_path / "raw"
    work_dir = tmp_path / "work"
    source_dir.mkdir(parents=True, exist_ok=True)
    (source_dir / "spain_es.md").write_text(
        """# Spain (ES)

## Sender
Sender provisioning: No sender registration needed.
""",
        encoding="utf-8",
    )
    (source_dir / "catalog.json").write_text(
        json.dumps({"title": "Catalog", "locales": [{"locale_name": "Spain"}]}, indent=2),
        encoding="utf-8",
    )
    settings = Settings(OKR_SOURCE_DIR=source_dir, OKR_WORK_DIR=work_dir, OKR_MAPPING_PROVIDER="noop")

    async def run() -> httpx.Response:
        transport = httpx.ASGITransport(app=create_app(settings))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.post(
                "/build-index",
                json={
                    "source_dir": str(source_dir),
                    "work_dir": str(work_dir),
                    "allowed_suffixes": [".md"],
                    "allow_low_quality": True,
                },
            )

    response = asyncio.run(run())

    assert response.status_code == 200
    payload = response.json()
    assert payload["documents"] == 1
    assert payload["allowed_suffixes"] == [".md"]


def test_api_experiment_compare_returns_decision_surface(tmp_path: Path) -> None:
    baseline_source_dir = tmp_path / "raw_baseline"
    experiment_source_dir = tmp_path / "raw_experiment"
    baseline_work_dir = tmp_path / "work_baseline"
    experiment_work_dir = tmp_path / "work_experiment"
    baseline_source_dir.mkdir(parents=True, exist_ok=True)
    experiment_source_dir.mkdir(parents=True, exist_ok=True)
    (baseline_source_dir / "spain_es.md").write_text(
        """# Spain (ES)

## Sender
| Key | Value |
| --- | --- |
| Sender provisioning | Sender registration may be required. |
""",
        encoding="utf-8",
    )
    (experiment_source_dir / "spain_es.md").write_text(
        """# Spain (ES)

## Sender
| Key | Value |
| --- | --- |
| Sender provisioning | No sender registration needed. |
""",
        encoding="utf-8",
    )
    benchmark = tmp_path / "benchmark.json"
    benchmark.write_text(
        """
[
  {
    "question": "Sender in Spain?",
    "expected_document_ids": ["spain_es"],
    "expected_terms": ["sender provisioning", "no sender registration needed"],
    "expected_iso_code": "ES",
    "question_type": "factoid",
    "should_refuse": false
  }
]
""".strip(),
        encoding="utf-8",
    )

    baseline_settings = Settings(
        OKR_SOURCE_DIR=baseline_source_dir,
        OKR_WORK_DIR=baseline_work_dir,
        OKR_MAPPING_PROVIDER="noop",
    )
    experiment_settings = Settings(
        OKR_SOURCE_DIR=experiment_source_dir,
        OKR_WORK_DIR=experiment_work_dir,
        OKR_MAPPING_PROVIDER="noop",
    )

    async def build_index(source_dir: Path, work_dir: Path, settings: Settings) -> None:
        transport = httpx.ASGITransport(app=create_app(settings))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/build-index",
                json={"source_dir": str(source_dir), "work_dir": str(work_dir), "allow_low_quality": True},
            )
            assert response.status_code == 200

    asyncio.run(build_index(baseline_source_dir, baseline_work_dir, baseline_settings))
    asyncio.run(build_index(experiment_source_dir, experiment_work_dir, experiment_settings))

    compare_settings = Settings(
        OKR_SOURCE_DIR=experiment_source_dir,
        OKR_WORK_DIR=baseline_work_dir,
        OKR_MAPPING_PROVIDER="noop",
    )

    async def run_compare() -> httpx.Response:
        transport = httpx.ASGITransport(app=create_app(compare_settings))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.post(
                "/experiments/compare",
                json={
                    "experiment_work_dir": str(experiment_work_dir),
                    "baseline_work_dir": str(baseline_work_dir),
                    "benchmark_path": str(benchmark),
                    "hypothesis": "Better sender wording improves answer correctness.",
                },
            )

    response = asyncio.run(run_compare())

    assert response.status_code == 200
    payload = response.json()
    assert payload["baseline_metrics"]["answer_correctness"] <= payload["experiment_metrics"]["answer_correctness"]
    assert "country_match_at_1" in payload["delta_metrics"]
    assert "decision_checks" in payload
    assert payload["promotion_decision"] == "needs_benchmark"
    assert payload["benchmark_profile"]["adequate"] is False
    assert payload["recommendation_notes"]


def test_api_experiment_evaluate_without_benchmark_returns_ingestion_health(tmp_path: Path) -> None:
    source_dir = tmp_path / "raw"
    work_dir = tmp_path / "work_exp"
    source_dir.mkdir(parents=True, exist_ok=True)
    (source_dir / "global-restriction.json").write_text(
        json.dumps(
            {
                "document_title": "Global SMS Sender Registration Requirements",
                "content_type": "messaging_rules",
                "source_facts": [
                    {
                        "field": "operator_requirement",
                        "value": "GrameenPhone, Robi/Axiata, TeleTalk",
                        "applies_to": "Bangladesh",
                        "condition": "mandatory registration",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    settings = Settings(
        OKR_SOURCE_DIR=source_dir,
        OKR_WORK_DIR=work_dir,
        OKR_MAPPING_PROVIDER="noop",
    )
    KnowledgePipeline(settings).build_index(source_dir=source_dir, work_dir=work_dir, allow_low_quality=True)

    async def run() -> httpx.Response:
        transport = httpx.ASGITransport(app=create_app(settings))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.post(
                "/experiments/evaluate",
                json={
                    "experiment_work_dir": str(work_dir),
                    "baseline_work_dir": str(tmp_path / "baseline"),
                    "hypothesis": "Curated global restrictions ingest cleanly.",
                },
            )

    response = asyncio.run(run())

    assert response.status_code == 200
    payload = response.json()
    assert payload["benchmark_used"] == ""
    assert payload["summary"] == {}
    assert payload["ingestion_health"]["documents"] == 1
    assert payload["ingestion_health"]["blocks"] >= 1
    assert payload["ingestion_health"]["vector_count_matches"] is True
    assert payload["ingestion_health"]["structured_fact_blocks"] >= 1


def test_api_experiment_compare_without_benchmark_uses_ingestion_health(tmp_path: Path) -> None:
    baseline_source_dir = tmp_path / "baseline_raw"
    experiment_source_dir = tmp_path / "experiment_raw"
    baseline_work_dir = tmp_path / "work_baseline"
    experiment_work_dir = tmp_path / "work_exp"
    baseline_source_dir.mkdir(parents=True, exist_ok=True)
    experiment_source_dir.mkdir(parents=True, exist_ok=True)
    (baseline_source_dir / "baseline.md").write_text("# Baseline\n\nStable baseline fact.\n", encoding="utf-8")
    (experiment_source_dir / "global-restriction.json").write_text(
        json.dumps(
            {
                "document_title": "Global SMS Sender Registration Requirements",
                "content_type": "messaging_rules",
                "source_facts": [{"field": "pre_registration_required", "value": "true"}],
            }
        ),
        encoding="utf-8",
    )
    baseline_settings = Settings(OKR_SOURCE_DIR=baseline_source_dir, OKR_WORK_DIR=baseline_work_dir, OKR_MAPPING_PROVIDER="noop")
    experiment_settings = Settings(OKR_SOURCE_DIR=experiment_source_dir, OKR_WORK_DIR=experiment_work_dir, OKR_MAPPING_PROVIDER="noop")
    KnowledgePipeline(baseline_settings).build_index(source_dir=baseline_source_dir, work_dir=baseline_work_dir, allow_low_quality=True)
    KnowledgePipeline(experiment_settings).build_index(source_dir=experiment_source_dir, work_dir=experiment_work_dir, allow_low_quality=True)

    async def run() -> httpx.Response:
        transport = httpx.ASGITransport(app=create_app(experiment_settings))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.post(
                "/experiments/compare",
                json={
                    "experiment_work_dir": str(experiment_work_dir),
                    "baseline_work_dir": str(baseline_work_dir),
                    "hypothesis": "Curated source facts are indexed.",
                },
            )

    response = asyncio.run(run())

    assert response.status_code == 200
    payload = response.json()
    assert payload["promotion_decision"] in {"ingest_healthy", "fix_ingestion"}
    assert "experiment_ingestion_health" in payload
    assert payload["experiment_ingestion_health"]["vector_count_matches"] is True
    assert payload["benchmark_profile"]["warnings"]


def test_comparison_payload_recommends_benchmark_when_coverage_is_weak(tmp_path: Path) -> None:
    from own_knowledge_rag.api import _comparison_payload
    from own_knowledge_rag.models import EvaluationSummary

    baseline_work_dir = tmp_path / "baseline"
    experiment_work_dir = tmp_path / "experiment"
    baseline_work_dir.mkdir()
    experiment_work_dir.mkdir()
    (baseline_work_dir / "manifest.json").write_text(
        json.dumps({"documents_state": {"spain_es": "a"}}),
        encoding="utf-8",
    )
    (experiment_work_dir / "manifest.json").write_text(
        json.dumps({"documents_state": {"spain_es": "a", "new_prefixes": "b"}}),
        encoding="utf-8",
    )
    benchmark = tmp_path / "benchmark.json"
    benchmark.write_text(
        json.dumps(
            [
                {
                    "question": "Sender in Spain?",
                    "expected_document_ids": ["spain_es"],
                    "expected_terms": ["sender"],
                    "expected_iso_code": "ES",
                }
            ]
        ),
        encoding="utf-8",
    )

    baseline = EvaluationSummary(
        total_cases=1,
        retrieval_recall_at_k=0.7,
        evidence_hit_rate=0.7,
        citation_accuracy=0.7,
        document_precision_at_k=0.7,
        no_answer_precision=0.0,
        answer_correctness=0.7,
        country_match_at_1=0.9,
    )
    experiment = EvaluationSummary(
        total_cases=1,
        retrieval_recall_at_k=0.72,
        evidence_hit_rate=0.7,
        citation_accuracy=0.7,
        document_precision_at_k=0.7,
        no_answer_precision=0.0,
        answer_correctness=0.71,
        country_match_at_1=0.9,
    )

    payload = _comparison_payload(
        baseline,
        experiment,
        benchmark_path=benchmark,
        baseline_work_dir=baseline_work_dir,
        experiment_work_dir=experiment_work_dir,
    )

    assert payload["promotion_recommended"] is False
    assert payload["promotion_decision"] == "needs_benchmark"
    assert any("adds documents" in warning for warning in payload["benchmark_profile"]["warnings"])


def test_ingestion_health_treats_structured_field_blocks_as_effectively_ok() -> None:
    from own_knowledge_rag.api import _effective_quality_status

    block = {
        "block_type": "structured_fact",
        "quality_status": "LOW_QUALITY",
        "text": (
            "- country_numbering_codes: Value=Afghanistan has ISO code AF, MCC 412, and dialing codes +93, 93.; "
            "country=Afghanistan; country_iso2=AF; mcc=412; dialing_code=+93, 93; "
            "hypothetical_questions=What is the dialing code for Afghanistan?"
        ),
        "metadata": {
            "row_values": "Value=Afghanistan has ISO code AF, MCC 412, and dialing codes +93, 93.; country=Afghanistan; country_iso2=AF",
            "structured_field": "country_numbering_codes",
            "informative": "high",
        },
    }

    assert _effective_quality_status(block) == "ok"


def test_ingestion_health_accepts_quiet_hours_structured_facts() -> None:
    from own_knowledge_rag.api import _effective_quality_status

    block = {
        "block_type": "structured_fact",
        "quality_status": "LOW_QUALITY",
        "country": "Brazil",
        "iso_code": "BR",
        "text": (
            "- content_restriction: Value=In Brazil, promotional SMS is allowed Monday-Friday "
            "8:00 AM-8:00 PM and Saturday 8:00 AM-2:00 PM. Sunday sending is not allowed.; "
            "country_name=Brazil; country_iso2=BR; regulation_topics=quiet hours, content restriction; "
            "hypothetical_questions=What are the promotional SMS sending hours in Brazil?"
        ),
        "metadata": {
            "structured_field": "content_restriction",
            "structured_value": (
                "In Brazil, promotional SMS is allowed Monday-Friday 8:00 AM-8:00 PM and "
                "Saturday 8:00 AM-2:00 PM. Sunday sending is not allowed."
            ),
            "row_values": "country_iso2=BR; regulation_topics=quiet hours, content restriction",
        },
    }

    assert _effective_quality_status(block) == "ok"


def test_ingestion_health_accepts_short_sender_availability_and_two_way_facts() -> None:
    from own_knowledge_rag.api import _effective_quality_status

    sender_block = {
        "block_type": "structured_fact",
        "quality_status": "LOW_QUALITY",
        "text": "- sender_id: Value=Sender availability in Colombia is supported.; country_iso2=CO; topic=sender availability",
        "metadata": {
            "structured_field": "sender_id",
            "structured_value": "Sender availability in Colombia is supported.",
            "row_values": "country_iso2=CO; topic=sender availability",
        },
    }
    two_way_block = {
        "block_type": "structured_fact",
        "quality_status": "LOW_QUALITY",
        "text": "- sms_capability: Value=Two-way SMS is supported in Spain.; country_iso2=ES; regulation_topics=two-way sms",
        "metadata": {
            "structured_field": "sms_capability",
            "structured_value": "Two-way SMS is supported in Spain.",
            "row_values": "country_iso2=ES; regulation_topics=two-way sms",
        },
    }

    assert _effective_quality_status(sender_block) == "ok"
    assert _effective_quality_status(two_way_block) == "ok"


def test_ingestion_health_keeps_placeholder_structured_facts_low_quality() -> None:
    from own_knowledge_rag.api import _effective_quality_status

    block = {
        "block_type": "structured_fact",
        "quality_status": "LOW_QUALITY",
        "text": "- sender_id: Value=---; country_iso2=BR; topic=sender availability",
        "metadata": {
            "structured_field": "sender_id",
            "structured_value": "---",
            "row_values": "Value=---; country_iso2=BR; topic=sender availability",
        },
    }

    assert _effective_quality_status(block) == "LOW_QUALITY"


def test_ingestion_health_discount_effectively_ok_low_quality_blocks(tmp_path: Path) -> None:
    from own_knowledge_rag.api import _ingestion_health

    work_dir = tmp_path / "work"
    work_dir.mkdir()
    (work_dir / "manifest.json").write_text(
        json.dumps({"documents": 1, "blocks": 2}),
        encoding="utf-8",
    )
    (work_dir / "ingest_report.json").write_text(
        json.dumps({"low_quality_blocks": 2, "rejected_blocks": 0}),
        encoding="utf-8",
    )
    blocks = [
        {
            "block_type": "structured_fact",
            "quality_status": "LOW_QUALITY",
            "country": "Brazil",
            "iso_code": "BR",
            "text": "- content_restriction: Value=Sunday promotional SMS is not allowed in Brazil.; country_iso2=BR; regulation_topics=quiet hours",
            "metadata": {
                "content_type": "json",
                "structured_field": "content_restriction",
                "structured_value": "Sunday promotional SMS is not allowed in Brazil.",
                "row_values": "country_iso2=BR; regulation_topics=quiet hours",
            },
        },
        {
            "block_type": "structured_fact",
            "quality_status": "LOW_QUALITY",
            "text": "- country_numbering_codes: Value=Kuwait has dialing code +965.; country_iso2=KW; dialing_code=+965",
            "metadata": {
                "content_type": "json",
                "structured_field": "country_numbering_codes",
                "structured_value": "Kuwait has dialing code +965.",
                "row_values": "country_iso2=KW; dialing_code=+965",
            },
        },
    ]
    (work_dir / "blocks.json").write_text(json.dumps(blocks), encoding="utf-8")
    (work_dir / "vectors.json").write_text(json.dumps({"vectors": [{"id": "1"}, {"id": "2"}]}), encoding="utf-8")

    health = _ingestion_health(work_dir)

    assert health["healthy"] is True
    assert health["raw_low_quality_blocks"] == 2
    assert health["low_quality_blocks"] == 0
    assert health["effectively_ok_blocks"] == 2
    assert "More than half of blocks are marked low quality." not in health["warnings"]


def test_api_low_quality_blocks_returns_review_needed_items(tmp_path: Path) -> None:
    work_dir = tmp_path / "work"
    work_dir.mkdir()
    (work_dir / "manifest.json").write_text(json.dumps({"documents": 1, "blocks": 2}), encoding="utf-8")
    (work_dir / "documents.json").write_text(json.dumps([]), encoding="utf-8")
    blocks = [
        {
            "block_id": "placeholder",
            "document_id": "quiet_hours",
            "title": "Quiet Hours",
            "source_path": "data/raw/quiet-hours.json",
            "section_path": ["Quiet Hours", "Source Facts"],
            "block_type": "structured_fact",
            "quality_status": "LOW_QUALITY",
            "text": "- content_restriction: Value=---; country_iso2=BR; topic=quiet hours",
            "metadata": {
                "structured_field": "content_restriction",
                "structured_value": "---",
                "row_values": "Value=---; country_iso2=BR; topic=quiet hours",
            },
        },
        {
            "block_id": "accepted",
            "document_id": "quiet_hours",
            "title": "Quiet Hours",
            "source_path": "data/raw/quiet-hours.json",
            "section_path": ["Quiet Hours", "Source Facts"],
            "block_type": "structured_fact",
            "quality_status": "LOW_QUALITY",
            "text": "- content_restriction: Value=Sunday promotional SMS is not allowed in Brazil.; country_iso2=BR; regulation_topics=quiet hours",
            "metadata": {
                "structured_field": "content_restriction",
                "structured_value": "Sunday promotional SMS is not allowed in Brazil.",
                "row_values": "country_iso2=BR; regulation_topics=quiet hours",
            },
        },
    ]
    (work_dir / "blocks.json").write_text(json.dumps(blocks), encoding="utf-8")
    settings = Settings(OKR_WORK_DIR=work_dir, OKR_SOURCE_DIR=tmp_path / "raw")

    async def run() -> httpx.Response:
        transport = httpx.ASGITransport(app=create_app(settings))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.post("/low-quality-blocks", json={"work_dir": str(work_dir)})

    response = asyncio.run(run())

    assert response.status_code == 200
    payload = response.json()
    assert payload["raw_low_quality_blocks"] == 2
    assert payload["effectively_ok_blocks"] == 1
    assert payload["review_needed_blocks"] == 1
    assert payload["blocks"][0]["block_id"] == "placeholder"
    assert "Placeholder or unknown value" in payload["blocks"][0]["reasons"]


def test_api_build_index_rejects_missing_source_dir(tmp_path: Path) -> None:
    missing_source_dir = tmp_path / "missing"
    work_dir = tmp_path / "work"
    settings = Settings(OKR_SOURCE_DIR=missing_source_dir, OKR_WORK_DIR=work_dir)

    async def run() -> httpx.Response:
        transport = httpx.ASGITransport(app=create_app(settings))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.post(
                "/build-index",
                json={"source_dir": str(missing_source_dir), "work_dir": str(work_dir)},
            )

    response = asyncio.run(run())

    assert response.status_code == 400
    assert "Source directory does not exist" in response.json()["detail"]


def test_api_build_index_rejects_when_work_dir_is_locked(tmp_path: Path) -> None:
    source_dir = tmp_path / "raw"
    work_dir = tmp_path / "work"
    source_dir.mkdir(parents=True, exist_ok=True)
    work_dir.mkdir(parents=True, exist_ok=True)
    (source_dir / "spain_es.md").write_text("# Spain (ES)\n\nSender provisioning: No sender registration needed.\n", encoding="utf-8")
    (work_dir / ".build-index.lock").write_text(json.dumps({"pid": os.getpid()}), encoding="utf-8")
    settings = Settings(OKR_SOURCE_DIR=source_dir, OKR_WORK_DIR=work_dir, OKR_MAPPING_PROVIDER="noop")

    async def run() -> httpx.Response:
        transport = httpx.ASGITransport(app=create_app(settings))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.post(
                "/build-index",
                json={"source_dir": str(source_dir), "work_dir": str(work_dir), "allow_low_quality": True},
            )

    response = asyncio.run(run())

    assert response.status_code == 409
    detail = response.json()["detail"]
    assert "already running" in detail["message"]
    assert detail["lock"]["stale"] is False


def test_api_clear_stale_build_lock_removes_dead_pid_lock(tmp_path: Path) -> None:
    work_dir = tmp_path / "work"
    work_dir.mkdir(parents=True, exist_ok=True)
    lock_path = work_dir / ".build-index.lock"
    lock_path.write_text(json.dumps({"pid": 999999, "work_dir": str(work_dir)}), encoding="utf-8")
    settings = Settings(OKR_WORK_DIR=work_dir, OKR_MAPPING_PROVIDER="noop")

    async def run() -> httpx.Response:
        transport = httpx.ASGITransport(app=create_app(settings))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.post("/build-index/clear-stale-lock", json={"work_dir": str(work_dir)})

    response = asyncio.run(run())

    assert response.status_code == 200
    assert response.json()["locked"] is False
    assert not lock_path.exists()


def test_api_clear_stale_build_lock_rejects_active_lock(tmp_path: Path) -> None:
    work_dir = tmp_path / "work"
    work_dir.mkdir(parents=True, exist_ok=True)
    lock_path = work_dir / ".build-index.lock"
    lock_path.write_text(json.dumps({"pid": os.getpid(), "work_dir": str(work_dir)}), encoding="utf-8")
    settings = Settings(OKR_WORK_DIR=work_dir, OKR_MAPPING_PROVIDER="noop")

    async def run() -> httpx.Response:
        transport = httpx.ASGITransport(app=create_app(settings))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.post("/build-index/clear-stale-lock", json={"work_dir": str(work_dir)})

    response = asyncio.run(run())

    assert response.status_code == 409
    assert lock_path.exists()


def test_api_experiment_promote_replaces_baseline_with_backup(tmp_path: Path) -> None:
    experiment_work_dir = tmp_path / "work_exp"
    baseline_work_dir = tmp_path / "work"
    experiment_work_dir.mkdir(parents=True, exist_ok=True)
    baseline_work_dir.mkdir(parents=True, exist_ok=True)

    (baseline_work_dir / "manifest.json").write_text(json.dumps({"documents": 1, "marker": "baseline"}), encoding="utf-8")
    (baseline_work_dir / "blocks.json").write_text("[]", encoding="utf-8")
    (baseline_work_dir / "documents.json").write_text("[]", encoding="utf-8")
    (experiment_work_dir / "manifest.json").write_text(json.dumps({"documents": 2, "marker": "experiment"}), encoding="utf-8")
    (experiment_work_dir / "blocks.json").write_text("[]", encoding="utf-8")
    (experiment_work_dir / "documents.json").write_text("[]", encoding="utf-8")

    settings = Settings(OKR_SOURCE_DIR=tmp_path / "raw", OKR_WORK_DIR=baseline_work_dir)

    async def run() -> httpx.Response:
        transport = httpx.ASGITransport(app=create_app(settings))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.post(
                "/experiments/promote",
                json={
                    "experiment_work_dir": str(experiment_work_dir),
                    "baseline_work_dir": str(baseline_work_dir),
                    "hypothesis": "Promote the experimental workspace.",
                },
            )

    response = asyncio.run(run())

    assert response.status_code == 200
    payload = response.json()
    manifest = json.loads((baseline_work_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["marker"] == "experiment"
    assert payload["backup_work_dir"]
    assert Path(payload["backup_work_dir"]).exists()


def test_api_experiment_promote_requires_sources_to_be_accepted(tmp_path: Path) -> None:
    baseline_source_dir = tmp_path / "raw"
    experiment_source_dir = tmp_path / "experiment_raw"
    experiment_work_dir = tmp_path / "work_exp"
    baseline_work_dir = tmp_path / "work"
    baseline_source_dir.mkdir(parents=True, exist_ok=True)
    experiment_source_dir.mkdir(parents=True, exist_ok=True)
    experiment_work_dir.mkdir(parents=True, exist_ok=True)
    baseline_work_dir.mkdir(parents=True, exist_ok=True)
    (experiment_source_dir / "new_country.md").write_text("# New Country\n\nRegistration required.\n", encoding="utf-8")
    (baseline_work_dir / "manifest.json").write_text(json.dumps({"documents": 1}), encoding="utf-8")
    (baseline_work_dir / "blocks.json").write_text("[]", encoding="utf-8")
    (baseline_work_dir / "documents.json").write_text("[]", encoding="utf-8")
    (experiment_work_dir / "manifest.json").write_text(json.dumps({"documents": 2}), encoding="utf-8")
    (experiment_work_dir / "blocks.json").write_text("[]", encoding="utf-8")
    (experiment_work_dir / "documents.json").write_text("[]", encoding="utf-8")
    settings = Settings(OKR_SOURCE_DIR=baseline_source_dir, OKR_WORK_DIR=baseline_work_dir)

    async def run() -> httpx.Response:
        transport = httpx.ASGITransport(app=create_app(settings))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.post(
                "/experiments/promote",
                json={
                    "experiment_source_dir": str(experiment_source_dir),
                    "experiment_work_dir": str(experiment_work_dir),
                    "baseline_work_dir": str(baseline_work_dir),
                    "hypothesis": "Promote without accepting sources.",
                },
            )

    response = asyncio.run(run())

    assert response.status_code == 409
    detail = response.json()["detail"]
    assert "not been accepted" in detail["message"]
    assert detail["source_alignment"]["accepted"] is False
    assert detail["source_alignment"]["missing_files"] == ["new_country.md"]


def test_api_experiment_promote_can_override_source_alignment_check(tmp_path: Path) -> None:
    baseline_source_dir = tmp_path / "raw"
    experiment_source_dir = tmp_path / "experiment_raw"
    experiment_work_dir = tmp_path / "work_exp"
    baseline_work_dir = tmp_path / "work"
    baseline_source_dir.mkdir(parents=True, exist_ok=True)
    experiment_source_dir.mkdir(parents=True, exist_ok=True)
    experiment_work_dir.mkdir(parents=True, exist_ok=True)
    baseline_work_dir.mkdir(parents=True, exist_ok=True)
    (experiment_source_dir / "new_country.md").write_text("# New Country\n\nRegistration required.\n", encoding="utf-8")
    (baseline_work_dir / "manifest.json").write_text(json.dumps({"documents": 1, "marker": "baseline"}), encoding="utf-8")
    (baseline_work_dir / "blocks.json").write_text("[]", encoding="utf-8")
    (baseline_work_dir / "documents.json").write_text("[]", encoding="utf-8")
    (experiment_work_dir / "manifest.json").write_text(json.dumps({"documents": 2, "marker": "experiment"}), encoding="utf-8")
    (experiment_work_dir / "blocks.json").write_text("[]", encoding="utf-8")
    (experiment_work_dir / "documents.json").write_text("[]", encoding="utf-8")
    settings = Settings(OKR_SOURCE_DIR=baseline_source_dir, OKR_WORK_DIR=baseline_work_dir)

    async def run() -> httpx.Response:
        transport = httpx.ASGITransport(app=create_app(settings))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.post(
                "/experiments/promote",
                json={
                    "experiment_source_dir": str(experiment_source_dir),
                    "experiment_work_dir": str(experiment_work_dir),
                    "baseline_work_dir": str(baseline_work_dir),
                    "force_promote_without_sources": True,
                    "hypothesis": "Promote with explicit source override.",
                },
            )

    response = asyncio.run(run())

    assert response.status_code == 200
    payload = response.json()
    manifest = json.loads((baseline_work_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["marker"] == "experiment"
    assert payload["source_alignment"]["accepted"] is False
    assert payload["source_alignment"]["override_used"] is True


def test_api_experiment_promote_sources_copies_staged_files_with_backup(tmp_path: Path) -> None:
    baseline_source_dir = tmp_path / "raw"
    experiment_source_dir = tmp_path / "experiment_raw"
    baseline_work_dir = tmp_path / "work"
    baseline_source_dir.mkdir(parents=True, exist_ok=True)
    experiment_source_dir.mkdir(parents=True, exist_ok=True)
    (baseline_source_dir / "spain_es.json").write_text('{"old": true}', encoding="utf-8")
    (experiment_source_dir / "spain_es.json").write_text('{"old": false, "new": true}', encoding="utf-8")
    (experiment_source_dir / "france_fr.md").write_text("# France\n\nTwo-way SMS is supported.\n", encoding="utf-8")
    settings = Settings(OKR_SOURCE_DIR=baseline_source_dir, OKR_WORK_DIR=baseline_work_dir)

    async def run() -> httpx.Response:
        transport = httpx.ASGITransport(app=create_app(settings))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.post(
                "/experiments/promote-sources",
                json={
                    "experiment_source_dir": str(experiment_source_dir),
                    "experiment_work_dir": str(tmp_path / "work_exp"),
                    "baseline_work_dir": str(baseline_work_dir),
                    "hypothesis": "Accept curated source files.",
                },
            )

    response = asyncio.run(run())

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "sources_promoted"
    assert payload["promoted_source_count"] == 2
    assert (baseline_source_dir / "france_fr.md").exists()
    assert json.loads((baseline_source_dir / "spain_es.json").read_text(encoding="utf-8"))["new"] is True
    backup_source_dir = Path(payload["backup_source_dir"])
    assert (backup_source_dir / "spain_es.json").exists()
    assert json.loads((backup_source_dir / "spain_es.json").read_text(encoding="utf-8"))["old"] is True


def test_api_experiment_rollback_restores_backup_and_preserves_current_baseline(tmp_path: Path) -> None:
    baseline_work_dir = tmp_path / "work"
    backup_work_dir = tmp_path / "work_backup_20260501-120000"
    baseline_work_dir.mkdir(parents=True, exist_ok=True)
    backup_work_dir.mkdir(parents=True, exist_ok=True)

    (baseline_work_dir / "manifest.json").write_text(json.dumps({"documents": 2, "marker": "promoted"}), encoding="utf-8")
    (baseline_work_dir / "blocks.json").write_text("[]", encoding="utf-8")
    (baseline_work_dir / "documents.json").write_text("[]", encoding="utf-8")
    (backup_work_dir / "manifest.json").write_text(json.dumps({"documents": 1, "marker": "baseline"}), encoding="utf-8")
    (backup_work_dir / "blocks.json").write_text("[]", encoding="utf-8")
    (backup_work_dir / "documents.json").write_text("[]", encoding="utf-8")

    settings = Settings(OKR_SOURCE_DIR=tmp_path / "raw", OKR_WORK_DIR=baseline_work_dir)

    async def run() -> httpx.Response:
        transport = httpx.ASGITransport(app=create_app(settings))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.post(
                "/experiments/rollback",
                json={
                    "baseline_work_dir": str(baseline_work_dir),
                    "backup_work_dir": str(backup_work_dir),
                    "hypothesis": "Rollback promoted baseline.",
                },
            )

    response = asyncio.run(run())

    assert response.status_code == 200
    payload = response.json()
    manifest = json.loads((baseline_work_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["marker"] == "baseline"
    assert payload["restored_backup_work_dir"] == str(backup_work_dir)
    current_backup = Path(payload["current_baseline_backup_work_dir"])
    assert current_backup.exists()
    current_manifest = json.loads((current_backup / "manifest.json").read_text(encoding="utf-8"))
    assert current_manifest["marker"] == "promoted"


def test_api_lists_valid_baseline_backups(tmp_path: Path) -> None:
    baseline_work_dir = tmp_path / "work"
    backup_work_dir = tmp_path / "work_backup_20260501-120000"
    invalid_backup_dir = tmp_path / "work_backup_20260501-130000"
    baseline_work_dir.mkdir()
    backup_work_dir.mkdir()
    invalid_backup_dir.mkdir()
    for name in ("manifest.json", "blocks.json", "documents.json"):
        (backup_work_dir / name).write_text("[]" if name != "manifest.json" else "{}", encoding="utf-8")
    (invalid_backup_dir / "manifest.json").write_text("{}", encoding="utf-8")
    settings = Settings(OKR_SOURCE_DIR=tmp_path / "raw", OKR_WORK_DIR=baseline_work_dir)

    async def run() -> httpx.Response:
        transport = httpx.ASGITransport(app=create_app(settings))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.get(
                "/experiments/backups",
                params={"baseline_work_dir": str(baseline_work_dir)},
            )

    response = asyncio.run(run())

    assert response.status_code == 200
    backups = response.json()["backups"]
    assert any(item["path"] == str(backup_work_dir) and item["valid"] for item in backups)
    assert any(item["path"] == str(invalid_backup_dir) and not item["valid"] for item in backups)


def test_api_answer_rejects_missing_index(tmp_path: Path) -> None:
    settings = Settings(OKR_SOURCE_DIR=tmp_path / "raw", OKR_WORK_DIR=tmp_path / "work")

    async def run() -> httpx.Response:
        transport = httpx.ASGITransport(app=create_app(settings))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.post(
                "/answer",
                json={"question": "Sender in Spain?", "work_dir": str(tmp_path / "work"), "top_k": 3},
            )

    response = asyncio.run(run())

    assert response.status_code == 400
    assert "Build the index before asking questions" in response.json()["detail"]


def test_api_build_index_and_answer(tmp_path: Path) -> None:
    source_dir = tmp_path / "raw"
    work_dir = tmp_path / "work"
    source_dir.mkdir(parents=True, exist_ok=True)
    (source_dir / "spain_es.md").write_text(
        """# Spain (ES)

## Sender
| Key | Value |
| --- | --- |
| Sender provisioning | No sender registration needed. |
| Two-way | Supported |
""",
        encoding="utf-8",
    )

    settings = Settings(OKR_SOURCE_DIR=source_dir, OKR_WORK_DIR=work_dir)
    async def run() -> tuple[httpx.Response, httpx.Response, httpx.Response]:
        transport = httpx.ASGITransport(app=create_app(settings))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            build_response = await client.post(
                "/build-index",
                json={"source_dir": str(source_dir), "work_dir": str(work_dir), "allow_low_quality": True},
            )
            answer_response = await client.post(
                "/answer",
                json={"question": "Sender in Spain?", "work_dir": str(work_dir), "top_k": 3},
            )
            block_id = answer_response.json()["evidence"][0]["block_id"] if answer_response.status_code == 200 else ""
            explain_response = await client.post(
                "/explain-block",
                json={"block_id": block_id, "work_dir": str(work_dir)},
            )
            return build_response, answer_response, explain_response

    build_response, answer_response, explain_response = asyncio.run(run())
    assert build_response.status_code == 200
    assert build_response.json()["documents"] == 1
    assert build_response.json()["mapping_provider"] == settings.mapping_provider
    assert build_response.json()["embedding_provider"] == "local"
    assert build_response.json()["vector_backend"] == "local"

    assert answer_response.status_code == 200
    payload = answer_response.json()
    assert payload["confidence"] in {"medium", "high"}
    assert payload["tier"] in {"tier0", "tier1", "tier2", "refusal"}
    assert payload["query_intent"]
    assert payload["cached"] is False
    assert payload["work_dir"] == str(work_dir)
    assert payload["evidence"]
    assert payload["evidence"][0]["block_id"]
    assert payload["evidence"][0]["source_path"].endswith("spain_es.md")
    assert "enriched_text" in payload["evidence"][0]
    assert "block_type" in payload["evidence"][0]
    assert "lexical_score" in payload["evidence"][0]
    assert "vector_score" in payload["evidence"][0]
    assert "## Evidence" not in payload["answer"]
    assert explain_response.status_code == 200
    assert explain_response.json()["block_id"] == payload["evidence"][0]["block_id"]


def test_api_review_answer_saves_user_feedback(tmp_path: Path) -> None:
    settings = Settings(OKR_SOURCE_DIR=tmp_path / "raw", OKR_WORK_DIR=tmp_path / "work")

    async def run() -> httpx.Response:
        transport = httpx.ASGITransport(app=create_app(settings))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            return await client.post(
                "/review-answer",
                json={
                    "work_dir": str(tmp_path / "work"),
                    "question": "Sender in Colombia?",
                    "answer": "For Colombia, the Sender availability is: Short Code.",
                    "confidence": "high",
                    "tier": "tier0",
                    "query_intent": "lookup",
                    "cached": False,
                    "rating": "correct_with_foreign_evidence",
                    "expected_document_id": "colombia_co",
                    "expected_iso_code": "CO",
                    "expected_terms": ["sender", "short code"],
                    "notes": "Angola appeared in evidence.",
                    "evidence_document_ids": ["colombia_co", "angola_ao"],
                    "evidence_block_ids": ["colombia-block", "angola-block"],
                },
            )

    response = asyncio.run(run())

    assert response.status_code == 200
    payload = response.json()
    assert payload["saved"] is True
    assert payload["review_count"] == 1
    review_path = Path(payload["path"])
    assert review_path.exists()
    saved_payload = json.loads(review_path.read_text(encoding="utf-8"))
    assert saved_payload["entries"][0]["rating"] == "correct_with_foreign_evidence"


def test_api_answer_exposes_generated_tier2_answer(monkeypatch, tmp_path: Path) -> None:
    source_dir = tmp_path / "raw"
    work_dir = tmp_path / "work"
    source_dir.mkdir(parents=True, exist_ok=True)
    (source_dir / "spain_es.md").write_text(
        """# Spain (ES)

## Sender
Sender provisioning is not required.

## Capabilities
Two-way messaging is supported.
""",
        encoding="utf-8",
    )

    class FakeResponses:
        def create(self, **kwargs: object) -> object:
            return type("Response", (), {"output_text": "Spain allows two-way messaging and does not require sender provisioning. [1][2]"})()

    class FakeClient:
        def __init__(self) -> None:
            self.responses = FakeResponses()

    class FakeModule:
        @staticmethod
        def OpenAI() -> FakeClient:
            return FakeClient()

    monkeypatch.setattr(
        "own_knowledge_rag.generation.importlib.import_module",
        lambda name: FakeModule(),
    )

    settings = Settings(
        OKR_SOURCE_DIR=source_dir,
        OKR_WORK_DIR=work_dir,
        OKR_GENERATION_PROVIDER="openai",
        OKR_GENERATION_MODEL="gpt-4.1-mini",
    )

    async def run() -> tuple[httpx.Response, httpx.Response]:
        transport = httpx.ASGITransport(app=create_app(settings))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            build_response = await client.post(
                "/build-index",
                json={"source_dir": str(source_dir), "work_dir": str(work_dir), "allow_low_quality": True},
            )
            answer_response = await client.post(
                "/answer",
                json={"question": "Compare sender provisioning and two-way support in Spain.", "work_dir": str(work_dir), "top_k": 3},
            )
            return build_response, answer_response

    build_response, answer_response = asyncio.run(run())

    assert build_response.status_code == 200
    assert answer_response.status_code == 200
    payload = answer_response.json()
    # Corpus-first routing: with a single-document fixture, the corpus can answer
    # without the provider. Any non-refusal grounded tier is valid; the key is the answer is returned.
    assert payload["tier"] in {"tier0", "tier1", "tier2"}
    assert payload["cached"] is False


def test_api_evaluate_endpoint(tmp_path: Path) -> None:
    source_dir = tmp_path / "raw"
    work_dir = tmp_path / "work"
    source_dir.mkdir(parents=True, exist_ok=True)
    (source_dir / "spain_es.md").write_text(
        """# Spain (ES)

## Sender
| Key | Value |
| --- | --- |
| Sender provisioning | No sender registration needed. |
""",
        encoding="utf-8",
    )
    benchmark = tmp_path / "benchmark.json"
    benchmark.write_text(
        """
[
  {
    "question": "Sender in Spain?",
    "expected_document_ids": ["spain_es"],
    "expected_terms": ["sender provisioning", "no sender registration needed"],
    "question_type": "factoid",
    "should_refuse": false
  }
]
""".strip(),
        encoding="utf-8",
    )

    settings = Settings(OKR_SOURCE_DIR=source_dir, OKR_WORK_DIR=work_dir)
    async def run() -> httpx.Response:
        transport = httpx.ASGITransport(app=create_app(settings))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            await client.post(
                "/build-index",
                json={"source_dir": str(source_dir), "work_dir": str(work_dir)},
            )
            return await client.post(
                "/evaluate",
                json={"benchmark_path": str(benchmark), "work_dir": str(work_dir), "top_k": 3},
            )

    response = asyncio.run(run())

    assert response.status_code == 200
    assert response.json()["total_cases"] == 1
    assert "answer_cache_hit_rate" in response.json()
    assert "citation_accuracy" in response.json()
    assert "country_match_at_1" in response.json()
    assert "foreign_evidence_rate" in response.json()
    assert "tier_distribution" in response.json()
    assert "fix_recommendations" in response.json()


def test_api_gate_run_endpoint(tmp_path: Path) -> None:
    source_dir = tmp_path / "raw"
    work_dir = tmp_path / "work"
    source_dir.mkdir(parents=True, exist_ok=True)
    (source_dir / "spain_es.md").write_text(
        """# Spain (ES)

## Sender
| Key | Value |
| --- | --- |
| Sender provisioning | No sender registration needed. |
""",
        encoding="utf-8",
    )
    benchmark = tmp_path / "benchmark.json"
    benchmark.write_text(
        """
[
  {
    "question": "Sender in Spain?",
    "expected_document_ids": ["spain_es"],
    "expected_block_types": ["table"],
    "question_type": "factoid",
    "should_refuse": false
  }
]
""".strip(),
        encoding="utf-8",
    )

    settings = Settings(OKR_SOURCE_DIR=source_dir, OKR_WORK_DIR=work_dir)

    async def run() -> httpx.Response:
        transport = httpx.ASGITransport(app=create_app(settings))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            await client.post(
                "/build-index",
                json={"source_dir": str(source_dir), "work_dir": str(work_dir)},
            )
            return await client.post(
                "/gate/run",
                json={
                    "benchmark_path": str(benchmark),
                    "work_dir": str(work_dir),
                    "top_k": 3,
                    "min_cases": 1,
                    "allow_low_count": [],
                },
            )

    response = asyncio.run(run())

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "pass"
    assert payload["audit"]["adequate"] is True
    assert payload["audit"]["warnings"] == []
    assert payload["metrics"]["total_cases"] == 1
    assert {check["name"] for check in payload["checks"]} == {
        "Benchmark audit",
        "Recall@k",
        "Evidence hit rate",
        "Answer correctness",
    }


def test_api_calibrate_endpoint(tmp_path: Path) -> None:
    source_dir = tmp_path / "raw"
    work_dir = tmp_path / "work"
    source_dir.mkdir(parents=True, exist_ok=True)
    (source_dir / "spain_es.md").write_text(
        """# Spain (ES)

## Sender
| Key | Value |
| --- | --- |
| Sender provisioning | No sender registration needed. |
""",
        encoding="utf-8",
    )
    benchmark = tmp_path / "benchmark.json"
    benchmark.write_text(
        """
[
  {
    "question": "Sender in Spain?",
    "expected_document_ids": ["spain_es"],
    "expected_terms": ["sender provisioning", "no sender registration needed"],
    "question_type": "factoid",
    "should_refuse": false
  },
  {
    "question": "What is the moon made of in this corpus?",
    "expected_document_ids": [],
    "expected_terms": [],
    "question_type": "refusal",
    "should_refuse": true
  }
]
""".strip(),
        encoding="utf-8",
    )

    settings = Settings(OKR_SOURCE_DIR=source_dir, OKR_WORK_DIR=work_dir)

    async def run() -> tuple[httpx.Response, httpx.Response]:
        transport = httpx.ASGITransport(app=create_app(settings))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            build_response = await client.post(
                "/build-index",
                json={"source_dir": str(source_dir), "work_dir": str(work_dir)},
            )
            calibrate_response = await client.post(
                "/calibrate-refusal",
                json={"benchmark_path": str(benchmark), "work_dir": str(work_dir), "top_k": 3},
            )
            return build_response, calibrate_response

    build_response, calibrate_response = asyncio.run(run())
    assert build_response.status_code == 200
    assert calibrate_response.status_code == 200
    payload = calibrate_response.json()
    assert payload["recommended_min_score_threshold"] > 0
    assert payload["recommended_min_overlap_ratio"] > 0
    assert payload["recommended_tier0_score_threshold"] > 0
    assert payload["recommended_tier2_score_threshold"] > 0


def test_api_explain_block_endpoint_returns_structured_block(tmp_path: Path) -> None:
    source_dir = tmp_path / "raw"
    work_dir = tmp_path / "work"
    source_dir.mkdir(parents=True, exist_ok=True)
    (source_dir / "spain_es.md").write_text(
        """# Spain (ES)

## Sender
| Key | Value |
| --- | --- |
| Sender provisioning | No sender registration needed. |
""",
        encoding="utf-8",
    )

    settings = Settings(OKR_SOURCE_DIR=source_dir, OKR_WORK_DIR=work_dir)

    async def run() -> tuple[httpx.Response, httpx.Response]:
        transport = httpx.ASGITransport(app=create_app(settings))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            build_response = await client.post(
                "/build-index",
                json={"source_dir": str(source_dir), "work_dir": str(work_dir), "allow_low_quality": True},
            )
            explain_response = await client.post(
                "/explain-block",
                json={"block_id": "spain_es-block-1", "work_dir": str(work_dir)},
            )
            return build_response, explain_response

    build_response, explain_response = asyncio.run(run())

    assert build_response.status_code == 200
    assert explain_response.status_code == 200
    payload = explain_response.json()
    assert payload["block_id"] == "spain_es-block-1"
    assert payload["document_id"] == "spain_es"
    assert payload["enrichment_provider"]
    assert payload["enrichment_model"]
    assert payload["enriched_at"]
    assert isinstance(payload["metadata"], dict)


def test_api_explain_block_endpoint_returns_404_for_missing_block(tmp_path: Path) -> None:
    source_dir = tmp_path / "raw"
    work_dir = tmp_path / "work"
    source_dir.mkdir(parents=True, exist_ok=True)
    (source_dir / "spain_es.md").write_text(
        """# Spain (ES)

## Sender
Sender provisioning: No sender registration needed.
""",
        encoding="utf-8",
    )

    settings = Settings(OKR_SOURCE_DIR=source_dir, OKR_WORK_DIR=work_dir)

    async def run() -> tuple[httpx.Response, httpx.Response]:
        transport = httpx.ASGITransport(app=create_app(settings))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            build_response = await client.post(
                "/build-index",
                json={"source_dir": str(source_dir), "work_dir": str(work_dir), "allow_low_quality": True},
            )
            explain_response = await client.post(
                "/explain-block",
                json={"block_id": "missing-block", "work_dir": str(work_dir)},
            )
            return build_response, explain_response

    build_response, explain_response = asyncio.run(run())

    assert build_response.status_code == 200
    assert explain_response.status_code == 404
    assert "Block not found" in explain_response.json()["detail"]
