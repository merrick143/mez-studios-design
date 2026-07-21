# 16 · Motion

Status: DEFAULT · working values, flag deviations to Olli

Without a motion rule every build invents its own physics: a different duration on every hover, a spring here, a scroll-reveal there. This doc closes that with the smallest possible spec. One duration, one easing, hover only, plus one named continuous exception for the living core. Motion here is a whisper that confirms an action, never a feature that asks for attention.

## Duration and easing

| Token | Value | Use |
|-------|-------|-----|
| `--mz-duration` | 200ms | The default. Button hover lift, card hover shadow, link underline, focus ring. |
| `--mz-duration-slow` | 280ms | The two larger moves only: accordion open/close and the mobile nav sheet. |
| `--mz-ease` | `cubic-bezier(.2,.7,.2,1)` | Every transition, both durations. One curve, no exceptions. |

These formalise the `.15s ease` placeholder written into [12-states-and-forms.md](12-states-and-forms.md) and [13-sections.md](13-sections.md) before this doc existed: those transitions now resolve to `var(--mz-duration) var(--mz-ease)`. Use the tokens, not a literal duration.

## What animates

Five things move. Four match the states in [12-states-and-forms.md](12-states-and-forms.md) and the sections in [13-sections.md](13-sections.md). The fifth is the product-only living-core exception in [20-living-core.md](20-living-core.md).

| What | Change | Duration |
|------|--------|----------|
| Button hover lift | `transform: translateY(-2px)` and the shadow swaps `--mz-shadow-card` to `--mz-shadow-float`. | `--mz-duration` |
| Card hover shadow | `box-shadow` deepens `--mz-shadow-card` to `--mz-shadow-float`. Shadow only, no lift. | `--mz-duration` |
| Accordion open/close | The answer body opens and the ink chevron rotates. One open at a time ([13-sections.md](13-sections.md) · FAQ). | `--mz-duration-slow` |
| Mobile nav sheet | The links sheet reveals behind the menu toggle; the CTA pill stays put ([13-sections.md](13-sections.md) · Nav). | `--mz-duration-slow` |
| Living core | Continuous shader motion on a product core only. Hover may accelerate the fluid to 1.85×, with no scale or geometry change. | Continuous, exempt from `--mz-duration` |

```css
.mz-btn   { transition: transform var(--mz-duration) var(--mz-ease), box-shadow var(--mz-duration) var(--mz-ease); }
.mz-card  { transition: box-shadow var(--mz-duration) var(--mz-ease); }
.mz-accordion__panel,
.mz-accordion__chevron { transition: all var(--mz-duration-slow) var(--mz-ease); }
.mz-nav__sheet         { transition: transform var(--mz-duration-slow) var(--mz-ease); }
```

Nothing changes colour on hover: the button pill stays near-black, links only add an underline ([12-states-and-forms.md](12-states-and-forms.md)). Colour is never an animated signal.

## What never animates

- **Gradient fills.** A gradient used as a fill never shifts, pulses, rotates or drifts. The sole exception is the living core ([20-living-core.md](20-living-core.md)), which is a rendered product treatment, not a fill.
- **Text.** No typewriter, no word-by-word fade, no counting numbers. Text is set at load.
- **Layout position on scroll.** No scroll-reveal, no fade-up-on-enter, no parallax. Every section is fully present the moment it renders ([13-sections.md](13-sections.md)).
- **Static discs.** A static disc never spins, floats or breathes. A disc rendered as a living core is governed by [20-living-core.md](20-living-core.md).

## Reduced motion

`prefers-reduced-motion: reduce` disables all transforms. Every transition and animation collapses to instant, and the two transform moves (the button lift and the chevron rotate) are cancelled outright, so state still changes but nothing travels. Paste this once at the app root.

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    transition-duration: 0.01ms !important;
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    scroll-behavior: auto !important;
  }
  .mz-btn:hover, .mz-btn:active { transform: none !important; }
  .mz-accordion__chevron        { transform: none !important; }
}
```

The accordion still opens and the sheet still shows, they just arrive without the ease. The shadow swap and the link underline stay, since neither is a transform and neither triggers motion sensitivity.

A living core does not freeze on an arbitrary shader frame under reduced motion. It is replaced by its defined static WebP twin. The static twin is also mandatory when WebGL is unavailable.

## The rule

> **One duration, one easing, hover only, plus the living core.** 200ms on `cubic-bezier(.2,.7,.2,1)`, or 280ms for the accordion and the mobile sheet. Buttons lift, cards deepen their shadow, the accordion and sheet open. Gradient fills, text, scroll position and static discs never move. A moving gradient is off-system unless it is a living core governed by doc 20. `prefers-reduced-motion: reduce` replaces every living core with its static twin and cancels every other transform.

## Tokens (machine readable)

```json
{
  "motion": {
    "status": "DEFAULT",
    "duration": { "default": "200ms", "slow": "280ms", "$note": "slow = accordion + mobile nav sheet only" },
    "ease": "cubic-bezier(.2,.7,.2,1)",
    "tokens": {
      "--mz-duration": "200ms",
      "--mz-duration-slow": "280ms",
      "--mz-ease": "cubic-bezier(.2,.7,.2,1)"
    },
    "animates": [
      { "what": "button-hover-lift", "change": "translateY(-2px) + shadow card->float", "duration": "--mz-duration" },
      { "what": "card-hover-shadow", "change": "box-shadow card->float", "duration": "--mz-duration" },
      { "what": "accordion", "change": "body open + chevron rotate", "duration": "--mz-duration-slow" },
      { "what": "mobile-nav-sheet", "change": "sheet reveal", "duration": "--mz-duration-slow" },
      { "what": "living-core", "change": "continuous product-core shader; hover speed 1.85x; no scale", "duration": "continuous" }
    ],
    "neverAnimates": ["gradient-fills", "text", "layout-position-on-scroll", "static-discs"],
    "continuousException": { "treatment": "living-core", "scope": "product cores only", "ref": "20-living-core.md" },
    "reducedMotion": {
      "query": "prefers-reduced-motion: reduce",
      "effect": "living cores become their static twins; all other transitions and animations are instant; transforms cancelled"
    },
    "supersedes": "The '.15s ease' placeholder in 12-states-and-forms.md and 13-sections.md now resolves to var(--mz-duration) var(--mz-ease)."
  }
}
```
