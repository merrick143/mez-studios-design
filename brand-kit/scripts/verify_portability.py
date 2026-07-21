#!/usr/bin/env python3
"""Verify the human/LLM knowledge transfer and shared skill adapters."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
BRAND_KIT = HERE.parent
REPO = BRAND_KIT.parent
SNAPSHOT = BRAND_KIT / "history" / "mezcorp-2026-07-21"
HISTORY_MANIFEST = BRAND_KIT / "history" / "mezcorp-2026-07-21-manifest.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    failures: list[str] = []
    required = [
        REPO / "AGENTS.md",
        REPO / "CLAUDE.md",
        BRAND_KIT / "AGENT-GUIDE.md",
        BRAND_KIT / "START-HERE.md",
        BRAND_KIT / "docs/CURRENT-STATE.md",
        BRAND_KIT / "docs/ROADMAP.md",
        BRAND_KIT / "docs/END-TO-END-ROADMAP.md",
        BRAND_KIT / "docs/PROGRAMME-CHARTER.md",
        BRAND_KIT / "docs/HUMAN-LLM-WORKFLOW.md",
        BRAND_KIT / "docs/HANDOFF.md",
        BRAND_KIT / "docs/RESEARCH-INDEX.md",
        BRAND_KIT / "llm/README.md",
        BRAND_KIT / "llm/tasks/TASK-FND-01-TYPOGRAPHY.json",
        BRAND_KIT / "governance/evidence-paths.json",
        BRAND_KIT / "skills/codex-made-it/SKILL.md",
        BRAND_KIT / "skills/codex-made-it/references/product-disc-contract.md",
        HISTORY_MANIFEST,
    ]
    for path in required:
        if not path.is_file() or path.stat().st_size == 0:
            failures.append(f"missing or empty portable file: {path.relative_to(REPO)}")

    canonical_skill = (BRAND_KIT / "skills/codex-made-it").resolve()
    adapters = [
        REPO / ".agents/skills/codex-made-it",
        REPO / ".claude/skills/codex-made-it",
        BRAND_KIT / "llm/skills/codex-made-it",
    ]
    for adapter in adapters:
        if not adapter.is_symlink():
            failures.append(f"skill adapter is not a symlink: {adapter.relative_to(REPO)}")
        elif adapter.resolve() != canonical_skill:
            failures.append(f"skill adapter does not resolve to canonical skill: {adapter.relative_to(REPO)}")

    skill_path = BRAND_KIT / "skills/codex-made-it/SKILL.md"
    if skill_path.is_file():
        skill = skill_path.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n", skill, re.DOTALL)
        if not match:
            failures.append("canonical skill is missing YAML frontmatter")
        else:
            frontmatter = match.group(1)
            if "name: codex-made-it" not in frontmatter or "description:" not in frontmatter:
                failures.append("canonical skill frontmatter lacks name or description")

    if HISTORY_MANIFEST.is_file():
        manifest = json.loads(HISTORY_MANIFEST.read_text(encoding="utf-8"))
        records = manifest.get("files", [])
        if manifest.get("markdownCount") != 104:
            failures.append(f"historical Markdown count must remain 104, found {manifest.get('markdownCount')}")
        if manifest.get("fileCount") != len(records):
            failures.append("historical manifest file count is inconsistent")
        for record in records:
            path = SNAPSHOT / record["path"]
            if not path.is_file():
                failures.append(f"historical record is missing: {record['path']}")
            elif sha256(path) != record["sha256"]:
                failures.append(f"historical record hash drift: {record['path']}")

    decisions_path = BRAND_KIT / "governance/decisions.json"
    evidence_paths = BRAND_KIT / "governance/evidence-paths.json"
    if decisions_path.is_file() and evidence_paths.is_file():
        decisions = json.loads(decisions_path.read_text(encoding="utf-8"))
        evidence = json.loads(evidence_paths.read_text(encoding="utf-8")).get("decisions", {})
        decision_ids = {decision.get("id") for decision in decisions.get("decisions", [])}
        if set(evidence) != decision_ids:
            failures.append("decision evidence map does not cover the immutable decision ledger exactly")
        for decision_id, source in evidence.items():
            if not (REPO / source).is_file():
                failures.append(f"decision evidence does not resolve: {decision_id} -> {source}")

    active_docs = [
        BRAND_KIT / "START-HERE.md",
        BRAND_KIT / "AGENT-GUIDE.md",
        *sorted(
            path
            for path in (BRAND_KIT / "docs").glob("*.md")
            if path.name != "END-TO-END-ROADMAP.md"
        ),
        BRAND_KIT / "llm/README.md",
    ]
    for path in active_docs:
        text = path.read_text(encoding="utf-8")
        if "/Users/olivermerrick/" in text:
            failures.append(f"active documentation contains a machine-specific path: {path.relative_to(REPO)}")

    branch_close = (BRAND_KIT / "docs/MIGRATION-PLAN.md").read_text(encoding="utf-8")
    close_section = branch_close.split("## Branch-close checklist", 1)[-1]
    for forbidden in ("Geist asset", "Foundation tokens", "Product-expression suite", "consumer ingests"):
        if forbidden in close_section:
            failures.append(f"migration branch-close checklist still blocks on post-migration work: {forbidden}")

    if failures:
        print("KNOWLEDGE PORTABILITY: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("KNOWLEDGE PORTABILITY: PASS")
    print("- active programme guidance and the complete roadmap are present")
    print("- 104 historical Markdown files remain hashed and non-authoritative")
    print("- Claude Code and Codex resolve one canonical skill source")
    print("- approved decision evidence resolves inside the repository")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
