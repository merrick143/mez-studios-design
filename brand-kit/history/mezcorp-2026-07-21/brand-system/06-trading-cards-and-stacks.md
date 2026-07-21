# 06 · Trading cards, stacks & bundles

A second product format, distinct from the disc card. Where the disc card is calm and white-surfaced for the site, the **trading card** is a full-bleed gradient object that reads as collectible. It is the format for decks, stacks, and bundles.

Reference in Figma: "Trading card · stack + bundle" (Drafts page, node `49:2`) is the correct system. Rebuild any trading-card work on top of it.

Design language study: see [../trading-cards-fut-study/fut-teardown.md](../trading-cards-fut-study/fut-teardown.md).

## The trading card (V2 spec, locked 2026-07-12)

A single product as a full-bleed gradient nameplate. The lockup is no longer a floating centred block. It is split: a small glass eyebrow chip top-left, and a name + wings lockup anchored to the bottom third.

| Part | Spec |
|------|------|
| Card | Full-bleed **product gradient**, portrait **3:4** |
| Radius | **7.5% of the card width** |
| Inner hairline | **White at 16%**, inset just inside the edge |
| Eyebrow chip | Top-left. A **small dark glass chip** (rounded rect, radius **~8**) holding **"MEZ SYSTEMS"** in **white**. Inset from the top-left corner by **~8% of the card width**. The dark glass gives the eyebrow a legible backplate so it reads over any gradient. |
| Mark | **White wings, 32% of the card width**, sitting directly above the product name with a **small gap** |
| Name | Product name (e.g. "AI OS") in **white Semi Bold**, anchored to the **bottom third**, sitting just above the bottom edge with **bottom padding ~9% of the card height** |
| Lockup scrim | The bottom **45%** carries `--mz-lockup-scrim`: ink at `.58` at the top to `.68` at the bottom. It sits beneath the wings and name, never behind the whole card. |

The gradient is the whole card. The eyebrow chip, bottom lockup scrim, wings, and name are the only overlays. The scrim is a sanctioned accessibility treatment, not a new gradient or decorative glow: it guarantees white lockup contrast even over the lightest core pixels. **No paper surface and no sphere. No floating centred lockup:** the eyebrow lives top-left and the name + wings lockup lives in the bottom third.

### Layout in order (top to bottom)

1. **Top-left:** dark glass eyebrow chip, "MEZ SYSTEMS" in white, inset ~8% of width from the top-left corner.
2. **Bottom third:** white wings at 32% of the card width, then a small gap, then the product name in white Semi Bold, with ~9% of the card height as bottom padding beneath the name.

## The stack (a deck)

Multiple trading cards fanned as a **deck**: each card offset **50px across and 38px down**, with the **newest card on top** and the back cards peeking. Reads as a physical deck of the product set.

Use for: "the whole suite", collect-the-set moments, hero visuals for the bundle.

## The bundle

The product set inside a **dark `#0D0D0D` rounded container**, with the bundle name beneath (e.g. "Ultimate AI OS"). The dark container is always near-black; the cards keep their own gradients. This is the packaged-offer visual.

## Rules

- **Trading card = gradient nameplate.** Never a paper surface, never a sphere.
- **Eyebrow lives top-left** in a dark glass chip; the **name + wings lockup lives in the bottom third**. Never a floating centred lockup.
- **Lockup scrim is required** under the bottom 45%. Use `--mz-lockup-scrim`; do not tune it per product.
- **Wings are 32% of the card width**, radius is **7.5% of the card width**, inner hairline is **white 16%**.
- **Stack = a deck** of trading cards, fanned and overlapped (offset 50 across, 38 down, newest on top). Not a card grid.
- A bundle groups the cards in a **dark `#0D0D0D` container**, **never a gradient container**.
- One product, one gradient, on its card (same core as everywhere else).
