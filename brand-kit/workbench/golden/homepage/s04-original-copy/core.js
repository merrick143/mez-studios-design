import { mountLivingCores } from "../../../../source-pack/design-system-export/mz-core.js";

/* GH-S04 · ten treatments of the original copy.
 *
 * One live core across the whole page, handed to whichever material surface is
 * most visible (MOT-01). Every anchor already carries its exact static twin as a
 * CSS background, so reduced motion, no WebGL and a renderer failure all land on
 * the same image without a flash.
 *
 * mz-core renders every surface through one shared framebuffer capped at 2048
 * device pixels with dpr clamped to 2, so a surface wider than 1024 CSS pixels
 * is drawn from source that ran out and shows a hard seam near its right edge.
 * Anything wider keeps its twin rather than rendering broken.
 */

const CATALOGUE = new URL("../../../../gradient-library/catalogue.json", import.meta.url);
const STATIC_BASE = new URL("../../../../gradient-library/assets/static/", import.meta.url);
const PRODUCTS = new URL("../../../../registry/products.json", import.meta.url);

const query = new URLSearchParams(location.search);
const forceStatic = matchMedia("(prefers-reduced-motion: reduce)").matches || query.has("static") || query.has("no-webgl");
const twin = id => new URL(`${id.toLowerCase()}.webp`, STATIC_BASE).href;
const MAX_LIVE = () => 2048 / Math.min(devicePixelRatio || 1, 2);

const response = await fetch(PRODUCTS);
if (!response.ok) throw new Error("canonical product registry unavailable");
const aios = (await response.json()).products.find(p => p.slug === "aios");

/* Identity is never hardcoded: the gradient and the name come from the registry. */
document.querySelectorAll("[data-material]").forEach(node => {
  node.style.setProperty("--material", `url("${twin(aios.gradientId)}")`);
  node.dataset.gradientId = aios.gradientId;
});
document.querySelectorAll("[data-product-name]").forEach(n => { n.textContent = aios.publicName; });
document.querySelectorAll("[data-product-function]").forEach(n => { n.textContent = aios.function; });

if (!forceStatic) {
  let renderer = null;
  let active = null;
  try {
    const cat = await fetch(CATALOGUE);
    if (!cat.ok) throw new Error("Living Core catalogue unavailable");
    const mounted = await mountLivingCores(document, {
      catalogue: await cat.json(),
      selector: "[data-never]",
      staticBaseUrl: STATIC_BASE
    });
    renderer = mounted.renderer;
  } catch (error) {
    document.documentElement.dataset.coreFailure = error?.message || "unknown";
  }

  const ratios = new Map();
  const observer = new IntersectionObserver(entries => {
    entries.forEach(e => ratios.set(e.target, e.intersectionRatio));
    const [best] = [...ratios.entries()].sort((a, b) => b[1] - a[1]);
    if (!renderer || !best || best[1] <= 0.2 || active === best[0]) return;
    const anchor = best[0];
    if (anchor.getBoundingClientRect().width > MAX_LIVE()) {
      anchor.dataset.coreSkipped = "wider than the renderer framebuffer";
      return;
    }
    if (active) {
      renderer.surfaces?.delete(active);
      active.querySelector("canvas[data-mz-core-canvas]")?.remove();
      active.removeAttribute("data-mz-core");
    }
    try {
      renderer.mount(anchor, anchor.dataset.gradientId, {
        shape: anchor.dataset.coreShape || "rect",
        radius: Number(anchor.dataset.coreRadius || 0.06),
        profile: "deep"
      });
      anchor.dataset.mzCore = anchor.dataset.gradientId;
      active = anchor;
    } catch (error) {
      document.documentElement.dataset.coreFailure = error?.message || "unknown";
    }
  }, { threshold: [0, 0.2, 0.4, 0.6, 0.8, 1] });

  document.querySelectorAll("[data-material]").forEach(n => observer.observe(n));
} else {
  document.documentElement.dataset.motion = "static";
}
