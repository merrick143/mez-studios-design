"""Public generation, input boundaries, exact output and browser ZIP compatibility."""
import base64
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
import zipfile

from PIL import Image
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('public_maker', ROOT / 'api/gradient-maker.py')
public = importlib.util.module_from_spec(spec)
spec.loader.exec_module(public)
engine = public.engine


def recipe():
    presets = json.loads((Path(__file__).parent / 'presets.json').read_text())
    return {'version': engine.VERSION, 'seed': 7, 'softness': .45, 'flow': .35,
            'points': [{'hex': colour, 'x': xy[0], 'y': xy[1], 'weight': 1}
                       for colour, xy in zip(presets['presets'][0]['colours'], presets['positions'])]}


class PublicTests(unittest.TestCase):
    def test_hosted_extractor_dependencies_match_canonical_pins(self):
        def pins(path):
            return [line.strip() for line in path.read_text().splitlines()
                    if line.strip() and not line.lstrip().startswith('#')]
        self.assertEqual(pins(ROOT / 'requirements.txt'),
                         pins(ROOT / 'brand-kit/source-pack/living-core/requirements.txt'))

    def test_public_source_and_core_match_the_local_pipeline(self):
        payload = {'mode': 'compose', 'recipe': recipe()}
        body, content_type = public.generate(payload, 'preview')
        preview = json.loads(body)
        original = engine.build_draft(payload)
        self.assertEqual(content_type, 'application/json')
        self.assertEqual(preview['fingerprint'], original['fingerprint'])
        self.assertEqual(preview['core'], original['core'])
        self.assertNotIn('staticUrl', preview)
        self.assertLess(len(body), public.MAX_BODY)
        source = base64.b64decode(preview['sourceUrl'].split(',')[1])
        twin, kind = public.generate({'mode': 'upload', 'imageBase64': base64.b64encode(source).decode()}, 'static')
        self.assertEqual(kind, 'image/webp')
        self.assertTrue(np.array_equal(np.array(Image.open(io.BytesIO(source))), np.array(Image.open(io.BytesIO(twin)))))

    def test_oversized_image_and_malformed_payloads_are_rejected(self):
        source = engine.image_bytes(Image.new('RGB', (2048, 2048), '#ff0000'))
        with self.assertRaisesRegex(ValueError, '1024'):
            public.generate({'mode': 'upload', 'imageBase64': base64.b64encode(source).decode()}, 'preview')
        for invalid in [None, [], {'mode': 'compose', 'recipe': {}}, {'mode': 'upload', 'imageBase64': 'bad data'}]:
            with self.subTest(payload=invalid), self.assertRaises(ValueError):
                public.generate(invalid, 'preview')

    def test_uncompressible_source_fits_the_response_limit(self):
        image = Image.fromarray(np.random.default_rng(7).integers(0, 256, (1024, 1024, 3), dtype=np.uint8))
        source = engine.image_bytes(image)
        # The normalized source may exceed the 3 MB upload limit by PNG overhead,
        # but still fits as a static-twin request and as a source-only JSON reply.
        body = json.dumps({'sourceUrl': engine.encoded(source), 'core': {}}).encode()
        self.assertLess(len(body) + 20_000, public.MAX_BODY)
        twin, _ = public.generate({'mode': 'upload', 'imageBase64': base64.b64encode(source).decode()}, 'static')
        self.assertLess(len(twin), public.MAX_BODY)

    def request(self, action='preview', payload=None, origin='https://design.mez.studio', length=None, content_type='application/json'):
        obj = object.__new__(public.handler)
        body = json.dumps(payload or {'mode': 'compose', 'recipe': {}}).encode()
        obj.path = '/api/gradient-maker?action=' + action
        obj.headers = {'Host': 'design.mez.studio', 'Origin': origin, 'Content-Type': content_type, 'Content-Length': str(length or len(body))}
        obj.rfile = io.BytesIO(body)
        obj.respond = lambda data, status=200, content_type='application/json': setattr(obj, 'result', (status, data, content_type))
        obj.do_POST()
        return obj.result

    def test_http_boundary_and_no_remote_collection_access(self):
        self.assertEqual(self.request(origin='https://other.example')[0], 403)
        self.assertEqual(self.request(origin='')[0], 403)
        self.assertEqual(self.request(length=public.MAX_BODY + 1)[0], 413)
        self.assertEqual(self.request(content_type='text/plain')[0], 415)
        for action in ['save', 'review', 'candidates', 'export']:
            self.assertEqual(self.request(action=action)[0], 404)
        self.assertEqual(self.request()[0], 400)
        self.assertEqual(self.request(payload={'mode': 'compose', 'recipe': recipe()})[0], 200)

    def test_busy_instances_fail_without_queuing_more_image_work(self):
        public.WORKERS.acquire(); public.WORKERS.acquire()
        try:
            self.assertEqual(self.request()[0], 429)
        finally:
            public.WORKERS.release(); public.WORKERS.release()

    def test_browser_zip_reads_with_standard_python_and_preserves_binary(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'package.zip'
            code = """import {zipBlob} from './brand-kit/gradient-maker/zip.js';
import {writeFile} from 'node:fs/promises';
const data = Uint8Array.from({length: 65537}, (_, i) => i % 256);
const zip = zipBlob({'source.png': data, 'unicode-é.txt': new TextEncoder().encode('Mez ✓'), 'empty': new Uint8Array()});
await writeFile(process.argv[1], new Uint8Array(await zip.arrayBuffer()));"""
            subprocess.run(['node', '--input-type=module', '-e', code, str(path)], cwd=ROOT, check=True)
            with zipfile.ZipFile(path) as package:
                self.assertIsNone(package.testzip())
                self.assertEqual(package.read('source.png'), bytes(i % 256 for i in range(65537)))
                self.assertEqual(package.read('unicode-é.txt').decode(), 'Mez ✓')
                self.assertEqual(package.read('empty'), b'')


if __name__ == '__main__':
    unittest.main()
