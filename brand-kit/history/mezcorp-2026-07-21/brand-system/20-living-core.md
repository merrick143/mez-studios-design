# 20 · Living core

Status: DEFAULT · working values, flag deviations to Olli

Decision authority: `DEC-MOTION-002`, approved 2026-07-20

The living core is the fifth product-gradient treatment. It reconstructs a product core from four colour anchors, four spatial positions, source weights, a shade colour and a bloom colour, then renders those values as slow continuous shader motion. It is product identity in motion, not general permission to animate the interface.

## What it is

- The canonical data lives in [`../gradients.json`](../gradients.json).
- The renderer is the dependency-free ES module [`../design-system-export/mz-core.js`](../design-system-export/mz-core.js).
- The reference implementation is [`../canvas/core.html`](../canvas/core.html).
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

## One engine, four expression masks

The Living Core is one renderer, not a collection of separately styled components. The same core data and shader feed four approved masks:

- **Disc** — the canonical compact product mark and default card object.
- **Sphere** — the large identity expression for a hero, launch frame or single focal product.
- **Rounded rectangle** — the core field inside a trading card or compact pill. The surrounding card, copy and controls are ordinary static UI.
- **Wings** — a gradient-field expression of the canonical Wings geometry for identity or motion studies. The ordinary product mark remains white Wings inside the core.

Shape changes never create a new palette, lighting model or motion language. This is the practical meaning of **one chassis, many cores**.

## Expression selection law

These defaults apply until the dedicated product-expression component suite is approved:

| Output | Default expression | Animation rule |
| --- | --- | --- |
| Website hero for one focal product | sphere or disc | one approved Living Core maximum |
| Mez Systems family hero | static product objects | multi-core animation is calibration-only until promoted |
| Product card or catalogue grid | static disc or static card field | a single focal card may animate after consumer approval |
| Bundle, upsell or checkout summary | aligned static discs/cards | bundle container and price UI never animate |
| Navigation, filter or dense utility UI | static compact mark; no core if below the mark floor | never animated |
| Email, ad still, social still, OG image, document, print or PDF | exact static twin | never WebGL |
| Video or motion ad | rendered Living Core as one focal product object | surrounding typography, Wings and end frame remain static |
| Packaged app icon or favicon | exact static asset | runtime app-icon motion requires a separate consumer decision |

When more than one product appears, use equal geometry and alignment. Product distinction comes from the core and copy, not jagged card sizes, ornamental labels or a different chassis for every product.

## Static versus animated decision

Use the animated form only when all of the following are true:

1. The output is a live runtime or authored motion file.
2. One product is the intentional focal object.
3. Motion materially improves recognition or product energy.
4. The exact static twin is present and tested.
5. Reduced motion, offscreen pause and failure fallback are working.
6. The consuming surface has a recorded promotion decision.

If any condition fails, use the exact static twin. Static is the system default; motion is an approved expression mode.

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

## Ingestion and candidate rule

An assigned core is generated from a square source gradient at least `512 × 512` pixels. The deterministic extractor downsamples to `160 × 160`, runs seeded five-cluster k-means, uses the darkest cluster as shade, and stores the other four clusters with source positions and weights. Rebuilding the same source with the pinned toolchain must produce identical data.

New product gradients enter as research candidates. The candidate workflow may generate a review plate and exact static twin, but it must not edit `products.json`, `gradients.json`, `palettes.json` or the portable export. Promotion requires:

1. visual comparison with the exact source;
2. approval of the static and animated expressions;
3. a product-assignment decision;
4. canonical data and portable mirrors updated together;
5. deterministic validators passing.

`DEC-PRODUCT-ARCHITECTURE-001` assigns Context Engine to the genuine `MZ-G12` source. The assignment is an approved migration input and must enter the canonical registries only through the atomic versioned migration snapshot.

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
