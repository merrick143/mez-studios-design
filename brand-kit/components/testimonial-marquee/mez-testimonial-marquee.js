/* TASK-CMP-06 · Testimonial Marquee · Round 03
 *
 * A continuously drifting testimonial rail, approved by Olli as a bounded
 * CMP-06 exception on 2026-07-28. The exception does not rewrite Website
 * Motion 1.0.0: it is scoped to this component and requires phase hover/focus,
 * manual-input recovery, offscreen and reduced-motion safeguards.
 *
 * The fixture owns every quote, name, Instagram fact and media path. This
 * element owns the viewport, track, motion, semantics and responsive
 * presentation. Portrait rendering stays with <mez-halftone-portrait>.
 */

import "../halftone-portrait/mez-halftone-portrait.js";

const query = new URLSearchParams(location.search);
const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
const forceStatic = reduced || query.has("static");
const AUTO_SPEED_PX_PER_SECOND = 24;
const INTERACTION_PAUSE_MS = 900;
const PRESENTATIONS = new Set([
  "profile-strip",
  "portrait-window",
  "social-caption",
  "quote-first",
  "proof-ledger"
]);

const escapeHtml = value => String(value).replace(/[&<>'"]/g, character => ({
  "&": "&amp;",
  "<": "&lt;",
  ">": "&gt;",
  "'": "&#39;",
  '"': "&quot;"
})[character]);

const isSafeFixtureUrl = value => {
  try {
    const url = new URL(value, document.baseURI);
    return url.origin === location.origin;
  } catch {
    return false;
  }
};

export function validateTestimonials(value) {
  if (!Array.isArray(value) || value.length === 0) {
    return "at least one testimonial is required";
  }

  const ids = new Set();
  for (const [index, item] of value.entries()) {
    const at = `testimonial ${index + 1}`;
    if (!item || typeof item !== "object") return `${at} is not an object`;
    if (!item.id || typeof item.id !== "string") return `${at} has no stable id`;
    if (ids.has(item.id)) return `${at} repeats id '${item.id}'`;
    ids.add(item.id);
    if (!item.quote || typeof item.quote !== "string") return `${at} has no quote`;
    if (!item.name || typeof item.name !== "string") return `${at} has no name`;
    if (!item.handle || typeof item.handle !== "string") return `${at} has no handle`;
    if (!item.portrait?.src || !item.portrait?.label) return `${at} has no approved portrait`;
    if (!item.social || typeof item.social !== "object") return `${at} has no social proof`;
    if (item.social.platform !== "Instagram") return `${at} social platform is not Instagram`;
    if (!item.social.followers || typeof item.social.followers !== "string") return `${at} has no follower count`;
    if (item.social.verified !== true) return `${at} is not verified`;
    if (!item.social.profileImage || !isSafeFixtureUrl(item.social.profileImage)) return `${at} has no local profile image`;
  }
  return null;
}

class MezTestimonialMarquee extends HTMLElement {
  static observedAttributes = ["src", "label", "presentation"];

  constructor() {
    super();
    this.viewport = null;
    this.primaryTrack = null;
    this.items = [];
    this.status = null;
    this.abortController = null;
    this.hostObserver = null;
    this.resizeObserver = null;
    this.animationFrame = null;
    this.lastFrameAt = null;
    this.autoOffset = 0;
    this.cycleWidth = 0;
    this.isVisible = false;
    this.hoverPaused = false;
    this.focusPaused = false;
    this.pointerActive = false;
    this.interactionPauseUntil = 0;
    this.currentAutoState = null;
    this.onKeyDown = event => this.handleKeyDown(event);
    this.onPointerDown = () => {
      this.pointerActive = true;
      this.registerInteraction("pointerdown");
    };
    this.onPointerMove = () => {
      if (this.pointerActive) this.registerInteraction("pointermove");
    };
    this.onPointerEnd = event => {
      this.pointerActive = false;
      this.registerInteraction(event.type);
    };
    this.onWheelIntent = () => this.registerInteraction("wheel");
    this.onPointerEnter = () => {
      this.hoverPaused = true;
      this.syncAutoState();
    };
    this.onPointerLeave = () => {
      this.hoverPaused = false;
      this.syncAutoState();
    };
    this.onFocusIn = () => {
      this.focusPaused = true;
      this.syncAutoState();
    };
    this.onFocusOut = event => {
      if (!this.viewport?.contains(event.relatedTarget)) {
        this.focusPaused = false;
        this.syncAutoState();
      }
    };
    this.onVisibilityChange = () => this.syncAutoState();
  }

  connectedCallback() {
    this.normalisePresentation();
    this.dataset.motionMode = forceStatic ? "static-complete" : "auto-scroll";
    this.load();
  }

  disconnectedCallback() {
    this.stopAutoScroll();
    this.abortController?.abort();
    this.hostObserver?.disconnect();
    this.resizeObserver?.disconnect();
    document.removeEventListener("visibilitychange", this.onVisibilityChange);
    this.detachViewportListeners();
  }

  attributeChangedCallback(name, previous, next) {
    if (name === "presentation") this.normalisePresentation();
    if (previous !== next && this.isConnected && name !== "presentation") this.load();
  }

  normalisePresentation() {
    const requested = this.getAttribute("presentation") || "social-caption";
    this.dataset.presentation = PRESENTATIONS.has(requested) ? requested : "social-caption";
  }

  detachViewportListeners() {
    if (!this.viewport) return;
    this.viewport.removeEventListener("keydown", this.onKeyDown);
    this.viewport.removeEventListener("pointerdown", this.onPointerDown);
    this.viewport.removeEventListener("pointermove", this.onPointerMove);
    this.viewport.removeEventListener("pointerup", this.onPointerEnd);
    this.viewport.removeEventListener("pointercancel", this.onPointerEnd);
    this.viewport.removeEventListener("wheel", this.onWheelIntent);
    this.viewport.removeEventListener("pointerenter", this.onPointerEnter);
    this.viewport.removeEventListener("pointerleave", this.onPointerLeave);
    this.viewport.removeEventListener("focusin", this.onFocusIn);
    this.viewport.removeEventListener("focusout", this.onFocusOut);
  }

  async load() {
    const source = this.getAttribute("src");
    if (!source) {
      this.fail("testimonial source unavailable");
      return;
    }
    if (!isSafeFixtureUrl(source)) {
      this.fail("testimonial source must be same-origin");
      return;
    }

    this.stopAutoScroll();
    this.detachViewportListeners();
    this.abortController?.abort();
    this.abortController = new AbortController();

    try {
      const url = new URL(source, document.baseURI);
      const response = await fetch(url, {
        credentials: "same-origin",
        signal: this.abortController.signal
      });
      if (!response.ok) throw new Error("testimonial source unavailable");
      const fixture = await response.json();
      const testimonials = fixture.testimonials ?? fixture;
      const failure = validateTestimonials(testimonials);
      if (failure) throw new Error(failure);
      this.render(testimonials, url);
    } catch (error) {
      if (error?.name !== "AbortError") this.fail(error?.message || "testimonial source unavailable");
    }
  }

  render(testimonials, fixtureUrl) {
    this.hostObserver?.disconnect();
    this.resizeObserver?.disconnect();
    this.removeAttribute("data-failure");

    const label = this.getAttribute("label") || "Testimonials";
    const primaryItems = testimonials
      .map((item, index) => this.renderItem(item, index, testimonials.length, fixtureUrl, false))
      .join("");
    const clonedItems = forceStatic
      ? ""
      : testimonials
          .map((item, index) => this.renderItem(item, index, testimonials.length, fixtureUrl, true))
          .join("");

    this.dataset.count = String(testimonials.length);
    this.innerHTML = `
      <div class="mz-testimonial-marquee__frame">
        <div class="mz-testimonial-marquee__viewport"
          tabindex="0" role="region" aria-roledescription="carousel"
          aria-label="${escapeHtml(label)}">
          <div class="mz-testimonial-marquee__rail">
            <ol class="mz-testimonial-marquee__track" data-copy="primary">${primaryItems}</ol>
            ${forceStatic ? "" : `<ol class="mz-testimonial-marquee__track" data-copy="clone" aria-hidden="true">${clonedItems}</ol>`}
          </div>
        </div>
        <p class="mz-testimonial-marquee__status" aria-live="polite" aria-atomic="true"></p>
      </div>
    `;

    this.viewport = this.querySelector(".mz-testimonial-marquee__viewport");
    this.primaryTrack = this.querySelector('[data-copy="primary"]');
    this.items = [...this.primaryTrack.querySelectorAll(".mz-testimonial-marquee__item")];
    this.status = this.querySelector(".mz-testimonial-marquee__status");
    this.pointerActive = false;
    this.interactionPauseUntil = 0;
    this.currentAutoState = null;

    this.viewport.addEventListener("keydown", this.onKeyDown);
    this.viewport.addEventListener("pointerdown", this.onPointerDown, { passive: true });
    this.viewport.addEventListener("pointermove", this.onPointerMove, { passive: true });
    this.viewport.addEventListener("pointerup", this.onPointerEnd, { passive: true });
    this.viewport.addEventListener("pointercancel", this.onPointerEnd, { passive: true });
    this.viewport.addEventListener("wheel", this.onWheelIntent, { passive: true });
    this.viewport.addEventListener("pointerenter", this.onPointerEnter);
    this.viewport.addEventListener("pointerleave", this.onPointerLeave);
    this.viewport.addEventListener("focusin", this.onFocusIn);
    this.viewport.addEventListener("focusout", this.onFocusOut);
    document.addEventListener("visibilitychange", this.onVisibilityChange);

    if (forceStatic) {
      this.status.textContent = `All ${this.items.length} testimonials are shown as a complete list.`;
      this.dataset.autoState = "static";
    } else {
      this.status.textContent = `${this.items.length} testimonials. Use arrow keys to browse.`;
      this.setupAutoScroll();
    }

    this.dispatchEvent(new CustomEvent("mez-testimonial-ready", {
      bubbles: true,
      detail: {
        count: testimonials.length,
        portraits: testimonials.length,
        socialProfiles: testimonials.length,
        verified: testimonials.filter(item => item.social.verified).length,
        motionMode: this.dataset.motionMode,
        presentation: this.dataset.presentation
      }
    }));
  }

  renderItem(item, index, total, fixtureUrl, clone) {
    return `
      <li class="mz-testimonial-marquee__item" data-testimonial-id="${escapeHtml(item.id)}"
        ${clone ? 'data-clone="true" aria-hidden="true"' : `aria-label="${index + 1} of ${total}"`}>
        <figure>
          <mez-halftone-portrait
            class="mz-testimonial-marquee__portrait"
            motion-policy="always"
            src="${escapeHtml(new URL(item.portrait.src, fixtureUrl).href)}"
            label="${escapeHtml(item.portrait.label)}"
            grid-step="4" max-radius="1.8"
            dot-colour="#212121" background="#ffffff"
            contrast="1.3" brightness="-0.03"
          ></mez-halftone-portrait>
          <div class="mz-testimonial-marquee__copy">
            <figcaption class="mz-testimonial-marquee__instagram">
              <img class="mz-testimonial-marquee__profile-image"
                src="${escapeHtml(new URL(item.social.profileImage, fixtureUrl).href)}" alt="" />
              <span class="mz-testimonial-marquee__profile-copy">
                <span class="mz-testimonial-marquee__name-line">
                  <strong class="mz-testimonial-marquee__name">${escapeHtml(item.name)}</strong>
                  <span class="mz-testimonial-marquee__verified" role="img" aria-label="Verified Instagram account"><span aria-hidden="true">✓</span></span>
                </span>
                <span class="mz-testimonial-marquee__handle">${escapeHtml(item.handle)}</span>
                <span class="mz-testimonial-marquee__followers">${escapeHtml(item.social.followers)}</span>
              </span>
            </figcaption>
            <blockquote>${escapeHtml(item.quote)}</blockquote>
          </div>
        </figure>
      </li>
    `;
  }

  setupAutoScroll() {
    this.resizeObserver = new ResizeObserver(() => {
      this.cycleWidth = this.primaryTrack?.getBoundingClientRect().width ?? 0;
    });
    this.resizeObserver.observe(this.primaryTrack);
    this.hostObserver = new IntersectionObserver(entries => {
      this.isVisible = entries.some(entry => entry.isIntersecting && entry.intersectionRatio > 0.08);
      this.syncAutoState();
    }, { threshold: [0, 0.08, 0.25] });
    this.hostObserver.observe(this);
    this.cycleWidth = this.primaryTrack.getBoundingClientRect().width;
    this.autoOffset = this.viewport.scrollLeft;
    this.animationFrame = requestAnimationFrame(time => this.tick(time));
  }

  stopAutoScroll() {
    if (this.animationFrame != null) cancelAnimationFrame(this.animationFrame);
    this.animationFrame = null;
    this.lastFrameAt = null;
  }

  shouldAutoScroll(now = performance.now()) {
    return !forceStatic && this.isVisible && document.visibilityState === "visible" &&
      !this.pointerActive && !this.hoverPaused && !this.focusPaused && now >= this.interactionPauseUntil;
  }

  tick(time) {
    if (this.lastFrameAt == null) this.lastFrameAt = time;
    const delta = Math.min(64, time - this.lastFrameAt);
    this.lastFrameAt = time;

    if (this.shouldAutoScroll(time) && this.viewport && this.cycleWidth > 0) {
      this.autoOffset += AUTO_SPEED_PX_PER_SECOND * delta / 1000;
      if (this.autoOffset >= this.cycleWidth) {
        this.autoOffset -= this.cycleWidth;
      }
      this.viewport.scrollLeft = this.autoOffset;
    } else if (this.viewport) {
      this.autoOffset = this.viewport.scrollLeft;
    }
    this.syncAutoState(time);
    this.animationFrame = requestAnimationFrame(next => this.tick(next));
  }

  syncAutoState(now = performance.now()) {
    if (forceStatic) return;
    const next = this.shouldAutoScroll(now) ? "running" : "paused";
    if (next === this.currentAutoState) return;
    this.currentAutoState = next;
    this.dataset.autoState = next;
    this.dispatchEvent(new CustomEvent("mez-testimonial-motion-change", {
      bubbles: true,
      detail: { state: next }
    }));
  }

  registerInteraction(source) {
    this.interactionPauseUntil = performance.now() + INTERACTION_PAUSE_MS;
    this.syncAutoState();
    this.emitInteraction(source);
  }

  currentIndex() {
    if (!this.viewport || !this.items.length || !this.cycleWidth) return 0;
    const position = ((this.viewport.scrollLeft % this.cycleWidth) + this.cycleWidth) % this.cycleWidth;
    let bestIndex = 0;
    let bestDistance = Number.POSITIVE_INFINITY;
    this.items.forEach((item, index) => {
      const distance = Math.abs(item.offsetLeft - position);
      if (distance < bestDistance) {
        bestDistance = distance;
        bestIndex = index;
      }
    });
    return bestIndex;
  }

  move(direction, source) {
    if (forceStatic || this.items.length === 0) return;
    const current = this.currentIndex();
    const next = (current + direction + this.items.length) % this.items.length;
    this.goTo(next, source);
  }

  handleKeyDown(event) {
    const keys = ["ArrowLeft", "ArrowRight", "Home", "End"];
    if (!keys.includes(event.key) || forceStatic) return;
    event.preventDefault();
    if (event.key === "ArrowLeft") this.move(-1, "keyboard");
    if (event.key === "ArrowRight") this.move(1, "keyboard");
    if (event.key === "Home") this.goTo(0, "keyboard");
    if (event.key === "End") this.goTo(this.items.length - 1, "keyboard");
  }

  goTo(index, source) {
    if (forceStatic || !this.items[index]) return;
    this.registerInteraction(source);
    this.items[index].scrollIntoView({
      behavior: "auto",
      block: "nearest",
      inline: "start"
    });
    this.status.textContent = `Testimonial ${index + 1} of ${this.items.length}: ${this.items[index].dataset.testimonialId.replaceAll("-", " ")}.`;
    this.dispatchEvent(new CustomEvent("mez-testimonial-change", {
      bubbles: true,
      detail: { index, id: this.items[index].dataset.testimonialId, source }
    }));
  }

  emitInteraction(source) {
    this.dispatchEvent(new CustomEvent("mez-testimonial-interaction", {
      bubbles: true,
      detail: { source }
    }));
  }

  fail(reason) {
    this.stopAutoScroll();
    this.dataset.failure = reason;
    this.innerHTML = `<p class="mz-testimonial-marquee__failure" role="status">Testimonials are unavailable.</p>`;
    this.dispatchEvent(new CustomEvent("mez-testimonial-failure", {
      bubbles: true,
      detail: { reason }
    }));
  }
}

if (!customElements.get("mez-testimonial-marquee")) {
  customElements.define("mez-testimonial-marquee", MezTestimonialMarquee);
}

export { MezTestimonialMarquee };
