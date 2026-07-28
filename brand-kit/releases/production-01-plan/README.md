# Production release 01 boundary

Status: `1.0.0-rc.1` generated, verified and approved by Olli at
`H-PORT-03-PRODUCTION-RELEASE-CANDIDATE`, then frozen as the first portable
milestone by `SEQ-CONSUMER-LAST-001`. Nothing is published or deployed.

`TASK-PORT-01-RELEASE-BOUNDARY` defines the first production-package boundary around the canonical Mez Systems foundations, expression system, Global Navigation and Golden Homepage. It is a release-engineering contract, not a release artifact and not permission to deploy a consumer.

## The boundary

The target package is a self-contained `@mez-systems/design-system-web` release. It must carry its own canonical authority snapshot, foundations, identity data, local fonts and licences, Living Core runtime and static twins, approved expressions, approved components, Golden Homepage composition, guidance, skills, schemas, validators and examples. A clean consumer may not import from `brand-kit/`, an absolute workstation path or a network-hosted design dependency.

The target candidate version is `1.0.0-rc.1`. `1.0.0` may be assigned only after the candidate-component gates, release-safe proof payload, isolated package proof and named consumer proof have all passed.

## Component dependency resolution

CMP-05 Halftone Portrait and CMP-06 Testimonial Marquee were separately promoted by Olli on 2026-07-28 under `DEC-HALFTONE-PORTRAIT-COMPONENT-001` and `DEC-TESTIMONIAL-MARQUEE-COMPONENT-001`. Their exact locked revisions are now release-eligible inputs to PORT-03.

PORT-02 selected the first of the two explicit paths defined by this plan:

1. Both components passed their own promotion questions and received separate decision IDs before entering release-candidate assembly.

The exclusion interface remains documented as historical contingency evidence, but it is not the active PORT-03 route.

`TASK-PORT-02-HOMEPAGE-DEPENDENCY-GATES` is closed. PORT-03 assembled the
isolated candidate at `brand-kit/releases/production-01/1.0.0-rc.1/`; its
content SHA-256 is
`5be57efb5e48cba8ac2bdc98445852fbaf6e2decfea1546e3b7ad0eac8d7f26c`.
Olli approved the exact package on 2026-07-28; `release-candidate-approval.json`
records the manifest-identified gate. That gate made the bytes eligible for
named-consumer proof, but Olli subsequently sequenced consumer ingestion after
Figma, channel systems and whole-system certification. The package remains a
frozen milestone and may not be changed, published, deployed or renamed `1.0.0`.

## Operating-proof safety

The four raw screenshots remain evidence-only and explicitly ineligible for
release. Olli approved four separate redacted derivatives on 2026-07-28; the
approved payload preserves original hashes without original paths or bytes and
is the only operating-proof media copied into the candidate.

`operating-proof-payload.schema.json` defines that payload. `operating-proof-payload.example.json` deliberately remains ineligible: it records the four roles and source hashes, but contains no redacted asset paths, derivative hashes or public-release approval.

## Consumer interface

The final consumer is `CON-MEZ-SYSTEMS-WEB-001`, named **Mez Systems production web** and registered as `https://github.com/mezcorp-studio/ceos-notion-landingpage.git`. Its confirmed local checkout is recorded in `brand-kit/governance/consumer-register.json`. `TASK-PORT-04-NAMED-CONSUMER-PROOF` is ready and begins with a read-only audit. The consumer owns routes, analytics, SEO deployment, live availability, testimonial data freshness, consent operations and application logic. It receives a versioned package and may not copy values or become an independent source of design truth.

## Required evidence before assembly can become a release

- Keep the reconciled Foundation Release, Global Navigation and Golden Homepage decision records aligned with their existing Olli approval sources. PORT-02 completed this index repair without creating component authority.
- Preserve the two component promotion decisions and their bounded authority in the assembled package.
- Produce and review the redacted operating-proof payload.
- Build deterministically with an integrity manifest and no undeclared private dependency.
- Copy only the package into a temporary clean directory, deny access to the canonical checkout, serve it locally and run the package verifier.
- Prove 320, 375, 390, 430, 768, 1024, 1280 and 1440 layouts; keyboard, focus, screen-reader structure, reduced motion, no-WebGL and missing-media behaviour; zero runtime network dependency; and version visibility.
- Complete the Figma companion, channel systems and whole-system certification; assemble a later immutable candidate; then register and integrate the named real consumer and prove update and rollback without copying design values.

## Verification

From the repository root:

```bash
.venv/bin/python brand-kit/releases/production-01-plan/verify_release_boundary.py
.venv/bin/python brand-kit/releases/production-01-plan/verify_built_release_candidate.py
.venv/bin/python brand-kit/releases/production-01-plan/verify_port_03_closure.py
```

This verifier validates the plan schema, traces the current Golden Homepage imports, checks the live candidate authority, proves the raw proof media is excluded, verifies the clean-install/update/rollback contract and confirms that the decision-ledger discrepancy is represented as a blocking prerequisite rather than hidden.
