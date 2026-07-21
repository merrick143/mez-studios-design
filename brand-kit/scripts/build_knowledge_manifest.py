#!/usr/bin/env python3
"""Build the frozen Mezcorp knowledge-snapshot manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
BRAND_KIT = HERE.parent
SNAPSHOT = BRAND_KIT / "history" / "mezcorp-2026-07-21"
OUTPUT = BRAND_KIT / "history" / "mezcorp-2026-07-21-manifest.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    if not SNAPSHOT.is_dir():
        raise SystemExit(f"Knowledge snapshot not found: {SNAPSHOT}")

    records = []
    for path in sorted(item for item in SNAPSHOT.rglob("*") if item.is_file()):
        records.append(
            {
                "path": path.relative_to(SNAPSHOT).as_posix(),
                "sha256": sha256(path),
                "bytes": path.stat().st_size,
            }
        )

    payload = {
        "schemaVersion": "1.0.0",
        "snapshotId": "MEZCORP-KNOWLEDGE-2026-07-21",
        "sourceRepository": "merrick143/mezcorp-claudecode",
        "sourceBranch": "codex/mez-gradient-system",
        "sourceCommit": "c742224a2e095d5671f821a33fa9d3fc35c014c0",
        "sourcePath": "departments/cmo/brand-library/brands/mez-systems",
        "role": "frozen-documentation-and-machine-record-evidence",
        "productionAuthority": False,
        "fileCount": len(records),
        "markdownCount": sum(record["path"].endswith(".md") for record in records),
        "files": records,
    }
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(BRAND_KIT)} with {len(records)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
