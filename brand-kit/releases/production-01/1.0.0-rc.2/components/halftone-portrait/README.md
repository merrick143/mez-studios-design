# TASK-CMP-05 · Halftone Portrait

**Status: canonical 1.0.0 under `DEC-HALFTONE-PORTRAIT-COMPONENT-001`. No release package is built.**

A human face rendered as a live halftone dot grid, drawn from video on a canvas
one frame at a time. The component owns the render contract and the motion
allocation. The consumer owns the media, the caption and the layout around it.

Only the animated portrait is in scope. The testimonial card is deliberately
absent: Olli asked for the moving part alone because he intends to design a
better card.

## Usage

```html
<link rel="stylesheet" href="brand-kit/components/halftone-portrait/mez-halftone-portrait.css" />

<mez-halftone-portrait
  src="./media/portrait-a.mp4"
  label="Halftone portrait of the speaker"
  grid-step="4" max-radius="1.8"
  dot-colour="#212121" background="#ffffff"
  contrast="1.3" brightness="-0.03"
></mez-halftone-portrait>

<script type="module" src="brand-kit/components/halftone-portrait/mez-halftone-portrait.js"></script>
```

Open `fixtures/static-html.html` for the dependency-free proof, or
`workbench/components/halftone-portrait/` for the instrumented review page.
`fixtures/react.jsx` is a thin props-to-attributes bridge.

## The two rules the component leans on

### The cutout is not a runtime concern

The look depends on the subject being separated from the room. The obvious
implementation runs segmentation live, and that is what the original React
version did: an 11MB wasm runtime, a 244KB model and a neural network on every
frame, in every consumer, forever.

It is unnecessary. The mask never changes once a clip is approved, and a
luminance halftone maps a light plate to no dots. So the subject is composited
over solid white **before** the media reaches the browser, and a plain halftone
reproduces the identical result for free.

The component therefore has no model, no wasm, no dependencies and makes no
network calls. `verify_halftone_portrait_contract.py` asserts that against the
JavaScript rather than trusting this paragraph.

Media preparation lives with the pipeline that produces the clips, documented in
`fixtures/media/PROVENANCE.md`.

### Motion is allocated by default, and the escape is recorded

Website Motion 1.0.0 permits one expressive event running in the viewport, so
the default policy is `allocated`: every instance mounts **static**, and a
shared `IntersectionObserver` hands the animation to the single most visible
one. Instances that are not animating hold a complete static halftone frame;
they are never blank, dimmed or placeholder.

`motion-policy="always"` opts an instance out of that allocation and lets it
animate whenever it is visible. **This is a bounded exception approved by Olli
on 2026-07-27 for the testimonial marquee**, recorded as
`motionDecisionException` in the source contract, on the same footing as the
five-live-cores exception Global Navigation carries.

It is cheaper than that one. A halftone portrait costs a canvas fill, not a
WebGL context or a neural network, and an always-on instance still idles the
moment it leaves the viewport, so a long marquee never pays for portraits nobody
can see.

The default is unchanged: a portrait dropped onto any other surface still
allocates one live instance. The workbench measures both policies, because a
documented budget that nothing enforces is not a budget.

## Fallbacks

| Condition | Result |
|---|---|
| `prefers-reduced-motion` | One frame painted, no render loop. The static frame carries the same meaning. |
| `?static` in the URL | Same as reduced motion. For review and screenshots. |
| Not the allocated instance | Complete static frame. |
| Autoplay refused | Silently keeps the static frame. No fabricated play control. |
| Missing or broken source | Box retained, reason stated, `mez-halftone-failure` dispatched. |
| Tainted canvas (cross-origin media) | Same visible failure rather than a per-frame exception. |

## Attributes

| Attribute | Default | Notes |
|---|---|---|
| `src` | required | Same-origin or CORS-enabled |
| `label` | required | Accessible label on the canvas |
| `grid-step` | `4` | Grid pitch in CSS px. Lower is finer and costs more |
| `max-radius` | `grid-step / 2` | Radius of a fully dark dot |
| `dot-colour` | `#212121` | |
| `background` | `#ffffff` | Plate painted behind the dots |
| `contrast` | `1.3` | Tone gain around mid grey |
| `brightness` | `-0.03` | Offset after contrast |
| `dot-gamma` | `1` | Radius response curve. Below 1 fattens midtones |
| `screen-angle` | `0` | Rotates the lattice like a print screen angle |
| `stagger` | absent | Half-step offset on alternate rows |
| `invert` | absent | Light areas take the large dots |
| `auto-levels` | `on` | Set `off` to disable the per-frame histogram stretch |
| `dot-shape` | `circle` | `circle`, `square`, `diamond`, `cross`, `ring` |
| `zoom` | `1` | Crop in. Never below 1, there is no source outside the frame |
| `focus-x`, `focus-y` | `0.5` | Crop centre when zoomed |
| `motion-policy` | `allocated` | `always` opts out of the one-live allocation. Bounded exception |

Events: `mez-halftone-ready`, `mez-halftone-failure`.

## How the render works

Per frame: the video is drawn into an offscreen canvas **sized to the dot grid**
rather than the display, so the browser performs the downscale and
`getImageData` reads one pixel per cell instead of the whole frame. Each cell's
luminance is `0.299R + 0.587G + 0.114B`, stretched by a per-frame histogram,
pushed through the tone curve, and drawn as one dot. Every dot joins a single
path and is filled once.

Two details are load-bearing and easy to undo by accident:

**Auto-levels.** Without it, every clip needs hand-tuned contrast, and a
well-lit face on a light plate falls entirely below the dot threshold and
renders as a blank silhouette. The range is eased 12 percent per frame so
exposure changes do not pulse the grid.

**Device pixel ratio is clamped to 2.** A 3x backing store triples fill cost
with no visible gain at this dot size.

## What this component must never do

Fabricate a subject, assert consent for a likeness, fetch media it was not
given, run a model, animate beyond its declared policy, render blank when motion
is unavailable, or own a quote, a name, a card or a marquee.

## Settled

- **A marquee may animate several portraits.** Approved by Olli on 2026-07-27
  and implemented as `motion-policy="always"`.
- **The fixture likenesses are consented.** Confirmed by Olli on 2026-07-27; the
  subjects are people he knows and who agreed to appear. See
  `fixtures/media/PROVENANCE.md`. Do not re-open this in review.

## Open questions for the human gate

1. **Does this belong in the Phase B pantry?** It is not a product or commerce
   component, so it currently carries no pantry ID.
2. **Should the matte carry an alpha channel?** The baked light plate removes the
   ML runtime but also removes a real inverted treatment, because inverting now
   dots the plate instead of the subject.

## Known gaps

No Gate B design-critique pass has been run. No responsive evidence has been
captured across the declared viewports. This is a candidate, and it says so
everywhere it can.
