# Mez Systems typography foundation

Status: canonical; approved through `H-FND-01-TYPE-PROOF`

This folder turns `DEC-TYPE-001` into the licensed, portable, responsive typography system approved by `DEC-TYPE-FOUNDATION-001`. The exact role scale and cross-channel implementation are canonical for this foundation.

## Authority

- `typography.source.json` owns family assignments, role metrics and behaviour.
- `typography.schema.json` defines the source contract.
- `review.json` is the immutable approval record for the implementation gate.
- `build_typography.py` generates the self-contained `dist/` package: CSS, JSON, source snapshot, review, fonts, authoring files, licences and manifest.
- `fonts/` contains the exact self-hosted web and design-authoring assets plus each upstream OFL notice.
- `brand-kit/workbench/foundations/typography/` is the review and stress-test surface. It is not a separate source of truth.

Do not hand-edit `dist/`. Change the source and rebuild.

## Approved family policy

| Role | Family | Rule |
|---|---|---|
| Display | Geist | Hero, section and page titles only. |
| Body and UI | Inter | Reading, navigation, controls, compact UI, headings below display level and numerals. |
| Editorial | Instrument Serif | Contextual statements only; never a quota or body family. |
| Technical | IBM Plex Mono | Code, provenance, identifiers and technical metadata only. |

## Build and verify

```bash
python3 brand-kit/foundations/typography/build_typography.py
python3 brand-kit/foundations/typography/verify_typography.py
```

An unchanged rebuild must produce no Git diff. `dist/` can be copied out of this repository and its CSS still resolves every packaged webfont. This portable slice does not replace the active whole-system migration release or imply that the remaining foundations are complete.
