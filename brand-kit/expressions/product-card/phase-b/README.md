# Product Card 02 · Phase B functional website components

Status: canonical 1.0.0 through `H-EXP-04B-CARD-FUNCTIONAL-PROOF` and `DEC-PRODUCT-COMPONENT-SYSTEM-001`

Phase B applies the approved Phase A visual grammar to functional components, website composition patterns and complete buyer journeys.

The architecture deliberately separates:

1. inherited foundations and product-expression adapters;
2. fifteen reusable component contracts;
3. thirteen product-aware website patterns;
4. six complete journey fixtures.

This is how a `ProductPricingCard` can serve a one-time digital product, a recurring SaaS plan, a multi-tier pricing section, a checkout summary or a mobile decision surface without five unrelated implementations.

## Approved result

Olli approved all forty-six Round 04 functional specimens as keeps on 22 July 2026 and closed Product Card 02 Phase B.

- The exact Round 03 receipt records eleven keeps, thirty-five revisions and one kill.
- `B-FT04` was killed in Round 02 and remains removed; `B-FT06` was killed in Round 03 and is now removed.
- The eleven Round 03 champions and thirty-five rebuilt revisions are now one unanimously approved 46-specimen system.
- Every surviving functional specimen preserves every Phase A reference recorded in the verbatim Round 02 and Round 03 receipts.
- `phase-a-lineage.js` remains the machine-readable ancestry source for the canonical functional system.

The thirty-two Round 10 keeps remain canonical Phase A visual inputs. They are not additional Phase B components. Round 02 application views and all four Phase B feedback receipts remain historical evidence for the approved forty-six survivors.

## Authority boundaries

- Product identity comes from `brand-kit/registry/products.json`.
- Visual grammar comes from the pinned Product Card 02 Phase A 1.0.0 contract and Round 10 approval.
- The 32 canonical Phase A keeps remain approved visual inputs and have a Phase B candidate count of zero.
- SaaS, one-time, bundle and checkout prices are illustrative fixtures unless a consumer supplies authorised data.
- Components expose events and slots. They do not own network calls, payment-provider logic, Stripe keys, tax calculation or production prices.
- The golden homepage, generic application UI, Figma library and consumer migration remain outside this phase.

`H-EXP-04B-CARD-FUNCTIONAL-PROOF` is approved for the bounded component-design and interaction scope. It does not authorise illustrative prices, payment-provider logic, a golden homepage or consumer-owned production content. Exhaustive consumer-specific container, zoom, keyboard and content-stress proof continues under EXP-08 and consumer proof rather than reopening Phase B.

`round-01-feedback.json` records why Round 02 expanded the review surface. `round-02-feedback.json` drove Round 03. `round-03-feedback.json` records 11 keep, 35 revise and 1 kill. `round-04-feedback.json` records 46 keep, zero revise, zero kill and zero unreviewed; `review.json` records the resulting canonical decision. All are integrity-tracked in the 1.0.0 package.

## Commands

```bash
.venv/bin/python brand-kit/expressions/product-card/phase-b/verify_product_component_pantry.py
```

Open the locked functional proof at `http://127.0.0.1:8914/brand-kit/workbench/expressions/product-card/phase-b/`.
