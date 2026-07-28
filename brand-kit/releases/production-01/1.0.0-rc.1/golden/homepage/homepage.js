import "../../components/global-navigation/mez-global-navigation.js";
import "../../components/testimonial-marquee/mez-testimonial-marquee.js";
import { mountLivingCores } from "../../runtime/mz-core.js";

const PRODUCTS_URL = new URL("../../identity/products.json", import.meta.url);
const CATALOGUE_URL = new URL("../../identity/catalogue.json", import.meta.url);
const STATIC_BASE = new URL("../../identity/gradients/", import.meta.url);
const WINGS_URL = new URL("../../identity/wings.svg", import.meta.url);
const query = new URLSearchParams(location.search);
const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
const forceStatic = reducedMotion || query.has("static") || query.has("no-webgl");
if (query.has("strip")) document.documentElement.dataset.strip = "true";

/* Research-only frame evidence for Gate B. It is inert unless `?proof` is
   present and does not alter renderer behaviour or page composition. */
if (query.has("proof")) {
  document.documentElement.dataset.mzDrawCalls = "0";
  [window.WebGLRenderingContext, window.WebGL2RenderingContext]
    .filter(Boolean)
    .forEach(Context => {
      ["drawArrays", "drawElements"].forEach(method => {
        const original = Context.prototype[method];
        if (typeof original !== "function") return;
        Context.prototype[method] = function countedDrawCall(...args) {
          document.documentElement.dataset.mzDrawCalls = String(
            Number(document.documentElement.dataset.mzDrawCalls || 0) + 1
          );
          return original.apply(this, args);
        };
      });
    });
}

const escapeHtml = value => String(value).replace(/[&<>'"]/g, character => ({
  "&": "&amp;",
  "<": "&lt;",
  ">": "&gt;",
  "'": "&#39;",
  '"': "&quot;"
})[character]);

const staticTwin = gradientId => new URL(`${gradientId.toLowerCase()}.webp`, STATIC_BASE).href;

const PROCESS = {
  "context-engine": ["Understand", "Map", "Rank", "Run"],
  "ai-ads-system": ["Research", "Angles", "Creative", "Tests", "Learnings"],
  "claude-code-os": ["Context", "Skills", "Execute", "Approve"],
  "organic-content-os": ["Signals", "Ideas", "Create", "Publish", "Learn"]
};

const ECOSYSTEM_COPY = {
  "context-engine": {
    promise: "Find where AI belongs in the business.",
    body: "Map how the company works, rank the highest-leverage opportunities and load the context needed to get the first useful workflow running."
  },
  "ai-ads-system": {
    promise: "Turn every campaign into a learning loop.",
    body: "Connect audience research, angles, creative, experiments and results so every campaign improves the next one."
  },
  "claude-code-os": {
    promise: "Give Claude Code the context to execute real work.",
    body: "Connect business rules, skills, documentation, integrations and approval points in one execution environment."
  },
  "organic-content-os": {
    promise: "Turn scattered ideas into a compounding content system.",
    body: "Connect audience signals, brand voice, ideas, production and performance so the system remembers what you believe, what you have published and what works."
  }
};

const productsResponse = await fetch(PRODUCTS_URL);
if (!productsResponse.ok) throw new Error("Canonical product registry unavailable");
const { products } = await productsResponse.json();

/* GH-S01 · Five-card centred arc. DOM order stays literal registry order; the
   visual slot places AI OS centred with two cards stepping out each side. */
const HERO_SLOTS = {
  aios: 0,
  "context-engine": -1,
  "ai-ads-system": 1,
  "claude-code-os": -2,
  "organic-content-os": 2
};

const heroProducts = document.querySelector("[data-hero-products]");
heroProducts.innerHTML = products.map(product => {
  const slot = HERO_SLOTS[product.slug];
  return `
  <article
    class="hero-card"
    data-product="${escapeHtml(product.slug)}"
    data-arc-slot="${slot}"
    style="--arc-slot:${slot}; --arc-depth:${Math.abs(slot)}"
  >
    <div
      class="hero-card__material"
      data-hero-material
      data-gradient-id="${escapeHtml(product.gradientId)}"
      style="--material:url('${staticTwin(product.gradientId)}')"
    >
      <div class="material-identity">
        <img class="material-wings" src="${WINGS_URL.href}" alt="" />
        <strong>${escapeHtml(product.publicName)}</strong>
        <span>${escapeHtml(product.function)}</span>
      </div>
    </div>
  </article>
`;
}).join("");

/* Motion allocation.
   Every Living Core mounts directly on an intrinsically sized product-material
   element, never on an empty positioning layer, so the canvas always has real
   layout size. The hero owns the bounded five-live exception from
   DEC-GOLDEN-HOMEPAGE-HERO-MOTION-001; ordinary regions run one core; the
   expanded Global Navigation suppresses every page core. Material speed is the
   canonical Phase A automatic default — no overrides, hover eases speed only. */
let renderer = null;
let navigationOpen = false;
let heroRenderersActive = false;
let singleActiveAnchor = null;
let currentRegion = "hero";
let currentAnchor = null;

const heroMaterials = [...document.querySelectorAll("[data-hero-material]")];
const anchors = [...document.querySelectorAll("[data-live-anchor]")];
const motionSections = new Map([
  [document.querySelector("#top"), { region: "hero", anchor: null }],
  [document.querySelector("#principle"), { region: "single", anchor: anchors.find(anchor => anchor.dataset.liveAnchor === "principle") }],
  [document.querySelector("#why-mez"), { region: "sequence", anchor: null }],
  [document.querySelector("#ai-os"), { region: "single", anchor: anchors.find(anchor => anchor.dataset.liveAnchor === "ai-os") }]
]);

function unmountCore(element) {
  renderer.surfaces?.delete(element);
  element.querySelector("canvas[data-mz-core-canvas]")?.remove();
  element.removeAttribute("data-mz-core");
}

function unmountSingleCore() {
  if (!renderer || !singleActiveAnchor) return;
  unmountCore(singleActiveAnchor);
  singleActiveAnchor = null;
}

function unmountHeroCores() {
  if (!renderer || !heroRenderersActive) return;
  heroMaterials.forEach(material => unmountCore(material));
  heroRenderersActive = false;
}

function unmountAllPageCores() {
  unmountSingleCore();
  unmountHeroCores();
}

function mountSingleCore() {
  if (!renderer || navigationOpen || forceStatic || !currentAnchor) return;
  if (singleActiveAnchor === currentAnchor) return;
  unmountSingleCore();
  try {
    /* Shape is per-anchor: GH-S03's core is a canonical disc expression, the
       rest are rounded rects. */
    const shape = currentAnchor.dataset.coreShape || "rect";
    const radius = shape === "disc" ? 0 : 0.16;
    renderer.mount(currentAnchor, currentAnchor.dataset.gradientId, { shape, radius, profile: "deep" });
    currentAnchor.dataset.mzCore = currentAnchor.dataset.gradientId;
    singleActiveAnchor = currentAnchor;
  } catch (error) {
    document.documentElement.dataset.coreFailure = error?.message || "unknown";
  }
}

function mountHeroCores() {
  if (!renderer || heroRenderersActive || navigationOpen || forceStatic) return;
  try {
    heroMaterials.forEach(material => {
      renderer.mount(material, material.dataset.gradientId, { shape: "rect", radius: 0.16, profile: "deep" });
      material.dataset.mzCore = material.dataset.gradientId;
    });
    heroRenderersActive = true;
  } catch (error) {
    unmountHeroCores();
    document.documentElement.dataset.coreFailure = error?.message || "unknown";
  }
}

/* GH-S04 · the sequence terminus blends between two live cores rather than
   fading through a still. Two surfaces on the one context, which the renderer
   supports because surfaces is a Map. Riding a static twin across a setCore call
   is correct when a swap must be hidden, but here it would put a frozen frame in
   the middle of every transition. */
/* Read from the canonical registry, so adding or removing a product changes what
   the terminus blends through without touching this file (LAY-09). */
const productGradients = products.map(product => product.gradientId);
const sequenceHost = document.querySelector("[data-sequence-core]");
const sequenceCores = sequenceHost ? [...sequenceHost.querySelectorAll(".mseq__core")] : [];
const SEQUENCE_FADE = 1600;
const SEQUENCE_HOLD = 3600;
let sequenceFront = sequenceCores[0] || null;
let sequenceBack = sequenceCores[1] || null;
let sequenceIndex = 0;
let sequenceTimer = null;
let sequenceLive = false;
let sequenceBusy = false;

if (sequenceFront) {
  sequenceFront.style.background = `#101010 center / cover no-repeat url("${staticTwin(productGradients[0])}")`;
  sequenceFront.style.opacity = "1";
  if (sequenceBack) sequenceBack.style.opacity = "0";
}

async function advanceSequence() {
  if (!renderer || !sequenceLive || sequenceBusy) return;
  sequenceBusy = true;
  const next = (sequenceIndex + 1) % productGradients.length;
  try {
    renderer.mount(sequenceBack, productGradients[next], { shape: "disc", radius: 0, profile: "deep" });
    sequenceBack.dataset.mzCore = productGradients[next];
    /* Two frames, so the incoming core has drawn before it is revealed. */
    await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
    sequenceBack.style.opacity = "1";
    sequenceFront.style.opacity = "0";
    await new Promise(resolve => setTimeout(resolve, SEQUENCE_FADE));
    unmountCore(sequenceFront);
    [sequenceFront, sequenceBack] = [sequenceBack, sequenceFront];
    sequenceIndex = next;
  } catch (error) {
    document.documentElement.dataset.coreFailure = error?.message || "unknown";
  }
  sequenceBusy = false;
}

function mountSequence() {
  if (!renderer || sequenceLive || navigationOpen || forceStatic || !sequenceHost) return;
  try {
    renderer.mount(sequenceFront, productGradients[sequenceIndex], { shape: "disc", radius: 0, profile: "deep" });
    sequenceFront.dataset.mzCore = productGradients[sequenceIndex];
    sequenceLive = true;
    sequenceTimer = setInterval(advanceSequence, SEQUENCE_HOLD + SEQUENCE_FADE);
  } catch (error) {
    document.documentElement.dataset.coreFailure = error?.message || "unknown";
  }
}

function unmountSequence() {
  if (!sequenceLive) return;
  clearInterval(sequenceTimer);
  sequenceTimer = null;
  sequenceCores.forEach(core => unmountCore(core));
  sequenceFront = sequenceCores[0];
  sequenceBack = sequenceCores[1];
  sequenceFront.style.opacity = "1";
  sequenceBack.style.opacity = "0";
  sequenceLive = false;
}

function activateRegion(region, anchor = null) {
  currentRegion = region;
  if (anchor) currentAnchor = anchor;
  if (navigationOpen || forceStatic || !renderer) return;
  if (region === "hero") {
    unmountSingleCore();
    unmountSequence();
    mountHeroCores();
    return;
  }
  unmountHeroCores();
  if (region === "idle") {
    unmountSingleCore();
    unmountSequence();
    return;
  }
  if (region === "sequence") {
    unmountSingleCore();
    mountSequence();
    return;
  }
  unmountSequence();
  mountSingleCore();
}

if (!forceStatic) {
  try {
    const catalogueResponse = await fetch(CATALOGUE_URL);
    if (!catalogueResponse.ok) throw new Error("Living Core catalogue unavailable");
    const catalogue = await catalogueResponse.json();
    const mounted = await mountLivingCores(document, {
      catalogue,
      selector: "[data-homepage-never]",
      staticBaseUrl: STATIC_BASE
    });
    renderer = mounted.renderer;
    activateRegion("hero");
  } catch (error) {
    document.documentElement.dataset.coreFailure = error?.message || "unknown";
  }
}

const visibility = new Map();
const allocationObserver = new IntersectionObserver(entries => {
  entries.forEach(entry => visibility.set(entry.target, entry.intersectionRatio));
  const eligible = [...motionSections.entries()]
    .sort((a, b) => (visibility.get(b[0]) || 0) - (visibility.get(a[0]) || 0));
  const [section, allocation] = eligible[0] || [];
  if (section && allocation && (visibility.get(section) || 0) > 0.18) {
    activateRegion(allocation.region, allocation.anchor);
  } else if (currentRegion !== "idle") {
    activateRegion("idle");
  }
}, {
  rootMargin: "-18% 0px -18%",
  threshold: [0, .18, .35, .55, .75]
});
motionSections.forEach((_, section) => allocationObserver.observe(section));

/* GH-S07 · The selected unboxed rail hover-animates one product disc. Its material
   mounts a single live core (exact static twin at rest); leaving unmounts it,
   so at most one ecosystem core is ever live and reduced-motion / no-WebGL keep
   the static twin. The ecosystem is not a motion region, so nothing competes. */
const ecoFields = [...document.querySelectorAll("[data-eco-live]")];
let ecoActiveField = null;
function unmountEcoField() {
  if (!renderer || !ecoActiveField) return;
  unmountCore(ecoActiveField);
  ecoActiveField = null;
}
ecoFields.forEach(field => {
  const card = field.closest(".eco-card") || field;
  const activateEcoField = () => {
    if (!renderer || forceStatic || navigationOpen || ecoActiveField === field) return;
    unmountEcoField();
    unmountSingleCore();
    unmountSequence();
    unmountHeroCores();
    try {
      renderer.mount(field, field.dataset.gradientId, { shape: "disc", radius: 0, profile: "deep" });
      field.dataset.mzCore = field.dataset.gradientId;
      ecoActiveField = field;
    } catch (error) {
      document.documentElement.dataset.coreFailure = error?.message || "unknown";
    }
  };
  const releaseEcoField = () => {
    unmountEcoField();
    activateRegion(currentRegion, currentAnchor);
  };
  card.addEventListener("pointerenter", activateEcoField);
  card.addEventListener("pointerleave", releaseEcoField);
  card.addEventListener("focusin", activateEcoField);
  card.addEventListener("focusout", releaseEcoField);
});

const navigation = document.querySelector("mez-global-navigation");
navigation.addEventListener("mez-navigation-open", event => {
  navigationOpen = Boolean(event.detail?.expanded);
  if (navigationOpen) {
    unmountEcoField();
    unmountSequence();
    unmountAllPageCores();
  } else {
    activateRegion(currentRegion, currentAnchor);
  }
});

/* GH-S03 · Interchangeable intelligence over the owned layer is a static
   authored diagram now (abstract swap-slots over an owned base — no rented
   brand logos, real or invented, and no live core). No JS wiring required. */


/* One restrained section-entry treatment, armed only when motion is allowed
   so the page stays complete without JavaScript or with reduced motion. */
if (!reducedMotion) {
  document.body.classList.add("entry-armed");
  const entryObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add("is-entered");
      entryObserver.unobserve(entry.target);
    });
  }, { threshold: .2 });
  document.querySelectorAll("[data-entry]").forEach(target => entryObserver.observe(target));
}

/* Consumer-owned destination events. */
document.querySelectorAll("[data-action]").forEach(link => {
  link.addEventListener("click", () => {
    link.dispatchEvent(new CustomEvent(
      link.dataset.action === "primary" ? "mez-homepage-primary-action" : "mez-homepage-secondary-action",
      { bubbles: true, detail: { label: link.textContent.trim(), target: link.getAttribute("href") } }
    ));
  });
});

document.querySelectorAll("[data-consumer-route]").forEach(button => {
  button.addEventListener("click", () => {
    button.dispatchEvent(new CustomEvent("mez-consumer-route-request", {
      bubbles: true,
      detail: { routeId: button.dataset.consumerRoute }
    }));
  });
});

/* ============================================================ GH-S03 · principle

   Two registers of third-party mark, and one core cycling the product family.

   A HARNESS is a system the business is run from. A CONNECTION is a tool the
   business already uses. They are sized and weighted differently on purpose: a
   harness is not a plugin, and the gap between the two treatments is what says
   so without a label.

   Marks are resolved from the generated registry. Only entries recorded as
   form:"symbol" are used, because two vendors ship a horizontal wordmark under
   the mark.svg filename and one ships a filled app icon, all of which wreck a
   ring of peers. Slack, Linear, HubSpot, Klaviyo, 1Password, Google Drive,
   Google Calendar, shadcn and MCP have no mark in the registry and are absent
   rather than drawn.

   The core shows every product in turn. renderer.setCore() swaps a mounted
   surface's gradient without a second WebGL context, but the swap is a hard cut,
   so the transition rides the exact static twins: fade the next product's twin
   in over the live canvas, swap underneath it, fade the twin back out. The
   element's CSS background follows so the no-WebGL fallback lands on the same
   product. */

const MARKS_BASE = new URL("../../assets/third-party-marks/", import.meta.url);
const conc = document.querySelector(".conc");

if (conc) {
  const HARNESSES = [
    ["chatgpt", "ChatGPT"], ["claude", "Claude"], ["gemini", "Gemini"],
    ["grok", "Grok"], ["mistral", "Mistral"], ["perplexity", "Perplexity"]
  ];
  const CONNECTIONS = [
    ["stripe", "Stripe"], ["notion", "Notion"], ["shopify", "Shopify"], ["figma", "Figma"],
    ["github", "GitHub"], ["gmail", "Gmail"], ["supabase", "Supabase"], ["vercel", "Vercel"],
    ["n8n", "n8n"], ["clickup", "ClickUp"]
  ];

  const concCore = conc.querySelector(".conc__core");
  const concProducts = products.map(product => [product.gradientId, product.publicName]);
  let concIndex = 0;

  const markUrl = slug => new URL(`marks/${slug}/logos/mark.svg`, MARKS_BASE).href;

  const fillRing = (ring, set, variant) => {
    set.forEach(([slug, name], index) => {
      const slot = document.createElement("span");
      slot.className = "conc__slot";
      slot.style.setProperty("--a", `${(360 / set.length) * index}deg`);
      const upright = document.createElement("span");
      upright.className = "conc__upright";
      const img = document.createElement("img");
      img.className = `conc__mark conc__mark--${variant}`;
      img.src = markUrl(slug);
      img.alt = name;
      img.loading = "lazy";
      img.decoding = "async";
      upright.append(img);
      slot.append(upright);
      ring.append(slot);
    });
  };

  fillRing(conc.querySelector('[data-orbit="connections"]'), CONNECTIONS, "tool");
  fillRing(conc.querySelector('[data-orbit="harnesses"]'), HARNESSES, "harness");

  const veil = document.createElement("img");
  veil.className = "conc__veil";
  veil.alt = "";
  veil.setAttribute("aria-hidden", "true");
  veil.src = staticTwin(concProducts[0][0]);
  concCore.prepend(veil);
  concCore.style.setProperty("--conc-material", `url("${staticTwin(concProducts[0][0])}")`);

  /* The lockup names the holdco, not the product in play. The material cycles
     the family underneath a label that holds still, so the mark stays an anchor
     rather than a caption that keeps rewriting itself. */

  if (!forceStatic) {
    const FADE = 1100;
    const HOLD = 4200;
    let cycling = null;

    const advance = async () => {
      if (!renderer || singleActiveAnchor !== concCore) return;
      const next = (concIndex + 1) % concProducts.length;
      const [id] = concProducts[next];
      veil.src = staticTwin(id);
      await new Promise(resolve => (veil.complete ? resolve() : veil.addEventListener("load", resolve, { once: true })));
      veil.style.opacity = "1";
      await new Promise(resolve => setTimeout(resolve, FADE));
      try {
        renderer.setCore(concCore, id);
        concCore.dataset.mzCore = id;
        concCore.style.setProperty("--conc-material", `url("${staticTwin(id)}")`);
      } catch (error) {
        document.documentElement.dataset.coreFailure = error?.message || "unknown";
      }
      concIndex = next;
      await new Promise(resolve => requestAnimationFrame(resolve));
      veil.style.opacity = "0";
    };

    const startCycle = () => { if (!cycling) cycling = setInterval(advance, HOLD + FADE); };
    const stopCycle = () => { clearInterval(cycling); cycling = null; };
    startCycle();
    document.addEventListener("visibilitychange", () => (document.hidden ? stopCycle() : startCycle()));
  }
}


/* Package diagnostic: candidate identity is visible without claiming release authority. */
fetch(new URL("../../manifest.json", import.meta.url))
  .then(response => response.json())
  .then(manifest => {
    const node = document.querySelector("[data-package-diagnostic]");
    if (node) node.textContent = `${manifest.name} ${manifest.version} · ${manifest.contentSha256.slice(0, 12)}`;
  })
  .catch(() => {
    const node = document.querySelector("[data-package-diagnostic]");
    if (node) node.textContent = "@mez-systems/design-system-web 1.0.0-rc.1 · manifest unavailable";
  });
