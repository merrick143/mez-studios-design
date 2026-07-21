# Button and control system calibration 01

Status: human review complete, approved direction
Production implementation authority: pending
Study: `MEZ-BUTTON-CONTROL-SYSTEM-01`

## Purpose

Typography is closed through `DEC-TYPE-001`. This plate isolated the next foundation layer:
the actions people use to move through a Mez website, compare products, buy a system and confirm a
high-consequence operation.

It tests button shape, hierarchy, depth, size, icons, dark-surface inversion and mobile behaviour.
The approved type split is held constant: Geist for the plate's display titles and tuned Inter for
button labels, body copy and operating text.

## Approved territory

The approved direction is called `quiet pressure`:

- 12px control radius, rounded but not pill-shaped;
- 48px default height and 52px prominent height;
- flat near-black primary at rest;
- one-pixel interaction lift with a tight contact shadow, never a glow;
- outlined secondary and text tertiary actions;
- directional icons only when they clarify movement or reveal;
- white primary action on a dark section;
- one full-width primary on mobile with a quiet secondary beneath it.

`DEC-CONTROL-001` approves this direction. Existing button tokens and components remain unchanged
until the implementation and migration phase.

## Review

Open:

```text
http://127.0.0.1:8911/research/phase-2/calibration-plates/button-control-system-01/
```

The completed review is preserved in `button-control-system-01-review.json`. The live plate remains
available for audit and comparison.

## Validate

```bash
python3 research/phase-2/calibration-plates/button-control-system-01/validate_calibration.py
```
