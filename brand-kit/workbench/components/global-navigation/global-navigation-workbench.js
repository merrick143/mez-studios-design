import "../../../components/global-navigation/mez-global-navigation.js?v=1.0.0";

const component=document.querySelector("mez-global-navigation"),query=new URLSearchParams(location.search),eventLog=document.querySelector("[data-event-log]"),canvasReadout=document.querySelector("[data-canvas-count]");
const waitForReady=()=>new Promise(resolve=>{if(component.dataset.ready==="true")resolve();else new MutationObserver((_,observer)=>{if(component.dataset.ready==="true"){observer.disconnect();resolve();}}).observe(component,{attributes:true,attributeFilter:["data-ready"]});});
const updateCanvasCount=()=>{const count=component.querySelectorAll("canvas[data-mz-core-canvas]").length;canvasReadout.textContent=`${count} / 5 live canvases`;canvasReadout.dataset.pass=String(count===5||count===0);};
const writeEvent=event=>{eventLog.textContent=JSON.stringify({event:event.type,detail:event.detail,observedAt:new Date().toISOString()},null,2);setTimeout(updateCanvasCount,500);};
["mez-navigation-open","mez-product-focus","mez-product-navigate"].forEach(type=>component.addEventListener(type,writeEvent));

document.querySelector("[data-open-menu]").addEventListener("click",()=>component.setExpanded(true));
document.querySelector("[data-surface]").addEventListener("change",event=>{if(event.target.value==="light")component.setAttribute("surface","light");else component.removeAttribute("surface");});
document.querySelector("[data-product]").addEventListener("change",async event=>{await waitForReady();const index=component.products.findIndex(product=>product.slug===event.target.value);if(index>=0)component.select(index,false);});

await waitForReady();
if(query.has("open"))await component.setExpanded(true);
updateCanvasCount();
