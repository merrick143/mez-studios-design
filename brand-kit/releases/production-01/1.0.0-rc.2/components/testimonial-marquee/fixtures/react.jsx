/* Testimonial Marquee · thin React adapter
 *
 * The custom element owns loading, semantics, scrolling and controls. This
 * adapter only maps props to attributes and forwards component events.
 *
 *   import { TestimonialMarquee } from "./react.jsx";
 *   import "../mez-testimonial-marquee.css";
 *   import "../mez-testimonial-marquee.js";
 */

import { useEffect, useRef } from "react";

export function TestimonialMarquee({
  src,
  label,
  presentation = "social-caption",
  className,
  style,
  onReady,
  onChange,
  onInteraction,
  onMotionChange,
  onFailure
}) {
  const ref = useRef(null);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;
    if (src == null) element.removeAttribute("src");
    else element.setAttribute("src", String(src));
    if (label == null) element.removeAttribute("label");
    else element.setAttribute("label", String(label));
    if (presentation == null) element.removeAttribute("presentation");
    else element.setAttribute("presentation", String(presentation));
  }, [src, label, presentation]);

  useEffect(() => {
    const element = ref.current;
    if (!element) return undefined;
    const ready = event => onReady?.(event.detail);
    const change = event => onChange?.(event.detail);
    const interaction = event => onInteraction?.(event.detail);
    const motionChange = event => onMotionChange?.(event.detail);
    const failure = event => onFailure?.(event.detail);
    element.addEventListener("mez-testimonial-ready", ready);
    element.addEventListener("mez-testimonial-change", change);
    element.addEventListener("mez-testimonial-interaction", interaction);
    element.addEventListener("mez-testimonial-motion-change", motionChange);
    element.addEventListener("mez-testimonial-failure", failure);
    return () => {
      element.removeEventListener("mez-testimonial-ready", ready);
      element.removeEventListener("mez-testimonial-change", change);
      element.removeEventListener("mez-testimonial-interaction", interaction);
      element.removeEventListener("mez-testimonial-motion-change", motionChange);
      element.removeEventListener("mez-testimonial-failure", failure);
    };
  }, [onReady, onChange, onInteraction, onMotionChange, onFailure]);

  return <mez-testimonial-marquee ref={ref} class={className} style={style} />;
}

export default TestimonialMarquee;
