#!/usr/bin/env python3
"""Verify the canonical CMP-06 Testimonial Marquee contract.

Round 03 intentionally autoscrolls under a recorded bounded exception. The
high-risk checks therefore inspect the JavaScript for both the drift mechanism
and every promised stop condition, rather than accepting JSON claims alone.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

try:
    import jsonschema
except ImportError:  # pragma: no cover
    print("jsonschema is required: use the pinned environment in brand-kit/START-HERE.md")
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parent
BRAND_KIT = ROOT.parents[1]
WORKBENCH = BRAND_KIT / "workbench" / "components" / "testimonial-marquee"
HOMEPAGE = BRAND_KIT / "workbench" / "golden" / "homepage"
DECISIONS = BRAND_KIT / "governance" / "post-cutover-decisions.json"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []
    source = read_json(ROOT / "testimonial-marquee.source.json")
    schema = read_json(ROOT / "testimonial-marquee.schema.json")
    review = read_json(ROOT / "review.json")
    fixture = read_json(ROOT / "fixtures" / "ai-os-testimonials.json")
    approval_record = read_json(ROOT / "approval.json")
    decisions = read_json(DECISIONS)

    try:
        jsonschema.Draft202012Validator(schema).validate(source)
    except jsonschema.ValidationError as error:
        failures.append(f"source does not satisfy its schema: {error.message}")

    decision_id = "DEC-TESTIMONIAL-MARQUEE-COMPONENT-001"
    if source.get("status") != "canonical" or source.get("productionAuthority") is not True:
        failures.append("canonical authority is missing from the source contract")
    if source.get("decisionIds") != [decision_id] or source.get("approval", {}).get("state") != "canonical":
        failures.append("source does not cite the exact canonical promotion decision")
    if review.get("verdict") != "approved" or review.get("productionAuthority") is not True:
        failures.append("review does not record the approved canonical promotion")
    if review.get("decisionId") != decision_id:
        failures.append("review cites the wrong promotion decision")
    if approval_record.get("decisionId") != decision_id or approval_record.get("candidateRevision") != source.get("candidateRevision"):
        failures.append("approval record does not promote the exact candidate revision")
    indexed = {item.get("id"): item for item in decisions.get("decisions", [])}
    if indexed.get(decision_id, {}).get("source") != "brand-kit/components/testimonial-marquee/approval.json":
        failures.append("promotion decision is absent from the post-cutover governance supplement")
    for key in ("componentId", "gateId", "taskId", "candidateRevision"):
        if source.get(key) != review.get(key):
            failures.append(f"{key} disagrees between source and review")

    required = [
        "README.md", "mez-testimonial-marquee.js", "mez-testimonial-marquee.css",
        "testimonial-marquee.source.json", "testimonial-marquee.schema.json", "review.json", "approval.json",
        "gate-b.json", "round-02-feedback.json", "round-02-gate-b.json",
        "round-03-feedback.json", "round-03-gate-b.json",
        "round-04-feedback.json", "round-04-lock.json", "round-04-gate-b.json",
        "fixtures/static-html.html", "fixtures/react.jsx", "fixtures/ai-os-testimonials.json",
        "fixtures/media/PROVENANCE.md",
    ]
    for relative in required:
        if not ROOT.joinpath(relative).is_file():
            failures.append(f"missing {relative}")
    for relative in ("index.html", "styles.css", "testimonial-marquee-workbench.js"):
        if not WORKBENCH.joinpath(relative).is_file():
            failures.append(f"missing workbench/{relative}")

    gate_path = ROOT / "round-04-gate-b.json"
    if gate_path.is_file():
        gate_b = read_json(gate_path)
        if gate_b.get("productionAuthority") is not False:
            failures.append("Round 04 Gate B record claims authority")
        if review.get("gateB", {}).get("record") != "brand-kit/components/testimonial-marquee/round-04-gate-b.json":
            failures.append("review does not resolve the Round 04 Gate B record")

    js = (ROOT / "mez-testimonial-marquee.js").read_text(encoding="utf-8")
    css = (ROOT / "mez-testimonial-marquee.css").read_text(encoding="utf-8")
    workbench_html = (WORKBENCH / "index.html").read_text(encoding="utf-8")
    workbench_js = (WORKBENCH / "testimonial-marquee-workbench.js").read_text(encoding="utf-8")

    motion = source.get("motion", {})
    exception = source.get("motionDecisionException", {})
    if motion.get("trackPolicy") != "continuous-auto-scroll-bounded-exception":
        failures.append("track policy does not name the bounded autoplay exception")
    if motion.get("autoplay") is not True or motion.get("continuousDrift") is not True:
        failures.append("source contract quietly denies implemented autoplay or drift")
    if motion.get("scrollHijacking") is not False:
        failures.append("source contract permits scroll hijacking")
    if motion.get("speedPxPerSecond") != 24 or motion.get("interactionPauseMilliseconds") != 900:
        failures.append("source and implementation speed or interaction pause are unpinned")
    if exception.get("approvedBy") != "Olli" or exception.get("approvedAt") != "2026-07-28":
        failures.append("bounded drift exception lacks Olli attribution")
    approval = source.get("approval", {})
    if approval.get("approvedPresentation") != "social-caption" or source.get("presentations", {}).get("selected") != "social-caption":
        failures.append("Round 04 does not lock the selected social-caption presentation")
    if approval.get("decisionId") != decision_id or approval.get("followerPolicy") != "frozen-evidence":
        failures.append("canonical approval or frozen follower policy is missing")

    # Prove actual drift and every stop condition in source.
    for needle, why in (
        ("const AUTO_SPEED_PX_PER_SECOND = 24", "24px/s drift speed is not implemented"),
        ("const INTERACTION_PAUSE_MS = 900", "interaction pause duration is not implemented"),
        ("requestAnimationFrame", "autoscroll has no frame loop"),
        ("cancelAnimationFrame", "frame loop cannot be stopped"),
        ("this.autoOffset +=", "frame loop has no fractional movement accumulator"),
        ("this.viewport.scrollLeft = this.autoOffset", "frame loop does not move the native viewport"),
        ('data-copy="clone" aria-hidden="true"', "seam clone is not hidden from assistive technology"),
        ("this.autoOffset -= this.cycleWidth", "continuous loop has no cycle reset"),
        ("IntersectionObserver", "offscreen track pause is not implemented"),
        ('document.visibilityState === "visible"', "hidden-document pause is not implemented"),
        ("!this.pointerActive", "active-pointer pause is not enforced"),
        ("!this.hoverPaused", "hover pause is not enforced"),
        ("!this.focusPaused", "focus pause is not enforced"),
        ("now >= this.interactionPauseUntil", "direct-interaction pause is not enforced"),
        ('this.viewport.addEventListener("pointerenter"', "hover pause is not owned by the testimonial phase"),
        ('this.viewport.addEventListener("focusin"', "focus pause is not owned by the testimonial phase"),
        ('{ passive: true }', "wheel or pointer listener is not explicitly passive"),
        ('this.dataset.motionMode = forceStatic ? "static-complete" : "auto-scroll"', "static and autoplay modes are not explicit"),
    ):
        if needle not in js:
            failures.append(why)
    if "setInterval(" in js or "setTimeout(" in js:
        failures.append("component uses an uncontracted timer for track motion")
    if 'addEventListener("scroll"' in js:
        failures.append("component drives behaviour from a scroll listener")
    if js.count("preventDefault()") != 1 or "handleKeyDown(event)" not in js:
        failures.append("input cancellation is not limited to focused keyboard navigation")

    css_without_comments = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    for pattern, why in (
        (r"@keyframes", "CSS keyframes create a second motion system"),
        (r"\banimation\s*:", "CSS animation creates a second motion system"),
        (r"backdrop-filter", "MAT-01 glass is prohibited"),
        (r"box-shadow", "boxed or ambient testimonial shadow is prohibited"),
        (r"#000000|#0a0a0a", "COL-05 pure or near black is prohibited"),
    ):
        if re.search(pattern, css_without_comments, flags=re.I):
            failures.append(why)

    for needle, why in (
        ('tabindex="0"', "viewport is not keyboard focusable"),
        ('aria-live="polite"', "motion or selection changes are not announced"),
        ("ArrowLeft", "ArrowLeft is not implemented"),
        ("ArrowRight", "ArrowRight is not implemented"),
        ('event.key === "Home"', "Home is not implemented"),
        ('event.key === "End"', "End is not implemented"),
        ("scrollIntoView", "explicit navigation does not move to a testimonial"),
        ("<blockquote>", "quote semantics are absent"),
        ("<figcaption", "attribution semantics are absent"),
        ('class="mz-testimonial-marquee__profile-image"', "local profile image is not rendered"),
        ('class="mz-testimonial-marquee__name"', "profile name is not rendered"),
        ('class="mz-testimonial-marquee__handle"', "profile username is not rendered"),
        ('class="mz-testimonial-marquee__followers"', "profile follower count is not rendered"),
        ('aria-label="Verified Instagram account"', "verified state has no accessible name"),
    ):
        if needle not in js:
            failures.append(why)
    if "overflow-x: auto" not in css:
        failures.append("native horizontal overflow is not implemented")
    if "data-auto-control" in js or 'data-direction="' in js or "<button" in js:
        failures.append("Round 03 still renders carousel controls")
    if "instagram.com" in js or "<a href=" in js:
        failures.append("Round 03 still renders or validates an outbound Instagram link")

    # CMP-05 composition must remain exact.
    if 'import "../halftone-portrait/mez-halftone-portrait.js"' not in js:
        failures.append("CMP-05 is not composed")
    for attribute in (
        'motion-policy="always"', 'grid-step="4"', 'max-radius="1.8"',
        'dot-colour="#212121"', 'background="#ffffff"', 'contrast="1.3"',
        'brightness="-0.03"',
    ):
        if attribute not in js:
            failures.append(f"locked CMP-05 treatment missing {attribute}")
    if "getImageData" in js or "getContext(" in js:
        failures.append("CMP-06 reimplements the halftone renderer")

    if "prefers-reduced-motion: reduce" not in css or 'data-motion-mode="static-complete"' not in css:
        failures.append("complete reduced or forced-static recomposition is absent")
    if "overflow: visible" not in css or "display: grid" not in css:
        failures.append("static-complete mode does not expose a complete list")

    testimonials = fixture.get("testimonials", [])
    if len(testimonials) != 7:
        failures.append(f"Round 03 fixture must carry 7 testimonials, found {len(testimonials)}")
    if any(item.get("id") == "daniel-leung" for item in testimonials):
        failures.append("Daniel remains in the video-backed Round 03 fixture")
    for item in testimonials:
        for field in ("id", "quote", "name", "handle", "portrait", "social"):
            if not item.get(field):
                failures.append(f"{item.get('id', 'unknown')}: missing {field}")
        portrait = item.get("portrait", {})
        relative = portrait.get("src", "")
        if not relative.startswith("./media/"):
            failures.append(f"{item.get('id')}: portrait is not fixture-local")
        elif not ROOT.joinpath("fixtures", relative.removeprefix("./")).is_file():
            failures.append(f"{item.get('id')}: portrait file is missing")
        social = item.get("social", {})
        if social.get("platform") != "Instagram" or social.get("verified") is not True:
            failures.append(f"{item.get('id')}: Instagram or verified evidence is incomplete")
        for field in ("followers", "profileImage", "evidence"):
            if not social.get(field):
                failures.append(f"{item.get('id')}: social proof has no {field}")
        profile_image = social.get("profileImage", "")
        if not profile_image.startswith("./media/"):
            failures.append(f"{item.get('id')}: profile image is not fixture-local")
        elif not ROOT.joinpath("fixtures", profile_image.removeprefix("./")).is_file():
            failures.append(f"{item.get('id')}: profile image file is missing")
        if "profileUrl" in social or "postUrl" in social:
            failures.append(f"{item.get('id')}: fixture still carries an Instagram destination")

    for presentation in source.get("presentations", {}).get("available", []):
        if f'data-presentation="{presentation}"' not in css:
            failures.append(f"CSS has no real {presentation} presentation")
        if f'presentation="{presentation}"' not in workbench_html:
            failures.append(f"workbench does not mount {presentation}")
    if workbench_html.count("<mez-testimonial-marquee") != 5:
        failures.append("workbench must show exactly five comparison versions")

    html_fixture = (ROOT / "fixtures" / "static-html.html").read_text(encoding="utf-8")
    react = (ROOT / "fixtures" / "react.jsx").read_text(encoding="utf-8")
    if "mez-testimonial-marquee" not in html_fixture or "ai-os-testimonials.json" not in html_fixture:
        failures.append("dependency-free fixture does not mount the live source")
    if "<mez-testimonial-marquee" not in react or "useEffect" not in react or "presentation" not in react:
        failures.append("React fixture is not a thin presentation-aware custom-element adapter")

    for needle in ("scrollLeft", "runningMovementSamples", "pausedMovementSamples", "offscreenLive", "data-motion", "resumeLatencyMs"):
        if needle not in workbench_js:
            failures.append(f"workbench does not measure {needle}")

    homepage_html = HOMEPAGE / "index.html"
    homepage_js = HOMEPAGE / "homepage.js"
    homepage_css = HOMEPAGE / "styles.css"
    if homepage_html.exists():
        text = homepage_html.read_text(encoding="utf-8")
        if "Consent verification pending" in text or "review-marquee__status" in text:
            failures.append("GH-S08 still renders the false consent-pending line or status dot")
        if "<mez-testimonial-marquee" not in text or "ai-os-testimonials.json" not in text:
            failures.append("GH-S08 does not compose CMP-06 with a content source")
        if 'presentation="social-caption"' not in text:
            failures.append("GH-S08 does not select the Round 03 recommended carriage")
        if "Running on Mez Systems" not in text or "Proof from the operating system." not in text:
            failures.append("GH-S08 does not carry the Round 03 approved centered copy")
        if text.count("<blockquote>") >= 3:
            failures.append("GH-S08 still owns hardcoded testimonial quotes")
    if homepage_js.exists() and "mez-testimonial-marquee.js" not in homepage_js.read_text(encoding="utf-8"):
        failures.append("Golden Homepage does not load CMP-06")
    if homepage_css.exists():
        text = homepage_css.read_text(encoding="utf-8")
        testimonial_rule = text[text.find(".testimonials {"):text.find(".testimonial-grid {")]
        if "background: transparent" not in testimonial_rule or "border-block: 0" not in testimonial_rule:
            failures.append("GH-S08 does not blend into the homepage canvas without section rules")

    if not review.get("knownGaps"):
        failures.append("approved review hides every accepted follow-up limitation")

    if failures:
        print("CMP-06 Testimonial Marquee contract FAILED")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    print("CMP-06 Testimonial Marquee contract OK")
    print(f"  status               {source['status']} {source['version']}")
    print(f"  production authority {source['productionAuthority']}")
    print(f"  track policy         {motion['trackPolicy']} at {motion['speedPxPerSecond']}px/s")
    print(f"  exception            {exception['approvedBy']} · {exception['approvedAt']}")
    print(f"  fixture              {len(testimonials)} testimonials · all video-backed · all verified")
    print(f"  presentations        {len(source['presentations']['available'])}")
    print("  reduced motion       complete static list")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
