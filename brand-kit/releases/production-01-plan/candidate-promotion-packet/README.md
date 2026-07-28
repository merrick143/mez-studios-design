# Golden Homepage candidate promotion packet

Status: `H-PORT-02-HOMEPAGE-DEPENDENCY-GATES` closed by Olli on 2026-07-28. Both exact candidates promoted under separate decision IDs. This packet is the review receipt, not a generated release or permission to deploy.

This is one efficient review surface for two separate decisions. CMP-05 Halftone Portrait and CMP-06 Testimonial Marquee do not share authority: either can be promoted or excluded independently, each promotion requires its own decision ID, and no verdict in this packet is pre-filled for Olli.

## Approved decision

Olli approved both locked candidates without changing their visual or JavaScript bytes:

- CMP-05 has now passed Gate B at 67/75 and rendered overflow-free across every declared viewport. Accept its documented `invert` limitation because the locked treatment never uses inversion.
- CMP-06 retains the exact Round 04 social-caption design Olli selected and its 67/75 Gate B. Accept the explicitly recorded VoiceOver-speech and pointer-harness limitations for component promotion, but require real spoken-output, physical-pointer and device-performance proof in the named consumer before deployment.
- Use **frozen evidence** for follower counts: the fixture or consumer supplies a dated snapshot and source attribution; the component makes no Instagram request and never implies the number is live.
- Reconfirm the two existing component-specific motion exceptions exactly as bounded. Neither decision changes Website Motion 1.0.0 outside CMP-05 `motion-policy="always"` instances or the CMP-06 rail.

## Decisions recorded

1. CMP-05 promoted under `DEC-HALFTONE-PORTRAIT-COMPONENT-001`; the optional invert limitation is accepted.
2. CMP-06 promoted under `DEC-TESTIMONIAL-MARQUEE-COMPONENT-001`; frozen dated follower evidence is approved.
3. Both bounded motion exceptions are reconfirmed unchanged. Exact spoken VoiceOver, physical-pointer timing and device profiling remain named-consumer obligations.

If either component is excluded, the production plan keeps it out and GH-S08 uses the complete static `testimonial-proof` adapter. That path cannot claim exact visual parity without a bounded homepage adaptation review.

## Evidence

- CMP-05: component verifier, `responsive-evidence.json` and `gate-b.json` in its package.
- CMP-06: component verifier, locked Round 04 Gate B, existing responsive/reduced-motion receipts and this packet's `interaction-evidence.json`.
- Governance: the hash-locked cutover ledger remains unchanged; its post-cutover supplement indexes the three prior approvals and both component promotion decisions.

## Verification

From the repository root:

```bash
.venv/bin/python brand-kit/releases/production-01-plan/candidate-promotion-packet/verify_candidate_promotion_packet.py
```

The verifier validates the packet schema, exact live candidate revisions, Gate B thresholds, one-to-one known-gap accounting, follower and motion policies, reconciled authority records and the absence of premature CMP authority.
