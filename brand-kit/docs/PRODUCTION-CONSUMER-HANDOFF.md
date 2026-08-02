# Mez Systems production consumer handoff

Updated: 2 August 2026

This document is the short operational handoff for people working across the canonical design repository and the live Mez Systems website.

## Where the two repositories fit

| Responsibility | Repository | Current state |
| --- | --- | --- |
| Canonical design authority | `https://github.com/merrick143/mez-studios-design` under `brand-kit/` | Active authority on `main` |
| Production website consumer | `https://github.com/mezcorp-studio/ceos-notion-landingpage` | Live from `main` at `https://mez.systems/` |

The repositories are deliberately separate. The production site does not load code, CSS or assets from a local design-repository path at runtime. Its integration is a versioned, consumer-owned adapter generated from exact rc.2 source inputs.

## Exact production lineage

- Design source commit: `0b07254636470e7da6cda174a34d49073d800f52`
- Source candidate: `brand-kit/releases/production-01/1.0.0-rc.2/`
- rc.2 manifest SHA-256: `129e0faab15173633987fe7c0c66bde982978f850c18b9689412968b718aa2e9`
- Consumer integration tip: `9d56d90e84b2280478b7fc5aa505e9ed9832cdca`
- Consumer production merge: `626580ab18624702912cad82c2c681ddb8f16cb2`
- Consumer pull request: `https://github.com/mezcorp-studio/ceos-notion-landingpage/pull/28`
- Production site: `https://mez.systems/`
- Machine-readable proof: `brand-kit/releases/production-01-plan/consumer-proof/port-04-production-proof.json`

## What is live

- The Mez Systems company homepage at `/`.
- The canonical AI OS product page at `/ai-os` and its ten variants.
- Agency Supply with its consumer-owned identity and behaviour preserved.
- Contact, privacy, terms, refund policy and the 404 fallback with shared visual foundations.
- The consumer-owned checkout presentation shell, with Stripe, pricing, attribution, analytics, APIs and fulfilment still owned by the website repository.

The base live checkout received a successful zero-total production smoke test using an existing 100 percent discount code. The code itself is not recorded here. The live order bump remains hidden because `LIVE_STRIPE_PRICE_PROMPT_VAULT` is not configured; that path remains a named operational follow-up.

## Authority boundary

The website being live does not publish `@mez-systems/design-system-web`, promote rc.2 to production version `1.0.0`, or make the consumer repository a second design authority. The design repository still owns versioned design values, approved component contracts and source assets. The consumer still owns routes, SEO, analytics, attribution, content truth, consent, commerce, provider logic and deployment.

Do not edit the frozen rc.2 release. A design-system change must follow this sequence:

1. Make and approve the source change under `brand-kit/` on a normal feature branch.
2. Assemble a new immutable candidate or release version with a new manifest.
3. Update the consumer adapter in a separate consumer pull request.
4. Re-run the affected consumer verifiers and rendered review.
5. Merge and deploy only after the consumer change is separately approved.

## Team start path

1. Read `brand-kit/AGENT-GUIDE.md`.
2. Read `brand-kit/START-HERE.md` and `brand-kit/docs/CURRENT-STATE.md`.
3. Use `brand-kit/docs/ROADMAP.md` to select bounded follow-up work.
4. Read the exact component contract and review record before changing a component.
5. Keep `merrick143/mez-studios-design@main:brand-kit` as the canonical authority until a separately approved repository transfer updates `brand-kit/authority/current.json`.

## Immediate team follow-ups

- Configure and separately test the optional live Prompt Vault order-bump Price ID before exposing that offer.
- Plan new versioned candidates for future website improvements; never patch rc.2 in place.
- Keep the priority-deferred channel families explicitly deferred until Olli selects them.
- Treat the current design-repository URL as authoritative. A move to a Mez organisation repository is a separate governance and provenance change, not an administrative cleanup.

Classification: live named-consumer integration using an approved immutable candidate; the candidate remains unpublished and has no independent production-release authority.
