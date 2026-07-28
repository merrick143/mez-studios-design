import { mountLivingCores } from "../../../../source-pack/design-system-export/mz-core.js";
import {
  productViewModel,
  buildRound,
  bindSpecimenInteractions,
  specimenCount,
  specimenIds,
} from "./functional-components.js";

const query = new URLSearchParams(location.search);
const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
const forceStatic = query.has("static") || reduced;
const disableWebGL = query.has("no-webgl");
const storageKey = "mz-product-card-phase-b-pb2-r04-review";
const approvalLocked = true;
// Round 03 remains available for audit at its own key. It is deliberately not
// merged because Round 04 is a fresh review of the surviving convergence set.
const previousStorageKey = "mz-product-card-phase-b-pb2-r03-review";
let previousReviewPreserved = false;
try {
  previousReviewPreserved = localStorage.getItem(previousStorageKey) !== null;
} catch {
  previousReviewPreserved = false;
}
document.documentElement.dataset.previousReview = previousReviewPreserved ? "preserved" : "not-found";

const familyOrder = ["discovery", "features", "pricing", "checkout", "bundles", "mobile"];
const killedSpecimenIds = new Set(["B-FT04", "B-FT06"]);
const activeSpecimenIds = new Set(specimenIds);
const phaseAVisualInputCount = 32;
const functionalCandidateCount = 46;

function readSavedReview(key) {
  try {
    return JSON.parse(localStorage.getItem(key) || "{}");
  } catch {
    return {};
  }
}

function activeRecord(record) {
  return Object.fromEntries(
    Object.entries(record || {}).filter(([id]) => activeSpecimenIds.has(id)),
  );
}

function activeFamilyNotes(record) {
  return Object.fromEntries(
    Object.entries(record || {}).filter(([family]) => familyOrder.includes(family)),
  );
}

const saved = readSavedReview(storageKey);
const state = {
  decisions: approvalLocked ? Object.fromEntries(specimenIds.map((id) => [id, "keep"])) : activeRecord(saved.decisions),
  specimenNotes: approvalLocked ? {} : activeRecord(saved.specimenNotes),
  familyNotes: approvalLocked ? {} : activeFamilyNotes(saved.familyNotes),
  family: approvalLocked ? "undecided" : ([...familyOrder, "hybrid"].includes(saved.family) ? saved.family : "undecided"),
  note: approvalLocked ? "Good enough for now. Lock it in, close Phase B and progress. Treat all 46 Round 04 specimens as keep." : (saved.note || ""),
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

function persistReview() {
  try {
    localStorage.setItem(storageKey, JSON.stringify(state));
  } catch {
    document.documentElement.dataset.reviewPersistence = "unavailable";
  }
}

function setCoreMode(message) {
  document.querySelectorAll("[data-core-mode]").forEach((node) => {
    node.textContent = `Motion: ${message}`;
  });
}

function renderRound(nodes) {
  nodes.forEach((node) => {
    const mount = document.querySelector(`[data-mount="${node.dataset.specimenFamily}"]`);
    if (!mount) throw new Error(`Missing mount for ${node.dataset.specimenFamily}`);
    mount.append(node);
  });
}

function updateSummary() {
  const summary = document.querySelector("[data-review-summary]");
  summary.replaceChildren();
  ["keep", "revise", "kill"].forEach((verdict) => {
    const item = document.createElement("div");
    const count = Object.values(state.decisions).filter((value) => value === verdict).length;
    const strong = document.createElement("strong");
    const label = document.createElement("span");
    strong.textContent = String(count);
    label.textContent = verdict;
    item.append(strong, label);
    summary.append(item);
  });
  const notes = [...Object.values(state.specimenNotes), ...Object.values(state.familyNotes), state.note]
    .filter((value) => value?.trim()).length;
  const item = document.createElement("div");
  const strong = document.createElement("strong");
  const label = document.createElement("span");
  strong.textContent = String(notes);
  label.textContent = "notes";
  item.append(strong, label);
  summary.append(item);
}

function updateReview() {
  document.querySelectorAll("[data-verdict]").forEach((button) => {
    const specimen = button.closest("[data-specimen-id]");
    const selected = state.decisions[specimen.dataset.specimenId] === button.dataset.verdict;
    button.setAttribute("aria-pressed", String(selected));
    button.disabled = approvalLocked;
  });
  document.querySelectorAll("[data-specimen-id]").forEach((node) => {
    node.dataset.selectedVerdict = state.decisions[node.dataset.specimenId] || "";
  });
  updateSummary();
  persistReview();
}

function hydrateFeedback() {
  document.querySelectorAll("[data-specimen-note]").forEach((input) => {
    input.value = state.specimenNotes[input.dataset.specimenNote] || "";
    input.dataset.hasNote = String(Boolean(input.value.trim()));
    input.disabled = approvalLocked;
  });
  document.querySelectorAll("[data-family-note]").forEach((input) => {
    input.value = state.familyNotes[input.dataset.familyNote] || "";
    input.dataset.hasNote = String(Boolean(input.value.trim()));
    input.disabled = approvalLocked;
  });
  document.querySelector("[data-family-choice]").value = state.family;
  document.querySelector("[data-review-note]").value = state.note;
  document.querySelector("[data-family-choice]").disabled = approvalLocked;
  document.querySelector("[data-review-note]").disabled = approvalLocked;
}

function buildFeedbackPayload() {
  const sections = familyOrder.map((family) => {
    const heading = document.querySelector(`#${family} h2`);
    return {
      id: family,
      title: heading?.innerText.replace(/\s+/g, " ").trim() || family,
      feedback: state.familyNotes[family] || "",
    };
  });
  const specimens = [...document.querySelectorAll("[data-specimen-id]")].map((node) => ({
    id: node.dataset.specimenId,
    title: node.dataset.specimenTitle,
    family: node.dataset.specimenFamily,
    scope: "functional",
    phaseARefs: node.dataset.phaseARefs ? node.dataset.phaseARefs.split(" ").filter(Boolean) : [],
    verdict: state.decisions[node.dataset.specimenId] || "unreviewed",
    feedback: state.specimenNotes[node.dataset.specimenId] || "",
  }));
  return {
    schemaVersion: "1.0.0",
    gateId: "H-EXP-04B-CARD-FUNCTIONAL-PROOF",
    taskId: "TASK-EXP-04-PRODUCT-CARD",
    candidateRevision: "product-card-02-phase-b-pb2-r04",
    reviewScope: {
      phaseAVisualInputs: phaseAVisualInputCount,
      functionalCandidates: functionalCandidateCount,
      totalReviewCandidates: functionalCandidateCount,
    },
    verdict: "round-feedback",
    leadingFamily: state.family,
    note: state.note,
    sections,
    specimens,
    productionAuthority: false,
  };
}

function bindReview() {
  const panel = document.querySelector("#review-panel");
  const trigger = document.querySelector("[data-review-open]");
  const toggle = (open) => {
    document.body.classList.toggle("is-reviewing", open);
    panel.setAttribute("aria-hidden", String(!open));
    trigger.setAttribute("aria-expanded", String(open));
  };

  document.addEventListener("click", async (event) => {
    const verdict = event.target.closest("[data-verdict]");
    if (verdict && !approvalLocked) {
      const id = verdict.closest("[data-specimen-id]").dataset.specimenId;
      state.decisions[id] = state.decisions[id] === verdict.dataset.verdict ? "" : verdict.dataset.verdict;
      updateReview();
    }
    if (event.target.closest("[data-review-open]")) toggle(true);
    if (event.target.closest("[data-review-close]")) toggle(false);
    const exportButton = event.target.closest("[data-export]");
    if (exportButton) {
      const output = JSON.stringify(buildFeedbackPayload(), null, 2);
      document.querySelector("[data-review-output]").textContent = output;
      try {
        await navigator.clipboard.writeText(output);
        exportButton.textContent = "Copied locked approval receipt";
      } catch {
        exportButton.textContent = "Feedback ready below";
      }
    }
  });

  document.addEventListener("input", (event) => {
    if (approvalLocked) return;
    if (event.target.matches("[data-specimen-note]")) {
      state.specimenNotes[event.target.dataset.specimenNote] = event.target.value;
      event.target.dataset.hasNote = String(Boolean(event.target.value.trim()));
    }
    if (event.target.matches("[data-family-note]")) {
      state.familyNotes[event.target.dataset.familyNote] = event.target.value;
      event.target.dataset.hasNote = String(Boolean(event.target.value.trim()));
    }
    if (event.target.matches("[data-review-note]")) state.note = event.target.value;
    updateSummary();
    persistReview();
  });
  document.querySelector("[data-family-choice]").addEventListener("change", (event) => {
    if (approvalLocked) return;
    state.family = event.target.value;
    persistReview();
  });

  hydrateFeedback();
  updateReview();
}

function demoteCore() {
  if (!activeSurface) return;
  renderer?.surfaces?.delete(activeSurface);
  activeSurface.querySelector("canvas")?.remove();
  activeSurface.removeAttribute("data-mz-core");
  activeSurface.classList.remove("is-live");
  activeSurface = null;
}

function moveCore(target) {
  if (forceStatic || disableWebGL || !renderer || target === activeSurface) return;
  const coreId = target.dataset.gradientId;
  if (!coreId) return;
  demoteCore();
  const rect = target.getBoundingClientRect();
  const radius = Math.min(0.42, 24 / (Math.min(rect.width, rect.height) / 2 || 1));
  try {
    const positioned = getComputedStyle(target).position;
    if (["absolute", "fixed", "sticky"].includes(positioned)) target.style.position = positioned;
    renderer.mount(target, coreId, { shape: "rect", radius, profile: "deep" });
    target.dataset.mzCore = coreId;
    target.classList.add("is-live");
    activeSurface = target;
    const id = target.closest("[data-specimen-id]")?.dataset.specimenId || "cover";
    setCoreMode(`automatic live focus · ${id}`);
  } catch (error) {
    document.documentElement.dataset.coreError = error?.message || "unknown renderer error";
    setCoreMode("exact static fallback");
  }
}

function chooseVisibleTarget() {
  const best = [...visibility.entries()]
    .filter(([, ratio]) => ratio > 0.08)
    .sort((a, b) => b[1] - a[1])[0];
  if (best) moveCore(best[0]);
}

function bindAutomaticMotion() {
  if (forceStatic || disableWebGL || !renderer) return;
  observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => visibility.set(entry.target, entry.isIntersecting ? entry.intersectionRatio : 0));
    chooseVisibleTarget();
  }, { rootMargin: "-12% 0px -12% 0px", threshold: [0, 0.08, 0.2, 0.35, 0.5, 0.7, 0.9] });
  document.querySelectorAll("[data-auto-live]").forEach((target) => observer.observe(target));
}

async function initialiseMotion() {
  if (forceStatic) {
    setCoreMode(reduced ? "static fallback · reduced motion" : "static fallback · forced");
    return;
  }
  if (disableWebGL) {
    setCoreMode("static fallback · renderer disabled");
    return;
  }
  try {
    const catalogue = await fetchJson("../../../../gradient-library/catalogue.json");
    const mounted = await mountLivingCores(document, {
      catalogue,
      staticBaseUrl: "../../gradient-library/assets/static/",
    });
    renderer = mounted.renderer;
    setCoreMode("automatic live focus");
    bindAutomaticMotion();
  } catch (error) {
    document.documentElement.dataset.coreMoveError = error?.message || "unknown renderer error";
    setCoreMode("exact static fallback");
  }
}

async function main() {
  try {
    const registry = await fetchJson("../../../../registry/products.json");
    const products = productViewModel(registry.products);
    if (specimenCount !== functionalCandidateCount) {
      throw new Error(`Expected ${functionalCandidateCount} functional definitions`);
    }
    if (specimenIds.some((id) => killedSpecimenIds.has(id))) {
      throw new Error("A killed candidate remains in the active definitions");
    }
    const candidates = buildRound(products).filter((node) => !killedSpecimenIds.has(node.dataset.specimenId));
    renderRound(candidates);
    const count = document.querySelectorAll("[data-specimen-id]").length;
    if (count !== functionalCandidateCount) throw new Error(`Expected ${functionalCandidateCount} functional candidates, rendered ${count}`);
    if ([...killedSpecimenIds].some((id) => document.querySelector(`[data-specimen-id="${id}"]`))) {
      throw new Error("A killed candidate rendered");
    }
    document.querySelectorAll("[data-specimen-id]").forEach((node) => {
      if (!node.dataset.phaseARefs?.trim()) throw new Error(`${node.dataset.specimenId} is missing explicit Phase A lineage`);
    });
    bindSpecimenInteractions(document);
    bindReview();
    await initialiseMotion();
  } catch (error) {
    console.error(error);
    const failure = document.createElement("p");
    failure.className = "failure";
    failure.textContent = `Phase B Round 04 failed: ${error.message}`;
    document.body.prepend(failure);
  }
}

main();
