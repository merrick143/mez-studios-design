#!/usr/bin/env python3
"""Verify the exact PORT-03 approval without widening it into release authority."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


PLAN = Path(__file__).resolve().parent
BRAND_KIT = PLAN.parents[1]
PACKAGE = BRAND_KIT / "releases/production-01/1.0.0-rc.1"
FAILURES: list[str] = []


def load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as error:
        FAILURES.append(f"invalid JSON {path}: {error}")
        return {}


def expect(condition: bool, message: str) -> None:
    if not condition:
        FAILURES.append(message)


approval = load(PLAN / "release-candidate-approval.json")
verification = load(PLAN / "port-03-verification.json")
release_plan = load(PLAN / "release-plan.source.json")
payload = load(PLAN / "operating-proof-review/payload.json")
manifest_path = PACKAGE / "manifest.json"
manifest = load(manifest_path)
task_03 = load(BRAND_KIT / "llm/tasks/TASK-PORT-03-PRODUCTION-RELEASE-ASSEMBLY.json")
task_04 = load(BRAND_KIT / "llm/tasks/TASK-PORT-04-NAMED-CONSUMER-PROOF.json")
fig_task = load(BRAND_KIT / "llm/tasks/TASK-FIG-01-FIGMA-COMPANION.json")
sequence = load(BRAND_KIT / "docs/consumer-transition-sequence.json")

manifest_sha = hashlib.sha256(manifest_path.read_bytes()).hexdigest() if manifest_path.is_file() else ""
exact = approval.get("exactPackage", {})
expect(approval.get("gateId") == "H-PORT-03-PRODUCTION-RELEASE-CANDIDATE", "wrong or missing PORT-03 gate")
expect(approval.get("verdict") == "approved-for-named-consumer-proof", "candidate is not approved for named-consumer proof")
expect(approval.get("approvedBy") == "Olli", "approval is not attributed to Olli")
expect(approval.get("productionAuthority") is False, "approval incorrectly claims production authority")
expect(approval.get("resultingStatus") == "approved-candidate-unreleased", "approval status is not approved-candidate-unreleased")
expect(exact.get("manifestSha256") == manifest_sha, "approved manifest SHA-256 does not match package bytes")
expect(exact.get("contentSha256") == manifest.get("contentSha256"), "approved content SHA-256 does not match package manifest")
expect(exact.get("artifactCount") == manifest.get("artifactCount") == 312, "approved artifact count does not match package")

not_authorised = set(approval.get("notAuthorised", []))
expect("Publishing the package." in not_authorised, "publication exclusion is absent")
expect("Deploying a website." in not_authorised, "deployment exclusion is absent")
expect("Assigning production version 1.0.0." in not_authorised, "1.0.0 exclusion is absent")

expect(payload.get("status") == "redacted-approved", "redacted proof is not approved")
expect(payload.get("review", {}).get("reviewedBy") == "Olli", "redacted proof review is not attributed to Olli")
expect(verification.get("status") == "complete", "PORT-03 verification is not complete")
expect(verification.get("humanGate", {}).get("status") == "approved", "PORT-03 verification gate is not approved")
expect(task_03.get("status") == "complete", "TASK-PORT-03 is not complete")
expect(task_04.get("status") in {"blocked", "ready", "complete"}, "TASK-PORT-04 has an invalid lifecycle state")
expect(task_04.get("inputs", {}).get("consumerIds") == ["CON-MEZ-SYSTEMS-WEB-001"], "TASK-PORT-04 has the wrong named consumer")
expect(fig_task.get("status") in {"awaiting-human", "complete"}, "TASK-FIG-01 has an invalid state")
expect(sequence.get("frozenMilestone", {}).get("manifestSha256") == manifest_sha, "consumer-last sequence changed the approved rc.1 bytes")
expect(sequence.get("orderedWork", [])[-1].get("taskId") == "TASK-PORT-04-NAMED-CONSUMER-PROOF", "PORT-04 must remain the final transition")

consumer = release_plan.get("consumerInterface", {})
expect(consumer.get("consumerId") == "CON-MEZ-SYSTEMS-WEB-001", "release plan named consumer mismatch")
if consumer.get("repository") is None:
    expect(task_04.get("status") == "blocked", "PORT-04 must remain blocked before registration")
else:
    registry = load(BRAND_KIT / "governance/consumer-register.json")
    records = registry.get("consumers", [])
    registered = records[0] if len(records) == 1 else {}
    expect(consumer.get("repository") == registered.get("repository"), "registered consumer identity drifted")
    expect(task_04.get("status") in {"ready", "complete"}, "registered PORT-04 has an invalid lifecycle state")
    if task_04.get("status") == "complete":
        expect(registered.get("state") == "integrated-production", "complete PORT-04 lacks the production integration record")
followups = {item.get("taskId"): item.get("status") for item in release_plan.get("followUps", [])}
expect(followups.get("TASK-PORT-03-PRODUCTION-RELEASE-ASSEMBLY") == "complete", "release plan does not close PORT-03")
expect(followups.get("TASK-PORT-04-NAMED-CONSUMER-PROOF") in {"deferred-until-system-ready-and-consumer-registration", "ready-for-read-only-consumer-audit"}, "release plan has the wrong PORT-04 state")

if FAILURES:
    print("PORT-03 CLOSURE: FAIL")
    for failure in FAILURES:
        print(f"- {failure}")
    raise SystemExit(1)

print("PORT-03 CLOSURE: PASS")
print(f"- exact approved manifest {manifest_sha[:12]} matches 312 packaged artifacts")
print("- Olli approved both redacted proof and package for named-consumer proof")
print("- publication, deployment and production 1.0.0 remain unauthorised")
print("- rc.1 remains frozen; later completed gates do not widen the original approval")
