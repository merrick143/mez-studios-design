# Foundation release migration boundary

## What this release changes

The canonical release provides one copyable directory and one CSS entrypoint for the four already approved foundations. It does not change any canonical token, font, colour, spacing value, responsive profile, radius, depth rule or control contract.

## What it does not change

- No production consumer is migrated by this task.
- No product-expression or homepage component is introduced.
- No Figma file becomes authoritative.
- No gradient or Living Core asset is bundled.
- The immutable migration identity release `0.1.0-alpha.1` remains separate and unchanged.

## Future consumer migration

After the release gate is approved, migrate one named consumer at a time. Copy the complete `dist/` directory, load `index.css`, remove overlapping local foundation declarations only after visual and accessibility comparison, and record a consumer-specific receipt. Never infer that approval of this package authorises an unreviewed consumer rollout.
