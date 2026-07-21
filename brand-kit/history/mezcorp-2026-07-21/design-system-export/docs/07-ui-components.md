# 07 · UI components and conventions

> **LOCKED: V1 (2026-07-12).** Surfaces follow [01-colour.md](01-colour.md); radius and spacing scales below are authoritative. One surface system, not five.

## Radius scale (component)

| Token | Value | Use |
|-------|-------|-----|
| `--mz-r-chip` | 8px | Chips, tags, small inline controls. |
| `--mz-r-tile` | 14px | Tiles, small media, list items. |
| `--mz-r-card` | 20px | Product cards and standard cards. |
| `--mz-r-panel` | 28px | Panels, large recessed sections, hero surfaces. |
| `--mz-r-pill` | 999px | Pills, primary CTA, product pills. |

Separate from the **brand-tier radius** (radius encodes entity scale): product = pill, holdco = medium (`--mz-radius-holdco` 22px), parent = nearly square (`--mz-radius-parent` 8px). See [00-brand-architecture.md](00-brand-architecture.md).

## Spacing scale (4px base, 8 steps, plus section steps 96/120/160, see [11-layout-and-grid.md](11-layout-and-grid.md))

| `--mz-s-1` | `--mz-s-2` | `--mz-s-3` | `--mz-s-4` | `--mz-s-5` | `--mz-s-6` | `--mz-s-7` | `--mz-s-8` |
|-----|-----|-----|-----|-----|-----|-----|-----|
| 4 | 8 | 12 | 16 | 24 | 32 | 48 | 64 |

## Components

- **Primary CTA:** a dark near-black (`#0D0D0D`) **pill**, label **"Get the AI OS"**, white text, button weight (Semi Bold 600). **Never show a price**, ever. Text-CTA variant: ink label with a trailing arrow ("Get the AI OS →").
- **Product pill:** a **white pill** (`--mz-r-pill`) containing a small gradient **disc** glyph + the product name. The compact product reference for nav, selectors, and inline mentions.
- **Product card:** **white** (`#FFFFFF`), radius **20** (`--mz-r-card`), hairline border `rgba(13,13,13,.08)`, soft drop shadow (`--mz-shadow-card`), with a gradient **disc** inside sized at **50% of the card width** (wings = 50% of the disc, hard edge, no glow). Always the disc on a product card; the sphere is reserved for identity boards, glow is retired and never built. Full anatomy in [05-product-system.md](05-product-system.md).
- **Trading card:** a **full-bleed product-gradient nameplate**, portrait **3:4**, radius **7.5% of width**, a **white 16% inner hairline**. **Top-left:** a small **dark glass eyebrow chip** (radius ~8) with **"MEZ SYSTEMS"** in white, inset ~8% of the width. **Bottom third:** **white wings at 32% of the width** directly above the product name (small gap), the name in **white Semi Bold** just above the bottom edge (~9% of height padding). **No paper surface, no sphere, no floating centred lockup.** See [06-trading-cards-and-stacks.md](06-trading-cards-and-stacks.md).
- **Stack:** a fanned **deck of trading cards**, each card offset **50px across, 38px down**, newest card on top.
- **Bundle:** a **dark `#0D0D0D` container** grouping product cards, bundle name beneath. Always near-black, **never a gradient container**.
- **Recessed panel:** `#F6F5F4`, radius **28** (`--mz-r-panel`), for inset sections on the page.
- **Chip / tag:** small rounded rect, radius **8** (`--mz-r-chip`), `rgba(13,13,13,.08)` fill, ink label. For "included in" lists, metadata, gradient IDs.

### Pill states

- **Selected** = filled white pill with a soft shadow.
- **Unselected** = transparent or low-contrast, no shadow.
- **Ghost** = faded, for overflow items in a selector row.

## Hero (carousel)

A rounded `#F6F5F4` panel (radius `--mz-r-panel`) with a five-disc carousel (faded edges, medium sides, one big centre disc), the centre product's name and description, chevrons, and a bottom feature nav. The focal element in the centre disc is a **white wings button**, not a play button. Top of the panel: segmented tabs. Bottom: feature nav with the CTA "Get the AI OS".

## Surfaces (quick reference)

- Page `#F8F8F8` → recessed panel `#F6F5F4` → card `#FFFFFF` → dark UI `#0D0D0D`.
- Cards use radius 20; panels use radius 28.
- Hairline dividers and card borders: `rgba(13,13,13,.08)`.
- No colour except the product gradient, and never a gradient on a background or a bundle container.
