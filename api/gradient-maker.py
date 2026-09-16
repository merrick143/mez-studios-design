"""Stateless public generation. Drafts and uploads are never saved by this API."""
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse
import importlib.util
import json
import threading

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("public_gradient_engine", ROOT / "brand-kit/gradient-maker/engine.py")
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)

# Keep both directions below the platform's 4.5 MB request/response ceiling.
# A 1024px RGB PNG fits even when it cannot be compressed. Send its WebP twin
# separately, as binary, so no JSON response contains two copies of an image.
MAX_BODY = 4_300_000
MAX_UPLOAD = 3 * 1024 * 1024
MAX_SIDE = 1024
WORKERS = threading.BoundedSemaphore(2)


def generate(payload, action):
    if not isinstance(payload, dict):
        raise ValueError("Send a colour recipe or a source image.")
    mode = payload.get("mode", "compose")
    if mode == "upload":
        image, original, _ = engine.upload_source(payload)
        # The static route receives our normalised PNG, which can be slightly
        # larger than the original file after lossless encoding.
        if action != "static" and len(original) > MAX_UPLOAD:
            raise ValueError("Choose a PNG or JPEG no larger than 3 MB.")
        if image.width > MAX_SIDE:
            raise ValueError("Choose a square PNG or JPEG between 512 and 1024 pixels.")
    if action == "static":
        if mode != "upload":
            raise ValueError("Send the saved source PNG to make its static twin.")
        return engine.image_bytes(image, "WEBP"), "image/webp"
    if action != "preview":
        raise ValueError("Unknown gradient maker operation.")
    draft = engine.build_draft(payload)
    result = {
        "ok": True, "recipe": draft["recipe"], "sourceUrl": engine.encoded(draft["source"]),
        "core": draft["core"], "fingerprint": draft["fingerprint"],
        "width": draft["width"], "height": draft["height"], "origin": draft["origin"],
        "extraction": {"clusters": engine.extractor.K, "sample": engine.extractor.SAMPLE,
                       "seed": engine.extractor.SEED, "method": "k-means++"},
        "environment": {"numpy": engine.np.__version__, "pillow": engine.pillow_version},
        "productionAuthority": False,
    }
    return json.dumps(result, allow_nan=False).encode(), "application/json"


class handler(BaseHTTPRequestHandler):
    def respond(self, body, status=200, content_type="application/json"):
        if isinstance(body, dict):
            body = json.dumps(body).encode()
        if len(body) > MAX_BODY:
            body = b'{"error":"This image is too large to return. Try a smaller source image."}'
            status, content_type = 413, "application/json"
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        if status == 429:
            self.send_header("Retry-After", "3")
        self.end_headers()
        self.wfile.write(body)

    def action(self):
        return parse_qs(urlparse(self.path).query).get("action", ["status"])[0]

    def do_GET(self):
        if self.action() != "status":
            self.respond({"error": "Unknown gradient maker route."}, 404)
            return
        self.respond({"ok": True, "local": False, "storage": "browser", "version": engine.VERSION,
                      "maxUploadBytes": MAX_UPLOAD, "maxUploadSide": MAX_SIDE})

    def do_POST(self):
        acquired = False
        try:
            action = self.action()
            if action not in {"preview", "static"}:
                self.respond({"error": "This service only generates previews. Drafts stay in your browser."}, 404)
                return
            origin = urlparse(self.headers.get("Origin", ""))
            host = self.headers.get("Host", "")
            local = urlparse("http://" + host).hostname in {"127.0.0.1", "localhost", "::1"}
            if origin.netloc != host or origin.scheme != ("http" if local else "https"):
                self.respond({"error": "Open the maker on this website to generate a gradient."}, 403)
                return
            if self.headers.get("Content-Type", "").split(";")[0] != "application/json":
                self.respond({"error": "Send a JSON colour recipe or source image."}, 415)
                return
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= MAX_BODY:
                self.respond({"error": "Choose a PNG or JPEG no larger than 3 MB."}, 413)
                return
            acquired = WORKERS.acquire(blocking=False)
            if not acquired:
                self.respond({"error": "The maker is busy. Try again in a few seconds."}, 429)
                return
            payload = json.loads(self.rfile.read(length))
            data, content_type = generate(payload, action)
            self.respond(data, content_type=content_type)
        except (ValueError, TypeError, KeyError) as error:
            # Validation messages contain input constraints, never uploaded bytes.
            message = str(error) if isinstance(error, ValueError) and not isinstance(error, json.JSONDecodeError) else "Check your colour recipe or source image and try again."
            self.respond({"error": message}, 400)
        except (BrokenPipeError, ConnectionResetError):
            pass
        except Exception:
            self.respond({"error": "The maker could not finish. Your browser drafts are safe; try again."}, 500)
        finally:
            if acquired:
                WORKERS.release()
