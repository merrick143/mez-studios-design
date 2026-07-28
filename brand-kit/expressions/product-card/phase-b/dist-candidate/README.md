# Product Card 02 · Phase B functional website components

Status: PB2 Round 04 active review candidate, no production authority

Phase B applies the approved Phase A visual grammar to functional components, website composition patterns and complete buyer journeys.

The architecture deliberately separates:

1. inherited foundations and product-expression adapters;
2. fifteen reusable component contracts;
3. thirteen product-aware website patterns;
4. six complete journey fixtures.

This is how a `ProductPricingCard` can serve a one-time digital product, a recurring SaaS plan, a multi-tier pricing section, a checkout summary or a mobile decision surface without five unrelated implementations.

## Current stage

`PB2` Round 04 is the active review candidate: forty-six surviving functional specimens across discovery, features and proof, pricing, checkout, bundles and growth, mobile and confirmation.

- The exact Round 03 receipt records eleven keeps, thirty-five revisions and one kill.
- `B-FT04` was killed in Round 02 and remains removed; `B-FT06` was killed in Round 03 and is now removed.
- The eleven Round 03 champions carry forward and the thirty-five named revisions are rebuilt without adding replacement specimens.
- Every surviving functional specimen preserves every Phase A reference recorded in the verbatim Round 02 and Round 03 receipts.
- `phase-a-lineage.js` remains the machine-readable ancestry source for functional candidates.

The thirty-two Round 10 keeps are canonical approved Phase A visual inputs. They are not thirty-two additional Round 04 candidates. The Round 02 application views and their feedback remain preserved as historical evidence, but Round 04 reviews only the forty-six functional survivors.

## Authority boundaries

- Product identity comes from `brand-kit/registry/products.json`.
- Visual grammar comes from the pinned Product Card 02 Phase A 1.0.0 contract and Round 10 approval.
- The 32 canonical Phase A keeps remain approved visual inputs and have a Round 04 candidate count of zero.
- SaaS, one-time, bundle and checkout prices are illustrative fixtures unless a consumer supplies authorised data.
- Components expose events and slots. They do not own network calls, payment-provider logic, Stripe keys, tax calculation or production prices.
- The golden homepage, generic application UI, Figma library and consumer migration remain outside this phase.

The final gate remains `H-EXP-04B-CARD-FUNCTIONAL-PROOF`. Nothing in this candidate package has production authority.

`round-01-feedback.json` records why Round 02 expanded the review surface. `round-02-feedback.json` is the verbatim human feedback receipt that drove Round 03. `round-03-feedback.json` is the exact human export that drives Round 04: 11 keep, 35 revise and 1 kill. All three are integrity-tracked and packaged; none grants Phase B production authority.

## Commands

```bash
.venv/bin/python brand-kit/expressions/product-card/phase-b/verify_product_component_pantry.py
```

Open the functional review at `http://127.0.0.1:8914/brand-kit/workbench/expressions/product-card/phase-b/`.
