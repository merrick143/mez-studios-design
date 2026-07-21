# 18 · Imagery and OG

Status: DEFAULT · working values, flag deviations to Olli

The Mez Systems products are Notion and Claude systems, so the product pages sell on screenshots: the feature rows in [13-sections.md](13-sections.md) and the product archetype in [14-page-archetypes.md](14-page-archetypes.md) both hang the proof on a screenshot, and both defer its treatment here. Until now nothing said how a screenshot is framed, so every build cropped and cornered it differently, and the monochrome discipline that governs the chrome left it unclear whether a screenshot should be desaturated to match. Two other surfaces were also unspecified: the Open Graph card every archetype names but no doc drew, and the favicon and app-icon set. The live site still broadcasts pre-Mez favicons and OG images. This doc closes all of it. It sets the screenshot law and its one colour exception, the window frame recipe, the OG template, and the favicon and app-icon system. Every number traces to [07-ui-components.md](07-ui-components.md), [03-typography.md](03-typography.md), [11-layout-and-grid.md](11-layout-and-grid.md) or the token files. No new layout number is introduced; the frame's title-bar height and dots are the only bespoke values, and the brief sets them.

---

## 1 · Screenshot law: evidence stays in colour

A product screenshot is **evidence**, not chrome. The monochrome rule ([01-colour.md](01-colour.md), [07-ui-components.md](07-ui-components.md)) governs the **chrome**: the page, the cards, the buttons, the pills, everything the brand draws. It does **not** govern the product UI captured inside a screenshot. A screenshot shows the real product doing the real thing, and the real thing has colour: Notion's blues, Claude's surfaces, a status green, a gradient the product itself renders. Draining that to greyscale to "match the brand" makes the proof look like a mock and reads as a stock placeholder, not a running system.

- **Real product UI.** Capture the actual product (the AI OS in Notion, a Claude Code surface, a real dashboard). Never a redrawn or faked screen.
- **In colour, always.** The screenshot keeps its native colour. **Never greyscale, tint, duotone or desaturate a screenshot.** This is the single, explicit exception to the monochrome rule.
- **Chrome stays mono around it.** The frame, the section, the page around the screenshot stay monochrome. The colour lives only inside the captured surface, so the one hit of colour on the page is the product being itself. The product gradient is the only brand colour ([02-gradients.md](02-gradients.md)); a screenshot's own UI colour is not a brand colour, it is evidence.

> **The rule.** The monochrome law governs chrome, not evidence. A product screenshot is evidence and stays in full colour. Never greyscale a screenshot.

---

## 2 · The window frame recipe

Every product screenshot wears the same frame: a neutral window with a title bar and three dots, the screenshot filling below. It reads as "a real app window" without pretending to be any one operating system, and it is the only chrome the screenshot gets.

**Capture and crop**

- Capture the **product surface only**. Crop out the browser and OS chrome: no address bar, no OS menu bar, no tab strip, no desktop, no cursor, no notifications. The frame below supplies the only chrome.
- Crop **tight to the content** that makes the point. A feature row shows one capability, so the crop shows that capability, not the whole app.
- Capture at **2x** for a crisp result on retina, then place at the display size. Export as PNG (lossless UI edges) or WebP.

**Frame spec**

| Part | Value | Token |
|------|-------|-------|
| Corner radius | **14** | `--mz-r-tile` |
| Border | **1px `rgba(13,13,13,.08)`** | `--mz-border` |
| Shadow | **`--mz-shadow-card`** (`0 18px 40px -10px rgba(13,13,13,.10)`) | `--mz-shadow-card` |
| Title bar height | **36px** | bespoke (brief) |
| Title bar fill | **`#F6F5F4`** (neutral, recessed surface) | `--mz-surface` |
| Dots | **three**, each **8px** diameter | bespoke (brief) |
| Dot colour | **`rgba(13,13,13,.16)`** | bespoke (brief) |
| Dot spacing | **6px** between dots | bespoke (brief) |
| Screenshot | fills the frame **below** the title bar, clipped to the 14 radius | `--mz-r-tile` |

The dots sit at the **left** of the title bar, inset by the component spacing step **12px** (`--mz-s-3`) from the left edge and optically centred in the 36px bar. Three mono dots only: no red / amber / green traffic lights, since colour on the chrome is off-system. The title bar carries **no text and no icon**; it is a neutral band, not a browser tab.

```css
.mz-shot {
  border-radius: var(--mz-r-tile);        /* 14 */
  border: 1px solid var(--mz-border);      /* rgba(13,13,13,.08) */
  box-shadow: var(--mz-shadow-card);
  overflow: hidden;                        /* clip the screenshot to the radius */
  background: var(--mz-card);
}
.mz-shot__bar {
  height: 36px;
  background: var(--mz-surface);           /* #F6F5F4 */
  border-bottom: 1px solid var(--mz-border);
  display: flex; align-items: center; gap: 6px;
  padding-inline: var(--mz-s-3);           /* 12 */
}
.mz-shot__dot { width: 8px; height: 8px; border-radius: 999px; background: rgba(13,13,13,.16); }
.mz-shot__img { display: block; width: 100%; height: auto; }   /* real UI, in colour, never greyscale */
```

**Where the frame sits**

- On **white** (`#FFFFFF`) or on the **recessed** page or panel surface (`#F8F8F8` page, `#F6F5F4` panel). **Never on a dark panel.** On the dark `#0D0D0D` cta-band the imagery is a disc, not a screenshot ([13-sections.md](13-sections.md) · CTA band), so the frame never meets a dark surface.
- As the feature-row media ([13-sections.md](13-sections.md) · Feature row) the framed screenshot **is** the media panel. Where 13 gives the media panel radius **20**, the screenshot's own window frame is the tile at **14** and is the panel itself, not an extra card wrapped around it (both carry `--mz-border` and `--mz-shadow-card`, so they read the same). Default to the single 14 frame; flag to Olli if a radius-20 outer card around the frame is ever wanted.
- In the **gradient-strip** ([14-page-archetypes.md](14-page-archetypes.md) · gradient-strip) the three surface mocks may use the same 14 tile frame; the gradient still only shows through a surface, never behind the strip.

> **The rule.** One screenshot, one frame: radius 14, hairline border, `--mz-shadow-card`, a 36px `#F6F5F4` title bar with three 8px `rgba(13,13,13,.16)` dots, the real UI in colour below. On white or recessed, never on dark. A screenshot with any other chrome, a browser bar, a device shell or a desaturated capture is off-system.

---

## 3 · Device frames and photography

**Device frames: none for v1.** No phone mockups, no laptop bezels, no floating iPhone. The window frame in section 2 is the only frame a screenshot gets. A device shell would add chrome the monochrome system does not want and date the page the moment the device does. If a phone context is ever needed it is a decision to log in [09-governance.md](09-governance.md), not a default.

**Photography: none for v1.** The system carries no stock photography, no office shots, no abstract imagery. The page is type, discs, gradients through surfaces, and product screenshots. The **only** photograph that may ever enter is a **founder photo Olli supplies himself**, and only if he supplies it; there is no sourced or generated photography. Until Olli provides one, there is no photo slot on any archetype.

---

## 4 · OG template (1200 × 630)

Every archetype in [14-page-archetypes.md](14-page-archetypes.md) names an OG subject and defers the dimensions, safe area and treatment here. One template renders them all.

**Canvas and treatment**

| Part | Value | Token |
|------|-------|-------|
| Size | **1200 × 630** (the OG standard) | bespoke (spec) |
| Background | **`#F8F8F8`** (the page surface, flat, no gradient) | `--mz-bg` |
| Safe area | **64px** padding on all four edges; nothing load-bearing outside it | `--mz-s-8` |
| Brand lockup | **wings + "Mez Systems" wordmark**, top-left, inside the safe area | [04-the-mark.md](04-the-mark.md) |
| Page title | the page title in the **H2 style**: Inter Bold (700), tracking **-2.5%**, leading **104%**, ink **`#0D0D0D`**, set at **40px** (the locked desktop H2 size, [03-typography.md](03-typography.md)) | `--mz-h2-*` |
| Product disc | on the **right**, **only when the page is product-scoped**, wearing that page's core gradient ([05-product-system.md](05-product-system.md), no glow) | [05-product-system.md](05-product-system.md) |

**Layout.** Wings + wordmark lock top-left. The page title sets on the left, below the lockup, as the dominant element (it wraps to at most two lines inside the safe area). A product page places that product's disc on the right. The home / suite page places the four-core trading-card fan on the right. Every other non-product page leaves the right empty. The background is the flat page surface, never a gradient (gradient only ever shows through a surface, [02-gradients.md](02-gradients.md)).

**Per-archetype subject** (from [14-page-archetypes.md](14-page-archetypes.md); this doc supplies the treatment those slots defer to):

| Archetype | OG subject | Product-scoped |
|-----------|-----------|----------------|
| Home / suite | the suite as a trading-card fan (four cores) + title | no (suite, not one core) |
| Product page | this product's disc, its core gradient + name + function | **yes** |
| Checkout | default brand OG (wings + wordmark), page usually noindex | no |
| Success | default brand OG, page noindex | no |
| 404 | default brand OG | no |
| Legal | default brand OG | no |

The **default brand OG** is the template with the lockup and title and no disc: wings + "Mez Systems" + the page title on the flat page. It is the fallback the archetypes reference for "until 18 lands"; it has landed, and this is it.

**File naming.** One file per page, **`og-{page}.png`**: `og-home.png`, `og-aios.png`, `og-aurora.png`, `og-checkout.png`, `og-404.png`. Export at 1200 × 630 PNG. Product OGs key off the product slug ([../products.json](../products.json)).

> **The rule.** One OG template, 1200 × 630 on `#F8F8F8`, 64px safe area, wings + "Mez Systems" top-left, and the page title in H2 style. Product pages place their disc on the right; the home / suite page places the four-core trading-card fan there; other non-product pages leave it empty. Name files `og-{page}.png`. A bespoke OG, gradient background or screenshot on the OG is off-system.

---

## 5 · Favicon system

Two favicon families, split by surface tier ([00-brand-architecture.md](00-brand-architecture.md): product = disc, holdco = wings).

| Surface | Icon | Fill / background |
|---------|------|-------------------|
| **Product** pages (product archetype, its checkout and success) | the **AI OS disc** (`MZ-G13`, [../products.json](../products.json), [05-product-system.md](05-product-system.md), no glow) | the disc's own core gradient |
| **Holdco / brand** pages (home / suite, legal, 404, the Mez Systems brand) | the **wings**, **ink `#0D0D0D`** on **white** | ink on white |

**Size set (both families): 32 / 180 / 512.**

| File | Size | Use |
|------|------|-----|
| `favicon-32.png` | 32 | browser tab / bookmark |
| `apple-touch-icon.png` | 180 | iOS home-screen / Safari pinned |
| `icon-512.png` | 512 | PWA manifest / high-density |

The product favicon uses the **AI OS disc** as the standing product mark, since AI OS is the live product and the site's product identity ([../products.json](../products.json)). A **per-product favicon** (each product wearing its own core on its own page) is a candidate, not the default; flag to Olli before shipping per-product favicons ([09-governance.md](09-governance.md)).

**Ship note.** The live site still serves **pre-Mez favicons and OG images**. Replacing them with this set (the two favicon families, the app-icon marks, the OG template) is a launch task, not optional polish. Until it ships, tabs and shares still carry the old identity.

---

## 6 · App-icon marks

For app tiles, launcher icons and directory listings, the mark is the **disc with the wings** (the disc treatment from [05-product-system.md](05-product-system.md): gradient disc, white wings at 50% of the disc, nudged ~2% up, no glow), the same construction as the product favicon.

**Size set: 128 / 256 / 512.**

| File | Size | Use |
|------|------|-----|
| `app-icon-128.png` | 128 | small tile, list row |
| `app-icon-256.png` | 256 | standard app tile |
| `app-icon-512.png` | 512 | large tile, store / directory listing |

These are the disc-and-wings marks, distinct from the wings-on-white holdco favicon: an app tile is a product surface, so it wears the disc. The wings-only app-icon variant ([04-the-mark.md](04-the-mark.md): ink squircle + white wings) stays available for a holdco tile; the disc-and-wings set above is the product default.

> **The rule.** Product surfaces wear the disc, brand surfaces wear the wings. Favicons ship at 32 / 180 / 512 (`favicon-32.png`, `apple-touch-icon.png`, `icon-512.png`); app-icon marks ship the disc-and-wings at 128 / 256 / 512. Nothing on the live site keeps a pre-Mez icon.

---

## Imagery and OG (machine readable)

```json
{
  "imageryAndOg": {
    "status": "DEFAULT",
    "screenshotLaw": {
      "rule": "monochrome governs chrome, not evidence",
      "product_ui": "real UI only, never faked or redrawn",
      "colour": "always full colour",
      "neverGreyscale": true,
      "exceptionTo": "the monochrome rule in 01-colour.md and 07-ui-components.md"
    },
    "windowFrame": {
      "radius": 14,
      "radiusToken": "--mz-r-tile",
      "border": "rgba(13,13,13,.08)",
      "borderToken": "--mz-border",
      "shadow": "--mz-shadow-card",
      "shadowValue": "0 18px 40px -10px rgba(13,13,13,.10)",
      "titleBar": {
        "height": 36,
        "fill": "#F6F5F4",
        "fillToken": "--mz-surface",
        "insetLeft": 12,
        "insetLeftToken": "--mz-s-3",
        "dots": { "count": 3, "diameter": 8, "colour": "rgba(13,13,13,.16)", "spacing": 6, "position": "left" },
        "text": "none",
        "trafficLights": false
      },
      "screenshot": { "position": "below title bar", "clippedToRadius": 14, "capture": "product surface only, no browser/OS chrome, 2x, PNG or WebP" },
      "background": ["#FFFFFF", "#F8F8F8", "#F6F5F4"],
      "neverOn": "#0D0D0D dark panels",
      "featureRowNote": "the framed screenshot IS the media panel; the 14 tile frame resolves 13-sections feature-row 'media radius 20' (default single frame, flag radius-20 outer card to Olli)"
    },
    "deviceFrames": { "v1": "none", "reason": "window frame is the only chrome; device shells off-system" },
    "photography": { "v1": "none", "onlyEver": "founder photos Olli supplies himself, if ever; no sourced or generated photography" },
    "og": {
      "size": { "width": 1200, "height": 630 },
      "background": "#F8F8F8",
      "backgroundToken": "--mz-bg",
      "safeArea": 64,
      "safeAreaToken": "--mz-s-8",
      "lockup": "wings + 'Mez Systems' wordmark, top-left",
      "title": { "style": "H2", "font": "Inter Bold 700", "size": 40, "tracking": "-2.5%", "leading": "104%", "ink": "#0D0D0D", "maxLines": 2 },
      "rightVisual": {
        "productPage": "that product's disc using the page core gradient, no glow",
        "homeSuite": "four-core trading-card fan",
        "otherNonProduct": "none"
      },
      "flatBackground": true,
      "fileNaming": "og-{page}.png",
      "examples": ["og-home.png", "og-aios.png", "og-aurora.png", "og-checkout.png", "og-404.png"],
      "perArchetype": {
        "home": { "subject": "suite trading-card fan (four cores) + title", "productScoped": false },
        "product": { "subject": "this product's disc + core gradient + name + function", "productScoped": true },
        "checkout": { "subject": "default brand OG", "productScoped": false, "noindex": true },
        "success": { "subject": "default brand OG", "productScoped": false, "noindex": true },
        "notfound": { "subject": "default brand OG", "productScoped": false },
        "legal": { "subject": "default brand OG", "productScoped": false }
      },
      "defaultBrandOg": "template with lockup + title, no disc (resolves the 'until 18 lands' fallback in 14-page-archetypes.md)"
    },
    "favicons": {
      "sizes": [32, 180, 512],
      "files": { "32": "favicon-32.png", "180": "apple-touch-icon.png", "512": "icon-512.png" },
      "appleTouchIcon": 180,
      "product": { "mark": "AI OS disc", "core": "MZ-G13", "background": "core gradient", "glow": false, "source": "products.json" },
      "holdco": { "mark": "wings", "fill": "#0D0D0D", "background": "#FFFFFF" },
      "split": "product surfaces = disc; holdco/brand surfaces = wings (00-brand-architecture.md)",
      "perProductFavicon": "candidate, not default; flag to Olli",
      "shipNote": "live site still serves pre-Mez favicons and OG; replacing them is a launch task"
    },
    "appIconMarks": {
      "mark": "disc + wings (disc treatment, wings 50% of disc, no glow)",
      "sizes": [128, 256, 512],
      "files": { "128": "app-icon-128.png", "256": "app-icon-256.png", "512": "app-icon-512.png" },
      "holdcoVariant": "wings-only (ink squircle + white wings, 04-the-mark.md) available for a holdco tile"
    },
    "satisfiesForwardRefs": {
      "13-sections.md": "feature-row screenshot treatment (crop, corner radius, frame, shadow)",
      "14-page-archetypes.md": "OG dimensions, safe area, treatment; default brand OG"
    }
  }
}
```
