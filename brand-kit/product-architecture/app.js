import { mountLivingCores } from "../source-pack/design-system-export/mz-core.js";

const MANIFEST_URL = "./manifest.json";
const REVIEW_URL = "./review.json";
const CATALOGUE_URL = "../gradient-library/catalogue.json";
const STATIC_BASE = "../../gradient-library/assets/static/";
const WINGS_URL = "../../source-pack/design-system-export/assets/wings.svg";
const SOURCE_BASE = "../gradient-library/source-masters/";

let manifest;
let review;

const wingsMarkup = () => `<img src="../source-pack/design-system-export/assets/wings.svg" alt="">`;

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function renderFamilyPreview() {
  document.querySelector("#family-preview").innerHTML = manifest.products.map((product) => `
    <article class="family-mark">
      <div class="family-mark__core" data-mz-core="${escapeHtml(product.gradientId)}" data-shape="disc">${wingsMarkup()}</div>
      <strong>${escapeHtml(product.publicName)}</strong>
      <span>${escapeHtml(product.gradientId)}</span>
    </article>`).join("");
}

function renderRoster() {
  document.querySelector("#roster").innerHTML = manifest.products.map((product) => `
    <article class="roster-row">
      <h3>${escapeHtml(product.publicName)}<span>${escapeHtml(product.function)}</span></h3>
      <code class="machine-id">${escapeHtml(product.productId)}</code>
      <p class="roster-copy">${escapeHtml(product.summary)}</p>
      <span class="state state--${product.gradientState === "locked" ? "locked" : "live"}">${escapeHtml(product.gradientState)}</span>
    </article>`).join("");
}

function renderAssignments() {
  document.querySelector("#assignment-list").innerHTML = manifest.products.map((product, index) => `
    <article class="assignment-row assignment-row--approved">
      <div class="assignment-copy">
        <span class="index">0${index + 1}</span>
        <h3>${escapeHtml(product.publicName)}</h3>
        <p>${escapeHtml(product.selectionReason)}</p>
        <code>${escapeHtml(product.productId)}</code>
      </div>
      <div class="approved-core">
        <div class="approved-core__stage">
          <div class="approved-core__living" data-mz-core="${escapeHtml(product.gradientId)}" data-shape="disc">${wingsMarkup()}</div>
          <img class="approved-core__source" src="${SOURCE_BASE}${escapeHtml(product.gradientId)}.png" alt="Exact ${escapeHtml(product.gradientId)} source">
        </div>
        <div class="approved-core__meta">
          <div><strong>${escapeHtml(product.gradientId)}</strong><span>${escapeHtml(product.gradientState)}</span></div>
          <p>Animated Deep Mineral expression + exact static colour authority.</p>
        </div>
      </div>
    </article>`).join("");
}

function renderDecision() {
  document.querySelector("#review-summary").innerHTML = review.products.map((product) => `
    <div class="summary-row"><strong>${escapeHtml(product.publicName)}</strong><span>${escapeHtml(product.gradientId)}</span></div>`).join("");
  document.querySelector("#approval-note").textContent = review.overallNote;
  document.querySelector("#approval-meta").textContent = `${review.approvedBy} · ${review.approvedAt} · ${review.verdict}`;
}

function downloadDecision() {
  const blob = new Blob([`${JSON.stringify(review, null, 2)}\n`], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "mez-product-architecture-gradient-assignment-01-approved.json";
  document.body.append(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

async function initialise() {
  const responses = await Promise.all([fetch(MANIFEST_URL), fetch(REVIEW_URL), fetch(CATALOGUE_URL)]);
  if (responses.some((response) => !response.ok)) throw new Error("Approved product architecture sources failed to load");
  const documents = await Promise.all(responses.map((response) => response.json()));
  [manifest, review] = documents;
  renderFamilyPreview();
  renderRoster();
  renderAssignments();
  renderDecision();
  document.querySelector("#export-decision").addEventListener("click", downloadDecision);

  const catalogueData = documents[2];
  const query = new URLSearchParams(location.search);
  const result = await mountLivingCores(document, {
    catalogue: catalogueData,
    staticBaseUrl: STATIC_BASE,
    wingsUrl: WINGS_URL,
    forceStatic: query.has("static"),
    disableWebGL: query.has("no-webgl"),
  });
  document.documentElement.dataset.livingCoreMode = result.mode;
  document.documentElement.dataset.livingCoreCount = String(result.count);
}

initialise().catch((error) => {
  console.error("Approved product architecture record failed", error);
  document.documentElement.dataset.livingCoreMode = "failed";
  document.querySelector("#approval-meta").textContent = error.message;
});
