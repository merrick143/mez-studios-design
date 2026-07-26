import { mountLivingCores } from "../../../../source-pack/design-system-export/mz-core.js";

/* GH-S04 · nine expressions of the thing that ships.
 *
 * Each section blends between two live cores rather than fading through a still,
 * so both sides of every transition are moving. Two surfaces on the one WebGL
 * context; the renderer keeps surfaces in a Map, which is how the navigation
 * component already mounts five.
 *
 * Only the section in view holds cores. Nine sections each running a blend would
 * be nine times the work for eight things nobody is looking at, so a section
 * releases its cores when it leaves and remounts when it returns.
 */

const CATALOGUE = new URL("../../../../gradient-library/catalogue.json", import.meta.url);
const STATIC_BASE = new URL("../../../../gradient-library/assets/static/", import.meta.url);
const PRODUCTS = new URL("../../../../registry/products.json", import.meta.url);

const FADE = 1600;
const HOLD = 3600;

const query = new URLSearchParams(location.search);
const forceStatic = matchMedia("(prefers-reduced-motion: reduce)").matches
  || query.has("static") || query.has("no-webgl");
const twin = id => new URL(`${id.toLowerCase()}.webp`, STATIC_BASE).href;
const wait = ms => new Promise(r => setTimeout(r, ms));
const MAX_LIVE = () => 2048 / Math.min(devicePixelRatio || 1, 2);

const response = await fetch(PRODUCTS);
if (!response.ok) throw new Error("canonical product registry unavailable");
const gradients = (await response.json()).products.map(p => p.gradientId);

let renderer = null;
if (!forceStatic) {
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
} else {
  document.documentElement.dataset.motion = "static";
}

document.querySelectorAll("[data-live]").forEach(host => {
  const a = host.querySelector('[data-core="a"]');
  const b = host.querySelector('[data-core="b"]');
  const shape = host.dataset.shape || "disc";
  const radius = Number(host.dataset.radius || 0);
  let index = 0;
  let front = a;
  let back = b;
  let timer = null;
  let running = false;

  /* The twin is the fallback, so reduced motion and a renderer failure land on
     the image the core would have drawn. The wings mask has no rectangular twin,
     so that one stays empty rather than showing a square of material. */
  if (shape !== "wings") {
    a.style.background = `center / cover no-repeat url("${twin(gradients[0])}")`;
    a.style.borderRadius = "inherit";
  }
  a.style.opacity = "1";
  b.style.opacity = "0";

  if (forceStatic || !renderer) return;

  const mount = (node, id) => {
    renderer.mount(node, id, { shape, radius, profile: "deep" });
    node.dataset.mzCore = id;
  };
  const release = node => {
    renderer.surfaces?.delete(node);
    node.querySelector("canvas[data-mz-core-canvas]")?.remove();
    node.removeAttribute("data-mz-core");
  };

  const advance = async () => {
    if (running) return;
    running = true;
    const next = (index + 1) % gradients.length;
    try {
      mount(back, gradients[next]);
      /* Two frames, so the incoming core has drawn before it is revealed. */
      await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
      back.style.opacity = "1";
      front.style.opacity = "0";
      await wait(FADE);
      release(front);
      [front, back] = [back, front];
      index = next;
    } catch (error) {
      document.documentElement.dataset.coreFailure = error?.message || "unknown";
    }
    running = false;
  };

  let live = false;
  const observer = new IntersectionObserver(entries => {
    const visible = entries.some(e => e.intersectionRatio > 0.25);
    if (visible && !live) {
      if (host.getBoundingClientRect().width > MAX_LIVE()) {
        host.dataset.coreSkipped = "wider than the renderer framebuffer";
        return;
      }
      try {
        mount(front, gradients[index]);
        live = true;
        timer = setInterval(advance, HOLD + FADE);
      } catch (error) {
        document.documentElement.dataset.coreFailure = error?.message || "unknown";
      }
    } else if (!visible && live) {
      clearInterval(timer);
      timer = null;
      release(front);
      release(back);
      front.style.opacity = "1";
      back.style.opacity = "0";
      live = false;
    }
  }, { threshold: [0, 0.25, 0.5, 1] });
  observer.observe(host);
});
