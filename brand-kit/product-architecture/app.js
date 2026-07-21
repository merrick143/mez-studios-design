import { mountLivingCores } from "../source-pack/design-system-export/mz-core.js";

const MANIFEST_URL = "./manifest.json";
const CATALOGUE_URL = "../gradient-library/catalogue.json";
const STATIC_BASE = "../../gradient-library/assets/static/";
const WINGS_URL = "../../source-pack/design-system-export/assets/wings.svg";
const SOURCE_BASE = "../gradient-library/source-masters/";

let manifest;
let currentDecision = null;
let selections = { products: {}, legacyMappings: {} };

const wingsMarkup = () => `<img src="../source-pack/design-system-export/assets/wings.svg" alt="">`;

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function resetSelections() {
  selections = {
    products: Object.fromEntries(manifest.products.map((product) => [product.productId, product.recommendedGradient])),
    legacyMappings: Object.fromEntries(manifest.legacyMappings.map((row) => [row.legacySlug, row.recommendedDisposition])),
  };
}

function renderFamilyPreview() {
  document.querySelector("#family-preview").innerHTML = manifest.products.map((product) => `
    <article class="family-mark">
      <div class="family-mark__core" data-family-core="${escapeHtml(product.productId)}" data-mz-core="${escapeHtml(selections.products[product.productId])}" data-shape="disc">${wingsMarkup()}</div>
      <strong>${escapeHtml(product.publicName)}</strong>
      <span data-family-gradient="${escapeHtml(product.productId)}">${escapeHtml(selections.products[product.productId])}</span>
    </article>`).join("");
}

function renderRoster() {
  document.querySelector("#roster").innerHTML = manifest.products.map((product) => `
    <article class="roster-row">
      <h3>${escapeHtml(product.publicName)}<span>${escapeHtml(product.function)}</span></h3>
      <code class="machine-id">${escapeHtml(product.productId)}</code>
      <p class="roster-copy">${escapeHtml(product.summary)}</p>
      <span class="state state--${escapeHtml(product.gradientState)}">${escapeHtml(product.gradientState)}</span>
    </article>`).join("");
}

function renderLegacy() {
  document.querySelector("#legacy-list").innerHTML = manifest.legacyMappings.map((row) => `
    <article class="legacy-row">
      <span class="legacy-name">${escapeHtml(row.legacyName)}</span>
      <span class="legacy-arrow">Historical product name → migration disposition</span>
      <select class="legacy-select" data-legacy="${escapeHtml(row.legacySlug)}" aria-label="${escapeHtml(row.legacyName)} disposition">
        ${row.options.map((option) => `<option value="${escapeHtml(option.id)}" ${option.id === selections.legacyMappings[row.legacySlug] ? "selected" : ""}>${escapeHtml(option.label)}</option>`).join("")}
      </select>
    </article>`).join("");
}

function renderAssignments() {
  document.querySelector("#assignment-list").innerHTML = manifest.products.map((product, index) => {
    const selected = selections.products[product.productId];
    const className = product.gradientOptions.length > 3 ? "gradient-options gradient-options--five" : "gradient-options";
    return `<article class="assignment-row">
      <div class="assignment-copy">
        <span class="index">0${index + 1}</span>
        <h3>${escapeHtml(product.publicName)}</h3>
        <p>${escapeHtml(product.summary)}</p>
        <code>${escapeHtml(product.gradientState)} · ${escapeHtml(product.productId)}</code>
      </div>
      <div class="${className}" role="radiogroup" aria-label="${escapeHtml(product.publicName)} gradient">
        ${product.gradientOptions.map((option) => `<button class="gradient-option ${option.id === selected ? "is-selected" : ""}" type="button" role="radio" aria-checked="${option.id === selected}" data-product="${escapeHtml(product.productId)}" data-gradient="${escapeHtml(option.id)}" ${product.gradientState === "locked" ? "disabled" : ""}>
          <span class="gradient-option__stage">
            <span class="gradient-option__check">✓</span>
            <span class="gradient-option__core" data-mz-core="${escapeHtml(option.id)}" data-shape="disc">${wingsMarkup()}</span>
            <img class="gradient-option__source" src="${SOURCE_BASE}${escapeHtml(option.id)}.png" alt="Exact ${escapeHtml(option.id)} source">
          </span>
          <strong>${escapeHtml(option.id)}</strong>
          <em>${escapeHtml(option.label)}</em>
          <p>${escapeHtml(option.reason)}</p>
        </button>`).join("")}
      </div>
    </article>`;
  }).join("");
}

function renderSummary() {
  const productRows = manifest.products.map((product) => `<div class="summary-row"><strong>${escapeHtml(product.publicName)}</strong><span>${escapeHtml(selections.products[product.productId])}</span></div>`).join("");
  const legacyRows = manifest.legacyMappings.map((row) => {
    const option = row.options.find((item) => item.id === selections.legacyMappings[row.legacySlug]);
    return `<div class="summary-row"><strong>${escapeHtml(row.legacyName)}</strong><span>${escapeHtml(option?.label || "Unresolved")}</span></div>`;
  }).join("");
  document.querySelector("#review-summary").innerHTML = productRows + legacyRows;
}

function updateFamilyCore(productId, gradientId) {
  const element = document.querySelector(`[data-family-core="${CSS.escape(productId)}"]`);
  if (element && window.mezRenderer) window.mezRenderer.setCore(element, gradientId);
  document.querySelector(`[data-family-gradient="${CSS.escape(productId)}"]`).textContent = gradientId;
}

function isRecommended() {
  return manifest.products.every((product) => selections.products[product.productId] === product.recommendedGradient)
    && manifest.legacyMappings.every((row) => selections.legacyMappings[row.legacySlug] === row.recommendedDisposition);
}

function buildDecision(verdict) {
  const now = new Date().toISOString();
  return {
    schemaVersion: "1.0.0",
    studyId: manifest.studyId,
    exportedAt: now,
    complete: true,
    verdict,
    productionAuthority: false,
    mutatesCanonicalAuthority: false,
    sourceExpressionApproved: false,
    finishProfile: manifest.finishProfile,
    products: manifest.products.map((product) => ({
      productId: product.productId,
      slug: product.slug,
      publicName: product.publicName,
      function: product.function,
      gradientId: selections.products[product.productId],
      priorReference: product.historicalSource,
      assignmentState: product.gradientState === "locked" ? "locked" : "selected-for-migration",
    })),
    legacyMappings: manifest.legacyMappings.map((row) => ({
      legacySlug: row.legacySlug,
      legacyName: row.legacyName,
      disposition: selections.legacyMappings[row.legacySlug],
    })),
    overallNote: document.querySelector("#overall-note").value.trim(),
    nextAction: "Record DEC-PRODUCT-ARCHITECTURE-001 and update products plus gradients atomically in the internal migration control plane.",
  };
}

async function saveDecision(verdict) {
  const decision = buildDecision(verdict);
  const response = await fetch("/api/product-architecture-decisions", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(decision),
  });
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error || "Decision could not be saved");
  currentDecision = payload.decision;
  document.querySelector("#decision-status").textContent = verdict === "approve"
    ? "Recommended product system approved and saved locally."
    : "Edited product system saved locally.";
  document.querySelector("#export-decision").disabled = false;
}

async function loadDecision() {
  try {
    const response = await fetch("/api/product-architecture-decisions", { cache: "no-store" });
    if (!response.ok) throw new Error();
    currentDecision = (await response.json()).decision;
    if (!currentDecision) return;
    currentDecision.products.forEach((product) => { selections.products[product.productId] = product.gradientId; });
    currentDecision.legacyMappings.forEach((row) => { selections.legacyMappings[row.legacySlug] = row.disposition; });
    document.querySelector("#overall-note").value = currentDecision.overallNote || "";
    document.querySelector("#decision-status").textContent = `${currentDecision.verdict} decision already saved locally.`;
    document.querySelector("#export-decision").disabled = false;
  } catch {
    document.querySelector("#decision-status").textContent = "Static review active. Run brand-kit/server.py to save the decision.";
  }
}

function downloadDecision() {
  if (!currentDecision) return;
  const blob = new Blob([`${JSON.stringify(currentDecision, null, 2)}\n`], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "mez-product-architecture-gradient-assignment-01.json";
  document.body.append(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

function bindInteractions() {
  document.querySelector("#assignment-list").addEventListener("click", (event) => {
    const button = event.target.closest(".gradient-option:not(:disabled)");
    if (!button) return;
    const productId = button.dataset.product;
    selections.products[productId] = button.dataset.gradient;
    button.parentElement.querySelectorAll(".gradient-option").forEach((item) => {
      const selected = item === button;
      item.classList.toggle("is-selected", selected);
      item.setAttribute("aria-checked", String(selected));
    });
    updateFamilyCore(productId, button.dataset.gradient);
    renderSummary();
    currentDecision = null;
    document.querySelector("#export-decision").disabled = true;
    document.querySelector("#decision-status").textContent = "Selection changed. Save when ready.";
  });

  document.querySelector("#legacy-list").addEventListener("change", (event) => {
    const select = event.target.closest("[data-legacy]");
    if (!select) return;
    selections.legacyMappings[select.dataset.legacy] = select.value;
    renderSummary();
    currentDecision = null;
    document.querySelector("#export-decision").disabled = true;
    document.querySelector("#decision-status").textContent = "Selection changed. Save when ready.";
  });

  document.querySelector("#approve-recommended").addEventListener("click", async () => {
    resetSelections();
    renderLegacy();
    document.querySelectorAll(".gradient-option").forEach((button) => {
      const selected = selections.products[button.dataset.product] === button.dataset.gradient;
      button.classList.toggle("is-selected", selected);
      button.setAttribute("aria-checked", String(selected));
    });
    manifest.products.forEach((product) => updateFamilyCore(product.productId, product.recommendedGradient));
    renderSummary();
    try { await saveDecision("approve"); }
    catch (error) { document.querySelector("#decision-status").textContent = error.message; }
  });

  document.querySelector("#decision-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    try { await saveDecision(isRecommended() ? "approve" : "edit"); }
    catch (error) { document.querySelector("#decision-status").textContent = error.message; }
  });

  document.querySelector("#reset-recommended").addEventListener("click", () => {
    resetSelections();
    renderLegacy();
    document.querySelectorAll(".gradient-option").forEach((button) => {
      const selected = selections.products[button.dataset.product] === button.dataset.gradient;
      button.classList.toggle("is-selected", selected);
      button.setAttribute("aria-checked", String(selected));
    });
    manifest.products.forEach((product) => updateFamilyCore(product.productId, product.recommendedGradient));
    renderSummary();
    currentDecision = null;
    document.querySelector("#export-decision").disabled = true;
    document.querySelector("#decision-status").textContent = "Recommendations restored. Review not yet recorded.";
  });

  document.querySelector("#export-decision").addEventListener("click", downloadDecision);
}

async function initialise() {
  const [manifestResponse, catalogueResponse] = await Promise.all([fetch(MANIFEST_URL), fetch(CATALOGUE_URL)]);
  if (!manifestResponse.ok || !catalogueResponse.ok) throw new Error("Product architecture sources failed to load");
  manifest = await manifestResponse.json();
  resetSelections();
  await loadDecision();
  renderFamilyPreview();
  renderRoster();
  renderLegacy();
  renderAssignments();
  renderSummary();
  bindInteractions();

  const catalogue = await catalogueResponse.json();
  const query = new URLSearchParams(location.search);
  const result = await mountLivingCores(document, {
    catalogue,
    staticBaseUrl: STATIC_BASE,
    wingsUrl: WINGS_URL,
    forceStatic: query.has("static"),
    disableWebGL: query.has("no-webgl"),
  });
  window.mezRenderer = result.renderer;
  document.documentElement.dataset.livingCoreMode = result.mode;
  document.documentElement.dataset.livingCoreCount = String(result.count);
}

initialise().catch((error) => {
  console.error("Product architecture review failed", error);
  document.documentElement.dataset.livingCoreMode = "failed";
  document.querySelector("#decision-status").textContent = error.message;
});
