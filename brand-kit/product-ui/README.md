# Product UI foundation

`TASK-UI-01-PRODUCT-UI-DATA-VISUALISATION` establishes the first code-first product interface grammar for Mez Systems. Olli approved the operational-ledger direction through `H-UI-01-PRODUCT-UI-FOUNDATION` on 28 July 2026. It is an approved foundation direction, not a canonical or production product screen and not production authority.

The first composition is an **operational ledger**. It deliberately uses repository facts rather than invented customers, metrics or workflows: one application shell, one dense ledger, one contextual inspector and one accessible status distribution. This gives the system real interface evidence while the actual AI OS product screens remain outside the repository.

## Files

- `product-ui-foundation.source.json` — approved foundation-direction authority, anatomy, behaviour and data-truth contract.
- `product-ui-foundation.schema.json` — machine validation for the source contract.
- `review.json` — measured review evidence, honest gaps and human gate state.
- `verify_product_ui_contract.py` — checks source/schema/review, fixture lineage and promised implementation behaviour.
- `../workbench/product-ui/` — dependency-free browser review surface.

## Run

From the repository root:

```bash
python3 -m http.server 8915
```

Open `http://127.0.0.1:8915/brand-kit/workbench/product-ui/`.

Run the bounded verifier:

```bash
python3 brand-kit/product-ui/verify_product_ui_contract.py
```

## Authority boundary

This approved foundation owns application-shell geometry, navigation, ledger/table behaviour, density, filtering, sorting, selection, contextual inspection, semantic status display, responsive recomposition and the accessible data-view pattern for its recorded scope.

It does not own product content, production data, authentication, permissions, persistence, analytics, routing, export behaviour or consumer state. The fixture is review evidence only. Product-specific workflows require a separate bounded task backed by real evidence.
