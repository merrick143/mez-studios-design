# 11 · Layout and grid

Status: DEFAULT · working values, flag deviations to Olli

Until now the pack had no page geometry: no container width, no breakpoints, no section rhythm, so every build invented its own. This doc ends that. One container, three named breakpoints, one vertical rhythm. The numeric values also live in the token files as `--mz-container`, `--mz-gutter`, `--mz-gutter-lg`, spacing steps 9 to 11, and `breakpoints` in tokens.json.

## Container

| Property | Value |
|----------|-------|
| Max width | **1160px** (`--mz-container`) |
| Alignment | Centred (`margin-inline: auto`) |
| Gutter, below 920 | **24px** (`--mz-gutter`) |
| Gutter, 920 and up | **32px** (`--mz-gutter-lg`) |

Why 1160: it fits a 1280 laptop with gutters to spare (1160 + 2 × 32 = 1224), holds the four-card suite grid at a workable card size, and keeps a single text column from stretching past a readable measure.

```css
.mz-container { max-width: var(--mz-container); margin-inline: auto; padding-inline: var(--mz-gutter); }
@media (min-width: 920px) { .mz-container { padding-inline: var(--mz-gutter-lg); } }
```

## Breakpoints

Three, min-width, named. No others.

| Name | Width | Crossing it |
|------|-------|-------------|
| `sm` | 600px | Mobile → tablet. |
| `md` | 920px | Tablet → desktop. Columns come back, gutter widens to 32, section padding steps up. |
| `lg` | 1200px | Desktop → wide. Suite grid goes four-up; the container reaches its max. |

Why these: 600 is where phones end, 920 is the first width where two real columns plus gutters carry the type scale comfortably, 1200 is the first width where four product cards sit inside 1160 without crowding.

CSS custom properties cannot drive `@media` queries. Use the raw px values in queries and keep them in sync with `breakpoints` in [tokens.json](../tokens/tokens.json).

## Section rhythm

| Padding | Below 920 | 920 and up |
|---------|-----------|------------|
| Section vertical | **72px** | **120px** (`--mz-s-10`) |
| Hero top | **96px** (`--mz-s-9`) | **140px** |

Why: desktop sections breathe at a full section step (120); mobile takes 60% of that so pages do not scroll forever. The hero opens the page, so it gets extra headroom above every other section.

## Spacing scale · section steps

The component scale (`--mz-s-1` to `--mz-s-8`, see [07-ui-components.md](07-ui-components.md)) stops at 64. Three **section steps** extend it for page rhythm:

| `--mz-s-9` | `--mz-s-10` | `--mz-s-11` |
|-----|-----|-----|
| 96 | 120 | 160 |

Steps 1 to 8 belong inside components; steps 9 to 11 belong between sections. Never invent a value in between.

## Type at small widths

| Role | Rule |
|------|------|
| h1 | Already fluid: `clamp(2.75rem, 6vw, 4.5rem)` (`--mz-h1-size`, unchanged, see [03-typography.md](03-typography.md)). |
| h2 | Fluid on the web layer: `clamp(1.75rem, 4.5vw, 2.5rem)`. It caps at the locked 2.5rem desktop size at and above the `md` breakpoint. |
| body | Does not scale with the viewport: **16px** below `md`, **17px** (`--mz-body-size`) at `md` and up. Never smaller than 16. |

Fluid h2 caps at the locked token size (2.5rem) so one role has one number. DEFAULT: flag to Olli if a larger web h2 is wanted.

## Stacking

- Multi-column sections (text + media splits, comparison rows) stack to **one column below 920**, in **source order**. Never reorder on stack: if a section reads wrong stacked, fix the source order.
- The **suite grid** (AI OS · Aurora · Prism · Forge, see [05-product-system.md](05-product-system.md)) runs its own ladder down the breakpoints, 4 → 2 → 1: **four** columns at `lg` (1200), **two** at `md` (920), **one** below that, through `sm` (600) and under.

## The rule

> **One geometry.** Every page uses the 1160 container, the three named breakpoints, and the section rhythm above. A build that invents its own container width, breakpoint, or section padding is off-system.

## Tokens (machine readable)

```json
{
  "layout": {
    "container": 1160,
    "gutter": { "base": 24, "lg": 32, "switchAt": 920 },
    "breakpoints": { "sm": 600, "md": 920, "lg": 1200 },
    "sectionPaddingY": { "base": 72, "md": 120 },
    "heroPaddingTop": { "base": 96, "md": 140 },
    "spaceSectionSteps": { "9": 96, "10": 120, "11": 160 },
    "type": {
      "h1": "clamp(2.75rem, 6vw, 4.5rem)",
      "h2": "clamp(1.75rem, 4.5vw, 2.5rem)",
      "bodyPx": { "base": 16, "md": 17 }
    },
    "stacking": {
      "stackBelow": 920,
      "order": "source",
      "suiteGridColumns": { "lg": 4, "md": 2, "base": 1 }
    }
  }
}
```
