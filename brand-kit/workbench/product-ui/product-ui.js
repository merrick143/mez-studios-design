const FIXTURE_URL="./fixtures/system-proof.json";
const stateMessages={
  loading:{tone:"info",title:"Loading repository records.",detail:"The ledger remains named while the source fixture is being resolved."},
  empty:{tone:"info",title:"No records match this view.",detail:"Clear the filter or return to the complete ledger."},
  error:{tone:"danger",title:"The fixture could not be read.",detail:"No cached value is presented as current. Reload the review fixture to try again."},
  stale:{tone:"warning",title:"This view may be stale.",detail:"Records remain readable, but reconcile the named source paths before making an authority decision."},
  partial:{tone:"warning",title:"Partial source coverage.",detail:"Available records are shown and missing coverage remains explicit."},
  "no-permission":{tone:"danger",title:"You do not have permission to inspect these records.",detail:"The workspace names the restriction without exposing record details."}
};

const els={
  body:document.body,ledger:document.querySelector(".ledger-region"),tbody:document.querySelector("[data-ledger-body]"),
  tableWrap:document.querySelector("[data-table-wrap]"),filter:document.querySelector("[data-filter]"),summary:document.querySelector("[data-result-summary]"),
  banner:document.querySelector("[data-state-banner]"),live:document.querySelector("[data-live-region]"),state:document.querySelector("[data-state]"),
  dialog:document.querySelector("[data-dialog]"),commandInput:document.querySelector("[data-command-input]"),commandResults:document.querySelector("[data-command-results]")
};
let fixture={records:[],distribution:[]},selectedId=null,activeView="ledger",sort={key:"updated",direction:"desc"},returnFocus=null;
const viewIncludes={ledger:()=>true,registry:record=>record.type==="Registry",components:record=>record.type==="Runtime component",release:record=>record.id==="foundations"};
const viewLabels={ledger:"Ledger",registry:"Registry",components:"Components",release:"Release"};

const words=value=>value.replaceAll("-"," ");
const announce=message=>{els.live.textContent=els.live.textContent===message?`${message}\u200b`:message;};
const orderedRecords=()=>{
  const query=els.filter.value.trim().toLowerCase();
  return fixture.records.filter(record=>viewIncludes[activeView](record)&&Object.values(record).join(" ").toLowerCase().includes(query)).sort((a,b)=>{
    const result=String(a[sort.key]).localeCompare(String(b[sort.key]));
    return sort.direction==="asc"?result:-result;
  });
};
const statusMarkup=status=>`<span class="status-label" data-status="${status}">${words(status)}</span>`;

function renderRows(){
  const records=orderedRecords();
  els.tbody.innerHTML=records.map((record,index)=>`<tr data-record="${record.id}">
    <td data-label="Record"><button type="button" class="record-button" data-select="${record.id}" aria-current="${record.id===selectedId}"><span class="record-marker" aria-hidden="true"></span>${record.name}</button></td>
    <td data-label="Type">${record.type}</td><td data-label="Status">${statusMarkup(record.status)}</td><td data-label="Updated">${record.updated}</td>
  </tr>`).join("");
  els.summary.textContent=`${records.length} of ${fixture.records.length} records`;
  document.querySelector("[data-record-count]").textContent=String(fixture.records.length).padStart(2,"0");
  els.tbody.querySelectorAll("[data-select]").forEach(button=>button.addEventListener("click",()=>selectRecord(button.dataset.select,true)));
  if(!records.length&&els.state.value==="ready")setReviewState("empty",false);
}

function selectRecord(id,focusInspector=false){
  const record=fixture.records.find(item=>item.id===id);if(!record)return;
  selectedId=id;renderRows();
  const index=fixture.records.indexOf(record)+1;
  document.querySelector("[data-inspector-index]").textContent=String(index).padStart(2,"0");
  document.querySelector("[data-inspector-name]").textContent=record.name;
  document.querySelector("[data-inspector-type]").textContent=record.type;
  document.querySelector("[data-inspector-detail]").textContent=record.detail;
  document.querySelector("[data-inspector-status]").textContent=words(record.status);
  document.querySelector("[data-inspector-source]").textContent=record.source;
  document.querySelector("[data-inspector-updated]").textContent=record.updated;
  announce(`${record.name} selected. Status ${words(record.status)}.`);
  if(focusInspector)document.querySelector("[data-inspector]").scrollIntoView({block:"nearest",behavior:matchMedia("(prefers-reduced-motion: reduce)").matches?"auto":"smooth"});
}

function renderDistribution(){
  const total=fixture.distribution.reduce((sum,item)=>sum+item.count,0);
  const bar=document.querySelector("[data-status-bar]"),legend=document.querySelector("[data-status-legend]"),alternative=document.querySelector("[data-status-alternative]");
  bar.innerHTML=fixture.distribution.map(item=>`<span class="status-segment" data-status="${item.status}" style="flex:${item.count}" aria-hidden="true">${item.count}</span>`).join("");
  bar.setAttribute("aria-label",fixture.distribution.map(item=>`${item.label}: ${item.count}`).join("; "));
  legend.innerHTML=fixture.distribution.map(item=>`<span class="legend-item" data-status="${item.status}"><i aria-hidden="true"></i>${item.label} · ${item.count}</span>`).join("");
  alternative.innerHTML=fixture.distribution.map(item=>`<li>${item.label}: ${item.count} of ${total} records.</li>`).join("");
  document.querySelector("[data-status-caption]").textContent=`Distribution across ${total} fixture records. Exact values are repeated in text.`;
}

function setReviewState(state,updateSelect=true){
  if(updateSelect)els.state.value=state;
  const message=stateMessages[state];
  els.banner.hidden=state==="ready";
  els.ledger.dataset.loading=String(state==="loading");
  els.tableWrap.hidden=["error","no-permission"].includes(state);
  if(message){els.banner.dataset.tone=message.tone;els.banner.innerHTML=`<strong>${message.title}</strong> ${message.detail}`;announce(`${message.title} ${message.detail}`);}
  else{els.banner.textContent="";announce("Ready state. Complete ledger restored.");}
  if(state==="empty")els.tbody.innerHTML="";
  else renderRows();
}

function setDensity(value){
  els.body.dataset.density=value;
  document.querySelectorAll("[data-density-value]").forEach(button=>{const active=button.dataset.densityValue===value;button.classList.toggle("is-active",active);button.setAttribute("aria-pressed",String(active));});
  announce(`${value} density selected. All records and controls remain available.`);
}

function renderCommandResults(query=""){
  const value=query.toLowerCase();const records=fixture.records.filter(record=>Object.values(record).join(" ").toLowerCase().includes(value));
  els.commandResults.innerHTML=records.length?records.map(record=>`<button type="button" class="command-result" data-command-record="${record.id}"><strong>${record.name}</strong><span>${words(record.status)}</span></button>`).join(""):`<p>No records found.</p>`;
  els.commandResults.querySelectorAll("[data-command-record]").forEach(button=>button.addEventListener("click",()=>{closeDialog();selectRecord(button.dataset.commandRecord,true);}));
}
function setBackgroundBlocked(blocked){
  for(const element of [document.querySelector(".topbar"),document.querySelector(".app-shell")]){
    if(blocked){element.setAttribute("inert","");element.setAttribute("aria-hidden","true");}
    else{element.removeAttribute("inert");element.removeAttribute("aria-hidden");}
  }
}
function openDialog(){returnFocus=document.activeElement;els.dialog.hidden=false;setBackgroundBlocked(true);renderCommandResults();requestAnimationFrame(()=>els.commandInput.focus());}
function closeDialog(){els.dialog.hidden=true;setBackgroundBlocked(false);els.commandInput.value="";returnFocus?.focus();}

document.querySelectorAll("[data-density-value]").forEach(button=>button.addEventListener("click",()=>setDensity(button.dataset.densityValue)));
els.filter.addEventListener("input",()=>{if(els.state.value!=="ready")setReviewState("ready");else renderRows();const count=orderedRecords().length;announce(`${count} ${count===1?"record matches":"records match"} the filter.`);});
els.state.addEventListener("change",()=>setReviewState(els.state.value));
document.querySelectorAll("[data-sort]").forEach(button=>button.addEventListener("click",()=>{
  const key=button.dataset.sort;sort.direction=sort.key===key&&sort.direction==="asc"?"desc":"asc";sort.key=key;
  document.querySelectorAll("th[aria-sort]").forEach(th=>th.removeAttribute("aria-sort"));button.closest("th").setAttribute("aria-sort",sort.direction==="asc"?"ascending":"descending");renderRows();announce(`Sorted by ${key}, ${sort.direction==="asc"?"ascending":"descending"}.`);
}));
document.querySelector("[data-command]").addEventListener("click",openDialog);
document.querySelectorAll("[data-dialog-close]").forEach(button=>button.addEventListener("click",closeDialog));
els.commandInput.addEventListener("input",()=>renderCommandResults(els.commandInput.value));
document.addEventListener("keydown",event=>{
  if((event.metaKey||event.ctrlKey)&&event.key.toLowerCase()==="k"){event.preventDefault();openDialog();return;}
  if(event.key==="Escape"&&!els.dialog.hidden){closeDialog();return;}
  if(event.key==="Tab"&&!els.dialog.hidden){
    const focusable=[...els.dialog.querySelectorAll('button:not([tabindex="-1"]),input')].filter(item=>!item.hidden&&!item.disabled);
    const first=focusable[0],last=focusable[focusable.length-1];
    if(event.shiftKey&&document.activeElement===first){event.preventDefault();last.focus();}
    else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first.focus();}
  }
});

const navButtons=[...document.querySelectorAll("[data-roving-nav] button")];
navButtons.forEach((button,index)=>button.addEventListener("keydown",event=>{
  const keys={ArrowDown:1,ArrowRight:1,ArrowUp:-1,ArrowLeft:-1};let next;
  if(event.key==="Home")next=0;else if(event.key==="End")next=navButtons.length-1;else if(keys[event.key])next=(index+keys[event.key]+navButtons.length)%navButtons.length;else return;
  event.preventDefault();navButtons.forEach(item=>item.tabIndex=-1);navButtons[next].tabIndex=0;navButtons[next].focus();
}));
navButtons.forEach(button=>button.addEventListener("click",()=>{
  navButtons.forEach(item=>{item.classList.remove("is-current");item.removeAttribute("aria-current");});button.classList.add("is-current");button.setAttribute("aria-current","page");
  activeView=button.dataset.view;els.filter.value="";setReviewState("ready");const records=orderedRecords();if(records.length)selectRecord(records[0].id);announce(`${viewLabels[activeView]} view selected. ${records.length} ${records.length===1?"record":"records"} shown.`);
}));

try{
  const response=await fetch(FIXTURE_URL);if(!response.ok)throw new Error(`HTTP ${response.status}`);fixture=await response.json();
  document.querySelector("[data-fixture-name]").textContent=fixture.scopeLabel;renderRows();renderDistribution();selectRecord(fixture.records[0].id);setReviewState("ready");
  document.documentElement.dataset.uiReady="true";
}catch(error){console.error(error);setReviewState("error");document.querySelector("[data-fixture-name]").textContent="Fixture unavailable";}
