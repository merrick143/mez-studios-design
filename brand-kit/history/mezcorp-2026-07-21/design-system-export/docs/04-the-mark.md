# 04 · The mark

The mark is the **wings** (the twin-panel "M"), shared with Mez Studios. What changes between tiers is the fill, not the shape (see [00-brand-architecture.md](00-brand-architecture.md)).

## Usage

- **Free-floating.** The wings sit in space; they do not need a container. When a container is used (app icon, roundel, pill) it is a deliberate treatment, not a default.
- **Clear space** = one cap-height of the wings on every side.
- **Minimum size** 24px tall. Below that, use the disc treatment.
- **Never recolour** the wings outside the system. Fills are: near-black `#0D0D0D` (default, holdco and parent), white (knockout on a gradient), or a gradient (Gradient-M treatment).

## Approved variations

From the holdco mark exploration (Figma "Holdco lab · Mark exploration", node `146:30`):

| Variation | When |
|-----------|------|
| Wings, full | Default holdco / parent mark |
| Wings, app icon | Ink squircle + white wings, for app tiles |
| Wings, roundel | Ink circle + white wings, for avatars |
| Wings, monoline | Outline only, for watermarks / large light-touch |
| Wings, keyline | Thin square keyline + wings, for stamps |
| Gradient-M | Wings filled with a product gradient, for product marks |

Explorations kept for reference but **not** default identity: monogram M, wordmarks, and the abstract glyphs (layers, network, aperture, brackets, cube, emblem). Do not use these as the mark without a decision logged in governance.

## Exact geometry (Plugin API)

The wings are two vector paths in a `340 × 241` viewBox (`viewBox="9 16 340 241"`).

```
P1 = M9.31894 227.388C9.31894 243.442 22.3337 256.457 38.3883 256.457H141.746C157.801 256.457 170.815 243.442 170.815 227.388V172.807C170.815 168.476 169.848 164.201 167.984 160.292L107.284 33.0283C102.46 22.9142 92.2519 16.4734 81.0462 16.4734H38.3883C22.3337 16.4734 9.31894 29.4882 9.31894 45.5427V227.388Z

P2 = M348.462 227.388C348.462 243.442 335.447 256.457 319.392 256.457H216.034C199.98 256.457 186.965 243.442 186.965 227.388V172.807C186.965 168.476 187.932 164.201 189.797 160.292L250.497 33.0283C255.321 22.9142 265.529 16.4734 276.734 16.4734H319.392C335.447 16.4734 348.462 29.4882 348.462 45.5427V227.388Z
```

Helper used in every build (white wings, rescaled to width `w`):

```js
const wf = (w) => {
  const n = figma.createNodeFromSvg(
    `<svg width="340" height="241" viewBox="9 16 340 241" xmlns="http://www.w3.org/2000/svg">
       <path d="${P1}" fill="#FFFFFF"/><path d="${P2}" fill="#FFFFFF"/>
     </svg>`);
  n.rescale(w / n.width);
  return n;
};
```

For the **Gradient-M** treatment, flatten both paths into one vector (`figma.flatten([wingsFrame])`) then apply a single IMAGE fill so one continuous gradient reads across both wings (the "window into the gradient" look).

Parent Mez Studios source logo: node `1:5901` (mark inside at `1:5903`).
