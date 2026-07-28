# Basit A. Khan and adjacent SaaS bento work · colour allocation in a neutral system

| | |
|---|---|
| **Slug** | `premium-neutral-with-one-colour-event` |
| **Source** | Eight screenshots and two screen recordings supplied in chat 2026-07-26. Two dark insight cards; a three-card feature row (Undove); a light bento (Product Features); a testimonial bento (Myniq, "Trusted by 2500+ companies"); four framed light-and-dark split panels (Solowire, a precision engineering study, a goals study, a deployment study). Recordings: `/Users/olivermerrick/Downloads/Basit_A._Khan_-_Chaos_of_animations_...Mo9uyH.mp4` and `..._One_of_my_favorite_landing_pages_...FYhZdn.mp4` |
| **Provided by** | Olli, screenshot |
| **Studied** | 2026-07-26 |
| **Question** | How much saturated material a neutral surface can carry before it stops reading as premium, and where that material has to sit |
| **Mez problem it serves** | GH-S04 bento lab. Variant 4 put registry material on every cell and Olli rejected it by name |
| **Originality risk** | Medium. High on two elements: the multi-hue rainbow ribbon is the source's signature and the halftone dot texture over it is its fingerprint. Neither may transfer |
| **Captures** | `scratchpad/refs/chaos_01..05.jpg`, `scratchpad/refs/landing_01..05.jpg`, plus the eight supplied stills. Not committed |

## 1 · Observed expression

**Colour budget.** Across every reference the saturated area is small and concentrated. In the Myniq
testimonial bento there are seven cells and exactly two carry gradient; the other five are paper with
grey type and a small avatar. In the two recordings the entire viewport is off-white with one
gradient ribbon sweeping through it, and the ribbon occupies roughly a third of the frame while
everything else is neutral. In the dark insight pair the gradient is not a fill at all: it is a bloom
radiating from one region and falling off to near-black across two thirds of the card, so the type
sits on darkness rather than on colour.

**What the colour is used for.** In the testimonial bento the two gradient cells are the two
**numbers**: "3x more transactions" and "70% reducing errors". Colour marks the proof, not the prose.
In the dark pair the bloom sits behind the metric. In the recordings the ribbon sits behind the
headline. Colour never lands on a body paragraph, a list item or a control.

**The frame.** Six of the eight stills wrap their cells in an outer container that has its own
radius, its own surface tone and roughly 8 to 12px of padding before the cells begin. The grid reads
as one object with parts rather than loose cards on a background. Radii are visibly concentric: the
outer curve is larger than the inner by about the padding.

**Two-tone headings.** "Accelerate *your path to total* **Network Security**", "How Precision /
**Engineering is reshaping industrial solutions**", "Grow Faster by / **Unlocking Networking
Intelligence**". One sentence, one type size, and the emphasis is carried by tone alone: grey lead-in,
ink payload.

**Cell contents.** Toggles, keycaps, segmented controls, avatars, app icons, a real code block, a
radar chart. Approximately none of these cells are an icon above a heading above two lines of body.

**Light and dark pairing.** Four of the stills pair a light cell with a near-black cell inside the
same frame. The dark cell always holds the action and the machinery; the light cell holds the claim.

## 2 · Underlying mechanism

The neutrality is what makes the colour expensive. Saturated material has value only against
restraint, so the surrounding surface is doing the work: it is buying the one coloured element its
impact. Fill every cell and the colour stops being an event and becomes wallpaper, which reads
cheaper than no colour at all because the eye has nowhere to rest and no signal to follow.

Two supporting mechanisms make it hold together. First, **the coloured element is always the most
important element**, so colour is a hierarchy instrument rather than a decoration: you can find the
protagonist of every one of these compositions by looking for the saturated area. Second, **the frame
converts a grid into an object**, which is what stops an uneven bento reading as cells that happen to
be different sizes.

Remove the frame and the cells scatter. Remove the two-tone heading and you need a second type size
to get the same emphasis. Remove the neutral majority and the whole thing collapses at once.

## 3 · Transferable principle

**Colour is an event, not a finish.** A composition reads premium when it is almost entirely neutral
and exactly one region carries saturated material, that region is large enough to be unmistakably
deliberate, and it coincides with whatever the composition wants read first.

**A grid becomes an object when it is framed.** An outer container with concentric radii turns cells
of unequal size into parts of one thing rather than a scatter.

## 4 · Original Mez expression

**Family**: Product mosaic, per `design-authority/CRAFT.md` §1.
**Protagonist**: the product material, appearing exactly once per bento, on the cell that carries
either the proof number or the shipped product.

| Source element | Mez translation | Why |
|---|---|---|
| Multi-hue rainbow ribbon | A single registry gradient on one product object | COL-10: material resolves to a product with a registry ID. We never author a gradient |
| Gradient on the proof numbers | Material on the metric cell, one per bento | The observed allocation rule, transferred exactly |
| Outer white halo and drop glow | Dropped. The frame is a surface tone change plus a hairline | MAT-02, MAT-03: ambient shadow was rejected by name |
| Halftone dot texture over the gradient | Dropped | Source fingerprint, see §5 |
| Acid blue and green CTAs | Monochrome controls from the token stack | CL-02, COL-06 |
| Photographic media wells | Product material, or real UI atoms | We have material; we do not have a photo library |
| `#FFFFFF` cards on `#F0F0F0` | `--page-white` cells inside a `--page-recessed` frame on `--page-paper` | Token stack |
| Near-black dark cells | The charcoal ramp, `#171715` to `#252523` | COL-05, CL-02: never `#0A0A0A` |
| Three equal feature cards (Undove) | Not taken | LAY-01 |
| Two-tone heading | Taken as-is: `<span>` grey lead-in inside the `h2` | Already legal grammar, used in GH-S02 |
| Frame with concentric radius | `frame` 32 outer, 8 padding, `panel` 24 cells | A legal pair from CRAFT §5 |

**The allocation rule this study produces**, which is the deliverable:

> One material cell per bento. It carries the proof or the product. Every other cell is paper or
> charcoal. If a second cell wants material, the composition has not decided what its protagonist is.

## 5 · What not to take

- **The rainbow ribbon.** Multi-hue sweeping colour across a whole viewport is the source's
  signature. Our gradients come from the registry, are bound to products, and live on product
  objects. A full-bleed decorative sweep would break COL-10 on its own.
- **The halftone dot texture** laid over the gradient in both recordings. It is the single most
  identifiable thing in this work.
- **The outer glow and white halo** around every framed panel. It is four stacked depth cues and it
  is exactly what MAT-03 and MAT-04 exist to prevent.
- **The photography.** The Undove middle card and the NeoNet hero both lean on stock imagery.
- **Any of the copy.** "Accelerate your path to total Network Security" and its siblings are theirs.

## 6 · Open questions for Olli

- The frame reads as a light grey container around near-white cells. On our paper canvas that gives
  three neutral tones stacked. Confirm whether the frame should be recessed relative to the page or
  raised, because it changes whether the bento sits *in* the page or *on* it.
- The references almost always pair a light cell with a near-black one inside the frame. Our S04
  currently has no dark surfaces until S06. Worth deciding whether S04 introduces charcoal or stays
  entirely on paper with material as the only contrast.
