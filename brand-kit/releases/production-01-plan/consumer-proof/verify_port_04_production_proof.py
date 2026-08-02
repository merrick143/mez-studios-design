#!/usr/bin/env python3
"""Verify the recorded PORT-04 production-consumer handoff."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
BRAND_KIT = HERE.parents[2]
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


proof = load(HERE / "port-04-production-proof.json")
registry = load(BRAND_KIT / "governance/consumer-register.json")
task = load(BRAND_KIT / "llm/tasks/TASK-PORT-04-NAMED-CONSUMER-PROOF.json")
status = load(BRAND_KIT / "data/status.json")
manifest_path = BRAND_KIT / "releases/production-01/1.0.0-rc.2/manifest.json"
manifest_sha = hashlib.sha256(manifest_path.read_bytes()).hexdigest() if manifest_path.is_file() else ""

consumers = registry.get("consumers", [])
consumer = consumers[0] if len(consumers) == 1 else {}
integration = consumer.get("productionIntegration", {})

expect(proof.get("taskId") == "TASK-PORT-04-NAMED-CONSUMER-PROOF", "proof task mismatch")
expect(proof.get("gateId") == "H-PORT-04-NAMED-CONSUMER-PROOF", "proof gate mismatch")
expect(proof.get("approvedBy") == "Olli", "proof lacks Olli attribution")
expect(proof.get("status") == "deployed-approved-named-consumer", "proof status mismatch")
expect(proof.get("consumer", {}).get("mergeCommit") == "626580ab18624702912cad82c2c681ddb8f16cb2", "consumer merge commit mismatch")
expect(proof.get("consumer", {}).get("productionUrl") == "https://mez.systems/", "production URL mismatch")
expect(proof.get("designInput", {}).get("commit") == "0b07254636470e7da6cda174a34d49073d800f52", "design input commit mismatch")
expect(proof.get("designInput", {}).get("manifestSha256") == manifest_sha == "129e0faab15173633987fe7c0c66bde982978f850c18b9689412968b718aa2e9", "rc.2 manifest mismatch")
expect(proof.get("integrationBoundary", {}).get("runtimeCrossRepositoryImport") is False, "runtime cross-repository import became allowed")
expect(proof.get("integrationBoundary", {}).get("globalDesignSystemCssImport") is False, "global design-system CSS became allowed")
expect(proof.get("authority", {}).get("candidateProductionAuthority") is False, "proof promotes rc.2 to production authority")
expect(proof.get("authority", {}).get("packagePublished") is False, "proof claims package publication")
expect(consumer.get("state") == "integrated-production", "consumer register is not current")
expect(consumer.get("migrationState") == "deployed-and-human-approved", "consumer migration state is not closed")
expect(integration.get("consumerMergeCommit") == proof.get("consumer", {}).get("mergeCommit"), "register/proof commit mismatch")
expect(integration.get("proofRecord") == "brand-kit/releases/production-01-plan/consumer-proof/port-04-production-proof.json", "consumer proof path mismatch")
expect(task.get("status") == "complete", "PORT-04 task is not complete")
sections = {item.get("id"): item for item in status.get("sections", [])}
expect(sections.get("consumer-transition", {}).get("status") == "deployed-approved", "status summary is stale")

if FAILURES:
    print("PORT-04 PRODUCTION CONSUMER PROOF: FAIL")
    for failure in FAILURES:
        print(f"- {failure}")
    raise SystemExit(1)

print("PORT-04 PRODUCTION CONSUMER PROOF: PASS")
print("- consumer merge commit 626580ab is recorded as live at https://mez.systems/")
print("- rc.2 manifest remains exact, unpublished and non-authoritative for production release naming")
print("- the consumer adapter remains isolated with no runtime design-repository dependency")
