# 13 · Sections (the MVP eight)

Status: DEFAULT · working values, flag deviations to Olli

A homepage is six to ten sections, and until now the pack specified almost none of them, so every build invented roughly 80% of the page. This doc closes that. Eight sections, each fully specified: the components it draws from, its desktop layout inside the 1160 container, how it stacks below 920, its vertical rhythm, its copy slots with character limits, and its imagery rule. Build a Mez Systems page by composing these eight. A section that is not one of these, or one of these built with its own geometry, is off-system.

Two further sections, **quote-band** and **gradient-strip**, are folded in from [14-page-archetypes.md](14-page-archetypes.md) as sections 9 and 10 below. They were first specified there and now live here; they serve specific archetypes (quote-band on the product page, gradient-strip on the home page) rather than every page, so the MVP eight remain the page backbone.

Every layout number here traces to [11-layout-and-grid.md](11-layout-and-grid.md) (container, gutters, breakpoints, section rhythm, spacing steps 9 to 11), [07-ui-components.md](07-ui-components.md) (radius and spacing steps 1 to 8), [12-states-and-forms.md](12-states-and-forms.md) (button, link, focus and dark-surface states) or the token files. The nav alone carries two bespoke values the brief sets: **66px** height and a backdrop tint of **rgba(248,248,248,.78)**. Nothing else is a new number. Character limits are copy constraints, not design tokens: they cap the words, not the pixels.

Conventions used below:
- **Stack below 920** means the section collapses to one column at the `md` breakpoint, in **source order**, never reordered (see [11-layout-and-grid.md](11-layout-and-grid.md) · Stacking).
- **Section rhythm** is the vertical padding from [11-layout-and-grid.md](11-layout-and-grid.md): **72px** below 920, **120px** (`--mz-s-10`) at 920 and up. The hero opens the page and takes extra headroom on top (**96px** / **140px**).
- Buttons, links, chevrons and focus rings behave per [12-states-and-forms.md](12-states-and-forms.md): the lift on hover, the underline on links, the ink focus ring on light and the white ring on dark. No section restates those.

---

## 1 · Nav

The default site header. This is the one nav; a build that grows a second bar is off-system.

**Anatomy** ([07-ui-components.md](07-ui-components.md), [04-the-mark.md](04-the-mark.md)): wings + wordmark lockup (left), two text links (centre or left of the CTA), one primary CTA pill (right). Links and CTA follow [12-states-and-forms.md](12-states-and-forms.md).

**Desktop layout (≥920):** a single row inside the 1160 container. Left cluster: wings + "Mez Systems" wordmark. Right cluster: the links `Products · Pricing` (interpunct separator), then the dark ink pill CTA. Row height is a fixed **66px**. Horizontal padding is the container gutter (**32px** at `md` and up, `--mz-gutter-lg`). Sticky: `position: sticky; top: 0`, sitting above page content. Backdrop: `backdrop-filter: blur(12px)` (reusing `--mz-s-3` from the spacing scale, not a new value) over a translucent tint `background: rgba(248,248,248,.78)`. A hairline `--mz-border` bottom edge appears once the page scrolls under it.

> The `Products · Pricing` link set is a **DEFAULT (open)**: it is the working pick, not locked. Flag any change to the link set to Olli.

**Mobile layout (<920):** height stays **66px**, gutter drops to **24px** (`--mz-gutter`). The wings + wordmark stay left; below **400px**, the visible lockup reduces to the wings so the persistent CTA and menu control fit without overflow, while the link's accessible name remains "Mez Systems". The two text links collapse into a **sheet** behind a **44px** menu toggle; the **CTA pill stays visible** in the bar. Opening the sheet moves focus to its first link. Escape closes it and returns focus to the toggle; activating a link or clicking outside closes it. The sheet's links have a minimum 44px row and inherit the link states. No new colour enters: the sheet is a `--mz-card` surface with `--mz-border` hairlines.

**Vertical spacing:** the bar is a fixed 66px band, not on the section rhythm. Content below it starts at the hero's top padding.

**Copy slots**

| Slot | Limit | Note |
|------|-------|------|
| Wordmark | ≤ 16 chars | "Mez Systems". |
| Nav link (each, 2) | ≤ 14 chars | "Products", "Pricing" by default. |
| CTA label | ≤ 14 chars | Locked "Get the AI OS" ([07-ui-components.md](07-ui-components.md)). Never a price. |

**Imagery rule:** the wings mark only ([04-the-mark.md](04-the-mark.md)). No gradient, no disc, no product art in the bar.

---

## 2 · Hero

Opens the page: one claim, one supporting line, one CTA pair, one product visual.

**Anatomy** ([07-ui-components.md](07-ui-components.md), [05-product-system.md](05-product-system.md), [06-trading-cards-and-stacks.md](06-trading-cards-and-stacks.md)): eyebrow, H1, sub-paragraph, a CTA pair (primary ink pill + a ghost secondary), and one visual: a product **disc** ([05-product-system.md](05-product-system.md)) or a **trading-card fan** ([06-trading-cards-and-stacks.md](06-trading-cards-and-stacks.md), offset 50 across / 38 down). The ghost CTA is a pill with a transparent fill, ink label and `--mz-border` hairline; it takes the same button states as the primary ([12-states-and-forms.md](12-states-and-forms.md)).

**Desktop layout (≥920):** two columns inside the 1160 container. Text column left (eyebrow → H1 → sub → CTA pair), visual column right (disc or card fan). Column gap **48px** (`--mz-s-7`). H1 uses `--mz-h1-size` (`clamp(2.75rem, 6vw, 4.5rem)`), sub uses body at **17px**. A **centred variant** is allowed: the text block centres, the CTA pair centres, and the visual sits **below** it in a single column.

**Mobile layout (<920):** stacks to one column in source order: eyebrow → H1 → sub → CTA pair → visual. The CTA pair wraps to two full-width rows if needed, primary first. Body drops to **16px**.

**Vertical spacing:** top padding **96px** below 920, **140px** at `md` and up (hero top, [11-layout-and-grid.md](11-layout-and-grid.md)). Bottom padding is the standard section rhythm (72 / 120).

**Copy slots**

| Slot | Limit |
|------|-------|
| Eyebrow | ≤ 28 chars |
| H1 | ≤ 60 chars |
| Sub | ≤ 140 chars |
| Primary CTA label | ≤ 14 chars for purchase; ≤ 20 for planned interest |
| Ghost CTA label | ≤ 24 chars |

**Imagery rule:** exactly one product visual, either a single **disc** or a **trading-card fan**, never both. The disc is built per [05-product-system.md](05-product-system.md) (Ø = 50% of its card, wings 50% of the disc, no glow). No screenshot in the hero.

---

## 3 · Feature row

A single capability: one claim, one paragraph, one screenshot. Repeat the section with the media side alternating.

**Anatomy** ([07-ui-components.md](07-ui-components.md), [12-states-and-forms.md](12-states-and-forms.md)): optional eyebrow, H2, body paragraph, optional text-CTA, and one media panel (a product screenshot). Media panel radius **14** (`--mz-r-tile`), the window frame per [18-imagery-and-og.md](18-imagery-and-og.md), with `--mz-border` and `--mz-shadow-card`; a radius 20 outer card wrapped around the frame is an Olli option, not the default.

**Desktop layout (≥920):** two columns inside 1160, gap **48px** (`--mz-s-7`). Media occupies one column, text the other. **Media side alternates** row to row (left, then right, then left) via grid placement, not source reordering. H2 uses the fluid web-layer `clamp(1.75rem, 4.5vw, 2.5rem)` ([11-layout-and-grid.md](11-layout-and-grid.md)).

**Mobile layout (<920):** stacks to one column in **source order: text block, then media**, so the claim leads on a phone and the desktop alternation never changes what stacks first ([11-layout-and-grid.md](11-layout-and-grid.md) · Stacking). Body **16px**.

**Vertical spacing:** section rhythm, 72 / 120.

**Copy slots**

| Slot | Limit |
|------|-------|
| Eyebrow | ≤ 24 chars |
| Heading (H2) | ≤ 48 chars |
| Body | ≤ 180 chars |
| Feature bullet (each, up to 3) | ≤ 48 chars |
| Text-CTA | ≤ 24 chars |

**Imagery rule:** exactly one product **screenshot**, treated per [18-imagery-and-og.md](18-imagery-and-og.md) (crop, window frame, corner radius, shadow). One screenshot per row, no disc, no gradient behind it.

---

## 4 · Suite grid

The four products in one grid: AI OS, Aurora, Prism, Forge (roster per [../products.json](../products.json)).

**Anatomy** ([05-product-system.md](05-product-system.md), [07-ui-components.md](07-ui-components.md)): optional section eyebrow + H2, then **four disc cards**. Each card: a **disc at 50% of the card width** (wings 50% of the disc), the product **name**, its **function** label, and a **status chip** (chip radius **8**, `--mz-r-chip`, `--mz-border` fill, ink label). Optional one-line body and a text-CTA.

**Desktop layout:** the suite-grid ladder from [11-layout-and-grid.md](11-layout-and-grid.md): **four** columns at `lg` (1200), **two** at `md` (920), **one** below. Column and row gap **24px** (`--mz-s-5`). Cards are white, radius **20** (`--mz-r-card`), inside the 1160 container.

**Mobile layout (<920):** one column, cards full-width within the gutters, gap **24px** (`--mz-s-5`).

**Vertical spacing:** section rhythm, 72 / 120.

**Copy slots (per card)**

| Slot | Limit | Note |
|------|-------|------|
| Section eyebrow | ≤ 24 chars | Section-level, optional. |
| Section heading (H2) | ≤ 48 chars | Section-level, optional. |
| Product name | ≤ 16 chars | e.g. "AI OS" ([../products.json](../products.json)). |
| Function label | ≤ 28 chars | e.g. "AI OPERATING SYSTEM". |
| Status chip | ≤ 12 chars | Maps to `status` in [../products.json](../products.json) (LIVE / PLANNED). |
| Card body | ≤ 60 chars | One line. |
| Card text-CTA | ≤ 20 chars | e.g. "Get the AI OS →". Never a price on a card. |

**Imagery rule:** one **disc** per card ([05-product-system.md](05-product-system.md)), each product wearing its own core gradient ([02-gradients.md](02-gradients.md)). No sphere, no glow, no screenshot in this grid.

---

## 5 · Pricing moment

Where the price is shown plainly. This is the single section that carries a price: product cards never do (see [05-product-system.md](05-product-system.md)), but the pricing section is the pricing section.

**Anatomy** ([07-ui-components.md](07-ui-components.md)): one **white card** (radius **20**, `--mz-r-card`, `--mz-border`, `--mz-shadow-card`) holding an optional eyebrow + heading, the **price shown plainly** as `$99 · one-time`, an **inclusions list** (ticked lines or chips, chip radius **8**), a **primary ink pill CTA**, and a **GST note** for AU buyers.

**Desktop layout (≥920):** one card, centred inside the 1160 container, capped to a comfortable reading measure (never wider than the container). Card padding **48px** (`--mz-s-7`). Order inside: eyebrow → heading → price → inclusions → CTA → GST note.

**Mobile layout (<920):** the card goes full-width within the gutters, padding **24px** (`--mz-s-5`), same source order stacked.

**Vertical spacing:** section rhythm, 72 / 120.

**Copy slots**

| Slot | Limit |
|------|-------|
| Eyebrow | ≤ 24 chars |
| Heading | ≤ 40 chars |
| Price string | ≤ 16 chars (plain "$99 · one-time") |
| Price caption | ≤ 48 chars |
| Inclusion item (each, up to 6) | ≤ 48 chars |
| CTA label | ≤ 14 chars for purchase; ≤ 20 for planned interest |
| GST note | ≤ 80 chars |

**Imagery rule:** no product art required. The card is monochrome; the only accent allowed is a single small **disc** ([05-product-system.md](05-product-system.md)) if the card needs a product mark. The GST note for AU buyers is handled per [15-commerce.md](15-commerce.md) (when to show it, exact wording, tax-inclusive display).

---

## 6 · FAQ

An accordion, one item open at a time.

**Anatomy** ([07-ui-components.md](07-ui-components.md), [12-states-and-forms.md](12-states-and-forms.md)): a section heading, then a stack of native `details` items. Each `summary` is the question control with an **ink chevron** at the trailing edge and a collapsible answer body. Item radius **8** (`--mz-r-chip`), hairline `--mz-border` between items. Enter and Space toggle the focused summary; the implementation includes a small keyboard fallback so this remains deterministic in embedded browsers. Opening one item closes the prior item in the same named group.

**Desktop layout:** a single column, centred inside 1160 and capped to a readable measure. Question row padding **16px** vertical (`--mz-s-4`), inner gap **24px** (`--mz-s-5`) between rows if separated. The chevron is ink `#0D0D0D`, rotating on open via the `var(--mz-duration) var(--mz-ease)` transform transition ([12-states-and-forms.md](12-states-and-forms.md)); the question button carries the `:focus-visible` ink ring. **One open at a time:** opening an item closes the previously open one.

**Mobile layout (<920):** identical single column, full-width within the gutters. Answer body **16px**.

**Vertical spacing:** section rhythm, 72 / 120.

**Copy slots**

| Slot | Limit |
|------|-------|
| Section heading | ≤ 40 chars |
| Question (each, up to 8) | ≤ 80 chars |
| Answer (each) | ≤ 280 chars |

**Imagery rule:** none. Text and the ink chevron only. No disc, no screenshot.

---

## 7 · CTA band

A closing dark panel that repeats the primary action.

**Anatomy** ([12-states-and-forms.md](12-states-and-forms.md) · dark-surface tokens, [05-product-system.md](05-product-system.md)): a **dark `#0D0D0D` panel**, radius **28** (`--mz-r-panel`), holding an eyebrow, a heading, a sub-line and a primary CTA, with **one disc allowed** as an accent. All text uses the dark-surface set: `--mz-dark-text` (primary), `--mz-dark-text-2` (sub), `--mz-dark-muted` (eyebrow/meta), hairlines `--mz-dark-border`, focus ring `--mz-focus-ring-dark` (white at 50%). On this dark surface the CTA pill inverts to a **white pill** (`--mz-card` fill, ink label) so it reads; the label stays "Get the AI OS".

**Desktop layout (≥920):** the panel sits inside the 1160 container, content centred. Panel padding **64px** (`--mz-s-8`). The disc, if used, sits to one side of the centred lockup as an accent.

**Mobile layout (<920):** panel full-width within the gutters, radius **28** held, padding **32px** (`--mz-s-6`), content stacked and centred. The disc may shrink or drop; the CTA never drops.

**Vertical spacing:** the band sits within the section rhythm (72 / 120 around it). This is a **dark section, not a theme**: the page stays light ([12-states-and-forms.md](12-states-and-forms.md) · Light-only, LOCKED).

**Copy slots**

| Slot | Limit |
|------|-------|
| Eyebrow | ≤ 24 chars |
| Heading | ≤ 52 chars |
| Sub | ≤ 120 chars |
| CTA label | ≤ 14 chars for purchase; ≤ 20 for planned interest |

**Imagery rule:** at most one **disc** ([05-product-system.md](05-product-system.md)) as an accent. Never a gradient background behind the band: the panel stays near-black ([01-colour.md](01-colour.md)).

---

## 8 · Footer

The endorsement, the link columns, the legal row.

**Anatomy** ([04-the-mark.md](04-the-mark.md), [12-states-and-forms.md](12-states-and-forms.md)): a brand block (wings + wordmark + the endorsement **"A Mez Studios company"**), a set of link columns, and a **slim legal row** beneath. Links follow [12-states-and-forms.md](12-states-and-forms.md). The footer is a light surface: page `#F8F8F8` or the recessed `#F6F5F4` panel; the site is light-only.

**Desktop layout (≥920):** inside the 1160 container, a brand column plus up to **four** link columns in a row, gap **32px** (`--mz-s-6`). The legal row spans full width beneath, separated by a `--mz-border` top hairline, set in caption text (`--mz-caption`, `--mz-text-muted`).

**Mobile layout (<920):** stacks to one column in source order: brand block → each link column → legal row. Gap **24px** (`--mz-s-5`).

**Vertical spacing:** section rhythm, 72 / 120. The legal row adds its own top hairline, not extra section padding.

**Copy slots**

| Slot | Limit |
|------|-------|
| Endorsement | ≤ 24 chars (locked "A Mez Studios company") |
| Column heading (each, up to 4) | ≤ 20 chars |
| Link label (each, up to 6 per column) | ≤ 24 chars |
| Legal line | ≤ 80 chars |

**Imagery rule:** the wings mark only ([04-the-mark.md](04-the-mark.md)). No product art, no screenshot.

---

## 9 · Quote band

The lightest possible social proof: one pull-quote, no slider, no logo wall, no star ratings. A light section variant, monochrome. Folded in from [14-page-archetypes.md](14-page-archetypes.md); used by the product archetype.

**Anatomy** ([07-ui-components.md](07-ui-components.md), [03-typography.md](03-typography.md)): a single large **pull-quote** set in the accent serif (**Instrument Serif italic**, [03-typography.md](03-typography.md)) at heading scale, an **attribution line** beneath in caption (**13px**, `--mz-caption`) ink, and an optional small **disc** or **wings** mark. The serif pull-quote is the page's one permitted serif accent ([03-typography.md](03-typography.md): one use per page). No card chrome is required: the quote sits on the page surface, or on the recessed `#F6F5F4` panel (radius **28**, `--mz-r-panel`) if a container is wanted.

**Desktop layout (≥920):** one centred column inside the 1160 container, capped to a readable measure. The quote leads; the attribution follows on its own line in caption ink.

**Mobile layout (<920):** identical single column, full-width within the gutters. The quote scales with the fluid h2 clamp (`clamp(1.75rem, 4.5vw, 2.5rem)`, [11-layout-and-grid.md](11-layout-and-grid.md)); attribution stays caption.

**Vertical spacing:** section rhythm, 72 / 120.

**Copy slots**

| Slot | Limit |
|------|-------|
| Pull-quote | ≤ 140 chars |
| Attribution | ≤ 48 chars |

**Imagery rule:** none required. At most one small **disc** or the **wings** mark as an accent. No portrait photo, no logo, no rating stars.

---

## 10 · Gradient strip

One product core, shown across three surfaces in a row: a landing card, a checkout summary, and an email header, all wearing the same gradient. It proves the "one core, many surfaces" idea visually, in one glance. It is a strip, not a feature row: three small mocks side by side under one heading, no alternating text column. Folded in from [14-page-archetypes.md](14-page-archetypes.md); used by the home archetype. Visual source in Figma: the "05 · Gradient in context" section ([08-figma-map.md](08-figma-map.md)) and board **`176:47`**, with the AI OS in-context board **`309:41`** as the per-product reference.

**Anatomy** ([05-product-system.md](05-product-system.md), [07-ui-components.md](07-ui-components.md)): an optional eyebrow + H2, then **three surface mocks** in a row: (1) a **landing card** (a product disc card), (2) a **checkout summary** (a mono card with the price line), (3) an **email header** (the wings + wordmark on the product gradient). All three carry the same core gradient. Mocks sit on tiles (radius **14**, `--mz-r-tile`) or cards (radius **20**, `--mz-r-card`) with `--mz-border` and `--mz-shadow-card`.

**Desktop layout (≥920):** the three mocks in a **three-column** row inside the 1160 container, gap **24px** (`--mz-s-5`), optional heading centred above. The strip may sit on the page or inside a recessed `#F6F5F4` panel (radius **28**).

**Mobile layout (<920):** stacks to **one column** in source order (landing, checkout, email), gap **24px**. The heading leads.

**Vertical spacing:** section rhythm, 72 / 120.

**Copy slots**

| Slot | Limit |
|------|-------|
| Eyebrow | ≤ 24 chars |
| Heading (H2) | ≤ 48 chars |
| Surface label (each, 3) | ≤ 20 chars |

**Imagery rule:** exactly **three** surface mocks, all wearing the **same** product core gradient ([02-gradients.md](02-gradients.md)). The gradient is only ever shown through a surface, never as a bare background behind the strip ([02-gradients.md](02-gradients.md) · Rules).

---

## The rule

> **Eight core sections, one geometry.** Every Mez Systems page is composed from these eight (plus quote-band and gradient-strip, sections 9 and 10, where an archetype calls for them), each drawn inside the 1160 container, stacked below 920 in source order, and spaced on the 72 / 120 rhythm. Copy lives inside the slot limits; layout numbers come from [11-layout-and-grid.md](11-layout-and-grid.md), [07-ui-components.md](07-ui-components.md), [12-states-and-forms.md](12-states-and-forms.md) or the tokens. The nav's 66px height and its `rgba(248,248,248,.78)` tint are the only bespoke numbers on the page. A section that invents its own is off-system.

## Sections (machine readable)

```json
{
  "sections": [
    {
      "id": "nav",
      "status": "DEFAULT",
      "copySlots": [
        { "slot": "wordmark", "maxChars": 16 },
        { "slot": "navLink", "maxChars": 14, "count": 2, "note": "Products · Pricing default (OPEN, flag to Olli)" },
        { "slot": "ctaLabel", "maxChars": 14, "note": "locked 'Get the AI OS'" }
      ],
      "columns": { "base": 1, "md": 1, "lg": 1 },
      "spacing": {
        "height": 66,
        "gutter": { "base": 24, "md": 32 },
        "backdropBlur": 12,
        "backdropTint": "rgba(248,248,248,.78)",
        "onRhythm": false
      },
      "mobile": { "linksToSheet": true, "ctaStaysVisible": true, "wingsOnlyBelow": 400, "menuTarget": 44, "sheetLinkTarget": 44, "keyboard": ["focus first link on open", "Escape closes and returns focus", "link activation closes", "outside click closes"] },
      "imagery": "wings mark only"
    },
    {
      "id": "hero",
      "status": "DEFAULT",
      "copySlots": [
        { "slot": "eyebrow", "maxChars": 28 },
        { "slot": "h1", "maxChars": 60 },
        { "slot": "sub", "maxChars": 140 },
        { "slot": "ctaPrimary", "maxChars": 20, "note": "purchase maximum 14 for 'Get the AI OS'; planned-interest maximum 20 for 'Join the waitlist'" },
        { "slot": "ctaGhost", "maxChars": 24 }
      ],
      "columns": { "base": 1, "md": 2, "lg": 2 },
      "spacing": { "paddingTop": { "base": 96, "md": 140 }, "paddingBottom": { "base": 72, "md": 120 }, "columnGap": 48 },
      "mobile": { "stackBelow": 920, "order": "source: eyebrow, h1, sub, ctaPair, visual" },
      "imagery": "one disc OR one trading-card fan, never both; no screenshot"
    },
    {
      "id": "feature-row",
      "status": "DEFAULT",
      "copySlots": [
        { "slot": "eyebrow", "maxChars": 24 },
        { "slot": "heading", "maxChars": 48 },
        { "slot": "body", "maxChars": 180 },
        { "slot": "bullet", "maxChars": 48, "count": 3 },
        { "slot": "textCta", "maxChars": 24 }
      ],
      "columns": { "base": 1, "md": 2, "lg": 2 },
      "spacing": { "paddingY": { "base": 72, "md": 120 }, "columnGap": 48, "mediaRadius": 14, "mediaRadiusNote": "Window frame per 18-imagery-and-og.md; a radius 20 outer card is an Olli option" },
      "mobile": { "stackBelow": 920, "order": "source: text then media", "mediaSideAlternatesDesktopOnly": true },
      "imagery": "one screenshot per row, treatment per 18-imagery-and-og.md"
    },
    {
      "id": "suite-grid",
      "status": "DEFAULT",
      "copySlots": [
        { "slot": "sectionEyebrow", "maxChars": 24 },
        { "slot": "sectionHeading", "maxChars": 48 },
        { "slot": "productName", "maxChars": 16 },
        { "slot": "functionLabel", "maxChars": 28 },
        { "slot": "statusChip", "maxChars": 12, "note": "maps to products.json status" },
        { "slot": "cardBody", "maxChars": 60 },
        { "slot": "cardTextCta", "maxChars": 20 }
      ],
      "columns": { "base": 1, "md": 2, "lg": 4 },
      "spacing": { "paddingY": { "base": 72, "md": 120 }, "gridGap": 24, "cardRadius": 20, "discPctOfCard": 50 },
      "mobile": { "stackBelow": 920, "columns": 1 },
      "imagery": "one disc per card, product core gradient"
    },
    {
      "id": "pricing-moment",
      "status": "DEFAULT",
      "copySlots": [
        { "slot": "eyebrow", "maxChars": 24 },
        { "slot": "heading", "maxChars": 40 },
        { "slot": "priceString", "maxChars": 16, "note": "plain '$99 · one-time'" },
        { "slot": "priceCaption", "maxChars": 48 },
        { "slot": "inclusion", "maxChars": 48, "count": 6 },
        { "slot": "ctaLabel", "maxChars": 20, "note": "purchase maximum 14 for 'Get the AI OS'; planned-interest maximum 20 for 'Join the waitlist'" },
        { "slot": "gstNote", "maxChars": 80 }
      ],
      "columns": { "base": 1, "md": 1, "lg": 1 },
      "spacing": { "paddingY": { "base": 72, "md": 120 }, "cardPadding": { "base": 24, "md": 48 }, "cardRadius": 20 },
      "mobile": { "stackBelow": 920, "cardFullWidth": true },
      "imagery": "monochrome card, at most one small disc; GST per 15-commerce.md"
    },
    {
      "id": "faq",
      "status": "DEFAULT",
      "copySlots": [
        { "slot": "sectionHeading", "maxChars": 40 },
        { "slot": "question", "maxChars": 80, "count": 8 },
        { "slot": "answer", "maxChars": 280 }
      ],
      "columns": { "base": 1, "md": 1, "lg": 1 },
      "spacing": { "paddingY": { "base": 72, "md": 120 }, "itemRadius": 8, "rowPaddingY": 16, "rowGap": 24 },
      "mobile": { "stackBelow": 920, "columns": 1 },
      "behaviour": "native details/summary; Enter and Space keyboard fallback; one open at a time; ink chevron; var(--mz-duration) var(--mz-ease) rotate",
      "imagery": "none"
    },
    {
      "id": "cta-band",
      "status": "DEFAULT",
      "copySlots": [
        { "slot": "eyebrow", "maxChars": 24 },
        { "slot": "heading", "maxChars": 52 },
        { "slot": "sub", "maxChars": 120 },
        { "slot": "ctaLabel", "maxChars": 20, "note": "purchase maximum 14 for 'Get the AI OS'; planned-interest maximum 20 for 'Join the waitlist'; inverts to white pill on dark" }
      ],
      "columns": { "base": 1, "md": 1, "lg": 1 },
      "spacing": { "paddingY": { "base": 72, "md": 120 }, "panelPadding": { "base": 32, "md": 64 }, "panelRadius": 28 },
      "surface": { "background": "#0D0D0D", "tokens": "dark-surface set (12-states-and-forms.md)", "note": "section treatment, not a theme; site stays light" },
      "mobile": { "stackBelow": 920, "discOptional": true, "ctaAlwaysVisible": true },
      "imagery": "at most one disc; never a gradient background"
    },
    {
      "id": "footer",
      "status": "DEFAULT",
      "copySlots": [
        { "slot": "endorsement", "maxChars": 24, "note": "locked 'A Mez Studios company'" },
        { "slot": "columnHeading", "maxChars": 20, "count": 4 },
        { "slot": "linkLabel", "maxChars": 24, "count": 6, "note": "per column" },
        { "slot": "legalLine", "maxChars": 80 }
      ],
      "columns": { "base": 1, "md": 5, "lg": 5, "note": "brand column + up to 4 link columns" },
      "spacing": { "paddingY": { "base": 72, "md": 120 }, "columnGap": { "base": 24, "md": 32 }, "legalHairline": "--mz-border top" },
      "mobile": { "stackBelow": 920, "order": "source: brand, link columns, legal" },
      "imagery": "wings mark only"
    },
    {
      "id": "quote-band",
      "status": "DEFAULT",
      "note": "Folded in from 14-page-archetypes.md. Social proof: one serif pull-quote, monochrome, light section. Used by the product archetype.",
      "copySlots": [
        { "slot": "pullQuote", "maxChars": 140, "note": "Instrument Serif italic, accent serif (one per page)" },
        { "slot": "attribution", "maxChars": 48, "note": "caption 13px ink" }
      ],
      "columns": { "base": 1, "md": 1, "lg": 1 },
      "spacing": { "paddingY": { "base": 72, "md": 120 } },
      "surface": { "options": ["page #F8F8F8", "#F6F5F4 panel radius 28"], "note": "light section, monochrome, no card chrome required" },
      "imagery": "none required; at most one small disc or the wings mark; no portrait, no logo, no stars"
    },
    {
      "id": "gradient-strip",
      "status": "DEFAULT",
      "note": "Folded in from 14-page-archetypes.md. Gradient in context: one core across three surfaces (landing card, checkout summary, email header). Used by the home archetype.",
      "figmaSource": ["176:47", "309:41"],
      "copySlots": [
        { "slot": "eyebrow", "maxChars": 24 },
        { "slot": "heading", "maxChars": 48 },
        { "slot": "surfaceLabel", "maxChars": 20, "count": 3 }
      ],
      "columns": { "base": 1, "md": 3, "lg": 3 },
      "spacing": { "paddingY": { "base": 72, "md": 120 }, "gridGap": 24, "mockRadius": [14, 20] },
      "mobile": { "stackBelow": 920, "order": "source: landing, checkout, email" },
      "imagery": "exactly three surface mocks, all wearing the same product core gradient; gradient only ever through a surface, never a bare background"
    }
  ]
}
```
