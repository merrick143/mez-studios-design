import { mountLivingCores } from "../../../../source-pack/design-system-export/mz-core.js";

/* Marquee content and motion allocation.

   Marks are resolved from the generated registry rather than hardcoded paths, so
   a refreshed mark cannot silently break the row. Every entry below has a real
   freestanding mark.svg. Hermes, OpenClaw and a Mez mark are deliberately absent:
   no asset exists for the first two, and inventing one is the defect this
   section already failed on twice.

   One Living Core across every candidate layer: a single renderer moves to
   whichever is most in view. The core mounts on the .layer element itself, which
   is intrinsically sized, never on an empty positioning layer. */

const CATALOGUE_URL = new URL("../../../../gradient-library/catalogue.json", import.meta.url);
const STATIC_BASE = new URL("../../../../gradient-library/assets/static/", import.meta.url);
const MARKS_BASE = new URL("../../../../assets/third-party-marks/", import.meta.url);

const query = new URLSearchParams(location.search);
const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
const forceStatic = reducedMotion || query.has("static") || query.has("no-webgl");

const MARKS = [
  ["openai", "OpenAI"], ["claude", "Claude"], ["gemini", "Gemini"], ["grok", "Grok"],
  ["mistral", "Mistral"], ["deepseek", "DeepSeek"], ["perplexity", "Perplexity"],
  ["midjourney", "Midjourney"], ["elevenlabs", "ElevenLabs"], ["notebooklm", "NotebookLM"],
  ["google-ai-studio", "Google AI Studio"], ["character-ai", "Character.AI"],
  ["v0", "v0"], ["lovable", "Lovable"], ["veo", "Veo"], ["seedance", "Seedance"]
];

/* --- marquee ------------------------------------------------------------- */
/* The track holds the set twice so translateX(-50%) loops seamlessly. The
   duplicate is aria-hidden: it is the same content, and a screen reader should
   hear the list once. */
function buildTrack(track) {
  const pass = hidden =>
    MARKS.map(([slug, name]) => {
      const img = document.createElement("img");
      img.className = "mk";
      img.src = new URL(`marks/${slug}/logos/mark.svg`, MARKS_BASE).href;
      img.alt = hidden ? "" : name;
      if (hidden) img.setAttribute("aria-hidden", "true");
      img.loading = "lazy";
      img.decoding = "async";
      return img;
    });
  [...pass(false), ...pass(true)].forEach(node => track.append(node));
}
document.querySelectorAll("[data-marquee]").forEach(buildTrack);

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
