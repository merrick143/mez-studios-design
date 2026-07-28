# Website motion system

Status: Round 03 review candidate. No production authority.

Human gate: `H-EXP-07-CHANNEL-MOTION-PROOF`

Candidate: `channel-motion-matrix-01-r03`

Round 02 established the decisive scope correction: this repository does not need a motion system for every communication channel. Email, paid ads, organic social, motion graphics and film leave this task. Documents, compact identity and open graph remain static outputs and no longer need review specimens.

Round 03 is website-only. It preserves the approved Living Core exception and short functional response, radically simplifies product demonstration, and adds five reusable website behaviours: section entry, menu/disclosure, accordion/tabs, product carousel and processor/progress. The direction is deliberately calm: static is complete, motion is brief and local, carousels never autoplay, scroll is never hijacked, and only one expressive event may run in the viewport.

21st.dev and similar libraries may be used later as implementation catalogues. They do not set the Mez motion direction and no external component enters the system without passing this contract.

Build and verify:

```bash
.venv/bin/python brand-kit/expressions/channel-motion/verify_channel_motion_candidate.py
```

Review surface:

`/brand-kit/workbench/expressions/channel-motion/`
