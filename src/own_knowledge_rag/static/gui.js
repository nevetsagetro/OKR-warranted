/* Own Knowledge RAG GUI behavior
   The HTML template injects runtime defaults into #okr-defaults before this file loads. */

// Drawer Logic
const drawer = document.getElementById('evidence-drawer');
const overlay = document.getElementById('drawer-overlay');

function openDrawer() {
  drawer.classList.add('active');
  overlay.classList.add('active');
}

function closeDrawer() {
  drawer.classList.remove('active');
  overlay.classList.remove('active');
}

document.getElementById('drawer-close').addEventListener('click', closeDrawer);
overlay.addEventListener('click', closeDrawer);

// Global functions attached to window
window.openEvidenceDrawer = openDrawer;
window.closeEvidenceDrawer = closeDrawer;

function activateTab(targetId) {
  document.querySelectorAll('.nav-item').forEach(nav => {
    nav.classList.toggle('active', nav.getAttribute('data-target') === targetId);
  });
  document.querySelectorAll('.tab-pane').forEach(pane => pane.classList.remove('active'));
  const target = document.getElementById(targetId);
  if (target) target.classList.add('active');
}

function focusPanel(panelId) {
  const panel = document.getElementById(panelId);
  if (!panel) return;
  if (panel.tagName === "DETAILS") panel.open = true;
  panel.scrollIntoView({ behavior: "smooth", block: "start" });
  panel.style.boxShadow = "0 0 0 3px rgba(37, 99, 235, 0.18)";
  window.setTimeout(() => { panel.style.boxShadow = ""; }, 1600);
}

function openExperimentHistory() {
  activateTab("tab-ml-ds");
  refreshExperiments().catch(() => {});
  window.setTimeout(() => focusPanel("experiment-history-panel"), 80);
}

window.openExperimentHistory = openExperimentHistory;

function setSidebarCollapsed(collapsed) {
  document.body.classList.toggle("sidebar-collapsed", collapsed);
  const button = document.getElementById("sidebar-toggle");
  const icon = document.getElementById("sidebar-toggle-icon");
  if (button) {
    button.title = collapsed ? "Expand navigation" : "Collapse navigation";
    button.setAttribute("aria-label", collapsed ? "Expand navigation" : "Collapse navigation");
  }
  if (icon) {
    icon.setAttribute("d", collapsed ? "M13 5l7 7-7 7M5 5l7 7-7 7" : "M11 19l-7-7 7-7M19 19l-7-7 7-7");
  }
  try {
    localStorage.setItem("okrSidebarCollapsed", collapsed ? "1" : "0");
  } catch (_error) {}
}

try {
  const storedSidebar = localStorage.getItem("okrSidebarCollapsed");
  if (storedSidebar !== null) setSidebarCollapsed(storedSidebar !== "0");
} catch (_error) {}

const sidebarToggle = document.getElementById("sidebar-toggle");
if (sidebarToggle) {
  sidebarToggle.addEventListener("click", () => {
    setSidebarCollapsed(!document.body.classList.contains("sidebar-collapsed"));
  });
}

document.querySelectorAll('.nav-item, .nav-shortcut').forEach(item => {
  item.addEventListener('click', function(event) {
    event.preventDefault();
    activateTab(this.getAttribute('data-target'));
  });
});


// -----------------------------------------------------------------------------
// Runtime State
// -----------------------------------------------------------------------------
function readRuntimeDefaults() {
  const defaultsEl = document.getElementById("okr-defaults");
  if (!defaultsEl) return {};
  try {
    return JSON.parse(defaultsEl.textContent || "{}");
  } catch (_error) {
    return {};
  }
}

const defaults = readRuntimeDefaults();
const DEFAULT_TOP_K = 5;
const MIN_TOP_K = 0;
const MAX_TOP_K = 10;
const outputEl = document.getElementById("output");
const chatLogEl = document.getElementById("chat-log");
let lastAnswerPayload = null;
let latestHumanReviewPrompts = [];
let libraryEnrichmentPromptTemplate = defaults.enrichmentPromptTemplate || "";
let libraryFaqPromptTemplate = defaults.faqPromptTemplate || "";
let experimentWorkDirAutoValue = "";
let experimentSourceDirAutoValue = "";
let experimentWorkDirManualOverride = false;
let experimentSourceDirManualOverride = false;
let lastLoadedPromotionBackup = "";
let lastLowQualityBlocks = [];

function formatElapsed(seconds) {
  const value = Number(seconds);
  if (!Number.isFinite(value) || value < 0) return "0.0s";
  if (value < 60) return `${value.toFixed(1)}s`;
  const minutes = Math.floor(value / 60);
  const remaining = Math.round(value % 60).toString().padStart(2, "0");
  return `${minutes}m ${remaining}s`;
}

function startLoadingTimer(containerId, textId, label) {
  const container = document.getElementById(containerId);
  const text = document.getElementById(textId);
  const startedAt = performance.now();
  if (container) container.classList.add("active");
  const render = () => {
    const elapsed = (performance.now() - startedAt) / 1000;
    if (text) text.textContent = `${label} ${formatElapsed(elapsed)}`;
  };
  render();
  const interval = window.setInterval(render, 500);
  return {
    stop(finalLabel) {
      window.clearInterval(interval);
      const elapsed = (performance.now() - startedAt) / 1000;
      if (text) text.textContent = `${finalLabel || label} ${formatElapsed(elapsed)}`;
      if (container) container.classList.remove("active");
      return elapsed;
    },
  };
}

  
// -----------------------------------------------------------------------------
// Chat Transcript
// -----------------------------------------------------------------------------
function appendMessage(role, text, label) {
    if (!chatLogEl) return;
    const el = document.createElement("div");
    el.className = `chat-message ${role}`;
    const meta = label || role;
    const metaHtml = role === "answer"
      ? `<div class="chat-meta verified-badge">${verifiedIconSvg()} ${escapeHtml(meta)}</div>`
      : `<div class="chat-meta">${escapeHtml(meta)}</div>`;
    el.innerHTML = `
      ${metaHtml}
      <div class="chat-body">${text}</div>
    `;
    chatLogEl.appendChild(el);
    chatLogEl.scrollTop = chatLogEl.scrollHeight;
  }

  const clearBtn = document.getElementById("clear-chat-btn");
  if(clearBtn) clearBtn.addEventListener("click", () => {
    chatLogEl.innerHTML = '';
    appendMessage('system', 'Chat cleared.', 'System Status');
  });

  function downloadChatTranscript() {
    if (!chatLogEl) return;
    const lines = Array.from(chatLogEl.querySelectorAll(".chat-message")).map((message) => {
      const role = Array.from(message.classList).find((name) => name !== "chat-message") || "message";
      const meta = message.querySelector(".chat-meta")?.textContent?.trim() || role;
      const body = message.querySelector(".chat-body")?.textContent?.trim() || "";
      return `[${role.toUpperCase()}] ${meta}\n${body}`;
    });
    const blob = new Blob([lines.join("\n\n")], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `rag-chat-transcript-${new Date().toISOString().slice(0, 19).replace(/[:T]/g, "-")}.txt`;
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
  }

  const downloadChatBtn = document.getElementById("download-chat-btn");
  if (downloadChatBtn) downloadChatBtn.addEventListener("click", downloadChatTranscript);

function renderSummary(containerEl, rows) {
  if (!containerEl) return;
  containerEl.innerHTML = rows.map(([value, label]) => `
    <div class="kv"><span>${label}</span><strong>${value !== null && value !== undefined ? value : "—"}</strong></div>
  `).join("");
}

  
// -----------------------------------------------------------------------------
// Shared Formatting Helpers
// -----------------------------------------------------------------------------
function successIconSvg() {
    return `<svg width="12" height="12" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"></path></svg>`;
  }

  function verifiedIconSvg() {
    return `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 12l2 2 4-4"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3l7 4v5c0 4.5-2.7 7.8-7 9-4.3-1.2-7-4.5-7-9V7l7-4z"></path></svg>`;
  }

  function warningIconSvg() {
    return `<svg width="12" height="12" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M12 8v5m0 4h.01M10.3 4.3L2.7 18a2 2 0 001.7 3h15.2a2 2 0 001.7-3L13.7 4.3a2 2 0 00-3.4 0z"></path></svg>`;
  }

function renderHomeHealth(containerEl, rows) {
  if (!containerEl) return;
  containerEl.innerHTML = rows.map(({label, value, ok}) => `
    <div class="health-row">
      <span class="health-row-label">${escapeHtml(label)}</span>
      <strong class="health-status ${ok ? "" : "warning"}">
        <span class="health-icon ${ok ? "" : "warning"}">${ok ? successIconSvg() : warningIconSvg()}</span>
        ${escapeHtml(value)}
      </strong>
    </div>
  `).join("");
}

function formatUnixDate(seconds) {
  if (!seconds) return "Not indexed yet";
  try {
    return new Intl.DateTimeFormat(undefined, {
      year: "numeric",
      month: "short",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
    }).format(new Date(Number(seconds) * 1000));
  } catch (_error) {
    return String(seconds);
  }
}

function documentDisplayName(documentId) {
  const value = String(documentId || "").replace(/__\d+$/, "").replace(/_[a-z]{2}$/i, "");
  return value
    .split("_")
    .filter(Boolean)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

function sampleDocumentNames(ids, totalDocuments) {
  const names = (Array.isArray(ids) ? ids : []).map(documentDisplayName).filter(Boolean).slice(0, 3);
  if (!names.length) return `${totalDocuments || 0} documents`;
  const remaining = Math.max(0, Number(totalDocuments || 0) - names.length);
  return `${names.join(", ")}${remaining ? ` +${remaining} more` : ""}`;
}

function documentHoverDetails(ids, totalDocuments) {
  const idText = Array.isArray(ids) && ids.length ? ids.join(", ") : "No sample document IDs available";
  return `${totalDocuments || 0} total document(s). Sample IDs: ${idText}`;
}

function workspaceName(path) {
  const value = String(path || "Active workspace").replace(/\/+$/, "");
  const parts = value.split("/");
  return parts[parts.length - 1] || value;
}

function defaultIndexedMetadata() {
  const options = Array.isArray(defaults.workspaceOptions) ? defaults.workspaceOptions : [];
  return options.find((item) => item.path === defaults.workDir)
    || options.find((item) => item.kind === "baseline")
    || {};
}

function indexedWithFallback(indexed) {
  const fallback = defaultIndexedMetadata();
  indexed = indexed || {};
  return {
    ...indexed,
    available: Boolean(indexed.available || fallback.index_ready),
    documents: indexed.documents || fallback.documents || 0,
    blocks: indexed.blocks || fallback.blocks || 0,
    manifest_path: indexed.manifest_path || fallback.manifest_path || `${defaults.workDir || "data/work"}/manifest.json`,
    manifest_modified_at: indexed.manifest_modified_at || fallback.manifest_modified_at || 0,
    index_id: indexed.index_id || fallback.index_id || "",
    document_ids_sample: (
      Array.isArray(indexed.document_ids_sample) && indexed.document_ids_sample.length
        ? indexed.document_ids_sample
        : fallback.document_ids_sample || []
    ),
  };
}

function renderGateDetails(gate) {
  const el = document.getElementById("gate-details");
  if (!el) return;
  const checks = gate.checks || [];
  const warnings = gate.audit?.warnings || [];
  const allowed = gate.audit?.allowed_low_count_findings || [];
  const checkHtml = checks.map((check) => `
    <div class="kv"><span>${escapeHtml(check.name)}</span><strong>${escapeHtml(check.status)} · ${escapeHtml(check.value)} / ${escapeHtml(check.target)}</strong></div>
  `).join("");
  const warningHtml = warnings.length
    ? warnings.map((warning) => `<li>${escapeHtml(warning)}</li>`).join("")
    : "<li>none</li>";
  const allowedHtml = allowed.length
    ? allowed.map((finding) => `<li>${escapeHtml(finding)}</li>`).join("")
    : "<li>none</li>";
  el.style.display = "block";
  el.innerHTML = `
    <strong>Checks</strong>
    <div class="kv-list" style="margin-top:10px;">${checkHtml}</div>
    <div class="grid-2" style="gap:12px; margin-top:12px;">
      <div><strong>Audit warnings</strong><ul class="help-note" style="padding-left:18px;">${warningHtml}</ul></div>
      <div><strong>Allowed low-count</strong><ul class="help-note" style="padding-left:18px;">${allowedHtml}</ul></div>
    </div>
  `;
}

function renderTesting(runtime) {
  const el = document.getElementById("testing-readiness");
  if (!el) return;
  const indexed = indexedWithFallback(runtime.indexed);
  const items = [
    ["Index available", indexed.available ? "✓ yes" : "✗ not built"],
    ["Documents", indexed.documents ?? "—"],
    ["Blocks", indexed.blocks ?? "—"],
    ["Vector backend", indexed.vector_backend || "—"],
  ];
  renderSummary(el, items.map(([l,v])=>[v,l]));

  const chip = document.getElementById("status-chip");
  if(chip) {
    if(indexed.available) {
      chip.textContent = "● System Online";
      chip.classList.add("success");
    } else {
      chip.textContent = "○ Waiting for Index";
      chip.classList.remove("success");
    }
  }
}


// -----------------------------------------------------------------------------
// Dashboard Rendering
// -----------------------------------------------------------------------------
function renderHome(runtime) {
  const indexed = indexedWithFallback(runtime.indexed);
  const testing = runtime.testing;
  const status = indexed.available ? "Ready" : "Needs index";
  const sourceReady = Boolean(testing.source_dir_exists || indexed.available);
  const evaluationReady = Boolean(testing.latest_evaluation_available || indexed.available);
  const homeStatus = document.getElementById("home-status");
  if (homeStatus) {
    homeStatus.className = `status-pill ${indexed.available ? "" : "warning"}`;
    homeStatus.innerHTML = `${indexed.available ? successIconSvg() : warningIconSvg()} ${escapeHtml(status)}`;
  }
  const homeDocs = document.getElementById("home-documents");
  if (homeDocs) homeDocs.textContent = indexed.documents ?? 0;
  const homeBlocks = document.getElementById("home-blocks");
  if (homeBlocks) homeBlocks.textContent = indexed.blocks ?? 0;
  const homeBackend = document.getElementById("home-backend");
  if (homeBackend) homeBackend.textContent = indexed.vector_backend || "none";
  renderHomeHealth(document.getElementById("home-warnings"), [
    {
      label: "Index",
      value: testing.index_available ? "Ready for questions" : "Build an index",
      ok: Boolean(testing.index_available),
    },
    {
      label: "Source",
      value: testing.source_dir_exists
        ? "Source folder found"
        : indexed.available
          ? "Using prebuilt index"
          : "Source folder missing",
      ok: sourceReady,
    },
    {
      label: "Evaluation",
      value: testing.latest_evaluation_available
        ? "Report found"
        : indexed.available
          ? "Optional for demo"
          : "Run evaluation",
      ok: evaluationReady,
    },
  ]);
  renderSummary(document.getElementById("home-ingestion-summary"), [
    [formatUnixDate(indexed.manifest_modified_at), "Last indexed"],
    [`${indexed.documents ?? 0} documents / ${indexed.blocks ?? 0} blocks`, "Corpus scope"],
    [indexed.rebuilt_documents ?? 0, "Documents rebuilt"],
    [indexed.reused_documents ?? 0, "Documents reused"],
    [workspaceName(defaults.workDir), "Workspace"],
    [(indexed.allowed_suffixes || []).join(", ") || "All supported", "Indexed file types"],
    [`${indexed.mapping_provider || "n/a"} / ${indexed.embedding_provider || "n/a"}`, "Model pipeline"],
  ]);
}

function renderLibrary(runtime) {
  const indexed = indexedWithFallback(runtime.indexed);
  const docs = document.getElementById("library-documents");
  if (docs) docs.textContent = indexed.documents ?? 0;
  const blocks = document.getElementById("library-blocks");
  if (blocks) blocks.textContent = indexed.blocks ?? 0;
  const metadataStatus = document.getElementById("library-metadata-status");
  if (metadataStatus) {
    metadataStatus.className = `status-pill ${indexed.available ? "" : "warning"}`;
    metadataStatus.innerHTML = `${indexed.available ? successIconSvg() : warningIconSvg()} ${indexed.available ? "Ready" : "Missing"}`;
  }
  const fileTypes = document.getElementById("library-file-types");
  if (fileTypes) fileTypes.textContent = (indexed.allowed_suffixes || []).join(", ") || "—";
  const metadataCell = document.getElementById("library-metadata-cell");
  if (metadataCell) {
    metadataCell.innerHTML = indexed.available
      ? `<span class="badge success">Available</span>`
      : `<span class="badge" style="background:#fffbeb; color:#92400e; border-color:#fde68a;">Pending</span>`;
  }
  const chunkCell = document.getElementById("library-chunk-cell");
  if (chunkCell) chunkCell.textContent = indexed.blocks ?? 0;
  const table = document.getElementById("library-table-body");
  if (table) {
    const indexedAt = formatUnixDate(indexed.manifest_modified_at);
    const indexId = indexed.index_id || "—";
    const hoverDetails = documentHoverDetails(indexed.document_ids_sample, indexed.documents);
    const documentNames = sampleDocumentNames(indexed.document_ids_sample, indexed.documents);
    const activeWorkspaceName = workspaceName(defaults.workDir);
    table.innerHTML = `
      <tr>
        <td>
          <strong title="${escapeHtml(defaults.workDir || "Active workspace")}">${escapeHtml(activeWorkspaceName)}</strong>
          <div class="table-meta-line">${escapeHtml(defaults.workDir || "Active workspace")}</div>
          <div class="table-meta-line" title="${escapeHtml(hoverDetails)}"><span class="meta-label">Index ID:</span> <span class="meta-value">${escapeHtml(indexId)}</span></div>
        </td>
        <td>${(indexed.allowed_suffixes || []).join(", ") || "—"}</td>
        <td><span class="badge ${indexed.available ? "success" : ""}" style="${indexed.available ? "" : "background:#fffbeb; color:#92400e; border-color:#fde68a;"}">${indexed.available ? "Parsed" : "Pending"}</span></td>
        <td>${indexed.available ? `<span class="badge success">Available</span>` : `<span class="badge" style="background:#fffbeb; color:#92400e; border-color:#fde68a;">Pending</span>`}</td>
        <td>${indexed.blocks ?? 0}</td>
        <td>
          <strong>${escapeHtml(indexedAt)}</strong>
          <div class="table-meta-line"><span class="meta-label">Scope:</span> <span class="meta-value">${indexed.documents ?? 0} documents / ${indexed.blocks ?? 0} blocks</span></div>
          <div class="table-meta-line" title="${escapeHtml(hoverDetails)}"><span class="meta-label">Countries:</span> <span class="meta-value">${escapeHtml(documentNames).replace(/(\+\d+ more)$/, '<span class="compact-more" title="' + escapeHtml(hoverDetails) + '">$1</span>')}</span></div>
          <button class="ghost" type="button" onclick="openExperimentHistory()" style="margin-top:8px; padding:6px 10px; font-size:0.78rem;">Manage history</button>
        </td>
      </tr>
    `;
  }
}

function renderBaselineStatus(status) {
  status = status || {
    baseline_work_dir: defaults.workDir || "data/work",
    promoted_baseline: (defaults.workDir || "data/work").endsWith("/work") || defaults.workDir === "data/work",
    exists: false,
    index_ready: false,
    documents: null,
    blocks: null,
    rollback_backup_count: null,
    latest_rollback_backup: null,
  };
  const summaryEl = document.getElementById("baseline-status-summary");
  if (summaryEl) {
    const indexLabel = status.index_ready ? "Ready" : status.exists ? "Missing artifacts" : "Missing";
    const indexPill = status.index_ready
      ? `<span class="status-pill">${successIconSvg()} Ready</span>`
      : `<span class="status-pill warning">${warningIconSvg()} ${escapeHtml(indexLabel)}</span>`;
    summaryEl.innerHTML = `
      <div class="status-tile"><span>Promoted baseline</span><strong>${escapeHtml(status.promoted_baseline ? "data/work" : status.baseline_work_dir)}</strong></div>
      <div class="status-tile"><span>Index</span><strong>${indexPill}</strong></div>
      <div class="status-tile"><span>Documents</span><strong><span class="badge success">${escapeHtml(status.documents ?? 0)}</span></strong></div>
      <div class="status-tile"><span>Blocks</span><strong>${escapeHtml(status.blocks ?? 0)}</strong></div>
      <div class="status-tile"><span>Rollback backups</span><strong><span class="badge">${escapeHtml(status.rollback_backup_count ?? 0)}</span></strong></div>
    `;
  }
  const rollbackEl = document.getElementById("baseline-rollback-summary");
  if (!rollbackEl) return;
  const latest = status.latest_rollback_backup;
  if (latest && latest.valid) {
    rollbackEl.innerHTML = `
      <div class="flex-between" style="gap:12px; align-items:flex-start;">
        <div>
          <strong>Latest rollback</strong>
          <p class="help-note">${escapeHtml(latest.path)} · valid backup</p>
        </div>
        <button class="secondary mini-action" type="button" title="Open rollback tools" aria-label="Open rollback tools" onclick="activateTab('tab-system'); focusPanel('exp-rollback-button');">
          <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10a9 9 0 019-7 9 9 0 019 9 9 9 0 01-9 9 9 9 0 01-8-5M3 10V4m0 6h6"></path></svg>
        </button>
      </div>
    `;
  } else {
    rollbackEl.innerHTML = `
      <strong>Latest rollback</strong>
      <p class="help-note">No valid rollback backup found for this baseline yet.</p>
    `;
  }
}

async function refreshBaselineStatus() {
  const baselineDir = stringOrNull("exp-baseline-work-dir") || defaults.workDir;
  try {
    const payload = await request(`/baseline/status?baseline_work_dir=${encodeURIComponent(baselineDir)}`, null, "GET");
    renderBaselineStatus(payload);
    return payload;
  } catch (error) {
    renderBaselineStatus({
      baseline_work_dir: baselineDir,
      promoted_baseline: baselineDir === "data/work" || baselineDir.endsWith("/work"),
      exists: false,
      index_ready: false,
      documents: null,
      blocks: null,
      rollback_backup_count: null,
      latest_rollback_backup: null,
    });
    return null;
  }
}

function renderHumanReviewReadiness(readiness) {
  readiness = readiness || {
    work_dir: defaults.workDir || "data/work",
    total_query_reviews: 0,
    should_refuse_count: 0,
    foreign_or_wrong_country_count: 0,
    multi_fact_or_comparison_count: 0,
    accepted_review_findings_count: 0,
    quality_warnings: [],
    ready_for_export: false,
    gate_mode: "advisory",
    rating_counts: {},
    checks: [],
    missing_targets: [],
    proposed_outputs: [],
    message: "Human review readiness has not been checked yet.",
  };
  renderSummary(document.getElementById("human-review-summary"), [
    [readiness.ready_for_export ? "Ready" : "Collect reviews", "Benchmark export"],
    [readiness.gate_mode || "advisory", "Gate mode"],
    [readiness.total_query_reviews ?? 0, "Saved reviews"],
    [readiness.should_refuse_count ?? 0, "Should refuse"],
    [readiness.foreign_or_wrong_country_count ?? 0, "Foreign/wrong country"],
    [readiness.multi_fact_or_comparison_count ?? 0, "Multi-fact/comparison"],
    [readiness.accepted_review_findings_count ?? 0, "Accepted findings"],
  ]);
  const checksEl = document.getElementById("human-review-checks");
  if (!checksEl) return;
  const exportStatus = document.getElementById("human-review-export-status");
  if (exportStatus) {
    exportStatus.textContent = readiness.ready_for_export
      ? "Ready to export query-review benchmark artifacts."
      : "Export is guarded until review coverage reaches the approved thresholds.";
  }
  const checks = readiness.checks || [];
  const checkHtml = checks.length
    ? checks.map((check) => `
        <div class="kv">
          <span>${escapeHtml(check.name)}</span>
          <strong>${escapeHtml(check.status)} · ${escapeHtml(check.value)} / ${escapeHtml(check.target)}</strong>
        </div>
      `).join("")
    : `<p class="help-note">No human review file found yet.</p>`;
  const ratings = readiness.rating_counts || {};
  const ratingHtml = Object.keys(ratings).length
    ? Object.entries(ratings)
        .sort((a, b) => b[1] - a[1])
        .map(([rating, count]) => `<span class="badge">${escapeHtml(rating)}: ${escapeHtml(count)}</span>`)
        .join(" ")
    : `<span class="badge">no ratings yet</span>`;
  const outputHtml = (readiness.proposed_outputs || [])
    .map((path) => `<li>${escapeHtml(path)}</li>`)
    .join("");
  const warningHtml = (readiness.quality_warnings || []).length
    ? `
      <div style="margin-top:12px;">
        <strong>Review QA warnings</strong>
        <ul style="margin:8px 0 0 18px;">
          ${readiness.quality_warnings.map((warning) => `
            <li>${escapeHtml(warning.review_id)} · ${escapeHtml(warning.message)}</li>
          `).join("")}
        </ul>
      </div>
    `
    : "";
  latestHumanReviewPrompts = readiness.collection_prompts || [];
  const missingHtml = (readiness.missing_targets || []).length
    ? `
      <div style="margin-top:12px;">
        <strong>Next review targets</strong>
        <ul style="margin:8px 0 0 18px;">
          ${readiness.missing_targets.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
        </ul>
      </div>
    `
    : "";
  const templateHtml = latestHumanReviewPrompts.length
    ? `
      <div style="margin-top:12px;">
        <strong>Suggested review starters</strong>
        <div class="quick-actions" style="margin-top:8px;">
          ${latestHumanReviewPrompts.map((template, index) => `
            <button class="secondary human-review-prompt" type="button" data-review-prompt-index="${index}">
              ${escapeHtml(template.label)}
            </button>
          `).join("")}
        </div>
      </div>
    `
    : "";
  checksEl.innerHTML = `
    <strong>${escapeHtml(readiness.message || "Review readiness checked.")}</strong>
    <div class="kv-list" style="margin-top:12px;">${checkHtml}</div>
    <div style="margin-top:12px;">${ratingHtml}</div>
    ${warningHtml}
    ${missingHtml}
    ${templateHtml}
    <p class="help-note" style="margin-top:12px;">Reviews: ${escapeHtml(readiness.query_reviews_path || "")}</p>
    ${outputHtml ? `<ul style="margin:8px 0 0 18px;">${outputHtml}</ul>` : ""}
  `;
  checksEl.querySelectorAll(".human-review-prompt").forEach((button) => {
    button.addEventListener("click", () => useHumanReviewPrompt(Number(button.dataset.reviewPromptIndex)));
  });
}

async function refreshHumanReviewReadiness() {
  const workDir = stringOrNull("human-review-work-dir") || defaults.workDir;
  try {
    const payload = await request(`/human-review/readiness?work_dir=${encodeURIComponent(workDir)}`, null, "GET");
    renderHumanReviewReadiness(payload);
    return payload;
  } catch (error) {
    renderHumanReviewReadiness(null);
    return null;
  }
}

async function exportHumanReviewBenchmark() {
  const workDir = stringOrNull("human-review-work-dir") || defaults.workDir;
  const statusEl = document.getElementById("human-review-export-status");
  if (statusEl) statusEl.textContent = "Checking readiness before export...";
  try {
    const payload = await request("/human-review/export-benchmark", {
      work_dir: workDir,
      output_dir: "benchmarks",
      allow_undercovered: false,
    });
    renderHumanReviewReadiness(payload.readiness);
    if (statusEl) {
      statusEl.textContent = `${payload.message} Query cases: ${payload.query_review_cases}.`;
    }
    return payload;
  } catch (error) {
    const readiness = error?.data?.detail?.readiness;
    if (readiness) renderHumanReviewReadiness(readiness);
    if (statusEl) {
      statusEl.textContent = error?.data?.detail?.message || error.message;
    }
    return null;
  }
}

function openReviewCollection() {
  activateTab("tab-query");
  const questionEl = document.getElementById("question");
  if (questionEl) {
    const currentNeed = document.querySelector("#human-review-checks li")?.textContent || "";
    if (!questionEl.value.trim() && currentNeed) {
      questionEl.placeholder = `Collect: ${currentNeed}`;
    }
    questionEl.scrollIntoView({ behavior: "smooth", block: "center" });
    questionEl.focus();
  }
  appendMessage(
    "system",
    "Collect a Phase 9 review: ask a real question, inspect the evidence, then use Rate This Answer in the evidence drawer to save the rating.",
    "review"
  );
}

function useHumanReviewPrompt(index) {
  const template = latestHumanReviewPrompts[Number(index)];
  if (!template) return;
  activateTab("tab-query");
  const questionEl = document.getElementById("question");
  if (questionEl) {
    questionEl.value = template.question || "";
    questionEl.focus();
    questionEl.scrollIntoView({ behavior: "smooth", block: "center" });
  }
  const ratingEl = document.getElementById("review-rating");
  if (ratingEl && template.rating_hint) ratingEl.value = template.rating_hint;
  const statusEl = document.getElementById("review-save-status");
  if (statusEl) statusEl.textContent = template.notes || "Ask this starter, inspect the evidence, then save the review.";
  appendMessage("system", `Review starter loaded: ${template.label}.`, "review");
}

function setButtonsDisabled(disabled) {
  document.querySelectorAll("button").forEach((button) => {
    button.disabled = disabled;
  });
}

function setValue(id, value) {
  const el = document.getElementById(id);
  if (!el || value === undefined || value === null) return;
  if (el.type === "checkbox") {
    el.checked = Boolean(value);
    return;
  }
  el.value = value;
}

function stringOrNull(id) {
  const el = document.getElementById(id);
  if (!el) return null;
  const value = String(el.value || "").trim();
  return value ? value : null;
}

function numberOrNull(id) {
  const el = document.getElementById(id);
  if (!el) return null;
  const value = String(el.value || "").trim();
  if (!value) return null;
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

function parseSuffixes() {
  const selectedPreset = document.querySelector('input[name="suffix-preset"]:checked')?.value || "all_supported";
  if (selectedPreset === "markdown_only") return [".md"];
  if (selectedPreset === "markdown_json") return [".md", ".json"];
  if (selectedPreset === "all_supported") return [".md", ".txt", ".json"];
  const raw = stringOrNull("allowed-suffixes");
  if (!raw) return [];
  return raw
    .split(",")
    .map((value) => value.trim())
    .filter((value) => value)
    .map((value) => value.startsWith(".") ? value.toLowerCase() : `.${value.toLowerCase()}`);
}

function parseExperimentSuffixes() {
  const preset = stringOrNull("exp-suffix-preset") || "all_supported";
  if (preset === "markdown_only") return [".md"];
  if (preset === "markdown_json") return [".md", ".json"];
  if (preset === "all_supported") return [".md", ".txt", ".json"];
  const raw = stringOrNull("exp-allowed-suffixes");
  if (!raw) return [];
  return raw
    .split(",")
    .map((value) => value.trim())
    .filter((value) => value)
    .map((value) => value.startsWith(".") ? value.toLowerCase() : `.${value.toLowerCase()}`);
}

function experimentBuildSuffixes(mergeWithBaseline) {
  const suffixes = parseExperimentSuffixes();
  if (!mergeWithBaseline) return suffixes;
  const normalized = suffixes.map((value) => value.toLowerCase()).sort();
  if (normalized.length === 1 && normalized[0] === ".md") {
    return [".md", ".json", ".txt"];
  }
  return suffixes;
}

function selectedExperimentContentType() {
  return document.querySelector('input[name="exp-content-type"]:checked')?.value || "documents";
}

function syncExperimentContentType() {
  const type = selectedExperimentContentType();
  document.querySelectorAll('input[name="exp-content-type"]').forEach((input) => {
    input.closest(".radio-card")?.classList.toggle("active", input.checked);
  });
  const statusEl = document.getElementById("exp-content-type-status");
  const uploadLabel = document.getElementById("exp-upload-label");
  const uploadHelp = document.getElementById("exp-upload-help");
  const uploadInput = document.getElementById("exp-upload-files");
  const hypothesisEl = document.getElementById("exp-hypothesis");
  const faqHypothesis = "FAQ reviewed Q&A onboarding";
  const documentHypothesis = "Knowledge file onboarding";
  if (type === "faq") {
    if (statusEl) statusEl.textContent = "FAQ experiment selected. Upload reviewed FAQ JSON or Q&A seed files, then run ingestion-health evaluation first. Enable a benchmark only after exporting Q&A seeds.";
    if (uploadLabel) uploadLabel.textContent = "FAQ / Reviewed Q&A Files";
    if (uploadHelp) uploadHelp.textContent = "Upload reviewed FAQ JSON, Q&A seed JSON, or supporting source-fact files. The experiment record will be flagged as FAQ work; Q&A seed benchmarks must be exported before evaluation.";
    const uploadSubtitle = document.getElementById("exp-upload-zone-subtitle");
    if (uploadSubtitle) uploadSubtitle.textContent = "Reviewed FAQ JSON, Q&A seed JSON, source-fact JSON, Markdown, or text.";
    if (uploadInput) uploadInput.setAttribute("accept", ".json,.txt,.md,application/json");
    setValue("exp-suffix-preset", "all_supported");
    setValue("exp-allowed-suffixes", ".md,.json,.txt");
    setValue("exp-use-benchmark", false);
    setValue("exp-benchmark-path", stringOrNull("exp-benchmark-path") || "benchmarks/qa_seed_regressions.json");
    if (hypothesisEl && (!hypothesisEl.value.trim() || hypothesisEl.value.trim() === documentHypothesis)) {
      setValue("exp-hypothesis", faqHypothesis);
      maybeSuggestExperimentPaths(true);
    }
  } else {
    if (statusEl) statusEl.textContent = "Knowledge file experiment selected.";
    if (uploadLabel) uploadLabel.textContent = "Experiment Files";
    if (uploadHelp) uploadHelp.textContent = "Use this when you want to test new raw files without writing directly into the shared `data/raw` baseline.";
    const uploadSubtitle = document.getElementById("exp-upload-zone-subtitle");
    if (uploadSubtitle) uploadSubtitle.textContent = "Markdown, JSON, or text files for this experiment.";
    if (uploadInput) uploadInput.setAttribute("accept", ".md,.json,.txt");
    if (hypothesisEl && (!hypothesisEl.value.trim() || hypothesisEl.value.trim() === faqHypothesis)) {
      setValue("exp-hypothesis", documentHypothesis);
      maybeSuggestExperimentPaths(true);
    }
  }
  syncExperimentSuffixInputState();
  renderExperimentBuildPreview();
  renderExperimentBuildRisk();
}

function updateExperimentUploadSelectionLabel() {
  const filesInput = document.getElementById("exp-upload-files");
  const statusEl = document.getElementById("exp-upload-status");
  const files = Array.from(filesInput?.files || []);
  if (!statusEl) return;
  statusEl.classList.remove("success");
  statusEl.textContent = files.length ? `${files.length} selected` : "No staged files yet";
}

function setExperimentUploadProgress(active) {
  const progressEl = document.getElementById("exp-upload-progress");
  const statusEl = document.getElementById("exp-upload-status");
  if (progressEl) progressEl.classList.toggle("active", Boolean(active));
  if (statusEl) {
    statusEl.classList.toggle("success", !active && statusEl.textContent.includes("staged"));
  }
}

function syncExperimentSuffixInputState() {
  const customInput = document.getElementById("exp-allowed-suffixes");
  if (customInput) customInput.disabled = stringOrNull("exp-suffix-preset") !== "custom";
}

function applySuffixPresetFromDefaults() {
  const suffixes = (defaults.allowedSuffixes || []).slice().sort().join(",");
  const presetByKey = {
    ".md": "suffix-preset-markdown",
    ".json,.md": "suffix-preset-markdown-json",
    ".json,.md,.txt": "suffix-preset-all",
  };
  const presetId = presetByKey[suffixes] || "suffix-preset-custom";
  const presetEl = document.getElementById(presetId);
  if (presetEl) presetEl.checked = true;
  const customInput = document.getElementById("allowed-suffixes");
  if (customInput) {
    customInput.value = (defaults.allowedSuffixes || []).join(",");
    customInput.disabled = presetId !== "suffix-preset-custom";
  }
}

function syncSuffixInputState() {
  const customSelected = document.getElementById("suffix-preset-custom")?.checked;
  const customInput = document.getElementById("allowed-suffixes");
  if (customInput) customInput.disabled = !customSelected;
}

function applyBuildPreset(mode) {
  const statusEl = document.getElementById("build-preset-status");
  setActivePreset("build", mode);
  const baseLocal = {
    "embedding-provider": "local",
    "embedding-model": defaults.embeddingModel,
    "embedding-device": defaults.embeddingDevice || "cpu",
    "vector-backend": "local",
    "vector-collection": defaults.vectorCollection,
    "reranker-provider": "none",
    "reranker-model": defaults.rerankerModel,
    "reranker-top-n": defaults.rerankerTopN,
  };
  Object.entries(baseLocal).forEach(([id, value]) => setValue(id, value));
  setValue("allow-low-quality", false);
  setValue("mapping-retry-missing-results", false);

  if (mode === "no_enrichment") {
    setValue("mapping-provider", "noop");
    setValue("mapping-model", "");
    setValue("mapping-template-mode", "pass1");
    setValue("mapping-batch-size", 6);
    setValue("mapping-batch-delay-ms", 0);
    setValue("mapping-text-char-limit", 350);
    setValue("force-reenrich", false);
    if (statusEl) statusEl.textContent = "Preset applied: no enrichment, local embeddings, local vector store, no reranker.";
  } else if (mode === "cached_enrichment") {
    setValue("mapping-provider", defaults.mappingProvider || "gemini");
    setValue("mapping-model", defaults.mappingModel || "heuristic-v1");
    setValue("mapping-template-mode", defaults.mappingTemplateMode || "pass1");
    setValue("mapping-batch-size", defaults.mappingBatchSize || 6);
    setValue("mapping-batch-delay-ms", defaults.mappingBatchDelayMs || 0);
    setValue("mapping-text-char-limit", defaults.mappingTextCharLimit || 350);
    setValue("mapping-retry-missing-results", defaults.mappingRetryMissingResults);
    setValue("force-reenrich", false);
    if (statusEl) statusEl.textContent = "Preset applied: provider enrichment with cache reuse. External provider calls happen only for uncached or changed blocks.";
  } else if (mode === "force_enrichment") {
    setValue("mapping-provider", defaults.mappingProvider || "gemini");
    setValue("mapping-model", defaults.mappingModel || "heuristic-v1");
    setValue("mapping-template-mode", "full");
    setValue("mapping-batch-size", Math.min(Number(defaults.mappingBatchSize || 6), 8));
    setValue("mapping-batch-delay-ms", defaults.mappingBatchDelayMs || 0);
    setValue("mapping-text-char-limit", defaults.mappingTextCharLimit || 600);
    setValue("mapping-retry-missing-results", true);
    setValue("force-reenrich", true);
    if (statusEl) statusEl.textContent = "Preset applied: force re-enrichment. This can call the mapping provider for every eligible block.";
  } else if (mode === "local_only") {
    setValue("mapping-provider", "local");
    setValue("mapping-model", "local-heuristic");
    setValue("mapping-template-mode", "pass1");
    setValue("mapping-batch-size", 16);
    setValue("mapping-batch-delay-ms", 0);
    setValue("mapping-text-char-limit", 350);
    setValue("force-reenrich", false);
    if (statusEl) statusEl.textContent = "Preset applied: local heuristic mapping with local embeddings and no external provider.";
  }
  renderBuildCommandPreview();
  renderBuildRisk();
}

function applyExperimentPreset(mode) {
  const statusEl = document.getElementById("exp-preset-status");
  setActivePreset("exp", mode);
  setValue("exp-allow-low-quality", false);
  setValue("exp-embedding-provider", "local");
  setValue("exp-embedding-model", defaults.embeddingModel);
  setValue("exp-vector-backend", "local");
  setValue("exp-reranker-provider", "none");

  if (mode === "no_enrichment") {
    setValue("exp-mapping-provider", "noop");
    setValue("exp-mapping-model", "");
    setValue("exp-force-reenrich", false);
    if (statusEl) statusEl.textContent = "Experiment preset applied: no enrichment, local embeddings, no external provider/API expected.";
  } else if (mode === "cached_enrichment") {
    setValue("exp-mapping-provider", defaults.mappingProvider || "gemini");
    setValue("exp-mapping-model", defaults.mappingModel || "heuristic-v1");
    setValue("exp-force-reenrich", false);
    if (statusEl) statusEl.textContent = "Experiment preset applied: provider enrichment with cache reuse.";
  } else if (mode === "force_enrichment") {
    setValue("exp-mapping-provider", defaults.mappingProvider || "gemini");
    setValue("exp-mapping-model", defaults.mappingModel || "heuristic-v1");
    setValue("exp-force-reenrich", true);
    if (statusEl) statusEl.textContent = "Experiment preset applied: force re-enrichment. External mapping calls are likely.";
  } else if (mode === "local_only") {
    setValue("exp-mapping-provider", "local");
    setValue("exp-mapping-model", "local-heuristic");
    setValue("exp-force-reenrich", false);
    if (statusEl) statusEl.textContent = "Experiment preset applied: local heuristic mapping, local embeddings, local vector store.";
  }
  renderExperimentBuildPreview();
  renderExperimentBuildRisk();
}

function setActivePreset(scope, mode) {
  const prefix = scope === "exp" ? "preset-exp" : "preset-build";
  const ids = {
    no_enrichment: `${prefix}-no-enrichment`,
    cached_enrichment: `${prefix}-cached-enrichment`,
    force_enrichment: `${prefix}-force-enrichment`,
    local_only: `${prefix}-local-only`,
  };
  Object.values(ids).forEach((id) => document.getElementById(id)?.classList.remove("active"));
  document.getElementById(ids[mode])?.classList.add("active");
}

function commandPreviewHtml(parts) {
  return parts.map((part, index) => {
    const escaped = escapeHtml(part);
    if (index === 0) return `<span class="code-command">${escaped}</span>`;
    return escaped.replace(/(--[a-z0-9-]+)/g, '<span class="code-flag">$1</span>')
      .replace(/(data\/[^\s<]+)/g, '<span class="code-path">$1</span>');
  }).join(" ");
}

function renderBuildCommandPreview() {
  const previewEl = document.getElementById("build-command-preview");
  if (!previewEl) return;
  const parts = [
    "okr build-index",
    `--source-dir ${stringOrNull("source-dir") || "<source>"}`,
    `--work-dir ${stringOrNull("work-dir-build") || "<work>"}`,
  ];
  const suffixes = parseSuffixes();
  if (suffixes.length) parts.push(`--allowed-suffixes ${suffixes.join(" ")}`);
  if (document.getElementById("allow-low-quality")?.checked) parts.push("--allow-low-quality");
  if (document.getElementById("force-reenrich")?.checked) parts.push("--force-reenrich");
  [
    ["--chunk-size", numberOrNull("chunk-size")],
    ["--chunk-overlap", numberOrNull("chunk-overlap")],
    ["--mapping-provider", stringOrNull("mapping-provider")],
    ["--mapping-model", stringOrNull("mapping-model")],
    ["--mapping-batch-size", numberOrNull("mapping-batch-size")],
    ["--embedding-provider", stringOrNull("embedding-provider")],
    ["--embedding-model", stringOrNull("embedding-model")],
    ["--vector-backend", stringOrNull("vector-backend")],
  ].forEach(([flag, value]) => {
    if (value !== null && value !== undefined && value !== "") parts.push(`${flag} ${value}`);
  });
  previewEl.textContent = parts.join(" ");
  renderBuildRisk();
}

function buildRisk() {
  const mappingProvider = (stringOrNull("mapping-provider") || defaults.mappingProvider || "noop").toLowerCase();
  const embeddingProvider = (stringOrNull("embedding-provider") || defaults.embeddingProvider || "local").toLowerCase();
  const forceReenrich = document.getElementById("force-reenrich")?.checked || false;
  const externalMapping = ["openai", "gemini"].includes(mappingProvider);
  const externalEmbedding = embeddingProvider === "openai";
  const risky = externalMapping || externalEmbedding || forceReenrich;
  const reasons = [];
  if (externalMapping) reasons.push(`Mapping Provider is ${mappingProvider}, so enrichment can call an external provider/API.`);
  if (externalEmbedding) reasons.push("Embedding provider is remote, so vector creation can call an external API.");
  if (forceReenrich) reasons.push("Force re-enrichment is enabled, so cached enrichment may be ignored.");
  if (!reasons.length) reasons.push("Mapping and embeddings are local/noop and Force re-enrichment is off.");
  return { risky, reasons };
}

function renderBuildRisk() {
  const el = document.getElementById("build-risk");
  if (!el) return;
  const risk = buildRisk();
  el.classList.remove("safe", "danger");
  el.classList.add(risk.risky ? "danger" : "safe");
  const label = risk.risky ? "External provider/API use before indexing" : "Cheap build settings";
  const guidance = risk.risky
    ? "Switch Mapping Provider to noop/local, Embedding Provider to local, and Force re-enrichment off before Start Indexing if you want no external calls."
    : "Start Indexing should avoid external provider/API calls with these settings.";
  el.innerHTML = `
    <strong>${label}</strong><br>
    ${risk.reasons.map((item) => `• ${item}`).join("<br>")}<br>
    <span style="display:block; margin-top:8px;">${guidance}</span>
  `;
}

function confirmBuildIfRisky() {
  const risk = buildRisk();
  if (!risk.risky) return true;
  return window.confirm(
    "This ingestion build may call an external provider/API.\n\n" +
    risk.reasons.join("\n") +
    "\n\nContinue with Start Indexing?"
  );
}

function renderExperimentBuildPreview() {
  const previewEl = document.getElementById("exp-build-preview");
  if (!previewEl) return;
  const experimentSourceDir = stringOrNull("exp-source-dir");
  const parts = [
    "okr build-index",
    `--source-dir ${experimentSourceDir || "<experiment-source-required>"}`,
    `--work-dir ${stringOrNull("exp-work-dir") || "<experiment-work>"}`,
  ];
  const suffixes = parseExperimentSuffixes();
  if (suffixes.length) parts.push(`--allowed-suffixes ${suffixes.join(" ")}`);
  if (document.getElementById("exp-allow-low-quality")?.checked) parts.push("--allow-low-quality");
  if (document.getElementById("exp-force-reenrich")?.checked) parts.push("--force-reenrich");
  [
    ["--chunk-size", numberOrNull("exp-chunk-size")],
    ["--chunk-overlap", numberOrNull("exp-chunk-overlap")],
    ["--mapping-provider", stringOrNull("exp-mapping-provider")],
    ["--mapping-model", stringOrNull("exp-mapping-model")],
    ["--embedding-provider", stringOrNull("exp-embedding-provider")],
    ["--embedding-model", stringOrNull("exp-embedding-model")],
    ["--vector-backend", stringOrNull("exp-vector-backend")],
    ["--reranker-provider", stringOrNull("exp-reranker-provider")],
  ].forEach(([flag, value]) => {
    if (value !== null && value !== undefined && value !== "") parts.push(`${flag} ${value}`);
  });
  previewEl.innerHTML = commandPreviewHtml(parts);
  renderExperimentBuildRisk();
}

function experimentBuildRisk() {
  const mappingProvider = (stringOrNull("exp-mapping-provider") || "noop").toLowerCase();
  const embeddingProvider = (stringOrNull("exp-embedding-provider") || "local").toLowerCase();
  const forceReenrich = document.getElementById("exp-force-reenrich")?.checked || false;
  const externalMapping = ["openai", "gemini"].includes(mappingProvider);
  const externalEmbedding = embeddingProvider === "openai";
  const risky = externalMapping || externalEmbedding || forceReenrich;
  const reasons = [];
  if (externalMapping) reasons.push(`Mapping Provider is ${mappingProvider}, so enrichment can call an external provider/API.`);
  if (externalEmbedding) reasons.push("Embedding provider is remote, so vector creation can call an external API.");
  if (forceReenrich) reasons.push("Force re-enrichment is enabled, so cached enrichment may be ignored.");
  if (!reasons.length) {
    reasons.push("Mapping and embeddings are local/noop and Force re-enrichment is off.");
  }
  return { risky, externalMapping, externalEmbedding, forceReenrich, reasons };
}

function renderExperimentBuildRisk() {
  const el = document.getElementById("exp-build-risk");
  if (!el) return;
  const risk = experimentBuildRisk();
  el.classList.remove("safe", "danger");
  el.classList.add(risk.risky ? "danger" : "safe");
  const label = risk.risky ? "External provider/API use before build" : "Cheap build settings";
  const guidance = risk.risky
    ? "Use Create Experiment Record for metadata only, or switch Experiment Mapping Provider to noop/local and turn Experiment Force re-enrichment off before building."
    : "Build Experiment Workspace should avoid external provider calls with these settings.";
  el.innerHTML = `
    <strong>${label}</strong><br>
    ${risk.reasons.map((item) => `• ${item}`).join("<br>")}<br>
    <span style="display:block; margin-top:8px;">${guidance}</span>
  `;
}

function confirmExperimentBuildIfRisky() {
  const risk = experimentBuildRisk();
  if (!risk.risky) return true;
  return window.confirm(
    "This experiment build may call an external provider/API.\n\n" +
    risk.reasons.join("\n") +
    "\n\nContinue with Build Experiment Workspace?"
  );
}

function slugifyExperimentHypothesis(value) {
  const slug = String(value || "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "_")
    .replace(/^_+|_+$/g, "")
    .slice(0, 48);
  return slug || "candidate";
}

function simpleExperimentHash(value) {
  const text = String(value || "").trim();
  let hash = 2166136261;
  for (let index = 0; index < text.length; index += 1) {
    hash ^= text.charCodeAt(index);
    hash = Math.imul(hash, 16777619);
  }
  return (hash >>> 0).toString(16).padStart(8, "0").slice(0, 8);
}

function experimentTimestamp() {
  const now = new Date();
  const parts = [
    now.getFullYear(),
    String(now.getMonth() + 1).padStart(2, "0"),
    String(now.getDate()).padStart(2, "0"),
    String(now.getHours()).padStart(2, "0"),
    String(now.getMinutes()).padStart(2, "0"),
    String(now.getSeconds()).padStart(2, "0"),
  ];
  return `${parts[0]}${parts[1]}${parts[2]}_${parts[3]}${parts[4]}${parts[5]}`;
}

function suggestedExperimentLayout() {
  const workDir = String(defaults.workDir || "data/work").trim();
  const slashIndex = workDir.lastIndexOf("/");
  const baseDir = slashIndex >= 0 ? workDir.slice(0, slashIndex) : ".";
  const slug = slugifyExperimentHypothesis(document.getElementById("exp-hypothesis")?.value || "");
  const hypothesisHash = simpleExperimentHash(document.getElementById("exp-hypothesis")?.value || "");
  const token = `${slug}_${experimentTimestamp()}_${hypothesisHash}`;
  return {
    experimentWorkDir: `${baseDir}/work_exp_${token}`,
    experimentSourceDir: `${baseDir}/experiment_sources/exp_${token}/raw`,
  };
}

function updateExperimentPathOriginBadge() {
  const badge = document.getElementById("exp-workdir-origin");
  if (!badge) return;
  if (experimentWorkDirManualOverride || experimentSourceDirManualOverride) {
    badge.textContent = "Path mode: custom";
    badge.classList.remove("success");
    return;
  }
  badge.textContent = "Path mode: suggested";
  badge.classList.add("success");
}

function maybeSuggestExperimentPaths(force = false) {
  const workDirEl = document.getElementById("exp-work-dir");
  const sourceDirEl = document.getElementById("exp-source-dir");
  if (!workDirEl || !sourceDirEl) return;
  const current = normalizePathValue(workDirEl.value);
  const currentSource = normalizePathValue(sourceDirEl.value);
  const canReplaceWork = force || !current || current === normalizePathValue(experimentWorkDirAutoValue) || !experimentWorkDirManualOverride;
  const canReplaceSource = force || !currentSource || currentSource === normalizePathValue(experimentSourceDirAutoValue) || !experimentSourceDirManualOverride;
  if (!canReplaceWork && !canReplaceSource) return;
  let suggestion = suggestedExperimentLayout();
  if (force && normalizePathValue(suggestion.experimentWorkDir) === current) {
    suggestion = {
      experimentWorkDir: `${suggestion.experimentWorkDir}_r`,
      experimentSourceDir: `${suggestion.experimentSourceDir}_r`,
    };
  }
  if (canReplaceWork) {
    workDirEl.value = suggestion.experimentWorkDir;
    experimentWorkDirAutoValue = suggestion.experimentWorkDir;
  }
  if (canReplaceSource) {
    sourceDirEl.value = suggestion.experimentSourceDir;
    experimentSourceDirAutoValue = suggestion.experimentSourceDir;
  }
  experimentWorkDirManualOverride = false;
  experimentSourceDirManualOverride = false;
  updateExperimentPathOriginBadge();
  renderExperimentBuildPreview();
  updateAnswerWorkspaceIndicator();
}


// -----------------------------------------------------------------------------
// Form Defaults and Configuration
// -----------------------------------------------------------------------------
function clampTopK(value) {
  const parsed = Number(value);
  if (!Number.isFinite(parsed)) return DEFAULT_TOP_K;
  return Math.min(MAX_TOP_K, Math.max(MIN_TOP_K, Math.round(parsed)));
}

function fillDefaults() {
  setValue("source-dir", defaults.sourceDir);
  setValue("work-dir-build", defaults.workDir);
  applySuffixPresetFromDefaults();
  setValue("work-dir-answer", defaults.workDir);
  renderWorkspaceOptions(defaults.workspaceOptions || [], defaults.workDir, defaults.workDir);
  setValue("work-dir-eval", defaults.workDir);
  setValue("work-dir-calibrate", defaults.workDir);
  setValue("gate-work-dir", defaults.workDir);
    setValue("human-review-work-dir", defaults.workDir);
  setValue("top-k-answer", clampTopK(defaults.topK));
  syncTopKAnswerValue();
  setValue("top-k-eval", clampTopK(defaults.topK));
  setValue("top-k-calibrate", clampTopK(defaults.topK));
  setValue("gate-top-k", clampTopK(defaults.topK));
  setValue("benchmark-eval", defaults.benchmarkPath);
  setValue("benchmark-calibrate", defaults.benchmarkPath);
  setValue("gate-benchmark-path", defaults.benchmarkPath);
  setValue("gate-min-cases", 10);
  setValue("gate-allow-low-count", "sender_type:toll-free number");
  setValue("chunk-size", defaults.chunkSize);
  setValue("chunk-overlap", defaults.chunkOverlap);
  setValue("mapping-provider", defaults.mappingProvider);
  setValue("mapping-model", defaults.mappingModel);
  setValue("mapping-batch-size", defaults.mappingBatchSize);
  setValue("mapping-batch-delay-ms", defaults.mappingBatchDelayMs);
  setValue("mapping-text-char-limit", defaults.mappingTextCharLimit);
  setValue("mapping-template-mode", defaults.mappingTemplateMode);
  setValue("mapping-retry-missing-results", defaults.mappingRetryMissingResults);
  setValue("embedding-provider", defaults.embeddingProvider);
  setValue("embedding-model", defaults.embeddingModel);
  setValue("embedding-device", defaults.embeddingDevice);
  setValue("embedding-dimensions", defaults.embeddingDimensions);
  setValue("vector-backend", defaults.vectorBackend);
  setValue("vector-collection", defaults.vectorCollection);
  setValue("qdrant-url", defaults.qdrantUrl);
  setValue("reranker-provider", defaults.rerankerProvider);
  setValue("reranker-model", defaults.rerankerModel);
  setValue("reranker-top-n", defaults.rerankerTopN);
  setValue("exp-work-dir", defaults.experimentWorkDir);
  setValue("exp-source-dir", defaults.experimentSourceDir);
  experimentWorkDirAutoValue = normalizePathValue(defaults.experimentWorkDir);
  experimentSourceDirAutoValue = normalizePathValue(defaults.experimentSourceDir);
  experimentWorkDirManualOverride = false;
  experimentSourceDirManualOverride = false;
  setValue("exp-baseline-work-dir", defaults.experimentBaselineWorkDir);
  setValue("exp-use-benchmark", false);
  setValue("exp-benchmark-path", defaults.experimentBenchmarkPath);
  setValue("exp-suffix-preset", "all_supported");
  setValue("exp-allowed-suffixes", ".md,.json,.txt");
  setValue("exp-allow-low-quality", false);
  setValue("exp-force-reenrich", false);
  setValue("exp-force-promote-without-sources", false);
  setValue("exp-mapping-provider", "noop");
  setValue("exp-mapping-model", defaults.mappingModel);
  setValue("exp-chunk-size", defaults.chunkSize);
  setValue("exp-chunk-overlap", defaults.chunkOverlap);
  setValue("exp-embedding-provider", defaults.embeddingProvider);
  setValue("exp-embedding-model", defaults.embeddingModel);
  setValue("exp-vector-backend", defaults.vectorBackend);
  setValue("exp-reranker-provider", defaults.rerankerProvider);
  syncSuffixInputState();
  syncExperimentSuffixInputState();
  renderBuildCommandPreview();
  renderExperimentBuildPreview();
  renderExperimentBuildRisk();
  renderBuildRisk();
  updateExperimentPathOriginBadge();
  updateAnswerWorkspaceIndicator();
}

function experimentBenchmarkPath() {
  const useBenchmark = document.getElementById("exp-use-benchmark")?.checked || false;
  if (!useBenchmark) return null;
  return stringOrNull("exp-benchmark-path");
}

function experimentPayloadBase() {
  return {
    source_dir: null,
    experiment_source_dir: stringOrNull("exp-source-dir"),
    experiment_work_dir: stringOrNull("exp-work-dir"),
    baseline_work_dir: stringOrNull("exp-baseline-work-dir"),
    benchmark_path: experimentBenchmarkPath(),
    content_type: selectedExperimentContentType(),
    hypothesis: document.getElementById("exp-hypothesis")?.value?.trim() || "",
    notes: document.getElementById("exp-notes")?.value?.trim() || "",
  };
}

function experimentRollbackPayload() {
  return {
    baseline_work_dir: stringOrNull("exp-baseline-work-dir"),
    backup_work_dir: stringOrNull("exp-rollback-backup-dir"),
    experiment_work_dir: stringOrNull("exp-work-dir"),
    content_type: selectedExperimentContentType(),
    hypothesis: document.getElementById("exp-hypothesis")?.value?.trim() || "",
    notes: document.getElementById("exp-notes")?.value?.trim() || "",
  };
}

async function refreshRollbackBackups(preferredPath = "") {
  const selectEl = document.getElementById("exp-rollback-backup-select");
  const statusEl = document.getElementById("exp-rollback-status");
  const baselineDir = stringOrNull("exp-baseline-work-dir");
  if (!selectEl) return;
  if (!baselineDir) {
    selectEl.innerHTML = '<option value="">Set Baseline Work Dir first</option>';
    if (statusEl) statusEl.textContent = "Set Baseline Work Dir before loading backups.";
    return;
  }
  if (statusEl) statusEl.textContent = "Loading rollback backups...";
  try {
    const payload = await request(`/experiments/backups?baseline_work_dir=${encodeURIComponent(baselineDir)}`, null, "GET");
    const backups = Array.isArray(payload.backups) ? payload.backups : [];
    if (!backups.length) {
      selectEl.innerHTML = '<option value="">No backups found</option>';
      if (statusEl) statusEl.textContent = `No backups found for ${baselineDir}.`;
      return;
    }
    selectEl.innerHTML = backups.map((item) => {
      const label = `${item.name || item.path}${item.valid ? "" : " (invalid)"}`;
      return `<option value="${escapeHtml(item.path)}" ${item.valid ? "" : "disabled"}>${escapeHtml(label)}</option>`;
    }).join("");
    const selected = preferredPath && backups.some((item) => item.path === preferredPath && item.valid)
      ? preferredPath
      : backups.find((item) => item.valid)?.path || "";
    selectEl.value = selected;
    if (selected) setValue("exp-rollback-backup-dir", selected);
    if (statusEl) statusEl.textContent = `Loaded ${backups.length} backup(s) for ${payload.baseline_work_dir || baselineDir}.`;
  } catch (error) {
    selectEl.innerHTML = '<option value="">Could not load backups</option>';
    if (statusEl) statusEl.textContent = `Could not load backups: ${error.message}`;
  }
}

function renderWorkspaceOptions(workspaces, preferredPath = "", defaultWorkDir = "") {
  const selectEl = document.getElementById("work-dir-answer-select");
  const statusEl = document.getElementById("answer-workdir-indicator");
  if (!selectEl) return;
  const ready = Array.isArray(workspaces) ? workspaces.filter((item) => item.index_ready) : [];
  if (!ready.length) {
    selectEl.innerHTML = '<option value="">No indexed workspaces found</option>';
    if (statusEl) statusEl.textContent = "Answer workspace: none found";
    return;
  }
  selectEl.innerHTML = ready.map((item) => {
    const label = `${item.name || item.path} · ${item.kind || "workspace"} · ${item.documents ?? 0} docs / ${item.blocks ?? 0} blocks`;
    return `<option value="${escapeHtml(item.path)}">${escapeHtml(label)}</option>`;
  }).join("");
  const selected = preferredPath && ready.some((item) => item.path === preferredPath)
    ? preferredPath
    : ready.some((item) => item.path === defaultWorkDir)
      ? defaultWorkDir
      : ready[0].path;
  selectEl.value = selected;
  setValue("work-dir-answer", selected);
  updateAnswerWorkspaceIndicator();
}

async function refreshWorkspaceOptions(preferredPath = "") {
  const selectEl = document.getElementById("work-dir-answer-select");
  const statusEl = document.getElementById("answer-workdir-indicator");
  if (!selectEl) return;
  try {
    const payload = await request("/workspaces", null, "GET");
    renderWorkspaceOptions(payload.workspaces || [], preferredPath, payload.default_work_dir || defaults.workDir);
  } catch (error) {
    renderWorkspaceOptions(defaults.workspaceOptions || [], preferredPath || defaults.workDir, defaults.workDir);
    if (statusEl) statusEl.textContent = "Answer workspace: loaded from page defaults";
  }
}

function experimentPayloadFromEntry(entry) {
  return {
    source_dir: null,
    experiment_source_dir: entry.experiment_source_dir || entry.source_dir || null,
    experiment_work_dir: entry.experiment_work_dir || null,
    baseline_work_dir: stringOrNull("exp-baseline-work-dir") || entry.baseline_work_dir || null,
    benchmark_path: experimentBenchmarkPath(),
    hypothesis: entry.hypothesis || "",
    notes: entry.notes || "",
  };
}

function validateExperimentPayload(payload, mode) {
  if (!payload.experiment_work_dir) {
    return "Experiment Work Dir is required. Load an experiment record first, or paste the existing work_dir.";
  }
  return "";
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function applyCuratedPromptTemplate(sourceData) {
  const template = libraryEnrichmentPromptTemplate || defaults.enrichmentPromptTemplate || "";
  const data = String(sourceData || "").trim();
  if (template.includes("{{CURATED_SOURCE_DATA}}")) {
    return template.replace("{{CURATED_SOURCE_DATA}}", data || "[PASTE CURATED SOURCE DATA HERE]");
  }
  return `${template.trim()}\n\n--- SOURCE DATA ---\n${data || "[PASTE CURATED SOURCE DATA HERE]"}`;
}

function defaultFaqSourceFactPromptTemplate() {
  return `You are creating ingestion-ready FAQ/source-fact JSON for a telecom SMS regulatory RAG system.

Final Self-Check Before Output:
- All JSON parses correctly.
- No unescaped double quotes appear inside string values.
- All quoted tokens from the source, for example \\"01\\", \\"#\\", and \\"InfoSMS\\", are preserved exactly.
- No normalization or paraphrasing of quoted substrings occurred.

Return ONLY valid JSON. Do not return Markdown, comments, prose, code fences, qa_seeds, seeds, blocks, results, enriched_text, hypothetical_questions, or BatchedEnrichmentResponse fields.

This template is different from the Prose Source Ingestion Enrichment Template. FAQ Q&A Source-Fact Ingestion Template creates source-truth JSON with top-level source_facts. It does not create enrichment batches or benchmark cases.

Pipeline context:
- The parser recognizes top-level source_facts and turns each item into retrieval text.
- The retriever uses fact_type, topic, field, value, country_iso2, applies_to, structured_fields.question, structured_fields.answer, local_aliases, source_anchor, and source_quote for lexical and semantic matching.
- FAQ source facts are source truth. Benchmark cases belong in qa_seeds or exported benchmark JSON, not here.

Accepted input format:
Q: <reviewed user-facing question>
A: <reviewed factual answer>

There may be one pair or many pairs. Treat each Q/A pair as reviewed FAQ evidence. For each pair, create one or more atomic source_facts items. Use the question as structured_fields.question and the answer as structured_fields.answer/source_quote when supported.

Canonical fact_type values:
sender_capability, registration, content_restriction, quiet_hours, routing, provisioning, encoding, other

Support status values, when applicable:
Supported, Not supported, Required, Prohibited, Unknown

Useful SMS regulatory terms, only when supported by the input:
alphanumeric sender id, sender id registration, pre-registration, unregistered sender id, content restriction, political content, promotional content, quiet hours, two-way sms, message encoding, character limit, routing, provisioning time

Required output shape:
{
  "document_title": "<clear source title>",
  "content_type": "faq_source_facts",
  "source_facts": [
{
  "fact_id": "<stable-lowercase-ascii-slug>",
  "field": "<short FAQ/source label>",
  "fact_type": "<sender_capability|registration|content_restriction|quiet_hours|routing|provisioning|encoding|other>",
  "topic": "<human-readable canonical topic>",
  "value": "<canonical answer value copied from evidence>",
  "country_iso2": "<ISO2 if known, otherwise empty string>",
  "applies_to": "<country, region, operator, product scope, or empty string>",
  "structured_fields": {
    "question": "<reviewed question>",
    "answer": "<reviewed answer supported by evidence>",
    "support_status": "<Supported|Not supported|Required|Prohibited|Unknown when applicable>",
    "sender_type": "<specific sender type when applicable>",
    "question_pattern": "faq"
  },
  "local_aliases": [],
  "source_anchor": "<short evidence label useful for retrieval>",
  "source_quote": "<short exact factual phrase from the answer/evidence>"
}
  ],
  "notes": ["Human review required before promotion."]
}

Hard rules:
1. Output top-level source_facts, not seeds and not qa_seeds.
2. Do not invent countries, ISO codes, dates, operators, restrictions, exceptions, or legal claims.
3. If a Q/A pair lacks enough evidence to create a supported fact, output a needs_human_fact source_facts item.
16. This is a lossless extraction task. Do not paraphrase or regenerate quoted substrings. All quoted values must be copied exactly with escaping preserved.

JSON String Safety Rules (Strict):
IMPORTANT: Do not change, remove, normalize, or reinterpret escaped double quotes. Preserve every escaped quote sequence exactly as backslash-double-quote in any copied value, answer, alias, or source_quote. This is a serialization requirement and a source-truth preservation requirement.

1. JSON strings must use double quotes as delimiters.
2. Any double quote that is part of the actual value, not a delimiter, must be escaped as backslash-double-quote.
3. Escaping is a STRICT serialization requirement: you must preserve escaped quotes exactly as they appear in the source; you must not normalize, simplify, or reinterpret quoted values; you must not replace backslash-double-quote with an unescaped quote under any circumstance.
4. Always preserve exact tokens from evidence, including quoted values: quote-01-endquote becomes \\"01\\", quote-hash-endquote becomes \\"#\\", quote-Verify-endquote becomes \\"Verify\\", quote-InfoSMS-endquote becomes \\"InfoSMS\\".
5. If a value contains quotes and you are unsure, keep the text exactly the same and add escaping only.
6. Invalid transformations: quote-InfoSMS-endquote becoming InfoSMS loses meaning; quote-InfoSMS-endquote becoming single-quoted InfoSMS changes format.
7. Valid JSON serialization example: "value": "such as \\"InfoSMS\\" or \\"Verify\\""
8. Escape backslashes as \\\\, preserve line breaks as \\n when needed, and never output undefined, comments, trailing commas, or half-written JSON.
9. Before finalizing, mentally run python -m json.tool on the whole response. If one character would break JSON parsing, fix it before answering.

CRITICAL: Lossless String Preservation (Hard Requirement)
This task is a LOSSLESS transformation, not a paraphrasing or normalization task.
You must preserve all string values exactly as they appear in the input evidence, including escaped characters.

Non-Negotiable Rules:
1. Treat all input text as already-correct, pre-escaped JSON-safe content.
2. Never reinterpret, normalize, or clean up quoted values.
3. Never remove quotes that appear in the source text.
4. Never convert escaped quotes into unescaped quotes.

Escaped Quote Preservation:
If the input contains \\"01\\", you must output \\"01\\".
Do not output an unescaped quote-delimited 01 token.
Do not output bare 01.

Copy-Exact Requirement:
For value, structured_fields.answer, source_quote, and local_aliases, copy substrings exactly from the input. Do not retype, rephrase, or regenerate these values.

Validation Step (Mandatory):
Before returning JSON, scan every string value. If a double quote appears inside a string, it must be escaped as backslash-double-quote. If any unescaped quote exists inside a string, fix it.

Failure Condition:
If escaped quotes are not preserved exactly, the output is invalid.

## Input Data

{{CURATED_SOURCE_DATA}}`;
}

function applyFaqPromptTemplate(sourceData) {
  const template = libraryFaqPromptTemplate || defaults.faqPromptTemplate || defaultFaqSourceFactPromptTemplate();
  const data = String(sourceData || "").trim();
  if (template.includes("{{CURATED_SOURCE_DATA}}")) {
    return template.replace("{{CURATED_SOURCE_DATA}}", data || "[PASTE REVIEWED FAQ EVIDENCE HERE]");
  }
  return `${template.trim()}\n\n--- REVIEWED FAQ EVIDENCE ---\n${data || "[PASTE REVIEWED FAQ EVIDENCE HERE]"}`;
}

function faqPromptInputPayload(sourceData) {
  const raw = String(sourceData || "").trim();
  if (!raw) return "";
  let payload = null;
  try {
    payload = { reviewed_faq_evidence_json: JSON.parse(raw) };
  } catch (_error) {
    payload = { reviewed_faq_evidence_text: raw };
  }
  return [
    "JSON-safe reviewed FAQ evidence follows. Read the escaped JSON string values normally, but copy only the escaped forms when creating output JSON.",
    "",
    JSON.stringify(payload, null, 2),
    "",
    "Do not copy any literal unescaped quote from the source text into JSON. If the evidence contains quote-delimited 01, output it inside JSON strings as \\\"01\\\".",
  ].join("\n");
}

function nextNonspaceChar(text, start) {
  for (let index = start; index < text.length; index += 1) {
    const char = text[index];
    if (!/\s/.test(char)) return char;
  }
  return "";
}

function repairJsonTextForUpload(rawText) {
  const text = String(rawText || "").trim();
  if (!text) return text;
  try {
    return JSON.stringify(JSON.parse(text), null, 2);
  } catch (_error) {
    let repaired = "";
    let inString = false;
    let escaped = false;
    for (let index = 0; index < text.length; index += 1) {
      const char = text[index];
      if (!inString) {
        repaired += char;
        if (char === '"') {
          inString = true;
          escaped = false;
        }
        continue;
      }
      if (escaped) {
        repaired += char;
        escaped = false;
        continue;
      }
      if (char === "\\") {
        repaired += char;
        escaped = true;
        continue;
      }
      if (char === '"') {
        const nextChar = nextNonspaceChar(text, index + 1);
        if ([":", ",", "}", "]"].includes(nextChar)) {
          repaired += char;
          inString = false;
        } else {
          repaired += '\\"';
        }
        continue;
      }
      repaired += char;
    }
    return repaired;
  }
}

function repairExperimentUploadContent(fileName, content) {
  return String(fileName || "").toLowerCase().endsWith(".json")
    ? repairJsonTextForUpload(content)
    : content;
}

function generateCuratedPrompt() {
  const sourceEl = document.getElementById("curated-source-data");
  const outputEl = document.getElementById("curated-ready-prompt");
  const statusEl = document.getElementById("curated-prompt-status");
  if (!sourceEl || !outputEl) return;
  outputEl.value = applyCuratedPromptTemplate(sourceEl.value);
  if (statusEl) statusEl.textContent = "Template ready.";
}

async function loadCuratedSourceFile(event) {
  const file = event?.target?.files?.[0];
  const sourceEl = document.getElementById("curated-source-data");
  const outputEl = document.getElementById("curated-ready-prompt");
  const statusEl = document.getElementById("curated-prompt-status");
  if (!file || !sourceEl) return;
  try {
    const text = await file.text();
    sourceEl.value = text;
    if (outputEl) outputEl.value = "";
    generateCuratedPrompt();
    if (statusEl) statusEl.textContent = `Loaded ${file.name}. Prose ingestion template ready.`;
  } catch (error) {
    if (statusEl) statusEl.textContent = `Could not load file: ${error.message}`;
  } finally {
    if (event?.target) event.target.value = "";
  }
}

async function refreshCuratedPromptTemplate() {
  const statusEl = document.getElementById("curated-prompt-status");
  const outputEl = document.getElementById("curated-ready-prompt");
  if (statusEl) statusEl.textContent = "Refreshing template...";
  try {
    const payload = await request(`/library/prose-source-ingestion-enrichment-prompt?ts=${Date.now()}`, null, "GET");
    libraryEnrichmentPromptTemplate = payload.template || "";
    if (outputEl) outputEl.value = "";
    if (statusEl) statusEl.textContent = libraryEnrichmentPromptTemplate
      ? "Template refreshed."
      : "Template is empty.";
  } catch (error) {
    if (statusEl) statusEl.textContent = `Could not refresh template: ${error.message}`;
  }
}

function flashButtonText(buttonId, text) {
  const button = document.getElementById(buttonId);
  if (!button) return;
  const original = button.innerHTML;
  button.textContent = text;
  window.setTimeout(() => {
    button.innerHTML = original;
  }, 1400);
}

async function copyElementText(elementId, buttonId) {
  const el = document.getElementById(elementId);
  if (!el) return;
  const text = el.innerText || el.textContent || "";
  try {
    await navigator.clipboard.writeText(text.trim());
  } catch (_error) {
    const temp = document.createElement("textarea");
    temp.value = text.trim();
    document.body.appendChild(temp);
    temp.select();
    document.execCommand("copy");
    temp.remove();
  }
  flashButtonText(buttonId, "✓");
}

async function copyCuratedPrompt() {
  const sourceEl = document.getElementById("curated-source-data");
  const outputEl = document.getElementById("curated-ready-prompt");
  const statusEl = document.getElementById("curated-prompt-status");
  if (!outputEl) return;
  if (!outputEl.value.trim()) generateCuratedPrompt();
  try {
    await navigator.clipboard.writeText(outputEl.value);
    outputEl.value = "";
    if (sourceEl) sourceEl.value = "";
    if (statusEl) statusEl.textContent = "Template copied.";
    flashButtonText("copy-curated-prompt-button", "Copied!");
  } catch (_error) {
    outputEl.focus();
    outputEl.select();
    document.execCommand("copy");
    outputEl.value = "";
    if (sourceEl) sourceEl.value = "";
    if (statusEl) statusEl.textContent = "Template selected/copied.";
    flashButtonText("copy-curated-prompt-button", "Copied!");
  }
}

function generateFaqPrompt() {
  const sourceEl = document.getElementById("faq-source-data");
  const outputEl = document.getElementById("faq-ready-prompt");
  const statusEl = document.getElementById("faq-prompt-status");
  if (!sourceEl || !outputEl) return;
  const normalizedInput = faqPromptInputPayload(sourceEl.value);
  outputEl.value = applyFaqPromptTemplate(normalizedInput);
  const usedFallback = !(libraryFaqPromptTemplate || defaults.faqPromptTemplate);
  if (!outputEl.value.trim()) {
    outputEl.value = defaultFaqSourceFactPromptTemplate().replace(
      "{{CURATED_SOURCE_DATA}}",
      normalizedInput || "[PASTE REVIEWED FAQ EVIDENCE HERE]"
    );
  }
  const normalizedQuotes = normalizedInput && normalizedInput !== sourceEl.value.trim();
  if (statusEl) statusEl.textContent = usedFallback
    ? "FAQ template ready using built-in fallback. Restart or refresh the server to load the file template."
    : normalizedQuotes
      ? "FAQ Q&A Source-Fact Ingestion Template ready. Quotes were JSON-escaped in the template."
      : "FAQ Q&A Source-Fact Ingestion Template ready.";
}

async function loadFaqSourceFile(event) {
  const file = event?.target?.files?.[0];
  const sourceEl = document.getElementById("faq-source-data");
  const outputEl = document.getElementById("faq-ready-prompt");
  const statusEl = document.getElementById("faq-prompt-status");
  if (!file || !sourceEl) return;
  try {
    const text = await file.text();
    sourceEl.value = text;
    if (outputEl) outputEl.value = "";
    generateFaqPrompt();
    if (statusEl) statusEl.textContent = `Loaded ${file.name}. FAQ template ready.`;
  } catch (error) {
    if (statusEl) statusEl.textContent = `Could not load file: ${error.message}`;
  } finally {
    if (event?.target) event.target.value = "";
  }
}

async function refreshFaqPromptTemplate() {
  const statusEl = document.getElementById("faq-prompt-status");
  const outputEl = document.getElementById("faq-ready-prompt");
  if (statusEl) statusEl.textContent = "Refreshing FAQ template...";
  try {
    const payload = await request(`/library/faq-qa-source-fact-ingestion-prompt?ts=${Date.now()}`, null, "GET");
    libraryFaqPromptTemplate = payload.template || "";
    if (outputEl) outputEl.value = "";
    if (statusEl) statusEl.textContent = libraryFaqPromptTemplate
      ? "FAQ template refreshed."
      : "FAQ template is empty.";
  } catch (error) {
    if (statusEl) statusEl.textContent = `Could not refresh FAQ template: ${error.message}`;
  }
}

async function copyFaqPrompt() {
  const sourceEl = document.getElementById("faq-source-data");
  const outputEl = document.getElementById("faq-ready-prompt");
  const statusEl = document.getElementById("faq-prompt-status");
  if (!outputEl) return;
  if (!outputEl.value.trim()) generateFaqPrompt();
  try {
    await navigator.clipboard.writeText(outputEl.value);
    outputEl.value = "";
    if (sourceEl) sourceEl.value = "";
    if (statusEl) statusEl.textContent = "FAQ template copied.";
    flashButtonText("copy-faq-prompt-button", "Copied!");
  } catch (_error) {
    outputEl.focus();
    outputEl.select();
    document.execCommand("copy");
    outputEl.value = "";
    if (sourceEl) sourceEl.value = "";
    if (statusEl) statusEl.textContent = "FAQ template selected/copied.";
    flashButtonText("copy-faq-prompt-button", "Copied!");
  }
}

function reviewDataForPrompt() {
  if (!lastAnswerPayload) return "";
  const evidence = (lastAnswerPayload.evidence || []).slice(0, 5).map((item, index) => ({
    rank: index + 1,
    document_id: item.document_id,
    block_id: item.block_id,
    block_type: item.block_type,
    score: item.score,
    title: item.title,
    section_path: item.section_path,
    raw_text: item.text,
    enriched_text: item.enriched_text,
  }));
  return JSON.stringify({
    source_kind: "answer_review_to_faq_enrichment",
    user_question: lastAnswerPayload.question,
    generated_answer: lastAnswerPayload.answer,
    review_rating: document.getElementById("review-rating")?.value || "",
    expected_document_id: document.getElementById("review-expected-document-id")?.value || "",
    expected_iso_code: document.getElementById("review-expected-iso-code")?.value || "",
    expected_terms: document.getElementById("review-expected-terms")?.value || "",
    reviewer_notes: document.getElementById("review-notes")?.value || "",
    instruction: "Create ingestion-ready FAQ source_facts JSON for this exact question pattern. Return a top-level source_facts object, not seeds or qa_seeds. Escape quotes so the JSON passes python -m json.tool. If the correct fact is missing, create a needs_human_fact entry instead of inventing it.",
    evidence,
  }, null, 2);
}

function blockDataForTemplate(evidenceIndex) {
  const item = lastAnswerPayload?.evidence?.[evidenceIndex];
  if (!item) return reviewDataForPrompt();
  return JSON.stringify({
    source_kind: "retrieved_block_to_faq_enrichment",
    user_question: lastAnswerPayload?.question || "",
    document_id: item.document_id,
    block_id: item.block_id,
    block_type: item.block_type,
    title: item.title,
    section_path: item.section_path,
    raw_text: item.text,
    enriched_text: item.enriched_text,
    hypothetical_questions: item.metadata?.semantic_hypothetical_questions || "",
    instruction: "Create one or more ingestion-ready FAQ source_facts from this block. Return a top-level source_facts object, not seeds or qa_seeds. Preserve the original fact, escape quotes correctly, and add the user wording under structured_fields.question.",
  }, null, 2);
}

function aggregateFixDataForPrompt() {
  if (!lastAnswerPayload) return "";
  const evidence = (lastAnswerPayload.evidence || []).slice(0, 12).map((item, index) => ({
    rank: index + 1,
    country: item.country || "",
    iso_code: item.iso_code || item.metadata?.tag_iso_code || "",
    document_id: item.document_id,
    block_id: item.block_id,
    block_type: item.block_type,
    score: item.score,
    title: item.title,
    section_path: item.section_path,
    raw_text: item.text,
    enriched_text: item.enriched_text,
    row_key: item.metadata?.row_key || "",
    row_values: item.metadata?.row_values || "",
    hypothetical_questions: item.metadata?.semantic_hypothetical_questions || "",
  }));
  return JSON.stringify({
    source_kind: "failed_aggregate_answer_to_curated_source_facts",
    user_question: lastAnswerPayload.question,
    query_intent: lastAnswerPayload.query_intent,
    generated_answer: lastAnswerPayload.answer,
    review_rating: document.getElementById("review-rating")?.value || "incomplete",
    expected_document_id: document.getElementById("review-expected-document-id")?.value || "",
    expected_iso_code: document.getElementById("review-expected-iso-code")?.value || "",
    expected_terms: document.getElementById("review-expected-terms")?.value || "",
    reviewer_notes: document.getElementById("review-notes")?.value || "",
    instruction: [
      "Create atomic JSON source_facts to fix this aggregate retrieval pattern.",
      "For list-style country questions, create one standalone fact per country.",
      "Preserve positive and negative polarity explicitly, for example two_way_sms_supported: true or false.",
      "Do not group countries into generic phrases like multiple countries.",
      "If the evidence is wrong or insufficient, create needs_human_fact entries instead of inventing facts."
    ].join(" "),
    evidence,
  }, null, 2);
}

function openLibraryPromptWithData(sourceData) {
  closeDrawer();
  activateTab("tab-library");
  const sourceEl = document.getElementById("curated-source-data");
  if (sourceEl) sourceEl.value = sourceData || "";
  generateCuratedPrompt();
  document.getElementById("curated-source-data")?.scrollIntoView({ behavior: "smooth", block: "center" });
}

function openLibraryFaqPromptWithData(sourceData) {
  closeDrawer();
  activateTab("tab-library");
  const sourceEl = document.getElementById("faq-source-data");
  if (sourceEl) sourceEl.value = sourceData || "";
  generateFaqPrompt();
  document.getElementById("faq-source-data")?.scrollIntoView({ behavior: "smooth", block: "center" });
}

function renderExperimentLifecycle(rows) {
  renderSummary(document.getElementById("exp-lifecycle-summary"), rows);
}

function experimentHealthOutput(health) {
  if (!health || typeof health !== "object") {
    return [
      "Ingestion health: unavailable",
      "The API response did not include ingestion_health. Restart the GUI/API server so it uses the latest experiment-health code.",
    ].join("\n");
  }
  const warnings = Array.isArray(health.warnings) ? health.warnings : [];
  const actions = Array.isArray(health.suggested_actions) ? health.suggested_actions : [];
  const lines = [
    `Ingestion health: ${health.healthy ? "healthy" : "needs work"}`,
    `Documents: ${health.documents ?? "—"} | Blocks: ${health.blocks ?? "—"} | Vectors: ${health.vector_count ?? "—"}`,
    `Structured facts: ${health.structured_fact_blocks ?? "—"} | Rejected: ${health.rejected_blocks ?? "—"}`,
    `Low quality review: ${qualityBreakdownLabel(health)}`,
  ];
  if (warnings.length) {
    lines.push("", "Warnings:");
    warnings.forEach((item) => lines.push(`- ${item}`));
  }
  if (actions.length) {
    lines.push("", "Suggested actions:");
    actions.forEach((item) => lines.push(`- ${item}`));
  }
  return lines.join("\n");
}

function qualityBreakdownLabel(health) {
  if (!health || typeof health !== "object") return "—";
  const raw = health.raw_low_quality_blocks ?? health.low_quality_blocks ?? "—";
  const accepted = health.effectively_ok_blocks ?? 0;
  const remaining = health.low_quality_blocks ?? "—";
  return `${raw} flagged | ${accepted} accepted curated facts | ${remaining} need review`;
}

function renderLowQualityReview(payload) {
  const container = document.getElementById("exp-low-quality-review");
  if (!container) return;
  lastLowQualityBlocks = Array.isArray(payload.blocks) ? payload.blocks : [];
  const header = `
    <div class="chat-message system">
      Low quality review for ${escapeHtml(payload.work_dir || "workspace")}<br>
      ${payload.raw_low_quality_blocks ?? 0} flagged · ${payload.effectively_ok_blocks ?? 0} accepted curated facts · ${payload.review_needed_blocks ?? 0} need review
    </div>
  `;
  if (!lastLowQualityBlocks.length) {
    container.innerHTML = header + '<div class="chat-message system">No remaining low-quality blocks need review.</div>';
    return;
  }
  const renderBlock = (block, index) => {
    const reasons = Array.isArray(block.reasons) ? block.reasons : [];
    const reasonHtml = reasons.map((reason) => `<span class="badge">${escapeHtml(reason)}</span>`).join("");
    const section = Array.isArray(block.section_path) && block.section_path.length
      ? block.section_path.join(" > ")
      : "(root)";
    const structuredValue = block.metadata?.structured_value || "";
    const displayText = structuredValue || block.enriched_text || block.text || "";
    return `
      <div class="choice-card">
        <input type="checkbox" disabled>
        <span>
          <strong>${escapeHtml(block.title || block.document_id || block.block_id || "Low-quality block")}</strong><br>
          <span class="help-note">${escapeHtml(block.block_type || "unknown")} · ${escapeHtml(block.document_id || "unknown doc")} · ${escapeHtml(section)}</span>
          <div style="display:flex; gap:6px; flex-wrap:wrap; margin-top:8px;">${reasonHtml}</div>
          <div style="margin-top:10px; font-size:0.85rem; line-height:1.5;">${escapeHtml(displayText).slice(0, 700)}</div>
          <div style="margin-top:10px; display:flex; gap:8px; flex-wrap:wrap;">
            <button class="secondary" type="button" style="padding:6px 10px; font-size:0.78rem;" onclick="window.createLowQualityFixTemplate(${index})">Create Fix Template</button>
          </div>
        </span>
      </div>
    `;
  };
  const previewCount = Math.min(2, lastLowQualityBlocks.length);
  const previewHtml = lastLowQualityBlocks.slice(0, previewCount).map((block, index) => renderBlock(block, index)).join("");
  const remainingHtml = lastLowQualityBlocks.length > previewCount
    ? `
      <details class="panel-details" style="margin-top:12px;">
        <summary>Show ${lastLowQualityBlocks.length - previewCount} more review blocks</summary>
        <div class="panel-body">
          ${lastLowQualityBlocks.slice(previewCount).map((block, offset) => renderBlock(block, offset + previewCount)).join("")}
        </div>
      </details>
    `
    : "";
  container.innerHTML = header + previewHtml + remainingHtml;
}

async function reviewLowQualityBlocks() {
  const payload = experimentPayloadBase();
  const validationError = validateExperimentPayload(payload, "low_quality_review");
  if (validationError) {
    setExperimentOutput(validationError);
    return;
  }
  const button = document.getElementById("exp-review-low-quality-button");
  if (button) button.disabled = true;
  setExperimentOutput("Loading low-quality block review...");
  try {
    const result = await request("/low-quality-blocks", {
      work_dir: payload.experiment_work_dir,
      limit: 50,
      include_accepted: false,
    });
    renderLowQualityReview(result);
    setExperimentOutput(
      `Low-quality block review loaded.\n` +
      `Flagged: ${result.raw_low_quality_blocks ?? 0}\n` +
      `Accepted curated facts: ${result.effectively_ok_blocks ?? 0}\n` +
      `Need review: ${result.review_needed_blocks ?? 0}\n` +
      `Showing: ${result.returned_blocks ?? 0}`
    );
  } catch (error) {
    const restartHint = error.status === 404
      ? "\n\nThe GUI is newer than the running API process. Restart the FastAPI/Uvicorn server so the /low-quality-blocks endpoint is registered."
      : "";
    setExperimentOutput(`Could not load low-quality review:\n${error.message}${restartHint}`);
  } finally {
    if (button) button.disabled = false;
  }
}

window.createLowQualityFixTemplate = (index) => {
  const block = lastLowQualityBlocks[Number(index)];
  if (!block) return;
  openLibraryPromptWithData(JSON.stringify({
    source_kind: "low_quality_block_review",
    instruction: [
      "Convert this weak or incomplete indexed block into one or more standalone English JSON source_facts.",
      "Fix the listed review reasons.",
      "Preserve factual details only; do not invent missing values.",
      "Add country_iso2, fact_type/topic, value, structured_fields, and source_anchor whenever available.",
      "If the source is truly placeholder/unknown, create an explicit fact with notes explaining the uncertainty."
    ].join(" "),
    review_reasons: block.reasons || [],
    block,
  }, null, 2));
};

function renderExperimentRegistry(entries) {
  const listEl = document.getElementById("exp-registry-list");
  const statusEl = document.getElementById("exp-registry-status");
  if (!listEl || !statusEl) return;
  if (!entries.length) {
    listEl.innerHTML = '<div class="chat-message system">No experiment records yet. Create one to start tracking builds, evaluations, and promotions.</div>';
    statusEl.textContent = "Registry is empty.";
    return;
  }
  const latestEntries = entries.slice().reverse().slice(0, 2);
  listEl.innerHTML = latestEntries.map((entry, index) => {
    const benchmarkLine = entry.benchmark_path
      ? `<span class="help-note">optional benchmark saved</span><br>`
      : "";
    return `
      <div class="choice-card">
        <input type="checkbox" ${entry.status === "promoted" ? "checked" : ""} disabled>
        <span>
          <strong>${escapeHtml(entry.experiment_id || "experiment")}</strong><br>
          <span class="help-note">${escapeHtml(entry.experiment_work_dir || "—")} → ${escapeHtml(entry.status || "draft")}</span><br>
          <span class="help-note">index: ${escapeHtml(entry.artifact_status || "unknown")} (${entry.index_documents ?? 0} docs / ${entry.index_blocks ?? 0} blocks)</span><br>
          <span class="help-note">source: ${escapeHtml(entry.experiment_source_dir || entry.source_dir || "—")}</span><br>
          ${benchmarkLine}
          <span class="help-note">${escapeHtml(entry.hypothesis || "No hypothesis recorded yet.")}</span>
          <span style="display:flex; gap:8px; flex-wrap:wrap; margin-top:10px;">
            <button class="secondary exp-load-record" type="button" data-exp-index="${index}" style="padding:6px 10px; font-size:0.78rem;">Load</button>
            <button class="secondary exp-reevaluate-record" type="button" data-exp-index="${index}" ${entry.index_ready ? "" : "disabled"} style="padding:6px 10px; font-size:0.78rem;">Re-evaluate</button>
            <button class="secondary exp-recompare-record" type="button" data-exp-index="${index}" ${entry.index_ready ? "" : "disabled"} style="padding:6px 10px; font-size:0.78rem;">Re-compare</button>
          </span>
        </span>
      </div>
    `;
  }).join("");
  listEl.querySelectorAll(".exp-load-record").forEach((button) => {
    button.addEventListener("click", () => loadExperimentRegistryEntry(latestEntries[Number(button.dataset.expIndex)]));
  });
  listEl.querySelectorAll(".exp-reevaluate-record").forEach((button) => {
    button.addEventListener("click", () => rerunExperimentEvaluation(latestEntries[Number(button.dataset.expIndex)]));
  });
  listEl.querySelectorAll(".exp-recompare-record").forEach((button) => {
    button.addEventListener("click", () => rerunExperimentComparison(latestEntries[Number(button.dataset.expIndex)]));
  });
  statusEl.textContent = `Showing the latest ${latestEntries.length} of ${entries.length} experiment record(s).`;
}

function loadExperimentRegistryEntry(entry) {
  if (!entry) return;
  const payload = experimentPayloadFromEntry(entry);
  const backupWorkDir = entry.promotion?.backup_work_dir || entry.rollback?.restored_backup_work_dir || "";
  setValue("exp-source-dir", payload.experiment_source_dir);
  setValue("exp-work-dir", payload.experiment_work_dir);
  setValue("exp-baseline-work-dir", payload.baseline_work_dir);
  setValue("exp-use-benchmark", false);
  setValue("exp-benchmark-path", entry.benchmark_path || "");
  setValue("exp-rollback-backup-dir", backupWorkDir);
  lastLoadedPromotionBackup = backupWorkDir;
  const rollbackStatus = document.getElementById("exp-rollback-status");
  if (rollbackStatus) {
    rollbackStatus.textContent = backupWorkDir
      ? "Loaded backup path from this experiment record."
      : "This experiment record has no promotion backup path.";
  }
  refreshRollbackBackups(backupWorkDir).catch(() => {});
  setValue("exp-hypothesis", payload.hypothesis);
  setValue("exp-notes", payload.notes);
  experimentWorkDirAutoValue = normalizePathValue(payload.experiment_work_dir);
  experimentSourceDirAutoValue = normalizePathValue(payload.experiment_source_dir);
  experimentWorkDirManualOverride = false;
  experimentSourceDirManualOverride = false;
  updateExperimentPathOriginBadge();
  updateAnswerWorkspaceIndicator();
  renderExperimentLifecycle([
    [entry.experiment_id || "—", "Experiment ID"],
    [entry.status || "draft", "Status"],
    [payload.experiment_work_dir || "—", "Experiment work_dir"],
    [payload.baseline_work_dir || "—", "Baseline work_dir"],
    [entry.benchmark_path ? "saved; disabled by default" : "none", "Optional benchmark"],
  ]);
  setExperimentOutput(`Loaded experiment ${entry.experiment_id || "record"} from registry.`);
}

async function rerunExperimentEvaluation(entry) {
  if (!entry) return;
  const payload = experimentPayloadFromEntry(entry);
  const validationError = validateExperimentPayload(payload, "evaluate");
  if (validationError) {
    setExperimentOutput(validationError);
    return;
  }
  setButtonsDisabled(true);
  setExperimentOutput(
    payload.benchmark_path
      ? `Re-evaluating ${entry.experiment_id || "experiment"} with benchmark ${payload.benchmark_path}...`
      : `Re-evaluating ${entry.experiment_id || "experiment"} with ingestion health only...`
  );
  try {
    const result = await request("/experiments/evaluate", {
      ...payload,
      top_k: numberOrNull("top-k-eval") || defaults.topK,
    });
    const summary = result.summary || {};
    const health = result.ingestion_health || {};
    const benchmarkRan = Boolean(result.benchmark_used);
    renderExperimentLifecycle([
      [result.experiment_id, "Experiment ID"],
      [result.status, "Status"],
      [health.healthy ? "healthy" : "needs work", "Ingestion health"],
      [health.documents ?? "—", "Documents"],
      [health.blocks ?? "—", "Blocks"],
      [health.structured_fact_blocks ?? "—", "Structured facts"],
      [qualityBreakdownLabel(health), "Low quality review"],
      [benchmarkRan ? (summary.answer_correctness ?? "—") : "not run", "Answer correctness"],
    ]);
    await refreshExperiments();
    setExperimentOutput(
      `Re-evaluation complete.\n` +
      `Experiment: ${result.experiment_id}\n` +
      `Benchmark used: ${result.benchmark_used || "none; ingestion health only"}\n` +
      `${experimentHealthOutput(health)}\n\n` +
      `Answer correctness: ${benchmarkRan ? (summary.answer_correctness ?? "—") : "not run"}`
    );
  } catch (error) {
    setExperimentOutput(`Re-evaluation failed:\n${error.message}`);
  } finally {
    setButtonsDisabled(false);
  }
}

async function rerunExperimentComparison(entry) {
  if (!entry) return;
  const payload = experimentPayloadFromEntry(entry);
  const validationError = validateExperimentPayload(payload, "compare");
  if (validationError) {
    setExperimentOutput(validationError);
    return;
  }
  setButtonsDisabled(true);
  setExperimentOutput(
    payload.benchmark_path
      ? `Re-comparing ${entry.experiment_id || "experiment"} with benchmark ${payload.benchmark_path}...`
      : `Re-comparing ${entry.experiment_id || "experiment"} with ingestion health only...`
  );
  try {
    const result = await request("/experiments/compare", {
      ...payload,
      top_k: numberOrNull("top-k-eval") || defaults.topK,
    });
    await refreshExperiments();
    setExperimentOutput(
      `Re-comparison complete.\n` +
      `Experiment: ${result.experiment_id}\n` +
      `Promotion decision: ${result.promotion_decision || "review"}\n` +
      `Δ answer_correctness: ${result.delta_metrics?.answer_correctness ?? "—"}\n` +
      `Δ country_match_at_1: ${result.delta_metrics?.country_match_at_1 ?? "—"}\n` +
      `Δ foreign_evidence_rate: ${result.delta_metrics?.foreign_evidence_rate ?? "—"}`
    );
  } catch (error) {
    setExperimentOutput(`Re-comparison failed:\n${error.message}`);
  } finally {
    setButtonsDisabled(false);
  }
}

async function refreshExperiments() {
  const payload = await request("/experiments", null, "GET");
  renderExperimentRegistry(Array.isArray(payload.entries) ? payload.entries : []);
  return payload;
}

async function clearExperimentRegistry() {
  const confirmed = window.confirm(
    "Delete all experiment registry records and registered experiment workspaces? Baseline data and staged source files will not be deleted."
  );
  if (!confirmed) return;
  const button = document.getElementById("exp-clear-registry-button");
  if (button) button.disabled = true;
  try {
    const payload = await request("/experiments/clear-registry", { delete_workspaces: true }, "POST");
    renderExperimentRegistry([]);
    setExperimentOutput(
      `Experiment registry and workspaces cleared.\n` +
      `Records deleted: ${payload.cleared_count ?? 0}\n` +
      `Workspaces deleted: ${payload.deleted_workspace_count ?? 0}\n` +
      `Workspaces skipped: ${payload.skipped_workspace_count ?? 0}\n` +
      `Registry: ${payload.registry_path}\n\n` +
      `${payload.note || "Baseline data and staged source files were left untouched."}`
    );
  } catch (error) {
    setExperimentOutput(`Could not clear experiment registry:\n${error.message}`);
  } finally {
    if (button) button.disabled = false;
  }
}

function setExperimentOutput(text) {
  const el = document.getElementById("exp-action-output");
  if (el) el.textContent = text;
}

function normalizePathValue(value) {
  return String(value || "").trim().replace(/\/+$/, "");
}

function updateAnswerWorkspaceIndicator() {
  const answerDir = normalizePathValue(document.getElementById("work-dir-answer")?.value);
  const baselineDir = normalizePathValue(document.getElementById("exp-baseline-work-dir")?.value);
  const experimentDir = normalizePathValue(document.getElementById("exp-work-dir")?.value);
  const indicatorEl = document.getElementById("answer-workdir-indicator");
  const modeEl = document.getElementById("answer-workdir-mode");
  const flagEl = document.getElementById("ask-environment-flag");
  const selectEl = document.getElementById("work-dir-answer-select");
  if (selectEl && answerDir && Array.from(selectEl.options).some((option) => normalizePathValue(option.value) === answerDir)) {
    selectEl.value = Array.from(selectEl.options).find((option) => normalizePathValue(option.value) === answerDir)?.value || selectEl.value;
  }
  if (indicatorEl) {
    indicatorEl.textContent = `Answer workspace: ${answerDir || "—"}`;
  }
  if (flagEl) {
    flagEl.classList.remove("success");
    if (answerDir && baselineDir && answerDir === baselineDir) {
      flagEl.textContent = "Test environment: baseline";
      flagEl.classList.add("success");
    } else if (answerDir && experimentDir && answerDir === experimentDir) {
      flagEl.textContent = "Test environment: experiment";
    } else {
      flagEl.textContent = "Test environment: custom";
    }
  }
  if (!modeEl) return;
  if (answerDir && baselineDir && answerDir === baselineDir) {
    modeEl.textContent = "Mode: baseline";
    modeEl.classList.add("success");
    return;
  }
  if (answerDir && experimentDir && answerDir === experimentDir) {
    modeEl.textContent = "Mode: experiment";
    modeEl.classList.remove("success");
    return;
  }
  modeEl.textContent = "Mode: custom";
  modeEl.classList.remove("success");
}

function setAskWorkspaceFromExperiment(path, label) {
  const normalized = normalizePathValue(path);
  if (!normalized) return;
  setValue("work-dir-answer", normalized);
  updateAnswerWorkspaceIndicator();
  const statusEl = document.getElementById("exp-ask-workspace-status");
  if (statusEl) statusEl.textContent = `Ask workspace: ${label} (${normalized})`;
  activateTab("tab-query");
  const questionEl = document.getElementById("question");
  if (questionEl) questionEl.focus();
}

function renderBadges(answer) {
  const el = document.getElementById("answer-badges");
  if(!el) return;
  el.innerHTML = `
    <span class="badge ${answer.tier === 'tier0' ? 'success' : ''}">Tier: ${answer.tier}</span>
    <span class="badge">Cache: ${answer.cached ? "hit" : "miss"}</span>
  `;
}

function renderAnswerDetails(answer) {
  const el = document.getElementById("answer-detail-list");
  if(!el) return;
  el.innerHTML = `
    <div class="kv"><span>Confidence</span><strong>${answer.confidence}</strong></div>
    <div class="kv"><span>Intent</span><strong>${answer.query_intent}</strong></div>
    <div class="kv"><span>Evidence blocks</span><strong>${answer.evidence.length}</strong></div>
  `;
}

function prefillReviewForm(answer) {
  lastAnswerPayload = answer;
  const statusEl = document.getElementById("review-save-status");
  if (statusEl) statusEl.textContent = "Optional: save as regression.";

  const ratingEl = document.getElementById("review-rating");
  if (ratingEl) ratingEl.value = "correct";

  const topDoc = answer.evidence && answer.evidence.length ? answer.evidence[0].document_id : "";
  const docEl = document.getElementById("review-expected-document-id");
  if (docEl) docEl.value = topDoc || "";

  const isoEl = document.getElementById("review-expected-iso-code");
  if (isoEl) {
    const inferredIso = topDoc && topDoc.includes("_") ? topDoc.split("_").slice(-1)[0].toUpperCase() : "";
    isoEl.value = inferredIso;
  }

  const termsEl = document.getElementById("review-expected-terms");
  if (termsEl) termsEl.value = "";

  const notesEl = document.getElementById("review-notes");
  if (notesEl) notesEl.value = "";
}

async function submitAnswerReview() {
  const statusEl = document.getElementById("review-save-status");
  if (!lastAnswerPayload) {
    if (statusEl) statusEl.textContent = "Ask a question first so there is an answer to review.";
    return;
  }

  const expectedTerms = (document.getElementById("review-expected-terms")?.value || "")
    .split(",")
    .map((value) => value.trim())
    .filter((value) => value);

  if (statusEl) statusEl.textContent = "Saving review...";
  try {
    const result = await request("/review-answer", {
      work_dir: document.getElementById("work-dir-answer").value,
      question: lastAnswerPayload.question,
      answer: lastAnswerPayload.answer,
      confidence: lastAnswerPayload.confidence,
      tier: lastAnswerPayload.tier,
      query_intent: lastAnswerPayload.query_intent,
      cached: Boolean(lastAnswerPayload.cached),
      rating: document.getElementById("review-rating")?.value || "correct",
      expected_document_id: document.getElementById("review-expected-document-id")?.value || "",
      expected_iso_code: document.getElementById("review-expected-iso-code")?.value || "",
      expected_terms: expectedTerms,
      notes: document.getElementById("review-notes")?.value || "",
      evidence_document_ids: (lastAnswerPayload.evidence || []).map((item) => item.document_id),
      evidence_block_ids: (lastAnswerPayload.evidence || []).map((item) => item.block_id),
    });
    if (statusEl) statusEl.textContent = `Saved review #${result.review_count} to ${result.path}`;
    refreshHumanReviewReadiness().catch(() => null);
  } catch (error) {
    if (statusEl) statusEl.textContent = `Failed to save review: ${error.message}`;
  }
}


// -----------------------------------------------------------------------------
// Evidence Drawer
// -----------------------------------------------------------------------------
function renderEvidence(evidence) {
  const el = document.getElementById("evidence-list");
  if(!el) return;
  if (!evidence.length) {
    el.innerHTML = '<div class="chat-message system">This answer did not return evidence blocks.</div>';
    return;
  }
  el.innerHTML = evidence.map((item, index) => {
    const section = item.section_path && item.section_path.length ? item.section_path.join(" > ") : "(root)";
    const blockId = item.block_id || `block_${index}`; // Fallback if block_id missing in hit

    let tagsHtml = "";
    if (item.metadata) {
      const tags = Object.entries(item.metadata).filter(([k]) => k.startsWith('tag_'));
      if (tags.length > 0) {
        tagsHtml = '<div style="margin-top: 8px; display:flex; flex-wrap:wrap; gap:6px;">' +
          tags.map(([k, v]) => `<span class="badge" style="font-size: 0.7rem; background: var(--bg-panel); border-color: #cbd5e1; color: #475569;">${k.replace('tag_', '')}: ${v}</span>`).join("") +
          '</div>';
      }
    }

    const enriched = item.enriched_text;
    const questions = item.metadata && item.metadata.semantic_hypothetical_questions;
    const intent = item.metadata && item.metadata.semantic_intent;

    let qHtml = "";
    if (questions) {
      const qList = questions.split('|').map(q => q.trim()).filter(q => q);
      if (qList.length > 0) {
        qHtml = `<div style="margin-top:12px; font-size:0.8rem; border-top:1px dashed var(--border); padding-top:8px;">
          <div style="font-weight:600; color:var(--text-muted); margin-bottom:4px;">Indexed Questions:</div>
          <ul style="margin:0; padding-left:16px; color:var(--text-muted);">
            ${qList.map(q => `<li>${q}</li>`).join("")}
          </ul>
        </div>`;
      }
    }

    return `
      <div class="evidence-card">
        <div class="evidence-meta">
          <span class="badge">#${index + 1}</span>
          <span class="badge">${item.block_type}</span>
          ${intent ? `<span class="badge success" style="background:#fef3c7; color:#92400e; border-color:#fde68a;">${intent}</span>` : ''}
          <span class="badge">score ${item.score.toFixed(4)}</span>
        </div>
        <h3 class="evidence-title">${item.title}</h3>
        <p class="evidence-text" style="font-size:0.8rem;"><strong style="color:var(--text);">Doc:</strong> ${item.document_id} | <strong style="color:var(--text);">Sec:</strong> ${section}</p>

        <div style="margin-top:12px; padding:12px; background:var(--bg-panel); border-radius:6px; border-left:4px solid var(--accent);">
          <div style="font-weight:700; font-size:0.75rem; color:var(--accent); text-transform:uppercase; margin-bottom:4px;">Enriched Fact</div>
          <p class="evidence-text" style="color:var(--text); font-weight:500;">${enriched || item.text}</p>
        </div>

        <p class="evidence-text" style="margin-top:12px; font-size:0.85rem; opacity:0.7;"><strong>Raw Text:</strong> ${item.text}</p>

        <div style="margin-top:16px; display:flex; gap:8px;">
          <button class="secondary" style="padding: 4px 12px; font-size: 0.75rem; border-color: #94a3b8;" onclick="window.inspectBlock('${blockId}')">🛠 Inspect Full Metadata</button>
          <button class="secondary" style="padding: 4px 12px; font-size: 0.75rem; border-color: #94a3b8;" onclick="window.createFaqTemplateFromBlock(${index})">FAQ Template</button>
          <button class="secondary" style="padding: 4px 12px; font-size: 0.75rem; border-color: #94a3b8;" onclick="window.createAggregateFixTemplateFromBlock(${index})">Aggregate Fix</button>
        </div>

        ${tagsHtml}
        ${qHtml}
      </div>
    `;
  }).join("");
}

async function inspectBlock(blockId) {
  if (!blockId) return;
  const section = document.getElementById("block-inspection-section");
  const content = document.getElementById("block-detail-content");
  if (!section || !content) return;

  section.style.display = "block";
  content.innerHTML = '<div class="chat-message system">Fetching deep metadata...</div>';
  const fallbackEvidence = (lastAnswerPayload?.evidence || []).find((item) => item.block_id === blockId);

  try {
    const details = await request("/explain-block", {
      block_id: blockId,
      work_dir: lastAnswerPayload?.work_dir || document.getElementById("work-dir-answer").value
    });

    let canonicalHtml = "";
    if (details.canonical_terms && details.canonical_terms.length > 0) {
      canonicalHtml = `
        <div style="margin-top:16px;">
          <div style="font-weight:600; font-size:0.8rem; color:var(--text-muted); margin-bottom:8px;">Canonical Terms (Normalized)</div>
          <div style="display:flex; flex-wrap:wrap; gap:6px;">
            ${details.canonical_terms.map(t => `<span class="badge success">${t}</span>`).join("")}
          </div>
        </div>
      `;
    }

    let aliasesHtml = "";
    if (details.local_aliases && details.local_aliases.length > 0) {
      aliasesHtml = `
        <div style="margin-top:16px;">
          <div style="font-weight:600; font-size:0.8rem; color:var(--text-muted); margin-bottom:8px;">Local Aliases (Retrieval Recall)</div>
          <div style="display:flex; flex-wrap:wrap; gap:6px;">
            ${details.local_aliases.map(a => `<span class="badge" style="background:#f1f5f9;">${a}</span>`).join("")}
          </div>
        </div>
      `;
    }

    content.innerHTML = `
      <div class="kv-list">
        <div class="kv"><span>Block ID</span><strong>${details.block_id}</strong></div>
        <div class="kv"><span>Quality</span><strong>${details.quality_status}</strong></div>
        <div class="kv"><span>Signal</span><strong>${details.answer_signal}</strong></div>
        <div class="kv"><span>Provider</span><strong>${details.enrichment_provider || "unknown"}</strong></div>
        <div class="kv"><span>Model</span><strong>${details.enrichment_model || "unknown"}</strong></div>
        <div class="kv"><span>Enriched</span><strong>${details.enriched_at || "unknown"}</strong></div>
      </div>

      <div style="margin-top:20px; padding:16px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px;">
        <div style="font-weight:700; font-size:0.75rem; color:#64748b; text-transform:uppercase; margin-bottom:8px;">Reasoning</div>
        <p style="margin:0; font-size:0.9rem; line-height:1.6; color:#334155; font-style:italic;">"${details.reasoning || "No reasoning captured for this block."}"</p>
      </div>

      ${canonicalHtml}
      ${aliasesHtml}

      <div style="margin-top:20px; border-top:1px solid var(--border); padding-top:16px;">
        <div style="font-weight:600; font-size:0.8rem; color:var(--text-muted); margin-bottom:8px;">Raw Metadata JSON</div>
        <pre style="background:#f1f5f9; padding:12px; border-radius:6px; font-size:0.75rem; overflow:auto; max-height:200px;">${JSON.stringify(details.metadata, null, 2)}</pre>
      </div>
    `;

    section.scrollIntoView({ behavior: 'smooth', block: 'start' });
  } catch (error) {
    if (fallbackEvidence) {
      const fallbackSection = fallbackEvidence.section_path && fallbackEvidence.section_path.length
        ? fallbackEvidence.section_path.join(" > ")
        : "(root)";
      content.innerHTML = `
        <div class="chat-message system" style="max-width:100%; margin-bottom:14px;">
          Deep metadata is not available for this block in the selected workspace. Showing the evidence returned with the answer.
        </div>
        <div class="kv-list">
          <div class="kv"><span>Block ID</span><strong>${escapeHtml(fallbackEvidence.block_id || "—")}</strong></div>
          <div class="kv"><span>Document</span><strong>${escapeHtml(fallbackEvidence.document_id || "—")}</strong></div>
          <div class="kv"><span>Section</span><strong>${escapeHtml(fallbackSection)}</strong></div>
          <div class="kv"><span>Score</span><strong>${fallbackEvidence.score ?? "—"}</strong></div>
        </div>
        <div style="margin-top:16px; padding:12px; background:var(--bg-panel); border-radius:6px; border-left:4px solid var(--accent);">
          <div style="font-weight:700; font-size:0.75rem; color:var(--accent); text-transform:uppercase; margin-bottom:4px;">Evidence Text</div>
          <p class="evidence-text" style="color:var(--text);">${escapeHtml(fallbackEvidence.enriched_text || fallbackEvidence.text || "")}</p>
        </div>
      `;
    } else {
      content.innerHTML = `<div class="chat-message system" style="background:#fee2e2; color:#b91c1c; border-color:#fecaca;">Block details are unavailable for ${escapeHtml(blockId)} in the selected workspace.</div>`;
    }
    section.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}

window.inspectBlock = inspectBlock;
window.createFaqTemplateFromAnswer = () => openLibraryFaqPromptWithData(reviewDataForPrompt());
window.createFaqTemplateFromBlock = (index) => openLibraryFaqPromptWithData(blockDataForTemplate(Number(index)));
window.createAggregateFixTemplateFromAnswer = () => openLibraryPromptWithData(aggregateFixDataForPrompt());
window.createAggregateFixTemplateFromBlock = (index) => {
  const blockPayload = blockDataForTemplate(Number(index));
  const aggregatePayload = aggregateFixDataForPrompt();
  openLibraryPromptWithData(JSON.stringify({
    source_kind: "single_evidence_block_from_failed_aggregate_answer",
    aggregate_context: aggregatePayload ? JSON.parse(aggregatePayload) : null,
    focused_block: blockPayload ? JSON.parse(blockPayload) : null,
  }, null, 2));
};

function renderProvenance(runtime) {
  const el = document.getElementById("provenance-list");
  if(!el) return;
  const indexed = runtime.indexed;
  const probe = runtime.model_probe || {};
  const rows = [
    ["Mapping", `${indexed.mapping_provider || "n/a"} / ${indexed.mapping_model || "n/a"}`],
    ["Embeddings", `${indexed.embedding_provider || "n/a"} / ${indexed.embedding_model || "n/a"}`],
    ["Vector backend", indexed.vector_backend || "n/a"],
    ["Reranker", `${indexed.reranker_provider || "n/a"} / ${indexed.reranker_model || "n/a"}`],
    ["Generator", `${indexed.generation_provider || "n/a"} / ${indexed.generation_model || "n/a"}`],
  ];
  renderSummary(el, rows.map(([l,v])=>[v,l]));
  const probeEl = document.getElementById("model-probe-list");
  if (probeEl) {
    const checkedModels = probe.checked_models ? Object.keys(probe.checked_models).join(", ") : "";
    renderSummary(probeEl, [
      [probe.status || "unknown", "Provider model probe"],
      [checkedModels || "none", "Checked models"],
      [probe.message || "No probe message.", "Probe note"],
    ]);
  }

  const mDocs = document.getElementById("metric-documents");
  if (mDocs) mDocs.textContent = indexed.documents;
  const mBlocks = document.getElementById("metric-blocks");
  if (mBlocks) mBlocks.textContent = indexed.blocks;
  const mBackend = document.getElementById("metric-backend");
  if (mBackend) mBackend.textContent = indexed.vector_backend || "none";
}


// -----------------------------------------------------------------------------
// API Client
// -----------------------------------------------------------------------------
async function request(path, payload, method = "POST") {
  const response = await fetch(path, {
    method,
    headers: {"Content-Type": "application/json"},
    body: method === "GET" ? undefined : JSON.stringify(payload),
  });
  const raw = await response.text();
  let data = null;
  try {
    data = raw ? JSON.parse(raw) : null;
  } catch (_error) {
    data = raw;
  }
  if (!response.ok) {
    const message = data && typeof data === "object" ? JSON.stringify(data, null, 2) : String(data || `HTTP ${response.status}`);
    const error = new Error(message);
    error.status = response.status;
    error.data = data;
    throw error;
  }
  return data;
}

function currentBuildWorkDir() {
  return stringOrNull("work-dir-build");
}

function buildLockPayload() {
  return { work_dir: currentBuildWorkDir() };
}

function buildLockDetail(error) {
  const detail = error?.data?.detail;
  if (detail && typeof detail === "object") {
    return detail;
  }
  return null;
}

function renderBuildLockConflict(error) {
  const detail = buildLockDetail(error);
  const lock = detail?.lock || {};
  const message = detail?.message || error.message;
  const staleText = lock.stale ? "This lock looks stale and can be cleared from the button below." : "This lock looks active. Wait for the build to finish or use another work_dir.";
  const rows = [
    `Build blocked by workspace lock.`,
    staleText,
    ``,
    `Reason: ${lock.reason || "unknown"}`,
    `Work dir: ${lock.work_dir || currentBuildWorkDir() || "default"}`,
    `Lock path: ${lock.path || "unknown"}`,
    `PID: ${lock.pid || "unknown"}`,
    `Age seconds: ${lock.age_seconds ?? "unknown"}`,
    ``,
    message,
  ];
  if(outputEl) outputEl.textContent = rows.join("\n");
  const clearBtn = document.getElementById("clear-build-lock-button");
  if (clearBtn) clearBtn.style.display = lock.stale ? "inline-block" : "none";
}

async function clearStaleBuildLock() {
  const clearBtn = document.getElementById("clear-build-lock-button");
  if (clearBtn) clearBtn.disabled = true;
  if(outputEl) outputEl.textContent = "Clearing stale build lock...";
  try {
    const result = await request("/build-index/clear-stale-lock", buildLockPayload());
    if(outputEl) outputEl.textContent = [
      "Stale build lock cleared.",
      `Reason: ${result.reason || "cleared"}`,
      `Lock path: ${result.path}`,
      "",
      "You can start indexing again now.",
    ].join("\n");
    if (clearBtn) clearBtn.style.display = "none";
  } catch (error) {
    if (error?.data && typeof error.data === "object") {
      if(outputEl) outputEl.textContent = `Could not clear lock:\n${JSON.stringify(error.data, null, 2)}`;
    } else {
      if(outputEl) outputEl.textContent = `Could not clear lock:\n${error.message}`;
    }
  } finally {
    if (clearBtn) clearBtn.disabled = false;
  }
}

async function refreshRuntime() {
  const runtime = await request("/runtime", null, "GET");
  renderHome(runtime);
  renderLibrary(runtime);
  renderProvenance(runtime);
  renderTesting(runtime);
  await refreshBaselineStatus().catch(() => null);
  await refreshHumanReviewReadiness().catch(() => null);
  await refreshWorkspaceOptions(stringOrNull("work-dir-answer") || runtime.work_dir || "").catch(() => null);
  return runtime;
}


// -----------------------------------------------------------------------------
// Event Bindings
// -----------------------------------------------------------------------------
const btn_ask_button = document.getElementById("ask-button");
if (btn_ask_button) btn_ask_button.addEventListener("click", async () => {
  const question = document.getElementById("question").value.trim();
    if (!question) return;
    appendMessage("user", question, "query");
    document.getElementById("question").value = "";
    document.getElementById("question").dispatchEvent(new Event("input"));
    setButtonsDisabled(true);
  try {
    const answerWorkDir = document.getElementById("work-dir-answer").value;
    const answer = await request("/answer", {
      question,
      work_dir: answerWorkDir,
      top_k: clampTopK(document.getElementById("top-k-answer").value),
    });
    answer.work_dir = answer.work_dir || answerWorkDir;

      let answerHtml = `<div class="chat-body" style="white-space:pre-wrap;">${answer.answer}</div>`;
      if (answer.evidence && answer.evidence.length > 0) {
         answerHtml += `<button class="evidence-link" type="button" onclick="window.openEvidenceDrawer()"><svg width="15" height="15" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.3-4.3M10.8 18a7.2 7.2 0 100-14.4 7.2 7.2 0 000 14.4z"></path></svg>View evidence</button>`;
      }

      const el = document.createElement("div");
      el.className = `chat-message answer`;
      el.innerHTML = `
        <div class="chat-meta verified-badge">${verifiedIconSvg()} ${escapeHtml(answer.tier)} · ${escapeHtml(answer.confidence)}</div>
        ${answerHtml}
      `;
    chatLogEl.appendChild(el);
    chatLogEl.scrollTop = chatLogEl.scrollHeight;

    renderBadges(answer);
    renderAnswerDetails(answer);
    renderEvidence(answer.evidence);
    prefillReviewForm(answer);
    await refreshRuntime().catch(() => null);
  } catch (error) {
    appendMessage("system", error.message, "error");
  } finally {
    setButtonsDisabled(false);
  }
});

  const questionInputEl = document.getElementById("question");
  if (questionInputEl && btn_ask_button) {
    const resizeQuestionInput = () => {
      questionInputEl.style.height = "auto";
      questionInputEl.style.height = `${Math.min(questionInputEl.scrollHeight, 150)}px`;
    };
    questionInputEl.addEventListener("input", resizeQuestionInput);
    resizeQuestionInput();
    questionInputEl.addEventListener("keydown", (event) => {
      if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
        event.preventDefault();
        if (!btn_ask_button.disabled) btn_ask_button.click();
      }
    });
  }

  const topKAnswerEl = document.getElementById("top-k-answer");
  const topKAnswerValueEl = document.getElementById("top-k-answer-value");
function syncTopKAnswerValue() {
  if (!topKAnswerEl) return;
  topKAnswerEl.value = String(clampTopK(topKAnswerEl.value));
  if (topKAnswerValueEl) topKAnswerValueEl.textContent = topKAnswerEl.value;
}
  if (topKAnswerEl) {
    topKAnswerEl.addEventListener("input", syncTopKAnswerValue);
    syncTopKAnswerValue();
  }

  document.querySelectorAll(".sample-question").forEach((button) => {
    button.addEventListener("click", () => {
      const questionEl = document.getElementById("question");
      if (questionEl) {
        questionEl.value = button.textContent.trim();
        questionEl.dispatchEvent(new Event("input"));
        questionEl.focus();
      }
    });
  });

const btn_answer_use_baseline_button = document.getElementById("answer-use-baseline-button");
if (btn_answer_use_baseline_button) btn_answer_use_baseline_button.addEventListener("click", () => {
  const baselineDir = stringOrNull("exp-baseline-work-dir");
  if (!baselineDir) return;
  setValue("work-dir-answer", baselineDir);
  const selectEl = document.getElementById("work-dir-answer-select");
  if (selectEl && Array.from(selectEl.options).some((option) => option.value === baselineDir)) {
    selectEl.value = baselineDir;
  }
  updateAnswerWorkspaceIndicator();
});

const btn_exp_ask_baseline_button = document.getElementById("exp-ask-baseline-button");
if (btn_exp_ask_baseline_button) btn_exp_ask_baseline_button.addEventListener("click", () => {
  setAskWorkspaceFromExperiment(stringOrNull("exp-baseline-work-dir") || defaults.workDir, "baseline");
});

const btn_exp_ask_selected_workspace_button = document.getElementById("exp-ask-selected-workspace-button");
if (btn_exp_ask_selected_workspace_button) btn_exp_ask_selected_workspace_button.addEventListener("click", () => {
  const selectEl = document.getElementById("work-dir-answer-select");
  const selected = selectEl?.value || "";
  const label = selectEl?.selectedOptions?.[0]?.textContent?.split(" · ")?.[0] || "selected";
  setAskWorkspaceFromExperiment(selected, label);
});

const btn_exp_suggest_workdir_button = document.getElementById("exp-suggest-workdir-button");
if (btn_exp_suggest_workdir_button) btn_exp_suggest_workdir_button.addEventListener("click", () => {
  maybeSuggestExperimentPaths(true);
  setExperimentOutput(`Suggested experiment path refreshed:\n${document.getElementById("exp-work-dir")?.value || "—"}`);
});

const btn_exp_upload_button = document.getElementById("exp-upload-button");
if (btn_exp_upload_button) btn_exp_upload_button.addEventListener("click", async () => {
  const filesInput = document.getElementById("exp-upload-files");
  const statusEl = document.getElementById("exp-upload-status");
  const files = Array.from(filesInput?.files || []);
  if (!files.length) {
    if (statusEl) statusEl.textContent = "Select one or more files first";
    return;
  }
  setButtonsDisabled(true);
  if (statusEl) statusEl.textContent = "Uploading files...";
  setExperimentUploadProgress(true);
  try {
    const payload = await request("/experiments/upload-files", {
      experiment_source_dir: stringOrNull("exp-source-dir"),
      hypothesis: document.getElementById("exp-hypothesis")?.value?.trim() || "",
      files: await Promise.all(
        files.map(async (file) => ({
          name: file.name,
          content: repairExperimentUploadContent(file.name, await file.text()),
        }))
      ),
    });
    setValue("exp-source-dir", payload.experiment_source_dir);
    experimentSourceDirAutoValue = normalizePathValue(payload.experiment_source_dir);
    experimentSourceDirManualOverride = false;
    updateExperimentPathOriginBadge();
    if (statusEl) {
      statusEl.textContent = `${payload.file_count} file(s) staged`;
      statusEl.classList.add("success");
    }
    renderExperimentBuildRisk();
    setExperimentOutput(
      `Experiment files uploaded.\n` +
      `Source dir: ${payload.experiment_source_dir}\n` +
      `Files: ${payload.file_count}`
    );
  } catch (error) {
    if (statusEl) statusEl.textContent = "Upload failed";
    setExperimentOutput(`Experiment file upload failed:\n${error.message}`);
  } finally {
    setExperimentUploadProgress(false);
    setButtonsDisabled(false);
  }
});

const expUploadInput = document.getElementById("exp-upload-files");
if (expUploadInput) expUploadInput.addEventListener("change", updateExperimentUploadSelectionLabel);

const expUploadZone = document.getElementById("exp-upload-zone");
if (expUploadZone && expUploadInput) {
  ["dragenter", "dragover"].forEach((eventName) => {
    expUploadZone.addEventListener(eventName, (event) => {
      event.preventDefault();
      expUploadZone.classList.add("drag-over");
    });
  });
  ["dragleave", "drop"].forEach((eventName) => {
    expUploadZone.addEventListener(eventName, (event) => {
      event.preventDefault();
      expUploadZone.classList.remove("drag-over");
    });
  });
  expUploadZone.addEventListener("drop", (event) => {
    const files = event.dataTransfer?.files;
    if (!files || !files.length) return;
    expUploadInput.files = files;
    updateExperimentUploadSelectionLabel();
  });
}

const btn_build_button = document.getElementById("build-button");
if (btn_build_button) btn_build_button.addEventListener("click", async () => {
  if (!confirmBuildIfRisky()) return;
  setButtonsDisabled(true);
  const clearBtn = document.getElementById("clear-build-lock-button");
  if (clearBtn) clearBtn.style.display = "none";
  if(outputEl) outputEl.textContent = "Starting index build process...\nThis may take a moment.";
  const loadingTimer = startLoadingTimer("build-loading", "build-loading-text", "Re-indexing...");
  let browserElapsed = 0;
  try {
    const build = await request("/build-index", {
      source_dir: stringOrNull("source-dir"),
      work_dir: stringOrNull("work-dir-build"),
      allowed_suffixes: parseSuffixes(),
      allow_low_quality: document.getElementById("allow-low-quality")?.checked || false,
      force_reenrich: document.getElementById("force-reenrich")?.checked || false,
      chunk_size: numberOrNull("chunk-size"),
      chunk_overlap: numberOrNull("chunk-overlap"),
      mapping_provider: stringOrNull("mapping-provider"),
      mapping_model: stringOrNull("mapping-model"),
      mapping_batch_size: numberOrNull("mapping-batch-size"),
      mapping_batch_delay_ms: numberOrNull("mapping-batch-delay-ms"),
      mapping_text_char_limit: numberOrNull("mapping-text-char-limit"),
      mapping_template_mode: stringOrNull("mapping-template-mode"),
      mapping_retry_missing_results: document.getElementById("mapping-retry-missing-results")?.checked ?? null,
      embedding_provider: stringOrNull("embedding-provider"),
      embedding_model: stringOrNull("embedding-model"),
      embedding_device: stringOrNull("embedding-device"),
      embedding_dimensions: numberOrNull("embedding-dimensions"),
      vector_backend: stringOrNull("vector-backend"),
      vector_collection: stringOrNull("vector-collection"),
      qdrant_url: stringOrNull("qdrant-url"),
      reranker_provider: stringOrNull("reranker-provider"),
      reranker_model: stringOrNull("reranker-model"),
      reranker_top_n: numberOrNull("reranker-top-n"),
    });
    browserElapsed = loadingTimer.stop("Re-index complete in");
    const measuredTotal = Number.isFinite(Number(build.total_time)) && Number(build.total_time) > 0
      ? Number(build.total_time)
      : browserElapsed;
    await refreshRuntime();
    if(outputEl) outputEl.textContent = `Success!
Indexed ${build.documents} docs into ${build.blocks} blocks.
Re-index time: ${formatElapsed(measuredTotal)}
Rebuilt: ${build.rebuilt_documents} | Reused: ${build.reused_documents}
Allowed suffixes: ${build.allowed_suffixes.join(", ")}
Chunking: ${build.chunk_size}/${build.chunk_overlap}
Mapping: ${build.mapping_provider} / ${build.mapping_model} (${build.mapping_template_mode}, batch ${build.mapping_batch_size})
Embeddings: ${build.embedding_provider} / ${build.embedding_model}
Vector backend: ${build.vector_backend} / ${build.vector_collection}
Reranker: ${build.reranker_provider} / ${build.reranker_model}`;
  } catch (error) {
    if (error.status === 409 && buildLockDetail(error)) {
      renderBuildLockConflict(error);
    } else if(outputEl) {
      outputEl.textContent = `Error:\n${error.message}`;
    }
  } finally {
    if (!browserElapsed) loadingTimer.stop("Re-index stopped after");
    setButtonsDisabled(false);
  }
});

const btn_clear_build_lock_button = document.getElementById("clear-build-lock-button");
if (btn_clear_build_lock_button) btn_clear_build_lock_button.addEventListener("click", clearStaleBuildLock);

const btn_exp_clear_registry_button = document.getElementById("exp-clear-registry-button");
if (btn_exp_clear_registry_button) btn_exp_clear_registry_button.addEventListener("click", clearExperimentRegistry);

const btn_exp_refresh_registry_button = document.getElementById("exp-refresh-registry-button");
if (btn_exp_refresh_registry_button) btn_exp_refresh_registry_button.addEventListener("click", async () => {
  setButtonsDisabled(true);
  try {
    await refreshExperiments();
    setExperimentOutput("Experiment history refreshed.");
  } catch (error) {
    setExperimentOutput(`Could not refresh experiment history:\n${error.message}`);
  } finally {
    setButtonsDisabled(false);
  }
});

const btn_exp_review_low_quality_button = document.getElementById("exp-review-low-quality-button");
if (btn_exp_review_low_quality_button) btn_exp_review_low_quality_button.addEventListener("click", reviewLowQualityBlocks);

[
  ["preset-build-no-enrichment", "no_enrichment"],
  ["preset-build-cached-enrichment", "cached_enrichment"],
  ["preset-build-force-enrichment", "force_enrichment"],
  ["preset-build-local-only", "local_only"],
].forEach(([id, mode]) => {
  const el = document.getElementById(id);
  if (!el) return;
  el.addEventListener("click", () => applyBuildPreset(mode));
});

[
  ["preset-exp-no-enrichment", "no_enrichment"],
  ["preset-exp-cached-enrichment", "cached_enrichment"],
  ["preset-exp-force-enrichment", "force_enrichment"],
  ["preset-exp-local-only", "local_only"],
].forEach(([id, mode]) => {
  const el = document.getElementById(id);
  if (!el) return;
  el.addEventListener("click", () => applyExperimentPreset(mode));
});

const btn_copy_exp_build_preview_button = document.getElementById("copy-exp-build-preview-button");
if (btn_copy_exp_build_preview_button) {
  btn_copy_exp_build_preview_button.addEventListener("click", () => {
    copyElementText("exp-build-preview", "copy-exp-build-preview-button");
  });
}

const btn_refresh_button = document.getElementById("refresh-button");
if (btn_refresh_button) btn_refresh_button.addEventListener("click", async () => {
  setButtonsDisabled(true);
  try { await refreshRuntime(); }
  catch (error) {}
  finally { setButtonsDisabled(false); }
});

const btn_gate_run_button = document.getElementById("gate-run-button");
if (btn_gate_run_button) btn_gate_run_button.addEventListener("click", async () => {
  setButtonsDisabled(true);
  try {
    const allowedLowCount = (document.getElementById("gate-allow-low-count").value || "")
      .split(",")
      .map((item) => item.trim())
      .filter(Boolean);
    const gate = await request("/gate/run", {
      benchmark_path: document.getElementById("gate-benchmark-path").value,
      work_dir: document.getElementById("gate-work-dir").value,
      top_k: Number(document.getElementById("gate-top-k").value),
      min_cases: Number(document.getElementById("gate-min-cases").value),
      allow_low_count: allowedLowCount,
      disable_query_cache: true,
    });
    renderSummary(document.getElementById("gate-summary"), [
      [gate.status.toUpperCase(), "Gate"],
      [gate.metrics?.answer_correctness, "Answer correctness"],
      [gate.metrics?.retrieval_recall_at_k, "Recall@k"],
      [gate.metrics?.evidence_hit_rate, "Evidence hit rate"],
      [gate.audit?.warnings?.length ?? 0, "Audit warnings"],
      [(gate.audit?.allowed_low_count_findings || []).length, "Allowed low-count"],
    ]);
    renderGateDetails(gate);
  } catch (error) {}
  finally { setButtonsDisabled(false); }
});

const btn_evaluate_button = document.getElementById("evaluate-button");
if (btn_evaluate_button) btn_evaluate_button.addEventListener("click", async () => {
  setButtonsDisabled(true);
  try {
    const summary = await request("/evaluate", {
      benchmark_path: document.getElementById("benchmark-eval").value,
      work_dir: document.getElementById("work-dir-eval").value,
      top_k: Number(document.getElementById("top-k-eval").value),
    });
    renderSummary(document.getElementById("evaluation-summary"), [
      [summary.total_cases, "Cases"],
      [summary.retrieval_recall_at_k, "Recall@k"],
      [summary.evidence_hit_rate, "Hit rate"],
      [summary.citation_accuracy, "Citation acc"],
    ]);
  } catch (error) {}
  finally { setButtonsDisabled(false); }
});

const btn_exp_create_button = document.getElementById("exp-create-button");
if (btn_exp_create_button) btn_exp_create_button.addEventListener("click", async () => {
  setButtonsDisabled(true);
  setExperimentOutput("Creating experiment record...");
  try {
    const payload = await request("/experiments/create", experimentPayloadBase());
    setValue("exp-source-dir", payload.experiment_source_dir);
    experimentSourceDirAutoValue = normalizePathValue(payload.experiment_source_dir);
    experimentSourceDirManualOverride = false;
    updateExperimentPathOriginBadge();
    renderExperimentLifecycle([
      [payload.experiment_id, "Experiment ID"],
      [payload.status, "Status"],
      [payload.experiment_source_dir, "Experiment source_dir"],
      [payload.experiment_work_dir, "Experiment work_dir"],
      [payload.baseline_work_dir, "Baseline work_dir"],
      [payload.benchmark_path || "—", "Benchmark"],
    ]);
    updateAnswerWorkspaceIndicator();
    await refreshExperiments();
    setExperimentOutput(
      `Experiment ${payload.experiment_id} saved.\n` +
      `Registry: ${payload.registry_path}\n\n` +
      `No index build was run and no provider/API call was needed for this action.`
    );
  } catch (error) {
    setExperimentOutput(`Failed to create experiment:\n${error.message}`);
  } finally {
    setButtonsDisabled(false);
  }
});

async function buildExperimentWorkspace(mergeWithBaseline) {
  if (!confirmExperimentBuildIfRisky()) return;
  setButtonsDisabled(true);
  const allowedSuffixes = experimentBuildSuffixes(mergeWithBaseline);
  setExperimentOutput(
    mergeWithBaseline
      ? "Building merged candidate incrementally...\nThis reuses baseline artifacts and rebuilds only staged experiment files."
      : "Building isolated experimental workspace...\nThis uses only staged experiment files."
  );
  const loadingTimer = startLoadingTimer(
    "exp-build-loading",
    "exp-build-loading-text",
    mergeWithBaseline ? "Building merged candidate..." : "Building experiment index..."
  );
  let browserElapsed = 0;
  try {
    const payload = await request("/experiments/build", {
      ...experimentPayloadBase(),
      merge_with_baseline: Boolean(mergeWithBaseline),
      allowed_suffixes: allowedSuffixes,
      allow_low_quality: document.getElementById("exp-allow-low-quality")?.checked || false,
      force_reenrich: document.getElementById("exp-force-reenrich")?.checked || false,
      chunk_size: numberOrNull("exp-chunk-size"),
      chunk_overlap: numberOrNull("exp-chunk-overlap"),
      mapping_provider: stringOrNull("exp-mapping-provider"),
      mapping_model: stringOrNull("exp-mapping-model"),
      embedding_provider: stringOrNull("exp-embedding-provider"),
      embedding_model: stringOrNull("exp-embedding-model"),
      vector_backend: stringOrNull("exp-vector-backend"),
      reranker_provider: stringOrNull("exp-reranker-provider"),
    });
    if (payload.experiment_source_dir) {
      setValue("exp-source-dir", payload.experiment_source_dir);
      experimentSourceDirAutoValue = normalizePathValue(payload.experiment_source_dir);
      experimentSourceDirManualOverride = false;
      updateExperimentPathOriginBadge();
    }
    const build = payload.build || {};
    browserElapsed = loadingTimer.stop("Experiment build complete in");
    const measuredTotal = Number.isFinite(Number(build.total_time)) && Number(build.total_time) > 0
      ? Number(build.total_time)
      : browserElapsed;
    renderExperimentLifecycle([
      [payload.experiment_id, "Experiment ID"],
      [payload.status, "Status"],
      [payload.experiment_source_dir || document.getElementById("exp-source-dir")?.value || "—", "Experiment source_dir"],
      [payload.merge_with_baseline ? "baseline + staged files" : "staged files only", "Build mode"],
      [payload.merge_strategy || "isolated_build", "Merge strategy"],
      [payload.build_source_dir || "—", "Build source_dir"],
      [build.documents ?? "—", "Documents"],
      [build.blocks ?? "—", "Blocks"],
      [formatElapsed(measuredTotal), "Build time"],
      [`${build.rebuilt_documents ?? 0} rebuilt / ${build.reused_documents ?? 0} reused`, "Build result"],
    ]);
    updateAnswerWorkspaceIndicator();
    await refreshExperiments();
    setExperimentOutput(
      `Experiment build complete.\n` +
      `Mode: ${payload.merge_with_baseline ? "baseline + staged files" : "staged files only"}\n` +
      `Strategy: ${payload.merge_strategy || "isolated_build"}\n` +
      `Allowed file types: ${allowedSuffixes.join(", ")}\n` +
      `Build source: ${payload.build_source_dir || "—"}\n` +
      `Docs: ${build.documents}\nBlocks: ${build.blocks}\n` +
      `Build time: ${formatElapsed(measuredTotal)}\n` +
      `Rebuilt: ${build.rebuilt_documents} | Reused: ${build.reused_documents}`
    );
  } catch (error) {
    setExperimentOutput(`Experiment build failed:\n${error.message}`);
  } finally {
    if (!browserElapsed) loadingTimer.stop("Experiment build stopped after");
    setButtonsDisabled(false);
  }
}

const btn_exp_build_button = document.getElementById("exp-build-button");
if (btn_exp_build_button) btn_exp_build_button.addEventListener("click", () => {
  buildExperimentWorkspace(false);
});

const btn_exp_build_merged_button = document.getElementById("exp-build-merged-button");
if (btn_exp_build_merged_button) btn_exp_build_merged_button.addEventListener("click", () => {
  buildExperimentWorkspace(true);
});

const btn_exp_promote_sources_button = document.getElementById("exp-promote-sources-button");
if (btn_exp_promote_sources_button) btn_exp_promote_sources_button.addEventListener("click", async () => {
  const experimentSourceDir = stringOrNull("exp-source-dir");
  if (!experimentSourceDir) {
    setExperimentOutput("Accept Sources Into Library needs an Experiment Source Dir.");
    return;
  }
  const confirmed = window.confirm(
    `Copy staged source files from ${experimentSourceDir} into the baseline source library?\n\nExisting files with the same path will be backed up before overwrite.`
  );
  if (!confirmed) return;
  setButtonsDisabled(true);
  setExperimentOutput("Accepting staged source files into the baseline source library...");
  try {
    const payload = await request("/experiments/promote-sources", experimentPayloadBase());
    renderExperimentLifecycle([
      [payload.experiment_id, "Experiment ID"],
      [payload.status, "Status"],
      [payload.baseline_source_dir, "Baseline source_dir"],
      [payload.experiment_source_dir, "Experiment source_dir"],
      [payload.promoted_source_count ?? 0, "Copied/overwritten files"],
      [payload.unchanged_count ?? 0, "Unchanged files"],
      [payload.backup_source_dir || "—", "Source backup"],
    ]);
    await refreshExperiments();
    setExperimentOutput(
      `Source promotion complete.\n` +
      `Baseline source: ${payload.baseline_source_dir}\n` +
      `Copied/overwritten: ${payload.promoted_source_count ?? 0}\n` +
      `Unchanged: ${payload.unchanged_count ?? 0}\n` +
      `Source backup: ${payload.backup_source_dir || "none needed"}\n\n` +
      `The source library is now aligned. Rebuild/promote the baseline index when you want those source files reflected in the serving index.`
    );
  } catch (error) {
    setExperimentOutput(`Source promotion failed:\n${error.message}`);
  } finally {
    setButtonsDisabled(false);
  }
});

const btn_exp_evaluate_button = document.getElementById("exp-evaluate-button");
if (btn_exp_evaluate_button) btn_exp_evaluate_button.addEventListener("click", async () => {
  const requestPayload = {
    ...experimentPayloadBase(),
    top_k: numberOrNull("top-k-eval") || defaults.topK,
  };
  const validationError = validateExperimentPayload(requestPayload, "evaluate");
  if (validationError) {
    setExperimentOutput(validationError);
    return;
  }
  setButtonsDisabled(true);
  setExperimentOutput(experimentBenchmarkPath() ? "Running experiment benchmark..." : "Running ingestion-health evaluation...");
  try {
    const payload = await request("/experiments/evaluate", requestPayload);
    const summary = payload.summary || {};
    const health = payload.ingestion_health || {};
    const benchmarkRan = Boolean(payload.benchmark_used);
    renderExperimentLifecycle([
      [payload.experiment_id, "Experiment ID"],
      [payload.status, "Status"],
      [health.healthy ? "healthy" : "needs work", "Ingestion health"],
      [health.documents ?? "—", "Documents"],
      [health.blocks ?? "—", "Blocks"],
      [health.structured_fact_blocks ?? "—", "Structured facts"],
      [qualityBreakdownLabel(health), "Low quality review"],
      [benchmarkRan ? (summary.answer_correctness ?? "—") : "not run", "Answer correctness"],
    ]);
    await refreshExperiments();
    setExperimentOutput(
      `Experiment evaluation complete.\n` +
      `Benchmark used: ${payload.benchmark_used || "none; ingestion health only"}\n` +
      `${experimentHealthOutput(health)}\n\n` +
      `Answer correctness: ${benchmarkRan ? (summary.answer_correctness ?? "—") : "not run"}`
    );
  } catch (error) {
    setExperimentOutput(`Experiment evaluation failed:\n${error.message}`);
  } finally {
    setButtonsDisabled(false);
  }
});

const btn_exp_compare_button = document.getElementById("exp-compare-button");
if (btn_exp_compare_button) btn_exp_compare_button.addEventListener("click", async () => {
  const requestPayload = {
    ...experimentPayloadBase(),
    top_k: numberOrNull("top-k-eval") || defaults.topK,
  };
  const validationError = validateExperimentPayload(requestPayload, "compare");
  if (validationError) {
    setExperimentOutput(validationError);
    return;
  }
  setButtonsDisabled(true);
  setExperimentOutput(experimentBenchmarkPath() ? "Comparing experiment against baseline benchmark..." : "Comparing ingestion health against baseline...");
  try {
    const payload = await request("/experiments/compare", requestPayload);
    await refreshExperiments();
    setExperimentOutput(
      `Comparison complete.\n` +
      `Promotion decision: ${payload.promotion_recommended ? "yes" : "no"}\n` +
      `Promotion decision: ${payload.promotion_decision || "review"}\n` +
      `\nExperiment index:\n` +
      `${experimentHealthOutput(payload.experiment_ingestion_health)}\n` +
      `\nBaseline index:\n` +
      `${experimentHealthOutput(payload.baseline_ingestion_health)}\n\n` +
      `Δ answer_correctness: ${payload.delta_metrics?.answer_correctness ?? "—"}\n` +
      `Δ country_match_at_1: ${payload.delta_metrics?.country_match_at_1 ?? "—"}\n` +
      `Δ foreign_evidence_rate: ${payload.delta_metrics?.foreign_evidence_rate ?? "—"}`
    );
  } catch (error) {
    setExperimentOutput(`Comparison failed:\n${error.message}`);
  } finally {
    setButtonsDisabled(false);
  }
});

const btn_exp_promote_button = document.getElementById("exp-promote-button");
if (btn_exp_promote_button) btn_exp_promote_button.addEventListener("click", async () => {
  const experimentDir = stringOrNull("exp-work-dir");
  const baselineDir = stringOrNull("exp-baseline-work-dir");
  if (!experimentDir || !baselineDir) return;
  const forceWithoutSources = document.getElementById("exp-force-promote-without-sources")?.checked || false;
  const confirmed = window.confirm(
    `Promote ${experimentDir} into ${baselineDir}?\n\nThe current baseline will be backed up before replacement.` +
    (forceWithoutSources ? "\n\nSource-library override is enabled." : "\n\nStaged source files must already be accepted into the baseline library.")
  );
  if (!confirmed) return;
  setButtonsDisabled(true);
  setExperimentOutput("Promoting experiment into baseline with backup...");
  try {
    const payload = await request("/experiments/promote", {
      ...experimentPayloadBase(),
      force_promote_without_sources: forceWithoutSources,
    });
    const alignment = payload.source_alignment || {};
    renderExperimentLifecycle([
      [payload.experiment_id, "Experiment ID"],
      [payload.status, "Status"],
      [payload.baseline_work_dir, "Baseline work_dir"],
      [payload.backup_work_dir || "—", "Backup work_dir"],
      [alignment.accepted ? "accepted" : alignment.override_used ? "override used" : "not accepted", "Source alignment"],
      [payload.promoted_at, "Promoted at"],
    ]);
    updateAnswerWorkspaceIndicator();
    await refreshRuntime();
    await refreshExperiments();
    setExperimentOutput(
      `Promotion complete.\n` +
      `Baseline: ${payload.baseline_work_dir}\n` +
      `Backup: ${payload.backup_work_dir || "none created"}\n` +
      `Source alignment: ${alignment.accepted ? "accepted" : alignment.override_used ? "override used" : "not accepted"}`
    );
    if (payload.backup_work_dir) {
      lastLoadedPromotionBackup = payload.backup_work_dir;
      setValue("exp-rollback-backup-dir", payload.backup_work_dir);
      refreshRollbackBackups(payload.backup_work_dir).catch(() => {});
      const rollbackStatus = document.getElementById("exp-rollback-status");
      if (rollbackStatus) rollbackStatus.textContent = "Promotion backup is ready for rollback if needed.";
    }
  } catch (error) {
    setExperimentOutput(`Promotion failed:\n${error.message}`);
  } finally {
    setButtonsDisabled(false);
  }
});

const btn_exp_refresh_backups_button = document.getElementById("exp-refresh-backups-button");
if (btn_exp_refresh_backups_button) btn_exp_refresh_backups_button.addEventListener("click", () => {
  refreshRollbackBackups(lastLoadedPromotionBackup || stringOrNull("exp-rollback-backup-dir") || "").catch(() => {});
});

const btn_refresh_baseline_status_button = document.getElementById("refresh-baseline-status-button");
if (btn_refresh_baseline_status_button) btn_refresh_baseline_status_button.addEventListener("click", async () => {
  setButtonsDisabled(true);
  try {
    await refreshBaselineStatus();
    await refreshRollbackBackups(lastLoadedPromotionBackup || stringOrNull("exp-rollback-backup-dir") || "");
  } catch (error) {}
  finally { setButtonsDisabled(false); }
});

const btn_human_review_refresh_button = document.getElementById("human-review-refresh-button");
if (btn_human_review_refresh_button) btn_human_review_refresh_button.addEventListener("click", async () => {
  setButtonsDisabled(true);
  try { await refreshHumanReviewReadiness(); }
  catch (error) {}
  finally { setButtonsDisabled(false); }
});

const btn_human_review_collect_button = document.getElementById("human-review-collect-button");
if (btn_human_review_collect_button) btn_human_review_collect_button.addEventListener("click", openReviewCollection);

const btn_human_review_export_button = document.getElementById("human-review-export-button");
if (btn_human_review_export_button) btn_human_review_export_button.addEventListener("click", async () => {
  setButtonsDisabled(true);
  try { await exportHumanReviewBenchmark(); }
  catch (error) {}
  finally { setButtonsDisabled(false); }
});

const exp_rollback_backup_select = document.getElementById("exp-rollback-backup-select");
if (exp_rollback_backup_select) exp_rollback_backup_select.addEventListener("change", () => {
  const selected = exp_rollback_backup_select.value;
  if (selected) {
    setValue("exp-rollback-backup-dir", selected);
    lastLoadedPromotionBackup = selected;
    const statusEl = document.getElementById("exp-rollback-status");
    if (statusEl) statusEl.textContent = "Selected rollback backup.";
  }
});

const work_dir_answer_select = document.getElementById("work-dir-answer-select");
if (work_dir_answer_select) work_dir_answer_select.addEventListener("change", () => {
  const selected = work_dir_answer_select.value;
  if (selected) {
    setValue("work-dir-answer", selected);
    updateAnswerWorkspaceIndicator();
  }
});

const btn_refresh_workspaces_button = document.getElementById("refresh-workspaces-button");
if (btn_refresh_workspaces_button) btn_refresh_workspaces_button.addEventListener("click", async () => {
  await refreshWorkspaceOptions(stringOrNull("work-dir-answer") || defaults.workDir);
});

const btn_exp_rollback_button = document.getElementById("exp-rollback-button");
if (btn_exp_rollback_button) btn_exp_rollback_button.addEventListener("click", async () => {
  const payloadBase = experimentRollbackPayload();
  if (!payloadBase.baseline_work_dir || !payloadBase.backup_work_dir) {
    setExperimentOutput("Rollback needs both Baseline Work Dir and Backup Work Dir.");
    return;
  }
  const confirmed = window.confirm(
    `Rollback ${payloadBase.baseline_work_dir} from ${payloadBase.backup_work_dir}?\n\nThe current baseline will be backed up before restore.`
  );
  if (!confirmed) return;
  setButtonsDisabled(true);
  setExperimentOutput("Rolling back baseline from backup...");
  try {
    const payload = await request("/experiments/rollback", payloadBase);
    renderExperimentLifecycle([
      [payload.experiment_id, "Experiment ID"],
      [payload.status, "Status"],
      [payload.baseline_work_dir, "Baseline work_dir"],
      [payload.restored_backup_work_dir, "Restored backup"],
      [payload.current_baseline_backup_work_dir || "—", "Current baseline backup"],
      [payload.rolled_back_at, "Rolled back at"],
    ]);
    updateAnswerWorkspaceIndicator();
    await refreshRuntime();
    await refreshExperiments();
    await refreshRollbackBackups(payload.current_baseline_backup_work_dir || "");
    setExperimentOutput(
      `Rollback complete.\n` +
      `Baseline: ${payload.baseline_work_dir}\n` +
      `Restored backup: ${payload.restored_backup_work_dir}\n` +
      `Previous current baseline saved as: ${payload.current_baseline_backup_work_dir || "none created"}`
    );
  } catch (error) {
    setExperimentOutput(`Rollback failed:\n${error.message}`);
  } finally {
    setButtonsDisabled(false);
  }
});

const btn_calibrate_button = document.getElementById("calibrate-button");
if (btn_calibrate_button) btn_calibrate_button.addEventListener("click", async () => {
  setButtonsDisabled(true);
  try {
    const report = await request("/calibrate-refusal", {
      benchmark_path: document.getElementById("benchmark-calibrate").value,
      work_dir: document.getElementById("work-dir-calibrate").value,
      top_k: Number(document.getElementById("top-k-calibrate").value),
    });
    renderSummary(document.getElementById("calibration-summary"), [
      [report.recommended_min_score_threshold, "Min score thres"],
      [report.recommended_min_overlap_ratio, "Min overlap"],
    ]);
  } catch (error) {}
  finally { setButtonsDisabled(false); }
});

const btn_submit_review_button = document.getElementById("submit-review-button");
if (btn_submit_review_button) btn_submit_review_button.addEventListener("click", async () => {
  await submitAnswerReview();
});

const btn_review_to_faq_template_button = document.getElementById("review-to-faq-prompt-button");
if (btn_review_to_faq_template_button) btn_review_to_faq_template_button.addEventListener("click", () => {
  openLibraryFaqPromptWithData(reviewDataForPrompt());
});

const btn_aggregate_fix_template_button = document.getElementById("aggregate-fix-prompt-button");
if (btn_aggregate_fix_template_button) btn_aggregate_fix_template_button.addEventListener("click", () => {
  openLibraryPromptWithData(aggregateFixDataForPrompt());
});

const btn_generate_curated_template_button = document.getElementById("generate-curated-prompt-button");
if (btn_generate_curated_template_button) btn_generate_curated_template_button.addEventListener("click", generateCuratedPrompt);

const btn_copy_curated_template_button = document.getElementById("copy-curated-prompt-button");
if (btn_copy_curated_template_button) btn_copy_curated_template_button.addEventListener("click", copyCuratedPrompt);

const btn_refresh_curated_template_template_button = document.getElementById("refresh-curated-prompt-template-button");
if (btn_refresh_curated_template_template_button) btn_refresh_curated_template_template_button.addEventListener("click", refreshCuratedPromptTemplate);

const curated_source_file = document.getElementById("curated-source-file");
if (curated_source_file) curated_source_file.addEventListener("change", loadCuratedSourceFile);

const btn_generate_faq_template_button = document.getElementById("generate-faq-prompt-button");
if (btn_generate_faq_template_button) btn_generate_faq_template_button.addEventListener("click", generateFaqPrompt);

const btn_copy_faq_template_button = document.getElementById("copy-faq-prompt-button");
if (btn_copy_faq_template_button) btn_copy_faq_template_button.addEventListener("click", copyFaqPrompt);

const btn_refresh_faq_template_template_button = document.getElementById("refresh-faq-prompt-template-button");
if (btn_refresh_faq_template_template_button) btn_refresh_faq_template_template_button.addEventListener("click", refreshFaqPromptTemplate);

const faq_source_file = document.getElementById("faq-source-file");
if (faq_source_file) faq_source_file.addEventListener("change", loadFaqSourceFile);

const btn_library_focus_curated_template_button = document.getElementById("library-focus-curated-prompt-button");
if (btn_library_focus_curated_template_button) btn_library_focus_curated_template_button.addEventListener("click", () => {
  const target = document.getElementById("curated-source-data");
  if (target) {
    target.scrollIntoView({behavior: "smooth", block: "center"});
    target.focus();
  }
});

[
  "source-dir",
  "work-dir-build",
  "allowed-suffixes",
  "allow-low-quality",
  "force-reenrich",
  "chunk-size",
  "chunk-overlap",
  "mapping-provider",
  "mapping-model",
  "mapping-batch-size",
  "embedding-provider",
  "embedding-model",
  "vector-backend",
  "reranker-provider",
  "reranker-model",
].forEach((id) => {
  const el = document.getElementById(id);
  if (!el) return;
  el.addEventListener("input", () => {
    renderBuildCommandPreview();
    renderBuildRisk();
  });
  el.addEventListener("change", () => {
    renderBuildCommandPreview();
    renderBuildRisk();
  });
});

[
  "exp-work-dir",
  "exp-source-dir",
  "exp-hypothesis",
  "exp-suffix-preset",
  "exp-allowed-suffixes",
  "exp-allow-low-quality",
  "exp-force-reenrich",
  "exp-mapping-provider",
  "exp-mapping-model",
  "exp-chunk-size",
  "exp-chunk-overlap",
  "exp-embedding-provider",
  "exp-embedding-model",
  "exp-vector-backend",
  "exp-reranker-provider",
].forEach((id) => {
  const el = document.getElementById(id);
  if (!el) return;
  el.addEventListener("input", renderExperimentBuildPreview);
  el.addEventListener("change", renderExperimentBuildPreview);
});

[
  "work-dir-answer",
  "exp-work-dir",
  "exp-baseline-work-dir",
].forEach((id) => {
  const el = document.getElementById(id);
  if (!el) return;
  el.addEventListener("input", updateAnswerWorkspaceIndicator);
  el.addEventListener("change", () => {
    updateAnswerWorkspaceIndicator();
    if (id === "exp-baseline-work-dir") {
      refreshBaselineStatus().catch(() => {});
      refreshRollbackBackups().catch(() => {});
    }
  });
});

const expHypothesisEl = document.getElementById("exp-hypothesis");
if (expHypothesisEl) {
  expHypothesisEl.addEventListener("input", () => maybeSuggestExperimentPaths(false));
  expHypothesisEl.addEventListener("change", () => maybeSuggestExperimentPaths(false));
}

const expWorkDirEl = document.getElementById("exp-work-dir");
if (expWorkDirEl) {
  expWorkDirEl.addEventListener("input", () => {
    const current = normalizePathValue(expWorkDirEl.value);
    experimentWorkDirManualOverride = current !== normalizePathValue(experimentWorkDirAutoValue);
    updateExperimentPathOriginBadge();
  });
  expWorkDirEl.addEventListener("change", () => {
    const current = normalizePathValue(expWorkDirEl.value);
    experimentWorkDirManualOverride = current !== normalizePathValue(experimentWorkDirAutoValue);
    updateExperimentPathOriginBadge();
  });
}

const expSourceDirEl = document.getElementById("exp-source-dir");
if (expSourceDirEl) {
  expSourceDirEl.addEventListener("input", () => {
    const current = normalizePathValue(expSourceDirEl.value);
    experimentSourceDirManualOverride = current !== normalizePathValue(experimentSourceDirAutoValue);
    updateExperimentPathOriginBadge();
  });
  expSourceDirEl.addEventListener("change", () => {
    const current = normalizePathValue(expSourceDirEl.value);
    experimentSourceDirManualOverride = current !== normalizePathValue(experimentSourceDirAutoValue);
    updateExperimentPathOriginBadge();
  });
}

document.querySelectorAll('input[name="suffix-preset"]').forEach((el) => {
  el.addEventListener("change", () => {
    syncSuffixInputState();
    renderBuildCommandPreview();
    renderExperimentBuildPreview();
  });
});

const expSuffixPresetEl = document.getElementById("exp-suffix-preset");
if (expSuffixPresetEl) {
  expSuffixPresetEl.addEventListener("change", () => {
    syncExperimentSuffixInputState();
    renderExperimentBuildPreview();
  });
}

document.querySelectorAll('input[name="exp-content-type"]').forEach((el) => {
  el.addEventListener("change", syncExperimentContentType);
});


// -----------------------------------------------------------------------------
// Boot
// -----------------------------------------------------------------------------
fillDefaults();
syncExperimentContentType();
renderBaselineStatus();
generateCuratedPrompt();
maybeSuggestExperimentPaths(false);
refreshRuntime().catch(() => {});
refreshExperiments().catch(() => {});
