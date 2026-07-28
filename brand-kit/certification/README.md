# Mez Systems whole-system certification

`TASK-CERT-01-SYSTEM-CERTIFICATION` certifies the explicitly agreed current release scope and assembles the later immutable candidate used by the final consumer-transition gate.

This package does not expand the design system into the deferred channel families. It does not make Figma independently authoritative, promote the Product UI fixture into a real product screen, publish a package, deploy a website or assign production version `1.0.0`.

## Certification surfaces

- `certification.source.json` and `certification.schema.json` define the bounded certification contract.
- `scope.json` records exactly what is certified, bounded, deferred and still consumer-owned.
- `audits/` records authority, accessibility, portability, onboarding and release-governance evidence.
- `benchmarks/` records the named-model transfer benchmark and its limitations.
- `health-checks.json` defines the recurring repository checks and failure routing.
- `review.json` records the machine result, known gaps and closed human gate.
- `verify_certification.py` checks claims against repository files and executable implementation evidence.
- `build_certified_release_candidate.py` copies the frozen `1.0.0-rc.1` bytes into a new output, adds the approved Figma mirror, Product UI foundation and certification evidence, and emits `1.0.0-rc.2` without modifying `rc.1`.
- `verify_certified_release_candidate.py` runs dependency-free inside the isolated `rc.2` package.

## Status boundary

Olli closed `H-CERT-01-SYSTEM-CERTIFICATION` over exact manifest SHA-256 `129e0faab15173633987fe7c0c66bde982978f850c18b9689412968b718aa2e9`. The current-scope certification and exact `1.0.0-rc.2` candidate are approved for final named-consumer proof. This does not authorise consumer integration before exact registration, publication, deployment or production version `1.0.0`.

## Run

From the repository root:

```bash
.venv/bin/python brand-kit/certification/verify_certification.py
.venv/bin/python brand-kit/certification/verify_certified_release_candidate.py brand-kit/releases/production-01/1.0.0-rc.2
```

The builder created the exact pre-gate candidate and now refuses to rebuild it because `approval.json` exists. Any later package change requires a new version and bounded review.
