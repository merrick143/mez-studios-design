# 12 · States and forms

Status: DEFAULT · working values, flag deviations to Olli. One declaration below is LOCKED (light-only) and is marked where it appears.

Until now the pack had no interaction states, no form primitives, and no text tokens for dark sections, and the muted text failed WCAG AA. Forms and dark panels are exactly where a build with no rule improvises, so every LLM build has invented its own. This doc closes all four gaps. The values live in the token files as `--mz-error`, `--mz-success`, `--mz-focus-ring` / `--mz-focus-ring-dark`, `--mz-input-border`, `--mz-placeholder` and the `--mz-dark-*` set.

## Button states

The primary CTA is the near-black pill from [07-ui-components.md](07-ui-components.md). These states apply to every button, whether pill or ink.

| State | What changes |
|-------|--------------|
| Rest | The button as specified in [07-ui-components.md](07-ui-components.md). |
| Hover | Lift: `translateY(-2px)` and swap the card shadow for `--mz-shadow-float`. Nothing else moves. |
| Active (press) | Settle back: `translateY(0)`. No new shadow. |
| Focus-visible | A **2px** ring in `rgba(13,13,13,.45)` at **2px** offset. It clears 3:1 against the light surfaces. Keyboard focus only (`:focus-visible`), never on a mouse click. |
| Disabled | `opacity: .4`, `pointer-events: none`. No lift, no ring, no cursor. |

```css
.mz-btn { transition: transform var(--mz-duration) var(--mz-ease), box-shadow var(--mz-duration) var(--mz-ease); }
.mz-btn:hover        { transform: translateY(-2px); box-shadow: var(--mz-shadow-float); }
.mz-btn:active       { transform: translateY(0); }
.mz-btn:focus-visible{ outline: 2px solid var(--mz-focus-ring); outline-offset: 2px; }
.mz-btn:disabled     { opacity: .4; pointer-events: none; }
```

The lift is the only motion. Nothing changes colour on hover: the pill stays near-black, the gradient stays put. Colour is never a state signal here.

## Links

| Property | Value |
|----------|-------|
| Colour | Ink `#0D0D0D` (`--mz-text`). Always. Never a functional or accent colour. |
| Rest | No underline. |
| Hover | The underline appears. That is the whole hover treatment. |
| Focus-visible | The same 2px `rgba(13,13,13,.45)` ring at 2px offset as buttons. |

```css
.mz-link              { color: var(--mz-text); text-decoration: none; }
.mz-link:hover        { text-decoration: underline; }
.mz-link:focus-visible{ outline: 2px solid var(--mz-focus-ring); outline-offset: 2px; }
```

## Inputs

Text inputs, selects and text areas share one primitive.

| Property | Value |
|----------|-------|
| Height | **44px** (single-line controls) |
| Radius | **8px** (`--mz-r-chip`) |
| Background | `#FFFFFF` (`--mz-card`) |
| Border | **1px** `rgba(13,13,13,.45)` (`--mz-input-border`) |
| Focus | Border to ink `#0D0D0D`, plus the focus ring |
| Label | **13px** Inter Medium (500), ink |
| Placeholder | `rgba(46,46,46,.70)` (`--mz-placeholder`) |

The input border is `rgba(13,13,13,.45)`, distinct enough to clear the 3:1 non-text contrast requirement against white and light surfaces. It is intentionally much stronger than the `rgba(13,13,13,.08)` decorative hairline used for cards and dividers (see [01-colour.md](01-colour.md)). On focus the border goes solid ink and the ring joins it. Placeholder text uses the same AA-safe alpha as muted text and clears 4.5:1.

```css
.mz-input {
  height: 44px;
  border-radius: var(--mz-r-chip);
  background: var(--mz-card);
  border: 1px solid var(--mz-input-border);
  padding-inline: 12px;
  color: var(--mz-text);
}
.mz-input::placeholder { color: var(--mz-placeholder); }
.mz-input:focus        { border-color: var(--mz-text); outline: 2px solid var(--mz-focus-ring); outline-offset: 2px; }
.mz-label              { font: 500 13px/1.2 var(--mz-font-sans); color: var(--mz-text); }
```

## Functional colours

Forms and feedback are the one place the monochrome rule bends. Two colours, and only here.

| Token | Hex | Use |
|-------|-----|-----|
| `--mz-error` | `#B42318` | Error text, invalid field borders, destructive confirmation. |
| `--mz-success` | `#15803D` | Success text, confirmed state. |

These are **the sole colour exception besides the product gradients** (see [01-colour.md](01-colour.md)). They never appear as decoration, a background, a heading colour or a brand accent: only to tell the user what happened in a form or a system message. Status: DEFAULT, flag to Olli.

## Dark-surface text

Dark sections (`#0D0D0D` panels, the bundle container, dark UI) had no text tokens, so builds guessed at greys. Here is the set, on `#0D0D0D`.

| Token | Value | Role |
|-------|-------|------|
| `--mz-dark-text` | `#FFFFFF` | Primary text on dark. |
| `--mz-dark-text-2` | `rgba(255,255,255,.64)` | Secondary text on dark. |
| `--mz-dark-muted` | `rgba(255,255,255,.45)` | Muted text, captions and meta on dark. |
| `--mz-dark-border` | `rgba(255,255,255,.14)` | Hairlines and borders on dark. |
| `--mz-focus-ring-dark` | `rgba(255,255,255,.5)` | Focus ring on dark surfaces. |

On dark the focus ring flips to `--mz-focus-ring-dark` (white at 50%) so it reads against the near-black. On light surfaces the ring stays `--mz-focus-ring` (`rgba(13,13,13,.45)`), the default. Same 2px width, same 2px offset, both sides.

## Light-only

> **LOCKED · 17 JUL 2026. The site is light-only.** Dark is a section treatment, not a theme. There is one light system (see [01-colour.md](01-colour.md)); a `#0D0D0D` band is a deliberate dark section inside a light page, drawn with the dark-surface tokens above. `prefers-color-scheme` handling is forbidden: no dark-mode media query, no theme toggle, no auto-inverting surfaces. A build that ships a dark theme is off-system.

## Accessibility: muted text raised to AA

`--mz-text-muted` was the ink grey at `.58` alpha, about 3.4:1 on the `#F8F8F8` page: below the WCAG AA floor of 4.5:1 for body text. It is now `rgba(46,46,46,.70)`, about 4.6:1, which passes AA. The value changed in the token files and in [01-colour.md](01-colour.md), and the change is logged in [09-governance.md](09-governance.md). Captions, meta and function labels all inherit the fix with no further edits.

## The rule

> **States are motion and ink, not new colour.** Buttons lift, links underline, inputs darken their border, and focus draws a ring. The only colour that ever enters is a functional `--mz-error` or `--mz-success` inside a form or a message, or a product gradient. Everything else stays monochrome, and the page stays light.

## Tokens (machine readable)

```json
{
  "button": {
    "hover": { "transform": "translateY(-2px)", "shadow": "--mz-shadow-float" },
    "active": { "transform": "translateY(0)" },
    "focusVisible": { "ring": "rgba(13,13,13,.45)", "width": 2, "offset": 2 },
    "disabled": { "opacity": 0.4, "pointerEvents": "none" }
  },
  "link": {
    "colour": "#0D0D0D",
    "underline": "hover-only",
    "focusVisible": { "ring": "rgba(13,13,13,.45)", "width": 2, "offset": 2 }
  },
  "input": {
    "height": 44,
    "radius": 8,
    "background": "#FFFFFF",
    "border": "rgba(13,13,13,.45)",
    "focusBorder": "#0D0D0D",
    "label": { "size": 13, "family": "Inter", "weight": 500 },
    "placeholder": "rgba(46,46,46,.70)"
  },
  "functional": {
    "$note": "Forms + feedback ONLY. The sole colour exception besides product gradients.",
    "error": "#B42318",
    "success": "#15803D"
  },
  "darkSurface": {
    "$note": "On #0D0D0D. A section treatment, never a theme.",
    "text": "#FFFFFF",
    "text2": "rgba(255,255,255,.64)",
    "muted": "rgba(255,255,255,.45)",
    "border": "rgba(255,255,255,.14)",
    "focusRing": "rgba(255,255,255,.5)"
  },
  "focusRing": {
    "$note": "--mz-focus-ring carries the light value (default); --mz-focus-ring-dark carries the dark value.",
    "light": "rgba(13,13,13,.45)",
    "dark": "rgba(255,255,255,.5)",
    "width": 2,
    "offset": 2
  },
  "lightOnly": {
    "status": "LOCKED",
    "date": "2026-07-17",
    "rule": "Site is light-only. Dark is a section treatment, not a theme. prefers-color-scheme handling forbidden."
  },
  "accessibility": {
    "focusIndicator": { "contrastOnLight": ">=3:1", "token": "--mz-focus-ring" },
    "inputBoundary": { "contrastOnLight": ">=3:1", "token": "--mz-input-border" },
    "placeholder": { "contrastOnLight": ">=4.5:1", "token": "--mz-placeholder" },
    "textMuted": {
      "wasAlpha": 0.58,
      "now": "rgba(46,46,46,.70)",
      "contrastOn": "#F8F8F8",
      "ratio": "~4.6:1",
      "standard": "WCAG AA"
    }
  }
}
```
