import { mountLivingCores } from "../../../source-pack/design-system-export/mz-core.js";

const query = new URLSearchParams(location.search);
const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
const forceStatic = query.has("static") || reduced;
const disableWebGL = query.has("no-webgl");

try {
  const catalogueResponse = await fetch("../../../gradient-library/catalogue.json");
  if (!catalogueResponse.ok) throw new Error(`Catalogue failed: ${catalogueResponse.status}`);
  const catalogue = await catalogueResponse.json();
  const result = await mountLivingCores(document, {
    catalogue,
    staticBaseUrl: "../../gradient-library/assets/static/",
    wingsUrl: "./assets/wings.svg",
    forceStatic,
    disableWebGL
  });
  document.documentElement.dataset.coreMode = result.mode;
} catch (error) {
  document.documentElement.dataset.coreMode = "static";
  console.error("[disc-proof] Exact static twin retained after renderer failure.", error);
}

const panel = document.querySelector("#review-panel");
const scrim = document.querySelector("[data-scrim]");
const openButtons = document.querySelectorAll(".review-open, [data-open-review]");
const closeButton = document.querySelector(".review-close");
const output = document.querySelector("#review-json");
const status = document.querySelector("#review-status");

const approvalPayload = {
  schemaVersion: "1.0.0",
  gateId: "H-EXP-01-DISC-PROOF",
  taskId: "TASK-EXP-01-DISC-CONTRACT",
  expressionId: "mz.systems.expression.disc",
  candidateStatus: "review-candidate",
  candidateRevision: "disc-contract-01",
  verdict: "approve",
  note: "Okay yeah so I approve all that. If you can lock it in then let's proceed.",
  reviewedAt: "2026-07-21T13:32:29.000Z",
  approver: "Olli",
  submittedProductionAuthority: false,
  decisionId: "DEC-DISC-EXPRESSION-001",
  resultingStatus: "canonical",
  productionAuthority: true
};

function renderPayload() {
  output.textContent = JSON.stringify(approvalPayload, null, 2);
}

function setPanel(open) {
  panel.classList.toggle("open", open);
  scrim.classList.toggle("open", open);
  panel.setAttribute("aria-hidden", String(!open));
  document.querySelector(".review-open").setAttribute("aria-expanded", String(open));
  if (open) { renderPayload(); closeButton.focus(); }
}

openButtons.forEach(button => button.addEventListener("click", () => setPanel(true)));
closeButton.addEventListener("click", () => setPanel(false));
scrim.addEventListener("click", () => setPanel(false));
addEventListener("keydown", event => { if (event.key === "Escape") setPanel(false); });
document.querySelector("#copy-review").addEventListener("click", async () => {
  renderPayload();
  await navigator.clipboard.writeText(output.textContent);
  status.textContent = "Approval JSON copied";
});
