# 05 · Product system

## The default: the disc card

The **disc card** is the primary product unit. Landing pages, the site, feature rows: this is the default. It is a white card with a gradient disc, the wings, the product name, its function, one line of copy, and a text CTA. The sphere formation is reserved for identity boards only, never product cards (see "The rule" below).

### Anatomy & spec

| Part | Spec |
|------|------|
| Surface | White `#FFFFFF`, radius 20 (`--mz-r-card`), hairline `rgba(13,13,13,.08)`, soft drop shadow |
| Orb | Disc. **Diameter = 50% of the card width** (e.g. Ø ~190 on a ~380 card). Gradient core + inner-shadow depth |
| Mark | White wings, **50% of the orb diameter**, optically centred, **nudged ~2% up** |
| Title | Inter Semi Bold (600) ~22–30, text `#0D0D0D` |
| Function | Inter Medium (500) 12, tracked +6%, muted (e.g. "AI OPERATING SYSTEM") |
| Body | Inter Regular (400) ~15–17, text `#2E2E2E`, centred, max 2 lines |
| CTA | Text link, Semi Bold, `#0D0D0D`. Never a price (e.g. "Get the AI OS →") |

Drop shadow on a free-floating disc: `0 16px 34px -18px rgba(13,13,13,.4)`. Wings nudge: 1.5 to 2% of Ø up, optical.

### The disc recipe (Plugin API)

The disc is two stacked elements: the gradient ellipse with inner shadows for depth, and the white wings on top. Locked ratios (relative to the orb diameter `d`): **wings = 50% of `d`**, wings **nudged ~2% up**.

```js
function disc(parent, cx, cy, d, hash) {
  // 1. the disc with inner-shadow depth (dark top, light bottom)
  const e = figma.createEllipse();
  e.resize(d, d);
  e.fills = [{ type:'IMAGE', scaleMode:'FILL', imageHash: hash }];
  e.effects = [
    { type:'INNER_SHADOW', color:{r:0,g:0,b:0,a:0.32}, offset:{x:0,y:-7}, radius:16, spread:0, visible:true, blendMode:'NORMAL' },
    { type:'INNER_SHADOW', color:{r:1,g:1,b:1,a:0.30}, offset:{x:0,y:7},  radius:12, spread:0, visible:true, blendMode:'NORMAL' }
  ];
  parent.appendChild(e); e.x = cx - d/2; e.y = cy - d/2;

  // 2. white wings on top: 50% of the orb, optically centred, nudged ~2% up
  const w = wf(d*0.5); // wf from 04-the-mark.md
  parent.appendChild(w); w.x = cx - w.width/2; w.y = cy - w.height/2 - d*0.02;
}
```

Glow was retired 2026-07-17. Never add a blurred halo behind the disc or any other core.

### Orb sizing in a card

The orb diameter is **50% of the card width**. On the standard ~380px-wide card that is Ø ~190. This ratio holds across the card variations (compact, horizontal, dark): the orb tracks the card width, not a fixed pixel size.

## Variations (all keep the disc)

Layout and context change; the orb stays a disc.

| Variation | Use |
|-----------|-----|
| **Standard** | The canonical card above. Grids of four (AI OS / Aurora / Prism / Forge). |
| **Compact** | Smaller card, tighter padding. Dense grids, related-products rows. |
| **Horizontal** | Disc left, text right. Lists, comparison rows, settings. |
| **Dark** | Near-black `#0D0D0D` surface instead of white, for dark sections. Disc unchanged. |

For collectible / stack contexts, use the **trading card** instead (a different format, see [06-trading-cards-and-stacks.md](06-trading-cards-and-stacks.md)).

## The rule

> **Always the disc.** On a product card the core is always the flat disc (hard edge, wings 50% of Ø). The sphere is reserved for identity boards; glow is retired and never built.

## When to use which format

- **Disc card** → landing, site, feature rows, comparison. The default.
- **Trading card** → decks, bundles, "collect the set", stacks.
- **Pill** → navigation, selectors, compact product references (see [07-ui-components.md](07-ui-components.md)).
