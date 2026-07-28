---
name: design-critique
description: Score a Mez surface for design excellence before Olli sees it. Use when a round candidate is built and needs judging, when asked "is this good", "is this AI slop", "review this section", "run Gate B", or before presenting any visual work for review. Renders the surface, looks at it, sweeps the anti-slop canon, runs the four named tests, and returns a scored verdict with the smallest set of changes that would move the grade.
---

# Design critique · Gate B

Judge a Mez surface the way Olli would, before it costs him a round.

**The mandate in one sentence: passing compliance does not imply excellent design.** Every verifier
in this repository can be green on work that is rejected on sight.

## When this runs

- A round candidate is built and not yet shown to Olli
- "Is this good", "is this slop", "review this", "score it", "run Gate B"
- Before any visual work is presented for review
- Reviewing work another agent produced

**Do not run it as reassurance.** If the honest answer is that the direction is wrong, say so; that
is cheaper than Olli discovering it.

## Read first

1. `brand-kit/design-authority/GATE-B-DESIGN-EXCELLENCE.md`: the full procedure and rubric
2. `brand-kit/design-authority/ANTI-SLOP-CANON.md`: so findings cite IDs, not adjectives
3. `brand-kit/design-authority/CRAFT.md` §1: so you can name every section's composition family
4. `brand-kit/docs/PRODUCT-CARD-DESIGN-ETHOS.md`: the approved grammar and rejection list
5. The round's own feedback records beside the work

## The procedure

Follow `GATE-B-DESIGN-EXCELLENCE.md`. In short:

1. **Render.** `.venv/bin/python brand-kit/server.py --port 8914`. Capture at 320, 375, 390, 768,
   920, 1280, 1440.
2. **Look.** Read every capture with your own vision. A score written without reading the images is
   void, and this is the most-broken rule in the repository's history.
3. **Run the four tests.** T1 distinctiveness (strip the material, is it still Mez), T2 repetition
   (composition families, adjacency), T3 motion truth (draw calls and pixel delta, not canvas
   count), T4 product truth (real material, real data, no placeholders).
4. **Sweep the canon** in ID order.
5. **Score eleven dimensions**, 1 to 5. Hierarchy, composition, product truth and distinctiveness
   count double. Max 75.
6. **Report** verdict first, then the rubric, then findings with file and element, then the smallest
   ranked set of changes.

## Capture pitfalls on this machine

- Playwright viewport screenshots at scroll offsets return **stale composited frames** when a live
  WebGL core is on the page. Use element screenshots (`target: '#section'`) or DOM geometry probes.
- The browser pane serves stale frames when hidden.
- Never accept canvas count as animation proof. Wrap `drawArrays`/`drawElements` and count calls,
  and diff two element screenshots seconds apart: expect >10% changed pixels on a live surface.

## Blocking failures

Regardless of score: any named test failed, any canon CRITICAL, any dimension at 1, a default
cluster identified, motion claimed but unproven, a second live core, or anything that dies under
reduced motion or with JavaScript disabled.

## Defects versus taste calls

**Defect:** objectively wrong against the canon or an approved decision. Route it back to the
builder and fix it.

**Taste call:** Olli's. Never decide one silently. Route it as a bounded packet: the decision, why
now, at most three meaningfully different options, your recommendation with reasoning, each shown on
a real render, and a clear response format. Never hand him a folder of experiments and ask what he
thinks.

## Recording

A Gate B run before Olli's review is an **agent** record. Write it beside the work as
`round-NN-feedback.json` with `"verdict": "gate-b"` and `"productionAuthority": false`. It never
overwrites or pre-empts his verdict; only his own keep/revise/kill is recorded as his.

## Never ship a "looks fine" review

If you find nothing wrong, state what you checked and what would have had to be true for it to fail.
A review with no findings and no method is worthless.
