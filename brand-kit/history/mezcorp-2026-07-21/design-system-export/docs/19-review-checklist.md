# 19 · Review checklist

Status: LOCKED · 17 JUL 2026

This is the self-review an LLM runs on its own work **before it presents any Mez Systems
build**. Every earlier doc states a law. This doc turns those laws into a pass gate: ten
checks, each a yes or no with a concrete way to prove it, then ten do/don't pairs drawn from
the failures this remediation had to undo. It tests the locked laws, not the DEFAULT working
values, so it is LOCKED even though most of the pack is default. A build that fails any check
is off-system: fix it, then present. Do not present a failing build with a note.

The checks pull their values from the numbered docs and the token files, so nothing here is a
new rule. It is the same system, restated as a test you can run.

---

## How to use this

Run all ten baseline checks against the build before you show it. Each check must be **yes**. If the build contains a living core, run the four additional living-core checks too. The "How
to check" column is the proof: a grep that must return nothing, a number to measure, or a look
at the rendered surface. A grep that returns a hit, or a measurement outside the allowed set,
is a fail. Fix the fail, do not annotate it. When every check is yes, compare the build with the
latest certified golden named in `governance/authority-model.json`. If no certified golden exists,
keep the build in `candidate` state and request design-excellence review before presenting it as final.

---

## The ten checks

| # | Check · must be yes | How to check |
|---|---------------------|--------------|
| 1 | The product name reads **AI OS** with a space everywhere it is customer-visible. "AIOS" and "Atlas" appear nowhere in copy. | Run `python3 governance/scripts/validate_phase_one.py`. It parses rendered Canvas text rather than internal slugs, filenames, history or code comments. |
| 2 | Every product core is a **flat disc**. No glow, no halo, no blurred light ring behind any core. | The validator rejects `filter: blur()` and unsanctioned blur selectors, while allowing the documented nav and trading-card-chip backdrop blur. Then look: the disc edge is hard. |
| 3 | The **gradient appears on product elements only** (disc, product card, trading card). Never on a page or section background, the holdco, or a bundle container. | Every `gradient` hit lands on a product treatment. No `background` gradient on `body`, a section, or a bundle. Look: page and section fills are flat `#F8F8F8` / `#F6F5F4` / `#FFFFFF` / `#0D0D0D`. |
| 4 | Every colour, radius, shadow, spacing and duration **resolves to a token**. No invented grey, shadow, radius or duration. | `grep -rniE '#[0-9a-f]{3,8}'` and check each hit against the palette (`#F8F8F8` `#F6F5F4` `#FFFFFF` `#0D0D0D` `#2E2E2E` `#B42318` `#15803D`, plus gradient stops inside a core). Radius is one of 8 / 14 / 20 / 28 / 999. Spacing is one of 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96 / 120 / 160. Duration is 200ms (280ms for the accordion and mobile nav sheet only). |
| 5 | Every interactive element has **hover, active and a focus-visible ring**. The ring is 2px at 2px offset. | `grep -rn ':focus-visible'` covers every button, link and input. Then tab through with the keyboard: each control draws a 2px ring, `--mz-focus-ring` on light, `--mz-focus-ring-dark` on dark ([12-states-and-forms.md](12-states-and-forms.md)). |
| 6 | At a **375px viewport** there is no horizontal overflow and sections stack in source order. | Set the viewport to 375. `document.documentElement.scrollWidth <= 375` is true (no sideways scroll). Body text is not below 16px. The suite grid is one column ([11-layout-and-grid.md](11-layout-and-grid.md)). |
| 7 | Copy is **sentence case, Australian English, inside the char limits**, with no banned or hype word. | The validator checks visible Canvas text only, then the reviewer reads sentence case, AU spelling and each slot against [17-voice-and-copy.md](17-voice-and-copy.md). |
| 8 | Wherever a **price** shows it reads **$99 one-time** (USD $99), never a positive subscription frame. | The validator distinguishes prohibited offers such as `$99/mo`, `billed monthly` or `renews` from legitimate reassurance such as "No subscription" and the FAQ question "Is it a subscription?". Price surfaces read "$99 · one-time" ([15-commerce.md](15-commerce.md)). |
| 9 | Product **screenshots stay in full colour inside the doc-18 window frame** (radius 14, 36px `#F6F5F4` title bar, three 8px mono dots), on white or recessed, never dark, with no browser or device chrome. | `grep -rniE 'grayscale\(\|saturate\(0'` over screenshot styles returns nothing. Look: the capture keeps its native colour, the frame matches the recipe in [18-imagery-and-og.md](18-imagery-and-og.md), and it sits on `#FFFFFF` / `#F8F8F8` / `#F6F5F4`, never `#0D0D0D`. |
| 10 | **OG cards and favicons are on-brand** and no pre-Mez asset remains. | Open each `og-*.png`: 1200×630 on `#F8F8F8`, wings + "Mez Systems" top-left, product disc on product pages, four-core trading-card fan on home / suite, no right visual on other non-product pages. Favicons are the disc on product surfaces and the wings on holdco surfaces, at 32 / 180 / 512. `grep -n 'favicon\|apple-touch-icon\|og:image' index.html` points only at the doc-18 set ([18-imagery-and-og.md](18-imagery-and-og.md)). |

## Living-core checks

Run these four checks whenever the build contains the living-core treatment. All four must be yes.

| # | Check · must be yes | How to check |
|---|---------------------|--------------|
| LC1 | Every living core has a defined **static twin**, and reduced motion renders that twin rather than a frozen shader frame. | Confirm the core entry in `gradients.json` names an existing WebP. Emulate `prefers-reduced-motion: reduce` and verify the canvas is replaced by that image. |
| LC2 | A normal consumer shows no more than **one living core per viewport**. | Inspect each supported breakpoint. More than one is allowed only on the explicitly labelled internal calibration board. |
| LC3 | No living core appears **behind text**, in dense utility UI, or on a surface repeated more than six times. | Inspect the stacking order and count runtime instances. Text, wings, labels, chips and borders remain static above or outside the live field. |
| LC4 | The renderer and fallback paths are proven, and the **console is clean**. | Verify the live shader, force no-WebGL and compile-failure paths, check the white product-card and dark bundle canaries, and confirm no errors in the successful path. |

### Deterministic validator

Run this from the pack root:

```bash
python3 governance/scripts/validate_phase_one.py
```

The script parses customer-visible HTML separately from code, checks the export manifest and
internal links, verifies token parity and asset hashes, and consumes the saved responsive browser
evidence. Em dashes and double hyphens are checked only in visible copy, so CSS custom properties
and historical documentation do not create false failures.

### Sanctioned exceptions

- `backdrop-filter: blur()` is allowed only on the sticky nav tint and trading-card eyebrow chip.
- `drop-shadow()` is allowed on white wings for edge legibility. It is not a diffuse core halo.
- `#FFFFFF` is allowed on cards and controls, never as the page background.
- Error and success colours are allowed only in forms and system feedback.
- Product screenshots keep their native colour because they are evidence, not brand chrome.
- Continuous gradient motion is allowed only inside the living-core treatment under [20-living-core.md](20-living-core.md). It is not allowed on fills or backgrounds.
- `--mz-lockup-scrim` is required under the bottom 45% of a trading card. It is a contrast treatment,
  not a product gradient, page background or glow.

---

## Do and don't

Ten pairs, each one a failure this remediation had to reverse. The don't is what a build did;
the do is the law it broke.

| Don't | Do | Law |
|-------|----|-----|
| Put a blurred glow or halo behind a core. | Build the flat disc, hard edge, no halo. | [05-product-system.md](05-product-system.md) |
| Write "Atlas" or "AIOS". | Write "AI OS", with the space. | [17-voice-and-copy.md](17-voice-and-copy.md) |
| Frame the price as "$99/mo" or a subscription. | State "$99 · one-time", USD, on price surfaces only. | [15-commerce.md](15-commerce.md) |
| Invent a white-alpha grey for text on a dark section. | Use the `--mz-dark-text` / `--mz-dark-muted` set. | [12-states-and-forms.md](12-states-and-forms.md) |
| Put a sphere on a product card. | Use the disc on cards; the sphere is identity boards only. | [05-product-system.md](05-product-system.md) |
| Start a CTA with a hype verb (unlock, supercharge). | Use the semantic family: Get, Join, Explore, See, Open or Start. | [17-voice-and-copy.md](17-voice-and-copy.md) |
| Animate sections in on scroll, or move a gradient fill. | Keep interface motion on the standard tokens. Continuous motion belongs only to a living core under doc 20. | [16-motion.md](16-motion.md) |
| Drop a price into an ad CTA by default. | Keep ads and the default CTA price-free; price is a per-surface judgement. | [09-governance.md](09-governance.md) |
| Set the page background to pure `#FFFFFF`. | Page is `#F8F8F8`; white is for cards. | [01-colour.md](01-colour.md) |
| Make the primary CTA a bare text link. | Primary CTA is the dark ink pill "Get the AI OS". | [07-ui-components.md](07-ui-components.md) |

---

## The rule

> **Ten baseline checks, plus four for a living core, all yes, then present.** Before showing any build, run the applicable checks and clear
> every fail: name is "AI OS", no glow, gradient on products only, tokens only, states and focus
> rings present, 375 has no overflow, copy is sentence-case AU English inside the limits with no
> banned word, price is $99 one-time where shown, screenshots stay in colour in the window frame,
> and OG and favicons are on-brand with no pre-Mez asset. A living-core build must also prove its static twin, reduced-motion behaviour, instance limit, safe layering and clean renderer. A build that fails a check is off-system.
> Fix it, compare it with the latest certified golden when one exists, then complete the
> design-excellence review before presenting it as final.

## Review checklist (machine readable)

```json
{
  "doc": "19-review-checklist",
  "status": "LOCKED",
  "date": "2026-07-17",
  "gate": "run all checks before presenting; every check must be yes; fix fails, never annotate them",
  "checks": [
    { "id": 1, "name": "name is AI OS", "test": "context-aware visible-copy assertion passes", "ref": "17-voice-and-copy.md" },
    { "id": 2, "name": "no glow or halo", "test": "no filter blur or unsanctioned backdrop blur; disc edge is hard", "ref": "05-product-system.md" },
    { "id": 3, "name": "gradient on products only", "test": "no gradient on page/section/holdco/bundle background", "ref": "01-colour.md" },
    { "id": 4, "name": "tokens only", "test": "every hex/radius/shadow/spacing/duration resolves to a token", "ref": "07-ui-components.md" },
    { "id": 5, "name": "states and focus rings", "test": "hover, active and a 2px :focus-visible ring on every interactive element", "ref": "12-states-and-forms.md" },
    { "id": 6, "name": "mobile at 375", "test": "scrollWidth <= 375, no horizontal overflow, source-order stack, body >= 16px", "ref": "11-layout-and-grid.md" },
    { "id": 7, "name": "copy law", "test": "sentence case, AU English, inside char limits, no banned or hype word", "ref": "17-voice-and-copy.md" },
    { "id": 8, "name": "price is $99 one-time", "test": "context-aware pricing assertion rejects positive subscription offers but permits negative reassurance", "ref": "15-commerce.md" },
    { "id": 9, "name": "screenshots in colour in the frame", "test": "no greyscale/saturate(0); doc-18 window frame; on white or recessed", "ref": "18-imagery-and-og.md" },
    { "id": 10, "name": "OG and favicons on-brand", "test": "OG 1200x630 on #F8F8F8; disc on product favicons, wings on holdco; no pre-Mez asset", "ref": "18-imagery-and-og.md" }
  ],
  "livingCoreChecks": [
    { "id": "LC1", "name": "static twin and reduced motion", "test": "defined WebP exists and replaces the shader under reduced motion", "ref": "20-living-core.md" },
    { "id": "LC2", "name": "one per viewport", "test": "normal consumer has at most one live instance; calibration board is explicitly exempt", "ref": "20-living-core.md" },
    { "id": "LC3", "name": "safe placement", "test": "not behind text, in utility UI or repeated more than six times", "ref": "20-living-core.md" },
    { "id": "LC4", "name": "renderer and fallback proven", "test": "live, no-WebGL and compile-failure paths verified; card and bundle canaries visible; successful console clean", "ref": "20-living-core.md" }
  ],
  "doDont": [
    { "dont": "glow or halo behind a core", "do": "flat disc, hard edge", "ref": "05-product-system.md" },
    { "dont": "Atlas or AIOS", "do": "AI OS with a space", "ref": "17-voice-and-copy.md" },
    { "dont": "$99/mo subscription framing", "do": "$99 one-time on price surfaces", "ref": "15-commerce.md" },
    { "dont": "invented white-alpha grey on dark", "do": "the --mz-dark-* token set", "ref": "12-states-and-forms.md" },
    { "dont": "sphere on a product card", "do": "disc on cards, sphere for identity boards", "ref": "05-product-system.md" },
    { "dont": "hype CTA verb", "do": "semantic action family: Get, Join, Explore, See, Open or Start", "ref": "17-voice-and-copy.md" },
    { "dont": "scroll-reveal or moving gradient fill", "do": "token motion, with continuous motion only for a living core", "ref": "16-motion.md" },
    { "dont": "price in an ad CTA by default", "do": "price-free ads and default CTA, per-surface judgement", "ref": "09-governance.md" },
    { "dont": "pure-white page background", "do": "page is #F8F8F8, white is for cards", "ref": "01-colour.md" },
    { "dont": "text-link primary CTA", "do": "dark ink pill 'Get the AI OS'", "ref": "07-ui-components.md" }
  ],
  "anchors": {
    "mobileWidth": 375,
    "palette": ["#F8F8F8", "#F6F5F4", "#FFFFFF", "#0D0D0D", "#2E2E2E", "#B42318", "#15803D"],
    "radii": [8, 14, 20, 28, 999],
    "spacing": [4, 8, 12, 16, 24, 32, 48, 64, 96, 120, 160],
    "durationsMs": [200, 280],
    "focusRing": { "width": 2, "offset": 2 },
    "ctaVerbs": ["Get", "Explore", "Open", "See", "Start"],
    "bannedWords": ["Unlock", "Unleash", "Supercharge", "Revolutionise", "Elevate", "Seamless", "Empower"],
    "price": "$99 · one-time"
  }
}
```
