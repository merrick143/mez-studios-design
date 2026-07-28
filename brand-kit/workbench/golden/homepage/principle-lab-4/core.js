import { mountLivingCores } from "../../../../source-pack/design-system-export/mz-core.js";

/* Motion allocation for the lab.
   Six candidate bars, one Living Core. A single renderer moves to whichever bar
   is most in view and unmounts the previous one, so exactly one WebGL context
   exists at any moment. This is the same allocation the homepage runs; the lab
   only differs in having six candidates on one page.

   The core mounts directly on the .layer element, which is intrinsically sized
   by its own min-height. Mounting on an empty positioning layer is what caused
   the Golden Homepage R03 to R05 "not animated" defect: mount() stamps inline
   position:relative, inline beats the stylesheet, and the host collapses to 0x0
   leaving only the static twin visible. */

const CATALOGUE_URL = new URL("../../../../gradient-library/catalogue.json", import.meta.url);
const STATIC_BASE = new URL("../../../../gradient-library/assets/static/", import.meta.url);

const query = new URLSearchParams(location.search);
const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
const forceStatic = reducedMotion || query.has("static") || query.has("no-webgl");

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
    renderer.mount(anchor, anchor.dataset.gradientId, { shape: "rect", radius: 0.08, profile: "deep" });
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
      // Nothing auto-mounts: allocation is decided by the observer below.
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
