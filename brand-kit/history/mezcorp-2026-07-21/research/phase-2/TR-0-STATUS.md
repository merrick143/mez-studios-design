# TR-0 stabilisation status

Status: operational exit gate passed, repository checkpoint pending  
Updated: 20 July 2026

## Complete

- One live name across project, product, package, CLI, and newly generated outputs: Taste Reverse.
- Version `0.2.0` and findings-export schema `1.0.0` recorded.
- Legacy `pnpm taste` command retained as a compatibility alias.
- Manual and enriched exemplar artifacts documented separately from deterministic pipeline output.
- Stable findings and normalised-measurement schemas implemented.
- Source fingerprint, export manifest, sizes, and SHA-256 checksums implemented.
- Sanitised export excludes screenshots, source assets, source copy, and raw element evidence.
- Copied fixture export validated without the research repository, producing 77 measurements.
- Build, lint, unit, integration, and end-to-end tests pass.

## Pending

The Taste Reverse repository has no existing commit and its entire codebase, historical research packages, screenshots, and overlays are untracked. A content checkpoint exists in `release.json`, but creating the first Git commit and tag remains pending until the repository owner confirms whether the historical media trees belong in the initial history.

This does not block H1 panel selection or controlled research. It does block describing Taste Reverse `0.2.0` as an immutable Git-pinned dependency.
