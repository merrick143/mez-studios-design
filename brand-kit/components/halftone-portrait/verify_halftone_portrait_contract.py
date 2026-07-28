#!/usr/bin/env python3
"""Verify the canonical CMP-05 Halftone Portrait contract.

This checks the things a reviewer should not have to check by hand: that the
source validates, that the candidate does not quietly claim authority it has
not been granted, and that the two rules the whole component leans on are
actually present in the code rather than only in the documentation.

Those two rules are:

  1. One animated instance at a time. Website Motion 1.0.0 permits one
     expressive event in the viewport.
  2. No machine learning at runtime. The cutout is baked into the media, so a
     consumer inherits no model, no wasm runtime and no network call.

A verifier that only reads JSON would pass a component that documented both and
implemented neither, so both are asserted against the JavaScript.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:  # pragma: no cover - environment guidance only
    print("jsonschema is required: use the pinned environment in brand-kit/START-HERE.md")
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parent
BRAND_KIT = ROOT.parents[1]
WORKBENCH = BRAND_KIT / "workbench" / "components" / "halftone-portrait"
DECISIONS = BRAND_KIT / "governance" / "post-cutover-decisions.json"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []

    source = read_json(ROOT / "halftone-portrait.source.json")
    review = read_json(ROOT / "review.json")
    schema = read_json(ROOT / "halftone-portrait.schema.json")
    gate_b = read_json(ROOT / "gate-b.json")
    responsive = read_json(ROOT / "responsive-evidence.json")
    approval = read_json(ROOT / "approval.json")
    decisions = read_json(DECISIONS)

    try:
        jsonschema.Draft202012Validator(schema).validate(source)
    except jsonschema.ValidationError as error:
        failures.append(f"source does not satisfy its schema: {error.message}")

    decision_id = "DEC-HALFTONE-PORTRAIT-COMPONENT-001"
    if source.get("productionAuthority") is not True or source.get("status") != "canonical":
        failures.append("canonical authority is missing from the source contract")
    if source.get("decisionIds") != [decision_id]:
        failures.append("source does not cite the exact promotion decision")
    if review.get("decisionId") != decision_id or review.get("verdict") != "approved":
        failures.append("review does not carry the approved promotion decision")
    if review.get("productionAuthority") is not True:
        failures.append("approved review does not grant bounded component authority")
    if approval.get("decisionId") != decision_id or approval.get("resultingStatus") != "canonical":
        failures.append("approval record does not promote the exact candidate")
    if approval.get("candidateRevision") != source.get("candidateRevision"):
        failures.append("approval record targets a different candidate revision")
    indexed = {item.get("id"): item for item in decisions.get("decisions", [])}
    if indexed.get(decision_id, {}).get("source") != "brand-kit/components/halftone-portrait/approval.json":
        failures.append("promotion decision is absent from the post-cutover governance supplement")
    for key in ("componentId", "gateId", "taskId", "candidateRevision"):
        if source.get(key) != review.get(key):
            failures.append(f"{key} disagrees between source and review")

    # Required files.
    for relative in (
        "README.md",
        "approval.json",
        "mez-halftone-portrait.js",
        "mez-halftone-portrait.css",
        "fixtures/static-html.html",
        "fixtures/react.jsx",
        "fixtures/media/PROVENANCE.md",
    ):
        if not (ROOT / relative).exists():
            failures.append(f"missing {relative}")
    if not WORKBENCH.joinpath("index.html").exists():
        failures.append("missing workbench page at workbench/components/halftone-portrait/index.html")

    js = (ROOT / "mez-halftone-portrait.js").read_text(encoding="utf-8")
    css = (ROOT / "mez-halftone-portrait.css").read_text(encoding="utf-8")

    # Rule 1: motion is allocated by default, and any escape from that default
    # is a recorded, human-attributed exception rather than a quiet edit.
    declared = source["motion"]["maximumLiveInstancesDefault"]
    if declared != 1:
        failures.append(f"default budget is {declared}; the allocated default must remain 1")
    if source["motion"]["defaultPolicy"] != "allocated":
        failures.append("default motion policy is not 'allocated'")
    exception = source.get("motionDecisionException", {})
    if "motion-policy" in js and exception.get("status") != "approved-bounded":
        failures.append("the code offers a motion-policy escape with no approved exception recorded")
    if exception and not exception.get("requestedBy"):
        failures.append("motion exception has no human attribution")
    if 'policy === "always"' not in js:
        failures.append("motion-policy is documented but the always path is not implemented")
    if "IntersectionObserver" not in js:
        failures.append("no IntersectionObserver: motion cannot be allocated by visibility")
    if "allocate" not in js or "releaseMotion" not in js:
        failures.append("no allocate/releaseMotion pair: the live instance is never handed over")
    if "prefers-reduced-motion" not in js:
        failures.append("reduced motion is not consulted in JavaScript")
    if "prefers-reduced-motion" not in css:
        failures.append("reduced motion is not acknowledged in CSS")

    # Rule 2: nothing is fetched and no model runs.
    banned = {
        "mediapipe": "MediaPipe must not be a runtime dependency",
        "tflite": "no model weights may be loaded at runtime",
        ".onnx": "no model weights may be loaded at runtime",
        "fetch(": "the component must not fetch anything",
        "XMLHttpRequest": "the component must not fetch anything",
        "importScripts": "the component must not load remote code",
    }
    lowered = js.lower()
    for needle, why in banned.items():
        if needle.lower() in lowered:
            failures.append(f"{why} (found '{needle}')")
    if re.search(r"""from\s+["'](https?:)?//""", js):
        failures.append("the component imports from a remote origin")

    # The element must exist and be registered under the documented tag.
    if 'customElements.define("mez-halftone-portrait"' not in js:
        failures.append("custom element mez-halftone-portrait is not registered")

    # Every documented attribute must actually be observed or read.
    documented = {entry["name"] for entry in source["attributes"]}
    for name in sorted(documented):
        if f'"{name}"' not in js:
            failures.append(f"attribute '{name}' is documented but never read")

    # The locked treatment must be expressible: every key maps to an attribute.
    for key in source["lockedTreatment"]["values"]:
        if key not in documented:
            failures.append(f"locked treatment sets '{key}', which is not a documented attribute")

    # Accepted limitations stay visible after promotion.
    if not review.get("knownGaps"):
        failures.append("approved review hides every accepted limitation")

    # Promotion evidence must describe the exact candidate bytes. Gate B does
    # not grant authority; the separate human decision does.
    if review.get("gateB", {}).get("record") != "brand-kit/components/halftone-portrait/gate-b.json":
        failures.append("review does not point to the exact Gate B record")
    if gate_b.get("candidateRevision") != source.get("candidateRevision") or gate_b.get("score", 0) < 64:
        failures.append("exact candidate has no passing Gate B score")
    if gate_b.get("productionAuthority") is not False or gate_b.get("blockingReasons"):
        failures.append("Gate B invents authority or retains a blocking reason")

    # The responsive receipt closes the review's declared evidence gap. It
    # checks the source contract rather than a hand-maintained second list.
    expected_viewports = source.get("testViewports", [])
    if responsive.get("declaredViewports") != expected_viewports:
        failures.append("responsive evidence does not cover every declared viewport")
    results = {item.get("viewport"): item for item in responsive.get("results", [])}
    if any(width not in results for width in expected_viewports):
        failures.append("responsive evidence is missing declared results")
    for width in expected_viewports:
        result = results.get(width, {})
        size = result.get("primarySizePx", [])
        if result.get("pageOverflowPx") != 0 or len(size) != 2 or size[0] != size[1]:
            failures.append(f"responsive proof failed at {width}px")
        if result.get("allocatedLive") != 1:
            failures.append(f"allocated motion proof drifted at {width}px")

    if failures:
        print("CMP-05 Halftone Portrait contract FAILED")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    print("CMP-05 Halftone Portrait contract OK")
    print(f"  status              {source['status']} {source['version']}")
    print(f"  production authority {source['productionAuthority']}")
    print(f"  default live budget  {declared} ({source['motion']['defaultPolicy']})")
    print(f"  bounded exception   {source.get('motionDecisionException', {}).get('status', 'none')}")
    print(f"  attributes          {len(documented)}")
    print(f"  open questions      {len(source['openQuestions'])}")
    print(f"  known gaps          {len(review['knownGaps'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
