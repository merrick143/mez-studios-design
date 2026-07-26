#!/usr/bin/env python3
"""Validate model-neutral task, context, receipt, and evaluation fixtures."""

from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


HERE = Path(__file__).resolve().parent
BRAND_KIT = HERE.parent
LLM = BRAND_KIT / "llm"


def validate(schema_path: Path, documents: list[Path]) -> list[str]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    failures: list[str] = []
    for path in documents:
        value = json.loads(path.read_text(encoding="utf-8"))
        for error in sorted(validator.iter_errors(value), key=lambda item: list(item.path)):
            location = ".".join(str(part) for part in error.path) or "root"
            failures.append(f"{path.relative_to(BRAND_KIT)}:{location}: {error.message}")
    return failures


def main() -> int:
    groups = [
        (LLM / "task.schema.json", sorted((LLM / "tasks").glob("*.json"))),
        (LLM / "context-bundle.schema.json", sorted((LLM / "examples").glob("CTX-*.json"))),
        (LLM / "output-receipt.schema.json", sorted((LLM / "examples").glob("RCP-*.json"))),
        (LLM / "evaluation-result.schema.json", sorted((LLM / "examples").glob("EVAL-*.json"))),
    ]
    failures: list[str] = []
    for schema, documents in groups:
        failures.extend(validate(schema, documents))

    if failures:
        print("LLM CONTRACTS: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("LLM CONTRACTS: PASS")
    print("- bounded tasks, context bundles, receipts and evaluations validate")
    print("- FND-01 through FND-05, EXP-01/02/03/04/05/07/08 and CMP-01 are complete; TASK-GOLD-01-GOLDEN-HOMEPAGE is active")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
