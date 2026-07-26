import { mountLivingCores } from "../../../../source-pack/design-system-export/mz-core.js";

/* GH-S04 bento lab, round two.

   The allocation rule from brand-kit/references/premium-neutral-with-one-colour-event:

     One material cell per bento. It carries the proof or the product. Every other
     cell is paper or charcoal.

   Round one put registry material on every cell in variants 4 and 7 and Olli
   rejected it by name. Colour is only expensive against restraint; spread across
   every cell it becomes wallpaper. So the coming products in variant 4 are paper
   cells carrying a small material disc as an identity token, which is existing
   grammar from GH-S08, rather than five full material fields. */

const PRODUCTS_URL = new URL("../../../../registry/products.json", import.meta.url);
const CATALOGUE_URL = new URL("../../../../gradient-library/catalogue.json", import.meta.url);
const STATIC_BASE = new URL("../../../../gradient-library/assets/static/", import.meta.url);
const WINGS = new URL("../../../../source-pack/design-system-export/assets/wings.svg", import.meta.url);

const AI_OS = "MZ-G13";
const query = new URLSearchParams(location.search);
const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
const forceStatic = reducedMotion || query.has("static") || query.has("no-webgl");

const twin = id => new URL(`${id.toLowerCase()}.webp`, STATIC_BASE).href;
const esc = value => String(value).replace(/[&<>'"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" })[c]);

const response = await fetch(PRODUCTS_URL);
if (!response.ok) throw new Error("Canonical product registry unavailable");
const { products } = await response.json();

/* Availability sets the treatment, and nothing counts products, so the layout
   survives the registry gaining or losing one (LAY-09). */
function cell(product, anchor) {
  if (product.availability === "live") {
    return `
    <article class="c c--mat is-live c--l" style="--material:url('${twin(product.gradientId)}')"
      ${anchor ? `data-live-anchor="${anchor}" data-core-gradient="${esc(product.gradientId)}" data-core-shape="rect" data-core-radius="0.055"` : ""}>
      <div class="c__body">
        <img class="c__wings" src="${WINGS.href}" alt="" />
        <p class="c__t">${esc(product.publicName)}</p>
        <p class="c__s">${esc(product.function)}</p>
      </div>
    </article>`;
  }
  return `
    <article class="c c--paper c--s">
      <i class="disc" style="--material:url('${twin(product.gradientId)}')" aria-hidden="true"></i>
      <div class="c__body">
        <p class="c__t">${esc(product.publicName)}</p>
        <p class="c__s">${esc(product.function)}</p>
      </div>
    </article>`;
}

document.querySelectorAll("[data-registry-bento]").forEach(host => {
  const key = host.dataset.registryBento;
  const ordered = [...products].sort(
    (a, b) => (a.availability === "live" ? -1 : 0) - (b.availability === "live" ? -1 : 0)
  );
  host.innerHTML = ordered.map((product, index) => cell(product, index === 0 ? key : null)).join("");
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
