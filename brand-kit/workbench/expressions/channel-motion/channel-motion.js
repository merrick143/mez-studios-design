/** Mez Systems · EXP-07 Website Motion · canonical 1.0.0 proof controller. */
import { mountLivingCores } from "../../../source-pack/design-system-export/mz-core.js";

const STATIC_BASE = "../../../gradient-library/assets/static/";
const WINGS_URL = "../../../source-pack/design-system-export/assets/wings.svg";
const query = new URLSearchParams(location.search);
const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
const forceStatic = query.has("static") || reduced;
const disableWebGL = query.has("no-webgl");
const familyTitles = {laws:"Motion Laws",components:"Website Components"};

const specs = [
  {id:"MOT-L01",family:"laws",title:"Focal material",note:"One approved product field may feel alive while its object, Wings, copy and action stay fixed.",pattern:"focal-material",auto:"core",product:0,staticLabel:"Exact static product",motionLabel:"One live material"},
  {id:"MOT-L02",family:"laws",title:"Functional response",note:"A direct action receives one short confirmation. The interface does not perform for attention.",pattern:"functional-ui",product:1,staticLabel:"Immediate complete state",motionLabel:"120–180ms response"},
  {id:"MOT-L03",family:"laws",title:"Simple demonstration",note:"One input becomes one retained result. No storyboard, no film language and no looping narrative.",pattern:"simple-demonstration",auto:"demo",product:3,staticLabel:"Complete before and after",motionLabel:"One short pass"},
  {id:"MOT-W01",family:"components",title:"Section entry",note:"Nearby content enters once with a small fade and 16px of travel. There is no scroll choreography.",pattern:"section-entry",auto:"entry",product:4,staticLabel:"Content already present",motionLabel:"Single 360ms entry"},
  {id:"MOT-W03",family:"components",title:"Accordion and tabs",note:"Selection changes the nearby content plane. The response is local, brief and reversible.",pattern:"accordion-tabs",product:1,staticLabel:"All content available",motionLabel:"Try tabs and disclosure"},
  {id:"MOT-W04",family:"components",title:"Product carousel",note:"A user-driven product rail moves one measured step. It never autoplays and never hides navigation.",pattern:"product-carousel",product:2,staticLabel:"Static product family",motionLabel:"User-driven rail"},
  {id:"MOT-W05",family:"components",title:"Processor and progress",note:"Progress reports real sequence and completion. It runs only after user intent and never loops.",pattern:"processor-progress",product:3,staticLabel:"Complete result",motionLabel:"Run the processor"}
];

const state = {
  decisions:Object.fromEntries(specs.map(spec=>[spec.id,"keep"])),
  specimenNotes:{},
  familyNotes:{},
  leadingFamily:"website-motion",
  note:"Seven Round 03 specimens are approved. MOT-W02 is deferred to TASK-CMP-01-GLOBAL-NAVIGATION."
};

let renderer = null;
let activeMotion = null;
let observer = null;
let resumeTimer = null;
const visibility = new Map();

function h(tag,className="",text) {
  const node=document.createElement(tag);
  if(className)node.className=className;
  if(text!==undefined)node.textContent=text;
  return node;
}

async function fetchJson(url) {
  const response=await fetch(url);
  if(!response.ok)throw new Error(`${url} failed: ${response.status}`);
  return response.json();
}

function viewModel(products) {
  return products.map(product=>({...product,field:`${STATIC_BASE}${product.gradientId.toLowerCase()}.webp`}));
}

function wings(className="motion-wings") {
  const image=h("img",className);image.src=WINGS_URL;image.alt="";return image;
}

function material(product,className="material") {
  const node=h("div",className);node.style.setProperty("--field",`url("${product.field}")`);node.dataset.gradientId=product.gradientId;return node;
}

function focalCard(product,live=false) {
  const card=h("article","focal-card");
  const field=material(product,"focal-field");if(live)field.dataset.coreHost="";field.append(wings("focal-wings"));
  const copy=h("div","focal-copy");copy.append(h("span","","MEZ SYSTEMS PRODUCT"),h("h4","",product.publicName),h("p","",product.function),h("b","","Explore the system"));
  card.append(field,copy);return card;
}

function functionalPanel(product,interactive=false) {
  const shell=h("div",`functional-panel${interactive?" is-interactive":" is-complete"}`);
  const head=h("header");head.append(h("span","","WORKSPACE SETTINGS"),h("small","",product.publicName));
  const row=h("div","functional-row");const copy=h("div");copy.append(h("strong","","Retain proof records"),h("span","","Keep source, run and verification attached."));
  const toggle=h("button","functional-toggle");toggle.type="button";toggle.setAttribute("aria-pressed","true");toggle.dataset.functionalToggle="";toggle.append(h("i"));
  row.append(copy,toggle);
  const foot=h("footer");foot.append(h("span","functional-status",interactive?"Ready":"Saved"),h("button","functional-save",interactive?"Save change":"Complete"));
  foot.lastChild.type="button";if(interactive)foot.lastChild.dataset.functionalSave="";else foot.lastChild.disabled=true;
  shell.append(head,row,foot);return shell;
}

function simpleDemo(product,motion=false) {
  const shell=h("div",`simple-demo${motion?" is-demo":" is-complete"}`);
  const head=h("header");head.append(wings(),h("span","",product.publicName),h("small","",motion?"ONE SHORT PASS":"COMPLETE STATE"));
  const flow=h("div","demo-simple-flow");
  const input=h("section","demo-input");input.append(h("span","","INPUT"),h("strong","","Launch brief attached"),h("p","","Audience, offer and constraints."));
  const route=h("div","demo-simple-route");route.append(h("i"),h("span","","PROCESS"));
  const output=h("section","demo-output");output.append(h("span","","RESULT"),h("strong","","Operating plan ready"),h("p","","Source context retained."),h("b","","Verified"));
  flow.append(input,route,output);shell.append(head,flow);return shell;
}

function sectionEntry(product,motion=false) {
  const shell=h("div",`entry-frame${motion?" is-entry":""}`);
  const copy=h("div","entry-copy");copy.append(wings(),h("span","","OPERATING SYSTEM"),h("h4","","Start with context."),h("p","","Give the system the information it needs before asking it to act."),h("b","","Explore Context Engine"));
  const tiles=h("div","entry-tiles");["Context","System","Proof"].forEach((label,index)=>{const tile=h("div","entry-tile");tile.style.setProperty("--step",index);tile.append(h("span","",String(index+1).padStart(2,"0")),h("strong","",label));tiles.append(tile);});
  shell.append(copy,tiles);return shell;
}

function accordionTabs(product,interactive=false) {
  if(!interactive){
    const shell=h("div","content-static");shell.append(h("span","content-kicker","ALL CONTENT / STATIC"));
    [["What it knows","Business context, decisions and constraints."],["What it does","Frames the work and runs the operating sequence."],["What it keeps","Source, outcome and proof remain connected."]].forEach(([title,copy])=>{const row=h("section");row.append(h("strong","",title),h("p","",copy));shell.append(row);});return shell;
  }
  const shell=h("div","tabs-demo");const tabs=h("div","tab-list");
  [["context","Context"],["operate","Operate"],["proof","Proof"]].forEach(([id,label],index)=>{const button=h("button",index===0?"is-selected":"",label);button.type="button";button.dataset.tab=id;button.setAttribute("aria-pressed",String(index===0));tabs.append(button);});
  const panel=h("div","tab-panel");panel.dataset.tabPanel="";panel.append(h("span","","CONTEXT"),h("h4","","Give the system a complete starting point."),h("p","","Business knowledge, active constraints and the reason behind the work stay attached."));
  const accordion=h("div","accordion");const button=h("button","accordion-button");button.type="button";button.dataset.accordionToggle="";button.setAttribute("aria-expanded","false");button.append(h("span","","See what is retained"),h("i","","+"));const body=h("div","accordion-body");body.append(h("p","","Source context, the operating run and the proof record remain connected after completion."));accordion.append(button,body);shell.append(tabs,panel,accordion);return shell;
}

function miniProduct(product) {
  const card=h("article","mini-product");const field=material(product,"mini-field");field.append(wings());const copy=h("div");copy.append(h("strong","",product.publicName),h("span","",product.function));card.append(field,copy);return card;
}

function carouselDemo(products,interactive=false) {
  if(!interactive){const grid=h("div","carousel-static");products.slice(0,3).forEach(product=>grid.append(miniProduct(product)));return grid;}
  const shell=h("div","carousel-demo");const top=h("header");top.append(h("span","","PRODUCT FAMILY"),h("strong","carousel-count","01 / 05"));
  const viewport=h("div","carousel-viewport");const track=h("div","carousel-track");track.dataset.carouselTrack="";products.slice(0,5).forEach(product=>track.append(miniProduct(product)));viewport.append(track);
  const controls=h("footer");const previous=h("button","","←");previous.type="button";previous.dataset.carouselPrevious="";previous.setAttribute("aria-label","Previous product");const next=h("button","","→");next.type="button";next.dataset.carouselNext="";next.setAttribute("aria-label","Next product");controls.append(h("span","","Moves only when you ask."),previous,next);shell.append(top,viewport,controls);shell.dataset.carouselIndex="0";return shell;
}

function processorDemo(product,interactive=false) {
  const shell=h("div",`processor-demo${interactive?"":" is-complete"}`);const head=h("header");head.append(h("span","","OPERATING RUN"),h("small","",product.publicName));
  const rows=h("div","processor-rows");["Context attached","System checked","Proof retained"].forEach((label,index)=>{const row=h("div","processor-row");row.style.setProperty("--step",index);row.append(h("i","",interactive?String(index+1).padStart(2,"0"):"✓"),h("span","",label),h("b","",interactive?"Waiting":"Complete"));rows.append(row);});
  const progress=h("div","processor-progress");progress.append(h("i"));
  const foot=h("footer");foot.append(h("span","processor-status",interactive?"Ready to run":"Verified"));const button=h("button","",interactive?"Run check":"Complete");button.type="button";button.disabled=!interactive;if(interactive)button.dataset.processorRun="";foot.append(button);shell.append(head,rows,progress,foot);return shell;
}

function visualFor(spec,products,motion) {
  const product=products[spec.product%products.length];
  if(spec.pattern==="focal-material")return focalCard(product,motion);
  if(spec.pattern==="functional-ui")return functionalPanel(product,motion);
  if(spec.pattern==="simple-demonstration")return simpleDemo(product,motion);
  if(spec.pattern==="section-entry")return sectionEntry(product,motion);
  if(spec.pattern==="accordion-tabs")return accordionTabs(product,motion);
  if(spec.pattern==="product-carousel")return carouselDemo(products,motion);
  return processorDemo(product,motion);
}

function verdicts(id) {
  const controls=h("div","specimen-verdicts");
  [["keep","Keep"],["revise","Revise"],["kill","Kill"]].forEach(([verdict,label])=>{const button=h("button","",label);button.type="button";button.dataset.verdict=verdict;button.disabled=true;button.setAttribute("aria-label",`${label} ${id}`);controls.append(button);});return controls;
}

function reviewable(spec,products) {
  const article=h("article",`specimen specimen--${spec.family}`);article.id=spec.id.toLowerCase();article.dataset.specimenId=spec.id;article.dataset.specimenTitle=spec.title;article.dataset.specimenFamily=spec.family;
  const head=h("header","specimen-head");const identity=h("div","specimen-identity");identity.append(h("span","specimen-id",spec.id),h("h3","",spec.title),h("p","",spec.note));head.append(identity,verdicts(spec.id));
  const comparison=h("div","specimen-comparison");[[spec.staticLabel,false],[spec.motionLabel,true]].forEach(([label,motion])=>{const pane=h("div",`specimen-pane${motion?" is-motion":""}`);pane.append(h("span","state-label",label));const surface=h("div","motion-surface");if(spec.auto&&motion){surface.dataset.motionEligible="";surface.dataset.motionKind=spec.auto;surface.dataset.specimenId=spec.id;}surface.append(visualFor(spec,products,motion));pane.append(surface);comparison.append(pane);});
  const feedback=h("label","specimen-feedback");feedback.append(h("span","",`Approval for ${spec.id}`));const textarea=h("textarea");textarea.rows=2;textarea.dataset.specimenNote=spec.id;textarea.value="Kept in the Round 03 approval.";textarea.disabled=true;feedback.append(textarea);article.append(head,comparison,feedback);return article;
}

function render(products) { specs.forEach(spec=>document.querySelector(`[data-mount="${spec.family}"]`).append(reviewable(spec,products))); }

function updateSummary() {
  const summary=document.querySelector("[data-review-summary]");summary.innerHTML="";
  ["keep","revise","kill"].forEach(verdict=>{const item=h("div");item.append(h("strong","",String(Object.values(state.decisions).filter(value=>value===verdict).length)),h("span","",verdict));summary.append(item);});
  const notes=[...Object.values(state.specimenNotes),...Object.values(state.familyNotes),state.note].filter(value=>value?.trim()).length;const item=h("div");item.append(h("strong","",String(notes)),h("span","","notes"));summary.append(item);
}

function updateReview() {
  document.querySelectorAll("[data-verdict]").forEach(button=>{const id=button.closest("[data-specimen-id]").dataset.specimenId;button.setAttribute("aria-pressed",String(state.decisions[id]===button.dataset.verdict));});
  document.querySelectorAll("[data-specimen-id]").forEach(node=>node.dataset.selectedVerdict=state.decisions[node.dataset.specimenId]||"");updateSummary();
}

function exportPayload() {
  return {schemaVersion:"1.0.0",gateId:"H-EXP-07-CHANNEL-MOTION-PROOF",taskId:"TASK-EXP-07-CHANNEL-MOTION",candidateRevision:"channel-motion-matrix-01-r03",verdict:"approve-with-deferral",specimens:specs.map(spec=>({id:spec.id,title:spec.title,family:spec.family,verdict:"keep",feedback:""})),deferred:{specimenId:"MOT-W02",taskId:"TASK-CMP-01-GLOBAL-NAVIGATION"},decisionId:"DEC-WEBSITE-MOTION-SYSTEM-001",resultingStatus:"canonical",productionAuthority:true};
}

function bindReview() {
  const panel=document.querySelector("#review-panel");const trigger=document.querySelector("[data-review-open]");
  const toggle=open=>{document.body.classList.toggle("is-reviewing",open);panel.setAttribute("aria-hidden",String(!open));trigger.setAttribute("aria-expanded",String(open));if(open)document.querySelector("[data-review-close]").focus();};
  document.addEventListener("click",event=>{if(event.target.closest("[data-review-open]"))toggle(true);if(event.target.closest("[data-review-close]"))toggle(false);});
  document.querySelector("[data-export]").addEventListener("click",async event=>{const output=JSON.stringify(exportPayload(),null,2);document.querySelector("[data-review-output]").textContent=output;try{await navigator.clipboard.writeText(output);event.target.textContent="Copied";}catch{event.target.textContent="Feedback ready below";}});
  addEventListener("keydown",event=>{if(event.key==="Escape")toggle(false);});updateReview();
}

function setMotionMode(text) { document.querySelectorAll("[data-motion-mode]").forEach(node=>node.textContent=`Motion allocation: ${text}`); }

function demoteMotion() {
  if(!activeMotion)return;activeMotion.classList.remove("is-active");const host=activeMotion.querySelector("[data-core-host]");if(host){renderer?.surfaces?.delete(host);host.querySelector("canvas[data-mz-core-canvas]")?.remove();host.removeAttribute("data-mz-core");host.classList.remove("is-live");}activeMotion=null;
}

function promoteMotion(target) {
  if(forceStatic||target===activeMotion)return;demoteMotion();activeMotion=target;target.classList.add("is-active");const id=target.dataset.specimenId;
  if(target.dataset.motionKind==="core"){
    const host=target.querySelector("[data-core-host]");if(!disableWebGL&&renderer&&host){const coreId=host.dataset.gradientId;const rect=host.getBoundingClientRect();const radius=Math.min(.3,24/(Math.min(rect.width,rect.height)/2||1));try{renderer.mount(host,coreId,{shape:"rect",radius,profile:"deep"});host.dataset.mzCore=coreId;host.classList.add("is-live");setMotionMode(`one live product material · ${id}`);return;}catch(error){document.documentElement.dataset.coreError=error?.message||"unknown";}}
    setMotionMode(`exact static twin · ${id} runtime unavailable`);return;
  }
  setMotionMode(`one restrained component event · ${id}`);
}

function chooseMotion() { const best=[...visibility.entries()].filter(([,ratio])=>ratio>.12).sort((a,b)=>b[1]-a[1])[0];if(best)promoteMotion(best[0]); }

function interruptAuto(label) { if(forceStatic)return;demoteMotion();clearTimeout(resumeTimer);setMotionMode(`user response · ${label}`);resumeTimer=setTimeout(chooseMotion,900); }

function bindMotion() {
  if(forceStatic){setMotionMode(reduced?"complete static states · reduced motion":"complete static states · forced");return;}
  observer=new IntersectionObserver(entries=>{entries.forEach(entry=>visibility.set(entry.target,entry.isIntersecting?entry.intersectionRatio:0));chooseMotion();},{rootMargin:"-14% 0px -14% 0px",threshold:[0,.12,.25,.4,.6,.8]});document.querySelectorAll("[data-motion-eligible]").forEach(target=>observer.observe(target));
}

function bindComponents() {
  document.addEventListener("click",event=>{
    const toggle=event.target.closest("[data-functional-toggle]");if(toggle){const pressed=toggle.getAttribute("aria-pressed")!=="true";toggle.setAttribute("aria-pressed",String(pressed));toggle.closest(".functional-panel").querySelector(".functional-status").textContent="Unsaved";interruptAuto("setting changed");}
    const save=event.target.closest("[data-functional-save]");if(save){const panel=save.closest(".functional-panel");panel.classList.remove("is-saved");void panel.offsetWidth;panel.classList.add("is-saved");panel.querySelector(".functional-status").textContent="Saved";interruptAuto("change confirmed");}
    const tab=event.target.closest("[data-tab]");if(tab){const demo=tab.closest(".tabs-demo");demo.querySelectorAll("[data-tab]").forEach(button=>{const selected=button===tab;button.classList.toggle("is-selected",selected);button.setAttribute("aria-pressed",String(selected));});const content={context:["CONTEXT","Give the system a complete starting point.","Business knowledge, active constraints and the reason behind the work stay attached."],operate:["OPERATE","Run one clear operating sequence.","Each action follows the context and records what changed."],proof:["PROOF","Keep the result connected to its source.","The outcome remains inspectable after the run is complete."]}[tab.dataset.tab];const panel=demo.querySelector("[data-tab-panel]");panel.classList.remove("is-changing");void panel.offsetWidth;panel.classList.add("is-changing");panel.children[0].textContent=content[0];panel.children[1].textContent=content[1];panel.children[2].textContent=content[2];interruptAuto("tab selection");}
    const accordion=event.target.closest("[data-accordion-toggle]");if(accordion){const root=accordion.closest(".accordion");const open=root.classList.toggle("is-open");accordion.setAttribute("aria-expanded",String(open));accordion.querySelector("i").textContent=open?"−":"+";interruptAuto("accordion disclosure");}
    const next=event.target.closest("[data-carousel-next]");const previous=event.target.closest("[data-carousel-previous]");if(next||previous){const demo=(next||previous).closest(".carousel-demo");let index=Number(demo.dataset.carouselIndex);index=Math.max(0,Math.min(4,index+(next?1:-1)));demo.dataset.carouselIndex=String(index);demo.querySelector("[data-carousel-track]").style.setProperty("--carousel-index",index);demo.querySelector(".carousel-count").textContent=`${String(index+1).padStart(2,"0")} / 05`;demo.querySelector("[data-carousel-previous]").disabled=index===0;demo.querySelector("[data-carousel-next]").disabled=index===4;interruptAuto("product carousel");}
    const run=event.target.closest("[data-processor-run]");if(run){const demo=run.closest(".processor-demo");demo.classList.remove("is-finished");demo.classList.remove("is-running");void demo.offsetWidth;demo.classList.add("is-running");run.disabled=true;demo.querySelector(".processor-status").textContent="Running";demo.querySelectorAll(".processor-row b").forEach(item=>item.textContent="Waiting");interruptAuto("processor running");setTimeout(()=>{demo.classList.remove("is-running");demo.classList.add("is-finished");demo.querySelector(".processor-status").textContent="Verified";demo.querySelectorAll(".processor-row").forEach(row=>{row.querySelector("i").textContent="✓";row.querySelector("b").textContent="Complete";});run.disabled=false;run.textContent="Run again";},1700);}
  });
}

async function initialiseMotion() {
  if(forceStatic){bindMotion();return;}
  if(!disableWebGL){try{const catalogue=await fetchJson("../../../gradient-library/catalogue.json");const mounted=await mountLivingCores(document,{catalogue,staticBaseUrl:"../../gradient-library/assets/static/"});renderer=mounted.renderer;}catch(error){document.documentElement.dataset.coreInitError=error?.message||"unknown";}}
  setMotionMode("waiting for one eligible component");bindMotion();
}

async function main() {
  try {
    const registry=await fetchJson("../../../registry/products.json");const products=viewModel(registry.products);render(products);if(document.querySelectorAll("article.specimen[data-specimen-id]").length!==7)throw new Error("Expected 7 canonical specimens");bindReview();bindComponents();await initialiseMotion();const deepLink=document.getElementById(location.hash.slice(1));if(deepLink)requestAnimationFrame(()=>deepLink.scrollIntoView({block:"start"}));
  } catch(error) { console.error(error);document.body.prepend(h("p","render-failure",`Website Motion 1.0.0 failed: ${error.message}`)); }
}

main();
