import { mountLivingCores } from "../../../../source-pack/design-system-export/mz-core.js";

/* GH-S04 lab wiring.

   Deliberately simpler than the principle lab. S03 owns the cycling product
   family: its argument is "all five sit inside the layer", so its core walks the
   whole registry. S04's argument is "the one that shipped came out of our own
   business", so the material here is fixed to the AI OS and never cycles. Two
   adjacent sections running the same material trick would read as a page effect
   rather than two arguments.

   MOT-01 still holds: one live core across the whole lab, handed to whichever
   variant is most visible. */

const CATALOGUE_URL = new URL("../../../../gradient-library/catalogue.json", import.meta.url);
const STATIC_BASE = new URL("../../../../gradient-library/assets/static/", import.meta.url);

const AI_OS = "MZ-G13";
const query = new URLSearchParams(location.search);
const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
const forceStatic = reducedMotion || query.has("static") || query.has("no-webgl");

const twin = id => new URL(`${id.toLowerCase()}.webp`, STATIC_BASE).href;

/* Every material surface gets its exact static twin as a CSS background, so the
   no-WebGL and reduced-motion paths land on the same image the core renders. */
document.querySelectorAll("[data-material]").forEach(node => {
  node.style.setProperty("--material", `url("${twin(node.dataset.material || AI_OS)}")`);
});

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
    const shape = anchor.dataset.coreShape || "rect";
    const radius = Number(anchor.dataset.coreRadius || 0.06);
    renderer.mount(anchor, AI_OS, { shape, radius, profile: "deep" });
    anchor.dataset.mzCore = AI_OS;
    activeAnchor = anchor;
    setBadge(anchor, "on");
  } catch (error) {
    document.documentElement.dataset.coreFailure = error?.message || "unknown";
  }
}

/* --- variant A: the seam ---------------------------------------------------

   The seam is a compositional line, not a control. It has no handle, it cannot
   be dragged, and it is driven only by how far the card has travelled through
   the viewport. Under reduced motion it parks at the halfway point, where both
   halves of the argument are legible at once. */

const seamHosts = [...document.querySelectorAll("[data-seam]")];
const SEAM_START = 88;
const SEAM_END = 10;

function paintSeams() {
  seamHosts.forEach(host => {
    const box = host.getBoundingClientRect();
    const span = window.innerHeight + box.height;
    const travelled = (window.innerHeight - box.top) / span;
    const eased = Math.min(1, Math.max(0, (travelled - 0.18) / 0.5));
    host.style.setProperty("--seam", `${SEAM_START - (SEAM_START - SEAM_END) * eased}%`);
  });
}

if (reducedMotion) {
  seamHosts.forEach(host => host.style.setProperty("--seam", "50%"));
} else if (seamHosts.length) {
  let queued = false;
  const schedule = () => {
    if (queued) return;
    queued = true;
    requestAnimationFrame(() => { queued = false; paintSeams(); });
  };
  addEventListener("scroll", schedule, { passive: true });
  addEventListener("resize", schedule);
  paintSeams();
}

/* --- motion allocation ----------------------------------------------------- */

if (forceStatic) {
  document.documentElement.dataset.motion = "static";
} else {
  try {
    const response = await fetch(CATALOGUE_URL);
    if (!response.ok) throw new Error("Living Core catalogue unavailable");
    const catalogue = await response.json();
    const mounted = await mountLivingCores(document, {
      catalogue,
      selector: "[data-why-lab-never]",
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
  anchors.forEach(anchor => observer.observe(anchor));
}
