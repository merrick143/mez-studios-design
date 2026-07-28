import { mountLivingCores } from "../../../../source-pack/design-system-export/mz-core.js";

/* GH-S04 · the sequence.
 *
 * Four charcoal dots and one live gradient. The stages are process, so they are
 * flat; only the thing that ships carries material, which leaves the section
 * with exactly one colour event.
 *
 * The blend is between two live gradients. Two surfaces are mounted on the one
 * WebGL context, which the renderer supports because surfaces is a Map and the
 * navigation component already mounts five, and their opacity is cross-faded.
 * Both sides of the transition are moving.
 *
 * The obvious approach, and the one used in GH-S03, is to ride the exact static
 * twin across a setCore call. That is correct when a swap must be hidden, but
 * here it puts a still image in the middle of the transition, which is precisely
 * what reads as a freeze. Two live cores never stop moving.
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

const host = document.querySelector("[data-live]");
if (host) {
  const a = host.querySelector('[data-core="a"]');
  const b = host.querySelector('[data-core="b"]');
  let index = 0;

  /* The twin is the fallback surface, so reduced motion and a renderer failure
     both land on the same image the core would have drawn. */
  const paintTwin = node => {
    node.style.background = `#101010 center / cover no-repeat url("${twin(gradients[index])}")`;
  };
  paintTwin(a);
  a.style.opacity = "1";
  b.style.opacity = "0";

  if (forceStatic) {
    document.documentElement.dataset.motion = "static";
  } else {
    let renderer = null;
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

    let front = a;
    let back = b;
    let running = false;

    const mount = (node, id) => {
      renderer.mount(node, id, { shape: "disc", radius: 0, profile: "deep" });
      node.dataset.mzCore = id;
    };

    const advance = async () => {
      if (!renderer || running) return;
      running = true;
      const next = (index + 1) % gradients.length;
      try {
        /* Mount the incoming gradient behind the outgoing one, let it render a
           frame so it is already moving before it is revealed, then cross-fade. */
        mount(back, gradients[next]);
        await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
        back.style.opacity = "1";
        front.style.opacity = "0";
        await wait(FADE);
        /* Only now release the one that faded out, so the context never holds
           more than two surfaces and never fewer than one live. */
        renderer.surfaces?.delete(front);
        front.querySelector("canvas[data-mz-core-canvas]")?.remove();
        front.removeAttribute("data-mz-core");
        [front, back] = [back, front];
        index = next;
      } catch (error) {
        document.documentElement.dataset.coreFailure = error?.message || "unknown";
      }
      running = false;
    };

    let started = false;
    const observer = new IntersectionObserver(entries => {
      if (!renderer || started || !entries.some(e => e.intersectionRatio > 0.25)) return;
      if (host.getBoundingClientRect().width > MAX_LIVE()) {
        host.dataset.coreSkipped = "wider than the renderer framebuffer";
        return;
      }
      try {
        mount(front, gradients[index]);
        started = true;
        setInterval(advance, HOLD + FADE);
      } catch (error) {
        document.documentElement.dataset.coreFailure = error?.message || "unknown";
      }
    }, { threshold: [0, 0.25, 0.5, 1] });
    observer.observe(host);
  }
}
