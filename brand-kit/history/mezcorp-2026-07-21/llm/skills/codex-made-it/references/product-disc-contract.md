# Mez Living Core expression contract

## Core truth

A product core has two linked representations:

1. An exact static source twin for fixed output and colour authority.
2. A parametric runtime core with four colour anchors, positions, weights, one shade colour and one bloom colour.

The runtime core approximates the source. It does not replace the source asset.

## Shape grammar

### Disc

- Perfect circular mask with a hard edge.
- Canonical compact product object.
- White canonical Wings sit directly inside the gradient.
- No halo, glow cloud or inset tile.

### Sphere

- Same palette, motion and Wings treatment as the disc.
- Adds only approved spherical shading.
- Reserved for a hero, launch frame or single focal product.

### Rounded rectangle

- Same shader under a rounded-rectangle mask.
- Used as the gradient field of a trading card or product pill.
- Card copy, price, status, CTA, border and shadow remain static HTML/CSS.

### Wings mask

- Uses the canonical two-path Wings geometry as the shader mask.
- Useful for an identity or motion study.
- Does not change the standard product-mark rule: white Wings inside the core.

## Collection rules

- Equal products use equal geometry and alignment.
- Product distinction comes from gradient and copy.
- Do not use jagged card sizes or a different chassis per product.
- A family calibration board may show several live cores for comparison.
- Production default remains one animated core per viewport.
- Bundle and upsell containers never animate.

## Motion

- Slow, continuous and non-looping to the eye.
- No spin, pulse, breath, bounce, spring, scroll reveal or visible reset.
- Hover changes field speed only.
- Core geometry, Wings and structural overlays never move.
- Pause hidden and offscreen work.
- Reduced motion renders the exact static twin.

## Candidate promotion gate

A research candidate may not mutate canonical authority. Promotion requires:

1. exact-source versus parametric comparison;
2. human select, edit, or reject decision;
3. product assignment recorded in governance;
4. canonical and portable data updated atomically;
5. deterministic rebuild and runtime validators passing.

## QA canaries

- White cards and dark bundle surfaces both show the core.
- The shared renderer owns exactly one WebGL context.
- All shapes appear at the correct local coordinates.
- No surface collapses to one flat tone unless the source genuinely does.
- Console is clean.
- Reduced motion and WebGL failure show the exact static twin.
- No horizontal overflow at supported desktop and mobile widths.
