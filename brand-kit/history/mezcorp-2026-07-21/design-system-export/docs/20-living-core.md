# 20 · Living core

Status: DEFAULT · working values, flag deviations to Olli

Decision authority: `DEC-MOTION-002`, approved 2026-07-20

The living core is the fifth product-gradient treatment. It reconstructs a product core from four colour anchors, four spatial positions, source weights, a shade colour and a bloom colour, then renders those values as slow continuous shader motion. It is product identity in motion, not general permission to animate the interface.

## What it is

- The canonical data lives in [`../gradients.json`](../gradients.json).
- The renderer is the dependency-free ES module [`../mz-core.js`](../mz-core.js).
- The reference implementation is `canvas/core.html` in the internal source pack.
- The parametric result approximates the source swatch. It does not reproduce the Figma asset pixel for pixel.
- Figma and the supplied static WebP remain the reference when exact colour reproduction matters.

## Initial release scope

The first release is an internal identity and calibration surface. The board may render all four assigned cores so the system can be tested, but only AI OS / `MZ-G13` is production-locked. Aurora, Prism and Forge remain candidate assignments exactly as declared in [`../products.json`](../products.json).

Live-site use requires a separate consumer release decision after visual, performance, accessibility and fallback verification. This restriction avoids turning candidate calibration output into production authority.

## Where it is allowed

- Internal identity and calibration boards.
- A hero product core after that consumer is approved.
- The disc inside a product card after that consumer is approved.
- A runtime app-icon expression after that consumer is approved. Packaged operating-system icons remain static assets.
- One living core per viewport is the default maximum. A calibration matrix may exceed this only because comparison is its explicit purpose.

## Where it is banned

- Never in a table, dense list, nav chip or other repeated utility surface.
- Never on a surface repeated more than six times outside an approved calibration board.
- Never behind text.
- Never as a page or section background.
- Never on the holdco, a bundle container or a non-product element.
- Never as permission for scroll reveal, parallax, springs, animated text, moving layout or decorative ambient gradients.

## Static twin

The static fallback is the default representation, not a degraded afterthought. Every living core must declare a static WebP twin in `gradients.json`. Print, email, OG images, PDF, reduced motion, no-WebGL environments and packaged icons always use the static twin. A surface that cannot render the static twin is not allowed to render the living version.

## Motion character

- Continuous, slow and non-looping to the eye.
- No pulse, strobe, spin, breath, bounce or visible reset.
- Hover may accelerate only the fluid field to 1.85×.
- Hover never scales the core, moves its geometry or moves the wings.
- Wings, labels, chips, borders and structural overlays stay perfectly static above the live field.
- The renderer pauses when the page is hidden and skips offscreen surfaces.

## Reduced motion and failure behaviour

`prefers-reduced-motion: reduce` renders the static twin. It does not render a slowed or frozen shader. A missing WebGL context, shader compile failure, missing core definition or runtime exception also renders the static twin and reports a console error or warning with the affected core ID.

## Size

The 24px mark floor in [04-the-mark.md](04-the-mark.md) applies to living and static forms. Below 24px the mark is not used. Small surfaces use lower shader detail, but they do not change the core data or geometry.

## Data contract

Each product core in `gradients.json` carries:

```json
{
  "anchors": [
    { "hex": "#000000", "pos": [0, 0], "weight": 1 }
  ],
  "shade": "#000000",
  "bloom": "#FFFFFF",
  "staticTwin": "mz-g13.webp",
  "approximation": true
}
```

There must be exactly four anchors. Positions are normalised shader coordinates. Weights retain the source colour share after compression and clamping. The fixed extraction seed is `7`, the working sample is `160 × 160`, and colour mixing occurs in linear space.

## The rule

> A living core is one product core, rendered by the approved parametric engine, with a mandatory static twin. It may move continuously only inside the scope above. Everything surrounding it stays still.

## Machine-readable summary

```json
{
  "treatment": "living-core",
  "decision": "DEC-MOTION-002",
  "status": "DEFAULT",
  "initialRelease": "internal-only",
  "productionLockedCores": ["MZ-G13"],
  "candidateCalibrationCores": ["MZ-G20", "MZ-G06", "MZ-G15"],
  "maximumPerViewport": 1,
  "calibrationBoardException": true,
  "hover": { "fluidSpeed": 1.85, "scale": false },
  "reducedMotion": "static-twin",
  "fallback": "static-twin",
  "minimumMarkSizePx": 24,
  "approximation": true
}
```
