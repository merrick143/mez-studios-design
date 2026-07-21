import { mountLivingCores } from "../../../source-pack/design-system-export/mz-core.js";

const CORE_IDS = ["MZ-G06", "MZ-G13", "MZ-G48"];
const CATALOGUE_URL = "../../catalogue.json";
const PROFILES_URL = "./profiles.json";
const STATIC_BASE = "../../gradient-library/assets/static/";
const RENDERER_WINGS = "./assets/wings.svg";
const MARK_WINGS = "../../../source-pack/design-system-export/assets/wings.svg";

let catalogue;
let profileDocument;
let renderer;
let selectedProfile = "current";
let comparisonShape = { shape: "disc", radius: 0, layout: "disc" };
let currentDecision = null;

const matrixNode = document.querySelector("#matrix");
const pickerNode = document.querySelector("#profile-picker");
const valuesNode = document.querySelector("#profile-values");
const detailNode = document.querySelector("#detail-grid");
const noteNode = document.querySelector("#decision-note");
const statusNode = document.querySelector("#decision-status");
const exportNode = document.querySelector("#export-decision");

function profileMap() {
  return Object.fromEntries(profileDocument.profiles.map((profile) => [profile.id, profile.values]));
}

function profile(id) {
  return profileDocument.profiles.find((row) => row.id === id);
}

function wingsMarkup(extra = "") {
  return `<img class="wings ${extra}" src="${MARK_WINGS}" alt="">`;
}

function renderMatrix() {
  matrixNode.innerHTML = `<div class="matrix-corner"></div>${profileDocument.profiles.map((row) => `
    <button class="matrix-head ${row.id === selectedProfile ? "is-selected" : ""}" type="button" data-profile-select="${row.id}">
      <span>${row.number}</span><strong>${row.name}</strong><p>${row.description}</p>
    </button>`).join("")}${CORE_IDS.map((coreId) => `
      <div class="matrix-label"><img src="../../source-masters/${coreId}.png" alt="${coreId} PNG authority"><strong>${coreId}</strong></div>
      ${profileDocument.profiles.map((row) => `<button class="matrix-cell ${row.id === selectedProfile ? "is-selected" : ""}" type="button" data-profile-select="${row.id}">
        <span class="matrix-surface" data-matrix-surface data-mz-core="${coreId}" data-profile="${row.id}" data-shape="disc">${wingsMarkup()}</span>
      </button>`).join("")}`).join("")}`;
}

function renderDetail() {
  detailNode.innerHTML = CORE_IDS.map((coreId) => `<article class="detail-card">
    <header class="detail-card__head"><h3>${coreId}</h3><span>Same palette · one finish</span></header>
    <div class="source-compare"><img src="../../source-masters/${coreId}.png" alt="${coreId} PNG authority"><p>PNG authority<br>Finish variables never alter this source.</p></div>
    <div class="expressions">
      <figure><div class="stage"><div class="detail-surface detail-disc" data-detail-surface data-mz-core="${coreId}" data-profile="current" data-shape="disc">${wingsMarkup()}</div></div><figcaption>Disc</figcaption></figure>
      <figure><div class="stage"><div class="detail-surface detail-sphere" data-detail-surface data-mz-core="${coreId}" data-profile="current" data-shape="sphere">${wingsMarkup()}</div></div><figcaption>Sphere</figcaption></figure>
      <figure class="span-2"><div class="stage"><div class="detail-surface detail-card-field" data-detail-surface data-mz-core="${coreId}" data-profile="current" data-shape="rect" data-radius="0.08">${wingsMarkup()}</div></div><figcaption>Card · full field</figcaption></figure>
      <figure class="span-2"><div class="stage"><div class="detail-surface detail-pill" data-detail-surface data-mz-core="${coreId}" data-profile="current" data-shape="rect" data-radius="1">${wingsMarkup()}</div></div><figcaption>Pill · full bleed</figcaption></figure>
      <figure class="span-2"><div class="stage"><div class="detail-surface detail-wings" data-detail-surface data-mz-core="${coreId}" data-profile="current" data-shape="wings"></div></div><figcaption>Gradient Wings</figcaption></figure>
    </div>
  </article>`).join("");
}

function showProfile(id) {
  selectedProfile = id;
  const row = profile(id);
  document.querySelector("#profile-title").textContent = `${row.number} · ${row.name}`;
  document.querySelector("#profile-description").textContent = row.description;
  document.querySelectorAll("[data-profile-select]").forEach((button) => button.classList.toggle("is-selected", button.dataset.profileSelect === id));
  pickerNode.querySelectorAll("button").forEach((button) => button.classList.toggle("is-active", button.dataset.profileSelect === id));
  valuesNode.innerHTML = Object.entries(row.values).map(([key, value]) => `<span>${key} ${value}</span>`).join("");
  document.querySelectorAll("[data-detail-surface]").forEach((element) => renderer.setProfile(element, id));
  showDecision();
  history.replaceState(null, "", `#${id}`);
}

function setComparisonExpression(button) {
  comparisonShape = { shape: button.dataset.shape, radius: Number(button.dataset.radius || 0), layout: button.dataset.layout || button.dataset.shape };
  document.querySelectorAll("#expression-switch button").forEach((item) => item.classList.toggle("is-active", item === button));
  document.querySelectorAll("[data-matrix-surface]").forEach((element) => {
    element.className = `matrix-surface layout-${comparisonShape.layout}`;
    renderer.setShape(element, comparisonShape.shape, comparisonShape.radius);
  });
}

function renderPicker() {
  pickerNode.innerHTML = profileDocument.profiles.map((row) => `<button type="button" data-profile-select="${row.id}"><span>${row.number}</span><strong>${row.name}</strong></button>`).join("");
}

async function loadDecision() {
  try {
    const response = await fetch("/api/finish-decisions", { cache: "no-store" });
    if (!response.ok) throw new Error();
    currentDecision = (await response.json()).decision || null;
    showDecision();
  } catch {
    statusNode.textContent = "Static review active. Run brand-kit/server.py to save a finish decision.";
  }
}

function showDecision() {
  const matches = currentDecision?.profileId === selectedProfile;
  document.querySelectorAll("[data-verdict]").forEach((button) => button.classList.toggle("is-selected", matches && button.dataset.verdict === currentDecision.verdict));
  noteNode.value = matches ? currentDecision.note : "";
  exportNode.disabled = !matches;
  if (matches) statusNode.textContent = `${currentDecision.verdict} recorded for ${profile(selectedProfile).name}.`;
  else if (!statusNode.textContent.includes("Static review")) statusNode.textContent = "No finish decision recorded for this profile.";
}

async function saveDecision(verdict) {
  const response = await fetch("/api/finish-decisions", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ studyId: profileDocument.studyId, profileId: selectedProfile, verdict, note: noteNode.value, values: profile(selectedProfile).values }),
  });
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error || "Finish decision could not be saved");
  currentDecision = payload.decision;
  showDecision();
}

function downloadDecision() {
  const blob = new Blob([`${JSON.stringify(currentDecision, null, 2)}\n`], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "mez-living-core-depth-light-01-decision.json";
  document.body.append(link);
  link.click(); link.remove(); URL.revokeObjectURL(url);
}

async function initialise() {
  const [catalogueResponse, profilesResponse] = await Promise.all([fetch(CATALOGUE_URL), fetch(PROFILES_URL)]);
  if (!catalogueResponse.ok || !profilesResponse.ok) throw new Error("Calibration data failed to load");
  [catalogue, profileDocument] = await Promise.all([catalogueResponse.json(), profilesResponse.json()]);
  const hashProfile = location.hash.slice(1);
  if (profileDocument.profiles.some((row) => row.id === hashProfile)) selectedProfile = hashProfile;
  renderMatrix(); renderDetail(); renderPicker();
  const query = new URLSearchParams(location.search);
  const result = await mountLivingCores(document, {
    catalogue,
    profiles: profileMap(),
    staticBaseUrl: STATIC_BASE,
    wingsUrl: RENDERER_WINGS,
    forceStatic: query.has("static"),
    disableWebGL: query.has("no-webgl"),
  });
  renderer = result.renderer;
  document.documentElement.dataset.livingCoreMode = result.mode;
  document.documentElement.dataset.livingCoreCount = String(result.count);
  showProfile(selectedProfile);
  await loadDecision();
}

document.querySelector("#expression-switch").addEventListener("click", (event) => { const button = event.target.closest("button"); if (button) setComparisonExpression(button); });
document.addEventListener("click", (event) => { const button = event.target.closest("[data-profile-select]"); if (button) showProfile(button.dataset.profileSelect); });
document.querySelector("#decision-actions").addEventListener("click", async (event) => { const button = event.target.closest("[data-verdict]"); if (!button) return; try { await saveDecision(button.dataset.verdict); } catch (error) { statusNode.textContent = error.message; } });
exportNode.addEventListener("click", () => { if (currentDecision) downloadDecision(); });

initialise().catch((error) => { console.error("Depth and light calibration failed", error); document.documentElement.dataset.livingCoreMode = "failed"; });
