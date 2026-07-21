# 14 · Page archetypes

Status: DEFAULT · working values, flag deviations to Olli

[13-sections.md](13-sections.md) gave the pack eight fully specified sections. It did not say which sections go on which page, or in what order. Given the tokens and the sections but no composition map, a build decides the page structure itself, and the default an LLM reaches for is a generic SaaS stack: hero, three feature cards, logos, pricing, testimonial slider, CTA. This doc removes that decision. It pins the ordered section list for every page type Mez Systems ships. Build a page by reading its archetype here, then composing the named sections from [13-sections.md](13-sections.md) in the order given. A page whose section order is not one of these is off-system.

Every id in an ordered list is one of the sections in [13-sections.md](13-sections.md), used exactly. Two of them, **quote-band** (social proof) and **gradient-strip** (gradient in context), were first specified here and are now folded into [13-sections.md](13-sections.md) as its sections 9 and 10. They are still detailed in full below for the archetypes that use them, and their numbers now agree with 13. Utility pages (checkout, success, 404, legal) reuse the core sections in **reduced** form plus a small typography recipe, never a new section.

Layout, rhythm, breakpoints and stacking come from [11-layout-and-grid.md](11-layout-and-grid.md); section anatomy and copy slots from [13-sections.md](13-sections.md); states, forms and the dark-surface set from [12-states-and-forms.md](12-states-and-forms.md); the product roster from [../products.json](../products.json). No new layout number is introduced here.

## Conventions used below

- **Ordered sections** lists section ids from [13-sections.md](13-sections.md) top to bottom. A build renders them in exactly that order.
- **Reduced nav** is the [13-sections.md](13-sections.md) nav (66px band, `rgba(248,248,248,.78)` tint) with the two text links and the CTA removed, leaving only the wings + wordmark lockup, which links home. Same id (`nav`), a documented variant.
- **Slim footer** is the [13-sections.md](13-sections.md) footer with the link columns dropped, leaving the brand block (wings + wordmark + endorsement) and the legal row. Same id (`footer`), a documented variant.
- **Meta title** follows the formula `{Page} · Mez Systems`. Home is the one exception (a page titled "Home" is never useful), and leads with the brand.
- **Meta description** is a per-archetype formula, capped at **155 characters** including spaces. Each archetype below gives the formula and one concrete example with its character count.
- **OG image slot** names the intended subject only. Dimensions, safe area, and treatment are set in [18-imagery-and-og.md](18-imagery-and-og.md); where an archetype has no product to show, use the default brand OG (wings + wordmark on the light page).
- **Commerce surfaces** (checkout, success, GST, planned-product actions) defer to [15-commerce.md](15-commerce.md) for the exact fields, wording and tax display.

---

## 1 · Home / suite

The front door. It sells the suite, not one product: one chassis, four product cores, one place. It opens with the whole set as a deck and closes with the bundle.

**Ordered sections**

| # | Section | Variant / note |
|---|---------|----------------|
| 1 | `nav` | Full nav. |
| 2 | `hero` | **Trading-card fan** visual (the suite as a deck, offset 50 across / 38 down, [06-trading-cards-and-stacks.md](06-trading-cards-and-stacks.md)), never a single disc. |
| 3 | `suite-grid` | The four disc cards: AI OS, Aurora, Prism, Forge ([05-product-system.md](05-product-system.md), [../products.json](../products.json)). |
| 4 | `gradient-strip` | Section 10 in [13-sections.md](13-sections.md) (specified below). One core across three surfaces. |
| 5 | `cta-band` | **Dark bundle** variant: the dark `#0D0D0D` panel carries a **trading-card stack / bundle** as its accent instead of a single disc ([06-trading-cards-and-stacks.md](06-trading-cards-and-stacks.md)). CTA stays "Get the AI OS". |
| 6 | `faq` | Suite-level questions. |
| 7 | `footer` | Full footer. |

**Fixed:** the section order and count; every layout number; the trading-card fan in the hero; the four-card roster and its order in the suite grid; the dark bundle band; "Get the AI OS" as the only CTA label; "A Mez Studios company" in the footer.

**Varies:** the home copy (eyebrow, H1, sub, FAQ, band copy); which product core leads the hero fan and the strip (default AI OS, `MZ-G13`); the suite-grid status chips as products go LIVE ([../products.json](../products.json)).

**Meta**

- Title: `Mez Systems · {suite promise}`. Example: `Mez Systems · One chassis, four cores` (38 chars).
- Description formula: `Mez Systems builds {suite promise}. One chassis, four product cores: AI OS, Aurora, Prism, Forge. Get the AI OS. A Mez Studios company.`
- Description example: `Mez Systems builds AI systems for solo operators. One chassis, four product cores: AI OS, Aurora, Prism, Forge. Get the AI OS. A Mez Studios company.` (150 chars).
- OG slot: the suite as a trading-card fan (four cores) on the light page, wings + "Mez Systems".

---

## 2 · Product page

**One template, four products.** There is a single product-page archetype. AI OS, Aurora, Prism and Forge all render it. Only **copy**, **screenshots** and the **product core** change from one product to the next: the structure, the geometry and the component set are identical. Build the template once; a new product is a new content set poured into it, never a new layout.

**Ordered sections**

| # | Section | Variant / note |
|---|---------|----------------|
| 1 | `nav` | Full nav. |
| 2 | `hero` | **Disc** visual: this product's disc, wearing its core gradient ([05-product-system.md](05-product-system.md)). Never the fan. |
| 3 | `feature-row` | Feature 1. Media on the left. |
| 4 | `feature-row` | Feature 2. Media on the right (alternation is desktop-only, [13-sections.md](13-sections.md) · Feature row). |
| 5 | `feature-row` | Feature 3. Media on the left. |
| 6 | `quote-band` | Section 9 in [13-sections.md](13-sections.md) (specified below). Social proof: one pull-quote. |
| 7 | `pricing-moment` | The price, plainly. Live product only shows a price; planned products show a status line, never a price (see Varies). |
| 8 | `faq` | Product-level questions. |
| 9 | `cta-band` | Standard closing dark band, one disc accent, "Get the AI OS" on the AI OS page (see Varies for planned products). |
| 10 | `footer` | Full footer. |

**Fixed across all four products**

- The section order and count above (10 sections, three feature rows).
- Every layout number: the 1160 container, the 72 / 120 rhythm, the 48px column gaps, all breakpoints ([11-layout-and-grid.md](11-layout-and-grid.md)).
- The nav content: wings + "Mez Systems" wordmark, `Products · Pricing` links, the "Get the AI OS" CTA.
- The hero uses the **disc** treatment, built to the locked recipe (Ø = 50% of its card, wings = 50% of the disc, no glow, [05-product-system.md](05-product-system.md)).
- The feature-row alternation pattern (left, right, left).
- The dark `#0D0D0D` cta-band and its dark-surface tokens ([12-states-and-forms.md](12-states-and-forms.md)).
- The footer: link columns, "A Mez Studios company" endorsement, legal row.
- Every copy-slot limit from [13-sections.md](13-sections.md).
- Typography, colour, radius, spacing, shadows (the token files).

**Varies per product**

- The **product core gradient**, which drives every disc and gradient on the page: AI OS `MZ-G13`, Aurora `MZ-G20`, Prism `MZ-G06`, Forge `MZ-G15` ([02-gradients.md](02-gradients.md), [../products.json](../products.json)).
- The **product name** and **function label**: AI OS / Aurora / Prism / Forge and their functions.
- All **copy**: hero eyebrow, H1 and sub; the three feature headings and bodies; the FAQ; the pull-quote text and attribution.
- The three **feature-row screenshots** (treatment per [18-imagery-and-og.md](18-imagery-and-og.md)).
- The **status**, which changes two sections:
  - **pricing-moment.** AI OS is `live` and shows `$99 · one-time` plus the AU GST note ([15-commerce.md](15-commerce.md)). Aurora, Prism and Forge are `planned` and carry **no price**: the section becomes a status line ("In build" / "Join the waitlist"), never a dollar figure ([../products.json](../products.json)).
  - **cta-band and hero CTA.** On the AI OS page the CTA is the locked "Get the AI OS". A planned product cannot use that label; its primary action is a status-appropriate CTA ("Join the waitlist"), still the same pill component, still **never a price**. The non-AI-OS CTA wording is a **DEFAULT**, flag the exact words to Olli ([09-governance.md](09-governance.md)).
- The **status chip** on any product pill or card (LIVE / PLANNED, [../products.json](../products.json)).

**Meta**

- Title: `{Name} · Mez Systems`. Example: `AI OS · Mez Systems` (19 chars).
- Description formula: `{Name} is the {function} for solo operators. {one-line value}. {price line | status line}. {product CTA}. A Mez Systems product.`
- Description example (AI OS, live): `AI OS is the AI Operating System for solo operators. One core, one workspace, $99 one-time. Get the AI OS. A Mez Systems product.` (129 chars).
- Description example (Forge, planned): `Forge is the Claude Code OS for solo operators. Part of the Mez Systems suite, in build now. Join the waitlist. A Mez Systems product.` (134 chars).
- OG slot: this product's disc (or trading card) on the light page, wearing its core gradient, with the product name and function.

---

## Two sections folded into 13

Two sections the archetypes above need. They were first written here and are now folded into [13-sections.md](13-sections.md) (sections 9 and 10). Each is specified to the same shape as the eight core sections, and is kept here in full for the archetypes that use it.

### quote-band (social proof)

`now section 9 in 13-sections.md`

The lightest possible social proof: one pull-quote, no slider, no logo wall, no star ratings. A light section variant, monochrome.

**Anatomy** ([07-ui-components.md](07-ui-components.md), [12-states-and-forms.md](12-states-and-forms.md)): a single large **pull-quote** set in the accent serif (Instrument Serif, [03-typography.md](03-typography.md)) at heading scale, an **attribution line** beneath (name, role), and an optional small **disc** or **wings** mark. No card chrome is required: the quote sits on the page surface, or on the recessed `#F6F5F4` panel (radius 28, `--mz-r-panel`) if a container is wanted.

**Desktop layout (≥920):** one centred column inside the 1160 container, capped to a readable measure. The quote leads; the attribution follows on its own line in caption or body ink.

**Mobile layout (<920):** identical single column, full-width within the gutters. Quote scales with the fluid h2 clamp; attribution stays body / caption.

**Vertical spacing:** section rhythm, 72 / 120.

**Copy slots**

| Slot | Limit |
|------|-------|
| Pull-quote | ≤ 140 chars |
| Attribution | ≤ 48 chars |

**Imagery rule:** none required. At most one small **disc** or the **wings** mark as an accent. No portrait photo, no logo, no rating stars.

### gradient-strip (gradient in context)

`now section 10 in 13-sections.md`

One product core, shown across three surfaces in a row: a landing card, a checkout summary, and an email header, all wearing the same gradient. It proves the "one core, many surfaces" idea visually, in one glance. It is a strip, not a feature row: three small mocks side by side under one heading, no alternating text column.

Visual source in Figma: the planned "05 · Gradient in context" section ([08-figma-map.md](08-figma-map.md), landing / checkout / email) and board **`176:47`**, with the AI OS in-context board **`309:41`** on the Products page as the per-product reference.

**Anatomy** ([05-product-system.md](05-product-system.md), [07-ui-components.md](07-ui-components.md)): an optional eyebrow + H2, then **three surface mocks** in a row: (1) a **landing card** (a product disc card), (2) a **checkout summary** (a mono card with the price line), (3) an **email header** (the wings + wordmark on the product gradient). All three carry the same core gradient. Mocks sit on tiles (radius 14, `--mz-r-tile`) or cards (radius 20, `--mz-r-card`) with `--mz-border` and `--mz-shadow-card`.

**Desktop layout (≥920):** the three mocks in a **three-column** row inside the 1160 container, gap 24px (`--mz-s-5`), optional heading centred above. The strip may sit on the page or inside a recessed `#F6F5F4` panel (radius 28).

**Mobile layout (<920):** stacks to **one column** in source order (landing, checkout, email), gap 24px. The heading leads.

**Vertical spacing:** section rhythm, 72 / 120.

**Copy slots**

| Slot | Limit |
|------|-------|
| Eyebrow | ≤ 24 chars |
| Heading (H2) | ≤ 48 chars |
| Surface label (each, 3) | ≤ 20 chars |

**Imagery rule:** exactly **three** surface mocks, all wearing the **same** product core gradient ([02-gradients.md](02-gradients.md)). The gradient is only ever shown through a surface, never as a bare background behind the strip ([02-gradients.md](02-gradients.md) · Rules).

---

## 3 · Checkout entry

The page that takes the order and hands off to payment. A commerce surface: the exact fields, the pay control and the GST display come from [15-commerce.md](15-commerce.md). The archetype gives it the shell and the summary.

**Ordered sections**

| # | Section | Variant / note |
|---|---------|----------------|
| 1 | `nav` | **Reduced**: wings + wordmark only, links home. No links, no CTA. |
| 2 | `pricing-moment` | The **order summary**: the price shown plainly (`$99 · one-time`), the inclusions list, the AU GST note. The primary control is the **pay / continue** action per [15-commerce.md](15-commerce.md), not "Get the AI OS". |
| 3 | `footer` | **Slim**: brand block + legal row only. |

**Fixed:** the shell (reduced nav, slim footer); the price shown plainly with inclusions and the GST note; monochrome surfaces.

**Varies:** the product being bought and its price line; the pay control's exact fields and wording ([15-commerce.md](15-commerce.md)).

**Meta**

- Title: `Checkout · Mez Systems` (22 chars).
- Description formula: `Checkout for {product} by Mez Systems. {price} {tax note}. Secure payment. A Mez Studios company.`
- Description example: `Checkout for the AI OS by Mez Systems. $99 one-time, GST shown for AU buyers. Secure payment. A Mez Studios company.` (116 chars).
- OG slot: default brand OG (wings + wordmark on light). Checkout pages are typically noindex; keep the tag minimal.

---

## 4 · Success

The post-purchase confirmation and the path to access. A commerce surface: what "access" resolves to (link, dashboard, email) comes from [15-commerce.md](15-commerce.md) and the fulfilment pipeline.

**Ordered sections**

| # | Section | Variant / note |
|---|---------|----------------|
| 1 | `nav` | **Reduced**: wings + wordmark, links home. |
| 2 | `cta-band` | **Confirmation** variant: the panel confirms the purchase (heading + sub) and its CTA is the **access** action ("Open your AI OS"), not "Get the AI OS". One disc accent allowed. |
| 3 | `footer` | **Slim**: brand block + legal row only. |

**Fixed:** the shell; a single confirmation panel with one clear next action.

**Varies:** the product bought; the access CTA's destination and wording ([15-commerce.md](15-commerce.md)); the disc's core gradient.

**Meta**

- Title: `You're in · Mez Systems` (23 chars).
- Description formula: `You're in. Your Mez Systems purchase is confirmed and your access is on the way. A Mez Studios company.`
- Description example: `You're in. Your Mez Systems purchase is confirmed and your access is on the way. A Mez Studios company.` (103 chars).
- OG slot: default brand OG. Success pages are noindex; keep the tag minimal.

---

## 5 · 404

Page not found. The brief is exact: **wings, one line, a pill home**. A single centred lockup, nothing more.

This is a **recipe**, not a section stack. The body is not one of the eight sections; it is a bare lockup drawn on the light page.

**The lockup (top to bottom, centred in the 1160 container):**

1. The **wings** mark ([04-the-mark.md](04-the-mark.md)), on the light page surface. No disc, no gradient.
2. **One line** of copy, at h2 scale, ink `#0D0D0D`. One sentence, no paragraph.
3. A single **primary pill** labelled to go home ("Back to Mez Systems"), the near-black CTA pill with its standard button states ([12-states-and-forms.md](12-states-and-forms.md)). This pill replaces the nav; a full nav is not required.

Chrome is optional and minimal: a **slim footer** (legal row) may sit beneath, and a **reduced nav** may sit above, but the pill home is the required navigation. Vertical centring uses the section rhythm as its floor.

**Fixed:** wings + one line + one home pill, centred, on the light page, monochrome. No product art.

**Varies:** the one line of copy only.

**Meta**

- Title: `Page not found · Mez Systems` (28 chars).
- Description formula: `That page has moved or never existed. Head back to Mez Systems. A Mez Studios company.`
- Description example: `That page has moved or never existed. Head back to Mez Systems. A Mez Studios company.` (86 chars).
- OG slot: default brand OG.

---

## 6 · Legal

Privacy, terms, refunds, any long-form policy. **A typography-only recipe:** no product art, no cards, no dark bands. Prose set for reading, inside the chrome.

**Ordered sections**

| # | Section | Variant / note |
|---|---------|----------------|
| 1 | `nav` | **Reduced** or full; reduced is the default. |
| 2 | (body) | The legal prose. A **recipe**, not a section (below). |
| 3 | `footer` | **Slim** or full; slim is the default. |

**The prose recipe:**

- **Measure:** one column, capped to a readable measure (never the full 1160), centred in the container.
- **Type:** body at 16 / 17px per [11-layout-and-grid.md](11-layout-and-grid.md); headings step down the type scale from [03-typography.md](03-typography.md) (h2 for sections, h3 for sub-sections). Inter throughout; the accent serif is not used for legal.
- **Rhythm:** paragraphs and headings on the component spacing steps ([07-ui-components.md](07-ui-components.md)), not the 72 / 120 section rhythm, since it is one continuous body.
- **Colour:** ink `#0D0D0D` body, `--mz-text-muted` for meta (last-updated date). Links follow [12-states-and-forms.md](12-states-and-forms.md) (ink, underline on hover). No functional colour, no gradient.
- **Top matter:** the policy title (h1 or h2) and a "Last updated" line.

**Fixed:** the chrome (reduced nav, slim footer); the reading measure; the type-only treatment; monochrome.

**Varies:** the policy title and the prose.

**Meta**

- Title: `{Policy} · Mez Systems`. Example: `Privacy · Mez Systems` (21 chars).
- Description formula: `The {policy name} for Mez Systems, a Mez Studios company. {one-line scope}.`
- Description example: `The privacy policy for Mez Systems, a Mez Studios company. How we handle your data across the AI OS and the suite.` (114 chars).
- OG slot: default brand OG.

---

## The rule

> **Compose, do not invent.** Every Mez Systems page is one of these archetypes, built by rendering the named sections from [13-sections.md](13-sections.md) in the order given. Home opens on the fan and closes on the bundle; the product page is one template poured with four content sets, its price and CTA changing only with product status; utility pages reuse the core sections in reduced form plus a typography recipe. `quote-band` and `gradient-strip` were first specified here and are now folded into [13-sections.md](13-sections.md) as its sections 9 and 10. A page that invents its own section order, or reaches for a generic testimonial slider or logo wall, is off-system.

## Archetypes (machine readable)

```json
{
  "archetypes": [
    {
      "id": "home",
      "sections": ["nav", "hero", "suite-grid", "gradient-strip", "cta-band", "faq", "footer"],
      "notInThirteen": [],
      "variants": { "hero": "trading-card fan", "cta-band": "dark bundle" },
      "fixed": [
        "section order and count",
        "all layout numbers (11-layout-and-grid)",
        "trading-card fan in hero",
        "four-card suite roster and order",
        "dark bundle cta-band",
        "CTA label 'Get the AI OS'",
        "footer endorsement 'A Mez Studios company'"
      ],
      "varies": [
        "home copy (eyebrow, h1, sub, faq, band)",
        "which product core leads the hero fan and the strip (default AI OS MZ-G13)",
        "suite-grid status chips as products go LIVE"
      ],
      "meta": {
        "titleFormula": "Mez Systems · {suite promise}",
        "titleExample": "Mez Systems · One chassis, four cores",
        "descriptionFormula": "Mez Systems builds {suite promise}. One chassis, four product cores: AI OS, Aurora, Prism, Forge. Get the AI OS. A Mez Studios company.",
        "descriptionExample": "Mez Systems builds AI systems for solo operators. One chassis, four product cores: AI OS, Aurora, Prism, Forge. Get the AI OS. A Mez Studios company.",
        "og": "suite as trading-card fan (four cores) on the light page, wings + 'Mez Systems'"
      }
    },
    {
      "id": "product",
      "note": "ONE template, reused by all four products. Only copy, screenshots and the product core vary.",
      "sections": ["nav", "hero", "feature-row", "feature-row", "feature-row", "quote-band", "pricing-moment", "faq", "cta-band", "footer"],
      "notInThirteen": [],
      "variants": { "hero": "disc", "feature-row": "media alternates left/right/left" },
      "fixed": [
        "section order and count (10 sections, three feature rows)",
        "all layout numbers (11-layout-and-grid)",
        "nav content (wordmark, Products · Pricing, Get the AI OS)",
        "hero disc treatment (locked recipe, no glow)",
        "feature-row alternation left/right/left",
        "dark #0D0D0D cta-band + dark-surface tokens",
        "footer link columns + 'A Mez Studios company' + legal row",
        "all copy-slot limits",
        "typography, colour, radius, spacing, shadows (tokens)"
      ],
      "varies": [
        "product core gradient (AI OS MZ-G13, Aurora MZ-G20, Prism MZ-G06, Forge MZ-G15)",
        "product name and function label",
        "all copy (hero, three features, faq, pull-quote)",
        "three feature-row screenshots",
        "pricing-moment: live shows $99 one-time + GST; planned shows status line, never a price",
        "cta-band and hero CTA: 'Get the AI OS' on AI OS; planned uses 'Join the waitlist' (DEFAULT, flag to Olli), never a price",
        "status chip (LIVE / PLANNED per products.json)"
      ],
      "meta": {
        "titleFormula": "{Name} · Mez Systems",
        "titleExample": "AI OS · Mez Systems",
        "descriptionFormula": "{Name} is the {function} for solo operators. {one-line value}. {price line | status line}. {product CTA}. A Mez Systems product.",
        "descriptionExample": "AI OS is the AI Operating System for solo operators. One core, one workspace, $99 one-time. Get the AI OS. A Mez Systems product.",
        "descriptionExamplePlanned": "Forge is the Claude Code OS for solo operators. Part of the Mez Systems suite, in build now. Join the waitlist. A Mez Systems product.",
        "og": "this product's disc (or trading card) on the light page, wearing its core gradient, with name + function"
      }
    },
    {
      "id": "checkout",
      "sections": ["nav", "pricing-moment", "footer"],
      "notInThirteen": [],
      "variants": { "nav": "reduced (wings + wordmark, links home)", "pricing-moment": "order summary, pay control per 15-commerce", "footer": "slim (brand + legal)" },
      "commerceDefer": "15-commerce.md (fields, pay control, GST display)",
      "fixed": [
        "shell (reduced nav, slim footer)",
        "price shown plainly with inclusions and GST note",
        "monochrome surfaces"
      ],
      "varies": [
        "product being bought and its price line",
        "pay control fields and wording (15-commerce)"
      ],
      "meta": {
        "titleFormula": "Checkout · Mez Systems",
        "titleExample": "Checkout · Mez Systems",
        "descriptionFormula": "Checkout for {product} by Mez Systems. {price} {tax note}. Secure payment. A Mez Studios company.",
        "descriptionExample": "Checkout for the AI OS by Mez Systems. $99 one-time, GST shown for AU buyers. Secure payment. A Mez Studios company.",
        "og": "default brand OG (wings + wordmark on light); page typically noindex"
      }
    },
    {
      "id": "success",
      "sections": ["nav", "cta-band", "footer"],
      "notInThirteen": [],
      "variants": { "nav": "reduced", "cta-band": "confirmation + access CTA (not 'Get the AI OS')", "footer": "slim" },
      "commerceDefer": "15-commerce.md (what 'access' resolves to)",
      "fixed": [
        "shell (reduced nav, slim footer)",
        "single confirmation panel with one clear next action"
      ],
      "varies": [
        "product bought",
        "access CTA destination and wording (15-commerce)",
        "disc core gradient"
      ],
      "meta": {
        "titleFormula": "You're in · Mez Systems",
        "titleExample": "You're in · Mez Systems",
        "descriptionFormula": "You're in. Your Mez Systems purchase is confirmed and your access is on the way. A Mez Studios company.",
        "descriptionExample": "You're in. Your Mez Systems purchase is confirmed and your access is on the way. A Mez Studios company.",
        "og": "default brand OG; page noindex"
      }
    },
    {
      "id": "notfound",
      "sections": ["nav", "footer"],
      "notInThirteen": [],
      "variants": { "nav": "reduced, optional", "footer": "slim, optional" },
      "centre": "recipe, not a section: wings + one line (h2, ink) + one home pill ('Back to Mez Systems'); centred on the light page; monochrome; no product art",
      "fixed": [
        "wings + one line + one home pill, centred, light page, monochrome"
      ],
      "varies": [
        "the one line of copy"
      ],
      "meta": {
        "titleFormula": "Page not found · Mez Systems",
        "titleExample": "Page not found · Mez Systems",
        "descriptionFormula": "That page has moved or never existed. Head back to Mez Systems. A Mez Studios company.",
        "descriptionExample": "That page has moved or never existed. Head back to Mez Systems. A Mez Studios company.",
        "og": "default brand OG"
      }
    },
    {
      "id": "legal",
      "sections": ["nav", "footer"],
      "notInThirteen": [],
      "variants": { "nav": "reduced (default)", "footer": "slim (default)" },
      "body": "typography-only recipe: one column capped to a readable measure; Inter body 16/17; h2/h3 step-down from 03-typography; component spacing not 72/120 rhythm; ink body, muted meta; links per 12-states-and-forms; no gradient, no product art, no accent serif",
      "fixed": [
        "chrome (reduced nav, slim footer)",
        "reading measure",
        "type-only treatment, monochrome"
      ],
      "varies": [
        "policy title and prose"
      ],
      "meta": {
        "titleFormula": "{Policy} · Mez Systems",
        "titleExample": "Privacy · Mez Systems",
        "descriptionFormula": "The {policy name} for Mez Systems, a Mez Studios company. {one-line scope}.",
        "descriptionExample": "The privacy policy for Mez Systems, a Mez Studios company. How we handle your data across the AI OS and the suite.",
        "og": "default brand OG"
      }
    }
  ],
  "addedSections": [
    {
      "id": "quote-band",
      "inThirteen": true,
      "note": "First specified here, now folded into 13-sections.md (section 9).",
      "role": "social proof: one pull-quote, monochrome, light section variant",
      "copySlots": [
        { "slot": "pullQuote", "maxChars": 140 },
        { "slot": "attribution", "maxChars": 48 }
      ],
      "columns": { "base": 1, "md": 1, "lg": 1 },
      "spacing": { "paddingY": { "base": 72, "md": 120 } },
      "imagery": "none required; at most one small disc or the wings mark; no portrait, no logo, no stars"
    },
    {
      "id": "gradient-strip",
      "inThirteen": true,
      "note": "First specified here, now folded into 13-sections.md (section 10).",
      "role": "gradient in context: one core across three surfaces (landing card, checkout summary, email header)",
      "figmaSource": ["176:47", "309:41"],
      "copySlots": [
        { "slot": "eyebrow", "maxChars": 24 },
        { "slot": "heading", "maxChars": 48 },
        { "slot": "surfaceLabel", "maxChars": 20, "count": 3 }
      ],
      "columns": { "base": 1, "md": 3, "lg": 3 },
      "spacing": { "paddingY": { "base": 72, "md": 120 }, "gridGap": 24 },
      "imagery": "exactly three surface mocks, all wearing the same product core gradient; gradient only ever through a surface, never a bare background"
    }
  ]
}
```
