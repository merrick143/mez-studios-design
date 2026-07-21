# Typography system calibration 01

Status: human review complete, approved direction pending implementation
Production authority: none
Study: `MEZ-TYPOGRAPHY-SYSTEM-01`

## Purpose

Hero calibration 01 showed that typography cannot be approved as a detail inside a hero. This
plate compares three complete primary-family territories across the work Mez actually makes:
homepage display, explanatory body copy, product naming, commerce, compact data, controls and
mobile wrapping.

The three candidates are:

1. Tuned Inter. The familiar baseline with deliberate display metrics.
2. Instrument Sans. A more human, flexible neo-grotesque with width and stylistic range.
3. Geist. A more engineered family with a strong product and developer character.

Inter is loaded from the existing local licensed asset. Instrument Sans is loaded from Google
Fonts for this research plate. Geist is loaded from Vercel's official open-source repository.
Selected fonts must be self-hosted and registered with their licence before production promotion.

## Review boundary

Judge the letters, hierarchy, rhythm, density and wrapping. Button surface, radius and depth are
held deliberately quiet because controls have their own next calibration. The serif and mono
questions are separated so choosing a primary sans does not silently decide every other role.

Open:

```text
http://127.0.0.1:8911/research/phase-2/calibration-plates/typography-system-01/
```

The completed review is preserved in `typography-system-01-review.json`.

Approved direction:

- Geist for display titles.
- Tuned Inter for primary UI, body and reading.
- Instrument Serif only when an editorial context genuinely requires it.
- IBM Plex Mono only for code, provenance and technical metadata.
- Mobile typography must be revised around the Geist and Inter split.

This closes the human direction gate. It does not silently replace production tokens or font
assets. Implementation, self-hosting, fallback, responsive and channel migration work remains.

## Validate

```bash
python3 research/phase-2/calibration-plates/typography-system-01/validate_calibration.py
```
