# Mez Systems: Brand System

The canonical written guidance for the **Mez Systems** brand. Mez Systems is the digital-products holdco that sits inside the parent company **Mez Studios**. Products it holds: AI OS, Aurora (Auto Ads System), Prism (Analytics Pack), Forge (Claude Code OS), plus the wider product ladder.

Approved decisions and canonical data live above this folder in `governance/decision-register.json`, `products.json`, `colours.json`, `fonts.json`, and `gradients.json`. The full precedence and conflict rules live in `governance/authority-model.json`. Figma is a milestone mirror and human exploration surface. Update the owning pack source first, then update Figma and note the mirror pass in [09-governance.md](09-governance.md).

- **Figma file:** `HU0GVaDhatjWrKCiSg3wlU` ("Mez Systems - branding")
- **Milestone mirror page:** "Mez Systems — Brand System" (node `149:30`)
- Node-by-node map of every board: [08-figma-map.md](08-figma-map.md)

## The one-line idea

> One chassis, many cores. Mez Studios builds the machine; Mez Systems is the systems house inside it; each product is one coloured core.

Two rules carry the whole system:

1. **Gradients belong to products.** Every product owns exactly one library gradient (its "core"). The holdco itself never wears a gradient; it stays monochrome (near-black `#0D0D0D`).
2. **Roundness falls as the entity grows.** A product is a fully round pill, the holdco is medium-radius, the parent is nearly square. Corner radius encodes scale.

## Read order

| # | File | What it covers |
|---|------|----------------|
| 00 | [brand-architecture.md](00-brand-architecture.md) | Studios → Systems → products, the holdco relationship, radius-is-scale |
| 01 | [colour.md](01-colour.md) | The V1 surface palette, hex, where you use each colour, the gradients-are-products rule |
| 02 | [gradients.md](02-gradients.md) | The gradient system: raw library (frame `312:57`, 53 swatches, MZ-G01–G53), the four cores, treatments |
| 03 | [typography.md](03-typography.md) | Type family (Inter, Notion-tuned), scale, weights, tracking |
| 04 | [the-mark.md](04-the-mark.md) | The wings, approved variations, clear space, exact SVG geometry |
| 05 | [product-system.md](05-product-system.md) | The disc product card (default), card anatomy and ratios; sphere is identity-only |
| 06 | [trading-cards-and-stacks.md](06-trading-cards-and-stacks.md) | The trading card, the deck/stack, the bundle, stack rules |
| 07 | [ui-components.md](07-ui-components.md) | Product pills (radius-is-scale), hero, buttons, chips |
| 08 | [figma-map.md](08-figma-map.md) | Every board's node ID on the Brand System page |
| 09 | [governance.md](09-governance.md) | Open decisions, do/don't, changelog |
| 10 | [product-template.md](10-product-template.md) | The reusable per-product template: inherit the system, own four things, 8 expressions |
| 11 | [layout-and-grid.md](11-layout-and-grid.md) | Page geometry: 1160 container, gutters, three breakpoints (600/920/1200), section rhythm 72/120, section spacing steps 9-11 |
| 12 | [states-and-forms.md](12-states-and-forms.md) | Button/link/input states, focus rings, functional colours (error/success), dark-surface text set, light-only LOCK, muted AA fix |
| 13 | [sections.md](13-sections.md) | The section catalogue: eight core sections plus quote-band and gradient-strip, each fully specified |
| 14 | [page-archetypes.md](14-page-archetypes.md) | Which sections compose each page: home, one product template, checkout, success, 404, legal |
| 15 | [commerce.md](15-commerce.md) | Checkout, success page and delivery email; price strings, GST by buyer location, email build rules |
| 16 | [motion.md](16-motion.md) | One duration, one easing, hover only, plus the named living-core exception; reduced motion |
| 17 | [voice-and-copy.md](17-voice-and-copy.md) | Language and naming law, semantic CTA actions, banned words, character limits, approved default copy |
| 18 | [imagery-and-og.md](18-imagery-and-og.md) | Screenshot law (colour evidence + window frame), OG template 1200x630, favicon and app-icon system |
| 19 | [review-checklist.md](19-review-checklist.md) | Definition of done: ten baseline checks plus four living-core checks when applicable |
| 20 | [living-core.md](20-living-core.md) | The parametric core treatment, internal-first scope, static twin, motion and fallback rules |

## Machine-readable data

For content tools (carousels, reels, ads) that need to read the brand programmatically:

- [`../colours.json`](../colours.json): palette with hex + type tags
- [`../fonts.json`](../fonts.json): font families + source
- [`../gradients.json`](../gradients.json): raw library, four assigned cores, living-core anchors and static twins
- [`../export-manifest.json`](../export-manifest.json): top-level brand metadata

## Status

Locked: brand architecture, radius-is-scale, gradients-are-products, the **surface V1 system** (2026-07-12), the **component radius + spacing scales**, the **component conventions**, the type system (Inter, Notion-tuned), the disc card, the trading-card system, the mark and its variations.

The web layer (docs 11-20, added 2026-07-17 through 2026-07-20) is DEFAULT working values, flag deviations to Olli; the light-only declaration in [12-states-and-forms.md](12-states-and-forms.md) and the [19-review-checklist.md](19-review-checklist.md) definition of done are LOCKED (the checklist tests the locked laws, not the defaults).

Open (see governance): final gradient picks for the four cores (current picks are strong candidates, not signed off), the master holdco mark direction.
