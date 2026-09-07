---
name: build-price-anchored-product-static
description: Build or revise a Mez 1080x1350 price-anchored product-proof static from the approved paid-social format pack. Use when a request mentions price-anchor ads, a costly category versus a smaller product first step, the approved AI OS R07 batch, authentic Notion product proof, or a new 4:5 static batch in Figma.
---

# Build Price Anchored Product Static

Create an editable Figma static and export while preserving the approved format grammar, real-product-proof requirement and campaign-specific public preflight. The pack is craft-approved; it does not authorise publishing or certify paid social as a whole.

## Read first

Read these repository files before acting:

- `brand-kit/AGENT-GUIDE.md`
- `brand-kit/channels/paid-social/AGENTS.md`
- `brand-kit/channels/paid-social/SOP.md`
- `brand-kit/channels/paid-social/content-model.schema.json`
- `brand-kit/channels/paid-social/templates/figma-template.json`
- `brand-kit/channels/paid-social/templates/copy-matrix.json`
- `brand-kit/assets/product-screenshots/AGENTS.md`
- The selected product screenshot manifest

## Workflow

1. Collect product, audience, destination, current product price, billing basis and verification date.
2. Collect attributable current category-cost evidence and write the comparison scope note.
3. Stop if the product is being represented as equivalent to a service it does not replace. Use `start with`, `first` or an equally clear sequencing relationship.
4. Select an authentic screenshot or supplied composition from the local product library. Never fabricate a Notion screen.
5. Inspect privacy and proof status. A `public-safe-candidate` is not `approved-public`.
6. Choose the champion, alternate or safe R07 source route.
7. Duplicate the selected frame into a new dated Figma section. Do not edit approved section `1407:936` in place.
8. Apply the content while preserving the locked 1080x1350 reading order, Geist Medium two-line title, restrained grid, downward glow, proof-led lower half and exactly three floating outcome cards.
9. For native proof, crop to legibility and keep corner treatment restrained. For device compositions, size against visible subject bounds and use no background card, fill, stroke or proof-area shadow.
10. Use the real Notion mark or canonical AI OS disc. Do not create substitute glyph tiles.
11. Render the batch and each frame at final size. Inspect full size and at about 360px preview width.
12. Export PNG 1x, keep the editable Figma source and record a receipt.
13. Run the craft validator. Before publishing, complete the separate campaign preflight.

## Allowed variation

Vary the downward glow, approved title-mark allocation, inline Notion versus AI OS label and native versus device proof treatment. Vary copy only after revalidating the evidence. A new ratio, extra outcome-card family, serif title, replacement of the price-anchor mechanism or motion version is a new composition-family review.

## Stop conditions

Stop and report the blocker if any of these is true:

- price, destination or comparison evidence cannot be verified;
- no authentic product screenshot is available;
- a public output lacks an `approved-public` derivative for the intended campaign;
- requested copy implies unsupported feature or service equivalence;
- the requested change expands into a new ratio or composition family without review;
- Figma write access is unavailable and the user requested an actual Figma build.

## Validation

Run from the repository root:

```bash
.venv/bin/python brand-kit/channels/paid-social/validator/validate_format.py --mode craft
```

The publish validator is intentionally stricter:

```bash
.venv/bin/python brand-kit/channels/paid-social/validator/validate_format.py --mode publish
```

Do not bypass a publish failure. Resolve and record the named campaign-specific blockers, then seek human publishing authority.

## Output contract

Return the Figma section and frame IDs, exported PNG paths, source screenshot ID, evidence verification dates, validator result, public-preflight status and receipt path. State plainly whether the work is craft-approved, pilot-ready, published or still blocked; never collapse these states.
