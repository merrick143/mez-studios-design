/** Mez Systems · Product Card 02 · Round 10 controller. */
import { mountLivingCores } from "../../../source-pack/design-system-export/mz-core.js";
import { productViewModel, buildLibrary, specimenCount } from "./card-components.js";

const query = new URLSearchParams(location.search);
const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
const forceStatic = query.has("static") || reduced;
const disableWebGL = query.has("no-webgl");
const legacyDecisions = JSON.parse(localStorage.getItem("mz-product-card-r10") || "{}");
const savedReview = JSON.parse(localStorage.getItem("mz-product-card-r10-review") || "{}");
const state = {
  decisions: savedReview.decisions || legacyDecisions,
  specimenNotes: savedReview.specimenNotes || {},
  familyNotes: savedReview.familyNotes || {},
  family: savedReview.family || "undecided",
  note: savedReview.note || ""
};
let renderer = null;
let activeSurface = null;
let observer = null;
const visibility = new Map();

async function fetchJson(url) {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`${url} failed: ${response.status}`);
  return response.json();
}

function setCoreMode(text) {
  document.querySelectorAll("[data-core-mode]").forEach(node => node.textContent = `Core mode: ${text}`);
}

function renderLibrary(nodes) {
  nodes.forEach(node => document.querySelector(`[data-mount="${node.dataset.specimenFamily}"]`).append(node));
}

function persistReview() {
  localStorage.setItem("mz-product-card-r10", JSON.stringify(state.decisions));
  localStorage.setItem("mz-product-card-r10-review", JSON.stringify(state));
}

function updateSummary() {
  const summary = document.querySelector("[data-review-summary]");
  summary.innerHTML = "";
  ["keep", "revise", "kill"].forEach(verdict => {
    const item = document.createElement("div");
    item.innerHTML = `<strong>${Object.values(state.decisions).filter(value => value === verdict).length}</strong><span>${verdict}</span>`;
    summary.append(item);
  });
  const notes = [...Object.values(state.specimenNotes), ...Object.values(state.familyNotes), state.note].filter(value => value?.trim()).length;
  const item = document.createElement("div");
  item.innerHTML = `<strong>${notes}</strong><span>notes</span>`;
  summary.append(item);
}

function updateReview() {
  ["keep", "revise", "kill"].forEach(verdict => {
    document.querySelectorAll(`[data-verdict="${verdict}"]`).forEach(button => {
      const id = button.closest("[data-specimen-id]").dataset.specimenId;
      button.setAttribute("aria-pressed", String(state.decisions[id] === verdict));
    });
  });
  document.querySelectorAll("[data-specimen-id]").forEach(node => node.dataset.selectedVerdict = state.decisions[node.dataset.specimenId] || "");
  updateSummary();
  persistReview();
}

function hydrateFeedback() {
  document.querySelectorAll("[data-specimen-note]").forEach(input => {
    input.value = state.specimenNotes[input.dataset.specimenNote] || "";
    input.dataset.hasNote = String(Boolean(input.value.trim()));
  });
  document.querySelectorAll("[data-family-note]").forEach(input => {
    input.value = state.familyNotes[input.dataset.familyNote] || "";
    input.dataset.hasNote = String(Boolean(input.value.trim()));
  });
  document.querySelector("[data-family-choice]").value = state.family;
  document.querySelector("[data-review-note]").value = state.note;
}

function bindReview() {
  const panel = document.querySelector("#review-panel");
  const trigger = document.querySelector("[data-review-open]");
  const toggle = open => {
    document.body.classList.toggle("is-reviewing", open);
    panel.setAttribute("aria-hidden", String(!open));
    trigger.setAttribute("aria-expanded", String(open));
  };
  document.addEventListener("click", event => {
    const verdict = event.target.closest("[data-verdict]");
    if (verdict) {
      const id = verdict.closest("[data-specimen-id]").dataset.specimenId;
      state.decisions[id] = state.decisions[id] === verdict.dataset.verdict ? "" : verdict.dataset.verdict;
      updateReview();
    }
    if (event.target.closest("[data-review-open]")) toggle(true);
    if (event.target.closest("[data-review-close]")) toggle(false);
  });
  document.addEventListener("input", event => {
    if (event.target.matches("[data-specimen-note]")) {
      state.specimenNotes[event.target.dataset.specimenNote] = event.target.value;
      event.target.dataset.hasNote = String(Boolean(event.target.value.trim()));
      persistReview();
      updateSummary();
    }
    if (event.target.matches("[data-family-note]")) {
      state.familyNotes[event.target.dataset.familyNote] = event.target.value;
      event.target.dataset.hasNote = String(Boolean(event.target.value.trim()));
      persistReview();
      updateSummary();
    }
  });
  document.querySelector("[data-family-choice]").addEventListener("change", event => { state.family = event.target.value; persistReview(); });
  document.querySelector("[data-review-note]").addEventListener("input", event => { state.note = event.target.value; persistReview(); updateSummary(); });
  document.querySelector("[data-export]").addEventListener("click", async event => {
    const sectionTitles = {landing:"Landing Plates",cards:"Product Cards",bundles:"Bundles and Packs",sections:"Website Sections"};
    const sections = Object.entries(sectionTitles).map(([id, title]) => ({id, title, feedback:state.familyNotes[id] || ""}));
    const specimens = [...document.querySelectorAll("[data-specimen-id]")].map(node => ({
      id: node.dataset.specimenId,
      title: node.dataset.specimenTitle,
      family: node.dataset.specimenFamily,
      verdict: state.decisions[node.dataset.specimenId] || "unreviewed",
      feedback: state.specimenNotes[node.dataset.specimenId] || ""
    }));
    const payload = {schemaVersion:"1.0.0",gateId:"H-EXP-04A-CARD-VISUAL-DIRECTION",taskId:"TASK-EXP-04-PRODUCT-CARD",candidateRevision:"product-card-02-phase-a-r10",verdict:"round-feedback",leadingFamily:state.family,note:state.note,sections,specimens,productionAuthority:false};
    const output = JSON.stringify(payload, null, 2);
    document.querySelector("[data-review-output]").textContent = output;
    try { await navigator.clipboard.writeText(output); event.target.textContent = "Copied"; }
    catch { event.target.textContent = "Feedback ready below"; }
  });
  hydrateFeedback();
  updateReview();
}

function demote() {
  if (!activeSurface) return;
  renderer?.surfaces?.delete(activeSurface);
  activeSurface.querySelector("canvas[data-mz-core-canvas]")?.remove();
  activeSurface.removeAttribute("data-mz-core");
  activeSurface.classList.remove("is-live");
  activeSurface = null;
}

function moveCore(target) {
  if (forceStatic || disableWebGL || !renderer || target === activeSurface) return;
  const coreId = target.dataset.gradientId;
  if (!coreId) return;
  demote();
  const rect = target.getBoundingClientRect();
  const radius = Math.min(.42, 24 / (Math.min(rect.width, rect.height) / 2 || 1));
  try {
    renderer.mount(target, coreId, {shape:"rect", radius, profile:"deep"});
    target.dataset.mzCore = coreId;
    target.classList.add("is-live");
    activeSurface = target;
    const id = target.closest("[data-specimen-id]")?.dataset.specimenId || "cover";
    setCoreMode(`automatic live focus · ${id} · Deep Mineral No. 5`);
  } catch (error) {
    document.documentElement.dataset.coreError = error?.message || "unknown renderer error";
    setCoreMode("exact static twin · renderer fallback");
  }
}

function chooseVisibleTarget() {
  const best = [...visibility.entries()].filter(([, ratio]) => ratio > .08).sort((a, b) => b[1] - a[1])[0];
  if (best) moveCore(best[0]);
}

function bindAutomaticMotion() {
  if (forceStatic || disableWebGL || !renderer) return;
  observer = new IntersectionObserver(entries => {
    entries.forEach(entry => visibility.set(entry.target, entry.isIntersecting ? entry.intersectionRatio : 0));
    chooseVisibleTarget();
  }, {rootMargin:"-12% 0px -12% 0px", threshold:[0,.08,.2,.35,.5,.7,.9]});
  document.querySelectorAll("[data-auto-live]").forEach(target => observer.observe(target));
}

async function initialiseMotion() {
  if (forceStatic) { setCoreMode(reduced ? "exact static twin · reduced motion" : "exact static twin · forced"); return; }
  if (disableWebGL) { setCoreMode("exact static twin · simulated renderer failure"); return; }
  try {
    const catalogue = await fetchJson("../../../gradient-library/catalogue.json");
    const mounted = await mountLivingCores(document, {
      catalogue,
      staticBaseUrl:"../../gradient-library/assets/static/"
    });
    renderer = mounted.renderer;
    activeSurface = null;
    setCoreMode("automatic live focus · waiting for a specimen");
    bindAutomaticMotion();
  } catch (error) {
    document.documentElement.dataset.coreMoveError = error?.message || "unknown core move error";
    setCoreMode("exact static twin · renderer fallback");
  }
}

async function main() {
  try {
    const registry = await fetchJson("../../../registry/products.json");
    const products = productViewModel(registry.products);
    renderLibrary(buildLibrary(products));
    const count = document.querySelectorAll("[data-specimen-id]").length;
    if (count !== specimenCount || count !== 32) throw new Error(`Expected 32 studies, rendered ${count}`);
    bindReview();
    await initialiseMotion();
  } catch (error) {
    console.error(error);
    const failure = document.createElement("p");
    failure.className = "failure";
    failure.textContent = `Round 10 failed: ${error.message}`;
    document.body.prepend(failure);
  }
}

main();
