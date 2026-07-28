#!/usr/bin/env python3
"""Run the verifier from the assembled release-candidate root."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "production-01" / "1.0.0-rc.1"


def main() -> int:
    verifier = PACKAGE / "verify.py"
    if not verifier.is_file():
        print(f"MEZ BUILT RELEASE CANDIDATE: FAIL\n- missing {verifier}")
        return 1
    return subprocess.run(
        [sys.executable, "-I", "-B", str(verifier)],
        cwd=PACKAGE,
        check=False,
        env={"PATH": "/usr/bin:/bin"},
    ).returncode


if __name__ == "__main__":
    raise SystemExit(main())
