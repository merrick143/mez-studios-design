import { mountLivingCores } from "../../../source-pack/design-system-export/mz-core.js";

const query = new URLSearchParams(location.search);
const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
const compactViewport = innerWidth < 430;
const forceStatic = query.has("static") || reduced || compactViewport;
const disableWebGL = query.has("no-webgl");
const runtimeState = document.querySelector("#runtime-state");
if (compactViewport) document.querySelector("[data-mz-core]").dataset.shape = "disc";

try {
  const response = await fetch("../../../gradient-library/catalogue.json");
  if (!response.ok) throw new Error(`Catalogue failed: ${response.status}`);
  const catalogue = await response.json();
  const result = await mountLivingCores(document, {
    catalogue,
    staticBaseUrl: "../../gradient-library/assets/static/",
    wingsUrl: "./assets/wings.svg",
    forceStatic,
    disableWebGL
  });
  document.documentElement.dataset.coreMode = result.mode;
  runtimeState.textContent = compactViewport ? "CANONICAL DISC · COMPACT" : result.mode === "live" ? "LIVE CANONICAL" : "EXACT COLOUR FALLBACK";
} catch (error) {
  document.documentElement.dataset.coreMode = "static";
  runtimeState.textContent = "EXACT COLOUR FALLBACK";
  console.error("[sphere-proof] Exact colour fallback retained after renderer failure.", error);
}

const panel = document.querySelector("#review-panel");
const scrim = document.querySelector("[data-scrim]");
const openButtons = document.querySelectorAll(".review-open, [data-open-review]");
const closeButton = document.querySelector(".review-close");
const output = document.querySelector("#review-json");
const status = document.querySelector("#review-status");
const approvalPayload = {
  schemaVersion: "1.0.0",
  gateId: "H-EXP-02-SPHERE-PROOF",
  taskId: "TASK-EXP-02-SPHERE-CONTRACT",
  expressionId: "mz.systems.expression.sphere",
  candidateStatus: "review-candidate",
  candidateRevision: "sphere-contract-01",
  verdict: "approve",
  note: "Perfect. I approve. Let's proceed.",
  reviewedAt: "2026-07-21T13:49:34.000Z",
  approver: "Olli",
  submittedProductionAuthority: false,
  decisionId: "DEC-SPHERE-EXPRESSION-001",
  resultingStatus: "canonical",
  productionAuthority: true
};

function renderPayload() { output.textContent = JSON.stringify(approvalPayload, null, 2); }
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
