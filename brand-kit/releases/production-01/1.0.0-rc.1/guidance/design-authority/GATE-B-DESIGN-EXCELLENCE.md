# Gate B · design-excellence review

The scored review that decides whether a build is **excellent**, not merely compliant.

## Gate A is not yours

Deterministic compliance belongs to the verifiers: `verify_portability.py`,
`verify_llm_contracts.py`, `verify_workbench.py`, `verify_library.py`, `verify_architecture.py`,
`verify_authority.py`, `verify_release.py` and the per-round expression verifiers. Schemas, token
parity, hashes, contrast assertions, overflow, link validity and naming are theirs. Do not duplicate
them. If a Gate A item has leaked through, log it as a one-line Gate A leak note, not as a Gate B
finding.

**Gate A passing tells you nothing about whether the work is good.** That sentence is this gate's
whole mandate. Product Card rounds 01 to 06 passed compliance and were rejected as vibe-coded.

## Before scoring

Read, in order:

1. `brand-kit/docs/PRODUCT-CARD-DESIGN-ETHOS.md`: the approved visual grammar and the rejection list
2. `brand-kit/docs/PHASE-B-COMPONENT-PANTRY.md`: if any component is in scope
3. [`ANTI-SLOP-CANON.md`](ANTI-SLOP-CANON.md): so you cite IDs rather than adjectives
4. [`CRAFT.md`](CRAFT.md) §1: so you can name the composition family of every section
5. The round's own feedback records under `brand-kit/golden/` or `brand-kit/expressions/<name>/`

Never score against remembered values. Pull the real ones from
`brand-kit/foundations/*/dist/tokens.css`.

---

## Step 1 · Render and look

Serve the workbench:

```bash
.venv/bin/python brand-kit/server.py --port 8914
```

Capture the surface at **320, 375, 390, 768, 920, 1280, 1440**. Full page at every width, plus a
first-viewport capture at 375 and 1440 for above-the-fold judgement.

**Then read every image with your own vision.** Saving a PNG is not the step; looking at it is. A
score written without having read the captures is void.

**Capture pitfalls on this machine.** Playwright viewport screenshots at scroll offsets return stale
composited frames when a live WebGL core is on the page, and the browser pane serves stale frames
when hidden. Use element screenshots (`target: '#section'`) or DOM geometry probes instead.

If you cannot render, say so plainly and stop. An honest "cannot verify visually" beats a fabricated
score.

---

## Step 2 · The four named tests

Each can block the gate on its own. Run them before scoring.

### T1 · Distinctiveness: strip the material, is it still Mez?

At 1280 and 375, neutralise every gradient and greyscale the page, then capture:

```js
document.querySelectorAll('*').forEach(el => {
  if ((getComputedStyle(el).backgroundImage || '').includes('gradient')) {
    el.style.backgroundImage = 'none';
    el.style.backgroundColor = '#2E2E2E';
  }
});
document.documentElement.style.filter = 'grayscale(1)';
```

Read the stripped captures and ask one question: **is any composition device left that is specific to
Mez?** Authored splits, apertures, rails, plates, cropped Wings geometry, the charcoal-beside-light
pairing, recurring alignment behaviour. If what remains is a sans-serif on off-white with rounded
white cards and dark pill buttons, the identity lives entirely in the gradients. That is a **blocking
distinctiveness failure**. Name the device you found, or state that you found none.

### T2 · Repetition: do sections differ in composition or only in copy?

Dump the composition skeleton of every section:

```js
[...document.querySelectorAll('section')].map(s => {
  const m = s.querySelector('img, video, svg, canvas, [data-mz-core]');
  return {
    id: s.id,
    h: Math.round(s.getBoundingClientRect().height),
    cols: getComputedStyle(s.querySelector('[class*=grid],[class*=split]') || s).gridTemplateColumns,
    media: !!m,
    mediaSide: m ? (m.getBoundingClientRect().left > innerWidth / 2 ? 'right' : 'left') : null
  };
});
```

Then assign a composition family to each from `CRAFT.md` §1 and apply the adjacency, frequency,
density and alternation tests. Two consecutive sections sharing a family is a **blocking** finding.

### T3 · Motion truth: is the live thing actually alive?

Never accept canvas count as proof. Wrap the GL draw calls and count them, **and** diff two element
screenshots several seconds apart. Expect more than 10% changed pixels on a live surface. Then
confirm exactly one `data-mz-core`, and that reduced motion resolves to the exact static twin with
no layout shift.

### T4 · Product truth: is the protagonist actually present?

Every proof slot must contain the real thing: real material, real registry content, real output. A
grey placeholder, a fabricated number or an invented logo fails this test outright, and it fails the
canon at `MAT-05`, `CPY-02` or `ICO-01` as well.

---

## Step 3 · Score the eleven dimensions

1 to 5 each. 3 means competent and unremarkable. 4 means genuinely good. 5 means this is the
reference other work gets held to.

| # | Dimension | 5 looks like |
|---|---|---|
| 1 | **Hierarchy** | First, second and third read are exactly what the section wants. One focal point, established by one device. |
| 2 | **Composition** | The family fits the argument. Asymmetry is authored. Space groups correctly. Nothing sits where it landed. |
| 3 | **Pacing and density** | The information rate changes deliberately down the page. No two neighbours share a shape. |
| 4 | **Typography** | On-role, on-scale, correct measure. Tracking and leading do their work. The type alone carries the register. |
| 5 | **Product truth and proof** | Real material, real data, real output, count-independent. The protagonist is unmistakable. |
| 6 | **Distinctiveness** | Passes T1 with a named device. Could not be another company's page with the logo swapped. |
| 7 | **Narrative** | The section makes one argument, and the composition is that argument rather than a container for it. |
| 8 | **Conversion clarity** | The action is obvious, singular, correctly worded, and reachable at 375. |
| 9 | **Emotional impact** | Precise, calm, intelligent, materially alive. It rewards a second look. |
| 10 | **Craft** | Concentric radii, optical alignment, honest depth, clean reflow at 320, no orphans. |
| 11 | **Originality** | Influences ran through the abstraction ladder. Nothing is a transfer of a studied source. |

**Weighting.** Dimensions 1, 2, 5 and 6 count double. Everything else counts once. Maximum 75.

| Score | Verdict |
|---|---|
| ≥ 64 and no blocking failure and no dimension below 3 | **Pass**: ready for Olli's review |
| 52 to 63 | **Revise**: named, bounded changes, then re-score |
| < 52, or any blocking failure, or any dimension at 1 | **Fail**: the direction is wrong, not the polish |

### Blocking failures

Regardless of score:

- Any T1 to T4 test failed
- Any canon **CRITICAL**
- Any dimension scored 1
- A default cluster (CL-01 to CL-04) named
- Motion claimed but not proven, or a second live core
- Any element that cannot survive reduced motion or JavaScript disabled

---

## Step 4 · Report

Lead with the verdict. Score before reasoning.

```
VERDICT: Revise · 57/75 · no blocking failures

Rubric      hierarchy 4 · composition 3 · pacing 3 · typography 4 · product truth 4
            distinctiveness 2 · narrative 3 · conversion 4 · emotional 3 · craft 4 · originality 4

T1 distinctiveness  PASS (weak). The authored split survives greyscale, but only just.
                    The dark half is the only Mez-specific device on the page
T2 repetition       FAIL: GH-S03 and GH-S04 are both authored split, adjacent
T3 motion           PASS: 61 draw calls in 3s, 18% pixel delta, one data-mz-core
T4 product truth    PASS

FINDINGS
CRITICAL  LAY-02  GH-S04 centres eyebrow, heading, lead and chip row on one axis
                  → workbench/golden/homepage/index.html:ּ612
MAJOR     MAT-03  .split-card carries --mz-depth-raised; editorial surfaces are hairline only
MINOR     TYP-09  Two Instrument Serif phrases in GH-S03

SMALLEST SET OF CHANGES THAT MOVES THE GRADE
1. Change GH-S04's family from authored split to workflow sequence (fixes T2, +2 composition)
2. Left-anchor the GH-S04 stack and offset the visual (fixes LAY-02, +1 hierarchy)
3. Drop the shadow to hairline (fixes MAT-03)

FOR OLLI (taste, not defect)
Whether the S02 dark-half device should read as fragmentation or as containment.
Two options, both rendered, at <path>. Recommendation: containment, because …
```

**Every finding names the file, the element and the observable problem.** "The hierarchy is weak" is
not a finding. "The H2 sits 4px from a 28px eyebrow at similar weight, so the section reads as two
competing titles" is.

**Separate defects from taste calls.** A defect is objectively wrong and it routes back to the
builder. A taste call is Olli's, and it goes to him as a bounded packet: the decision, why now, at
most three meaningfully different options, a recommendation with reasoning, each shown on a real
render. Never hand him a folder of experiments and ask what he thinks.

**Never ship a "looks fine" review.** If you find nothing wrong, say what you checked and what would
have had to be true for it to fail. A review with no findings and no method is worthless.

---

## Where reviews are written

Round feedback belongs beside the work it judges, following the existing convention:

- `brand-kit/golden/homepage/round-NN-feedback.json`
- `brand-kit/expressions/<name>/round-NN-feedback.json`

A Gate B run that precedes Olli's review is an **agent** record and must say so: `"verdict":
"gate-b"`, `"productionAuthority": false`. It never overwrites, pre-empts or paraphrases his
verdict. Only Olli's own keep/revise/kill goes in as his.
