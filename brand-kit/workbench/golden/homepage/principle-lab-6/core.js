import { mountLivingCores } from "../../../../source-pack/design-system-export/mz-core.js";

/* Two tiers of marks, one Living Core.

   AI operating systems are the things a business actually runs on, and they are
   the churning tier, so they marquee. Business tools are what the company has
   chosen and kept, so they sit still. One moving row plus the living material is
   the whole motion budget for this section.

   Every slug below is form: "symbol" in the generated registry. That field
   exists because not every file named mark.svg is a freestanding symbol: two
   vendors ship a horizontal wordmark under the same name, and dropping one into
   a row of symbols wrecks the row. Filter on form, never on filename. */

const CATALOGUE_URL = new URL("../../../../gradient-library/catalogue.json", import.meta.url);
const STATIC_BASE = new URL("../../../../gradient-library/assets/static/", import.meta.url);
const MARKS_BASE = new URL("../../../../assets/third-party-marks/", import.meta.url);

const query = new URLSearchParams(location.search);
const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
const forceStatic = reducedMotion || query.has("static") || query.has("no-webgl");

/* The systems you run the business from. Claude Code has no third-party mark of
   its own, so Claude stands for it.

   Manus is excluded. It is raster-only, and its file is a filled app icon rather
   than a transparent symbol, so recolouring it to a single ink produces a solid
   block. Same failure class as the two wordmarks: the asset is not a freestanding
   symbol. It can join the row when a real transparent mark exists. */
const SYSTEMS = [
  ["chatgpt", "ChatGPT", "svg"], ["claude", "Claude", "svg"], ["gemini", "Gemini", "svg"],
  ["grok", "Grok", "svg"], ["mistral", "Mistral", "svg"], ["perplexity", "Perplexity", "svg"],
  ["deepseek", "DeepSeek", "svg"]
];

/* What the business already uses. These are chosen and kept, not swapped. */
const TOOLS = [
  ["stripe", "Stripe"], ["notion", "Notion"], ["shopify", "Shopify"], ["github", "GitHub"],
  ["figma", "Figma"], ["gmail", "Gmail"], ["supabase", "Supabase"], ["vercel", "Vercel"],
  ["n8n", "n8n"], ["clickup", "ClickUp"]
];

function markSrc(slug, kind) {
  const path = kind === "raster" ? `marks/${slug}/logos/raster/mark-512.png` : `marks/${slug}/logos/mark.svg`;
  return new URL(path, MARKS_BASE).href;
}

function makeMark(slug, name, kind, hidden) {
  const img = document.createElement("img");
  img.className = "mk";
  img.src = markSrc(slug, kind);
  img.alt = hidden ? "" : name;
  if (hidden) img.setAttribute("aria-hidden", "true");
  img.loading = "lazy";
  img.decoding = "async";
  return img;
}

/* The track holds the set twice so translateX(-50%) loops seamlessly. The second
   pass is aria-hidden: same content, and it should be announced once. */
document.querySelectorAll("[data-marquee]").forEach(track => {
  [false, true].forEach(hidden =>
    SYSTEMS.forEach(([slug, name, kind]) => track.append(makeMark(slug, name, kind, hidden)))
  );
});

document.querySelectorAll("[data-tools]").forEach(row => {
  TOOLS.forEach(([slug, name]) => row.append(makeMark(slug, name, "svg", false)));
});

/* --- motion allocation --------------------------------------------------- */
const anchors = [...document.querySelectorAll("[data-live-anchor]")];
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
    renderer.mount(anchor, anchor.dataset.gradientId, { shape: "rect", radius: 0.06, profile: "deep" });
    anchor.dataset.mzCore = anchor.dataset.gradientId;
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
}
