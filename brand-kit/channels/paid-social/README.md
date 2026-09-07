# Paid social · Price-Anchored Product Proof

Status: `CRAFT_APPROVED` format inside an otherwise uncertified paid-social channel pack.

This pack turns the human-approved AI OS R07 batch into a reusable 4:5 static format. It owns the format grammar, content model, approved examples, anti-examples, Figma source pointers, export settings, outcome hypothesis and preflight gates. It does not certify all paid advertising or prove that this format performs.

## What the format does

The opening line names a verified expensive buying category. The next line offers a smaller, truthful first step. A real product screen then proves what the buyer receives, while three restrained floating cards translate visible product capability into outcomes.

The comparison must be a sequencing argument, not a feature-equivalence claim. Use language such as `start with` or `install first` when a product does not replace discovery, migration, training, integrations or bespoke implementation.

## Source hierarchy

1. `brand-kit/` remains canonical.
2. This pack owns the approved format contract.
3. The product screenshot library owns authentic screenshot masters and crop metadata.
4. Figma is the editable authoring and review surface.
5. Notion mirrors the format definition and operational SOP for discoverability.

## Start here

1. Read `AGENTS.md`, `strategy-and-use-cases.md`, `SOP.md` and `content-model.schema.json`.
2. Use `$build-price-anchored-product-static`.
3. Start from a duplicate of one approved R07 frame. Never edit the approved R07 section in place.
4. Run `.venv/bin/python brand-kit/channels/paid-social/validator/validate_format.py --mode craft`.
5. Before publishing, run the separate public preflight in `SOP.md`. The current pack intentionally fails `--mode publish` until those campaign-specific approvals are recorded.

## Approved reference set

- R07-01: champion
- R07-05: strongest alternate
- R07-03: safest sequencing version
- R07-02 and R07-04: controlled comparison variants

All five are 1080 × 1350 PNGs and editable in the linked Figma section.

## Notion mirrors

- [Format Library entry](https://app.notion.com/p/3b47e41bed0b81c095bfc21eff316f35)
- [Execution SOP](https://app.notion.com/p/3b47e41bed0b81e3ae77e18a0465d972)

The pages are cross-linked and recorded in `notion-sync.json`. No product-proof image was copied into Notion because the current media is not approved for that transfer.
