import { mountLivingCores } from "../../../../source-pack/design-system-export/mz-core.js";

/* GH-S04 bento lab.

   Two variants are built from the product registry rather than authored cell by
   cell, because LAY-09 says a layout must survive the registry returning a
   different number of products. Render with n-1 and n+1 and neither breaks: the
   span rule is a function of availability and index, not a hardcoded five. */

const PRODUCTS_URL = new URL("../../../../registry/products.json", import.meta.url);
const CATALOGUE_URL = new URL("../../../../gradient-library/catalogue.json", import.meta.url);
const STATIC_BASE = new URL("../../../../gradient-library/assets/static/", import.meta.url);
const WINGS = new URL("../../../../source-pack/design-system-export/assets/wings.svg", import.meta.url);

const AI_OS = "MZ-G13";
const query = new URLSearchParams(location.search);
const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
const forceStatic = reducedMotion || query.has("static") || query.has("no-webgl");

const twin = id => new URL(`${id.toLowerCase()}.webp`, STATIC_BASE).href;
const escape = value => String(value).replace(/[&<>'"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" })[c]);

/* --- registry-driven cells ------------------------------------------------- */

const response = await fetch(PRODUCTS_URL);
if (!response.ok) throw new Error("Canonical product registry unavailable");
const { products } = await response.json();

/* Availability sets the cell weight. Nothing counts products.

   ICO-05: Wings are composed, not sprinkled. They appear on the dominant cell,
   where identity is the focal event, and are omitted from the small cells where
   the material already fills the field and a second mark would be clutter. */
const cell = (product, anchor) => {
  const live = product.availability === "live";
  return `
  <article class="c c--mat ${live ? "is-live c--l" : "c--s"}"
    style="--material:url('${twin(product.gradientId)}')"
    ${anchor ? `data-live-anchor="${anchor}" data-core-gradient="${escape(product.gradientId)}" data-core-shape="rect" data-core-radius="0.055"` : ""}>
    <div class="c__body">
      ${live ? `<img class="c__wings" src="${WINGS.href}" alt="" />` : ""}
      <p class="c__t">${escape(product.publicName)}</p>
      <p class="c__s">${escape(product.function)}</p>
    </div>
  </article>`;
};

document.querySelectorAll("[data-registry-bento]").forEach(host => {
  const key = host.dataset.registryBento;
  const ordered = host.hasAttribute("data-live-first")
    ? [...products].sort((a, b) => (a.availability === "live" ? -1 : 0) - (b.availability === "live" ? -1 : 0))
    : products;
  host.innerHTML = ordered
    .map((product, index) => cell(product, index === 0 ? key : null))
    .join("");
});

/* --- motion allocation ----------------------------------------------------- */

document.querySelectorAll("[data-material]").forEach(node => {
  node.style.setProperty("--material", `url("${twin(node.dataset.material || AI_OS)}")`);
});

const badges = new Map(
  [...document.querySelectorAll("[data-live-badge]")].map(node => [node.dataset.liveBadge, node])
);

let renderer = null;
let activeAnchor = null;

function setBadge(anchor, state) {
  const badge = badges.get(anchor?.dataset.liveAnchor);
  if (!badge) return;
  badge.textContent = state === "on" ? "Core live" : "Core idle";
  badge.dataset.live = state;
}

function unmount(anchor) {
  if (!anchor) return;
  renderer?.surfaces?.delete(anchor);
  anchor.querySelector("canvas[data-mz-core-canvas]")?.remove();
  anchor.removeAttribute("data-mz-core");
  setBadge(anchor, "off");
}

function mount(anchor) {
  if (!renderer || forceStatic || !anchor || activeAnchor === anchor) return;
  unmount(activeAnchor);
  try {
    renderer.mount(anchor, anchor.dataset.coreGradient || AI_OS, {
      shape: anchor.dataset.coreShape || "rect",
      radius: Number(anchor.dataset.coreRadius || 0.055),
      profile: "deep"
    });
    anchor.dataset.mzCore = anchor.dataset.coreGradient || AI_OS;
    activeAnchor = anchor;
    setBadge(anchor, "on");
  } catch (error) {
    document.documentElement.dataset.coreFailure = error?.message || "unknown";
  }
}

if (forceStatic) {
  document.documentElement.dataset.motion = "static";
} else {
  try {
    const catalogueResponse = await fetch(CATALOGUE_URL);
    if (!catalogueResponse.ok) throw new Error("Living Core catalogue unavailable");
    const mounted = await mountLivingCores(document, {
      catalogue: await catalogueResponse.json(),
      selector: "[data-bento-lab-never]",
      staticBaseUrl: STATIC_BASE
    });
    renderer = mounted.renderer;
  } catch (error) {
    document.documentElement.dataset.coreFailure = error?.message || "unknown";
  }

  const visibility = new Map();
  const observer = new IntersectionObserver(
    entries => {
      entries.forEach(entry => visibility.set(entry.target, entry.intersectionRatio));
      const [best] = [...visibility.entries()].sort((a, b) => b[1] - a[1]);
      if (best && best[1] > 0.2) mount(best[0]);
    },
    { threshold: [0, 0.2, 0.4, 0.6, 0.8, 1] }
  );
  document.querySelectorAll("[data-live-anchor]").forEach(anchor => observer.observe(anchor));
}
