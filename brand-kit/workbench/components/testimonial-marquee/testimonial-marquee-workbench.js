const marquees = [...document.querySelectorAll("mez-testimonial-marquee")];
const readout = document.querySelector("#motion-readout");
const samples = new Map();

marquees.forEach(marquee => {
  samples.set(marquee, {
    previousLeft: null,
    previousAutoState: null,
    runningMovementSamples: 0,
    pausedMovementSamples: 0,
    peakVisibleLive: 0,
    peakOffscreenLive: 0,
    interactionAt: null,
    interactionSource: null,
    resumeLatencyMs: null,
    ready: marquee.dataset.count != null
  });

  marquee.addEventListener("mez-testimonial-ready", () => {
    samples.get(marquee).ready = true;
  });

  marquee.addEventListener("mez-testimonial-interaction", event => {
    const state = samples.get(marquee);
    state.interactionAt = performance.now();
    state.interactionSource = event.detail.source;
    state.resumeLatencyMs = null;
  });

  marquee.addEventListener("mez-testimonial-motion-change", event => {
    const state = samples.get(marquee);
    if (event.detail.state === "running" && state.interactionAt != null) {
      state.resumeLatencyMs = Math.round(performance.now() - state.interactionAt);
    }
  });
});

function measure() {
  const proof = marquees.map(marquee => {
    const state = samples.get(marquee);
    const viewport = marquee.querySelector(".mz-testimonial-marquee__viewport");
    const left = viewport?.scrollLeft ?? 0;
    const autoState = marquee.dataset.autoState;
    const stableState = state.previousAutoState === autoState;
    const delta = state.previousLeft == null || !stableState ? 0 : Math.abs(left - state.previousLeft);
    state.previousLeft = left;
    state.previousAutoState = autoState;

    if (autoState === "running" && delta > 0.2) {
      state.runningMovementSamples += 1;
    }
    if (autoState === "paused" && delta > 0.2) {
      state.pausedMovementSamples += 1;
    }

    const viewportRect = viewport?.getBoundingClientRect();
    const portraits = [...marquee.querySelectorAll("mez-halftone-portrait")];
    const live = portraits.filter(portrait => portrait.getAttribute("data-motion") === "live");
    const visible = viewportRect ? portraits.filter(portrait => {
      const rect = portrait.getBoundingClientRect();
      return rect.right > viewportRect.left && rect.left < viewportRect.right &&
        rect.bottom > viewportRect.top && rect.top < viewportRect.bottom &&
        rect.bottom > 0 && rect.top < innerHeight;
    }) : [];
    const visibleSet = new Set(visible);
    const visibleLive = live.filter(portrait => visibleSet.has(portrait)).length;
    const offscreenLive = live.filter(portrait => !visibleSet.has(portrait)).length;
    state.peakVisibleLive = Math.max(state.peakVisibleLive, visibleLive);
    state.peakOffscreenLive = Math.max(state.peakOffscreenLive, offscreenLive);

    return {
      presentation: marquee.dataset.presentation,
      ready: state.ready,
      autoState,
      scrollLeft: Math.round(left),
      runningMovementSamples: state.runningMovementSamples,
      pausedMovementSamples: state.pausedMovementSamples,
      visibleLive,
      offscreenLive,
      peakVisibleLive: state.peakVisibleLive,
      peakOffscreenLive: state.peakOffscreenLive,
      interactionSource: state.interactionSource,
      resumeLatencyMs: state.resumeLatencyMs
    };
  });

  document.documentElement.dataset.marqueeMotionProof = JSON.stringify(proof);
  const ready = proof.filter(item => item.ready);
  const runningProven = ready.filter(item => item.runningMovementSamples > 0).length;
  const pauseLeaks = ready.reduce((sum, item) => sum + item.pausedMovementSamples, 0);
  const offscreenLeaks = ready.reduce((sum, item) => sum + item.offscreenLive, 0);
  readout.textContent = [
    `fixtures             ${ready.length}/${marquees.length} ready · 7 video portraits each`,
    `auto-scroll proof    ${runningProven}/${ready.length || marquees.length} running rails changed position`,
    `pause leakage        ${pauseLeaks} movement samples while paused`,
    `portrait allocation  ${offscreenLeaks} offscreen live now`,
    `manual recovery      ${proof.filter(item => item.resumeLatencyMs != null && item.resumeLatencyMs <= 1200).length} rails resumed within 1.2s after sampled input`,
    "",
    ...proof.map(item =>
      `${item.presentation.padEnd(18)} ${String(item.autoState || "loading").padEnd(8)} · x ${String(item.scrollLeft).padStart(4)} · live ${item.visibleLive} · motion ${item.runningMovementSamples} · recovery ${item.resumeLatencyMs == null ? "not sampled" : `${item.resumeLatencyMs}ms`}`
    )
  ].join("\n");
}

measure();
setInterval(measure, 400);
