# 15 · Commerce

Status: DEFAULT · working values, flag deviations to Olli

Checkout, the success page and the delivery email are the buyer's last three touchpoints, and for a digital product they are the most-seen brand surfaces of all: a person who buys the AI OS spends more time on the receipt than on the homepage. Until now the pack specified none of them, so a build improvises the one moment where the brand has to feel paid-for. This doc closes that gap. It gives the three commerce surfaces their exact geometry, the canonical price strings, the GST rule by buyer location, and the email's hard constraints. Every surface composes from the eight sections in [13-sections.md](13-sections.md) and the archetypes in [14-page-archetypes.md](14-page-archetypes.md); every number traces to [11-layout-and-grid.md](11-layout-and-grid.md), [12-states-and-forms.md](12-states-and-forms.md), [07-ui-components.md](07-ui-components.md) or the token files. No new layout number is introduced.

## Scope and the do-not-touch rule

> **The live Stripe flow is do-not-touch until Olli schedules the restyle; this spec is the target.** The working checkout in the website repo takes real money and stays exactly as it is. Nothing here edits it. This doc is the design brief for when Olli books the restyle, and the reference for the success page and the delivery email, which are safe to build against now.

Three surfaces, three archetypes:

| Surface | Archetype ([14-page-archetypes.md](14-page-archetypes.md)) | Shell |
|---------|--------------|-------|
| Checkout entry | Checkout | Reduced nav, order summary, slim footer |
| Success | Success | Reduced nav, confirmation panel, slim footer |
| Delivery / receipt email | (email, not a web page) | 600px single column |

## Price display (the canonical strings)

AI OS is **USD $99, one-time, lifetime access, all future updates included**. It is never framed as a subscription: no `/mo`, no "per month", no "renews", no "plan". These strings are the only sanctioned ways to show the price and the offer. They agree with the `$99 · one-time` price string in [13-sections.md](13-sections.md) · Pricing moment and the `$99 one-time` prose in [14-page-archetypes.md](14-page-archetypes.md).

| Slot | String |
|------|--------|
| Product line | `AI OS · $99 one-time · Lifetime access` |
| Updates line | `Includes all future updates` |
| Plain price | `$99 · one-time` |
| Total line | `Total · $99 USD` |
| GST line (AU buyers only) | `Includes 10% GST (AU)` |
| GST line, amount form (AU buyers only) | `Includes 10% GST (AU) · $9.00` |

The headline is **one flat USD $99 for every buyer, anywhere**. Location never changes the number the buyer pays; it only changes whether a GST line appears beneath it.

### GST by buyer location

Mez Studios Pty Ltd is GST-registered in Australia (ABN 21 697 707 190). The price is **GST-inclusive** (`tax_behavior: 'inclusive'` on Stripe): GST is carved out of the $99, never added on top. See [[project_checkout_v2_gst]] for the tax decision.

| Buyer location | What shows | Why |
|----------------|-----------|-----|
| Australia | The GST line: `Includes 10% GST (AU)`. Optional amount form adds `· $9.00` (1/11 of $99). | A sale to an AU buyer is a taxable supply. |
| Outside Australia | **No GST line at all.** | GST-free export. Nothing tax-related is shown. |

The rule that decides this is the buyer's **location** (Stripe Tax reads billing address, IP and card), never the currency or the email domain. A USD sale to an AU buyer is still taxable. See [[feedback_stripe_gst_au_buyers]]. The GST line is text under the total, monochrome, in caption ink (`--mz-text-muted`); it is never a coloured tax badge.

---

## 1 · Checkout entry

The page that takes the order and hands off to Stripe. Archetype: Checkout ([14-page-archetypes.md](14-page-archetypes.md) · 3). Shell is the **reduced nav** (wings + wordmark, links home, no links, no CTA) and the **slim footer** (brand block + legal row). The body is one section: the order summary, built from the Pricing moment ([13-sections.md](13-sections.md) · 5) in its order-summary variant.

### Order summary card

One white card, the canonical Pricing-moment card.

| Property | Value |
|----------|-------|
| Surface | Card `#FFFFFF` |
| Radius | **20** (`--mz-r-card`) |
| Border | `--mz-border` hairline `rgba(13,13,13,.08)` |
| Shadow | `--mz-shadow-card` |
| Padding | **48px** (`--mz-s-7`) at `md` and up, **24px** (`--mz-s-5`) below 920 |

Contents, top to bottom:

1. **Product lockup:** a small **disc** ([05-product-system.md](05-product-system.md), Ø = 50% of its holder, wings 50% of the disc, no glow) wearing the AI OS core gradient `MZ-G13` ([02-gradients.md](02-gradients.md), [../products.json](../products.json)), beside the name.
2. **Product line:** `AI OS · $99 one-time · Lifetime access`.
3. **Updates line:** `Includes all future updates`, in body / caption ink.
4. A `--mz-border` hairline divider.
5. **Total line:** `Total · $99 USD`.
6. **GST line**, AU buyers only: `Includes 10% GST (AU)` (see [GST by buyer location](#gst-by-buyer-location)). Non-AU buyers see nothing here.

The card carries a price because it is the checkout summary, not a product card: product cards never show a price ([05-product-system.md](05-product-system.md)), the pricing surface does ([13-sections.md](13-sections.md) · 5).

### Fields

When the restyle lands, every input follows the form primitive in [12-states-and-forms.md](12-states-and-forms.md): **44px** high, radius **8** (`--mz-r-chip`), white fill, **1px** `--mz-input-border` (`rgba(13,13,13,.45)`), label 13px Inter Medium (500) ink, placeholder `--mz-placeholder` (`rgba(46,46,46,.70)`). On focus the border goes solid ink `#0D0D0D` and the 2px `--mz-focus-ring` (`rgba(13,13,13,.45)`) joins it at 2px offset. The boundary and ring clear 3:1; placeholder text clears 4.5:1. Validation uses the functional colours and nothing else: `--mz-error` `#B42318` for an invalid field, `--mz-success` `#15803D` for a confirmed one. No other colour enters the form.

Card details are Stripe's element and are **never** rendered as raw Mez inputs: the buyer types a card number into Stripe's field, not ours. Our styling stops at the summary and the surrounding chrome.

### Trust row

A slim row beneath the pay control, caption ink, monochrome:

- A **"Secure payment via Stripe"** line with the Stripe wordmark or lock glyph. No coloured badge; the mark sits in ink.
- A **refund line** reassuring the buyer, linking to the Refunds policy ([14-page-archetypes.md](14-page-archetypes.md) · Legal). The exact window is a **DEFAULT**, flag the wording to Olli before it ships.

The pay control itself is an **ink pill** ([07-ui-components.md](07-ui-components.md)) with an action label (`Pay securely` is the DEFAULT, flag to Olli), taking the standard button states from [12-states-and-forms.md](12-states-and-forms.md). The **price never sits on the pill**: the amount lives in the summary total, and the primary CTA rule ("never a price on the pill", [07-ui-components.md](07-ui-components.md)) holds even here.

### Layout

Inside the **1160 container** ([11-layout-and-grid.md](11-layout-and-grid.md)). The order summary is a single card, centred and capped to a comfortable reading measure (never the full 1160). The default is one column stacked in source order: summary, then the pay control and fields, then the trust row. An optional two-column split is allowed at `md` and up (summary on one side, fields on the other), both columns inside 1160 with the **48px** (`--mz-s-7`) gap; below 920 it collapses to the single stacked column. Section rhythm around the body is 72 / 120.

### Meta

- Title: `Checkout · Mez Systems`.
- Description: `Checkout for the AI OS by Mez Systems. $99 one-time, GST shown for AU buyers. Secure payment. A Mez Studios company.`
- **Indexing: `noindex`.** Checkout is not a landing page; keep the meta minimal and the robots tag on.

---

## 2 · Success

The post-purchase confirmation and the path into the product. Archetype: Success ([14-page-archetypes.md](14-page-archetypes.md) · 4). Shell is the **reduced nav** and the **slim footer**. The body is one confirmation panel with one clear next action.

### The confirmation panel

> **Deviation, flagged to Olli.** [14-page-archetypes.md](14-page-archetypes.md) lists success as a `cta-band` confirmation variant, and the standard `cta-band` is a dark `#0D0D0D` panel that inverts its CTA to a white pill ([13-sections.md](13-sections.md) · 7). This success panel instead sits on **light**, because it carries numbered delivery steps and an **ink** pill, which read as a checklist a buyer follows, not as a closing marketing band. Light is the working pick here; flag the choice to Olli.

The panel is a light surface: the recessed panel `#F6F5F4` at radius **28** (`--mz-r-panel`), or a white card at radius **20**, centred in the 1160 container and capped to a reading measure. Padding **64px** (`--mz-s-8`) at `md` and up, **32px** (`--mz-s-6`) below 920. Contents, top to bottom:

1. The **wings** mark ([04-the-mark.md](04-the-mark.md)) on the light surface. One small AI OS disc (`MZ-G13`) is allowed as an accent instead.
2. Heading: **"Your AI OS is ready"**, H2 scale, ink `#0D0D0D`.
3. A one-line sub confirming the purchase, body ink.
4. The **numbered delivery steps** (below).
5. The **ink pill** labelled **"Open your AI OS"** ([07-ui-components.md](07-ui-components.md), standard button states). This is the access action, not "Get the AI OS".
6. A quiet fallback text link: **"Didn't get the email? Resend it"**, link states per [12-states-and-forms.md](12-states-and-forms.md).

### Delivery steps

A short numbered list (three steps), Inter body, ink, on the light panel. The default copy:

1. **Open your AI OS** using the button above, or the link in your email.
2. **Duplicate it into your Notion** when Notion prompts you.
3. **Start with the welcome page.** Everything is inside.

"Open your AI OS" resolves to the fulfilment pipeline's install link (host `api.mez.systems`, the duplicate-into-Notion flow); the exact URL is owned by the pipeline, not this doc ([[project_digital_product_fulfilment_pipeline]]). The step copy is a **DEFAULT**, flag changes to Olli.

### Meta and indexing

- Title: `You're in · Mez Systems`.
- Description: `You're in. Your Mez Systems purchase is confirmed and your access is on the way. A Mez Studios company.`
- **Indexing: `noindex`.** The success page is per-buyer; keep the robots tag on and the meta minimal.

---

## 3 · Delivery / receipt email

The one email the buyer must receive: it confirms the purchase, carries the receipt, and links into the product. It is HTML built for email clients, which are a decade behind browsers, so it follows email rules, not web rules.

### Structure

| Constraint | Value |
|------------|-------|
| Width | **600px** single column, centred on the body background |
| Layout engine | **Table layout** (`role="presentation"` tables), never CSS grid or flexbox |
| Body background | `#F8F8F8` (brand page) |
| Content surface | White `#FFFFFF`, the email's card |
| Radius | Card corners at **20**, accepting that Outlook squares them |
| Inline styles | All styling inline on elements; no external stylesheet, minimal `<head>` CSS |

### Font stack

Email clients do not have Inter, so the email never asks for it. It uses the **system stack** and lets each client render its own UI font, which keeps the Notion / Inter feel without a web font:

```
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
```

No `@font-face`, no Google Fonts link. Web-only families (Inter, Instrument Serif, IBM Plex Mono) are not referenced in email.

### Header strip and logo

The email may open with a **gradient header strip**: a full-width band wearing the AI OS core gradient `MZ-G13` ([02-gradients.md](02-gradients.md)). This is the one place a gradient appears in commerce, and it is allowed because the gradient shows **through a surface** (the email header), never as a bare page background ([02-gradients.md](02-gradients.md) · Rules). On the strip sits the **logo as a hosted PNG** (wings + wordmark, white knockout), served at 2x for retina. **No SVG in email:** SVG is unsupported across major clients, so the mark is always a raster PNG with descriptive `alt` text.

Solid hex is used for every colour, since email clients handle `rgba` alpha unevenly: the card hairline is a solid `#E6E6E6` (the visual match for `rgba(13,13,13,.08)` on `#F8F8F8`), text is `#0D0D0D` and `#2E2E2E`, the button is solid `#0D0D0D`.

### Body and receipt block

Below the header, in the white card:

1. Heading: **"Your AI OS is ready"** (matches the success page), ink `#0D0D0D`.
2. A one-line confirmation.
3. The **numbered install steps**, the same three as the success page.
4. A **bulletproof button**: a table-cell button, background `#0D0D0D`, white label **"Open your AI OS"**, built as a table so it renders in Outlook (the 999 pill radius degrades to square there, which is acceptable).
5. A **receipt block**, hairline-separated:
   - `AI OS · $99 one-time · Lifetime access`
   - `Includes all future updates`
   - `Total · $99 USD`
   - GST line, AU buyers only: `Includes 10% GST (AU) · $9.00`. Non-AU buyers see no GST line.

Stripe issues its own compliant tax invoice separately; this email is the branded receipt and access hand-off, not the legal tax invoice.

### Plain-text version

A **plain-text alternative part is required** (multipart/alternative), for clients that block HTML and for deliverability. It carries, in plain text: the heading line, the three install steps with the access URL spelled out, the receipt lines (product, total, and the GST line for AU buyers), and the footer with the company line and ABN. No markup, no tracking, one link per line.

### Subject line

Formula: `Your {Product} is ready · Mez Systems`. Example: `Your AI OS is ready · Mez Systems`. It matches the success-page and email headings so the buyer recognises it in the inbox. No emoji, no "receipt #", no urgency.

### Footer

A slim footer inside the email, caption ink on the body background:

- Company line: **Mez Studios Pty Ltd**.
- **ABN placeholder** (`{ABN}`; current value `ABN 21 697 707 190`, confirm before it ships).
- The endorsement carries through the brand: a Mez Studios company.
- **No unsubscribe link.** This is a transactional email (a receipt and access hand-off), so an unsubscribe is not required and is deliberately omitted; marketing email is a separate list with its own unsubscribe.

---

## The rule

> **The receipt is the brand.** The three commerce surfaces are held to the same system as the homepage: monochrome surfaces, the disc for the product, the ink pill for the action, one flat USD $99 shown plainly, a GST line only for AU buyers, and never a subscription word. The checkout summary and the success panel compose from the eight sections; the email drops to table layout and a system font stack but keeps the price strings, the wings, and the single gradient-through-a-surface header. The live Stripe flow stays untouched until Olli schedules the restyle. A commerce surface that invents its own price framing, adds a coloured tax badge, or reaches for subscription language is off-system.

## Commerce (machine readable)

```json
{
  "doNotTouch": "The live Stripe flow is do-not-touch until Olli schedules the restyle; this spec is the target.",
  "surfaces": [
    {
      "id": "checkout",
      "archetype": "checkout",
      "shell": { "nav": "reduced", "footer": "slim" },
      "orderSummaryCard": {
        "surface": "#FFFFFF",
        "radius": 20,
        "border": "rgba(13,13,13,.08)",
        "shadow": "--mz-shadow-card",
        "padding": { "base": 24, "md": 48 },
        "contents": ["disc MZ-G13 + name", "productLine", "updatesLine", "hairline", "totalLine", "gstLine (AU only)"]
      },
      "fields": {
        "ref": "12-states-and-forms.md",
        "height": 44,
        "radius": 8,
        "background": "#FFFFFF",
        "border": "rgba(13,13,13,.45)",
        "focusBorder": "#0D0D0D",
        "focusRing": { "colour": "rgba(13,13,13,.45)", "width": 2, "offset": 2 },
        "placeholder": "rgba(46,46,46,.70)",
        "note": "Card entry is Stripe's element, never a raw Mez input."
      },
      "payControl": { "type": "ink pill", "labelDefault": "Pay securely", "priceOnPill": false, "note": "Amount lives in the summary total, never on the pill." },
      "trustRow": { "items": ["Secure payment via Stripe", "refund line links to Refunds policy"], "colour": "monochrome", "refundWording": "DEFAULT, flag to Olli" },
      "layout": { "container": 1160, "cardCappedToReadingMeasure": true, "columns": { "default": 1, "mdOptional": 2 }, "columnGap": 48, "sectionRhythm": { "base": 72, "md": 120 } },
      "meta": { "title": "Checkout · Mez Systems", "robots": "noindex" }
    },
    {
      "id": "success",
      "archetype": "success",
      "shell": { "nav": "reduced", "footer": "slim" },
      "confirmationPanel": {
        "surface": "light",
        "surfaceOptions": ["#F6F5F4 panel radius 28", "#FFFFFF card radius 20"],
        "padding": { "base": 32, "md": 64 },
        "deviation": "14 lists success as a dark cta-band; this panel is LIGHT so the ink pill + numbered steps read as a checklist. DEFAULT, flag to Olli.",
        "contents": ["wings (or one MZ-G13 disc)", "heading 'Your AI OS is ready'", "sub", "numberedSteps", "ink pill 'Open your AI OS'", "resend link"]
      },
      "deliverySteps": {
        "count": 3,
        "defaultCopy": ["Open your AI OS using the button above, or the link in your email.", "Duplicate it into your Notion when Notion prompts you.", "Start with the welcome page. Everything is inside."],
        "accessAction": { "label": "Open your AI OS", "resolvesTo": "fulfilment install link, host api.mez.systems (duplicate-into-Notion)", "ref": "project_digital_product_fulfilment_pipeline" },
        "status": "DEFAULT, flag to Olli"
      },
      "meta": { "title": "You're in · Mez Systems", "robots": "noindex" }
    },
    {
      "id": "email",
      "type": "delivery / receipt email",
      "notAWebPage": true
    }
  ],
  "priceDisplay": {
    "productLine": "AI OS · $99 one-time · Lifetime access",
    "updatesLine": "Includes all future updates",
    "plainPrice": "$99 · one-time",
    "totalLine": "Total · $99 USD",
    "currency": "USD",
    "amount": 99,
    "model": "one-time",
    "gstLine": "Includes 10% GST (AU)",
    "gstLineAmountForm": "Includes 10% GST (AU) · $9.00",
    "gstAmount": 9.00,
    "banned": ["/mo", "per month", "monthly", "subscription", "renews", "plan"]
  },
  "gst": {
    "registered": true,
    "entity": "Mez Studios Pty Ltd",
    "abn": "21 697 707 190",
    "behaviour": "inclusive",
    "flatPriceGlobally": true,
    "rule": "GST follows buyer LOCATION (Stripe Tax: billing address + IP + card), never currency or email domain.",
    "au": { "showsGstLine": true, "rate": "10%", "carvedFrom": 99, "gstAmount": 9.00 },
    "nonAu": { "showsGstLine": false, "treatment": "GST-free export" },
    "ref": ["project_checkout_v2_gst", "feedback_stripe_gst_au_buyers"]
  },
  "email": {
    "width": 600,
    "column": "single",
    "layout": "table (role=presentation), never grid or flexbox",
    "bodyBackground": "#F8F8F8",
    "contentSurface": "#FFFFFF",
    "hairline": "#E6E6E6 (solid hex; rgba alpha is unreliable in email)",
    "fontStack": "-apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, Helvetica, Arial, sans-serif",
    "webFontsReferenced": false,
    "logo": { "format": "PNG", "svgAllowed": false, "content": "wings + wordmark, white knockout, 2x" },
    "gradientHeaderStrip": { "allowed": true, "gradient": "MZ-G13", "reason": "gradient through a surface (email header), never a bare background" },
    "button": { "type": "bulletproof table-cell", "background": "#0D0D0D", "label": "Open your AI OS", "outlookRadius": "squares, acceptable" },
    "receiptBlock": ["AI OS · $99 one-time · Lifetime access", "Includes all future updates", "Total · $99 USD", "GST line (AU only): Includes 10% GST (AU) · $9.00"],
    "plainTextVersion": { "required": true, "carries": ["heading", "install steps with URL", "receipt lines + GST for AU", "footer company + ABN"] },
    "subject": { "formula": "Your {Product} is ready · Mez Systems", "example": "Your AI OS is ready · Mez Systems" },
    "footer": { "companyLine": "Mez Studios Pty Ltd", "abn": "{ABN} (default 21 697 707 190, confirm before ship)", "unsubscribe": "not required (transactional), omitted" },
    "stripeTaxInvoice": "Stripe issues the compliant tax invoice separately; this email is the branded receipt + access hand-off."
  }
}
```
