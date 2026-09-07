#!/usr/bin/env python3
"""Create a reviewable local candidate from a recipe or an original image."""
import argparse
import base64
import json
from pathlib import Path
import sys
import uuid

import engine


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--recipe', type=Path, help='Exported mesh-source-1 recipe JSON')
    source.add_argument('--source', type=Path, help='Original square PNG/JPEG, 512–4096px')
    parser.add_argument('--name', required=True, help='Working candidate name')
    parser.add_argument('--parent', help='Optional saved draft slug to refine')
    parser.add_argument('--request-id', default=None, help='Reuse a UUID to retry the same save')
    args = parser.parse_args()
    try:
        payload = {'name': args.name, 'requestId': args.request_id or str(uuid.uuid4()), 'parentSlug': args.parent}
        if args.recipe:
            payload.update(mode='compose', recipe=json.loads(args.recipe.read_text()))
        else:
            if args.source.stat().st_size > engine.MAX_IMAGE_BYTES:
                raise ValueError('Upload a PNG or JPEG under 12 MB.')
            payload.update(mode='upload', filename=args.source.name, imageBase64=base64.b64encode(args.source.read_bytes()).decode())
        result = engine.save(payload)
        print(json.dumps({'candidateId': result['candidateId'], 'path': str(engine.WORKSPACE / result['slug']), 'status': result['status'], 'productionAuthority': False}, indent=2))
        return 0
    except (ValueError, OSError) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
