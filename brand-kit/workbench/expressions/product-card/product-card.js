import { mountLivingCores } from "../../../source-pack/design-system-export/mz-core.js";

const query = new URLSearchParams(location.search);
const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;

try {
  const response = await fetch("../../../gradient-library/catalogue.json");
  if (!response.ok) throw new Error(`Catalogue failed: ${response.status}`);
  const catalogue = await response.json();
  const result = await mountLivingCores(document, {
    catalogue,
    staticBaseUrl: "/brand-kit/gradient-library/assets/static/",
    wingsUrl: "/brand-kit/source-pack/design-system-export/assets/wings.svg",
    forceStatic: query.has("static") || reduced,
    disableWebGL: query.has("no-webgl")
  });
  document.documentElement.dataset.coreMode = result.mode;
} catch (error) {
  document.documentElement.dataset.coreMode = "static";
  console.error("[product-card-02-round-02] Exact static twin retained after renderer failure.", error);
}

const direction = document.querySelector("#review-direction");
const verdict = document.querySelector("#review-verdict");
const note = document.querySelector("#review-note");
const output = document.querySelector("#review-json");
const status = document.querySelector("#review-status");

document.querySelectorAll("[data-select-direction]").forEach((button) => {
  button.addEventListener("click", () => {
    const selected = button.dataset.selectDirection;
    direction.value = selected;
    document.querySelectorAll(".candidate").forEach((candidate) => {
      candidate.classList.toggle("is-selected", candidate.dataset.directionId === selected);
    });
    document.querySelectorAll("[data-select-direction]").forEach((peer) => {
      peer.textContent = peer === button ? `${selected} selected` : `Choose ${peer.dataset.selectDirection}`;
    });
    status.textContent = `${selected} saved as the current base preference. Phase B is still held.`;
    renderPayload();
  });
});

const payload = {
  schemaVersion: "1.0.0",
  gateId: "H-EXP-04A-CARD-VISUAL-DIRECTION",
  taskId: "TASK-EXP-04-PRODUCT-CARD",
  expressionId: "mz.systems.expression.product-card",
  programmeItem: "Product Card 02",
  phase: "A-visual-architecture",
  round: "visual-architecture-round-02",
  candidateStatus: "visual-research-candidate",
  candidateRevision: "product-card-02-phase-a-r02",
  supersedes: "product-card-02-phase-a-r01",
  selectedBaseTreatment: null,
  agentRecommendation: "C01 Editorial Portrait as the base; C02 Full Field Portrait for one focal feature; C03 System Index for dense product surfaces; C04 Product Pack only for commerce or launch media.",
  contrastRule: "Use same-polarity white on F8 for calm repeated shelves; use charcoal on light or white on charcoal for one focal contrast; use #171715 and #252523 rather than pure black for dark surfaces.",
  phaseBStatus: "held-until-visual-lock",
  verdict: "iterate",
  note: "",
  reviewedAt: new Date().toISOString(),
  approver: "Olli",
  productionAuthority: false
};

function renderPayload() {
  payload.selectedBaseTreatment = direction.value || null;
  payload.verdict = verdict.value;
  payload.note = note.value;
  payload.reviewedAt = new Date().toISOString();
  output.textContent = JSON.stringify(payload, null, 2);
}

const panel = document.querySelector("#review-panel");
const scrim = document.querySelector("[data-scrim]");
const closeButton = document.querySelector(".review-close");

function setPanel(open) {
  panel.classList.toggle("open", open);
  scrim.classList.toggle("open", open);
  panel.setAttribute("aria-hidden", String(!open));
  document.querySelectorAll(".review-open").forEach((button) => button.setAttribute("aria-expanded", String(open)));
  if (open) {
    renderPayload();
    closeButton.focus();
  }
}

document.querySelectorAll(".review-open").forEach((button) => button.addEventListener("click", () => setPanel(true)));
closeButton.addEventListener("click", () => setPanel(false));
scrim.addEventListener("click", () => setPanel(false));
addEventListener("keydown", (event) => { if (event.key === "Escape") setPanel(false); });
[direction, verdict, note].forEach((input) => input.addEventListener("input", renderPayload));
document.querySelector("#copy-review").addEventListener("click", async () => {
  renderPayload();
  await navigator.clipboard.writeText(output.textContent);
  status.textContent = "Round 02 review JSON copied";
});

renderPayload();
