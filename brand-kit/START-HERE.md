# Start here: Mez Systems design system

Status: canonical control plane active on `main`; foundations next

## What this repository is

`brand-kit/` is the governed home for the Mez Systems identity, foundations, product expressions, channel systems, machine contracts, releases, and human/LLM operating guidance.

It is intentionally broader than a visual brand guide. The finished system must let a human or LLM create excellent websites, ads, email, social, video, presentations, documents, product surfaces, and future formats while preserving one unmistakable identity.

## Current truth

- The canonical five-product roster and MZ-G13/G12/G06/G15/G20 assignments are approved.
- The complete source-gradient library, source authority, shared Living Core renderer, static twins, and Deep Mineral finish are approved.
- The migration identity release is `0.1.0-alpha.1`.
- The recovery branch has been integrated into `main`; new work starts from normal feature branches based on `main`.
- Typography and controls have approved directions but incomplete implementations.
- Foundations, product expressions, the golden homepage, consumer proof, Figma, channels, and broad LLM certification remain roadmap work.

See [Current state](docs/CURRENT-STATE.md) for the exact programme boundary.

## Reading order

1. [Shared agent guide](AGENT-GUIDE.md).
2. [Current state](docs/CURRENT-STATE.md).
3. [Execution roadmap](docs/ROADMAP.md).
4. [Approved decisions](governance/decisions.json).
5. [Full audit and end-to-end roadmap](docs/END-TO-END-ROADMAP.md) when planning a phase.
6. [Research index](docs/RESEARCH-INDEX.md) when making a design decision.
7. [Source map](docs/SOURCE-MAP.md) before changing authority or generated data.

## Run locally

Create the pinned Python environment once:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r brand-kit/source-pack/living-core/requirements.txt
```

Run the local workbench:

```bash
.venv/bin/python brand-kit/server.py --port 8914
```

Open `http://127.0.0.1:8914/brand-kit/`.

## Choose work from the roadmap

Do not restart the original audit or rebuild the gradient engine. Continue from the first incomplete task in [ROADMAP.md](docs/ROADMAP.md), unless Olli explicitly changes priority.

The next programme phase is foundation implementation: typography packaging, neutral and surface semantics, spacing and layout, geometry, controls, and accessibility fixtures.
