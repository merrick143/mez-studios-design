/* Halftone Portrait · thin React adapter
 *
 * The custom element does the work. This is only a props-to-attributes bridge
 * and an event subscription, which is all a React consumer needs. It owns no
 * rendering, no media and no layout, and it deliberately does not wrap the
 * element in a card: the card is out of scope for CMP-05.
 *
 *   import { HalftonePortrait } from "./react.jsx";
 *   import "../mez-halftone-portrait.css";
 *   import "../mez-halftone-portrait.js";
 */

import { useEffect, useRef } from "react";

/* Boolean attributes are present or absent, never "false" as a string. */
const BOOLEAN_PROPS = new Set(["stagger", "invert"]);

const ATTRIBUTE_NAMES = {
  src: "src",
  label: "label",
  gridStep: "grid-step",
  maxRadius: "max-radius",
  dotColour: "dot-colour",
  background: "background",
  contrast: "contrast",
  brightness: "brightness",
  dotGamma: "dot-gamma",
  screenAngle: "screen-angle",
  stagger: "stagger",
  invert: "invert",
  autoLevels: "auto-levels",
  dotShape: "dot-shape",
  zoom: "zoom",
  focusX: "focus-x",
  focusY: "focus-y"
};

export function HalftonePortrait({ onReady, onFailure, className, style, ...props }) {
  const ref = useRef(null);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    for (const [prop, attribute] of Object.entries(ATTRIBUTE_NAMES)) {
      const value = props[prop];
      if (value === undefined || value === null || value === false) {
        element.removeAttribute(attribute);
      } else if (BOOLEAN_PROPS.has(prop)) {
        element.setAttribute(attribute, "");
      } else {
        element.setAttribute(attribute, String(value));
      }
    }
  });

  useEffect(() => {
    const element = ref.current;
    if (!element) return undefined;
    const ready = event => onReady?.(event);
    const failure = event => onFailure?.(event.detail);
    element.addEventListener("mez-halftone-ready", ready);
    element.addEventListener("mez-halftone-failure", failure);
    return () => {
      element.removeEventListener("mez-halftone-ready", ready);
      element.removeEventListener("mez-halftone-failure", failure);
    };
  }, [onReady, onFailure]);

  return <mez-halftone-portrait ref={ref} class={className} style={style} />;
}

export default HalftonePortrait;
