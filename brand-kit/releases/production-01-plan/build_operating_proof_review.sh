#!/bin/zsh
set -euo pipefail

script_dir=${0:A:h}
brand_kit=${script_dir:h:h}
source_dir="$brand_kit/workbench/golden/homepage/assets/operating-proof"
review_dir="$script_dir/operating-proof-review"
asset_dir="$review_dir/assets/operating-proof/redacted"
font_path="$brand_kit/releases/foundations/dist/packages/typography/fonts/ibm-plex-mono/IBMPlexMono-Regular.ttf"

mkdir -p "$asset_dir"

# Every derivative removes the 46px Notion chrome containing workspace
# breadcrumbs, avatars and sharing controls. Command additionally masks the
# personal page title and all internal link/task/content labels. Backend keeps
# only the public structural headings and masks internal destinations.
ffmpeg -y -hide_banner -loglevel error \
  -i "$source_dir/command.png" \
  -vf "crop=iw:ih-46:0:46,drawbox=x=92:y=350:w=920:h=88:color=0xf8f8f8:t=fill,drawtext=fontfile='$font_path':text='PRIVATE COMMAND TITLE REDACTED':fontcolor=0x666662:fontsize=22:x=120:y=382,drawbox=x=92:y=595:w=370:h=405:color=0xf8f8f8:t=fill,drawtext=fontfile='$font_path':text='PRIVATE LINKS REDACTED':fontcolor=0x8a8a84:fontsize=18:x=120:y=645,drawbox=x=470:y=595:w=980:h=405:color=0xf8f8f8:t=fill,drawtext=fontfile='$font_path':text='PRIVATE TASK DATA REDACTED':fontcolor=0x8a8a84:fontsize=18:x=500:y=645,drawbox=x=1455:y=595:w=385:h=405:color=0xf8f8f8:t=fill,drawtext=fontfile='$font_path':text='PRIVATE CONTENT REDACTED':fontcolor=0x8a8a84:fontsize=18:x=1480:y=645" \
  -frames:v 1 "$asset_dir/command.png"

ffmpeg -y -hide_banner -loglevel error \
  -i "$source_dir/backend.png" \
  -vf "crop=iw:ih-46:0:46,drawbox=x=118:y=520:w=485:h=105:color=0xf8f8f8:t=fill,drawtext=fontfile='$font_path':text='INTERNAL DESTINATIONS REDACTED':fontcolor=0x8a8a84:fontsize=17:x=135:y=555,drawbox=x=708:y=520:w=485:h=105:color=0xf8f8f8:t=fill,drawtext=fontfile='$font_path':text='INTERNAL DESTINATIONS REDACTED':fontcolor=0x8a8a84:fontsize=17:x=725:y=555,drawbox=x=1292:y=520:w=485:h=105:color=0xf8f8f8:t=fill,drawtext=fontfile='$font_path':text='INTERNAL DESTINATIONS REDACTED':fontcolor=0x8a8a84:fontsize=17:x=1309:y=555,drawbox=x=118:y=805:w=760:h=194:color=0xf8f8f8:t=fill,drawtext=fontfile='$font_path':text='INTERNAL KNOWLEDGE LINKS REDACTED':fontcolor=0x8a8a84:fontsize=17:x=135:y=850" \
  -frames:v 1 "$asset_dir/backend.png"

ffmpeg -y -hide_banner -loglevel error \
  -i "$source_dir/docs.png" \
  -vf "crop=iw:ih-46:0:46" \
  -frames:v 1 "$asset_dir/docs.png"

ffmpeg -y -hide_banner -loglevel error \
  -i "$source_dir/ad-system.png" \
  -vf "crop=iw:ih-46:0:46" \
  -frames:v 1 "$asset_dir/ad-system.png"

ffmpeg -y -hide_banner -loglevel error \
  -i "$asset_dir/command.png" \
  -i "$asset_dir/backend.png" \
  -i "$asset_dir/docs.png" \
  -i "$asset_dir/ad-system.png" \
  -filter_complex "[0:v]scale=930:500:force_original_aspect_ratio=decrease,pad=960:520:15:10:0xf8f8f8[a];[1:v]scale=930:500:force_original_aspect_ratio=decrease,pad=960:520:15:10:0xf8f8f8[b];[2:v]scale=930:500:force_original_aspect_ratio=decrease,pad=960:520:15:10:0xf8f8f8[c];[3:v]scale=930:500:force_original_aspect_ratio=decrease,pad=960:520:15:10:0xf8f8f8[d];[a][b][c][d]xstack=inputs=4:layout=0_0|960_0|0_520|960_520:fill=0xf8f8f8[out]" \
  -map "[out]" -frames:v 1 "$review_dir/contact-sheet.png"

command_hash=$(shasum -a 256 "$asset_dir/command.png" | awk '{print $1}')
backend_hash=$(shasum -a 256 "$asset_dir/backend.png" | awk '{print $1}')
docs_hash=$(shasum -a 256 "$asset_dir/docs.png" | awk '{print $1}')
ad_hash=$(shasum -a 256 "$asset_dir/ad-system.png" | awk '{print $1}')

jq -n \
  --arg command_hash "$command_hash" \
  --arg backend_hash "$backend_hash" \
  --arg docs_hash "$docs_hash" \
  --arg ad_hash "$ad_hash" \
  '{
    schemaVersion:"1.0.0",
    payloadId:"mz.systems.operating-proof.production-01",
    status:"redacted-awaiting-review",
    publicReleaseEligible:false,
    sourceProvenance:{
      repositoryRecord:"brand-kit/workbench/golden/homepage/assets/operating-proof/provenance.json",
      originalPathsIncluded:false,
      originalBytesIncluded:false
    },
    records:[
      {
        id:"proof-command",
        role:"command",
        originalSha256:"97f576860ab1151ef1379ed1bfcf7e44ccd7da5c7376e773f3091eb6326c6f59",
        redactedAsset:"assets/operating-proof/redacted/command.png",
        redactedSha256:$command_hash,
        alt:"Redacted Mez Studios command surface showing the branded operating shell and private working regions concealed.",
        redactionMethods:["cropped Notion workspace chrome", "opaque masks over personal title and internal links, tasks and content labels"],
        publicReleaseEligible:false
      },
      {
        id:"proof-context-backbone",
        role:"context-backbone",
        originalSha256:"6e34b55413ed333ab7230227e705a6bb4642f0b5e61ef6bb47fbf76467f14e73",
        redactedAsset:"assets/operating-proof/redacted/backend.png",
        redactedSha256:$backend_hash,
        alt:"Redacted Mez Backend surface showing Growth, Client, Content and Knowledge OS structure without internal destinations.",
        redactionMethods:["cropped Notion workspace chrome", "opaque masks over internal destination names and descriptions"],
        publicReleaseEligible:false
      },
      {
        id:"proof-structured-documentation",
        role:"structured-documentation",
        originalSha256:"069b7d76fe274801c6e3208b8f28c2277536854b872b050c0d01272a8b4e70d8",
        redactedAsset:"assets/operating-proof/redacted/docs.png",
        redactedSha256:$docs_hash,
        alt:"Mez Studios Docs surface grouped into Brief, Context, README, Reference, Strategy and Technical.",
        redactionMethods:["cropped Notion workspace chrome containing breadcrumb, avatar and sharing controls"],
        publicReleaseEligible:false
      },
      {
        id:"proof-working-application",
        role:"working-application",
        originalSha256:"af217f1949122469004055050389da7a10169a267dc2de057cd4fde2ef2937e8",
        redactedAsset:"assets/operating-proof/redacted/ad-system.png",
        redactedSha256:$ad_hash,
        alt:"Ultimate AI Ad System surface showing onboarding, playbook, strategy, AI and weekly operating views.",
        redactionMethods:["cropped Notion workspace chrome containing breadcrumb, avatar and sharing controls"],
        publicReleaseEligible:false
      }
    ],
    review:null
  }' > "$review_dir/payload.json"

echo "MEZ OPERATING PROOF REVIEW: BUILT"
echo "- four source hashes preserved"
echo "- four deterministic redacted derivatives generated"
echo "- publicReleaseEligible remains false pending exact-byte Olli review"
