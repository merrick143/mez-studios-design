#!/usr/bin/env python3
"""Serve the Brand Kit Workbench and generate non-canonical candidates locally."""

from __future__ import annotations

import argparse
import base64
import json
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from functools import partial
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent
WORKSPACE = HERE / "workspace"
CANDIDATES = WORKSPACE / "candidates"
GENERATOR = HERE / "source-pack" / "living-core" / "candidate.py"
ID_PATTERN = re.compile(r"^MZ-G\d{2,3}$")
SLUG_PATTERN = re.compile(r"^[a-z0-9-]+$")
MAX_REQUEST = 18 * 1024 * 1024


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def list_candidates() -> list[dict]:
    if not CANDIDATES.is_dir():
        return []
    rows: list[dict] = []
    for directory in sorted(CANDIDATES.iterdir(), reverse=True):
        record_path = directory / "candidate.json"
        if not directory.is_dir() or not record_path.is_file():
            continue
        record = read_json(record_path)
        decision_path = directory / "decision.json"
        rows.append(
            {
                "slug": directory.name,
                "candidate": record,
                "decision": read_json(decision_path) if decision_path.is_file() else None,
                "previewUrl": f"/brand-kit/workspace/candidates/{directory.name}/preview.html",
            }
        )
    return rows


class WorkbenchHandler(SimpleHTTPRequestHandler):
    server_version = "MezBrandKit/1.0"

    def json_response(self, value: object, status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(value).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def read_request_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0 or length > MAX_REQUEST:
            raise ValueError("Request is empty or exceeds the 18 MB local limit")
        return json.loads(self.rfile.read(length))

    def do_GET(self) -> None:
        if self.path == "/api/candidates":
            self.json_response({"localApi": True, "candidates": list_candidates()})
            return
        super().do_GET()

    def do_POST(self) -> None:
        try:
            if self.path == "/api/candidates":
                self.create_candidate()
                return
            if self.path == "/api/decisions":
                self.record_decision()
                return
            self.json_response({"error": "Unknown endpoint"}, HTTPStatus.NOT_FOUND)
        except (ValueError, json.JSONDecodeError) as error:
            self.json_response({"error": str(error)}, HTTPStatus.BAD_REQUEST)
        except subprocess.CalledProcessError as error:
            message = error.stderr.strip() or error.stdout.strip() or "Candidate generation failed"
            self.json_response({"error": message}, HTTPStatus.UNPROCESSABLE_ENTITY)
        except Exception as error:  # local workbench: return a bounded message, not a traceback
            self.json_response({"error": f"Local candidate operation failed: {error}"}, HTTPStatus.INTERNAL_SERVER_ERROR)

    def create_candidate(self) -> None:
        payload = self.read_request_json()
        candidate_id = str(payload.get("candidateId", "")).strip().upper()
        product = str(payload.get("product", "")).strip()
        filename = Path(str(payload.get("filename", "source.png"))).name
        encoded = str(payload.get("base64", ""))

        if not ID_PATTERN.fullmatch(candidate_id):
            raise ValueError("Candidate ID must match MZ-G## or MZ-G###")
        if not 2 <= len(product) <= 80:
            raise ValueError("Product name must contain 2 to 80 characters")
        if not encoded:
            raise ValueError("Choose a source image")
        try:
            source_bytes = base64.b64decode(encoded, validate=True)
        except Exception as error:
            raise ValueError("Source image payload is not valid base64") from error
        if len(source_bytes) > 16 * 1024 * 1024:
            raise ValueError("Source image exceeds the 16 MB candidate limit")

        stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        slug = f"{candidate_id.lower()}-{stamp}"
        output = CANDIDATES / slug
        CANDIDATES.mkdir(parents=True, exist_ok=True)
        if output.exists():
            raise ValueError("Candidate output already exists; retry in one second")

        suffix = Path(filename).suffix.lower()
        if suffix not in {".png", ".jpg", ".jpeg", ".webp"}:
            suffix = ".png"
        with tempfile.TemporaryDirectory(prefix="mez-brand-kit-") as temporary:
            source = Path(temporary) / f"source{suffix}"
            source.write_bytes(source_bytes)
            result = subprocess.run(
                [
                    sys.executable,
                    str(GENERATOR),
                    "--source",
                    str(source),
                    "--id",
                    candidate_id,
                    "--product",
                    product,
                    "--output",
                    str(output),
                ],
                cwd=GENERATOR.parent,
                text=True,
                capture_output=True,
                check=True,
            )

        self.json_response(
            {
                "ok": True,
                "slug": slug,
                "previewUrl": f"/brand-kit/workspace/candidates/{slug}/preview.html",
                "candidate": read_json(output / "candidate.json"),
                "generatorOutput": result.stdout.strip(),
            },
            HTTPStatus.CREATED,
        )

    def record_decision(self) -> None:
        payload = self.read_request_json()
        slug = str(payload.get("slug", ""))
        verdict = str(payload.get("verdict", ""))
        note = str(payload.get("note", "")).strip()
        if not SLUG_PATTERN.fullmatch(slug):
            raise ValueError("Candidate slug is invalid")
        if verdict not in {"select", "edit", "reject"}:
            raise ValueError("Verdict must be select, edit or reject")
        directory = CANDIDATES / slug
        candidate_path = directory / "candidate.json"
        if not candidate_path.is_file():
            raise ValueError("Candidate does not exist")
        candidate = read_json(candidate_path)
        decision = {
            "schemaVersion": "1.0.0",
            "candidateId": candidate["candidateId"],
            "product": candidate["product"],
            "verdict": verdict,
            "note": note,
            "decidedAt": datetime.now(timezone.utc).isoformat(),
            "productionAuthority": False,
            "mutatesCanonicalAuthority": False,
        }
        write_json(directory / "decision.json", decision)
        self.json_response({"ok": True, "decision": decision})


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Serve the Mez Brand Kit Workbench")
    parser.add_argument("--port", type=int, default=8914)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    handler = partial(WorkbenchHandler, directory=str(REPO_ROOT))
    server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    print(f"Mez Brand Kit Workbench: http://127.0.0.1:{args.port}/brand-kit/")
    print("Candidate writes are isolated under brand-kit/workspace/ and have no canonical authority.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nWorkbench stopped.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
