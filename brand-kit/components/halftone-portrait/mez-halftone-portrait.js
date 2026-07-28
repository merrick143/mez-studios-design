/* TASK-CMP-05 · Halftone Portrait
 *
 * Turns a video into a halftone dot grid on a canvas, one frame at a time.
 * No dependencies, no ML at runtime, no network calls.
 *
 * Two things about this component are deliberate and easy to get wrong.
 *
 * First, the cutout is NOT done here. A matted source (subject composited over
 * a flat light plate) reproduces the whole look for free, because a light plate
 * maps to no dots. Doing it live would drag an 11MB segmentation runtime and a
 * per-frame DNN into every consumer for a result that never changes after the
 * clip is approved. Segmentation is media preparation, not component behaviour.
 *
 * Second, motion is allocated, not assumed. Website Motion 1.0.0 permits one
 * expressive event running in the viewport. Every instance mounts static; the
 * single most visible instance is handed the animation and takes it back when
 * the page scrolls. Reduced motion, a missing video and a decode failure all
 * land on the same complete static frame rather than on an empty box.
 */

const TAU = Math.PI * 2;
const SHAPES = ["circle", "square", "diamond", "cross", "ring"];

const query = new URLSearchParams(location.search);
const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
const forceStatic = reduced || query.has("static");

const clamp01 = value => (value < 0 ? 0 : value > 1 ? 1 : value);
const num = (raw, fallback) => {
  const parsed = Number.parseFloat(raw);
  return Number.isFinite(parsed) ? parsed : fallback;
};

/* Motion allocation.
 *
 * Default policy is `allocated`: one animated portrait per page, handed to
 * whichever instance is most visible. That is Website Motion 1.0.0, where one
 * expressive event may run in the viewport.
 *
 * `motion-policy="always"` opts an instance out of the allocation and lets it
 * animate whenever it is visible. This is a bounded exception approved by Olli
 * on 2026-07-27 for the testimonial marquee, on the same footing as the
 * five-live-cores exception Global Navigation carries. It is bounded because a
 * halftone portrait costs a canvas fill, not a WebGL context or a neural
 * network, so a wall of them is affordable in a way five live cores was not.
 *
 * It is still an exception, not a new default. A surface that sets it is
 * making a deliberate claim, and the workbench measures the result. */
const live = { holder: null, instances: new Set(), observer: null, ratios: new Map() };

function ensureObserver() {
  if (live.observer) return;
  live.observer = new IntersectionObserver(
    entries => {
      for (const entry of entries) {
        const target = entry.target;
        live.ratios.set(target, entry.isIntersecting ? entry.intersectionRatio : 0);
        if (target.policy === "always") {
          // Self-managed: run while on screen, idle the moment it leaves, so a
          // long marquee never pays for portraits nobody can see.
          if (entry.isIntersecting) target.takeMotion();
          else target.releaseMotion();
        }
      }
      allocate();
    },
    { threshold: [0, 0.25, 0.5, 0.75, 1] }
  );
}

/* Give the animation to the most visible instance. Ties keep the current
   holder so a page that scrolls slowly does not flicker between two. */
function allocate() {
  let best = null;
  let bestRatio = 0;
  for (const instance of live.instances) {
    if (!instance.canAnimate || instance.policy === "always") continue;
    const ratio = live.ratios.get(instance) ?? 0;
    if (ratio > bestRatio + 0.01 || (ratio > 0 && instance === live.holder && ratio >= bestRatio)) {
      best = instance;
      bestRatio = ratio;
    }
  }
  if (best === live.holder) return;
  const previous = live.holder;
  live.holder = best;
  previous?.releaseMotion();
  best?.takeMotion();
}

class MezHalftonePortrait extends HTMLElement {
  static observedAttributes = [
    "src", "poster", "grid-step", "max-radius", "dot-colour", "background",
    "contrast", "brightness", "dot-gamma", "screen-angle", "stagger",
    "invert", "auto-levels", "dot-shape", "zoom", "focus-x", "focus-y", "label",
    "motion-policy"
  ];

  constructor() {
    super();
    this.canvas = null;
    this.video = null;
    this.sample = null;
    this.frame = 0;
    this.dirty = true;
    this.painted = false;
    this.animating = false;
    this.geometry = { cols: 0, rows: 0, width: 0, height: 0 };
    this.levels = null;
    this.bins = new Uint32Array(64);
    this.resizeObserver = null;
    this.onResize = () => this.measure();
  }

  /* `always` opts out of the one-live allocation. Bounded exception; see the
     note at the top of this file. */
  get policy() {
    return this.getAttribute("motion-policy") === "always" ? "always" : "allocated";
  }

  /* Reduced motion and forced-static never animate, but they still paint. */
  get canAnimate() {
    return !forceStatic && !this.hasAttribute("data-failure");
  }

  get settings() {
    const step = Math.max(2, num(this.getAttribute("grid-step"), 4));
    return {
      step,
      radius: num(this.getAttribute("max-radius"), step / 2),
      dot: this.getAttribute("dot-colour") || "#212121",
      background: this.getAttribute("background") || "#ffffff",
      contrast: num(this.getAttribute("contrast"), 1.3),
      brightness: num(this.getAttribute("brightness"), -0.03),
      gamma: num(this.getAttribute("dot-gamma"), 1),
      angle: num(this.getAttribute("screen-angle"), 0),
      stagger: this.hasAttribute("stagger"),
      invert: this.hasAttribute("invert"),
      autoLevels: this.getAttribute("auto-levels") !== "off",
      shape: SHAPES.includes(this.getAttribute("dot-shape")) ? this.getAttribute("dot-shape") : "circle",
      zoom: Math.max(1, num(this.getAttribute("zoom"), 1)),
      focusX: clamp01(num(this.getAttribute("focus-x"), 0.5)),
      focusY: clamp01(num(this.getAttribute("focus-y"), 0.5))
    };
  }

  connectedCallback() {
    if (!this.canvas) this.build();
    ensureObserver();
    live.instances.add(this);
    live.observer.observe(this);
    // Declare the state from mount. An instance with no data-motion is
    // indistinguishable from one that never initialised, which makes the
    // motion budget unauditable from outside.
    this.dataset.motion = "static";
    this.measure();
  }

  disconnectedCallback() {
    this.releaseMotion();
    live.instances.delete(this);
    live.ratios.delete(this);
    live.observer?.unobserve(this);
    if (live.holder === this) {
      live.holder = null;
      allocate();
    }
    this.resizeObserver?.disconnect();
    window.removeEventListener("resize", this.onResize);
  }

  attributeChangedCallback(name, previous, next) {
    if (previous === next || !this.canvas) return;
    if (name === "src") {
      this.painted = false;
      this.levels = null;
      this.video.src = next ?? "";
      this.video.load();
    }
    if (name === "grid-step") this.measure();
    this.dirty = true;
    this.paint();
  }

  build() {
    this.innerHTML = "";

    this.video = document.createElement("video");
    this.video.muted = true;
    this.video.loop = true;
    this.video.playsInline = true;
    this.video.preload = "auto";
    this.video.setAttribute("aria-hidden", "true");
    this.video.className = "mz-halftone__source";
    if (this.getAttribute("src")) this.video.src = this.getAttribute("src");
    this.video.addEventListener("loadeddata", () => {
      this.dirty = true;
      this.paint();
      // A static instance still owes the reader a complete image.
      if (!this.animating) this.paint();
    });
    this.video.addEventListener("error", () => this.fail("source unavailable"));

    this.canvas = document.createElement("canvas");
    this.canvas.className = "mz-halftone__canvas";
    this.canvas.setAttribute("role", "img");
    this.canvas.setAttribute("aria-label", this.getAttribute("label") || "Halftone portrait");

    this.append(this.video, this.canvas);
    this.sample = document.createElement("canvas");

    this.resizeObserver = new ResizeObserver(() => this.measure());
    this.resizeObserver.observe(this);
    window.addEventListener("resize", this.onResize);
  }

  measure() {
    if (!this.canvas) return;
    const rect = this.getBoundingClientRect();
    const width = Math.max(1, Math.round(rect.width));
    const height = Math.max(1, Math.round(rect.height));
    // Capped at 2: a 3x backing store triples fill cost with no visible gain
    // at this dot size.
    const ratio = Math.min(window.devicePixelRatio || 1, 2);

    this.canvas.width = Math.round(width * ratio);
    this.canvas.height = Math.round(height * ratio);
    this.canvas.style.width = `${width}px`;
    this.canvas.style.height = `${height}px`;
    this.canvas.getContext("2d")?.setTransform(ratio, 0, 0, ratio, 0, 0);

    const { step } = this.settings;
    const cols = Math.max(1, Math.ceil(width / step));
    const rows = Math.max(1, Math.ceil(height / step));
    this.sample.width = cols;
    this.sample.height = rows;

    this.geometry = { cols, rows, width, height };
    this.dirty = true;
    this.paint();
  }

  takeMotion() {
    if (this.animating || !this.canAnimate) return;
    this.animating = true;
    this.dataset.motion = "live";
    const attempt = this.video?.play();
    attempt?.catch(() => {
      // Autoplay refused. The static frame is already correct, so downgrade
      // quietly rather than showing a broken control.
      this.animating = false;
      this.dataset.motion = "static";
      this.video?.pause();
    });
    const loop = () => {
      if (!this.animating) return;
      this.frame = requestAnimationFrame(loop);
      this.paint();
    };
    this.frame = requestAnimationFrame(loop);
  }

  releaseMotion() {
    if (!this.animating) return;
    this.animating = false;
    cancelAnimationFrame(this.frame);
    this.video?.pause();
    this.dataset.motion = "static";
    // Leave the last frame on screen: a released instance is still complete.
    this.dirty = true;
    this.paint();
  }

  paint() {
    const video = this.video;
    const canvas = this.canvas;
    if (!video || !canvas) return;
    if (video.readyState < 2) return;
    if (!this.animating && this.painted && !this.dirty) return;

    const vw = video.videoWidth;
    const vh = video.videoHeight;
    if (!vw || !vh) return;

    const { cols, rows, width, height } = this.geometry;
    if (cols < 1 || rows < 1) return;

    const ctx = canvas.getContext("2d");
    const sctx = this.sample.getContext("2d", { willReadFrequently: true });
    if (!ctx || !sctx) return;

    const s = this.settings;

    // Cover-fit the source, then zoom and pan with the focus point, so a
    // non-square host never squashes a square portrait.
    const targetAspect = width / height;
    const videoAspect = vw / vh;
    let sw = videoAspect > targetAspect ? vh * targetAspect : vw;
    let sh = videoAspect > targetAspect ? vh : vw / targetAspect;
    sw /= s.zoom;
    sh /= s.zoom;
    const sx = (vw - sw) * s.focusX;
    const sy = (vh - sh) * s.focusY;

    let pixels;
    try {
      // The offscreen canvas is sized to the GRID, not the display, so the
      // browser does the downscale and getImageData reads cols*rows pixels
      // instead of the whole frame.
      sctx.drawImage(video, sx, sy, sw, sh, 0, 0, cols, rows);
      pixels = sctx.getImageData(0, 0, cols, rows).data;
    } catch {
      this.fail("frame could not be sampled");
      return;
    }

    ctx.fillStyle = s.background;
    ctx.fillRect(0, 0, width, height);
    ctx.fillStyle = s.dot;
    ctx.beginPath();

    const half = s.step / 2;
    const offset = 0.5 + s.brightness;
    const [low, span] = s.autoLevels ? this.autoLevels(pixels, cols * rows) : [0, 255];

    const plot = (index, cx, cy) => {
      const i = index * 4;
      const raw = 0.299 * pixels[i] + 0.587 * pixels[i + 1] + 0.114 * pixels[i + 2];
      let normalised = (raw - low) / span;
      if (normalised < 0) normalised = 0;
      else if (normalised > 1) normalised = 1;

      const value = s.invert ? normalised : 1 - normalised;
      let darkness = (value - 0.5) * s.contrast + offset;
      if (darkness <= 0.06) return;
      if (darkness > 1) darkness = 1;

      const r = s.radius * (s.gamma === 1 ? darkness : Math.pow(darkness, s.gamma));
      if (r < 0.15) return;
      this.addDot(ctx, s.shape, cx, cy, r);
    };

    if (s.angle === 0 && !s.stagger) {
      for (let y = 0; y < rows; y += 1) {
        const cy = y * s.step + half;
        for (let x = 0; x < cols; x += 1) plot(y * cols + x, x * s.step + half, cy);
      }
    } else {
      this.plotLattice(s, plot);
    }

    ctx.fill();
    this.dirty = false;
    if (!this.painted) {
      this.painted = true;
      this.dispatchEvent(new CustomEvent("mez-halftone-ready", { bubbles: true }));
    }
  }

  /* Rotated or staggered lattice. Walk it in its own space, map each point back
     into the frame and sample the nearest cell. Kept off the default path so
     the common case indexes the grid directly. */
  plotLattice(s, plot) {
    const { cols, rows, width, height } = this.geometry;
    const radians = (s.angle * Math.PI) / 180;
    const cos = Math.cos(radians);
    const sin = Math.sin(radians);
    const half = s.step / 2;

    let minU = Infinity, maxU = -Infinity, minV = Infinity, maxV = -Infinity;
    for (const [px, py] of [[0, 0], [width, 0], [0, height], [width, height]]) {
      const u = px * cos + py * sin;
      const v = -px * sin + py * cos;
      if (u < minU) minU = u;
      if (u > maxU) maxU = u;
      if (v < minV) minV = v;
      if (v > maxV) maxV = v;
    }

    for (let j = Math.floor(minV / s.step) - 1; j <= Math.ceil(maxV / s.step) + 1; j += 1) {
      const v = j * s.step + half;
      const shift = s.stagger && (j & 1) ? half : 0;
      for (let i = Math.floor(minU / s.step) - 1; i <= Math.ceil(maxU / s.step) + 1; i += 1) {
        const u = i * s.step + half + shift;
        const wx = u * cos - v * sin;
        const wy = u * sin + v * cos;
        if (wx < 0 || wy < 0 || wx >= width || wy >= height) continue;
        let cx = (wx / s.step) | 0;
        let cy = (wy / s.step) | 0;
        if (cx >= cols) cx = cols - 1;
        if (cy >= rows) cy = rows - 1;
        plot(cy * cols + cx, wx, wy);
      }
    }
  }

  addDot(ctx, shape, cx, cy, r) {
    if (shape === "square") {
      ctx.rect(cx - r, cy - r, r * 2, r * 2);
    } else if (shape === "diamond") {
      ctx.moveTo(cx, cy - r);
      ctx.lineTo(cx + r, cy);
      ctx.lineTo(cx, cy + r);
      ctx.lineTo(cx - r, cy);
      ctx.closePath();
    } else if (shape === "cross") {
      const arm = r * 0.42;
      ctx.rect(cx - r, cy - arm, r * 2, arm * 2);
      ctx.rect(cx - arm, cy - r, arm * 2, r * 2);
    } else if (shape === "ring") {
      ctx.moveTo(cx + r, cy);
      ctx.arc(cx, cy, r, 0, TAU);
      const inner = r * 0.5;
      if (inner > 0.3) {
        ctx.moveTo(cx + inner, cy);
        ctx.arc(cx, cy, inner, 0, TAU, true);
      }
    } else {
      // moveTo first, otherwise each arc joins onto the previous one.
      ctx.moveTo(cx + r, cy);
      ctx.arc(cx, cy, r, 0, TAU);
    }
  }

  /* Stretch the frame's real luminance range before the tone curve. Without it
     every clip needs hand-tuned contrast, and a bright face on a light plate
     falls entirely below the dot threshold and renders as a blank silhouette. */
  autoLevels(pixels, count) {
    const bins = this.bins;
    bins.fill(0);
    for (let index = 0; index < count; index += 1) {
      const i = index * 4;
      const lum = 0.299 * pixels[i] + 0.587 * pixels[i + 1] + 0.114 * pixels[i + 2];
      bins[(lum >> 2) & 63] += 1;
    }
    const tail = count * 0.02;
    let acc = 0;
    let lowBin = 0;
    let highBin = 63;
    for (let b = 0; b < 64; b += 1) {
      acc += bins[b];
      if (acc >= tail) { lowBin = b; break; }
    }
    acc = 0;
    for (let b = 63; b >= 0; b -= 1) {
      acc += bins[b];
      if (acc >= tail) { highBin = b; break; }
    }
    const rawLow = lowBin * 4;
    const rawHigh = highBin * 4 + 3;
    if (rawHigh - rawLow <= 24) return [0, 255];

    // Ease toward the new range so exposure changes do not pulse the grid.
    const previous = this.levels;
    const next = previous
      ? { low: previous.low + (rawLow - previous.low) * 0.12, high: previous.high + (rawHigh - previous.high) * 0.12 }
      : { low: rawLow, high: rawHigh };
    this.levels = next;
    return [next.low, Math.max(24, next.high - next.low)];
  }

  fail(reason) {
    this.dataset.failure = reason;
    this.releaseMotion();
    this.dispatchEvent(new CustomEvent("mez-halftone-failure", { bubbles: true, detail: { reason } }));
  }
}

if (!customElements.get("mez-halftone-portrait")) {
  customElements.define("mez-halftone-portrait", MezHalftonePortrait);
}

export { MezHalftonePortrait, SHAPES };
