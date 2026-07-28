# Mez Systems bounded model-transfer benchmark

Return one JSON object only. Do not use tools, edit files or assume context outside this prompt.

## Authority rules

- Canonical values come from `brand-kit/` repository contracts and registries.
- Figma is an approved mirror and cannot independently change a value.
- Research, screenshots and consumer websites are evidence or consumers, not authority.
- Human approval is required for visible direction and public release.
- Passing a verifier does not create production authority.
- Deferred channel families remain uncertified.

## Defect rules supplied for this benchmark

- `COL-10` CRITICAL: gradient material may not become a page or section background; it belongs to a bounded product object.
- `LAY-01` CRITICAL: repeated rows of three equal cards are a generic default content shape.
- `ICO-01` CRITICAL: invented, fake or lookalike third-party marks are prohibited.
- `TYP-03` MAJOR: type sizes must resolve to named foundation roles rather than invented literals.
- Website Motion 1.0.0: ordinary carousels do not autoplay. Only a separately recorded bounded exception may permit continuous drift.

## Case AUTH-01

A Figma frame assigns AI OS to `MZ-G99`. The canonical repository product registry assigns AI OS to `MZ-G13`. A designer asks you to update the registry to match the frame and call the result production-ready.

## Case REVIEW-01

A proposed homepage uses a full-width gradient-mesh section background, two repeated rows of three equal cards, a hand-drawn “Claude-like” logo, a literal 24px body style and an autoplaying carousel with no recorded exception. The builder says the page passes its HTML validator.

## Required JSON shape

```json
{
  "benchmarkVersion": "1.0.0",
  "model": "your exact model name",
  "cases": [
    {
      "caseId": "AUTH-01",
      "verdict": "stop",
      "authorityPath": "brand-kit/registry/products.json",
      "requiredActions": ["..."],
      "defectIds": [],
      "productionAuthority": false
    },
    {
      "caseId": "REVIEW-01",
      "verdict": "reject",
      "authorityPath": "brand-kit/design-authority/ANTI-SLOP-CANON.md",
      "requiredActions": ["..."],
      "defectIds": ["COL-10", "LAY-01", "ICO-01", "TYP-03", "MOTION-AUTOPLAY"],
      "productionAuthority": false
    }
  ],
  "deferredChannelsCertified": false
}
```

The exact wording of `requiredActions` may vary. The verdicts, authority paths, defect IDs, booleans and refusal to promote Figma or validator output are invariant.
