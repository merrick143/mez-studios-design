const WINGS = "../../../../source-pack/design-system-export/assets/wings.svg";

const variants = [
  { id: "V01", name: "Balanced bento", note: "Compact product card · orbit lead · split features", layout: "balance" },
  { id: "V02", name: "Product rail", note: "Identity left · mechanism centre · capability rail", layout: "rail" },
  { id: "V03", name: "Orbit first", note: "How it works owns the section", layout: "orbit-first" },
  { id: "V04", name: "Compact product strip", note: "Shallow identity event · generous mechanism", layout: "strip" },
  { id: "V05", name: "One dark canvas", note: "One composed field · no card pile", layout: "canvas" },
  { id: "V06", name: "Editorial bands", note: "Statement left · working proof right", layout: "editorial" },
  { id: "V07", name: "Two-by-two rooms", note: "Four authored cells · equal visual weight avoided", layout: "rooms" },
  { id: "V08", name: "Centred mechanism", note: "Orbit as identity event · quiet supporting cards", layout: "centred" },
  { id: "V09", name: "Operating ribbon", note: "Horizontal causal sequence · two outcome cards", layout: "ribbon" },
  { id: "V10", name: "Dense minimal", note: "Smallest footprint · least copy", layout: "minimal" }
];

const intro = () => `
  <header class="section-intro">
    <p class="eyebrow">Available now · AI OS</p>
    <h2>Give AI a business to understand.</h2>
    <p class="lead">One structured operating system for the context behind your work.</p>
  </header>`;

const product = (mode = "card") => `
  <article class="product product--${mode}" aria-label="AI OS product card">
    <div class="product__copy">
      <div>
        <p class="product__eyebrow">Available now</p>
        <h3>AI OS</h3>
        <span>AI Operating System</span>
      </div>
      <p>One reliable place for AI to understand what matters and why.</p>
      <a href="#">Explore the AI OS</a>
    </div>
    <div class="product__material" aria-hidden="true">
      <img src="${WINGS}" alt="" />
    </div>
  </article>`;

const orbit = (mode = "card") => `
  <article class="how how--${mode}" aria-label="How the AI OS works">
    <div class="panel-head">
      <p class="panel-kicker">How it works</p>
      <h3>Context in. Useful intelligence out.</h3>
    </div>
    <div class="orbit" aria-hidden="true">
      <span class="orbit__ring orbit__ring--3"></span>
      <span class="orbit__ring orbit__ring--2"></span>
      <span class="orbit__ring orbit__ring--1"></span>
      <span class="orbit__node orbit__node--context">Business context</span>
      <span class="orbit__node orbit__node--intel">Intelligence</span>
      <span class="orbit__core"><img src="${WINGS}" alt="" /><b>AI OS</b></span>
    </div>
    <p class="how__line">Business context <i>→</i> AI OS <i>→</i> the intelligence that fits.</p>
  </article>`;

const feature = (kind, mode = "card") => {
  const operate = kind === "operate";
  return `
    <article class="feature feature--${mode}">
      <span class="feature__no">${operate ? "01—02" : "03—04"}</span>
      <h3>${operate ? "Operate with context" : "Keep the why"}</h3>
      <ul>
        <li>${operate ? "Know what matters today" : "Retain decision reasoning"}</li>
        <li>${operate ? "Ask against real work" : "Connect direction to execution"}</li>
      </ul>
    </article>`;
};

const featureLedger = () => `
  <div class="feature-ledger" aria-label="AI OS features">
    <p>Know what matters today</p>
    <p>Ask against real work</p>
    <p>Retain decision reasoning</p>
    <p>Connect direction to execution</p>
  </div>`;

const ribbon = () => `
  <article class="mechanism-ribbon" aria-label="How the AI OS works">
    <div><span>01</span><b>Business context</b><small>Work, goals, decisions</small></div>
    <i aria-hidden="true">→</i>
    <div class="mechanism-ribbon__core"><img src="${WINGS}" alt="" /><b>AI OS</b><small>Structured operating layer</small></div>
    <i aria-hidden="true">→</i>
    <div><span>03</span><b>Intelligence</b><small>The model that fits</small></div>
  </article>`;

function composition(layout) {
  const pieces = {
    balance: `${intro()}<div class="bento">${product("compact")}${orbit()}<div class="feature-pair">${feature("operate")}${feature("remember")}</div></div>`,
    rail: `${intro()}<div class="bento">${product("vertical")}${orbit("wide")}<div class="feature-pair feature-pair--stack">${feature("operate")}${feature("remember")}</div></div>`,
    "orbit-first": `${intro()}<div class="bento">${orbit("hero")}${product("square")}${feature("operate")}${feature("remember")}</div>`,
    strip: `${intro()}<div class="bento">${product("strip")}${orbit("wide")}${feature("operate")}${feature("remember")}</div>`,
    canvas: `<div class="canvas-wrap">${intro()}${product("canvas")}${orbit("canvas")}${feature("operate", "canvas")}${feature("remember", "canvas")}</div>`,
    editorial: `<div class="editorial-wrap">${intro()}<div class="editorial-work">${product("editorial")}${orbit("editorial")}${featureLedger()}</div></div>`,
    rooms: `${intro()}<div class="bento">${product("room")}${orbit("room")}<div class="feature-pair">${feature("operate", "room")}${feature("remember", "room")}</div></div>`,
    centred: `${intro()}${product("pill")}<div class="centred-work">${orbit("centred")}<div class="feature-pair">${feature("operate", "quiet")}${feature("remember", "quiet")}</div></div>`,
    ribbon: `${intro()}${product("ribbon")}${ribbon()}<div class="feature-pair feature-pair--wide">${feature("operate", "outcome")}${feature("remember", "outcome")}</div>`,
    minimal: `<div class="minimal-wrap">${intro()}${product("minimal")}<div class="minimal-work">${orbit("minimal")}${featureLedger()}</div></div>`
  };
  return pieces[layout];
}

const main = document.querySelector("[data-variants]");
main.innerHTML = variants.map(variant => `
  <section class="lab" id="${variant.id.toLowerCase()}" data-variant="${variant.id}" data-layout="${variant.layout}">
    <header class="lab-head">
      <div><span>${variant.id}</span><h1>${variant.name}</h1><p>${variant.note}</p></div>
      <div class="verdicts" role="group" aria-label="Verdict for ${variant.id}">
        <button type="button" data-verdict="keep">Keep</button>
        <button type="button" data-verdict="maybe">Maybe</button>
        <button type="button" data-verdict="kill">Kill</button>
      </div>
    </header>
    <div class="stage">${composition(variant.layout)}</div>
  </section>`).join("");

document.querySelector("[data-nav]").innerHTML = variants
  .map(variant => `<a href="#${variant.id.toLowerCase()}">${variant.id.slice(1)}</a>`)
  .join("");

const storageKey = "mez-aios-lab-v1";
let verdictState = {};
try { verdictState = JSON.parse(localStorage.getItem(storageKey) || "{}"); } catch { verdictState = {}; }

function paintVerdicts() {
  document.querySelectorAll("[data-variant]").forEach(section => {
    const selected = verdictState[section.dataset.variant];
    section.querySelectorAll("[data-verdict]").forEach(button => {
      button.setAttribute("aria-pressed", String(button.dataset.verdict === selected));
    });
  });
}

document.addEventListener("click", event => {
  const button = event.target.closest("[data-verdict]");
  if (!button) return;
  const section = button.closest("[data-variant]");
  verdictState[section.dataset.variant] = button.dataset.verdict;
  localStorage.setItem(storageKey, JSON.stringify(verdictState));
  paintVerdicts();
});

document.querySelector("[data-copy]").addEventListener("click", async () => {
  const lines = variants.map(({ id, name }) => `${id} ${name}: ${verdictState[id] || "unreviewed"}`);
  await navigator.clipboard.writeText(lines.join("\n"));
  const status = document.querySelector("[data-status]");
  status.textContent = "Verdicts copied";
  status.classList.add("is-visible");
  setTimeout(() => status.classList.remove("is-visible"), 1400);
});

paintVerdicts();
