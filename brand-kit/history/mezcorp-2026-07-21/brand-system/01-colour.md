# 01 · Colour

> **LOCKED: surface V1 (2026-07-12).** One light-monochrome surface system, not five. The **product gradient is the only colour**; every surface and every piece of text is greyscale. The earlier Paper / Ink-Blue / Charcoal holdco palette is **superseded** (kept only as history at the bottom of this file). Current tokens: [`../design-system-export/tokens/tokens.css`](../design-system-export/tokens/tokens.css).

## The V1 surface palette

The surface stack is: page → recessed panel → card → dark UI. That single ladder carries the whole system.

| Token | Hex | Where you use each colour |
|-------|-----|---------------------------|
| **Background** | `#F8F8F8` | Page background / brand white. Never pure `#FFFFFF`. |
| **Surface** (recessed panel) | `#F6F5F4` | Recessed grey panels, subtle fills, inset sections. |
| **Card** | `#FFFFFF` | Cards sitting on the background. |
| **Text** | `#0D0D0D` | Primary text, headings, the mark. Also **dark UI / buttons / bundles** (near-black). |
| **Text 2** | `#2E2E2E` | Body / secondary text. |
| **Text muted** | `rgba(46,46,46,.70)` | Captions, meta, function labels. WCAG AA (~4.6:1 on `#F8F8F8`); raised from `.58` on 2026-07-17. |
| **Border** | `rgba(13,13,13,.08)` | Hairlines, card borders, dividers. |

RGB (0–1 range, for the Figma Plugin API):

- Background `{ r: 0.973, g: 0.973, b: 0.973 }`
- Surface `{ r: 0.965, g: 0.961, b: 0.957 }`
- Card `{ r: 1, g: 1, b: 1 }`
- Text `{ r: 0.051, g: 0.051, b: 0.051 }`
- Text 2 `{ r: 0.180, g: 0.180, b: 0.180 }`

## The rule

> **Gradients = products. Everything else is monochrome.**

Every product owns one gradient (see [02-gradients.md](02-gradients.md)). The holdco itself never wears a gradient. The gradient is used on **products only**, never on a page or section background. This is what keeps the parent readable next to the colourful products.

## Do / Don't

- **Do** build the surface stack in order: `#F8F8F8` page, `#F6F5F4` recessed panel, `#FFFFFF` card, `#0D0D0D` dark UI.
- **Do** set text in `#0D0D0D` / `#2E2E2E`, and muted text via the muted token, never a new grey or a lighter weight.
- **Don't** use any colour except the product gradient. No coloured text, no coloured UI.
- **Don't** put a gradient behind the mark, on a page background, or on a bundle container.
- **Don't** use pure white `#FFFFFF` for the page. The brand white is `#F8F8F8`. (Pure white is the card surface and the wings knockout on a gradient.)

---

## Superseded (history)

The earlier holdco exploration used a warm off-white and a blue ink. It is **retired** for the digital-products system and must not be used:

| Superseded name | Hex | Replaced by |
|-----------------|-----|-------------|
| ~~Paper~~ | `#F2F0EA` | `#F8F8F8` background / `#FFFFFF` card |
| ~~Ink Blue~~ | `#16233E` | `#0D0D0D` text and dark UI |
| ~~Charcoal~~ | `#2A2724` | `#0D0D0D` |
