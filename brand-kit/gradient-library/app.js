import { mountLivingCores } from "../source-pack/design-system-export/mz-core.js";

const CATALOGUE_URL = "./catalogue.json";
const MANIFEST_URL = "./library-manifest.json";
const ASSIGNMENTS_URL = "./assignments.json";
const APPROVAL_URL = "./approval.json";
// Renderer URLs resolve against mz-core.js, while markup URLs resolve against this page.
const STATIC_BASE = "../../gradient-library/assets/static/";
const RENDERER_WINGS_URL = "./assets/wings.svg";
const MARK_WINGS_URL = "../source-pack/design-system-export/assets/wings.svg";

const catalogueNode = document.querySelector("#catalogue");
const searchNode = document.querySelector("#search");
const filtersNode = document.querySelector("#filters");
const productNode = document.querySelector("#decision-product");
const noteNode = document.querySelector("#decision-note");
const statusNode = document.querySelector("#decision-status");
const exportNode = document.querySelector("#export-decision");

let catalogue;
let manifest;
let assignments;
let approval;
let renderer;
let selectedId = "MZ-G01";
let activeFilter = "all";
let decisions = [];
let currentDecision = null;

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function duplicateMap() {
  const result = new Map();
  manifest.duplicateIdGroups.forEach((group) => group.forEach((id) => result.set(id, group)));
  return result;
}

function assignmentMap() {
  return new Map(assignments.products.filter((row) => row.gradient).map((row) => [row.gradient, row]));
}

function renderMetrics() {
  document.querySelector("#active-count").textContent = manifest.activeCount;
  document.querySelector("#metric-active").textContent = manifest.activeCount;
  document.querySelector("#metric-sources").textContent = manifest.sourceCount;
  document.querySelector("#metric-unique").textContent = manifest.uniqueVisualCount;
  document.querySelector("#metric-duplicates").textContent = Object.keys(manifest.aliases).length;
  filtersNode.querySelector('[data-filter="all"] span').textContent = manifest.activeCount;
}

function renderCatalogue() {
  const duplicates = duplicateMap();
  const assigned = assignmentMap();
  catalogueNode.innerHTML = manifest.ids.map((id) => {
    const source = manifest.sources.find((row) => row.id === id);
    const alias = duplicates.get(id);
    const aliasOf = manifest.aliases[id];
    const product = assigned.get(id);
    const flags = [
      aliasOf ? `<span class="flag">Alias of ${aliasOf}</span>` : (alias ? `<span class="flag">Canonical ×${alias.length}</span>` : ""),
      product ? `<span class="flag flag--assigned">${escapeHtml(product.name)}</span>` : "",
      source.quality !== "pass" ? '<span class="flag flag--warning">Accepted source</span>' : "",
    ].join("");
    return `<button class="core-card" type="button" data-id="${id}" data-active="${!aliasOf}" data-duplicate="${Boolean(aliasOf)}" data-assigned="${Boolean(product)}" data-quality="${source.quality}">
      <span class="core-card__visual"><span class="core-card__disc" data-mz-core="${id}" data-shape="disc"><img class="wings" src="${MARK_WINGS_URL}" alt=""></span></span>
      <span class="core-card__meta"><strong>${id}</strong><span>${product ? escapeHtml(product.name) : "Unassigned"}</span></span>
      <span class="core-card__flags">${flags}</span>
    </button>`;
  }).join("");
}

function renderProductOptions() {
  productNode.innerHTML = [
    '<option value="library-curation">Library curation</option>',
    ...assignments.products.map((row) => `<option value="${row.slug}">${escapeHtml(row.name)}</option>`),
  ].join("");
}

function findDecision() {
  return decisions.find((row) => row.gradientId === selectedId && row.productContext === productNode.value) || null;
}

function showDecision() {
  currentDecision = findDecision();
  noteNode.value = currentDecision?.note || "";
  document.querySelectorAll("[data-verdict]").forEach((button) => {
    button.classList.toggle("is-selected", button.dataset.verdict === currentDecision?.verdict);
  });
  exportNode.disabled = !currentDecision;
  statusNode.textContent = currentDecision
    ? `${currentDecision.verdict} recorded for ${selectedId} · ${productNode.selectedOptions[0].textContent}.`
    : "Local decisions do not change product assignments.";
}

function selectGradient(id, shouldScroll = false) {
  selectedId = id;
  const core = Object.values(catalogue.cores).find((row) => row.id === id);
  const source = manifest.sources.find((row) => row.id === id);
  const aliases = duplicateMap().get(id);
  const assigned = assignmentMap().get(id);
  document.querySelectorAll(".core-card").forEach((card) => {
    card.classList.toggle("is-selected", card.dataset.id === id);
    card.setAttribute("aria-pressed", String(card.dataset.id === id));
  });
  document.querySelector("#selected-id").textContent = id;
  document.querySelector("#selected-status").textContent = assigned ? `${assigned.name} · ${assigned.state}` : "Unassigned library core";
  const image = document.querySelector("#source-master");
  image.src = `./source-masters/${id}.png`;
  image.alt = `${id} source gradient`;
  const acceptedException = approval.scope.sourceException?.id === id;
  document.querySelector("#source-dimensions").textContent = `${source.width} × ${source.height} PNG · ${source.quality === "pass" ? "source passes" : (acceptedException ? "accepted source exception" : "below 512px minimum")}`;
  document.querySelector("#source-hash").textContent = `SHA ${source.sha256.slice(0, 16)}…`;
  document.querySelector("#source-alias").textContent = aliases ? `Identical source: ${aliases.join(" · ")}` : "Unique source image";
  document.querySelector("#swatches").innerHTML = [...core.anchors.map((anchor) => anchor.hex), core.shade]
    .map((hex) => `<i style="background:${hex}" title="${hex}"></i>`).join("");
  document.querySelectorAll("[data-inspector-core]").forEach((element) => renderer.setCore(element, id));
  showDecision();
  history.replaceState(null, "", `#${id.toLowerCase()}`);
  if (shouldScroll && matchMedia("(max-width: 900px)").matches) {
    document.querySelector("#inspector").scrollIntoView({ behavior: "smooth", block: "start" });
  }
}

function applyFilters() {
  const query = searchNode.value.trim().toUpperCase();
  document.querySelectorAll(".core-card").forEach((card) => {
    const matchesQuery = !query || card.dataset.id.includes(query);
    const matchesFilter = (activeFilter === "all" && card.dataset.active === "true")
      || (activeFilter === "duplicate" && card.dataset.duplicate === "true")
      || (activeFilter === "assigned" && card.dataset.assigned === "true")
      || (activeFilter === "quality" && card.dataset.quality !== "pass");
    card.hidden = !(matchesQuery && matchesFilter);
  });
}

function downloadDecision(decision) {
  const blob = new Blob([`${JSON.stringify(decision, null, 2)}\n`], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `${decision.productContext}--${decision.gradientId.toLowerCase()}--decision.json`;
  document.body.append(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

async function loadDecisions() {
  try {
    const response = await fetch("/api/library-decisions", { cache: "no-store" });
    if (!response.ok) throw new Error();
    decisions = (await response.json()).decisions || [];
  } catch {
    decisions = [];
    statusNode.textContent = "Static review active. Run brand-kit/server.py to save decisions.";
  }
}

async function saveDecision(verdict) {
  const response = await fetch("/api/library-decisions", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ gradientId: selectedId, productContext: productNode.value, verdict, note: noteNode.value }),
  });
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error || "Decision could not be saved");
  decisions = decisions.filter((row) => !(row.gradientId === selectedId && row.productContext === productNode.value));
  decisions.push(payload.decision);
  showDecision();
}

async function initialise() {
  const responses = await Promise.all([fetch(CATALOGUE_URL), fetch(MANIFEST_URL), fetch(ASSIGNMENTS_URL), fetch(APPROVAL_URL)]);
  if (responses.some((response) => !response.ok)) throw new Error("Gradient library data failed to load");
  [catalogue, manifest, assignments, approval] = await Promise.all(responses.map((response) => response.json()));
  renderMetrics();
  renderCatalogue();
  applyFilters();
  renderProductOptions();
  await loadDecisions();
  const query = new URLSearchParams(location.search);
  const result = await mountLivingCores(document, {
    catalogue,
    staticBaseUrl: STATIC_BASE,
    wingsUrl: RENDERER_WINGS_URL,
    forceStatic: query.has("static"),
    disableWebGL: query.has("no-webgl"),
  });
  renderer = result.renderer;
  document.documentElement.dataset.livingCoreMode = result.mode;
  document.documentElement.dataset.livingCoreCount = String(result.count);
  const hashId = location.hash.slice(1).toUpperCase();
  selectGradient(manifest.ids.includes(hashId) ? hashId : manifest.ids[0]);
}

catalogueNode.addEventListener("click", (event) => {
  const card = event.target.closest(".core-card");
  if (card) selectGradient(card.dataset.id, true);
});
searchNode.addEventListener("input", applyFilters);
filtersNode.addEventListener("click", (event) => {
  const button = event.target.closest("[data-filter]");
  if (!button) return;
  activeFilter = button.dataset.filter;
  filtersNode.querySelectorAll("[data-filter]").forEach((item) => item.classList.toggle("is-active", item === button));
  applyFilters();
});
productNode.addEventListener("change", showDecision);
document.querySelector("#decision-actions").addEventListener("click", async (event) => {
  const button = event.target.closest("[data-verdict]");
  if (!button) return;
  try { await saveDecision(button.dataset.verdict); }
  catch (error) { statusNode.textContent = error.message; }
});
exportNode.addEventListener("click", () => { if (currentDecision) downloadDecision(currentDecision); });

initialise().catch((error) => {
  console.error("Gradient library failed", error);
  document.documentElement.dataset.livingCoreMode = "failed";
});
