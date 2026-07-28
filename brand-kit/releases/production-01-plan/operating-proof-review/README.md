# Operating-proof derivative review

Status: exact derivative bytes approved by Olli on 2026-07-28. The four
hash-locked derivatives are eligible to enter the `1.0.0-rc.1` release
candidate; this approval does not authorise deployment or production release.

`payload.json` preserves each original SHA-256 without copying its absolute
source path or original bytes. The four PNGs under
`assets/operating-proof/redacted/` are separate deterministic derivatives.
`contact-sheet.png` exists only to make the human review efficient.

Rebuild from the repository root:

```bash
zsh brand-kit/releases/production-01-plan/build_operating_proof_review.sh
```

Re-running the builder creates new derivative bytes and resets the payload to
`publicReleaseEligible: false`; any rebuilt bytes require a new exact-byte
review. A component or homepage approval does not substitute for this media
review.
