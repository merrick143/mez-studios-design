# Testimonial Marquee fixture media provenance

These seven files are exact copies of the matted clips prepared for the
originating testimonial-slider workbench. They are not reprocessed by CMP-06.

| File | Subject | Handle | Origin |
|---|---|---|---|
| `kayvon-ai-matte.mp4` | Kayvon Jafarzadeh | `@kayvon.ai` | `pipeline/matted/kayvon-ai-matte.mp4` |
| `koen-salo-matte.mp4` | Koen Salo | `@koen_salo` | `pipeline/matted/koen_salo-matte.mp4` |
| `omarontape-matte.mp4` | Omar Zeineddine | `@omarontape` | `pipeline/matted/omarontape-matte.mp4` |
| `tandalebobby-matte.mp4` | Bobby | `@tandalebobby` | `pipeline/matted/tandalebobby-matte.mp4` |
| `joaomore-ai-matte.mp4` | João Moreira | `@joaomore.ai` | `pipeline/matted/joaomore-ai-matte.mp4` |
| `mirkovicdev-matte.mp4` | Antonije Mirkovic | `@mirkovicdev` | `pipeline/matted/mirkovicdev-matte.mp4` |
| `speedy-devv-matte.mp4` | Hugues | `@speedy_devv` | `pipeline/matted/speedy_devv-matte.mp4` |

The seven matching `*-profile.png` files are 280px square crops of the curated
Mez testimonial-marquee profile images recorded as `referenceUrl` values in
`pipeline/accounts.json`. Those images were already the identity authority used
to verify the portrait footage. CMP-06 stores the crops locally and never loads
them from Supabase or Instagram at runtime.

Origin root:
`mezcorp_claude_code/departments/design/projects/testimonial-slider/`.

## Consent

Given. Olli confirmed on 2026-07-27 that the subjects are people he knows, they
agreed to appear, and their faces already run on the public site. CMP-05 records
the same confirmation in its media provenance.

## Preparation

Each source was cropped square, muted, shortened and composited over a flat
white plate before entering the browser. CMP-05 maps that white plate to no dots
with a luminance halftone. No segmentation model or network fetch runs in
CMP-06.

Daniel Leung is intentionally absent. No clean footage exists and no new clip
will be manufactured. Olli directed on 2026-07-28 that his testimonial be
removed from this video-backed fixture rather than represented without media.

## Instagram snapshot

The fixture adds account metadata as display evidence, not as a live social
integration. Public profiles were checked on 2026-07-28 for Kayvon, Antonije,
Omar, Hugues and Koen. Instagram presented a login wall for Bobby and João, so
their follower figures remain attributed to the originating testimonial-slider
fixture. Olli explicitly directed that every included subject display as
verified. CMP-06 does not fetch Instagram and does not promise that follower
counts stay current.
