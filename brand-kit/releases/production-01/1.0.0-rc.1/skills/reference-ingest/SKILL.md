---
name: reference-ingest
description: Turn a design Olli likes into a reusable Mez principle. Use when he sends screenshots of website sections, says "use these as inspo", "reverse-engineer this", "I like how this looks", or shares a URL to study. Produces a design-language study in brand-kit/references/ that climbs the abstraction ladder, so the influence becomes a principle rather than a copy. Run this BEFORE designing the section the reference was sent for.
---

# Reference ingest

Olli specifies taste by sending screenshots. This turns one into something the system can reuse.

**The whole job is crossing the gap between "I like this" and "here is what to build" in writing,
once, so the next agent does not reach for the screenshot and reproduce it.**

## When this runs

Trigger on: screenshots of website sections, "use these as inspo", "reverse-engineer this",
"I have screenshots of good design", "study {url}", or a pasted image alongside a design request.

Run it **before** building the section it was sent for. A reference ingested after the fact is a
justification, not an input.

## Non-negotiables

- **Never build the reference.** The output of this skill is a study, not a section. If the same
  turn is also meant to produce a design, the study lands first and the design cites it.
- **Never lift values.** Measurements are evidence of what the source did. They never enter a Mez
  token file.
- **Never commit captures.** Screenshots go to the scratchpad and are cited by filename.
- **A named question, or no folder.** "Interesting" is not a reason.

Read `brand-kit/references/README.md` for the abstraction ladder and the originality-risk scale
before starting.

---

## Steps

### 1 · Frame it

One line: the Mez problem, the specific question, the section or expression it serves. Then fix the
slug: lowercase, hyphenated, source first then surface. Check `REGISTRY.md` for an existing row on
this source; if the source has changed, recapture in place and bump the date rather than creating
`{slug}-v2`.

If Olli sent several screenshots at once, decide whether they are **one** study (variations on one
device) or **several** (different mechanisms). Several weak studies beat one that averages them into
mush.

### 2 · Look, properly

Read every image with your own vision, before writing a word.

Record, per reference:

- What you see first, second, third: and whether that order is what the design wants
- Where it is dense and where it is empty, and what triggers each change
- The proportion of the parts: what fraction of the width does the dominant element take
- What carries colour, what carries weight, what carries the argument
- **One thing that is genuinely unusual**: this is usually the reason he sent it
- What you would lose if you deleted each element in turn

If Olli said what he liked about it, that sentence outranks your reading. Quote it in the study.

### 3 · If there is a live URL, measure it

Optional, and only when a URL exists. Screenshots alone are enough for a valid study.

Serve nothing; navigate with the browser tools, capture at 1440 and 390, and pull the rendered
census: computed type roles by area coverage, the radius set actually used, the shadow set, the
grid columns, the section padding rhythm. Keep per-page results separate so a system value can be
told apart from a one-off: that separation is the entire reason to visit more than one page.

Dismiss cookie banners by declining non-essential before capturing.

### 4 · Climb the ladder

Fill `brand-kit/references/_template/design-language.md` into `brand-kit/references/{slug}/`.

The four rungs are the point. The tests:

- **Rung 2 passes** if someone who has never seen the screenshot could explain why the design works
  from your paragraph alone.
- **Rung 3 passes** if the principle survives being restated without the source's colours and
  typefaces. If it does not, it was an observation, not a principle. Go back.
- **Rung 4 is mandatory** and must name a composition family from `design-authority/CRAFT.md` §1,
  the protagonist, and a translation table for every element that cannot travel as-is.

Translation is where most of the value is. Work through the canon: the source's saturated accent
becomes monochrome or product material (`COL-06`, `COL-10`); its ambient glow is dropped
(`MAT-02`, `MAT-03`); its glass becomes an opaque surface (`MAT-01`); its brand logos come from
`brand-kit/assets/third-party-marks/` or the slot is cut (`ICO-01`); its pure black becomes the
charcoal ramp (`COL-05`).

### 5 · Section 5 is not optional

"What not to take" is what stops the next agent copying. Name the parts that are the source's
signature. If the originality risk is High, this section is the reason the study is safe to keep.

### 6 · Register it

Add the row to `REGISTRY.md`, newest first. Mark `Provided by` as `Olli, screenshot` when it came
from him: those are the highest-value inputs in the system and worth being able to find.

### 7 · Report back in three sentences

Not the whole study. Olli needs: the principle you extracted, what it becomes in Mez, and the one
thing you are deliberately not taking. If the study surfaced a taste call, ask it now as a bounded
question rather than deciding it.

---

## Output contract

- Files changed: `brand-kit/references/{slug}/design-language.md`, `brand-kit/references/REGISTRY.md`
- Status: **research**
- Production authority: **false**
- Never modifies: foundations, registry, releases, approved grammar

## The failure this prevents

Golden Homepage rounds 15 and earlier were rejected repeatedly on direction. R17 landed because
reference screenshots supplied the missing taste specification: and it landed *correctly* because
the polish was translated rather than transferred: the SaaS status-green became a monochrome badge,
the ambient glow was dropped, the invented AI logos were killed for good.

An ingest that skips rung 4 produces the other outcome: someone else's section wearing Mez tokens.
