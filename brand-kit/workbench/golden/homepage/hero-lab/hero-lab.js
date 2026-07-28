import { mountLivingCores } from "../../../../source-pack/design-system-export/mz-core.js";

const PRODUCTS_URL = new URL("../../../../registry/products.json", import.meta.url);
const CATALOGUE_URL = new URL("../../../../gradient-library/catalogue.json", import.meta.url);
const STATIC_BASE = new URL("../../../../gradient-library/assets/static/", import.meta.url);
const WINGS_URL = new URL("../../../../source-pack/design-system-export/assets/wings.svg", import.meta.url);

const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
const esc = value => String(value).replace(/[&<>'"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" }[c]));
const twin = id => new URL(`${id.toLowerCase()}.webp`, STATIC_BASE).href;

const { products } = await (await fetch(PRODUCTS_URL)).json();
const bySlug = Object.fromEntries(products.map(p => [p.slug, p]));

/* ------------------------------------------------------------- copy */

const COPY = {
  eyebrow: "Mez Systems",
  h1: "The operating systems AI-native businesses run on.",
  lead: "Own the context, workflows and decisions that make AI useful.",
  cta: "Explore the Systems"
};
document.querySelectorAll("[data-copy]").forEach(node => {
  node.innerHTML = `
    <p class="eyebrow">${COPY.eyebrow}</p>
    <h1>${COPY.h1}</h1>
    <p class="lead">${COPY.lead}</p>
    <a class="cta" href="#">${COPY.cta}</a>`;
});

/* ---------------------------------------------------- material card */

function matHtml(p, { shape = "rect", live = true, wingsOnly = false, radius = "0.16", focal = false } = {}) {
  const cls = ["mat"];
  if (shape === "disc") cls.push("mat--disc");
  if (shape === "sphere") cls.push("mat--sphere");
  if (wingsOnly) cls.push("mat--wings-only");
  const liveAttr = live
    ? ` data-live data-gradient-id="${esc(p.gradientId)}" data-shape="${shape}" data-radius="${radius}"`
    : "";
  const focalAttr = focal ? " data-focal" : "";
  return `<div class="${cls.join(" ")}"${focalAttr} data-slug="${esc(p.slug)}" style="--material:url('${twin(p.gradientId)}')"${liveAttr}>
    <div class="mat-identity">
      <img class="mat-wings" src="${WINGS_URL.href}" alt="" />
      <strong>${esc(p.publicName)}</strong>
      <span>${esc(p.function)}</span>
    </div>
  </div>`;
}

/* ------------------------------------------------------ arc / fan */

const ARC5 = { aios: 0, "context-engine": -1, "ai-ads-system": 1, "claude-code-os": -2, "organic-content-os": 2 };
const ARC4 = { aios: -0.5, "ai-ads-system": 0.5, "context-engine": -1.5, "organic-content-os": 1.5 };

function renderArc(mount, count, { staticCards = false } = {}) {
  mount.classList.add("deck--arc");
  const slots = count === 4 ? ARC4 : ARC5;
  const cards = Object.keys(slots).map(slug => ({ p: bySlug[slug], slot: slots[slug] }));
  const order = [...cards].sort((a, b) => a.slot - b.slot);
  mount.innerHTML = cards.map(({ p, slot }) => {
    const orderIndex = order.findIndex(c => c.p.slug === p.slug);
    return `<article class="card" style="--slot:${slot}; --depth:${Math.abs(slot)}; --slot-order:${orderIndex}; --enter-i:${orderIndex}">
      ${matHtml(p, { live: !staticCards })}
    </article>`;
  }).join("");
}

/* ---------------------------------------------------------- stack */

function renderStack(mount) {
  mount.classList.add("deck--stack");
  const orderSlugs = ["claude-code-os", "organic-content-os", "ai-ads-system", "context-engine", "aios"];
  mount.innerHTML = orderSlugs.map((slug, i) =>
    `<article class="card" style="--i:${i}">${matHtml(bySlug[slug])}</article>`
  ).join("");
}

/* ---------------------------------------------------------- shelf */

function renderShelf(mount) {
  mount.classList.add("deck--shelf");
  mount.innerHTML = products.map(p => `<article class="card">${matHtml(p)}</article>`).join("");
}

/* ------------------------------------------- clean even spread (V11–V14) */

const SPREAD5 = { "claude-code-os": -2, "context-engine": -1, aios: 0, "ai-ads-system": 1, "organic-content-os": 2 };
const SPREAD4 = { "context-engine": -1.5, aios: -0.5, "ai-ads-system": 0.5, "claude-code-os": 1.5 };

function renderSpread(mount, count) {
  mount.classList.add("deck--spread");
  const slots = count === 4 ? SPREAD4 : SPREAD5;
  const cards = Object.keys(slots).map(slug => ({ p: bySlug[slug], slot: slots[slug] }));
  const order = [...cards].sort((a, b) => a.slot - b.slot);
  mount.innerHTML = cards.map(({ p, slot }) => {
    const orderIndex = order.findIndex(c => c.p.slug === p.slug);
    const z = p.slug === "aios" ? 30 : 20 - Math.round(Math.abs(slot) * 4);
    return `<article class="card" style="--slot:${slot}; --depth:${Math.abs(slot)}; --slot-order:${orderIndex}; --z:${z}">
      ${matHtml(p)}
    </article>`;
  }).join("");
}

/* ------------------------------------------------- sphere focal */

function renderSphereFocal(mount) {
  mount.classList.add("deck--sphere-focal");
  const focal = bySlug.aios;
  const rest = products.filter(p => p.slug !== "aios");
  mount.innerHTML = `
    <div class="focal">${matHtml(focal, { shape: "sphere" })}</div>
    <div class="discs">
      ${rest.map(p => `
        <div class="disc">
          ${matHtml(p, { shape: "disc", live: false, wingsOnly: true })}
          <small>${esc(p.publicName)}</small>
        </div>`).join("")}
    </div>`;
}

/* ------------------------------------------------- single card */

function renderSingle(mount) {
  mount.classList.add("deck--single");
  mount.innerHTML = `<article class="card">${matHtml(bySlug.aios)}</article>`;
}

/* ------------------------------------------------------ bento */

function renderBento(mount) {
  mount.classList.add("deck--bento");
  const rest = products.filter(p => p.slug !== "aios");
  mount.innerHTML =
    `<article class="card card--lead">${matHtml(bySlug.aios)}</article>` +
    rest.map(p => `<article class="card">${matHtml(p, { live: false })}</article>`).join("");
}

/* ============================================= auto carousels (V15–V19) */

const CAROUSEL_ORDER = ["aios", "context-engine", "ai-ads-system", "claude-code-os", "organic-content-os"];
const CAROUSEL_INTERVAL = 3200;

function focalCard(slug, shape) {
  return matHtml(bySlug[slug], { shape: shape || "rect", live: true, focal: true });
}
function dotsNav() {
  return `<div class="carousel-nav carousel-dots">${CAROUSEL_ORDER.map((s, i) =>
    `<button type="button" class="carousel-dot" data-jump-i="${i}" aria-current="${i === 0}" aria-label="${esc(bySlug[s].publicName)}"></button>`).join("")}</div>`;
}

function renderCarousel(mount) {
  const style = mount.closest(".lab").dataset.carousel;
  mount.classList.add("deck--carousel", `carousel--${style}`);
  const first = CAROUSEL_ORDER[0];

  if (style === "deck") {
    mount.innerHTML =
      `<div class="carousel-stage">
         <div class="carousel-back" style="--o:2"></div>
         <div class="carousel-back" style="--o:1"></div>
         ${focalCard(first)}
       </div>${dotsNav()}`;
  } else if (style === "split") {
    mount.innerHTML =
      `<div class="carousel-rail">${CAROUSEL_ORDER.map((s, i) =>
         `<button type="button" class="rail-tick" data-jump-i="${i}" aria-current="${i === 0}" aria-label="${esc(bySlug[s].publicName)}"></button>`).join("")}</div>
       <div class="carousel-copy">
         <span class="carousel-copy__eyebrow">Mez Systems</span>
         <div data-carousel-copy></div>
       </div>
       <div class="carousel-stage">${focalCard(first)}</div>`;
  } else if (style === "reel") {
    mount.innerHTML =
      `<div class="carousel-stage carousel-stage--reel">
         <div class="reel-edge reel-edge--top"></div>
         <div class="reel-edge reel-edge--bottom"></div>
         ${focalCard(first)}
       </div>${dotsNav()}`;
  } else if (style === "sphere") {
    mount.innerHTML =
      `<div class="carousel-stage carousel-stage--sphere">${focalCard(first, "sphere")}</div>
       <div class="carousel-chips">${CAROUSEL_ORDER.map((s, i) =>
         `<button type="button" class="carousel-chip" data-jump-i="${i}" aria-current="${i === 0}">
            ${matHtml(bySlug[s], { shape: "disc", live: false, wingsOnly: true })}
            <small>${esc(bySlug[s].publicName)}</small>
          </button>`).join("")}</div>`;
  } else { // crossfade
    mount.innerHTML = `<div class="carousel-stage">${focalCard(first)}</div>${dotsNav()}`;
  }
}

function updateSplitCopy(section, p, idx) {
  const box = section.querySelector("[data-carousel-copy]");
  if (!box) return;
  const live = p.availability === "live";
  box.innerHTML =
    `<span class="carousel-copy__index">${String(idx + 1).padStart(2, "0")} / ${String(CAROUSEL_ORDER.length).padStart(2, "0")}</span>
     <strong class="carousel-copy__name">${esc(p.publicName)}</strong>
     <span class="carousel-copy__fn">${esc(p.summary)}</span>
     <span class="carousel-copy__status ${live ? "is-live" : ""}">${live ? "Available now" : "Coming soon"}</span>`;
}

function applyCarousel(section, idx, animate) {
  const style = section.dataset.carousel;
  const p = bySlug[CAROUSEL_ORDER[idx]];
  section.querySelectorAll("[data-jump-i]").forEach((b, n) => b.setAttribute("aria-current", String(n === idx)));
  const focal = section.querySelector("[data-focal]");
  if (!focal) return;
  const swap = () => {
    if (renderer && focal.dataset.mzCoreMode === "live") {
      try { renderer.setCore(focal, p.gradientId); } catch (e) { /* surface unmounted mid-flight */ }
    }
    focal.style.setProperty("--material", `url('${twin(p.gradientId)}')`);
    const id = focal.querySelector(".mat-identity");
    if (id) {
      const st = id.querySelector("strong"); if (st) st.textContent = p.publicName;
      const sp = id.querySelector("span"); if (sp) sp.textContent = p.function;
    }
    if (style === "split") updateSplitCopy(section, p, idx);
  };
  if (animate && !reducedMotion && focal.animate) {
    const E = "cubic-bezier(.22,1,.36,1)";
    const outKf = style === "deck"
      ? [{ transform: "translateX(0)", opacity: 1 }, { transform: "translateX(48px) rotate(3deg)", opacity: 0 }]
      : style === "reel"
        ? [{ transform: "translateY(0)", opacity: 1 }, { transform: "translateY(-42px)", opacity: 0 }]
        : [{ opacity: 1, transform: "scale(1)" }, { opacity: 0, transform: "scale(.985) translateY(6px)" }];
    const inKf = style === "deck"
      ? [{ transform: "translateX(-42px) rotate(-2deg)", opacity: 0 }, { transform: "none", opacity: 1 }]
      : style === "reel"
        ? [{ transform: "translateY(42px)", opacity: 0 }, { transform: "none", opacity: 1 }]
        : [{ opacity: 0, transform: "scale(.99) translateY(-6px)" }, { opacity: 1, transform: "none" }];
    // Cancel between stages so no forwards-fill lingers and traps the card at opacity 0.
    focal.getAnimations().forEach(a => a.cancel());
    focal.animate(outKf, { duration: 240, easing: E, fill: "forwards" }).finished.then(() => {
      focal.getAnimations().forEach(a => a.cancel()); // release the out-fill before swapping content
      swap();
      focal.animate(inKf, { duration: 320, easing: E, fill: "forwards" }).finished
        .then(() => focal.getAnimations().forEach(a => a.cancel())) // settle to base (visible)
        .catch(() => {});
    }).catch(() => {});
  } else {
    swap();
  }
}

function setupCarousels() {
  document.querySelectorAll("[data-carousel]").forEach(section => {
    const state = { i: 0, timer: null, paused: false };
    section.addEventListener("pointerenter", () => { state.paused = true; });
    section.addEventListener("pointerleave", () => { state.paused = false; });
    section.querySelectorAll("[data-jump-i]").forEach(btn => {
      btn.addEventListener("click", () => { state.i = Number(btn.dataset.jumpI); applyCarousel(section, state.i, true); });
    });
    applyCarousel(section, 0, false); // initialise navigator + copy before first mount
    section.__afterMount = () => {
      state.i = 0;
      applyCarousel(section, 0, false);
      if (reducedMotion) return; // no autoplay under reduced motion; manual nav still works
      clearInterval(state.timer);
      state.timer = setInterval(() => {
        if (state.paused || document.hidden || section !== activeSection) return;
        state.i = (state.i + 1) % CAROUSEL_ORDER.length;
        applyCarousel(section, state.i, true);
      }, CAROUSEL_INTERVAL);
    };
    section.__afterUnmount = () => { clearInterval(state.timer); state.timer = null; };
  });
}

const RENDERERS = {
  arc: (m, count, opts) => renderArc(m, count, opts),
  spread: (m, count) => renderSpread(m, count),
  stack: renderStack,
  shelf: renderShelf,
  "sphere-focal": renderSphereFocal,
  single: renderSingle,
  bento: renderBento
};

document.querySelectorAll("[data-cards]").forEach(mount => {
  const layout = mount.dataset.layout;
  const count = Number(mount.dataset.count || 5);
  const staticSection = mount.closest("[data-static]");
  if (layout === "arc") RENDERERS.arc(mount, count, { staticCards: Boolean(staticSection) });
  else if (layout === "carousel") renderCarousel(mount);
  else RENDERERS[layout]?.(mount, count);
});

/* --------------------------------------------- live-core allocation */

let renderer = null;
let activeSection = null;
const liveSurfaces = new Map(); // section -> [elements]

function unmountSection(section) {
  const els = liveSurfaces.get(section);
  if (!els || !renderer) return;
  els.forEach(el => {
    renderer.surfaces?.delete(el);
    el.querySelector("canvas[data-mz-core-canvas]")?.remove();
    el.removeAttribute("data-mz-core");
  });
  liveSurfaces.delete(section);
  if (section.__afterUnmount) section.__afterUnmount();
}

function mountSection(section) {
  if (!renderer || reducedMotion) return;
  if (section.dataset.static === "true") return;
  const els = [...section.querySelectorAll("[data-live]")];
  els.forEach(el => {
    try {
      renderer.mount(el, el.dataset.gradientId, {
        shape: el.dataset.shape || "rect",
        radius: Number(el.dataset.radius || 0.16),
        profile: "deep"
      });
      el.dataset.mzCore = el.dataset.gradientId;
    } catch (error) {
      document.documentElement.dataset.coreFailure = error?.message || "unknown";
    }
  });
  liveSurfaces.set(section, els);
  if (section.__afterMount) section.__afterMount();
}

function setActive(section) {
  if (section === activeSection) return;
  if (activeSection) unmountSection(activeSection);
  activeSection = section;
  if (section) mountSection(section);
}

const sections = [...document.querySelectorAll(".lab")];

if (!reducedMotion) {
  try {
    const catalogue = await (await fetch(CATALOGUE_URL)).json();
    const mounted = await mountLivingCores(document, { catalogue, selector: "[data-hero-lab-never]", staticBaseUrl: STATIC_BASE });
    renderer = mounted.renderer;
  } catch (error) {
    document.documentElement.dataset.coreFailure = error?.message || "unknown";
  }

  const visibility = new Map();
  const observer = new IntersectionObserver(entries => {
    entries.forEach(e => visibility.set(e.target, e.intersectionRatio));
    let best = null, bestRatio = 0;
    sections.forEach(s => {
      const r = visibility.get(s) || 0;
      if (r > bestRatio) { bestRatio = r; best = s; }
    });
    if (best && bestRatio > 0.3) setActive(best);
  }, { threshold: [0, 0.3, 0.55, 0.8] });
  sections.forEach(s => observer.observe(s));
}

/* set up carousel controllers after `renderer` exists (they read it on init) */
setupCarousels();

/* --------------------------------------------- V09 entrance + cycle */

const cycleSection = document.querySelector('[data-motion="cycle"]');
if (cycleSection && !reducedMotion) {
  const cards = [...cycleSection.querySelectorAll(".card")];
  cards.forEach(c => c.classList.add("entrance-armed"));

  const enterObserver = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      cycleSection.classList.add("is-entered");
      enterObserver.disconnect();
      startCycle();
    });
  }, { threshold: 0.4 });
  enterObserver.observe(cycleSection);

  function startCycle() {
    let index = 0;
    let paused = false;
    cycleSection.addEventListener("pointerenter", () => { paused = true; });
    cycleSection.addEventListener("pointerleave", () => { paused = false; });
    setInterval(() => {
      if (paused || document.hidden) return;
      cards.forEach(c => c.classList.remove("is-front"));
      // bring cards to front by visual centre order
      const centreOrder = [...cards].sort((a, b) =>
        Math.abs(Number(a.style.getPropertyValue("--slot"))) - Math.abs(Number(b.style.getPropertyValue("--slot")))
      );
      centreOrder[index % centreOrder.length].classList.add("is-front");
      index += 1;
    }, 2600);
  }
}

/* --------------------------------------------------- jump nav */

const jump = document.querySelector("[data-jump]");
jump.innerHTML = sections.map(s => `<a href="#${s.id}">${s.dataset.variation}</a>`).join("");

/* --------------------------------------------------- verdicts */

const verdicts = new Map();
const status = document.querySelector("[data-status]");
let statusTimer = null;
function flash(message) {
  status.textContent = message;
  status.classList.add("is-shown");
  clearTimeout(statusTimer);
  statusTimer = setTimeout(() => status.classList.remove("is-shown"), 1800);
}

sections.forEach(section => {
  const group = section.querySelector("[data-verdict-group]");
  group.innerHTML = ["keep", "maybe", "kill"]
    .map(v => `<button type="button" data-verdict="${v}" aria-pressed="false">${v[0].toUpperCase() + v.slice(1)}</button>`)
    .join("");
  group.addEventListener("click", event => {
    const btn = event.target.closest("[data-verdict]");
    if (!btn) return;
    verdicts.set(section.dataset.variation, btn.dataset.verdict);
    group.querySelectorAll("[data-verdict]").forEach(b => b.setAttribute("aria-pressed", String(b === btn)));
  });
});

document.querySelector("[data-export]").addEventListener("click", async () => {
  const payload = {
    surface: "golden-homepage-hero-lab",
    recordedAgainst: "golden-homepage-01-r14",
    verdicts: sections.map(s => ({
      variation: s.dataset.variation,
      title: s.querySelector(".lab-head__id h2").textContent,
      verdict: verdicts.get(s.dataset.variation) || "unreviewed"
    }))
  };
  try {
    await navigator.clipboard.writeText(JSON.stringify(payload, null, 2));
    flash("Hero-lab verdicts copied to clipboard.");
  } catch {
    flash("Clipboard unavailable — open the console to copy.");
    console.log(JSON.stringify(payload, null, 2));
  }
});
