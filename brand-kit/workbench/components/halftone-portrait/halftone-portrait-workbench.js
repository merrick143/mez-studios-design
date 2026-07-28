/* Workbench instrumentation for CMP-05.
 *
 * Measures the one-live-instance rule rather than restating it, because a
 * component that documents a motion budget and quietly breaks it passes every
 * JSON verifier ever written.
 */

const readout = document.getElementById("readout");
const labels = [...document.querySelectorAll("[data-motion-for]")];
const portraits = () => [...document.querySelectorAll("mez-halftone-portrait")];

let peakLive = 0;
let samples = 0;

function sample() {
  const all = portraits();
  const allocated = all.filter(node => node.getAttribute("motion-policy") !== "always");
  const always = all.filter(node => node.getAttribute("motion-policy") === "always");
  const live = all.filter(node => node.dataset.motion === "live");
  const liveAllocated = allocated.filter(node => node.dataset.motion === "live");
  const liveAlways = always.filter(node => node.dataset.motion === "live");
  const failed = all.filter(node => node.hasAttribute("data-failure"));
  // Only the allocated pool is budgeted. The always pool is the recorded
  // exception, and its own rule is that it idles off screen.
  peakLive = Math.max(peakLive, liveAllocated.length);
  samples += 1;

  for (const label of labels) {
    const target = document.getElementById(label.dataset.motionFor);
    label.textContent = target?.dataset.motion ?? "mounting";
  }

  const verdict = peakLive <= 1 ? "within budget" : "BUDGET BREACHED";
  readout.textContent = [
    `portraits ${all.length}`,
    `live ${live.length}`,
    `allocated pool ${liveAllocated.length}/${allocated.length} · peak ${peakLive} (${verdict})`,
    `always pool ${liveAlways.length}/${always.length} live`,
    `failed ${failed.length}`,
    `samples ${samples}`
  ].join("   ·   ");
  readout.dataset.state = peakLive <= 1 ? "ok" : "breach";
}

// Sample on a timer as well as on scroll: allocation changes on intersection,
// which does not always coincide with a scroll event.
addEventListener("scroll", sample, { passive: true });
setInterval(sample, 500);
document.addEventListener("mez-halftone-ready", sample);
document.addEventListener("mez-halftone-failure", sample);
sample();
