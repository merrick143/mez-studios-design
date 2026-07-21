import { mountLivingCore, mountLivingCores } from "./source-pack/design-system-export/mz-core.js";

const CATALOGUE_URL = "./source-pack/design-system-export/gradients.json";
const CLAUDE_CATALOGUE_URL = "./source-pack/claude-catalogue.json";
// The renderer resolves these against its own module URL, not this page.
const STATIC_BASE = "./assets/gradients/";
const WINGS_URL = "./assets/wings.svg";

const candidateForm = document.querySelector("#candidate-form");
const sourceInput = document.querySelector("#candidate-source");
const fileNote = document.querySelector("#file-note");
const statusNode = document.querySelector("#candidate-status");
const resultsNode = document.querySelector("#candidate-results");

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

async function mountCores() {
  try {
    const [response, claudeResponse] = await Promise.all([
      fetch(CATALOGUE_URL),
      fetch(CLAUDE_CATALOGUE_URL),
    ]);
    if (!response.ok) throw new Error(`Catalogue returned ${response.status}`);
    if (!claudeResponse.ok) throw new Error(`Claude catalogue returned ${claudeResponse.status}`);
    const [catalogue, claudeCatalogue] = await Promise.all([response.json(), claudeResponse.json()]);
    const result = await mountLivingCores(document, {
      catalogue,
      staticBaseUrl: STATIC_BASE,
      wingsUrl: WINGS_URL,
    });
    const claudeElement = document.querySelector("[data-claude-core]");
    const claudeRenderer = claudeElement
      ? await mountLivingCore(claudeElement, claudeElement.dataset.claudeCore, {
          catalogue: claudeCatalogue,
          staticBaseUrl: STATIC_BASE,
          wingsUrl: WINGS_URL,
          shape: claudeElement.dataset.shape || "sphere",
        })
      : null;
    const modes = [result.mode, claudeRenderer?.isStaticMode() ? "static" : "live"];
    document.documentElement.dataset.livingCoreMode = modes.includes("static") ? "mixed" : "live";
    document.documentElement.dataset.livingCoreCount = String(result.count + (claudeRenderer ? 1 : 0));
  } catch (error) {
    console.error("Living Core workbench failed", error);
    document.documentElement.dataset.livingCoreMode = "failed";
  }
}

function setActiveNavigation() {
  const links = Array.from(document.querySelectorAll(".rail nav a"));
  const sections = links
    .map((link) => document.querySelector(link.getAttribute("href")))
    .filter(Boolean);
  const observer = new IntersectionObserver(
    (entries) => {
      const visible = entries
        .filter((entry) => entry.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
      if (!visible) return;
      links.forEach((link) => {
        link.classList.toggle("is-active", link.getAttribute("href") === `#${visible.target.id}`);
      });
    },
    { rootMargin: "-20% 0px -68% 0px", threshold: [0, 0.2, 0.6] },
  );
  sections.forEach((section) => observer.observe(section));
}

function bytesToBase64(bytes) {
  const chunk = 0x8000;
  let binary = "";
  for (let index = 0; index < bytes.length; index += chunk) {
    binary += String.fromCharCode(...bytes.subarray(index, index + chunk));
  }
  return btoa(binary);
}

function decisionDownload(decision) {
  const blob = new Blob([`${JSON.stringify(decision, null, 2)}\n`], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `${decision.candidateId.toLowerCase()}-decision.json`;
  document.body.append(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

async function saveDecision(slug, verdict, note) {
  const response = await fetch("/api/decisions", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ slug, verdict, note }),
  });
  const result = await response.json();
  if (!response.ok) throw new Error(result.error || "Decision could not be saved");
  return result.decision;
}

function renderCandidates(rows) {
  resultsNode.replaceChildren();
  if (!rows.length) return;
  rows.forEach((row) => {
    const candidate = row.candidate;
    const existing = row.decision;
    const article = document.createElement("article");
    article.className = "candidate-result";
    article.dataset.slug = row.slug;
    article.innerHTML = `
      <div class="candidate-result__head">
        <div>
          <h3>${escapeHtml(candidate.product)} · ${escapeHtml(candidate.candidateId)}</h3>
          <p>Research only · exact source + parametric expressions</p>
        </div>
        <span>${existing ? `Decision: ${escapeHtml(existing.verdict)}` : "Undecided"}</span>
      </div>
      <iframe src="${escapeHtml(row.previewUrl)}" title="${escapeHtml(candidate.product)} candidate plate" loading="lazy"></iframe>
      <div class="decision-bar">
        <button type="button" data-verdict="select">Select</button>
        <button type="button" data-verdict="edit">Edit</button>
        <button type="button" data-verdict="reject">Reject</button>
        <input type="text" aria-label="Decision note" placeholder="What should change?" value="${escapeHtml(existing?.note || "")}">
        <button type="button" class="button button--secondary" data-export ${existing ? "" : "disabled"}>Export JSON</button>
      </div>`;
    let currentDecision = existing;
    const note = article.querySelector(".decision-bar input");
    const exportButton = article.querySelector("[data-export]");
    if (existing) article.querySelector(`[data-verdict="${existing.verdict}"]`)?.classList.add("is-selected");
    article.querySelectorAll("[data-verdict]").forEach((button) => {
      button.addEventListener("click", async () => {
        try {
          article.querySelectorAll("[data-verdict]").forEach((item) => item.classList.remove("is-selected"));
          button.classList.add("is-selected");
          currentDecision = await saveDecision(row.slug, button.dataset.verdict, note.value);
          exportButton.disabled = false;
          article.querySelector(".candidate-result__head > span").textContent = `Decision: ${currentDecision.verdict}`;
        } catch (error) {
          statusNode.textContent = error.message;
        }
      });
    });
    exportButton.addEventListener("click", () => {
      if (currentDecision) decisionDownload(currentDecision);
    });
    resultsNode.append(article);
  });
}

async function loadCandidates() {
  try {
    const response = await fetch("/api/candidates", { cache: "no-store" });
    if (!response.ok) throw new Error("Local API unavailable");
    const payload = await response.json();
    statusNode.textContent = "Local candidate workspace ready. Canonical files are isolated.";
    renderCandidates(payload.candidates || []);
  } catch {
    statusNode.textContent = "Static preview active. Run brand-kit/server.py locally to generate candidates.";
  }
}

sourceInput.addEventListener("change", () => {
  const file = sourceInput.files?.[0];
  fileNote.textContent = file
    ? `${file.name} · ${(file.size / 1024 / 1024).toFixed(2)} MB`
    : "Square PNG, JPEG or WebP · 512px minimum · 16 MB maximum";
});

candidateForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = new FormData(candidateForm);
  const file = form.get("source");
  if (!(file instanceof File) || !file.size) return;
  const submit = candidateForm.querySelector("button[type='submit']");
  submit.disabled = true;
  statusNode.textContent = "Extracting palette and generating the animated plate…";
  try {
    const bytes = new Uint8Array(await file.arrayBuffer());
    const response = await fetch("/api/candidates", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        product: form.get("product"),
        candidateId: form.get("candidateId"),
        filename: file.name,
        base64: bytesToBase64(bytes),
      }),
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "Candidate generation failed");
    statusNode.textContent = `${result.candidate.candidateId} generated without canonical changes.`;
    await loadCandidates();
    resultsNode.scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (error) {
    statusNode.textContent = error.message;
  } finally {
    submit.disabled = false;
  }
});

mountCores();
setActiveNavigation();
loadCandidates();
