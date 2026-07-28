import { mountLivingCores } from "../../../../source-pack/design-system-export/mz-core.js";

const PRODUCTS_URL = new URL("../../../../registry/products.json", import.meta.url);
const CATALOGUE_URL = new URL("../../../../gradient-library/catalogue.json", import.meta.url);
const STATIC_BASE = new URL("../../../../gradient-library/assets/static/", import.meta.url);
const WINGS_URL = new URL("../../../../source-pack/design-system-export/assets/wings.svg", import.meta.url);

const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
const params = new URLSearchParams(location.search);
const forceStatic = params.has("static") || reducedMotion;
const disableWebGL = params.has("no-webgl");

// Research-only render evidence. `?proof` counts real WebGL draw calls without
// changing the canonical renderer or the visual behaviour of the lab.
if (params.has("proof")) {
  document.documentElement.dataset.mzDrawCalls = "0";
  [window.WebGLRenderingContext, window.WebGL2RenderingContext]
    .filter(Boolean)
    .forEach(Context => {
      ["drawArrays", "drawElements"].forEach(method => {
        const original = Context.prototype[method];
        if (typeof original !== "function") return;
        Context.prototype[method] = function countedDrawCall(...args) {
          document.documentElement.dataset.mzDrawCalls = String(
            Number(document.documentElement.dataset.mzDrawCalls || 0) + 1
          );
          return original.apply(this, args);
        };
      });
    });
}
const esc = value => String(value).replace(/[&<>'"]/g, character => ({
  "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;"
}[character]));
const twin = gradientId => new URL(`${gradientId.toLowerCase()}.webp`, STATIC_BASE).href;

const productRegistry = await (await fetch(PRODUCTS_URL)).json();
const products = productRegistry.products.filter(product => product.availability === "coming-soon");

const variants = [
  { id: "V01", name: "Living directory", note: "Names control one shared hover-live sphere", layout: "directory" },
  { id: "V02", name: "Unboxed disc rail", note: "Open static discs · hovered disc becomes live", layout: "discs" },
  { id: "V03", name: "Wings ledger", note: "Rare gradient-Wings expression · no card chassis", layout: "wings" },
  { id: "V04", name: "Expression bento", note: "One promoted live sphere · four static selectors", layout: "bento" },
  { id: "V05", name: "Clear disc cards", note: "Disc, name and status · no background fill", layout: "clear" }
];

function sectionIntro() {
  return `
    <header class="section-intro">
      <div class="section-intro__lead">
        <p class="eyebrow">Coming next</p>
        <h2>Specialised systems for the work AI-native businesses do.</h2>
      </div>
      <div class="section-intro__aside">
        <p class="section-lead">One bloated product should not run every part of the company.</p>
        <p>Mez Systems builds focused operating systems around specific problems, while the customer keeps the context, workflow and history underneath them.</p>
      </div>
    </header>`;
}

function staticStyle(product) {
  return `--field:url('${twin(product.gradientId)}')`;
}

function coreHost(product, shape = "disc", extraClass = "", live = true) {
  const wings = shape === "wings" ? "" : `<img src="${WINGS_URL.href}" alt="" />`;
  return `<span class="core-host core-host--${shape} ${extraClass}" style="${staticStyle(product)}" data-gradient-id="${esc(product.gradientId)}" data-shape="${shape}"${live ? " data-live-host" : ""} aria-hidden="true">${wings}</span>`;
}

function productCopy(product, className = "product-copy") {
  return `<span class="${className}"><strong>${esc(product.publicName)}</strong><small>Coming soon</small></span>`;
}

function directory() {
  const first = products[0];
  return `
    <div class="living-directory" data-directory>
      <div class="directory-list" aria-label="Choose a coming Mez System">
        ${products.map((product, index) => `
          <button type="button" class="directory-row" data-directory-item data-index="${index}" aria-pressed="${index === 0}">
            <span>${esc(product.publicName)}</span><small>Coming soon</small><i aria-hidden="true">↗</i>
          </button>`).join("")}
      </div>
      <div class="directory-preview">
        ${coreHost(first, "sphere", "directory-sphere", false)}
        <div class="directory-preview__copy" aria-live="polite">
          <strong data-preview-name>${esc(first.publicName)}</strong>
          <span data-preview-status>Hover or focus a system</span>
        </div>
      </div>
    </div>`;
}

function discRail() {
  return `
    <div class="disc-rail" role="list" aria-label="The four coming Mez Systems">
      ${products.map(product => `
        <button type="button" class="disc-item" role="listitem" aria-label="Animate ${esc(product.publicName)}">
          ${coreHost(product, "disc", "disc-item__core")}
          ${productCopy(product)}
        </button>`).join("")}
    </div>`;
}

function wingsLedger() {
  return `
    <div class="wings-ledger" role="list" aria-label="The four coming Mez Systems">
      ${products.map(product => `
        <button type="button" class="wings-row" role="listitem" aria-label="Animate ${esc(product.publicName)} Wings">
          ${coreHost(product, "wings", "wings-row__mark")}
          ${productCopy(product)}
          <span class="wings-row__hint">Hover to live</span>
        </button>`).join("")}
    </div>`;
}

function expressionBento() {
  const first = products[0];
  return `
    <div class="expression-bento" data-bento>
      <article class="bento-lead">
        ${coreHost(first, "sphere", "bento-sphere", false)}
        <div class="bento-lead__copy" aria-live="polite">
          <span>Coming next</span>
          <strong data-preview-name>${esc(first.publicName)}</strong>
          <small data-preview-status>Hover or focus a product</small>
        </div>
      </article>
      <div class="bento-selectors" aria-label="Choose a coming Mez System">
        ${products.map((product, index) => `
          <button type="button" class="bento-selector" data-bento-item data-index="${index}" aria-pressed="${index === 0}">
            ${coreHost(product, "disc", "bento-selector__disc", false)}
            <strong>${esc(product.publicName)}</strong>
          </button>`).join("")}
      </div>
    </div>`;
}

function clearCards() {
  return `
    <div class="clear-grid" role="list" aria-label="The four coming Mez Systems">
      ${products.map(product => `
        <button type="button" class="clear-card" role="listitem" aria-label="Animate ${esc(product.publicName)}">
          ${coreHost(product, "disc", "clear-card__disc")}
          ${productCopy(product)}
          <span class="clear-card__arrow" aria-hidden="true">↗</span>
        </button>`).join("")}
    </div>`;
}

const compositions = { directory, discs: discRail, wings: wingsLedger, bento: expressionBento, clear: clearCards };
const main = document.querySelector("[data-variants]");
main.innerHTML = variants.map(variant => `
  <section class="lab" id="${variant.id.toLowerCase()}" data-variant="${variant.id}">
    <header class="lab-head">
      <div class="lab-head__identity"><span>${variant.id}</span><h1>${variant.name}</h1><p>${variant.note}</p></div>
      <div class="verdicts" role="group" aria-label="Verdict for ${variant.id}">
        <button type="button" data-verdict="keep">Keep</button>
        <button type="button" data-verdict="maybe">Maybe</button>
        <button type="button" data-verdict="kill">Kill</button>
      </div>
    </header>
    <div class="stage">${sectionIntro()}${compositions[variant.layout]()}</div>
  </section>`).join("");

document.querySelector("[data-nav]").innerHTML = variants
  .map(variant => `<a href="#${variant.id.toLowerCase()}">${variant.id.slice(1)}</a>`)
  .join("");

/* One shared renderer. Every expression is exact-static at rest and mounts only
   while its hover/focus interaction owns attention. */
let renderer = null;
let activeHost = null;

function unmountActive() {
  if (!activeHost || !renderer) return;
  renderer.surfaces?.delete(activeHost);
  activeHost.querySelector("canvas[data-mz-core-canvas]")?.remove();
  activeHost.removeAttribute("data-mz-core");
  activeHost.classList.remove("is-live");
  activeHost = null;
}

function mountHost(host) {
  if (!renderer || forceStatic || disableWebGL || !host) return;
  if (activeHost === host) return;
  unmountActive();
  try {
    const state = renderer.mount(host, host.dataset.gradientId, {
      shape: host.dataset.shape || "disc",
      radius: 0,
      profile: "deep"
    });
    state.speed = 1.4;
    state.speedTarget = 1.85;
    host.dataset.mzCore = host.dataset.gradientId;
    host.dataset.mzCoreSpeed = "1.85";
    host.classList.add("is-live");
    activeHost = host;
  } catch (error) {
    document.documentElement.dataset.coreFailure = error?.message || "unknown";
  }
}

function setPreview(container, product, hostSelector) {
  const host = container.querySelector(hostSelector);
  host.dataset.gradientId = product.gradientId;
  host.style.setProperty("--field", `url('${twin(product.gradientId)}')`);
  container.querySelector("[data-preview-name]").textContent = product.publicName;
  container.querySelector("[data-preview-status]").textContent = "Coming soon · material live";
  mountHost(host);
}

document.querySelectorAll("[data-live-host]").forEach(host => {
  const owner = host.closest("button") || host;
  owner.addEventListener("pointerenter", () => mountHost(host));
  owner.addEventListener("pointerleave", unmountActive);
  owner.addEventListener("focusin", () => mountHost(host));
  owner.addEventListener("focusout", unmountActive);
});

document.querySelectorAll("[data-directory-item]").forEach(button => {
  const activate = () => {
    const directoryRoot = button.closest("[data-directory]");
    const product = products[Number(button.dataset.index)];
    directoryRoot.querySelectorAll("[data-directory-item]").forEach(item => item.setAttribute("aria-pressed", String(item === button)));
    setPreview(directoryRoot, product, ".directory-sphere");
  };
  button.addEventListener("pointerenter", activate);
  button.addEventListener("pointerleave", unmountActive);
  button.addEventListener("focus", activate);
  button.addEventListener("blur", unmountActive);
});

document.querySelectorAll("[data-bento-item]").forEach(button => {
  const activate = () => {
    const bento = button.closest("[data-bento]");
    const product = products[Number(button.dataset.index)];
    bento.querySelectorAll("[data-bento-item]").forEach(item => item.setAttribute("aria-pressed", String(item === button)));
    setPreview(bento, product, ".bento-sphere");
  };
  button.addEventListener("pointerenter", activate);
  button.addEventListener("pointerleave", unmountActive);
  button.addEventListener("focus", activate);
  button.addEventListener("blur", unmountActive);
});

if (!forceStatic && !disableWebGL) {
  try {
    const catalogue = await (await fetch(CATALOGUE_URL)).json();
    const mounted = await mountLivingCores(document, {
      catalogue,
      selector: "[data-never-auto-mount]",
      staticBaseUrl: STATIC_BASE
    });
    renderer = mounted.renderer;
    document.documentElement.dataset.coreMode = mounted.mode;
  } catch (error) {
    document.documentElement.dataset.coreMode = "static";
    document.documentElement.dataset.coreFailure = error?.message || "unknown";
  }
} else {
  document.documentElement.dataset.coreMode = forceStatic ? "static" : "no-webgl";
}

const storageKey = "mez-ecosystem-expression-lab-v2";
let verdictState = {};
try { verdictState = JSON.parse(localStorage.getItem(storageKey) || "{}"); } catch { verdictState = {}; }

function paintVerdicts() {
  document.querySelectorAll("[data-variant]").forEach(section => {
    const selected = verdictState[section.dataset.variant];
    section.querySelectorAll("[data-verdict]").forEach(button => {
      button.setAttribute("aria-pressed", String(button.dataset.verdict === selected));
    });
  });
}

document.addEventListener("click", event => {
  const button = event.target.closest("[data-verdict]");
  if (!button) return;
  const section = button.closest("[data-variant]");
  verdictState[section.dataset.variant] = button.dataset.verdict;
  localStorage.setItem(storageKey, JSON.stringify(verdictState));
  paintVerdicts();
});

document.querySelector("[data-copy]").addEventListener("click", async () => {
  const lines = variants.map(({ id, name }) => `${id} ${name}: ${verdictState[id] || "unreviewed"}`);
  await navigator.clipboard.writeText(lines.join("\n"));
  const status = document.querySelector("[data-status]");
  status.textContent = "Verdicts copied";
  status.classList.add("is-visible");
  window.setTimeout(() => status.classList.remove("is-visible"), 1400);
});

paintVerdicts();
