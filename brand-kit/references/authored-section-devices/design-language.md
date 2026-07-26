# Eight sections Olli likes · what makes a section read as authored

| | |
|---|---|
| **Slug** | `authored-section-devices` |
| **Source** | Eight screenshots supplied in chat, 25 July 2026. Identifiable sources: Linear (FIG plates), Resend ("Go beyond editing"), a work-context landing page ("60% of work is lost in context"), a Myniq testimonial grid, plus four unattributed dashboard and split-card studies |
| **Provided by** | Olli, screenshot |
| **Studied** | 2026-07-25 |
| **Question** | Why do these read as authored rather than assembled, when a compliant Mez section built from the same tokens reads as default? |
| **Mez problem it serves** | Golden Homepage GH-S02 after four failed rebuild rounds, and the editorial sections GH-S03 to GH-S07 generally |
| **Originality risk** | **Medium overall.** High on two specific expressions: the tangled-rope metaphor object and Linear's `FIG 0.n` isometric plates are both signatures of their sources and must never be transferred. The underlying mechanisms are general |
| **Captures** | Supplied inline in session `d1e9001d`. Not committed |

Olli's framing outranks any reading of mine: *"It's not about directly doing it. It's about
understanding why they look good. What's the concept?"*

---

## 1 · Observed expression

Four device clusters, not eight unrelated designs.

### A · Emitted light (dark data cards; Resend "Go beyond editing")

Near-black cards carrying a colour field that radiates from behind the metric: warm orange for
revenue, blue for conversion, green for deliverability. A large numeral (75%, 250%, 98%) sits at
optical centre with a small directional arrow. The line chart is drawn as a glowing filament with a
single bright node at its extremum, and the dotted drop-lines from the number to the curve are
hairline. In the Resend pair, a real product UI fragment is cropped so it bleeds past the card edge.

First read is the number. Second read is the node on the curve. Third is the caption.

### B · Two registers side by side (precision engineering; goals updated)

A light editorial half beside a dark technical half, both inside a white outer frame with a soft
outer glow. Left: a two-tone heading (grey prefix line, then black subject line), a short lead,
hairline chips in a ragged cluster, a dark pill CTA with a small spinner glyph. Right: a charcoal
card with its own heading and lead, then a bespoke technical diagram, closed by a status pill and an
action pill.

The diagram differs per instance: overlapping construction circles with one active green dotted ring
in the first, a wireframe radar triangle with a blue gradient fill in the second. Same chassis,
different apparatus.

### C · A governing object, and documentary convention

*The tangle.* One continuous knotted rope runs the full width of the section. Real application marks
are caught in its loops, chat-bubble fragments ("Where's that…", "Is this accurate?") escape at the
right-hand end, and three callouts hang below on thin pointer lines, each a bold label plus a
stated number. The rope is the only graphic. Nothing else is decorated.

*The plates.* Linear runs `FIG 0.2 / 0.3 / 0.4` in mono above three thin-line isometric objects on
near-black, separated by hairline column dividers. The heading is one paragraph in two tones: the
opening sentence white, the continuation grey. The figure numbers are real references, not styling.

### D · Rationed colour on an uneven grid

The bento runs cells of deliberately unequal size, with the largest holding the largest numeral
(42%, 10X) treated as a graphic object rather than as text. One orange accent appears perhaps four
times on the whole surface: an icon tile, a toggle, one label, one avatar. Faint dotted and
square-grid textures sit inside two cells.

The testimonial grid is sharper still. Seven cells, five white and carrying words, **two** carrying
a full-bleed mesh gradient. The two gradient cells are exactly the two that carry proof numbers,
3x and 70%.

---

## 2 · Underlying mechanism

**Every one of these has a generative rule that you can name by looking at the output, and the
layout is a consequence of that rule rather than a container the content was poured into.**

- The tangle's rule is a metaphor made physical. The rope's path *is* the section's horizontal
  structure, and the taxonomy hangs off the object instead of sitting beside it. You understand
  "sprawl" before reading a word, so the words become confirmation rather than explanation.
- Linear's rule is a documentary convention. Adopt the apparatus of a technical paper and the mono
  labels, hairline gutters, restrained line drawings and even the two-tone heading all follow from
  it. The figure numbers earn their place because they genuinely reference figures.
- The dark cards' rule is that the datum is the light source. The card's whole atmosphere is an
  *output* of the metric, which is why it cannot be reskinned onto different content.
- The split's rule is that the two halves do different **jobs**: one is prose, one is instrument.
  The reader receives the claim and the apparatus in a single glance. Critically the apparatus is
  bespoke per instance, so the family reads authored rather than cloned.
- The grids' rule is that colour is a role. In the testimonial grid, colour literally means "this
  cell is the evidence". Cell size encodes importance, so the grid carries hierarchy rather than
  merely fitting content.

Two consequences follow, and they matter more than the individual devices.

**Restraint is in the number of systems, not the amount of stuff.** The tangle section is visually
busy. The dark cards carry a large luminous field. None of these is minimal. What is disciplined is
that each runs *one* device and spends everything on it. A surface running four generative systems
at once reads as noise no matter how well each is executed.

**Each rewards a second read with something correct rather than decorative.** One construction
circle is active and the rest are ghosted. A single node marks the curve's peak. "Is this accurate?"
is a real question a real person asks. The figure numbers are consistent. This is the difference
between expensive and merely clean, and it cannot be added at the end.

---

## 3 · Transferable principle

**A section reads as authored when a generative rule produced its layout, and that rule is legible
in the result. A section reads as default when its only organising idea is that the content fitted.**

The corollary is the operative one: fixing a default section means finding it a rule, not adjusting
how much is in it. Adding elements and removing elements are the same move against this axis.

---

## 4 · Original Mez expression

**Composition families** (`design-authority/CRAFT.md` §1): cluster A and D are *product mosaic* and
*metrics*, B is *authored split*, C is *architecture diagram* used at section scale.

**Protagonist**: in every Mez adoption the protagonist stays the product material. This is the
happiest finding in the study. Cluster A's mechanism, the datum as light source, is what the Living
Core already is, except the Mez version is genuinely generative rather than a static radial fill.
The reason those dark cards resonate is that Mez already owns that mechanism and does it better.

| Source element | Mez translation | Why |
|---|---|---|
| Radial glow field behind the metric | The one live Deep Mineral core, on a `data-mz-mode="dark"` band | Mez owns emitted light properly. A CSS radial would be `COL-03` and `MAT-02` |
| Near-black `#0A0A0A` card | Charcoal ramp `#171715` base, `#1B1B19` recessed, `#252523` raised | `COL-05`. Pure black is never a surface |
| White outer frame with soft outer glow | Hairline `--mz-border-default`, no shadow | `MAT-02`, `MAT-03`. Ambient glow was rejected by name |
| Green "Certified Secured" status pill | Monochrome badge | Colour belongs to product material only, `COL-06`, `COL-10`. Same translation R17 already made |
| Saturated per-card hue (orange, blue) | The product's own registry gradient, or nothing | One colour source per viewport, and it must trace to a product |
| Full-bleed mesh gradient proof cells | Material-carrying cells reserved for the proof numbers | Keeps colour as a role. Legitimate and strong: the material marks the evidence |
| Real application marks caught in the object | `brand-kit/assets/third-party-marks/`, greyscale, freestanding, no plates | `ICO-01`, `ICO-04`. Never invented |
| Huge display numeral as graphic | `--mz-type-numeric-display`, unit and label subordinate | Already the metrics family |
| Two-tone paragraph heading | The `.head-quiet` grey-prefix pattern R17 already established | Already in the system |
| `FIG 0.n` mono plate labels | **Do not adopt.** See section 5 | Signature of the source, and `TYP-04` bans decorative numbering |
| Cropped product UI bleeding past the card edge | Adopt. Crop a real workbench render or real material past the container | Implies the real thing continues. Passes `MAT-05` only if the fragment is genuinely real |

**The device that transfers most cleanly to GH-S02** is cluster C's rule, not its rope. The problem
section needs one governing object whose structure generates the layout and whose meaning is the
argument. What that object is remains open and is Olli's call.

---

## 5 · What not to take

- **The tangled rope.** High risk. It is that page's signature and it is doing the same job GH-S02
  needs, which makes it the single most tempting and most dangerous element in the set. Take the
  rule (one governing object, taxonomy hung off it), never the knot.
- **`FIG 0.2` plate numbering and the isometric line objects.** High risk. Linear's technical-paper
  register is a recognisable identity. Mez has its own technical register in mono and hairlines and
  does not need borrowed apparatus. Decorative figure numbering is also `TYP-04`.
- **Glass pills and frosted CTA capsules.** `MAT-01`.
- **The outer white frame with its glow.** It is doing the job a hairline does here.
- **Per-card hue as a mood.** Warm for revenue and cool for conversion is a colour-coding language
  Mez does not have, and inventing one would put a second colour source on the page.
- **Noise, dotted and squared texture fills.** `MAT-06`.
- **The stated numbers.** Every figure in these captures belongs to someone else. `CPY-02`.

## 6 · Open questions for Olli

**Answered 2026-07-25, and it corrects a bias in this study.** A governing rule does not require an
illustrated metaphor. Olli: *"it just visually has to show the different parts of it. It doesn't
have to be some crazy diagram… it can be just the words in boxes, but in our style. The objective is
to convey the point in a good way… in a minimalistic way. There's no need for crazy motion."*

So **structure is the visual.** Boxes, rules, alignment, count, adjacency and space are legitimate
devices in their own right, and for Mez they are usually the *better* ones. Note that two of the
eight references already work this way: Linear's rule is a documentary convention and the
testimonial grid's rule is colour-as-role, neither of which is a metaphor illustration. The device
that transfers to GH-S02 is a **structural** rule, not a picture.

This also retires the reading that GH-S02 needs a "governing object" in the sense of a drawn thing.
It needs a governing rule, and a typographic or box-based one is preferred.

1. **Which structural rule does GH-S02 use?** Six candidates put to Olli in words on 2026-07-25.
2. **Do the proof cells carry material?** Adopting cluster D's rule would let product material mark
   evidence cells on a light grid. It is a coherent extension of "material means product" but it is
   a genuine extension, so it is his to approve rather than mine to assume.
