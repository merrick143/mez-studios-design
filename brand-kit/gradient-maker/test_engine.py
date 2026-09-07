"""Behaviour tests run in temporary workspaces; never write the source library."""
import base64
from concurrent.futures import ThreadPoolExecutor
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
import uuid
import zipfile

from PIL import Image
import numpy as np

spec = importlib.util.spec_from_file_location('maker', Path(__file__).with_name('engine.py'))
maker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(maker)


def recipe():
    presets = json.loads(Path(__file__).with_name('presets.json').read_text())
    return {'version': maker.VERSION, 'seed': 7, 'softness': .45, 'flow': .35,
            'points': [{'hex': colour, 'x': xy[0], 'y': xy[1], 'weight': 1}
                       for colour, xy in zip(presets['presets'][0]['colours'], presets['positions'])]}


class MakerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = maker.author_source(recipe(), 512)
        cls.png = maker.image_bytes(cls.source)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='mez-maker-test-')
        self.workspace = Path(self.temp.name)
        self.request = {'mode': 'compose', 'recipe': recipe(), 'name': 'Test mineral', 'requestId': str(uuid.uuid4())}

    def tearDown(self):
        self.temp.cleanup()

    def upload(self, data=None):
        return {'mode': 'upload', 'imageBase64': base64.b64encode(data or self.png).decode(), 'filename': 'source.png'}

    def test_source_reproduction_and_remix(self):
        self.assertEqual(self.png, maker.image_bytes(maker.author_source(recipe(), 512)))
        remixed = recipe(); remixed['seed'] += 1
        self.assertNotEqual(self.png, maker.image_bytes(maker.author_source(remixed, 512)))

    def test_exact_static_twin_and_extraction(self):
        draft = maker.build_draft(self.upload())
        static = np.array(Image.open(io.BytesIO(draft['static'])))
        source = np.array(Image.open(io.BytesIO(draft['source'])))
        self.assertTrue(np.array_equal(source, static))
        self.assertEqual(len(draft['core']['anchors']), 4)
        self.assertEqual(draft['original'], self.png)
        self.assertEqual(draft['origin']['originalSha256'], hashlib.sha256(self.png).hexdigest())

    def test_recipe_rejects_invalid_and_nonfinite_inputs(self):
        for key, value in [('seed', 1.5), ('seed', True), ('softness', float('nan')), ('flow', 2)]:
            with self.subTest(key=key, value=value):
                invalid = recipe(); invalid[key] = value
                with self.assertRaises(ValueError): maker.validate_recipe(invalid)
        invalid = recipe(); invalid['points'][0]['hex'] = 'red'
        with self.assertRaises(ValueError): maker.validate_recipe(invalid)
        invalid = recipe()
        for point in invalid['points']: point['hex'] = '#444444'
        with self.assertRaisesRegex(ValueError, 'different colours'): maker.validate_recipe(invalid)

    def test_upload_errors_are_actionable(self):
        cases = [(Image.new('RGB', (512, 511)), 'PNG', 'square'),
                 (self.source, 'WEBP', 'original PNG'),
                 (Image.new('RGB', (512, 512), '#333333'), 'PNG', 'too flat')]
        for image, fmt, message in cases:
            with self.subTest(message=message), self.assertRaisesRegex(ValueError, message):
                maker.build_draft(self.upload(maker.image_bytes(image, fmt)))
        with self.assertRaisesRegex(ValueError, 'could not be read'):
            maker.build_draft({'mode': 'upload', 'imageBase64': 'not-base64!'})

    def test_transparency_is_recorded_and_original_retained(self):
        rgba = self.source.convert('RGBA'); rgba.putalpha(128)
        draft = maker.build_draft(self.upload(maker.image_bytes(rgba)))
        self.assertIn('white', draft['origin']['normalisation'])
        self.assertEqual(Image.open(io.BytesIO(draft['source'])).mode, 'RGB')

    def test_saved_upload_keeps_original_and_portable_source(self):
        request = dict(self.upload(), name='Upload fixture', requestId=str(uuid.uuid4()))
        candidate = maker.save(request, self.workspace)
        folder = self.workspace / candidate['slug']
        self.assertEqual((folder / 'original-upload.bin').read_bytes(), self.png)
        self.assertIsNone(candidate['recipe'])
        self.assertEqual(candidate['source']['kind'], 'upload')

    def test_http_validation_and_origin_boundary(self):
        class Handler:
            command = 'POST'
            path = '/api/gradient-maker/save'
            headers = {'Host': '127.0.0.1:8915', 'Origin': 'https://unrelated.example', 'Content-Type': 'application/json'}
            payload = []
            def read_request_json(self): return self.payload
            def json_response(self, body, status=200): self.result = (status, body)
        handler = Handler()
        maker.handle_http(handler)
        self.assertEqual(handler.result[0], 403)
        handler.headers = dict(handler.headers, Origin='http://127.0.0.1:8915')
        maker.handle_http(handler)
        self.assertEqual(handler.result[0], 400)
        handler.command = 'GET'; handler.path = '/api/gradient-maker/status'
        maker.handle_http(handler)
        self.assertTrue(handler.result[1]['local'])
        handler.headers = {'Host': 'unrelated.example'}
        maker.handle_http(handler)
        self.assertEqual(handler.result[0], 400)

    def test_immutable_save_retry_lineage_and_export_integrity(self):
        original = maker.save(self.request, self.workspace)
        retry = maker.save(self.request, self.workspace)
        self.assertEqual(original, retry)
        revised = dict(self.request, requestId=str(uuid.uuid4()), parentSlug=original['slug'], name='<b>Refined</b>')
        newer = maker.save(revised, self.workspace)
        self.assertNotEqual(original['candidateId'], newer['candidateId'])
        self.assertEqual(newer['parentSlug'], original['slug'])
        self.assertEqual(len(maker.list_candidates(self.workspace)), 2)
        with zipfile.ZipFile(io.BytesIO(maker.export_zip(newer['slug'], self.workspace))) as archive:
            manifest = json.loads(archive.read('manifest.json'))
            for name, expected in manifest['files'].items():
                self.assertEqual(hashlib.sha256(archive.read(name)).hexdigest(), expected, name)
            self.assertEqual(archive.read('mz-core.js'), maker.RUNTIME.read_bytes())
            self.assertIn(b'&lt;b&gt;Refined&lt;/b&gt;', archive.read('preview.html'))
            self.assertFalse(json.loads(archive.read('candidate.json'))['productionAuthority'])

    def test_review_history_and_no_canonical_writes(self):
        paths = [maker.BRAND / p for p in ['registry/gradients.json', 'registry/products.json', 'gradient-library/assignments.json', 'governance/post-cutover-decisions.json']]
        before = {str(p): p.read_bytes() for p in paths}
        candidate = maker.save(self.request, self.workspace)
        for verdict in ['shortlist', 'revise']:
            result = maker.review({'slug': candidate['slug'], 'verdict': verdict, 'note': 'Test note'}, self.workspace)
            self.assertFalse(result['promotesCandidate'])
        folder = self.workspace / candidate['slug']
        self.assertEqual(len((folder / 'review-history.jsonl').read_text().splitlines()), 2)
        self.assertEqual(maker.list_candidates(self.workspace)[0]['review']['verdict'], 'revise')
        self.assertEqual(before, {str(p): p.read_bytes() for p in paths})

    def test_parallel_saves_get_distinct_ids(self):
        with ThreadPoolExecutor(max_workers=2) as executor:
            rows = list(executor.map(lambda request: maker.save(request, self.workspace),
                                     [dict(self.request, requestId=str(uuid.uuid4())) for _ in range(2)]))
        self.assertEqual(len({row['candidateId'] for row in rows}), 2)

    def test_path_traversal_and_unknown_parent_rejected(self):
        for slug in ['../../registry', 'draft-foo', 'draft-' + 'a' * 32]:
            with self.assertRaises(ValueError): maker.export_zip(slug, self.workspace)
        with self.assertRaises(ValueError):
            maker.save(dict(self.request, parentSlug='draft-' + 'f' * 32), self.workspace)
        self.assertEqual(maker.list_candidates(self.workspace), [])


if __name__ == '__main__':
    unittest.main()
