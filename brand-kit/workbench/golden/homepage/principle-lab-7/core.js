import { mountLivingCores } from "../../../../source-pack/design-system-export/mz-core.js";

/* Three tiers, two registers of mark.

   HARNESSES are the systems a business is actually run from. They are named, set
   larger, and treated as first-class objects.
   CONNECTIONS are the tools the business already uses. They are small, unnamed
   and quiet. The visual difference between the two rows is the point: a harness
   is not a plugin.

   Every slug is form:"symbol" in the generated registry. Slack, Linear, HubSpot,
   Klaviyo, 1Password, Google Drive, Google Calendar, shadcn and MCP have no mark
   in the registry and are therefore absent rather than drawn. */

const CATALOGUE_URL = new URL("../../../../gradient-library/catalogue.json", import.meta.url);
const STATIC_BASE = new URL("../../../../gradient-library/assets/static/", import.meta.url);
const MARKS_BASE = new URL("../../../../assets/third-party-marks/", import.meta.url);

const query = new URLSearchParams(location.search);
const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
const forceStatic = reducedMotion || query.has("static") || query.has("no-webgl");

/* Claude Code has no mark of its own, so Claude stands for it. */
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

/* Harnesses, named. */
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

/* Connections, quiet. Doubled where the host is a marquee track. */
document.querySelectorAll("[data-connections]").forEach(host => {
  const passes = host.hasAttribute("data-loop") ? [false, true] : [false];
  passes.forEach(hidden =>
    CONNECTIONS.forEach(([slug, name]) => host.append(makeMark(slug, name, "mk mk--tool", hidden)))
  );
});

/* Orbit rings: marks are placed around the ring by angle, and each one carries a
   counter-rotation so the logo stays upright while the ring turns. */
document.querySelectorAll("[data-orbit]").forEach(ring => {
  const set = ring.dataset.orbit === "harnesses" ? HARNESSES : CONNECTIONS;
  const items = ring.dataset.orbit === "harnesses" ? set : set.slice(0, 10);
  items.forEach(([slug, name], index) => {
    const angle = (360 / items.length) * index;
    const slot = document.createElement("span");
    slot.className = "orbit__slot";
    slot.style.setProperty("--a", `${angle}deg`);
    const upright = document.createElement("span");
    upright.className = "orbit__upright";
    upright.append(makeMark(slug, name, ring.dataset.orbit === "harnesses" ? "mk mk--harness" : "mk mk--tool", false));
    slot.append(upright);
    ring.append(slot);
  });
});

/* --- motion allocation ---------------------------------------------------- */
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
    /* Shape comes from the anchor: disc and pill are canonical Mez expressions,
       not shapes invented for this section. */
    const shape = anchor.dataset.coreShape || "rect";
    const radius = Number(anchor.dataset.coreRadius || 0.06);
    renderer.mount(anchor, anchor.dataset.gradientId, { shape, radius, profile: "deep" });
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
