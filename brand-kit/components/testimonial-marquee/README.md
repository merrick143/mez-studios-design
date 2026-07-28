# TASK-CMP-06 · Testimonial Marquee

**Status: canonical 1.0.0 under `DEC-TESTIMONIAL-MARQUEE-COMPONENT-001`. No release package is built.**

A wide, shallow, continuously moving proof rail composed on CMP-05 Halftone
Portrait. Round 03 contains seven video-backed testimonials, fixture-owned
Instagram evidence, local curated profile images and five deliberately minimal
presentations. None establishes the final testimonial-card anatomy.

## Usage

```html
<link rel="stylesheet"
  href="brand-kit/components/testimonial-marquee/mez-testimonial-marquee.css" />

<mez-testimonial-marquee
  src="brand-kit/components/testimonial-marquee/fixtures/ai-os-testimonials.json"
  label="Operator testimonials for the AI OS"
  presentation="social-caption"
></mez-testimonial-marquee>

<script type="module"
  src="brand-kit/components/testimonial-marquee/mez-testimonial-marquee.js"></script>
```

Presentations: `profile-strip`, `portrait-window`, `social-caption`,
`quote-first` and `proof-ledger`. Olli selected and locked `social-caption` on
2026-07-28. The other four remain comparison evidence, not approved variants.

Open `fixtures/static-html.html` for the dependency-free proof,
`fixtures/react.jsx` for the thin React adapter, or
`workbench/components/testimonial-marquee/` for all five instrumented versions.

## The motion exception

The track does drift. Continuous carousel movement is autoplay under Website
Motion 1.0.0, so this canonical component carries a bounded exception rather
than claiming baseline compliance.

Olli explicitly requested auto-scroll on 2026-07-28. The bounded CMP-06
exception is recorded in `round-03-feedback.json` and the source contract. It is
limited to this component and requires:

- phase-level pause while the testimonial viewport is hovered or focused;
- a 900ms trailing pause after the last wheel, pointer or keyboard gesture;
- no track movement while the document or component is offscreen;
- native wheel, trackpad, touch and pointer scrolling without cancellation;
- one complete static source-ordered set under reduced motion.

The element advances native `scrollLeft` at 24 CSS pixels per second with
`requestAnimationFrame`. An `aria-hidden` and unfocusable duplicate closes the
visual loop. The verifier asserts this implementation and every safeguard
against the JavaScript, rather than trusting the JSON claim.

Every portrait separately sets `motion-policy="always"` and retains the exact
CMP-05 treatment locked on 2026-07-27. CMP-05 owns its own recorded exception
and idles each clipped or page-offscreen portrait.

## Seven video-backed testimonials

Daniel Leung is absent from Round 03 at Olli's direction because there is no
approved video image. The fixture now deliberately requires a portrait for
every record. CMP-06 does not manufacture a monogram, placeholder or apology
state.

## Instagram proof

The fixture supplies a local curated profile image, Instagram handle, verified
state, follower snapshot and evidence note for every testimonial. The component
renders Name, Username and Followers as a compact vertical profile structure.
It renders no outbound Instagram link, makes no Instagram API request and does
not own, infer or refresh those facts. The approved policy keeps follower
figures as dated frozen evidence and never represents them as live.

## Reduced motion

Under `prefers-reduced-motion` and `?static`:

- the duplicate track is not rendered;
- the viewport stops being horizontally scrollable;
- the primary track recomposes into a complete vertical list in source order;
- no visible carousel controls are introduced;
- all seven testimonials remain readable;
- CMP-05 paints each portrait once and starts no video render loop.

## Content contract

```json
{
  "testimonials": [
    {
      "id": "stable-id",
      "quote": "Real supplied quote",
      "name": "Real name",
      "handle": "@real-handle",
      "portrait": {
        "src": "./media/prepared-clip.mp4",
        "label": "Halftone portrait of the speaker"
      },
      "social": {
        "platform": "Instagram",
        "followers": "472K followers",
        "verified": true,
        "profileImage": "./media/example-profile.png",
        "evidence": "Fixture-owned source note"
      }
    }
  ]
}
```

All fields are required. Media paths resolve relative to the same-origin
fixture URL, not the page.

## Events

| Event | Detail |
|---|---|
| `mez-testimonial-ready` | `count`, `portraits`, `socialProfiles`, `verified`, `motionMode`, `presentation` |
| `mez-testimonial-change` | `index`, `id`, `source` |
| `mez-testimonial-interaction` | `source` |
| `mez-testimonial-motion-change` | `state` |
| `mez-testimonial-failure` | `reason` |

## Ownership boundary

CMP-06 owns the viewport, paired tracks, bounded movement, phase interaction,
keyboard and screen-reader behaviour, responsive recomposition and the selected
minimal presentation. It does not own the halftone renderer, testimonial or
Instagram facts, media, product identity, consent, live social fetching, final
testimonial-card anatomy or page composition.

## Verify

```bash
.venv/bin/python brand-kit/components/testimonial-marquee/verify_testimonial_marquee_contract.py
```

Mechanical checks are not design checks. Gate B is recorded separately after
the five rendered workbench versions are inspected across every declared
viewport.

## Selected candidate lock

Olli selected and provisionally locked the `social-caption` candidate at
`H-CMP-06-TESTIMONIAL-MARQUEE-PROOF`. Canonical promotion still requires a
governance decision ID; this package has no production authority.
