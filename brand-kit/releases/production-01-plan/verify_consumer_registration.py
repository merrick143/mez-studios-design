#!/usr/bin/env python3
"""Verify exact PORT-04 consumer registration without touching the consumer."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


PLAN = Path(__file__).resolve().parent
BRAND_KIT = PLAN.parents[1]
FAILURES: list[str] = []
EXPECTED_REMOTE = "https://github.com/mezcorp-studio/ceos-notion-landingpage.git"
EXPECTED_LOCAL = "/Users/olivermerrick/Desktop/mez-studios/landing-pages/apps/ceos-notion-landingpage"
EXPECTED_RC2_MANIFEST = "129e0faab15173633987fe7c0c66bde982978f850c18b9689412968b718aa2e9"


def load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as error:
        FAILURES.append(f"invalid JSON {path}: {error}")
        return {}


def expect(condition: bool, message: str) -> None:
    if not condition:
        FAILURES.append(message)


registry = load(BRAND_KIT / "governance/consumer-register.json")
plan = load(PLAN / "release-plan.source.json")
task = load(BRAND_KIT / "llm/tasks/TASK-PORT-04-NAMED-CONSUMER-PROOF.json")
rc2_manifest_path = BRAND_KIT / "releases/production-01/1.0.0-rc.2/manifest.json"
rc2_manifest_sha = hashlib.sha256(rc2_manifest_path.read_bytes()).hexdigest() if rc2_manifest_path.is_file() else ""

records = registry.get("consumers", [])
expect(len(records) == 1, "consumer register must contain exactly one current registered consumer")
record = records[0] if records else {}
repository = record.get("repository", {})
expect(record.get("id") == "CON-MEZ-SYSTEMS-WEB-001", "registered consumer ID mismatch")
expect(repository.get("remote") == EXPECTED_REMOTE, "registered consumer remote mismatch")
expect(repository.get("defaultBranch") == "main", "registered consumer default branch mismatch")
expect(record.get("localCheckout") == EXPECTED_LOCAL, "registered local checkout mismatch")
expect(record.get("state") == "registered-not-integrated", "registration must not claim integration")
expect(record.get("migrationState") == "ready-for-read-only-audit", "consumer must begin with a read-only audit")
expect(record.get("authorityBoundary", {}).get("consumerMutationAuthorised") is False, "registration incorrectly authorises consumer mutation")
expect(record.get("authorityBoundary", {}).get("productionDeploymentAuthorised") is False, "registration incorrectly authorises deployment")
expect(record.get("humanConfirmation", {}).get("approver") == "Olli", "registration lacks Olli attribution")
candidate = record.get("designSystemCandidate", {})
expect(candidate.get("name") == "@mez-systems/design-system-web", "registered package name mismatch")
expect(candidate.get("version") == "1.0.0-rc.2", "registered package version mismatch")
expect(candidate.get("manifestSha256") == rc2_manifest_sha == EXPECTED_RC2_MANIFEST, "registered rc.2 manifest mismatch")

interface = plan.get("consumerInterface", {})
expect(interface.get("consumerId") == record.get("id"), "release plan consumer ID does not match registry")
expect(interface.get("repository") == record.get("repository"), "release plan remote identity does not match registry")
expect(interface.get("localCheckout") == EXPECTED_LOCAL, "release plan local checkout does not match registry")
expect(interface.get("registrationRecord") == "brand-kit/governance/consumer-register.json", "release plan registration record is missing")
expect(interface.get("registrationRequiredBeforeIntegration") is False, "release plan still claims registration is missing")
expect(interface.get("runtimeCrossRepositoryImportAllowed") is False, "cross-repository runtime imports became allowed")

expect(task.get("status") == "ready", "PORT-04 must become ready after exact registration")
expect("brand-kit/governance/consumer-register.json" in task.get("inputs", {}).get("requiredFiles", []), "PORT-04 does not require the registration record")
expect(task.get("humanGate", {}).get("required") is True, "PORT-04 human gate is no longer required")
expect(task.get("humanGate", {}).get("gateId") == "H-PORT-04-NAMED-CONSUMER-PROOF", "PORT-04 human gate identity drifted")

if FAILURES:
    print("PORT-04 CONSUMER REGISTRATION: FAIL")
    for failure in FAILURES:
        print(f"- {failure}")
    raise SystemExit(1)

print("PORT-04 CONSUMER REGISTRATION: PASS")
print("- CON-MEZ-SYSTEMS-WEB-001 resolves to mezcorp-studio/ceos-notion-landingpage")
print("- exact rc.2 manifest remains bound to the registered consumer proof")
print("- registration authorises read-only audit only; integration and deployment remain pending")
