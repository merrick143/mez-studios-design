/** Mez Systems · Trading Card 01 · canonical 1.0.0 proof controller. */
import { mountLivingCores } from "../../../source-pack/design-system-export/mz-core.js";

const STATIC_BASE = "../../../gradient-library/assets/static/";
const WINGS_URL = "../../../source-pack/design-system-export/assets/wings.svg";
const query = new URLSearchParams(location.search);
const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
const forceStatic = query.has("static") || reduced;
const disableWebGL = query.has("no-webgl");
const familyTitles = {faces:"Card Faces",backs:"Information Backs",decks:"Decks and Packs",placements:"Website Placements"};
const specs = [
  {id:"TC-F01",family:"faces",title:"Anchored identity",note:"Bottom-anchored Wings and name with a controlled contrast zone.",variant:"anchored",product:0},
  {id:"TC-F02",family:"faces",title:"Centred identity refined",note:"Optically lifted Wings, measured name and more calm around the centred event.",variant:"centred",product:1},
  {id:"TC-F03",family:"faces",title:"Measured name",note:"The bold name direction survives with a fit-safe scale for every product.",variant:"oversized",product:2},
  {id:"TC-F05",family:"faces",title:"Corner identity",note:"Small supporting Wings with a strong lower-left reading order.",variant:"corner",product:4},
  {id:"TC-B01",family:"backs",title:"Product orientation refined",note:"The same useful reverse with a fully contained, fit-safe primary action.",variant:"orientation",product:0},
  {id:"TC-B02",family:"backs",title:"Operating sequence — static and alive",note:"The sequence is identical in both twins; its focal material is static on the left and alive on the right.",variant:"sequence",product:3},
  {id:"TC-B05",family:"backs",title:"Waitlist opening",note:"A completely rebuilt full-field waitlist card with one clear, honest action.",variant:"access",product:4},
  {id:"TC-B06",family:"backs",title:"Quiet reverse refined",note:"A calmer, useful reverse with one visual anchor and one properly contained action.",variant:"quiet",product:0},
  {id:"TC-D01",family:"decks",title:"Single object",note:"The baseline card as one portable product object.",variant:"single",product:0},
  {id:"TC-D02",family:"decks",title:"Connected pair",note:"Two products with a direct operating relationship.",variant:"pair",product:0},
  {id:"TC-D03",family:"decks",title:"Consistent operating handoff",note:"Two cards share the same face anatomy; the relationship comes from sequence, not mixed designs.",variant:"handoff",product:1},
  {id:"TC-D04",family:"decks",title:"Measured three-stack",note:"Three products overlap only enough to show a focused operating layer.",variant:"stack",product:2},
  {id:"TC-D05",family:"decks",title:"Five-system deck",note:"The whole family reads as one measured deck, not a grid reskin.",variant:"family",product:0},
  {id:"TC-D06",family:"decks",title:"Contained light pack",note:"A white package holds a real three-product relationship.",variant:"pack-light",product:0},
  {id:"TC-D07",family:"decks",title:"Contained charcoal pack",note:"Contained charcoal frames a family without pure black or white strokes.",variant:"pack-dark",product:0},
  {id:"TC-D08",family:"decks",title:"Compact mobile deck",note:"Container-aware overlap for narrow screens.",variant:"mobile-deck",product:0},
  {id:"TC-P01",family:"placements",title:"Single-product hero",note:"One full-field card acts as the product identity event.",variant:"hero",product:0},
  {id:"TC-P02",family:"placements",title:"Full-field launch",note:"A wide product launch uses the card grammar without a literal floating card.",variant:"launch",product:2},
  {id:"TC-P03",family:"placements",title:"Product explainer recomposed",note:"A light-overlay face and disciplined reading column explain one operating mechanism.",variant:"explainer",product:3},
  {id:"TC-P05",family:"placements",title:"Operating-layer sequence",note:"Three consistent cards sit in an explicit input-to-output sequence.",variant:"story",product:1},
  {id:"TC-P06",family:"placements",title:"Suite feature — balanced deck",note:"Five cards form one centred, measured deck below the offer with controlled overlap and no copy collision.",variant:"suite",product:0},
  {id:"TC-P07",family:"placements",title:"Mobile product opening",note:"The portrait object and product hierarchy recompose for one hand.",variant:"mobile-product",product:4},
  {id:"TC-P08",family:"placements",title:"Mobile family pack",note:"A compact family deck stays container-aware and legible.",variant:"mobile-pack",product:0}
];

const state = {
  decisions: Object.fromEntries(specs.map(spec => [spec.id, "keep"])),
  specimenNotes: {},
  familyNotes: {},
  leadingFamily: "undecided",
  note: "Round 03 received 23 unanimous keeps. Lock the surviving Trading Card expression, close EXP-05 and proceed."
};
let renderer = null;
let activeSurface = null;
let observer = null;
const visibility = new Map();

function h(tag, className = "", text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

async function fetchJson(url) {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`${url} failed: ${response.status}`);
  return response.json();
}

function viewModel(products) {
  return products.map(product => ({
    ...product,
    field:`${STATIC_BASE}${product.gradientId.toLowerCase()}.webp`,
    availabilityLabel:product.availability === "live" ? "Available now" : "Coming soon",
    action:product.availability === "live" ? "Explore AI OS" : "Join waitlist"
  }));
}

function wings(className = "tc-wings") {
  const image = h("img", className);
  image.src = WINGS_URL;
  image.alt = "";
  return image;
}

function material(product, className, live = false) {
  const node = h("div", className);
  node.style.setProperty("--field", `url("${product.field}")`);
  node.dataset.gradientId = product.gradientId;
  if (live) node.dataset.autoLive = "";
  return node;
}

function productIdentity(product, options = {}) {
  const copy = h("div", `tc-identity${options.compact ? " is-compact" : ""}`);
  if (options.wings !== false) copy.append(wings(options.large ? "tc-wings is-large" : "tc-wings"));
  copy.append(h(options.heading || "h4", "tc-name", product.publicName));
  copy.append(h("span", "tc-function", product.function));
  if (options.summary) copy.append(h("p", "tc-summary", product.summary));
  return copy;
}

function faceCard(product, variant, live = false, mini = false) {
  const card = h("article", `tc-card tc-face face--${variant}${mini ? " is-mini" : ""}`);
  const field = material(product, "tc-field", live);
  card.append(field);
  if (variant === "anchored") card.append(productIdentity(product, {large:true}));
  if (variant === "centred") card.append(productIdentity(product, {large:true}));
  if (variant === "oversized") {
    card.append(wings("tc-corner-wings"));
    const copy = productIdentity(product, {wings:false});
    card.append(copy);
  }
  if (variant === "nameplate") {
    field.append(wings("tc-field-wings"));
    card.append(productIdentity(product, {wings:false,summary:true}));
  }
  if (variant === "corner") {
    card.append(wings("tc-corner-wings"));
    card.append(productIdentity(product, {wings:false,summary:true}));
  }
  if (variant === "protected") {
    card.append(h("span", "tc-protected-edge"));
    card.append(productIdentity(product, {large:true}));
  }
  if (variant === "square" || variant === "landscape") card.append(productIdentity(product, {large:true,summary:variant === "landscape"}));
  return card;
}

function action(label, secondary = false) {
  const button = h("button", secondary ? "tc-action is-secondary" : "tc-action", label);
  button.type = "button";
  return button;
}

function backCard(product, variant, live = false) {
  const card = h("article", `tc-card tc-back back--${variant}`);
  if (variant === "access") {
    const field = material(product, "tc-waitlist-field", false);
    field.append(wings("tc-waitlist-wings"));
    const copy = h("div", "tc-waitlist-copy");
    copy.append(h("span", "tc-eyebrow", "OPENING SOON"), h("h4", "tc-name", product.publicName), h("span", "tc-function", product.function), h("p", "tc-back-lede", "Be first to see the complete system when access opens."));
    const form = h("div", "tc-waitlist-form");
    form.append(h("span", "tc-waitlist-input", "you@company.com"), action("Join waitlist"));
    copy.append(form, h("small", "tc-waitlist-note", "Product updates only. Leave any time."));
    card.append(field, copy);
    return card;
  }
  const accent = material(product, "tc-back-accent", live && variant === "sequence");
  accent.append(wings("tc-back-wings"));
  const head = h("header", "tc-back-head");
  head.append(h("h4", "tc-name", product.publicName), h("span", "tc-function", product.function));
  const body = h("div", "tc-back-body");
  if (variant === "orientation") {
    body.append(h("p", "tc-back-lede", product.summary));
    const list = h("ul", "tc-points");
    ["Shared operating context","Repeatable operating runs","Proof stays attached"].forEach(text => list.append(h("li", "", text)));
    body.append(list, action(product.action));
  }
  if (variant === "sequence") {
    const list = h("ol", "tc-sequence");
    [["01","Frame the work"],["02","Run the system"],["03","Verify the result"]].forEach(([n,text]) => { const li=h("li"); li.append(h("span","",n),h("strong","",text)); list.append(li); });
    body.append(list);
  }
  if (variant === "quiet") body.append(h("span", "tc-eyebrow", "ONE SYSTEM / ONE JOB"), h("p", "tc-back-lede", product.summary), action(product.action));
  card.append(accent, head, body);
  return card;
}

function deckCards(products, indexes, liveIndex = -1, variant = "anchored") {
  const deck = h("div", "tc-deck-cards");
  indexes.forEach((productIndex, index) => {
    const card = faceCard(products[productIndex % products.length], variant, index === liveIndex, true);
    card.style.setProperty("--i", index);
    deck.append(card);
  });
  return deck;
}

function deckComposition(product, products, variant, live) {
  const shell = h("section", `deck-composition deck--${variant}`);
  if (variant === "single") shell.append(faceCard(product, "anchored", live));
  if (variant === "pair") {
    shell.append(deckCards(products, [0,1], live ? 0 : -1));
    const copy=h("div","deck-copy"); copy.append(h("span","tc-eyebrow","CONNECTED SYSTEMS"),h("h4","","AI OS + Context Engine"),h("p","","The operating system and the context layer it runs on.")); shell.append(copy);
  }
  if (variant === "handoff") {
    shell.append(faceCard(products[1], "corner", live), h("span","deck-arrow","→"), faceCard(products[3], "corner", false));
  }
  if (variant === "stack") shell.append(deckCards(products, [2,3,4], live ? 2 : -1));
  if (variant === "family") shell.append(deckCards(products, [0,1,2,3,4], live ? 4 : -1));
  if (variant === "pack-light" || variant === "pack-dark") {
    const copy=h("div","deck-copy"); copy.append(h("span","tc-eyebrow","THE OPERATING LAYER"),h("h4","","Start with one. Add the next system when it earns its place."),h("p","","Three connected products shown as one real operating relationship."),action("Explore the systems"));
    shell.append(deckCards(products,[0,1,3],live ? 2 : -1),copy);
  }
  if (variant === "mobile-deck") {
    const phone=h("div","tc-phone"); phone.append(h("div","tc-phone-bar","9:41   MEZ SYSTEMS"),deckCards(products,[0,1,2],live ? 2 : -1),h("h4","","Three systems. One operating layer."),action("Explore the family")); shell.append(phone);
  }
  return shell;
}

function placement(product, products, variant, live) {
  const section = h("section", `tc-placement place--${variant}`);
  const copy = h("div", "placement-copy");
  const identity = () => {
    copy.append(h("span","tc-eyebrow",variant === "suite" ? "THE COMPLETE SUITE" : "MEZ SYSTEMS PRODUCT"),h("h3","",product.publicName),h("span","tc-function",product.function),h("p","",product.summary),action(product.action));
  };
  if (variant === "hero") { identity(); section.append(copy,faceCard(product,"anchored",live)); }
  if (variant === "launch") {
    const field=material(product,"placement-full-field",live); field.append(wings("placement-wings"));
    copy.append(h("h3","",product.publicName),h("span","tc-function",product.function),h("p","",product.summary),action(product.action)); section.append(field,copy);
  }
  if (variant === "explainer") {
    identity(); const steps=h("ol","placement-steps"); ["Frame the run","Operate the work","Keep proof attached"].forEach((text,index)=>{const li=h("li");li.append(h("span","",`0${index+1}`),h("strong","",text));steps.append(li);}); copy.append(steps); section.append(faceCard(product,"anchored",live),copy);
  }
  if (variant === "rail") {
    const head=h("header","placement-head");head.append(h("span","tc-eyebrow","FIND YOUR SYSTEM"),h("h3","","Five focused systems. One product language."));
    const rail=h("div","placement-rail");products.forEach((item,index)=>rail.append(faceCard(item,"corner",live&&index===0,true)));section.append(head,rail);
  }
  if (variant === "story") {
    copy.append(h("span","tc-eyebrow","ONE OPERATING STORY"),h("h3","","Context in. Verified work out."),h("p","","One consistent card anatomy makes each system legible; the sequence explains the relationship."));
    const sequence=h("div","placement-sequence");
    [[1,"01","Context"],[0,"02","Operate"],[3,"03","Verify"]].forEach(([index,number,label],step)=>{const item=h("div","placement-sequence-item");item.append(h("span","sequence-label",`${number} / ${label}`),faceCard(products[index],"corner",live&&step===1,true));sequence.append(item);});
    section.append(copy,sequence);
  }
  if (variant === "suite") {
    identity();
    const suiteDeck=deckCards(products,[0,1,2,3,4],live?2:-1);
    suiteDeck.classList.add("is-suite-stage");
    section.append(copy,suiteDeck);
  }
  if (variant === "mobile-product") {
    const phone=h("div","tc-phone");phone.append(h("div","tc-phone-bar","9:41   PRODUCT"),faceCard(product,"anchored",live),h("h3","",product.publicName),h("span","tc-function",product.function),h("p","",product.summary),action(product.action));section.append(phone);
  }
  if (variant === "mobile-pack") {
    const phone=h("div","tc-phone");phone.append(h("div","tc-phone-bar","9:41   SYSTEMS"),deckCards(products,[0,1,2],live?2:-1),h("h3","","Build your operating layer."),h("p","","Start with the job that matters now."),action("Explore all systems"));section.append(phone);
  }
  return section;
}

function specimenBuild(spec, product, products, live) {
  if (spec.family === "faces") return faceCard(product, spec.variant, live);
  if (spec.family === "backs") return backCard(product, spec.variant, live);
  if (spec.family === "decks") return deckComposition(product, products, spec.variant, live);
  return placement(product, products, spec.variant, live);
}

function verdicts(id) {
  const controls=h("div","specimen-verdicts");
  [["keep","Keep"],["revise","Revise"],["kill","Kill"]].forEach(([verdict,label])=>{const button=h("button","",label);button.type="button";button.dataset.verdict=verdict;button.disabled=true;button.setAttribute("aria-label",`${label} ${id}`);controls.append(button);});
  return controls;
}

function reviewable(spec, products) {
  const product=products[spec.product % products.length];
  const article=h("article",`specimen specimen--${spec.family}`);article.id=spec.id.toLowerCase();article.dataset.specimenId=spec.id;article.dataset.specimenTitle=spec.title;article.dataset.specimenFamily=spec.family;
  const head=h("header","specimen-head");const identity=h("div","specimen-identity");identity.append(h("span","specimen-id",spec.id),h("h3","",spec.title),h("p","",spec.note));head.append(identity,verdicts(spec.id));
  const comparison=h("div","specimen-comparison");
  [["Static",false],[spec.id === "TC-B02" ? "Automatic" : spec.family === "backs" ? "Static twin" : "Automatic",true]].forEach(([label,live])=>{const pane=h("div",`specimen-pane${live?" is-motion":""}`);pane.append(h("span","state-label",label),specimenBuild(spec,product,products,live));comparison.append(pane);});
  const feedback=h("label","specimen-feedback");feedback.append(h("span","",`Approval for ${spec.id}`));const textarea=h("textarea");textarea.rows=2;textarea.dataset.specimenNote=spec.id;textarea.value="Kept in the unanimous Round 03 approval.";textarea.disabled=true;feedback.append(textarea);
  article.append(head,comparison,feedback);return article;
}

function render(products) {
  specs.forEach(spec=>document.querySelector(`[data-mount="${spec.family}"]`).append(reviewable(spec,products)));
}

function persist() {}

function updateSummary() {
  const summary=document.querySelector("[data-review-summary]");summary.innerHTML="";
  ["keep","revise","kill"].forEach(verdict=>{const item=h("div");item.append(h("strong","",String(Object.values(state.decisions).filter(value=>value===verdict).length)),h("span","",verdict));summary.append(item);});
  const item=h("div");item.append(h("strong","","1"),h("span","","approval"));summary.append(item);
}

function updateReview() {
  document.querySelectorAll("[data-verdict]").forEach(button=>{const id=button.closest("[data-specimen-id]").dataset.specimenId;button.setAttribute("aria-pressed",String(state.decisions[id]===button.dataset.verdict));});
  document.querySelectorAll("[data-specimen-id]").forEach(node=>node.dataset.selectedVerdict=state.decisions[node.dataset.specimenId]||"");updateSummary();persist();
}

function hydrateReview() { document.querySelector("[data-leading-family]").value=state.leadingFamily; }

function exportPayload() {
  return {
    schemaVersion:"1.0.0",
    gateId:"H-EXP-05-TRADING-CARD-PROOF",
    taskId:"TASK-EXP-05-TRADING-CARD",
    candidateRevision:"trading-card-01-r03",
    verdict:"approve",
    leadingFamily:state.leadingFamily,
    note:state.note,
    sections:Object.entries(familyTitles).map(([id,title])=>({id,title,verdict:"approve"})),
    specimens:specs.map(spec=>({id:spec.id,title:spec.title,family:spec.family,verdict:"keep",feedback:""})),
    decisionId:"DEC-TRADING-CARD-EXPRESSION-001",
    resultingStatus:"canonical",
    productionAuthority:true
  };
}

function bindReview() {
  const panel=document.querySelector("#review-panel");const trigger=document.querySelector("[data-review-open]");
  const toggle=open=>{document.body.classList.toggle("is-reviewing",open);panel.setAttribute("aria-hidden",String(!open));trigger.setAttribute("aria-expanded",String(open));if(open)document.querySelector("[data-review-close]").focus();};
  document.addEventListener("click",event=>{if(event.target.closest("[data-review-open]"))toggle(true);if(event.target.closest("[data-review-close]"))toggle(false);});
  document.querySelector("[data-export]").addEventListener("click",async event=>{const output=JSON.stringify(exportPayload(),null,2);document.querySelector("[data-review-output]").textContent=output;try{await navigator.clipboard.writeText(output);event.target.textContent="Copied";}catch{event.target.textContent="Approval ready below";}});
  addEventListener("keydown",event=>{if(event.key==="Escape")toggle(false);});hydrateReview();updateReview();
}

function setCoreMode(text) { document.querySelectorAll("[data-core-mode]").forEach(node=>node.textContent=`Core mode: ${text}`); }
function demote() { if(!activeSurface)return;renderer?.surfaces?.delete(activeSurface);activeSurface.querySelector("canvas[data-mz-core-canvas]")?.remove();activeSurface.removeAttribute("data-mz-core");activeSurface.classList.remove("is-live");activeSurface=null; }
function moveCore(target) { if(forceStatic||disableWebGL||!renderer||target===activeSurface)return;const coreId=target.dataset.gradientId;if(!coreId)return;demote();const rect=target.getBoundingClientRect();const radius=Math.min(.34,24/(Math.min(rect.width,rect.height)/2||1));try{renderer.mount(target,coreId,{shape:"rect",radius,profile:"deep"});target.dataset.mzCore=coreId;target.classList.add("is-live");activeSurface=target;const id=target.closest("[data-specimen-id]")?.dataset.specimenId||"cover";setCoreMode(`automatic live focus · ${id} · Deep Mineral No. 5`);}catch(error){document.documentElement.dataset.coreError=error?.message||"unknown";setCoreMode("exact static twin · renderer fallback");} }
function chooseTarget() { const best=[...visibility.entries()].filter(([,ratio])=>ratio>.08).sort((a,b)=>b[1]-a[1])[0];if(best)moveCore(best[0]); }
function bindMotion() { if(forceStatic||disableWebGL||!renderer)return;observer=new IntersectionObserver(entries=>{entries.forEach(entry=>visibility.set(entry.target,entry.isIntersecting?entry.intersectionRatio:0));chooseTarget();},{rootMargin:"-12% 0px -12% 0px",threshold:[0,.08,.2,.35,.5,.7,.9]});document.querySelectorAll("[data-auto-live]").forEach(target=>observer.observe(target)); }
async function initialiseMotion() { if(forceStatic){setCoreMode(reduced?"exact static twin · reduced motion":"exact static twin · forced");return;}if(disableWebGL){setCoreMode("exact static twin · simulated renderer failure");return;}try{const catalogue=await fetchJson("../../../gradient-library/catalogue.json");const mounted=await mountLivingCores(document,{catalogue,staticBaseUrl:"../../gradient-library/assets/static/"});renderer=mounted.renderer;setCoreMode("automatic live focus · waiting for a specimen");bindMotion();}catch(error){document.documentElement.dataset.coreMoveError=error?.message||"unknown";setCoreMode("exact static twin · renderer fallback");} }

async function main() {
  try {
    const registry=await fetchJson("../../../registry/products.json");const products=viewModel(registry.products);render(products);
    const deepLink=document.getElementById(location.hash.slice(1));
    if(deepLink)requestAnimationFrame(()=>deepLink.scrollIntoView({block:"start"}));
    if(document.querySelectorAll("[data-specimen-id]").length!==23)throw new Error("Expected 23 canonical specimens");
    bindReview();await initialiseMotion();
  } catch(error) {
    console.error(error);const failure=h("p","render-failure",`Trading Card 1.0.0 failed: ${error.message}`);document.body.prepend(failure);
  }
}

main();
