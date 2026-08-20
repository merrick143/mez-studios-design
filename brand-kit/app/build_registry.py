#!/usr/bin/env python3
"""Generate brand-kit/app/registry.json from disk truth.

registry.source.json is the hand-authored overlay: navigation structure,
names, summaries and links. This script walks the repository for every
governance record (review.json / approval.json beside each item, plus the
two central registers), resolves each item's real status from those
records, builds the review queue automatically, and emits registry.json
for the console to render.

The console never trusts the overlay for status. If a record on disk says
awaiting-human-review, the item enters the Review zone even if nobody
edited the overlay. If a record disappears or disagrees, the item is
flagged. Run this after any review lands:

    python3 brand-kit/app/build_registry.py

No dependencies beyond the standard library, matching the repo's other
build_*.py scripts.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

APP = Path(__file__).resolve().parent
KIT = APP.parent

# Directories that may contain governance records for live items. Releases,
# dist mirrors and archives are excluded on purpose: they are frozen copies
# of records that already exist at the owning path.
SCAN_ROOTS = ["foundations", "expressions", "components", "golden", "product-ui"]
EXCLUDE_PARTS = {"dist", "dist-candidate", "node_modules", "fixtures"}

APPROVED_VERDICTS = {"approve", "approved", "approve-with-deferral"}
OPEN_VERDICTS = {"awaiting-human-review", "awaiting-review", "pending"}


def load(path: Path):
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as error:
        print(f"  ! unreadable {path.relative_to(KIT)}: {error}", file=sys.stderr)
        return None


def record_paths() -> list[Path]:
    found = []
    for root in SCAN_ROOTS:
        base = KIT / root
        if not base.is_dir():
            continue
        for name in ("review.json", "approval.json"):
            for path in base.rglob(name):
                if EXCLUDE_PARTS.intersection(path.parts):
                    continue
                found.append(path)
    return sorted(found)


def owner_key(path: Path) -> str:
    """components/testimonial-marquee/approval.json -> testimonial-marquee."""
    rel = path.relative_to(KIT)
    parts = rel.parts
    # golden/homepage/review.json -> golden-homepage; product-ui/approval.json -> product-ui
    if parts[0] == "golden":
        return "golden-homepage"
    if parts[0] == "product-ui":
        return "product-ui"
    if len(parts) >= 3 and parts[1] == "product-card" and parts[2] == "phase-b":
        return "product-card-phase-b"
    return parts[1]


def best_record(records: list[dict]) -> dict | None:
    """approval.json outranks review.json when both exist and agree on the
    decision; an open verdict outranks everything, because an open question
    must never be hidden by an older approval."""
    if not records:
        return None
    for record in records:
        verdict = str(record.get("verdict", "")).lower()
        if verdict in OPEN_VERDICTS or (
            verdict not in APPROVED_VERDICTS and not record.get("decisionId")
        ):
            return record
    for record in records:
        if record.get("_source", "").endswith("approval.json"):
            return record
    return records[0]


def main() -> int:
    overlay = load(APP / "registry.source.json")
    if overlay is None:
        print("registry.source.json is required", file=sys.stderr)
        return 1

    central: dict[str, dict] = {}
    for name in ("decisions.json", "post-cutover-decisions.json"):
        data = load(KIT / "governance" / name) or {}
        for record in data.get("decisions", []):
            central[record["id"]] = record

    by_owner: dict[str, list[dict]] = {}
    for path in record_paths():
        record = load(path)
        if not isinstance(record, dict):
            continue
        if "verdict" not in record and "decisionId" not in record:
            continue  # source/schema files named like records
        record["_source"] = str(path.relative_to(KIT))
        by_owner.setdefault(owner_key(path), []).append(record)

    known_ids: set[str] = set()
    queue_items: list[dict] = []
    decided_items: list[dict] = []
    drift: list[dict] = []

    # Overlay review-zone entries are metadata donors for the auto queue:
    # names, links and summaries for items the scan will find on disk.
    review_meta: dict[str, dict] = {}
    for zone in overlay["zones"]:
        if zone["id"] != "review":
            continue
        for group in zone.get("groups", []):
            for item in group.get("items", []):
                review_meta[item["id"]] = item

    def resolve(item: dict) -> dict:
        item = dict(item)
        known_ids.add(item["id"])
        records = list(by_owner.get(item["id"], []))
        for alias in item.get("aliases", []):
            known_ids.add(alias)
            records += by_owner.get(alias, [])
        record = best_record(records)
        if record is None:
            item["statusSource"] = "declared"
            return item

        item["record"] = {
            key: record.get(key)
            for key in (
                "gateId", "taskId", "verdict", "decisionId", "resultingStatus",
                "approver", "approvedBy", "approvedAt", "reviewedAt",
                "candidateRevision", "productionAuthority", "note", "_source",
            )
            if record.get(key) is not None
        }
        item["statusSource"] = record["_source"]

        verdict = str(record.get("verdict", "")).lower()
        if verdict in OPEN_VERDICTS or (verdict not in APPROVED_VERDICTS and not record.get("decisionId")):
            item["status"] = "candidate"
            queue_items.append(item)
        elif verdict in APPROVED_VERDICTS:
            claimed = item.get("status")
            resolved = "canonical" if record.get("productionAuthority") or str(
                record.get("resultingStatus", "")).startswith("canonical") else "non-production"
            item["status"] = resolved
            if claimed and claimed != resolved:
                drift.append({"id": item["id"], "reason": f"overlay said {claimed}, records resolve to {resolved}"})
            decision_id = record.get("decisionId")
            if decision_id and decision_id in central and central[decision_id].get("status") != "approved":
                drift.append({"id": item["id"], "reason": f"{decision_id} is {central[decision_id].get('status')} in the central register"})
        return item

    zones_out = []
    for zone in overlay["zones"]:
        if zone["id"] == "review":
            continue  # rebuilt from disk below
        zone = dict(zone)
        zone["groups"] = [
            {**group, "items": [resolve(item) for item in group.get("items", [])]}
            for group in zone.get("groups", [])
        ]
        zones_out.append(zone)

    # Records on disk whose owner has no overlay entry anywhere: surface them.
    # Overlay review-zone metadata enriches what the scan finds; the scan, not
    # the overlay, decides whether something is actually open.
    for owner, records in sorted(by_owner.items()):
        if owner in known_ids:
            continue
        record = best_record(records) or {}
        verdict = str(record.get("verdict", "")).lower()
        is_open = verdict in OPEN_VERDICTS or (verdict not in APPROVED_VERDICTS and not record.get("decisionId"))
        meta = review_meta.get(owner, {})
        item = {
            "id": owner,
            "name": meta.get("name", owner.replace("-", " ").title()),
            "status": "candidate" if is_open else "canonical",
            "summary": meta.get(
                "summary",
                "Found on disk by the registry scan. Add this item to registry.source.json for a proper name, link and summary.",
            ),
            "record": {k: record.get(k) for k in ("gateId", "taskId", "verdict", "decisionId", "approver", "approvedBy", "approvedAt", "reviewedAt", "note", "_source") if record.get(k)},
            "statusSource": record.get("_source", "scan"),
        }
        for key in ("href", "secondary", "gateId", "flag", "panel"):
            if key in meta:
                item[key] = meta[key]
        if owner not in review_meta:
            item["flag"] = "Auto-discovered: no overlay entry exists for this record."
        if is_open:
            queue_items.append(item)
        else:
            # Was in review (or unknown) and is now decided: keep it visible
            # until the overlay gives it a permanent home.
            item["flag"] = item.get("flag") or "Decided. Move this item into its permanent zone in registry.source.json."
            decided_items.append(item)

    groups = [{"id": "queue", "label": "Queue", "items": queue_items}]
    if decided_items:
        groups.append({"id": "decided", "label": "Recently decided", "items": decided_items})
    review_zone = {
        "id": "review",
        "label": "Review",
        "hint": "Built, and waiting on a human decision. Assembled automatically from disk records.",
        "groups": groups,
    }
    zones_out.insert(0, review_zone)

    out = {
        "schemaVersion": "0.3.0",
        "generated": True,
        "generatedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "generator": "brand-kit/app/build_registry.py",
        "recordsScanned": sum(len(v) for v in by_owner.values()),
        "system": overlay["system"],
        "statuses": overlay["statuses"],
        "drift": drift,
        "zones": zones_out,
    }

    (APP / "registry.json").write_text(json.dumps(out, indent=2) + "\n")
    print(f"registry.json written: {out['recordsScanned']} records, "
          f"{len(queue_items)} in review, {len(drift)} drift note(s)")
    for note in drift:
        print(f"  drift: {note['id']} — {note['reason']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
