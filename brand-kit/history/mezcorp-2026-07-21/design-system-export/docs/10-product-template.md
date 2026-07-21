# 10 · Per-product template

The reusable skeleton for building any single digital product on top of the Mez Systems brand. Everything the system already locked (surfaces, type, radius and spacing, the disc (default product unit), the sphere (identity boards only), the trading card, the deck, the bundle) is inherited. A product only fills in what is genuinely its own.

Lives as one Figma page, **"Mez Systems · Products"**. That single page holds this template plus every sub-product board. It is **not** a page per product: new products are new boards on the same page.

## The principle

> A product **inherits the whole Mez system**. It **owns only four things.**

Type, surfaces, radius and spacing, the mark, the disc recipe (default product unit), the sphere recipe (identity boards only), the trading-card layout, the pill states, the CTA: all already decided upstream in files 00 to 09. A product never re-invents any of them. It fills in exactly four owned slots, and everything else follows automatically:

| # | The product owns | Everything else |
|---|------------------|-----------------|
| a | Its **gradient core** (one library gradient, e.g. `MZ-G13`) | inherited |
| b | Its **name** (e.g. "AI OS") | inherited |
| c | Its **copy** (role, tagline, headline, subhead, body) | inherited |
| d | Its **own product screens** (hero, checkout, in-app UI) | inherited |

Fill those four and the product is fully specified. If a decision is not one of the four, it has already been made. See [09-governance.md](09-governance.md) for what is locked.

## The 8 expressions every product needs

The template skeleton. Every product board carries these eight, in order. Duplicating the template gives you all eight pre-wired to the AI OS core; swap the gradient and rewrite the copy to reskin them.

**1 · Identity.** The product's index card: the **name** (Inter Bold, Notion-tuned), a **core gradient chip** with its **gradient ID** (e.g. `MZ-G13`), a **one-line role** ("The AI operating system"), and the **tagline**. This is the single source of truth for the other seven expressions to read from.

**2 · Core and kit.** The product gradient shown three ways: as a flat **disc** (default product unit), as the **sphere** (identity boards only), and as the **gradient-M**. Plus the type lockup (name in Inter Bold, role in Inter Medium tracked) and a one-line **usage note** saying the disc is the default and the sphere / M are for identity and glyph use only. This board is the product's mini asset sheet.

**3 · Hero.** The landing hero: a small **eyebrow** (Inter Medium, tracked), an **Inter Bold headline** (Notion-tuned, negative tracking, tight leading), a **subhead** in `#2E2E2E`, a **primary pill CTA** (dark `#0D0D0D` pill, "Get the AI OS", never a price), and the **disc**, hard-edged with no glow. Sits on the page surface `#F8F8F8` or a recessed panel `#F6F5F4`.

**4 · Product card and in a bundle.** Two states of the same card. First the **disc product card on its own**: white `#FFFFFF`, radius 20, hairline, soft shadow, orb at 50% of the card width. Then the **same card inside a dark `#0D0D0D` bundle container** sitting next to its sibling products, showing how the one product reads inside the packaged offer. Card spec in [05-product-system.md](05-product-system.md).

**5 · Stacks and bundles.** The collectible formats: the product's **trading card**, the **fanned deck** (each card offset **50px across, 38px down**, newest card on top), and the **bundle** (the set inside a dark `#0D0D0D` container with the bundle name beneath). Full rules in [06-trading-cards-and-stacks.md](06-trading-cards-and-stacks.md).

**6 · Gradient in context.** The **one core** carried across the product's surfaces: **landing**, **checkout**, and **email**. Proves the single gradient holds the product together end to end, and that the gradient only ever appears on product objects, never on a page or section background.

**7 · UI.** The interactive kit: **product pills** in all three states (**selected** = filled white pill with soft shadow, **unselected** = low-contrast no shadow, **ghost** = faded overflow), **buttons** (primary dark pill plus text-CTA variant), and the **in-app product hero** (the recessed `#F6F5F4` panel with the five-disc carousel and a white wings button in the centre disc). Component specs in [07-ui-components.md](07-ui-components.md).

**8 · Trading card.** The locked nameplate, called out on its own because the layout is fixed: **full-bleed product gradient** (portrait 3:4, radius 7.5% of width, white 16% inner hairline), a **top-left dark glass "MEZ SYSTEMS" chip** (radius ~8, inset ~8% of width), and a **bottom-third lockup** of **white wings at 32% of the card width** directly above the **product name in white Semi Bold**, sitting just above the bottom edge (~9% of height padding). No paper surface, no sphere, no floating centred lockup.

## How to apply the template

Building a new product is a reskin, not a redesign:

1. **Duplicate** the AI OS product sheet (all eight expressions).
2. **Swap the gradient** everywhere: replace the image fill / core ID with the new product's library gradient (e.g. AI OS `MZ-G13` becomes Aurora `MZ-G20`). Because the disc is a flat fill of the same core, it re-colours itself wherever it appears.
3. **Rename**: the identity name, every product-name lockup, the trading-card name.
4. **Rewrite the copy**: role, tagline, headline, subhead, body.

Nothing else changes. Surfaces, type, radius, spacing, the disc recipe (default product unit), the sphere recipe (identity boards only), the trading-card layout, the pill states and the CTA are all inherited and stay exactly as locked.

## The current products

One page, one board per product. AI OS is built; the other three are slots to fill later with the same template.

| Product | Core | Role | Status |
|---------|------|------|--------|
| **AI OS** | `MZ-G13` | The AI operating system | **BUILT** |
| **Aurora** | `MZ-G20` | Auto Ads System | Slot |
| **Prism** | `MZ-G06` | Analytics Pack | Slot |
| **Forge** | `MZ-G15` | Claude Code OS | Slot |

> **Name note:** the first product's name is **"AI OS"**, with a space. No other spelling and no earlier working name applies.

The cores here are the current picks from the raw gradient library (53 swatches, `MZ-G01`–`MZ-G20` catalogued; [02-gradients.md](02-gradients.md)) and are not finally signed off (see the open decisions in [09-governance.md](09-governance.md)). Each new product assigns its core by ID from the library when it ships.

## Changelog

- **2026-07-12** — Per-product template documented. One reusable skeleton (8 expressions) on a single **"Mez Systems · Products"** Figma page; a product inherits the whole system and owns only four things (gradient core, name, copy, product screens). Current products: AI OS (`MZ-G13`, BUILT), Aurora, Prism, Forge (slots). Confirmed the first product ships as **AI OS**, with a space.
