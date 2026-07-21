# Phase 2 capture results

Status: complete  
Capture date: 20 July 2026  
Tool: Taste Reverse `0.2.0`  
Scope: public unauthenticated surfaces only

## Qualified runs

| Source | Page categories | Viewport observations | PNG captures | Element samples | Validation | Sanitised measurements |
| --- | ---: | ---: | ---: | ---: | --- | ---: |
| Notion | 5 | 15 | 63 | 5,473 | PASS 100/100 | 149 |
| Linear | 5 | 15 | 24 | 5,144 | PASS 100/100 | 152 |
| ElevenLabs | 5 | 15 | 25 | 5,697 | PASS 100/100 | 167 |
| Stripe | 5 | 15 | 46 | 6,239 | PASS 100/100 | 157 |
| Ramp | 5 | 15 | 59 | 3,354 | PASS 100/100 | 111 |
| Total | 25 source pages | 75 | 217 | 25,907 | All qualified runs pass | 736 |

Every source includes desktop, laptop, and mobile evidence. Safe public menu states and focused section captures were added where supported. Raw screenshots, element evidence, and source packages remain inside Taste Reverse and are prohibited from Mez distribution.

## Raw evidence locations

- Notion: `/Users/olivermerrick/Documents/taste-reverse/runs/mez-phase2-notion-20260720-r2/2026-07-19T221009732Z`
- Linear: `/Users/olivermerrick/Documents/taste-reverse/runs/mez-phase2-linear-20260720/2026-07-19T215943970Z`
- ElevenLabs: `/Users/olivermerrick/Documents/taste-reverse/runs/mez-phase2-elevenlabs-20260720/2026-07-19T215943970Z`
- Stripe: `/Users/olivermerrick/Documents/taste-reverse/runs/mez-phase2-stripe-20260720/2026-07-19T220951885Z`
- Ramp: `/Users/olivermerrick/Documents/taste-reverse/runs/mez-phase2-ramp-20260720/2026-07-19T221328262Z`

These paths are internal provenance pointers, not portable dependencies. Each qualified run has its own deterministic package validation and source fingerprint.

## Sanitised export locations

- `/Users/olivermerrick/Documents/taste-reverse/exports/mez-systems/phase-2/notion`
- `/Users/olivermerrick/Documents/taste-reverse/exports/mez-systems/phase-2/linear`
- `/Users/olivermerrick/Documents/taste-reverse/exports/mez-systems/phase-2/elevenlabs`
- `/Users/olivermerrick/Documents/taste-reverse/exports/mez-systems/phase-2/stripe`
- `/Users/olivermerrick/Documents/taste-reverse/exports/mez-systems/phase-2/ramp`

All five copied exports pass `taste-reverse validate-export`. Each contains only `manifest.json`, `findings.json`, and `README.md`, with checksums. The exports contain 736 deterministic measurements and zero interpreted findings because manual analysis is intentionally not presented as automatic pipeline output.

## Preserved failed and incomplete attempts

- The first Notion run scored 90/100 because the collector stored a public input `aria-label` in `textSample`. The collector now redacts text from inputs, selects, and textareas while retaining the strict evaluator privacy gate. A regression fixture verifies form-control redaction and labelled non-form text retention. The full R2 run passes 100/100.
- An earlier Notion R2 attempt passed privacy but ended during temporary network timeouts. It is not the qualified run.
- The first Ramp homepage seed found only one category and scored 90/100. Re-seeding from the official products surface exposed a representative five-category set and passes 100/100.

Failed and incomplete runs remain immutable historical evidence. They are excluded from synthesis counts and exports.

## Limits

- No authenticated product, private design library, advertising account, customer data, or internal analytics was accessed.
- Public marketing and screenshots are curated evidence, not proof of complete product behaviour.
- Motion semantics were studied, but timing, easing, hover systems, and reduced-motion behaviour were not comprehensively measured.
- Source values and screenshots remain research-only. They cannot become Mez tokens, assets, or production examples.
