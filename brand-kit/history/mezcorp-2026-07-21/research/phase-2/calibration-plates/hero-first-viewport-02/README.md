# Hero and first viewport calibration 02

Status: human review ready
Production authority: none
Study: \`MEZ-HERO-FIRST-VIEWPORT-02\`

## What changed

Hero calibration 01 treated the homepage like one product page. Olli rejected that composition and
asked for a centred opening that shows the product family through multiple cards, spheres or discs.
The later calibration gates approved:

- Geist for display and tuned Inter for body through \`DEC-TYPE-001\`;
- 12px controls, solid, outline and text hierarchy, 48px default height and micro-lift through \`DEC-CONTROL-001\`;
- the five-product homepage roster, aligned catalogue, gradient-and-copy territories, static cores,
  equal family weight, live-first commerce and a vertical mobile catalogue through \`DEC-FAMILY-001\`.

This plate applies those behaviours without inheriting the visual execution of the family and
commerce plate.

## Design direction

The opening is intentionally minimal but not empty:

- one centred proposition and one clarifying sentence;
- two actions with the approved control grammar;
- five equally sized product cores in one aligned line;
- exact Mez gradient textures and canonical Wings;
- no hero container, boxes, stagger, product UI, gradient text or decorative micro-labels;
- a neutral core for Context Engine because its gradient remains unassigned;
- a mobile composition that keeps all five products visible without a swipe-only rail.

The product cores are static because this is a repeated family context. The Living Core remains
approved through \`DEC-MOTION-002\`, but using it here would contradict the later static-core-only
family decision.

## Review

Open:

\`\`\`text
http://127.0.0.1:8911/research/phase-2/calibration-plates/hero-first-viewport-02/
\`\`\`

Review five bounded decisions and copy the JSON into Codex.

## Validate

\`\`\`bash
python3 research/phase-2/calibration-plates/hero-first-viewport-02/validate_calibration.py
\`\`\`
