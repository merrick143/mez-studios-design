# Reference library

Outside design that has been studied so an agent can answer a specific design question with evidence
instead of taste-by-vibes.

Status: **research evidence**. A reference can never create Mez truth. Nothing here is canonical,
nothing here is a component, and no value recorded here is ever permitted into
`brand-kit/foundations/`, `brand-kit/registry/` or a release.

## Why this exists

Olli specifies taste by sending screenshots of sections he likes. That is his most reliable channel
and it has worked: Golden Homepage R17 landed because reference screenshots supplied the direction
that four described rounds could not.

It also has a failure mode. A screenshot can be copied instead of understood, and the result is
someone else's page wearing Mez tokens. The library exists to force the gap between "I like this"
and "here is what to build" to be crossed **in writing**, once, in a form the next agent can reuse.

## The abstraction ladder

Every influence climbs all four rungs. A study that stops at rung one is a copy with extra steps.

| Rung | Question | Example |
|---|---|---|
| 1 · **Observed expression** | What is literally on screen? | A two-column card: light editorial half, dark half with a green status pill and an ambient glow |
| 2 · **Underlying mechanism** | What makes it work? | The dark half is a *different register*, not a different colour. Contrast of register signals "claim" beside "the thing itself" |
| 3 · **Transferable principle** | What is the rule, free of this brand? | A split card can carry an argument and its evidence at once if the two halves differ in register, not merely in tone |
| 4 · **Original Mez expression** | What does that become here? | The authored split family: light editorial half beside a charcoal generative half carrying a bespoke per-section device. Green → monochrome badge. Glow → dropped. Hairlines only |

**Rung 4 is mandatory.** A study without it is unfinished, and it is exactly the state in which an
agent reaches for the screenshot and reproduces rung 1.

## What must never be stored

- **Copied values.** Do not lift a hex, a radius, a shadow or a type scale into a Mez token file.
  Recorded measurements are evidence of what the source did, never a proposal for what Mez does.
- **Competitor screenshots committed to the repository.** Captures live in the scratchpad and are
  cited by filename. The study is the artefact; the image is not.
- **A study with no question.** "Interesting" is not a reason. No named question, no folder.
- **Brand logos or assets from the source.** Those come from
  `brand-kit/assets/third-party-marks/` if they are needed at all.

## Folder shape

```
brand-kit/references/
  README.md          this file
  REGISTRY.md        the index, one row per study
  _template/
    design-language.md
  <slug>/
    design-language.md
```

Slug is lowercase and hyphenated, source first then surface: `opentofu-feature-card`, not
`nice-card-2`. No dates in slugs. Once a row lands, the slug is final: renaming breaks citations.

## Originality risk

Every study records one.

| Level | Meaning | Consequence |
|---|---|---|
| **Low** | The mechanism is a general principle already common in good design | Absorb directly |
| **Medium** | The mechanism is distinctive but separable from its expression | Any Mez output influenced by it names the reference in its round record |
| **High** | The expression is a signature of the source; a close reading would recognise it | Must be re-expressed, and the influence stated explicitly in the Gate B review. Never ship an untouched transfer |

## Precedence

When a reference and the approved Mez grammar disagree, **the grammar wins**. Always. A reference is
an argument for a change, never the change itself, and any change to approved grammar is Olli's
decision as a bounded packet.
