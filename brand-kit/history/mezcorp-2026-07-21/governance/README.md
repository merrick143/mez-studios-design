# Mez Systems governance control plane

This directory is the operating layer for the Mez Systems design-system programme. It exists so a human or an LLM can determine what is authoritative, what is merely evidence, which decisions are open, and what must stop for human judgement.

## Read order

1. `PROGRAMME-CHARTER.md`
2. `MIGRATION-FIRST-GATE.md`
3. `decision-register.json`
4. `tasks/TASK-MIGRATION-CUTOVER-01.json`
5. `issue-register.json`
6. `consumer-register.json`
7. `artifact-register.json`
8. `reopened-decisions.md`
9. `H0-DECISION-PACKET.md`

## Operating rules

- The current production rules remain in force until a replacement decision is approved.
- A proposed decision is not permission to change production work.
- Every material output must name the decision IDs and source files it used.
- Reversible defaults may be trialled behind an explicit experiment label.
- Identity, architecture, publication, migration, and public-release choices require a human gate.
- Conflicts stop execution. They are not silently resolved by whichever file was read last.
- Generated registers must be reproducible from the baseline script or carry an explicit manual-owner field.

## Commands

Run the Phase 0 baseline from the repository root:

```bash
python3 departments/cmo/brand-library/brands/mez-systems/governance/scripts/build_baseline.py
python3 departments/cmo/brand-library/brands/mez-systems/governance/scripts/validate_phase_zero.py
```

Run the preserved Phase 2 TR-5 calibration gate from the Mez Systems pack root:

```bash
python3 governance/scripts/validate_phase_two_tr5.py
```

This confirms the historical 12 controlled pairs, copy equality, dimension coverage, local response capture, export contract, reduced-motion support, and denial of production authority. The round was later invalidated for taste calibration and remains evidence only.

Run the current Phase 2 authority and Hero 03 checkpoint:

```bash
python3 governance/scripts/validate_phase_two_tr6.py
```

Run the migration-first authority gate from the Mez Systems pack root:

```bash
python3 governance/scripts/validate_migration_first.py
```

This confirms the pushed recovery target, the three programme decisions, the next bounded human gate and the explicit separation between pre-cutover requirements and post-cutover backlog. It does not transfer canonical or production authority.

The baseline builder updates `artifact-register.json` and the dated `baseline/2026-07-19/manifest.json`. The validator checks JSON syntax, schema self-consistency, task and receipt examples, stable IDs, required control files, and screenshot evidence.
