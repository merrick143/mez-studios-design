# Product screenshot agent rules

Read `README.md`, `schema/product-screenshot-manifest.schema.json` and the canonical `brand-kit/registry/products.json` before changing this library.

- Treat local originals as the asset authority and Figma as a downstream composition surface.
- Do not move, rename or classify files in `_INBOX-DROP-HERE/` until the user says the dump is complete.
- Preserve original bytes. Calculate the SHA-256 hash before creating crops, redactions or proxies.
- Keep native product captures, supplied compositions and reference-only third-party material in separate folders and metadata classes.
- Never treat an inbox file or original as public-safe by default.
- Never fabricate interface proof or silently replace an authentic screenshot with a recreated screen.
- Never cite a file under `reference-material/` as Mez product proof or reuse it publicly without provenance and licensing review.
- Use the canonical product IDs and slugs exactly as registered.
- Record Notion width mode, chrome state, privacy state and proof role. Use `unknown` where evidence is missing.
- Store crop geometry against the original in pixels and store a normalised focal point.
- Put derived crops, redactions and Figma proxies in `derivatives/`. Do not overwrite the master.
- Run `.venv/bin/python brand-kit/assets/product-screenshots/scripts/catalogue.py --verify` from the repository root after every manifest or asset change.

This library has `productionAuthority: false`. Public use still requires privacy review and explicit human approval.
