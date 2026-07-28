# Fixture media provenance

**These are real people, and they consented. Read this before adding anyone new.**

| File | Subject | Source | Prepared |
|---|---|---|---|
| `portrait-a.mp4` | Kayvon Jafarzadeh, `@kayvon.ai` | Public Instagram reel, post `DYq3RqJKaYJ` | Matted and cropped, 640x640, 5s, muted |
| `portrait-b.mp4` | Antonije Mirkovic, `@mirkovicdev` | Public Instagram reel, post `DZ4ygSGhWPv` | Matted and cropped, 640x640, 5s, muted |

Both appear on the mez.systems AI OS testimonial marquee and gave written
testimonials for the product.

## Consent: given

Confirmed by Olli on 2026-07-27. Both subjects are people he knows personally,
they gave testimonials for the product, and they agreed to appear. Their faces
already run on the public mez.systems AI OS marquee.

That is the record. Do not re-open it in review, and do not add a caveat to a
surface that uses these clips.

Adding a **new** subject is a different question: a face may only enter this
folder once Olli confirms that person agreed, and the table above must be
extended in the same commit.

## How they were prepared

Produced by `pipeline/matte_clips.py` in the originating repository
(`mezcorp_claude_code/departments/design/projects/testimonial-slider`).

For each frame: MediaPipe selfie segmentation produces a person mask, the mask
edge is feathered by five pixels so the silhouette does not stair-step once
halftoned, and the subject is composited over solid white.

The white plate is what lets the component carry no machine learning. A light
plate maps to no dots under a luminance halftone, so a matted source renders
identically to live segmentation while costing nothing at runtime. Zero frames
failed segmentation across the seven clips processed.

## What the component may assume

Only that the media is a square, muted, looping video it was explicitly given.
It never fetches media on its own, never asserts who the subject is, and never
implies consent exists.
