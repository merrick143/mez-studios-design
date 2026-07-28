# Craft

How to make a Mez composition good, not merely legal. The canon says what never to make; this says
how to make the thing well.

Read the sections that bear on the surface you are building. Do not read it end to end every time.

---

## 0 · The one question

**What is the protagonist, and does the composition make it so?**

In this system the answer is almost always the product material. Typography, Wings, surfaces and
controls exist to give it a disciplined stage. Premium comes from hierarchy, proportion, restraint
and exact repetition. It does not come from luxury styling, decorative noise or fashionable effects,
and gradient material never compensates for weak layout.

If you cannot name the protagonist of a section in one phrase, the section has no idea yet and no
amount of treatment will supply one.

---

## 1 · Composition families

**This is the most load-bearing section in this file.** A composition family is the structural
pattern a section uses to make its argument. Naming it is what stops a page becoming the same shape
repeated at different sizes, and what stops a rebuild becoming a reshuffle.

| Family | Structure | The argument it makes |
|---|---|---|
| **Editorial narrative** | One column, generous measure, sequenced prose with a scale or serif accent | "Here is the reasoning" |
| **Product mosaic** | Uneven grid of unequal cells, cell count bound to content count | "Here is the whole set at once" |
| **Sticky proof** | One pinned element while a second column scrolls past it | "This holds while the evidence accumulates" |
| **Workflow sequence** | Ordered steps with a directional device; numbered only if the sequence is real | "This happens, then this" |
| **Architecture diagram** | Nodes and relationships, deliberate non-grid placement | "Here is how the parts connect" |
| **Metrics** | Few large numbers, unit and label subordinate, no decoration | "The scale is this" |
| **Comparison** | Two or three parallel columns with one explicit axis of difference | "This versus that, on one dimension" |
| **Immersive demo** | Media dominant, copy reduced to a caption, frame near or past the container edge | "Watch it work" |
| **Authored split** | Light editorial half beside a charcoal generative half carrying a bespoke per-section visual | "The claim, and the thing the claim is about" |
| **Testimonial proof** | Human evidence in the lightest form the system allows | "Someone real says so" |

**Authored split** is the family established by Golden Homepage R17 for the editorial sections. Its
defining discipline: the dark-side visual is **bespoke per section**, so the family reads authored
rather than cloned. A split card whose dark half is interchangeable with its neighbour's has failed
the family, not merely executed it poorly.

### How to use the taxonomy

Before building anything, write the family beside every section in order. **That list is the artefact
you review, not the finished page.** Then test it:

| Test | Pass |
|---|---|
| Adjacency | No two consecutive sections share a family |
| Frequency | No family used more than twice on a page |
| Density change | The density sequence changes at least twice |
| Alternation cap | Media-side alternation runs at most three rows before the pattern must break |
| Section count | Six to ten between nav and footer; more than ten means two pages |
| Scroll rate | No more than two consecutive full-viewport sections |
| Cell honesty | Every grid's cell count matches the content it represents, not what fits |

### Why consistency turns into repetition

The failure is never the tokens and rarely the components. It is that every section gets drawn from
the same one or two families, so the page has one shape at different sizes. Three causes, all
avoidable:

1. **Composing from a section list instead of a composition plan.** Two "feature rows" are the same
   family. Three in a row is a pattern the eye solves after the first and skips thereafter.
2. **Uniform density.** A constant information rate reads as length regardless of actual length.
   This bites hardest on mobile, where the columns are gone and family variety is the only
   remaining differentiator.
3. **Cell counts chosen for layout convenience.** Three cards because three fits, not because there
   are three things.

### The rebuild trap

When a section is rejected, the reflex is to keep the family and change the amount of stuff in it:
add a visual, remove a visual, add motion, strip it back. That is sliding a quantity dial, and it
is how four rebuild rounds can all fail while each one is "different". **A genuine restart changes
the family.** If the plan for round n+1 has the same family as round n, it is not a restart.

---

## 2 · Pacing

Pacing is the rate at which a page delivers new information.

**The movement model.** A page has three or four movements, not seven equal sections.

| Movement | Job | Density | Span |
|---|---|---|---|
| Open | One claim, one visual, one action | Sparse | 1 section |
| Argue | Evidence, mechanism, scope | Standard, family varying every slot | 2 to 4 sections |
| Decide | Comparison, objection handling, price | Compact | 1 to 2 sections |
| Close | Repeat the action | Sparse | 1 section |

**Density modes.** Sparse: one idea, large type, generous space, used to open and close. Standard:
the working mode, a claim plus its support. Compact: many small facts scanned rather than read,
used for indexes, matrices and FAQs. Assign one per section and check the sequence changes.

**Alternation.** Left/right/left stops three identical rows and costs nothing. It stops working at
the fourth row, because by then the reader predicts the next one and scanning replaces reading.

---

## 3 · Hierarchy, asymmetry and space

**Focal points.** Every section has exactly one. Establish it with size, weight, isolation or
material: ideally one of those, not all four at once. Two elements competing for first read is the
most common composition defect, and it usually shows up as an eyebrow and a heading set too close
at too similar a weight.

**First read, second read.** Name what the eye lands on first, second, third. If that order is not
what the section wants, the composition is wrong regardless of how clean it looks. A good section
also has a **second read**: something that rewards the reader who stays, which is not the same as
something decorative that fills space.

**Asymmetry.** The centred stack is the strongest AI tell in existence because it is what you get
when nothing decided where anything goes. Anchor type to a real edge and offset the visual weight.
One centred element in a composition is a choice; five is an absence of choices.

**Whitespace is structure, not margin.** Space is how the system says "these belong together and
that does not". Uneven space between siblings that are peers is a defect. Equal space between a
heading and its body and between that body and the next heading destroys the grouping entirely :
the gap above a heading should always exceed the gap below it.

**Optical over metric.** Equal numeric padding is not equal-looking padding. Marks, glyphs and
material objects have different ink-to-box ratios. Wings sit optically centred with a slight upward
nudge because that is where they *look* centred, not where the box says they are.

---

## 4 · Typography craft

**Measure.** Cap body at roughly 65 characters, `--mz-content-reading` `720px`. Long measure is the
quiet reason a page feels like homework.

**Leading falls as size rises.** Display sits below 1.0 (`0.91` hero, `0.98` section), headings
1.14 to 1.24, body 1.46 to 1.56. Uniform leading across sizes is the default-metrics tell.

**Tracking falls as size rises, and goes negative.** Hero `-0.064em`, section `-0.052em`, title
`-0.044em`, body around `-0.011em`, and only uppercase labels go positive at `0.09em`. Large type at
zero tracking is the single most recognisable AI heading.

**Weight discipline.** The scale runs 400 to 700 with deliberate intermediate values (650, 670,
680). Use the token weight for the role. Reaching for 800 or 900 to add emphasis means the
hierarchy is not working at the sizes you have.

**Numerals.** Tabular for anything in a column that will be compared, `--mz-type-numeric-tabular`.
Proportional elsewhere. A metrics section uses `--mz-type-numeric-display` with the unit and label
subordinate: the number is the whole point and decoration around it weakens it.

**Wrap.** `text-wrap: pretty` is already on the display roles, and `max-inline-size` in `ch` caps
them. Never hard-break a heading with `<br>` to fix one viewport; it breaks every other viewport.

---

## 5 · Depth and materiality

**The one law: depth is a hierarchy signal, not a finish.** Every shadow, border, bezel and
highlight must answer *what does this tell the reader about where this sits in the stack?* If the
answer is "nothing, it looks nicer", delete it.

Three legitimate jobs:

| Job | What it says | Instrument |
|---|---|---|
| **Separation** | This is a distinct object from what is behind it | `--mz-border-default` hairline |
| **Elevation** | This is temporarily raised, usually by the pointer | `--mz-depth-contact` / `--mz-depth-raised` on interaction |
| **Legibility** | This must survive an unpredictable background | A scrim over material, under text |

Anything else is decoration, and decoration is how a page starts looking generated. The tell is not
"there is a shadow", it is "every box has the same shadow and none of them mean anything". In this
system editorial surfaces are **hairline only**: ambient card shadow was rejected by name.

Testable form: for any element carrying depth, name the job and name the element it separates from
or rises above. Two siblings at the same document level must not carry different elevations.

### The concentric radius rule

When one rounded container sits inside another with padding between them, the curves must be
concentric or the corner gap visibly pinches:

```
R_inner = R_outer − padding
```

Too large and the corners collide. Too small and the gap fattens at the corners, so the object reads
as two unrelated shapes. Human vision is unusually good at spotting this, which is why a mis-nested
radius is one of the fastest ways for a surface to look amateur.

With this system's radius set (4 · 8 · 12 · 16 · 24 · 32) and spacing scale, the legal pairs are:

| Outer | Padding | Inner |
|---|---|---|
| `frame` 32 | 8 · 16 · 20 · 24 | `panel` 24 · `container` 16 · `control` 12 · `compact` 8 |
| `panel` 24 | 8 · 12 · 16 · 20 | `container` 16 · `control` 12 · `compact` 8 · `fine` 4 |
| `container` 16 | 4 · 8 · 12 | `control` 12 · `compact` 8 · `fine` 4 |
| `control` 12 | 4 · 8 | `compact` 8 · `fine` 4 |
| `compact` 8 | 4 | `fine` 4 |

**Fluid containers use the proportional variant.** Express both radii against the same dimension so
they stay concentric at every width, the way the trading card does: outer `7.5cqw`, inset `3cqw`,
inner `4.5cqw`. Exactly concentric from a 120px thumbnail to a full-bleed hero.

---

## 6 · Motion

Motion in this system runs at two levels, and confusing them is the recurring failure.

**Material motion.** The living Deep Mineral core. Alive by default when it is focal, never
controlled by a button, exactly one per viewport, always with an exact static twin for reduced
motion and renderer failure. This is expressive, continuous, and it is the point of the system.

**Interface motion.** `--mz-motion-fast` 120ms and `--mz-motion-default` 180ms on
`cubic-bezier(.2,.7,.2,1)`. A whisper that confirms an action: a control lift, a state change, a
disclosure. Nothing else.

**The allocation question is the design question.** "Which single object is alive here, and why that
one?" is a composition decision, not a technical one. Motion allocation is a feature to show
deliberately, not a footnote. Repeated products, bundle contents and supporting objects stay still
so that the one live thing means something.

**Never moves:** Wings, type, layout position on scroll. Reduced motion holds the whole composition
legible as a still: and a still that is genuinely good, not a broken frame of something else.

---

## 7 · Words

**Register.** Precise, calm, declarative. Concrete nouns over adjectives. The system is confident
enough not to sell.

**Active voice with a real subject.** "Mez Systems runs the business on the systems it sells" beats
"the business is run on systems that are sold".

**Sentence case everywhere**, including headings and buttons. Proper nouns keep their casing.

**CTA semantics are intent, not a verb lottery.** Get for purchase, Join for interest, Explore or
See for discovery, Open for access, Start for onboarding. If none fits, that is a gap to log, not a
prompt to invent a verb.

**One job per element.** A heading makes the claim. The lead adds what the heading could not carry.
A note qualifies. If the lead restates the heading in longer words, cut it.

**Product hierarchy is fixed.** Public name, then extended system name, then the job sentence.

---

## 8 · The accessibility floor

Not a separate pass. These are craft failures when they are wrong.

- **Contrast is measured, never estimated.** Over gradient material, sample the actual lightest and
  darkest pixels under the text rather than averaging the fill. 4.5:1 body, 3:1 for large text and
  for control boundaries.
- **Focus is visible and on-token.** `--mz-focus-ring` at `--mz-focus-width` 3px, `--mz-focus-offset`
  3px. Never removed, never replaced by a colour change alone.
- **Colour is never the only carrier** of a state. Greyscale the render; every state must still read.
- **Targets** clear 44px, or have adequate spacing around them.
- **Reduced motion is a requirement.** The static twin is a designed state, not a degraded one.
- **Reflow at 320px** with no horizontal body scroll, and at 200% zoom.
- **Semantic HTML first.** A heading is a heading. Content survives with JavaScript disabled.

---

## 9 · The habit that matters most

**Look at the render.** Screenshot it, read the image, form the judgement from what you see. The DOM
tells you `font-size: 56px`. Only your eyes tell you the section reads as two competing titles. When
a screenshot and the computed styles disagree, the screenshot wins and the disagreement is itself a
finding.

Every significant failure in this repository's history was written by an agent describing what a page
probably looked like.
