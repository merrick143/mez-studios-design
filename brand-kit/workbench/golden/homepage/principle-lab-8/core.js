import { mountLivingCores } from "../../../../source-pack/design-system-export/mz-core.js";

/* One core, five products.

   The renderer can swap the gradient on a mounted surface with setCore(), which
   keeps the same canvas and the same WebGL context. What it cannot do is blend:
   the swap is a hard cut. So the transition rides the exact static twins that
   already exist for every core:

     1. fade the next product's static twin in over the live canvas
     2. swap the core underneath it, hidden by the twin
     3. fade the twin back out, revealing the live core on the new product

   The result reads as a slow cross-fade through the product family while exactly
   one WebGL context is ever alive. The element's CSS background is updated in
   step 2 as well, so the no-WebGL fallback lands on the same product. */

const CATALOGUE_URL = new URL("../../../../gradient-library/catalogue.json", import.meta.url);
const STATIC_BASE = new URL("../../../../gradient-library/assets/static/", import.meta.url);
const MARKS_BASE = new URL("../../../../assets/third-party-marks/", import.meta.url);

const query = new URLSearchParams(location.search);
const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
const forceStatic = reducedMotion || query.has("static") || query.has("no-webgl");

/* The five products in the registry, in gradient order. */
const PRODUCTS = [
  ["MZ-G13", "AI OS"], ["MZ-G12", "Context Engine"], ["MZ-G06", "AI Ads System"],
  ["MZ-G15", "Claude Code OS"], ["MZ-G20", "Organic Content OS"]
];

const HARNESSES = [
  ["chatgpt", "ChatGPT"], ["claude", "Claude"], ["gemini", "Gemini"],
  ["grok", "Grok"], ["mistral", "Mistral"], ["perplexity", "Perplexity"]
];

const CONNECTIONS = [
  ["stripe", "Stripe"], ["notion", "Notion"], ["shopify", "Shopify"], ["figma", "Figma"],
  ["github", "GitHub"], ["gmail", "Gmail"], ["supabase", "Supabase"], ["vercel", "Vercel"],
  ["n8n", "n8n"], ["canva", "Canva"], ["miro", "Miro"], ["clickup", "ClickUp"],
  ["loom", "Loom"], ["meta", "Meta"]
];

const twin = id => new URL(`${id.toLowerCase()}.webp`, STATIC_BASE).href;
const markSrc = slug => new URL(`marks/${slug}/logos/mark.svg`, MARKS_BASE).href;

function makeMark(slug, name, cls, hidden) {
  const img = document.createElement("img");
  img.className = cls;
  img.src = markSrc(slug);
  img.alt = hidden ? "" : name;
  if (hidden) img.setAttribute("aria-hidden", "true");
  img.loading = "lazy";
  img.decoding = "async";
  return img;
}

/* --- content ------------------------------------------------------------- */
document.querySelectorAll("[data-harnesses]").forEach(host => {
  HARNESSES.forEach(([slug, name]) => {
    const cell = document.createElement("span");
    cell.className = "harness";
    cell.append(makeMark(slug, name, "mk mk--harness", false));
    const label = document.createElement("span");
    label.className = "harness__name";
    label.textContent = name;
    cell.append(label);
    host.append(cell);
  });
});

document.querySelectorAll("[data-connections]").forEach(host => {
  const passes = host.hasAttribute("data-loop") ? [false, true] : [false];
  passes.forEach(hidden =>
    CONNECTIONS.forEach(([slug, name]) => host.append(makeMark(slug, name, "mk mk--tool", hidden)))
  );
});

document.querySelectorAll("[data-orbit]").forEach(ring => {
  const kind = ring.dataset.orbit;
  const set = kind === "harnesses" ? HARNESSES : CONNECTIONS.slice(0, 10);
  set.forEach(([slug, name], index) => {
    const angle = (360 / set.length) * index;
    const slot = document.createElement("span");
    slot.className = "orbit__slot";
    slot.style.setProperty("--a", `${angle}deg`);
    const upright = document.createElement("span");
    upright.className = "orbit__upright";
    upright.append(makeMark(slug, name, kind === "harnesses" ? "mk mk--harness" : "mk mk--tool", false));
    slot.append(upright);
    ring.append(slot);
  });
});

/* Every core surface gets a veil for the cross-fade and a product caption. */
document.querySelectorAll("[data-live-anchor]").forEach(anchor => {
  const veil = document.createElement("img");
  veil.className = "veil";
  veil.alt = "";
  veil.setAttribute("aria-hidden", "true");
  veil.src = twin(PRODUCTS[0][0]);
  anchor.prepend(veil);
});

/* --- motion allocation and the product cycle ------------------------------ */
const anchors = [...document.querySelectorAll("[data-live-anchor]")];
const badges = new Map(
  [...document.querySelectorAll("[data-live-badge]")].map(node => [node.dataset.liveBadge, node])
);
const captions = [...document.querySelectorAll("[data-product-name]")];

let renderer = null;
let activeAnchor = null;
let productIndex = 0;
let cycleTimer = null;

function setBadge(anchor, state) {
  const badge = badges.get(anchor?.dataset.liveAnchor);
  if (!badge) return;
  badge.textContent = state === "on" ? "Core live" : "Core idle";
  badge.dataset.live = state;
}

function paintCaptions() {
  const name = PRODUCTS[productIndex][1];
  captions.forEach(node => { node.textContent = name; });
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
    const shape = anchor.dataset.coreShape || "rect";
    const radius = Number(anchor.dataset.coreRadius || 0.06);
    renderer.mount(anchor, PRODUCTS[productIndex][0], { shape, radius, profile: "deep" });
    anchor.dataset.mzCore = PRODUCTS[productIndex][0];
    activeAnchor = anchor;
    setBadge(anchor, "on");
  } catch (error) {
    document.documentElement.dataset.coreFailure = error?.message || "unknown";
  }
}

const FADE = 1100;
const HOLD = 4200;

async function advance() {
  if (!renderer || !activeAnchor || forceStatic) return;
  const next = (productIndex + 1) % PRODUCTS.length;
  const [id] = PRODUCTS[next];
  const veil = activeAnchor.querySelector(".veil");
  if (!veil) return;

  veil.src = twin(id);
  await new Promise(r => (veil.complete ? r() : veil.addEventListener("load", r, { once: true })));

  veil.style.opacity = "1";
  await new Promise(r => setTimeout(r, FADE));

  try {
    renderer.setCore(activeAnchor, id);
    activeAnchor.dataset.mzCore = id;
    activeAnchor.style.backgroundImage = `url("${twin(id)}")`;
  } catch (error) {
    document.documentElement.dataset.coreFailure = error?.message || "unknown";
  }
  productIndex = next;
  paintCaptions();

  await new Promise(r => requestAnimationFrame(r));
  veil.style.opacity = "0";
}

paintCaptions();

if (forceStatic) {
  document.documentElement.dataset.motion = "static";
} else {
  try {
    const response = await fetch(CATALOGUE_URL);
    if (!response.ok) throw new Error("Living Core catalogue unavailable");
    const catalogue = await response.json();
    const mounted = await mountLivingCores(document, {
      catalogue,
      selector: "[data-principle-lab-never]",
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
      if (best && best[1] > 0.25) mount(best[0]);
    },
    { threshold: [0, 0.25, 0.5, 0.75, 1] }
  );
  anchors.forEach(anchor => observer.observe(anchor));

  cycleTimer = setInterval(advance, HOLD + FADE);
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) { clearInterval(cycleTimer); cycleTimer = null; }
    else if (!cycleTimer) cycleTimer = setInterval(advance, HOLD + FADE);
  });
}
