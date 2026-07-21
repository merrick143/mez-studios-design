# Mez Systems: Design System (portable)

Single-file, AI-readable design system for **Mez Systems**. Drop this folder into any project. An AI agent should be able to read this one file and build on-brand.

- **Figma (human exploration and milestone mirror):** https://www.figma.com/design/HU0GVaDhatjWrKCiSg3wlU/Mez-Systems---branding?node-id=149-30
- **Authority:** this portable folder mirrors an approved pack release. It never overrides its included tokens, decisions, or guidance.
- **Tokens:** [`tokens/tokens.css`](tokens/tokens.css) · [`tokens/tokens.json`](tokens/tokens.json) · [`tokens/tailwind.tokens.cjs`](tokens/tailwind.tokens.cjs)
- **Typography (locked):** [`typography.md`](typography.md)
- **Mark:** [`assets/wings.svg`](assets/wings.svg)

> **Status:** Surface system **V1, locked 2026-07-12**. Type locked 2026-07-10. There is now **one surface system, not five**. The earlier "pick a combo" surface exploration is retired.

---

## 1. What Mez Systems is

The digital-products holdco inside parent company **Mez Studios**. It holds products: AI OS, Aurora (Auto Ads System), Prism (Analytics Pack), Forge (Claude Code OS), and a wider product ladder.

> **One chassis, many cores.** Mez Studios builds the machine; Mez Systems is the systems house inside it; each product is one coloured core.

Two rules carry the whole system:

1. **Gradients belong to products.** Each product owns one gradient (its core). The holdco itself is monochrome, never a gradient.
2. **Radius is scale.** Product = fully round pill, holdco = medium radius, parent = nearly square.

## 2. Surfaces (V1, locked 2026-07-12)

**One surface system, not five.** The old "pick a combo" exploration is retired. Light monochrome. The **product gradient is the only colour**; every surface and every piece of text is greyscale.

| Token | Value | Where you use it |
|-------|-------|------------------|
| `--mz-bg` | `#F8F8F8` | Page background / brand white. Never pure `#FFFFFF`. |
| `--mz-surface` | `#F6F5F4` | Recessed grey panel. Subtle fills, inset sections. |
| `--mz-card` | `#FFFFFF` | Cards sitting on the background. |
| `--mz-text` | `#0D0D0D` | Primary text, headings, the mark. Also **dark UI / buttons / bundles** (near-black). |
| `--mz-text-2` | `#2E2E2E` | Body / secondary text. |
| `--mz-text-muted` | `rgba(46,46,46,.70)` | Captions, meta. WCAG AA (~4.6:1 on `#F8F8F8`); raised from `.58` 2026-07-17. |
| `--mz-border` | `rgba(13,13,13,.08)` | Hairlines, card borders. |

**Functional colours (forms and feedback only, `12-states-and-forms.md`).** The sole colour exception besides the product gradient. Never a heading, background or brand accent.

| Token | Value | Where you use it |
|-------|-------|------------------|
| `--mz-error` | `#B42318` | Error text, invalid field borders, destructive confirmation. |
| `--mz-success` | `#15803D` | Success text, confirmed state. |
| `--mz-focus-ring` | `rgba(13,13,13,.45)` | Focus ring on light surfaces. At least 3:1, 2px width, 2px offset. |
| `--mz-focus-ring-dark` | `rgba(255,255,255,.5)` | Focus ring on dark sections. Same 2px width, 2px offset. |
| `--mz-input-border` | `rgba(13,13,13,.45)` | Form-control boundary on white / light, at least 3:1. |
| `--mz-placeholder` | `rgba(46,46,46,.70)` | Placeholder text on white / light, at least 4.5:1. |

**Dark-surface text (on `#0D0D0D` sections, `12-states-and-forms.md`).** A section treatment, never a theme; the site stays light-only.

| Token | Value | Where you use it |
|-------|-------|------------------|
| `--mz-dark-text` | `#FFFFFF` | Primary text on dark. |
| `--mz-dark-text-2` | `rgba(255,255,255,.64)` | Secondary text on dark. |
| `--mz-dark-muted` | `rgba(255,255,255,.45)` | Muted text, captions, meta on dark. |
| `--mz-dark-border` | `rgba(255,255,255,.14)` | Hairlines and borders on dark. |

**The one V1 rule:** page `#F8F8F8` → recessed panel `#F6F5F4` → card `#FFFFFF` → dark UI `#0D0D0D`. That stack is the whole surface language.

**Rule:** no colour except the product gradient, and the gradient is used on **products only**, never on a page or section background. No blue text, no coloured UI. The gradient does all the talking.

## 3. Typography (locked): Notion-inspired

Full detail in [`typography.md`](typography.md). Summary:

- **Default → Inter** · **Serif → Instrument Serif** (editorial italic accent, sparingly) · **Mono → IBM Plex Mono**
- The Notion feel = Inter run **Bold for headings, with negative tracking and tight leading** (not the default look).

| Role | Weight | Size | Tracking | Leading |
|------|--------|------|----------|---------|
| H1 | Bold 700 | 72 | -3% | 100% |
| H2 | Bold 700 | 40 | -2.5% | 104% |
| H3 | Semi Bold 600 | 22 | -1.5% | 125% |
| Body | Regular 400 | 17 | -1% | 150% |
| Button | Semi Bold 600 | 16 | -1% | n/a |
| Caption | Regular 400 | 13 | -0.5% | n/a |
| Eyebrow | Medium 500 | 12 | +6% | UPPERCASE |

Instrument Serif **italic** is the occasional editorial accent. IBM Plex Mono is code / technical labels only.

## 4. Radius and spacing

**Component radius scale (V1):**

| Token | Value | Use |
|-------|-------|-----|
| `--mz-r-chip` | 8px | Chips, tags, small inline controls. |
| `--mz-r-tile` | 14px | Tiles, small media, list items. |
| `--mz-r-card` | 20px | Product cards and standard cards. |
| `--mz-r-panel` | 28px | Panels, large recessed sections, hero surfaces. |
| `--mz-r-pill` | 999px | Pills, primary CTA, product pills. |

**Brand-tier radius (a separate namespace, where radius encodes entity scale):** `--mz-radius-pill` 999px (product), `--mz-radius-holdco` 22px (holdco, medium), `--mz-radius-parent` 8px (parent, nearly square). Use these for entity pills and lockups; use the component scale above for UI.

**Spacing scale (4px base, 8 ordinal steps):**

| Step | `--mz-s-1` | `--mz-s-2` | `--mz-s-3` | `--mz-s-4` | `--mz-s-5` | `--mz-s-6` | `--mz-s-7` | `--mz-s-8` |
|------|-----|-----|-----|-----|-----|-----|-----|-----|
| px | 4 | 8 | 12 | 16 | 24 | 32 | 48 | 64 |

## 5. Gradients (products only)

Each product owns one library gradient, named `MZ-G01` to `MZ-G53` (`MZ-G01` to `MZ-G20` catalogued with hashes). Current cores:

| Product | Function | Core | Source image hash (provenance) |
|---------|----------|------|-----------------|
| AI OS | AI Operating System | `MZ-G13` | `4ea105843cbc5fe3450b70aa0f3c3bcc9b487408` |
| Aurora | Auto Ads System | `MZ-G20` | `76df089a7f3d0fe9f9fc44349a71401ed214c4d9` |
| Prism | Analytics Pack | `MZ-G06` | `34e197fd0fc94cdc231d66446fa6c3f2b1e48fad` |
| Forge | Claude Code OS | `MZ-G15` | `876be3cf1c6da154d9a532d2b5a865199b29c939` |

Release catalogue: [`gradients.json`](gradients.json). It intentionally contains the four assigned product cores and their source/export hashes, not the 53-swatch research library. Exact **1600 × 1600 WebP** assets ship in `assets/gradients/`; `tokens.css` points to them directly. Each core also carries four parametric anchors for the optional living-core treatment rendered by [`mz-core.js`](mz-core.js). The living result is an approximation, while the WebP remains the pixel-accurate static twin. A core is always shown through a **treatment** (disc, gradient-M, trading, sphere, living core), never a bare rectangle, and never on a page or section background. Glow was retired 2026-07-17: never add a halo, blur or diffuse spread behind a core.

## 6. The mark

The **wings** (twin-panel "M"), shared with Mez Studios. Fill: `#0D0D0D` (default near-black), white (knockout on a gradient), or gradient (Gradient-M). Free-floating, clear space = one cap-height, min 24px. Geometry in [`assets/wings.svg`](assets/wings.svg).

## 7. Components

Locked V1 conventions. All surfaces follow section 2, all radii section 4.

- **Primary CTA:** a dark near-black (`#0D0D0D`) **pill**, label **"Get the AI OS"**, white text, button weight (Semi Bold 600). **Never show a price**, ever. Text-CTA variant: ink label with a trailing arrow ("Get the AI OS →").
- **Product pill:** a **white pill** (`--mz-r-pill`) containing a small gradient **disc** glyph + the product name. The compact product reference.
- **Product card:** **white** (`#FFFFFF`), radius **20** (`--mz-r-card`), hairline border `rgba(13,13,13,.08)`, soft shadow (`--mz-shadow-card`), with a gradient **disc** inside sized at **50% of the card width**. Always the disc on a product card; the sphere is reserved for identity boards, glow is retired and never built.
- **Trading card:** a **full-bleed product-gradient nameplate**, portrait **3:4**, radius **7.5% of width**, a **white 16% inner hairline**. **Top-left:** a small **dark glass eyebrow chip** (radius ~8) with **"MEZ SYSTEMS"** in white, inset ~8% of the width from the corner. **Bottom 45%:** the required `--mz-lockup-scrim`, ink `.58` to `.68`, sits beneath **white wings at 32% of the width** and the white Semi Bold product name. This is the sanctioned contrast treatment, not a glow. **No paper surface, no sphere, no floating centred lockup.** Full anatomy in the included `docs/06-trading-cards-and-stacks.md`.
- **Stack:** a fanned **deck of trading cards**, each card offset **50px across, 38px down**, newest card on top. The "collect the set" / whole-suite visual.
- **Bundle:** a **dark `#0D0D0D` container** grouping product cards, with the bundle name beneath. The container is always near-black, **never a gradient container**.
- **Recessed panel:** `#F6F5F4`, radius **28** (`--mz-r-panel`), for inset sections on the page.
- **Chip / tag:** small rounded rect, radius **8** (`--mz-r-chip`), `rgba(13,13,13,.08)` fill, ink label. For "included in" lists, metadata, gradient IDs.

## 8. Sizing and ratios (locked 2026-07-12)

All three are proportional, not fixed pixels. Reproduce them by ratio at any size.

| Ratio | Value | Applies to |
|-------|-------|------------|
| **Disc** | flat, hard edge, wings **50% of Ø**, optically centred with a **2% upward nudge**. Glow retired 2026-07-17, never build it. | every product core |
| **Orb in a product card** | orb diameter = **50% of the card width** | the product card (disc) |
| **Trading-card wings** | white wings = **32% of the card width** | the trading card |

### Trading-card layout (locked 2026-07-12)

The trading card is **not** a floating centred lockup. It splits into a top-left eyebrow and a bottom-third name + wings lockup.

- **Card:** full-bleed product gradient, portrait **3:4**, corner radius **7.5% of the width**, a **white 16% inner hairline** inset just inside the edge.
- **Top-left:** a small **dark glass chip** (rounded, radius **~8**) holding **"MEZ SYSTEMS"** in **white**, inset from the top-left corner by **~8% of the width**. This is the visible eyebrow overlay: the dark glass keeps it legible over any gradient.
- **Bottom third:** the **white wings (32% of the card width)** sit directly above the product name with a **small gap**; the **product name** in **white Semi Bold** sits just above the bottom edge with **bottom padding ~9% of the height**.

An LLM should build the card by: draw the gradient rect (3:4, radius = 0.075 × width), inset a white 16% stroke; place the glass "MEZ SYSTEMS" chip at ~8% inset top-left; place wings at 32% of width in the bottom third; place the name in white Semi Bold below the wings, ~9% of height from the bottom.

## 9. Do / Don't

**Do:** the `#F8F8F8` → `#F6F5F4` → `#FFFFFF` → `#0D0D0D` surface stack; `#0D0D0D`/`#2E2E2E` text; Inter Bold headings with tight tracking; one gradient per product through a treatment; radius from the component scale; "Get the AI OS" CTA with no price.

**Don't:** any colour except the product gradient; a gradient on a page/section background or on a bundle container; pure white surfaces; Extra Bold display headings or the wrong role weight; default Inter tracking/leading; a price in a CTA; serif for body or whole headings; a paper surface or sphere on a trading card; a floating centred lockup on a trading card (eyebrow is top-left, name + wings are bottom-third); a halo, blur or diffuse glow behind any core (glow is retired, build the flat disc).

---

# Web layer (docs 11-20)

The following condense the web-layer docs added 2026-07-17. Values only; the full rules and prose live in the included `docs/11-*` to `docs/19-*`. All are DEFAULT working values (flag deviations to Olli) except the light-only declaration in 12 and the review gate in 19, which are LOCKED.

## 10. Layout and grid (`docs/11-layout-and-grid.md`)

One geometry for every page. **Container** `1160px`, centred; **gutter** `24px` below 920, `32px` at 920 and up. **Breakpoints** (min-width): `sm 600` · `md 920` · `lg 1200`. **Section rhythm**: `72px` vertical padding below 920, `120px` at 920 and up; the hero opens with `96px` / `140px` on top. **Section spacing steps** extend the 8-step scale: `--mz-s-9` 96 · `--mz-s-10` 120 · `--mz-s-11` 160 (steps 1-8 inside components, 9-11 between sections). **Type at small widths**: h1 stays `clamp(2.75rem, 6vw, 4.5rem)`, h2 goes fluid `clamp(1.75rem, 4.5vw, 2.5rem)` (capped at the locked 2.5rem desktop token), body is 16px below `md` and 17px at `md` and up, never smaller than 16. **Stacking**: multi-column sections stack to one column below 920 in source order; the suite grid runs 4 (lg) → 2 (md) → 1.

## 11. States and forms (`docs/12-states-and-forms.md`)

States are motion and ink, not new colour. **Button**: hover lifts `translateY(-2px)` and swaps to `--mz-shadow-float`, active settles to `translateY(0)`, focus-visible draws a 2px ring at 2px offset, disabled is `opacity: .4` + `pointer-events: none`. **Link**: ink `#0D0D0D`, no underline at rest, underline on hover. **Input**: height `44px`, radius `8`, `#FFFFFF` fill, `1px` `--mz-input-border` (`rgba(13,13,13,.45)`) boundary, focus border goes ink plus the ring, label 13px Inter Medium (500), placeholder `--mz-placeholder` (`rgba(46,46,46,.70)`). **Functional colours** (forms + feedback only): `--mz-error` `#B42318`, `--mz-success` `#15803D`. **Focus ring**: `--mz-focus-ring` `rgba(13,13,13,.45)` on light, `--mz-focus-ring-dark` `rgba(255,255,255,.5)` on dark, both 2px / 2px offset. Light rings and control boundaries clear 3:1; placeholders clear 4.5:1. **Dark-surface text** on `#0D0D0D`: `--mz-dark-text` `#FFFFFF`, `--mz-dark-text-2` `rgba(255,255,255,.64)`, `--mz-dark-muted` `rgba(255,255,255,.45)`, `--mz-dark-border` `rgba(255,255,255,.14)`. **Light-only (LOCKED 2026-07-17)**: no `prefers-color-scheme`, no dark mode; dark is a section treatment, not a theme.

## 12. Sections (`docs/13-sections.md`)

Eight core sections, one geometry: **nav · hero · feature-row · suite-grid · pricing-moment · faq · cta-band · footer**, plus **quote-band** (§9) and **gradient-strip** (§10) folded in from 14. Each is fully specified: components, desktop layout inside 1160, how it stacks below 920, the 72/120 rhythm, copy slots with char limits, imagery rule. The nav carries the only two bespoke page numbers: **66px** height and a **`rgba(248,248,248,.78)`** backdrop tint (blur 12). A section built with its own geometry is off-system.

## 13. Page archetypes (`docs/14-page-archetypes.md`)

Compose, do not invent. **Home**: nav → hero (trading-card fan) → suite-grid → gradient-strip → cta-band (dark bundle) → faq → footer. **Product**: one template, four products (only copy, screenshots and the core vary): nav → hero (disc) → 3× feature-row → quote-band → pricing-moment → faq → cta-band → footer. **Utility** (checkout, success, 404, legal) reuse the core sections in reduced form (reduced nav, slim footer) plus a typography recipe. **Meta**: title `{Page} · Mez Systems` (home leads with the brand), description capped at 155 chars.

## 14. Commerce (`docs/15-commerce.md`)

The live Stripe flow is do-not-touch until Olli schedules the restyle; this is the target. AI OS is **USD $99, one-time, lifetime access**, never subscription framing (no `/mo`, `renews`, `plan`). One flat $99 for every buyer; **GST follows buyer location** (Stripe Tax reads billing address, IP, card), inclusive, ABN 21 697 707 190: AU buyers see `Includes 10% GST (AU)` (`· $9.00`, 1/11 of $99), non-AU buyers see no GST line. **Delivery email**: `600px` single column, table layout (`role="presentation"`), system font stack (no web fonts), logo as a hosted PNG (no SVG), one gradient header strip (MZ-G13, gradient through a surface), a bulletproof table-cell button, a required plain-text alternative part, no unsubscribe (transactional).

## 15. Motion (`docs/16-motion.md`)

One duration, one easing, hover only, plus one named continuous exception. `--mz-duration` **200ms** (button lift, card shadow, link underline, focus ring), `--mz-duration-slow` **280ms** (accordion/open close and the mobile nav sheet only), `--mz-ease` **`cubic-bezier(.2,.7,.2,1)`** for every standard transition. Gradient fills, text, layout position on scroll, and static discs never move. A product core may animate continuously only through `mz-core.js` under [`docs/20-living-core.md`](docs/20-living-core.md). Hover accelerates the fluid to 1.85× without scaling the core or moving the wings. `prefers-reduced-motion: reduce`, print, email, PDF and renderer failure use the exact static twin.

## 16. Voice and copy (`docs/17-voice-and-copy.md`)

Plain, calm, declarative. **Australian English**, **sentence case everywhere** (including headings and buttons), no em dashes, no exclamation marks in UI. **Names** (fixed): the product is **AI OS** (a space), the holdco is **Mez Systems**, the endorsement is **A Mez Studios company**; core codes never surface; banned spellings **AIOS** and **Atlas**. **CTA semantics**: Get for purchase, Join for planned-product interest, Explore/See for discovery, Open for access, Start for onboarding. The primary purchase CTA is locked to **"Get the AI OS"**. **Banned hype words**: Unlock, Unleash, Supercharge, Revolutionise, Elevate, Seamless, Empower (and variants). Copy fits the char limits from 13. Flagship headline: **"One system your whole business runs on"**.

## 17. Imagery and OG (`docs/18-imagery-and-og.md`)

**Screenshots stay in full colour**: a product screenshot is evidence, the single exception to the monochrome rule; never greyscale, tint or desaturate it. **Window frame**: radius `14` (`--mz-r-tile`), `1px` `--mz-border`, `--mz-shadow-card`, a **36px** `#F6F5F4` title bar with **three 8px** `rgba(13,13,13,.16)` dots at the left (6px apart, inset 12px), no traffic-light colour, no title text; on white or recessed, **never on dark**. No device frames and no photography for v1 (only a founder photo Olli supplies himself, if ever). **OG**: `1200 × 630` on `#F8F8F8`, `64px` safe area, wings + "Mez Systems" top-left, page title in H2 style (Inter Bold 700, 40px), a product disc on product pages, a four-core trading-card fan on the home/suite page, and no right-side visual on other non-product pages. The background is flat with no gradient. Name files `og-{page}.png`. **Favicons** 32 / 180 / 512 (product pages wear the AI OS disc, holdco/brand pages wear the ink wings on white); **app-icon marks** disc + wings at 128 / 256 / 512.
