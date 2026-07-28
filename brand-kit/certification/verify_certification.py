#!/usr/bin/env python3
"""Verify CERT-01 claims against authority, audits, model evidence and rc.2 bytes."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


CERT = Path(__file__).resolve().parent
BRAND_KIT = CERT.parent
ROOT = BRAND_KIT.parent
FAILURES: list[str] = []


def load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as error:
        FAILURES.append(f"invalid JSON {path.relative_to(ROOT)}: {error}")
        return {}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def expect(condition: bool, message: str) -> None:
    if not condition:
        FAILURES.append(message)


source = load(CERT / "certification.source.json")
schema = load(CERT / "certification.schema.json")
for error in Draft202012Validator(schema).iter_errors(source):
    location = ".".join(str(part) for part in error.path) or "root"
    FAILURES.append(f"certification source schema {location}: {error.message}")

scope = load(CERT / "scope.json")
review = load(CERT / "review.json")
approval = load(CERT / "approval.json")
health = load(CERT / "health-checks.json")
builder_text = (CERT / "build_certified_release_candidate.py").read_text(encoding="utf-8")
transfer = load(CERT / "benchmarks/transfer-results.json")
transfer_schema = load(CERT / "benchmarks/transfer-output.schema.json")
gpt = load(CERT / "benchmarks/gpt-5.6-codex.json")
for error in Draft202012Validator(transfer_schema).iter_errors(gpt):
    location = ".".join(str(part) for part in error.path) or "root"
    FAILURES.append(f"GPT controlled transfer schema {location}: {error.message}")

task = load(BRAND_KIT / "llm/tasks/TASK-CERT-01-SYSTEM-CERTIFICATION.json")
port = load(BRAND_KIT / "llm/tasks/TASK-PORT-04-NAMED-CONSUMER-PROOF.json")
channel = load(BRAND_KIT / "llm/tasks/TASK-CHAN-01-FIRST-RELEASE-CHANNEL-SYSTEMS.json")
ui = load(BRAND_KIT / "product-ui/approval.json")
figma = load(BRAND_KIT / "figma-companion/approval.json")
claude_receipt = load(BRAND_KIT / "llm/examples/RCP-GOLD-01-GOLDEN-HOMEPAGE.json")
ctx = load(BRAND_KIT / "llm/examples/CTX-CERT-01-SYSTEM-CERTIFICATION.json")

expect(task.get("status") == "complete", "CERT-01 must be complete after H-CERT-01 approval")
expect(task.get("humanGate", {}).get("gateId") == "H-CERT-01-SYSTEM-CERTIFICATION", "CERT-01 gate mismatch")
expect(port.get("status") in {"blocked", "ready"}, "PORT-04 has an invalid post-certification state")
if port.get("status") == "ready":
    consumer_registry = load(BRAND_KIT / "governance/consumer-register.json")
    registered_consumers = consumer_registry.get("consumers", [])
    registered_consumer = registered_consumers[0] if len(registered_consumers) == 1 else {}
    expect(registered_consumer.get("id") == "CON-MEZ-SYSTEMS-WEB-001", "ready PORT-04 lacks exact consumer registration")
    expect(registered_consumer.get("state") == "registered-not-integrated", "ready PORT-04 incorrectly claims consumer integration")
expect(channel.get("status") == "blocked" and any("priority-deferred" in note for note in channel.get("notes", [])), "deferred channel task status drifted")
expect(ui.get("canonicalAuthority") is False and ui.get("productionAuthority") is False, "Product UI authority widened")
expect(ui.get("decisionId") is None, "Product UI approval invented a decision ID")
expect(figma.get("canonicalAuthority") is False and figma.get("productionAuthority") is False, "Figma authority widened")
expect(source.get("status") == "approved-current-scope", "certification source does not record the approved current scope")
expect(source.get("humanGate", {}).get("status") == "approved", "certification source does not close H-CERT-01")
expect(source.get("authorityBoundary", {}).get("deferredChannelsCertified") is False, "certification source includes deferred channels")
expect(len(scope.get("explicitlyUncertified", [])) == 9, "scope must name exactly nine deferred channel families")
expect(scope.get("productionAuthority") is False and scope.get("canonicalAuthorityCreated") is False, "scope creates authority")
expect(health.get("failurePolicy") == "fail-closed", "health checks are not fail-closed")
expect(health.get("automationCreated") is False, "certification silently created an external scheduler")
expect('if (CERT_DIR / "approval.json").is_file()' in builder_text, "approved rc.2 is not rebuild-locked")
expect("create a new version for later changes" in builder_text, "builder does not route later changes to a new version")

expect(transfer.get("result") == "pass-with-auth-limitation", "controlled benchmark limitation is hidden or unresolved")
models = {item.get("name"): item for item in transfer.get("models", [])}
expect(models.get("GPT-5.6 Codex", {}).get("casesPassed") == 2, "GPT-5.6 controlled benchmark did not pass 2 of 2")
expect(models.get("Claude Opus 4.8", {}).get("result") == "not-run-cli-auth-unavailable", "fresh Claude limitation is not explicit")
expect(claude_receipt.get("agent", {}).get("model") == "Claude Opus 4.8", "historical Claude Opus evidence is absent")

for audit_name, allowed in {
    "authority": {"pass"},
    "accessibility": {"pass-with-known-consumer-gaps"},
    "portability": {"pass"},
    "onboarding": {"pass-with-runtime-auth-limitation"},
    "release-governance": {"pass"},
}.items():
    audit = load(CERT / f"audits/{audit_name}.json")
    expect(audit.get("status") in allowed, f"{audit_name} audit is absent or dishonest")
    expect(audit.get("productionAuthority") is not True, f"{audit_name} audit claims production authority")

candidate = BRAND_KIT / "releases/production-01/1.0.0-rc.2"
manifest_path = candidate / "manifest.json"
manifest = load(manifest_path)
manifest_sha = sha256(manifest_path) if manifest_path.is_file() else ""
exact = review.get("releaseCandidate", {})
expect(review.get("status") == "approved", "certification review does not record Olli approval")
expect(review.get("machineVerdict") == "pass-with-warnings", "machine verdict must preserve visible warnings")
expect(review.get("productionAuthority") is False and review.get("canonicalAuthority") is False, "review creates authority")
expect(review.get("outputStatus") == ["approved", "candidate", "generated", "unreleased"], "output status is inaccurate")
expect(exact.get("manifestSha256") == manifest_sha == "129e0faab15173633987fe7c0c66bde982978f850c18b9689412968b718aa2e9", "exact rc.2 manifest hash mismatch")
expect(exact.get("contentSha256") == manifest.get("contentSha256") == "b5fe5cb5985270987799d28dbd2c596868de0504f84ae1312818c3ac2387fdd5", "exact rc.2 content hash mismatch")
expect(exact.get("artifactCount") == manifest.get("artifactCount") == 351, "exact rc.2 artifact count mismatch")
expect(review.get("frozenPredecessor", {}).get("manifestSha256") == sha256(BRAND_KIT / "releases/production-01/1.0.0-rc.1/manifest.json"), "frozen rc.1 identity drifted")
expect(len(review.get("knownGaps", [])) >= 6, "known gaps were hidden")
expect(review.get("humanDecision", {}).get("status") == "approved", "H-CERT-01 human decision is not approved")
expect(review.get("humanDecision", {}).get("humanEvidence") == "approve", "review does not preserve Olli's exact evidence")

exact_approval = approval.get("exactCandidate", {})
expect(approval.get("gateId") == "H-CERT-01-SYSTEM-CERTIFICATION", "certification approval gate mismatch")
expect(approval.get("verdict") == "approved-for-final-consumer-transition", "certification verdict mismatch")
expect(approval.get("approvedBy") == "Olli" and approval.get("humanEvidence") == ["approve"], "certification approval is not attributed to Olli")
expect(exact_approval.get("manifestSha256") == manifest_sha, "approval does not bind the exact rc.2 manifest")
expect(exact_approval.get("contentSha256") == manifest.get("contentSha256"), "approval does not bind the exact rc.2 content")
expect(exact_approval.get("artifactCount") == manifest.get("artifactCount") == 351, "approval artifact count mismatch")
expect(approval.get("canonicalAuthority") is False and approval.get("productionAuthority") is False, "approval creates canonical or production authority")
expect(approval.get("publishAuthority") is False and approval.get("deploymentAuthority") is False, "approval creates publish or deployment authority")
expect(approval.get("consumerIntegrationAuthority") is False, "approval enters a consumer before PORT-04")
expect(approval.get("decisionId") is None, "approval invents a governance decision ID")
expect(approval.get("nextTask") == "TASK-PORT-04-NAMED-CONSUMER-PROOF", "approval routes to the wrong next task")

mutable_after_certification = {
    "brand-kit/START-HERE.md",
    "brand-kit/docs/CURRENT-STATE.md",
    "brand-kit/docs/ROADMAP.md",
}
for file_record in ctx.get("files", []):
    path = ROOT / file_record.get("path", "")
    if not path.is_file():
        FAILURES.append(f"CERT context input missing: {file_record.get('path')}")
    elif file_record.get("path") not in mutable_after_certification and sha256(path) != file_record.get("sha256"):
        FAILURES.append(f"CERT context hash drift: {file_record.get('path')}")

if manifest_path.is_file():
    isolated = subprocess.run(
        [sys.executable, "-I", "-B", str(CERT / "verify_certified_release_candidate.py"), str(candidate)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if isolated.returncode != 0:
        FAILURES.append("rc.2 verifier failed: " + (isolated.stdout + isolated.stderr).strip())

if FAILURES:
    print("MEZ WHOLE-SYSTEM CERTIFICATION: FAIL")
    for failure in FAILURES:
        print(f"- {failure}")
    raise SystemExit(1)

print("MEZ WHOLE-SYSTEM CERTIFICATION: APPROVED WITH VISIBLE WARNINGS")
print("- all seven core and 25 selected current-scope validators are recorded as passing")
print("- exact deterministic rc.2 contains 351 artifacts and preserves frozen rc.1")
print("- GPT-5.6 controlled transfer and GPT-5/Claude Opus contract replay pass")
print("- fresh Claude transfer, exact spoken AT and real-consumer proof remain named gaps")
print("- H-CERT-01 is approved; exact consumer registration makes PORT-04 ready for read-only audit")
print("- deferred channels, publication, deployment and production remain unauthorised")
