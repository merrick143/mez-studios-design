const STUDIES = [
  {
    id: 'layered-clarity', number: '01', name: 'Layered clarity',
    thesis: 'The owned operating layer remains visually persistent while models, tools and products rotate around it.',
    specs: [['TYPE', 'Inter, 700 / 450'], ['BUTTON', '12px'], ['CARD', '18px'], ['RHYTHM', '96px'], ['SURFACE', 'Cold white'], ['RECOGNITION', 'Owned-layer spine']]
  },
  {
    id: 'kinetic-shelf', number: '02', name: 'Kinetic shelf',
    thesis: 'The product shelf creates energy through scale, crop and responsive movement while the page remains restrained.',
    specs: [['TYPE', 'Avenir Next, 650 / 450'], ['BUTTON', '14px'], ['CARD', '24px'], ['RHYTHM', '120px'], ['SURFACE', 'Soft grey'], ['RECOGNITION', 'Moving product shelf']]
  },
  {
    id: 'system-ledger', number: '03', name: 'System ledger',
    thesis: 'Mez becomes recognisable through durable layers, exact labels and a repeated ledger of what changes and what compounds.',
    specs: [['TYPE', 'Helvetica Neue, 600 / 400'], ['BUTTON', '10px'], ['CARD', '14px'], ['RHYTHM', '80px'], ['SURFACE', 'Ink and white'], ['RECOGNITION', 'Compound ledger']]
  },
  {
    id: 'soft-infrastructure', number: '04', name: 'Soft infrastructure',
    thesis: 'Complex systems feel approachable through generous space, tactile nested surfaces and product packaging that invites inspection.',
    specs: [['TYPE', 'Inter, 650 / 400'], ['BUTTON', '12px'], ['CARD', '28px'], ['RHYTHM', '112px'], ['SURFACE', 'Warm stone'], ['RECOGNITION', 'Nested infrastructure']]
  }
];

const PRODUCTS = [
  {name:'Context Engine', job:'Find where AI actually belongs in your business.', flow:'Understand → Map → Rank → Run', gradient:'g20'},
  {name:'AI Ads System', job:'Turn every campaign into a compounding intelligence loop.', flow:'Research → Create → Test → Learn', gradient:'g06'},
  {name:'Claude Code OS', job:'Turn Claude Code into a business-aware execution environment.', flow:'Context → Skills → Execute → Approve', gradient:'g15'},
  {name:'Organic Content OS', job:'Turn scattered ideas into a compounding content system.', flow:'Signals → Ideas → Publish → Learn', gradient:'g13'}
];

const MODULES = {
  hero:'Hero and system visual', problem:'Enemy and market problem', ethos:'Ethos and owned layer',
  proof:'Built-on-ourselves proof', aios:'AI OS feature', shelf:'Product shelf', commerce:'Purchase and bundles', final:'Final route'
};
const REACTIONS = ['keep', 'change', 'too much', 'too plain', 'not Mez'];
const OVERALL = ['promising', 'useful details', 'not Mez'];
const state = JSON.parse(localStorage.getItem('mezHomepageStudioReview') || '{}');
const requestedStudy = new URLSearchParams(window.location.search).get('study');
let activeStudy = STUDIES.some(study => study.id === requestedStudy) ? requestedStudy : STUDIES[0].id;
let pendingModule = null;

const $ = (selector, root=document) => root.querySelector(selector);
const $$ = (selector, root=document) => [...root.querySelectorAll(selector)];
const mark = '<img class="mez-mark" src="../../../design-system-export/assets/wings.svg" alt="" aria-hidden="true">';
const feedbackButton = module => `<button class="annotate" type="button" data-annotate="${module}" aria-label="Give feedback on ${MODULES[module]}">Feedback</button>`;

function productCards(studyId){
  return PRODUCTS.map((p, i) => `<article class="product-card product-${i+1}">
    <div class="product-swatch ${p.gradient}"><span>COMING SOON</span></div>
    <div class="product-card-copy"><small>0${i+2} · OPERATING SYSTEM</small><h3>${p.name}</h3><p>${p.job}</p><b>${p.flow}</b><a href="#${studyId}-commerce">View system <span>↗</span></a></div>
  </article>`).join('');
}

function renderStudy(study){
  return `<article class="study study-${study.id}" data-study="${study.id}">
    <div class="study-meta"><div><span>FOUNDATION STUDY ${study.number}</span><h1>${study.name}</h1><p>${study.thesis}</p></div><dl>${study.specs.map(([a,b])=>`<div><dt>${a}</dt><dd>${b}</dd></div>`).join('')}</dl></div>
    <div class="site-shell">
      <nav class="site-nav"><a class="brand-lockup" href="#">${mark}<b>Mez Systems</b></a><div class="nav-links"><a href="#${study.id}-ethos">Why Mez</a><a href="#${study.id}-shelf">Systems</a><a href="#${study.id}-proof">Proof</a></div><a class="button button-dark nav-cta" href="#${study.id}-aios">Explore the AI OS</a><button class="menu-button" aria-label="Open menu"><i></i><i></i></button></nav>

      <section class="hero module" id="${study.id}-hero" data-module="hero">${feedbackButton('hero')}
        <div class="hero-copy"><p class="eyebrow">MEZ SYSTEMS · BUILT BY MEZ STUDIOS</p><h2>The systems <span>AI-native businesses</span> run on.</h2><p class="lede">Use the best models and harnesses at the source. Own the context, workflows and operating infrastructure that make them useful.</p><div class="actions"><a class="button button-dark" href="#${study.id}-aios">Explore the AI OS</a><a class="button button-light" href="#${study.id}-shelf">See what we're building</a></div></div>
        <div class="system-visual" aria-label="Interchangeable intelligence connected to an owned Mez operating layer">
          <div class="tool-row"><span>Claude Code</span><span>ChatGPT</span><span>Codex</span><span>Future model</span></div>
          <div class="connector connector-top"><i></i><i></i><i></i><i></i></div>
          <div class="owned-layer"><header><span>${mark}<b>YOUR OPERATING LAYER</b></span><small>OWNED</small></header><div class="layer-grid"><span>Context</span><span>Workflows</span><span>Decisions</span><span>History</span></div><div class="installed-system"><span class="gradient-chip g13"></span><div><small>INSTALLED SYSTEM 01</small><b>AI OS</b></div><em>AVAILABLE NOW</em></div></div>
          <div class="connector connector-bottom"><i></i><i></i><i></i><i></i></div>
          <div class="output-row"><span>Daily direction</span><span>Business context</span><span>Execution history</span></div>
        </div>
      </section>

      <section class="problem module" id="${study.id}-problem" data-module="problem">${feedbackButton('problem')}<div class="section-intro"><p class="eyebrow">THE AI STACK IS UPSIDE DOWN</p><h2>Too many tools.<br>Too many middlemen.</h2></div><div class="problem-list"><article><b>01</b><h3>Another interface</h3><p>The same frontier intelligence behind another login and another layer to maintain.</p></article><article><b>02</b><h3>More cost. Less control.</h3><p>Subscriptions, credits, margins and restrictions compound between you and the model.</p></article><article><b>03</b><h3>Built around yesterday</h3><p>A better model arrives and the workflow still depends on an interface that cannot move with it.</p></article></div></section>

      <section class="ethos module" id="${study.id}-ethos" data-module="ethos">${feedbackButton('ethos')}<p class="eyebrow">THE MEZ SYSTEMS PRINCIPLE</p><div class="ethos-statement"><h2>The intelligence is rented.</h2><h2>The operating layer is <span>yours.</span></h2></div><div class="ethos-flow"><div class="change-layer"><small>CHANGE WHEN SOMETHING BETTER ARRIVES</small><div><span>Claude Code</span><span>ChatGPT</span><span>Codex</span><span>Next</span></div></div><div class="keep-layer"><small>KEEP THE ENDURING BUSINESS LAYER</small><div><span>Context</span><span>Workflows</span><span>Documentation</span><span>Decisions</span><span>Permissions</span><span>History</span></div></div></div><p class="signature">Build the system. Rent the model.</p></section>

      <section class="proof module" id="${study.id}-proof" data-module="proof">${feedbackButton('proof')}<div class="section-intro"><p class="eyebrow">BUILT ON OURSELVES FIRST</p><h2>We run Mez Studios on the systems we sell.</h2><p>Every Mez System begins with a real operating problem. We build it, run it, find what breaks, refine it and only then package it for another operator.</p></div><div class="proof-frames"><article><header><span>01 · COMMAND SURFACE</span><em>REDACTED</em></header><div class="redacted-screen screen-a"><i></i><i></i><i></i><i></i><i></i></div><p>Live business context becomes the next clear action.</p></article><article><header><span>02 · CONTEXT LAYER</span><em>REDACTED</em></header><div class="redacted-screen screen-b"><i></i><i></i><i></i><i></i></div><p>AI starts with the business, not a blank chat.</p></article><article><header><span>03 · DECISION TRAIL</span><em>REDACTED</em></header><div class="redacted-screen screen-c"><i></i><i></i><i></i><i></i></div><p>The system keeps the reasoning, not only the result.</p></article></div><b class="proof-close">Built inside the business. Proven by the business. Packaged for yours.</b></section>

      <section class="aios module" id="${study.id}-aios" data-module="aios">${feedbackButton('aios')}<div class="aios-media"><div class="gradient-field g13"><span>${mark}</span><small>MZ-G13 · AI OS</small></div><div class="asset-tabs"><span>Daily direction</span><span>Connected context</span><span>Decision history</span></div></div><div class="aios-copy"><p class="eyebrow">AVAILABLE NOW</p><h2>Start with the AI OS.</h2><p>The AI OS connects tasks, projects, clients, goals, decisions, documentation and planning in one structured Notion system.</p><ul><li>Start with the right work</li><li>Ask questions with context</li><li>Keep decisions connected</li><li>Run one operating rhythm</li></ul><a class="button button-dark" href="#${study.id}-commerce">Explore the AI OS</a><small>Available today for founders and operators building AI-native businesses.</small></div></section>

      <section class="shelf module" id="${study.id}-shelf" data-module="shelf">${feedbackButton('shelf')}<div class="section-intro"><p class="eyebrow">COMING NEXT</p><h2>The operating systems we're building next.</h2><p>Specialised systems for specific operating problems. Different jobs, one enduring principle.</p></div><div class="product-shelf">${productCards(study.id)}</div><div class="shelf-rule"><span>Different systems.</span><b>Same rule.</b><span>Own the layer around the intelligence.</span></div></section>

      <section class="commerce module" id="${study.id}-commerce" data-module="commerce">${feedbackButton('commerce')}<div class="section-intro"><p class="eyebrow">BUILD YOUR OPERATING LAYER</p><h2>Start with one system.<br>Add the others as you grow.</h2></div><div class="commerce-grid"><article class="purchase-card"><header><div class="purchase-icon g13">${mark}</div><span><small>AVAILABLE NOW</small><b>AI OS</b></span></header><p>One structured operating layer for your tasks, projects, goals, decisions and business context.</p><ul><li>Complete Notion operating system</li><li>Installation and setup guide</li><li>Future system updates</li></ul><div class="price-row"><span><b>$99</b><small>USD · ONE TIME</small></span><a class="button button-dark" href="#">Get the AI OS</a></div></article><article class="bundle-card"><header><small>FUTURE BUNDLE</small><span>04 SYSTEMS</span></header><h3>The operating layer bundle.</h3><p>AI OS plus specialised systems for context, Claude Code and content. Each system stays useful on its own and compounds when connected.</p><div class="bundle-stack"><i class="g13"></i><i class="g20"></i><i class="g06"></i><i class="g15"></i></div><button class="button button-light" type="button">Join the bundle waitlist</button></article></div></section>

      <section class="final module" id="${study.id}-final" data-module="final">${feedbackButton('final')}<div><p class="eyebrow">START HERE</p><h2>Build the system your next AI tool can use.</h2><p>The models will keep improving. Your business should not need to start over with each one.</p><div class="actions"><a class="button button-dark" href="#${study.id}-aios">Explore the AI OS</a><a class="button button-light" href="#${study.id}-shelf">See what we're building</a></div></div><div class="final-visual"><div class="final-core g13">${mark}</div><span>AI OS</span><small>THE FIRST INSTALLED MEZ SYSTEM</small></div></section>
      <footer class="site-footer"><a class="brand-lockup" href="#">${mark}<b>Mez Systems</b></a><div><a href="#${study.id}-aios">AI OS</a><a href="#${study.id}-shelf">What we're building</a><a href="#${study.id}-proof">Mez Studios</a><a href="#">Contact</a></div><small>Mez Systems. Built by Mez Studios.</small></footer>
    </div>
    <section class="study-review"><p>STUDY ${study.number} · HUMAN SIGNAL</p><h2>Does this make Mez feel known?</h2><div class="choice-row" data-inline-overall></div><button class="open-review" type="button">Add specific feedback</button></section>
  </article>`;
}

function ensureStudyState(id){
  state[id] ||= {overall:'', note:'', annotations:{}};
  return state[id];
}
function saveState(){ localStorage.setItem('mezHomepageStudioReview', JSON.stringify(state)); updateFeedbackCount(); }
function renderTabs(){
  $('#study-tabs').innerHTML = STUDIES.map(s=>`<button type="button" data-tab="${s.id}" aria-pressed="${s.id===activeStudy}"><span>${s.number}</span>${s.name}</button>`).join('');
}
function showStudy(id){
  activeStudy=id; ensureStudyState(id);
  $$('.study').forEach(el=>el.hidden=el.dataset.study!==id);
  $$('[data-tab]').forEach(el=>el.setAttribute('aria-pressed', el.dataset.tab===id));
  $('#review-study-name').textContent=STUDIES.find(s=>s.id===id).name;
  $('#study-note').value=state[id].note||'';
  renderOverall(); renderAnnotations();
  const url = new URL(window.location.href); url.searchParams.set('study', id); history.replaceState({}, '', url);
  window.scrollTo({top:0,behavior:'auto'});
}
function choiceButtons(values, selected, attr){ return values.map(v=>`<button type="button" ${attr}="${v}" aria-pressed="${selected===v}">${v}</button>`).join(''); }
function renderOverall(){
  const selected=ensureStudyState(activeStudy).overall;
  $$('[data-overall-choices], [data-inline-overall]', $(`[data-study="${activeStudy}"]`)||document).forEach(el=>el.innerHTML=choiceButtons(OVERALL,selected,'data-overall'));
  $('[data-overall-choices]').innerHTML=choiceButtons(OVERALL,selected,'data-overall');
}
function renderAnnotations(){
  const annotations=ensureStudyState(activeStudy).annotations;
  const items=Object.entries(annotations);
  $('#annotation-list').innerHTML=items.length ? items.map(([id,a])=>`<article><span><small>${MODULES[id]}</small><b>${a.reaction}</b></span><p>${a.note||'No note'}</p><button type="button" data-edit-annotation="${id}">Edit</button></article>`).join('') : '<p class="empty-state">No section feedback yet.</p>';
}
function openPanel(){ $('#review-panel').classList.add('open'); $('#review-panel').setAttribute('aria-hidden','false'); $('.review-toggle').setAttribute('aria-expanded','true'); }
function closePanel(){ $('#review-panel').classList.remove('open'); $('#review-panel').setAttribute('aria-hidden','true'); $('.review-toggle').setAttribute('aria-expanded','false'); }
function openAnnotation(module){
  pendingModule=module; const current=ensureStudyState(activeStudy).annotations[module]||{};
  $('#annotation-title').textContent=MODULES[module];
  $('#annotation-reactions').innerHTML=choiceButtons(REACTIONS,current.reaction||'','data-reaction');
  $('#annotation-note').value=current.note||''; $('#annotation-dialog').showModal();
}
function updateFeedbackCount(){
  const count=Object.values(state).reduce((n,s)=>n+(s.overall?1:0)+Object.keys(s.annotations||{}).length+(s.note?1:0),0);
  $('#feedback-count').textContent=count;
}
function exportRecord(){
  return {schemaVersion:'1.0.0',studyId:'MEZ-HOMEPAGE-FOUNDATION-STUDIO-01',exportedAt:new Date().toISOString(),productionAuthority:false,sourceExpressionApproved:false,contentSource:'Notion page 8bb570a0-f71a-4e42-9243-e9aa9e760733',records:STUDIES.map(s=>({studyId:s.id,studyName:s.name,...ensureStudyState(s.id),productionAuthority:false}))};
}

$('#study-root').innerHTML=STUDIES.map(renderStudy).join(''); renderTabs(); showStudy(activeStudy); updateFeedbackCount();
if(window.location.hash){setTimeout(()=>document.getElementById(window.location.hash.slice(1))?.scrollIntoView(),80);}
document.addEventListener('click', e=>{
  const tab=e.target.closest('[data-tab]'); if(tab) showStudy(tab.dataset.tab);
  const overall=e.target.closest('[data-overall]'); if(overall){ ensureStudyState(activeStudy).overall=overall.dataset.overall; saveState(); renderOverall(); }
  const annotate=e.target.closest('[data-annotate]'); if(annotate) openAnnotation(annotate.dataset.annotate);
  const edit=e.target.closest('[data-edit-annotation]'); if(edit) openAnnotation(edit.dataset.editAnnotation);
  if(e.target.closest('.review-toggle,.open-review')) openPanel();
  if(e.target.closest('.review-close')) closePanel();
  const reaction=e.target.closest('[data-reaction]'); if(reaction){ $$('[data-reaction]').forEach(b=>b.setAttribute('aria-pressed',b===reaction)); }
});
$('#study-note').addEventListener('input',e=>{ensureStudyState(activeStudy).note=e.target.value;saveState();});
$('#save-annotation').addEventListener('click',e=>{
  const selected=$('[data-reaction][aria-pressed="true"]');
  if(!selected){e.preventDefault();return;}
  ensureStudyState(activeStudy).annotations[pendingModule]={reaction:selected.dataset.reaction,note:$('#annotation-note').value.trim()}; saveState(); renderAnnotations();
});
$('#copy-review').addEventListener('click',async()=>{await navigator.clipboard.writeText(JSON.stringify(exportRecord(),null,2));$('#review-status').textContent='Review JSON copied.';});
$('#download-review').addEventListener('click',()=>{const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(exportRecord(),null,2)],{type:'application/json'}));a.download='mez-homepage-foundation-review.json';a.click();URL.revokeObjectURL(a.href);$('#review-status').textContent='Review JSON downloaded.';});
