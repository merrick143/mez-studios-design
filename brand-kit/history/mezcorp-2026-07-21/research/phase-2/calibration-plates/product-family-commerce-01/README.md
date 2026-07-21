# Product family and commerce calibration 01

Status: behaviour approved through `DEC-FAMILY-001`; visual execution not approved
Production authority: none
Study: `MEZ-PRODUCT-FAMILY-COMMERCE-01`

## Purpose

This plate tests whether Mez Systems can present a growing product family and real purchase paths
without becoming a generic card grid or five unrelated mini-brands.

It inherits the approved foundations:

- `DEC-MOTION-002`: Living Core motion is reserved for an earned focal product object. Repeated and commerce objects stay static.
- `DEC-TYPE-001`: Geist for display, tuned Inter for body and controls.
- `DEC-CONTROL-001`: 12px action radius, solid/outline/text hierarchy, one-pixel lift, 48px default controls and mobile full-width primary.

## Product boundary

The live Notion homepage names five public products: AI OS, Context Engine, AI Ads System,
Claude Code OS and Organic Content OS. The portable pack still names AI OS, Aurora, Prism and Forge.
This conflict is not silently resolved here.

- AI OS keeps locked core `MZ-G13`.
- AI Ads System uses `MZ-G20` as a provisional research bridge from the former Aurora assignment.
- Claude Code OS uses `MZ-G15` as a provisional research bridge from Forge.
- Organic Content OS uses `MZ-G06` as a provisional research-only expression.
- Context Engine is shown with an unassigned neutral placeholder. No synthetic gradient is invented.

Only Olli can promote the homepage roster or assign future cores.

## Reviewed direction

Olli approved the following behaviour:

- one aligned family chassis, with no staggered card heights;
- product distinction through gradient and copy;
- static product cores inside repeated, selection and checkout contexts;
- equal product-family weight, while availability labels and actions remain truthful;
- current commerce sells AI OS once for USD $99;
- future bundle composition is shown as a labelled scenario without invented prices;
- mobile uses a vertical catalogue and persistent purchase summary, not a swipe-only carousel.

This approves behaviour, not the plate's visual execution. Olli explicitly stated that the general
design still needs a lot of work. The revised hero must materially raise the aesthetic standard.

## Review

Open:

```text
http://127.0.0.1:8911/research/phase-2/calibration-plates/product-family-commerce-01/
```

The completed review is preserved in `product-family-commerce-01-review.json`.

## Validate

```bash
python3 research/phase-2/calibration-plates/product-family-commerce-01/validate_calibration.py
```
