# TR-5 controlled taste calibration

Status: invalidated and replaced on 20 July 2026. This interface is disabled. The preserved evidence and rationale live in `invalid-pilot/`. The active review is `/Users/olivermerrick/Documents/taste-reverse/reviews/mez-systems-reference-taste-round-01/`.

This folder is the human review instrument for Phase 2, round one. It presents 12 original Mez A/B pairs across the eight unapproved taste dimensions. Every pair keeps its copy and content constant and changes one named variable where possible.

Nothing in this folder has production authority. The interface writes only to browser local storage until the reviewer exports a record. An exported record is evidence for synthesis, not approval of a token, component, or visual direction.

## Run it locally

From the Mez Systems pack root:

```bash
python3 -m http.server 8906
```

Then open:

`http://127.0.0.1:8906/research/phase-2/calibration/`

Do not open `index.html` directly from Finder. Browsers block local JSON loading under `file://`.

## Human review contract

1. Budget 30 to 45 minutes.
2. View both options before selecting.
3. Answer A, B, or neither. Do not try to approve both.
4. Add confidence only when useful. Low confidence and neither are automatically flagged for escalation.
5. Add a short note when a specific behaviour drove the decision.
6. Reveal the research notes after deciding to reduce framing bias.
7. Export the final JSON record and return it to the Mez design-system owner.

Keyboard shortcuts: `A`, `B`, `N`, left arrow, and right arrow.

## Files

- `specs/pairs-01-04.json`, `pairs-05-08.json`, `pairs-09-12.json`: controlled experiment contracts
- `index.html`, `calibration.css`, `calibration.js`: standalone review interface
- `preference-log.schema.json`: portable response contract
- `HUMAN-REVIEW-PACKET.md`: concise reviewer briefing and stop gate

## Privacy and recovery

The interface sends no data to a server. Decisions are stored under `mez-tr5-calibration-round-01` in local storage. Clearing site data clears the saved state. Export before clearing the browser or changing devices.

## Next gate

After one complete human record is returned:

1. validate it against `preference-log.schema.json`
2. convert records to `preference-log.jsonl`
3. isolate low-confidence, neither, and contradictory results
4. produce `HUMAN-TASTE-PROFILE.md` and the uncertainty list
5. ask only the unresolved questions
6. proceed to TR-6 only after the taste profile is explicitly reviewed
