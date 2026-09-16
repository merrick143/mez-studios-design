"""Local production-like QA: static site plus the stateless public function."""
import importlib.util
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import argparse
import os

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('public_maker', ROOT / 'api/gradient-maker.py')
public = importlib.util.module_from_spec(spec)
spec.loader.exec_module(public)


class Handler(public.handler, SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.split('?')[0] == '/api/gradient-maker':
            return public.handler.do_GET(self)
        return SimpleHTTPRequestHandler.do_GET(self)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8916)
    args = parser.parse_args()
    os.chdir(ROOT)
    print(f'Public-mode preview: http://127.0.0.1:{args.port}/brand-kit/gradient-maker/?public', flush=True)
    ThreadingHTTPServer(('127.0.0.1', args.port), Handler).serve_forever()
