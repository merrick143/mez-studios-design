# PC2-B-C04 · Product Feature Bento

**Status: candidate 0.1.0. Not production authority. No release is built until a human decision exists.**

A bento is a layout contract, not a style. This component owns geometry, surface allocation and the
motion budget. The fixture owns content. Product identity is never hardcoded: it resolves from
`registry/products.json` at runtime, so adding or removing a product reflows the bento with no code
change.

## The one rule everything else leans on

> A bento carries exactly one colour event. It sits on a product or metric cell, and every other cell
> is paper or charcoal.

`PHASE-B-COMPONENT-PANTRY.md` states it as "multiple live gradient cells fail validation".
[`references/premium-neutral-with-one-colour-event`](../../references/premium-neutral-with-one-colour-event/design-language.md)
arrived at the same rule from a different direction: colour is only expensive against restraint, and
spread across every cell it becomes wallpaper, which reads cheaper than no colour at all.

Because two sources agree, the rule is enforced in three places rather than trusted to care: the JSON
Schema, the Python verifier, and the element at render. A fixture asking for two material cells does
not render a slightly worse bento. It renders the reason it was rejected.
`fixtures/invalid-two-material.json` exists so that is provable rather than claimed.

## Usage

```html
<link rel="stylesheet" href="brand-kit/components/product-feature-bento/mez-product-feature-bento.css" />
<mez-product-feature-bento fixture="./fixtures/mechanism-map.json"></mez-product-feature-bento>
<script type="module" src="brand-kit/components/product-feature-bento/mez-product-feature-bento.js"></script>
```

Open `fixtures/index.html` to see all four variants plus the rejection case.

## Cell model

Every cell declares a **job**, one of `product`, `proof`, `workflow`, `metric`, `media`,
`integration`, `quote`, `action`. A cell with no job is not a cell, it is decoration.

| Field | Meaning |
|---|---|
| `job` | Required. What the cell is for. |
| `surface` | `paper` (default), `recessed`, `raised`, `dark`, `material`. |
| `label`, `detail`, `kicker`, `figure` | Content. A cell resolving to none of these is filler and is rejected. |
| `productSlug` | On a product cell. Name, function, gradient and availability come from the registry. |
| `span`, `rows` | Auto flow placement, in columns of twelve. |
| `col`, `row` | Explicit placement. Moves a cell visually, never reorders the document. |
| `focal` | At most one per bento. |
| `href`, `interactive` | Renders the cell as a link or button and emits `mez-bento-cell-activate`. |

A registry-driven fixture sets `"source": "registry"` and a `registryTemplate` with `live` and
`coming` treatments instead of listing cells. Nothing counts to five.

## Variants

| Variant | Argument | Cells |
|---|---|---|
| `mechanism-map` | These are the building blocks of a business. Four already have a Mez System, and all of them run on the same layer. | Eight block cells, one product cell. |
| `workflow` | Four working stages wrap the one that ships. | Five cells in a pinwheel, explicit placement. |
| `evidence-mosaic` | Paper proves, material ships. | Three metric cells, one product cell. |
| `product-comparison` | One ships, the rest are coming. | Registry-driven, count-independent. |

## Geometry

```
frame 32  -  padding 8  =  panel 24
```

The radii are concentric by construction, not by eye. Change `--bento-pad` and the cell radius must
move with it; the verifier asserts the relationship against the foundations tokens. That pair is the
only thing in the stylesheet not free to be adjusted independently.

## Motion

One live core, page-wide, not per instance. Several bentos on one page hand the single core between
them by visibility. `prefers-reduced-motion`, `?static` and `?no-webgl` all mount nothing and leave
the exact static twin in place.

## Copy provenance

Every string in every fixture is either existing approved copy or resolved from the registry, with
one exception: the three caption lines in `evidence-mosaic.json` are authored for this fixture and
are flagged in `review.json` as awaiting sign-off.

**The building blocks in `mechanism-map.json` are not canonical yet.** Four of the eight are named
exactly as `registry/products.json` names the function each system serves, so `Advertising →
AI Ads System` is read off the registry rather than asserted. The other four are inferred from the
six departments Mez Studios actually runs in `mezcorp_claude_code`, which is evidence and not
authority. A block with no system carries no disc and makes no claim; nothing here invents a product
assignment. If this bento becomes the canonical statement of what a business is made of, the
taxonomy needs promoting into `brand-kit/registry/` with a decision behind it.

## Verify

```bash
python3 brand-kit/components/product-feature-bento/verify_product_feature_bento_contract.py
```

Mechanical checks are not design checks. Run `design-critique` on the rendered variants before
putting any of this in front of Olli.
