# Product screenshot library

Status: `candidate-intake-system`

Task: `TASK-CHAN-ADS-PRODUCT-SCREENSHOT-LIBRARY`

Production authority: `false`

This library is the durable, local source of truth for product screenshots used in ad statics, websites, carousels and presentations. It does not approve a screenshot for public use and it does not certify a paid-ad system.

## Local files or Figma?

Use both, with different jobs:

1. Local originals are the masters. They keep stable paths, original pixels, hashes, dimensions, privacy state and reusable crop instructions.
2. Figma is the layout and review surface. It should receive a selected derivative or proxy, not become the only copy of the source screenshot.
3. A single original can carry several crop recommendations. Do not duplicate the master just because a 1:1 ad and a 9:16 story need different crops.
4. Embedded Figma image hashes are file-scoped implementation details. Record them only as optional delivery metadata.

Keep three asset classes separate:

- `native-capture`: an authentic product screen captured directly from Notion or the product.
- `supplied-composition`: a user-supplied device mockup or presentation composition containing a product screen.
- `reference-only`: first-party Notion creative used to study framing, motion or proof presentation. It is never Mez product proof.

## Intake workflow

1. Drop unedited screenshots into [`_INBOX-DROP-HERE/`](./_INBOX-DROP-HERE/).
2. Tell the agent when the dump is complete. The agent must not move or classify an in-progress dump.
3. Run `.venv/bin/python brand-kit/assets/product-screenshots/scripts/catalogue.py --scan-inbox` from the repository root to inventory dimensions and hashes without changing files.
4. Sort each original into its canonical product folder, or `shared-operating-system/` when it proves the operating system across products.
5. Put prebuilt device mockups in the product's `compositions/` folder. Do not mix them with native captures.
6. Put external Notion creative in `reference-material/notion-first-party/`. Unknown provenance or licensing keeps it reference-only.
7. Add a capture record to the matching `manifest.json` with asset class, page type, Notion width mode, privacy state, proof role and curation tier.
8. Add crop recommendations for the useful channel ratios. Crops are pixel coordinates against the immutable original.
9. Create redacted or compressed files in `derivatives/` only after the intended use is known.
10. Upload the chosen derivative to Figma for composition and review.
11. Run `.venv/bin/python brand-kit/assets/product-screenshots/scripts/catalogue.py --verify` from the repository root before handoff.

## Notion capture rules

Record whether a Notion source is `full-width` or `centred`. That distinction materially changes useful crops:

- `full-width`: preserve the database or operating surface and allow tighter horizontal crops.
- `centred`: protect the page title, icon and central content column from being cropped into an awkward narrow strip.
- `unknown`: do not guess. Leave the value unknown until the page can be inspected.

Also record the chrome state. A clean app-only capture, a browser-and-app capture and a no-chrome export serve different compositions.

## Privacy and proof

`_INBOX-DROP-HERE/` and every `originals/` folder are ignored by Git because raw operating screenshots may contain private names, clients, tasks or commercial data. Original does not mean public-safe.

The privacy states are:

- `internal`: never use publicly.
- `redaction-required`: potentially useful after specific information is removed.
- `public-safe-candidate`: reviewed for obvious risk but not approved.
- `approved-public`: explicitly approved for the stated use.

Do not fabricate product proof, invent interface content or rebuild a fake Notion screen when an authentic screenshot exists. Public delivery still requires the normal privacy and human review gates.

## Folder model

```text
product-screenshots/
  _INBOX-DROP-HERE/          raw drop zone, ignored by Git
  products/<product>/
    originals/               immutable raw masters, ignored by Git
    compositions/            supplied device and presentation compositions, ignored by Git
    derivatives/             deliberate crops, redactions and Figma proxies
    manifest.json            metadata and crop recommendations
  shared-operating-system/   proof that belongs to more than one product
  reference-material/        external creative, reference-only and never product proof
  schema/                    manifest contract
  scripts/                   non-destructive scan and verification tools
```

The canonical products are read from `brand-kit/registry/products.json`; do not create marketing aliases as product folders.

Current AI OS selection guidance is in [`products/aios/CURATION.md`](./products/aios/CURATION.md). External Notion creative observations are in [`reference-material/notion-first-party/REFERENCE-NOTES.md`](./reference-material/notion-first-party/REFERENCE-NOTES.md).
