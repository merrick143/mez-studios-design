import "./play-button.js";

const SVG_NS = "http://www.w3.org/2000/svg";
const WINGS_PATHS = [
  "M9.31894 227.388C9.31894 243.442 22.3337 256.457 38.3883 256.457H141.746C157.801 256.457 170.815 243.442 170.815 227.388V172.807C170.815 168.476 169.848 164.201 167.984 160.292L107.284 33.0283C102.46 22.9142 92.2519 16.4734 81.0462 16.4734H38.3883C22.3337 16.4734 9.31894 29.4882 9.31894 45.5427V227.388Z",
  "M348.462 227.388C348.462 243.442 335.447 256.457 319.392 256.457H216.034C199.98 256.457 186.965 243.442 186.965 227.388V172.807C186.965 168.476 187.932 164.201 189.797 160.292L250.497 33.0283C255.321 22.9142 265.529 16.4734 276.734 16.4734H319.392C335.447 16.4734 348.462 29.4882 348.462 45.5427V227.388Z"
];

const DECISIONS = [
  {id:"motionAllocation", group:"SYSTEM RULES", title:"Motion allocation", question:"Should static remain the default, with one living focal object only where attention is earned?", options:["lock","edit","reject"]},
  {id:"scaleBands", group:"SYSTEM RULES", title:"Contextual scale bands", question:"Should role and composition determine size instead of a universal minimum or maximum?", options:["lock","edit","reject"]},
  {id:"gradientWings", group:"EXPRESSION FAMILY", title:"Gradient Wings", question:"Allow the gradient-filled Wings as a product-family marker?", options:["allow","edit","drop"]},
  {id:"flatDisc", group:"EXPRESSION FAMILY", title:"Flat disc", question:"Allow the flat disc as the canonical compact product icon?", options:["allow","edit","drop"]},
  {id:"livingSphere", group:"EXPRESSION FAMILY", title:"Living sphere", question:"Allow the dimensional living sphere for rare focal moments?", options:["allow","edit","drop"]},
  {id:"landingCard", group:"EXPRESSION FAMILY", title:"Landing card", question:"Allow the wide product card for website feature and product surfaces?", options:["allow","edit","drop"]},
  {id:"tradingCard", group:"EXPRESSION FAMILY", title:"Trading card", question:"Allow the 3:4 collectible card for drops, packs and purchase moments?", options:["allow","edit","drop"]},
  {id:"productPill", group:"EXPRESSION FAMILY", title:"Product pill", question:"Allow the compact product pill for selectors and dense navigation?", options:["allow","edit","drop"]},
  {id:"collections", group:"COLLECTIONS", title:"Collection grammar", question:"Advance stack, bundle and constellation forms into the commerce calibration?", options:["advance","edit","drop"]}
];

const STORAGE_KEY = "mezIdentityProductObject02";
const state = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{"decisions":{},"overallNote":""}');

function wings(className = "wings") {
  const svg = document.createElementNS(SVG_NS, "svg");
  svg.setAttribute("class", className);
  svg.setAttribute("viewBox", "9 16 340 241");
  svg.setAttribute("aria-hidden", "true");
  WINGS_PATHS.forEach(data => {
    const path = document.createElementNS(SVG_NS, "path");
    path.setAttribute("d", data);
    path.setAttribute("fill", "currentColor");
    svg.append(path);
  });
  return svg;
}

function applyGradient(element, variant, living = false) {
  element.style.setProperty("--gradient-image", `url(${JSON.stringify(variant.url)})`);
  if (living) {
    element.classList.add("living-surface");
    const texture = document.createElement("aurora-texture");
    texture.setAttribute("gradient", variant.url);
    texture.setAttribute("gradient-id", variant.id);
    texture.setAttribute("aria-hidden", "true");
    element.append(texture);
  }
  return element;
}

function disc(variant, {living = false, sphere = false, className = ""} = {}) {
  const element = applyGradient(document.createElement("div"), variant, living);
  element.className = `${sphere ? "sphere" : "disc"} ${className} ${living ? "living-surface" : ""}`.trim();
  element.append(wings());
  return element;
}

function gradientMark(variant) {
  const mark = applyGradient(document.createElement("div"), variant, true);
  mark.className = "gradient-mark living-surface";
  const source = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="9 16 340 241">${WINGS_PATHS.map(path => `<path fill="white" d="${path}"/>`).join("")}</svg>`;
  const mask = `url("data:image/svg+xml,${encodeURIComponent(source)}")`;
  mark.style.maskImage = mask;
  mark.style.webkitMaskImage = mask;
  return mark;
}

function landingCard(variant) {
  const card = applyGradient(document.createElement("div"), variant, false);
  card.className = "landing-card";
  const chip = document.createElement("span");
  chip.className = "card-chip";
  chip.textContent = "MEZ SYSTEMS";
  const lockup = document.createElement("div");
  lockup.className = "card-lockup";
  const name = document.createElement("strong");
  name.textContent = "AI OS";
  lockup.append(wings(), name);
  card.append(chip, lockup);
  return card;
}

function tradingCard(variant, className = "") {
  const card = applyGradient(document.createElement("div"), variant, false);
  card.className = `trading-card ${className}`.trim();
  const chip = document.createElement("span");
  chip.className = "card-chip";
  chip.textContent = "MEZ SYSTEMS";
  const lockup = document.createElement("div");
  lockup.className = "card-lockup";
  const name = document.createElement("strong");
  name.textContent = "AI OS";
  lockup.append(wings(), name);
  card.append(chip, lockup);
  return card;
}

function productPill(variant) {
  const pill = document.createElement("div");
  pill.className = "product-pill";
  const core = disc(variant);
  const label = document.createElement("span");
  label.textContent = "AI OS";
  pill.append(core, label);
  return pill;
}

function expressionItem(id, index, name, use, visual) {
  const item = document.createElement("article");
  item.className = "expression-item";
  item.id = id;
  const stage = document.createElement("div");
  stage.className = "expression-stage";
  stage.append(visual);
  const copy = document.createElement("div");
  copy.className = "expression-copy";
  copy.innerHTML = `<span>${String(index).padStart(2,"0")}</span><h3>${name}</h3><p>${use}</p>`;
  item.append(stage, copy);
  return item;
}

function renderOpening(variant) {
  const split = document.createElement("div");
  split.className = "split-core";
  split.style.setProperty("--gradient-image", `url(${JSON.stringify(variant.url)})`);
  const still = document.createElement("div");
  still.className = "split-half split-half-static";
  const living = applyGradient(document.createElement("div"), variant, true);
  living.className = "split-half split-half-living living-surface";
  const livingTexture = living.querySelector("aurora-texture");
  livingTexture.style.position = "absolute";
  livingTexture.style.inset = "0 auto auto 0";
  livingTexture.style.width = "200%";
  livingTexture.style.height = "100%";
  livingTexture.style.transform = "translateX(-50%)";
  const divider = document.createElement("span");
  divider.className = "split-divider";
  const staticLabel = document.createElement("span");
  staticLabel.className = "split-label split-label-static";
  staticLabel.textContent = "STATIC";
  const livingLabel = document.createElement("span");
  livingLabel.className = "split-label split-label-living";
  livingLabel.textContent = "LIVING";
  split.append(still, living, wings(), divider, staticLabel, livingLabel);
  document.querySelector("[data-opening-visual]").append(split);
}

function renderMotion(variant) {
  document.querySelector("[data-static-state]").append(disc(variant, {className:"static-disc"}));
  document.querySelector("[data-living-state]").append(disc(variant, {living:true, sphere:true, className:"living-disc"}));
}

function renderScale(variant) {
  const bands = [
    ["24 to 48", "Utility", "Static mark or disc"],
    ["48 to 128", "Compact", "Static navigation and selectors"],
    ["160 to 360", "Product", "Default product recognition"],
    ["360 to 640", "Feature", "Static or living when focal"],
    ["640 to 1000+", "Immersive", "Living focal object, crop allowed"]
  ];
  const root = document.querySelector("[data-scale-bands]");
  bands.forEach(([range, title, use]) => {
    const item = document.createElement("article");
    item.className = "scale-band";
    const stage = document.createElement("div");
    stage.className = "scale-visual";
    stage.append(disc(variant));
    const copy = document.createElement("div");
    copy.className = "scale-copy";
    copy.innerHTML = `<b>${range}</b><span>${title}<br>${use}</span>`;
    item.append(stage, copy);
    root.append(item);
  });
}

function renderExpressions(variant) {
  const root = document.querySelector("[data-expression-grid]");
  root.append(
    expressionItem("gradient-wings", 1, "Gradient Wings", "Product-family marker. Never replaces the parent Wings lockup.", gradientMark(variant)),
    expressionItem("flat-disc", 2, "Flat disc", "Canonical compact product icon. Static in repeated and small contexts.", disc(variant, {className:"flat-disc"})),
    expressionItem("living-sphere", 3, "Living sphere", "Dimensional focal treatment for rare hero and reveal moments.", disc(variant, {living:true, sphere:true, className:"hero-sphere"})),
    expressionItem("landing-card", 4, "Landing card", "Wide product surface for feature sections and sales pages.", landingCard(variant)),
    expressionItem("trading-card", 5, "Trading card", "Collectible 3:4 format for drops, packs and commerce.", tradingCard(variant)),
    expressionItem("product-pill", 6, "Product pill", "Compact selector for dense navigation and product switching.", productPill(variant))
  );
}

function renderCollections(variant) {
  const root = document.querySelector("[data-collections]");
  const definitions = [
    ["Stack", "Layered product or module set", () => {
      const visual = document.createElement("div");
      visual.className = "collection-visual stack";
      visual.append(tradingCard(variant, "mini-card"), tradingCard(variant, "mini-card"), tradingCard(variant, "mini-card"));
      return visual;
    }],
    ["Bundle", "One commercial collection", () => {
      const visual = document.createElement("div");
      visual.className = "collection-visual";
      const shell = document.createElement("div");
      shell.className = "bundle-shell";
      shell.append(tradingCard(variant, "mini-card"), tradingCard(variant, "mini-card"), tradingCard(variant, "mini-card"));
      visual.append(shell);
      return visual;
    }],
    ["Constellation", "One parent system, multiple product cores", () => {
      const visual = document.createElement("div");
      visual.className = "collection-visual";
      const constellation = document.createElement("div");
      constellation.className = "constellation";
      constellation.append(disc(variant), disc(variant), disc(variant));
      visual.append(constellation);
      return visual;
    }]
  ];
  definitions.forEach(([name, use, makeVisual], index) => {
    const item = document.createElement("article");
    item.className = "collection-item";
    const copy = document.createElement("div");
    copy.className = "collection-copy";
    copy.innerHTML = `<span>0${index + 1}</span><h3>${name}</h3><p>${use}</p>`;
    item.append(makeVisual(), copy);
    root.append(item);
  });
}

function renderReview() {
  const root = document.querySelector("[data-review-body]");
  let group = "";
  DECISIONS.forEach((decision, index) => {
    if (decision.group !== group) {
      group = decision.group;
      const title = document.createElement("p");
      title.className = "review-group-title";
      title.textContent = group;
      root.append(title);
    }
    const fieldset = document.createElement("fieldset");
    fieldset.className = "decision";
    fieldset.dataset.key = decision.id;
    fieldset.innerHTML = `<legend><span>${String(index + 1).padStart(2,"0")}</span>${decision.title}</legend><p>${decision.question}</p><div class="choices">${decision.options.map(option => `<button type="button" data-value="${option}" aria-pressed="false">${option}</button>`).join("")}</div><textarea rows="2" data-note placeholder="Optional causal note"></textarea>`;
    root.append(fieldset);
  });
  const overall = document.createElement("label");
  overall.className = "overall-note";
  overall.innerHTML = `Anything the atlas still fails to show<textarea rows="3" data-overall-note placeholder="Optional"></textarea>`;
  root.append(overall);
}

const panel = document.querySelector("#review-panel");
const scrim = document.querySelector("[data-scrim]");
const progress = document.querySelector("[data-count]");
const status = document.querySelector("#review-status");

function setPanel(open) {
  panel.classList.toggle("open", open);
  scrim.classList.toggle("open", open);
  panel.setAttribute("aria-hidden", String(!open));
  document.querySelector(".review-open").setAttribute("aria-expanded", String(open));
  if (open) panel.querySelector(".review-close").focus();
}

function save() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  const complete = Object.values(state.decisions).filter(item => item.decision).length;
  progress.textContent = `${complete}/9`;
  status.textContent = complete === 9 ? "Ready to export" : `${complete} of 9 decisions complete`;
}

function hydrate() {
  document.querySelectorAll(".decision").forEach(group => {
    const record = state.decisions[group.dataset.key] || {};
    group.querySelectorAll("[data-value]").forEach(button => button.setAttribute("aria-pressed", String(button.dataset.value === record.decision)));
    group.querySelector("[data-note]").value = record.note || "";
  });
  document.querySelector("[data-overall-note]").value = state.overallNote || "";
  save();
}

function exportRecord() {
  return {
    schemaVersion:"1.0.0",
    studyId:"MEZ-IDENTITY-PRODUCT-OBJECT-02",
    exportedAt:new Date().toISOString(),
    productionAuthority:false,
    sourceExpressionApproved:false,
    sourceGradient:"MZ-G13",
    sourceGradientSha256:"7932fb83949329ad562a13010221d2c0e6cad9f24312993acf781935547a946e",
    supersedes:"MEZ-IDENTITY-PRODUCT-OBJECT-01",
    record:{decisions:state.decisions, overallNote:state.overallNote || "", productionAuthority:false}
  };
}

document.addEventListener("click", event => {
  const valueButton = event.target.closest("[data-value]");
  if (valueButton) {
    const group = valueButton.closest(".decision");
    const key = group.dataset.key;
    state.decisions[key] = state.decisions[key] || {decision:"",note:""};
    state.decisions[key].decision = valueButton.dataset.value;
    group.querySelectorAll("[data-value]").forEach(button => button.setAttribute("aria-pressed", String(button === valueButton)));
    save();
    return;
  }
  if (event.target.closest(".review-open") || event.target.closest("[data-open-review]")) setPanel(true);
  if (event.target.closest(".review-close") || event.target.closest("[data-scrim]")) setPanel(false);
});

document.addEventListener("input", event => {
  if (event.target.matches("[data-note]")) {
    const key = event.target.closest(".decision").dataset.key;
    state.decisions[key] = state.decisions[key] || {decision:"",note:""};
    state.decisions[key].note = event.target.value;
    save();
  }
  if (event.target.matches("[data-overall-note]")) { state.overallNote = event.target.value; save(); }
});

document.addEventListener("keydown", event => { if (event.key === "Escape" && panel.classList.contains("open")) setPanel(false); });
document.querySelector("#copy-review").addEventListener("click", async () => { await navigator.clipboard.writeText(JSON.stringify(exportRecord(), null, 2)); status.textContent = "Review JSON copied"; });
document.querySelector("#download-review").addEventListener("click", () => {
  const blob = new Blob([JSON.stringify(exportRecord(), null, 2)], {type:"application/json"});
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "mez-identity-product-object-02-review.json";
  link.click();
  URL.revokeObjectURL(link.href);
});

async function init() {
  renderReview();
  const response = await fetch("./assets/gradients/variants.json");
  if (!response.ok) throw new Error(`Gradient manifest returned ${response.status}`);
  const manifest = await response.json();
  const variant = {...manifest.variants[0], url:`./assets/gradients/${manifest.variants[0].asset}`};
  renderOpening(variant);
  renderMotion(variant);
  renderScale(variant);
  renderExpressions(variant);
  renderCollections(variant);
  hydrate();
}

init().catch(error => { console.error(error); document.body.dataset.renderError = "true"; });
