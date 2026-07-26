# EXP-08 expression stress proof

This is the consolidated adversarial proof for the approved Mez expression suite. It tests the existing system; it does not introduce a new expression family.

## Candidate boundary

- 6 suites and 14 representative scenarios.
- Responsive receivers from 240px containers and 320px viewports through 1440px.
- 200% and 400% text scaling, long copy, translation expansion and RTL.
- Reduced motion, WebGL failure, missing media and exact static fallbacks.
- Keyboard, focus, touch, semantic status and recovery states.
- One live Living Core maximum across repeated product material.

The candidate remains non-authoritative until `H-EXP-08-EXPRESSION-STRESS-PROOF` is closed by Olli. Repairs may address implementation defects only; approved visual, component and motion grammar stays inherited.

## Build and verify

```bash
python3 brand-kit/expressions/stress-proof/build_expression_stress_candidate.py
python3 brand-kit/expressions/stress-proof/verify_expression_stress_candidate.py
```

Review at `/brand-kit/workbench/expressions/stress-proof/`. Add `?static=1` or `?no-webgl=1` to inspect explicit fallback modes.
