"""Local gradient authoring and immutable research candidates.

The author creates a PNG. The existing Living Core extractor still owns the
PNG-to-palette contract. No operation writes the approved library or registers.
"""
from __future__ import annotations

import base64
import fcntl
import hashlib
import html
import importlib.util
import io
import json
import math
import re
import shutil
import tempfile
import threading
import uuid
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import numpy as np
from PIL import Image, ImageOps, UnidentifiedImageError, __version__ as pillow_version

HERE = Path(__file__).resolve().parent
BRAND = HERE.parent
WORKSPACE = BRAND / "workspace" / "gradient-maker"
RUNTIME = BRAND / "source-pack/design-system-export/mz-core.js"
WINGS = BRAND / "source-pack/design-system-export/assets/wings.svg"
BUILDER = BRAND / "source-pack/living-core/build.py"
VERSION = "mesh-source-1"
HEX = re.compile(r"^#[0-9a-fA-F]{6}$")
SLUG = re.compile(r"^draft-[0-9a-f]{32}$")
LOCK = threading.RLock()
PREVIEW_LOCK = threading.Semaphore(2)
MAX_IMAGE_BYTES = 12 * 1024 * 1024
MAX_PIXELS = 4096 * 4096

spec = importlib.util.spec_from_file_location("mez_gradient_extraction", BUILDER)
extractor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(extractor)


def stamp():
    return datetime.now(timezone.utc).isoformat()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(data, kind="png"):
    return f"data:image/{kind};base64," + base64.b64encode(data).decode()


def json_bytes(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode()


def number(value, low, high, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not low <= value <= high:
        raise ValueError(f"{name} must be between {low} and {high}.")
    return float(value)


def validate_recipe(value):
    if not isinstance(value, dict) or value.get("version", VERSION) != VERSION:
        raise ValueError("This recipe uses an unsupported source generator.")
    points = value.get("points")
    if not isinstance(points, list) or not 3 <= len(points) <= 6:
        raise ValueError("Choose between three and six colour points.")
    result = []
    for p in points:
        if not isinstance(p, dict) or not isinstance(p.get("hex"), str) or not HEX.fullmatch(p["hex"]):
            raise ValueError("Use six-digit hex colours, such as #167A68.")
        result.append({"hex": p["hex"].upper(), "x": number(p.get("x"), 0, 1, "Horizontal position"), "y": number(p.get("y"), 0, 1, "Vertical position"), "weight": number(p.get("weight", 1), 0.3, 2, "Colour strength")})
    if len({p['hex'] for p in result}) < 2:
        raise ValueError("Choose at least two different colours so the core has some depth.")
    seed = value.get("seed", 7)
    if type(seed) is not int or not 0 <= seed <= 999999:
        raise ValueError("The composition seed must be a whole number from 0 to 999999.")
    return {"version": VERSION, "points": result, "seed": seed, "softness": number(value.get("softness", 0.45), 0.15, 0.85, "Blend softness"), "flow": number(value.get("flow", 0.35), 0, 1, "Flow")}


def author_source(recipe, size=1024):
    """Deterministic linear-light mesh with a seeded smooth coordinate warp."""
    recipe = validate_recipe(recipe)
    if size not in (512, 1024, 2048):
        raise ValueError("Source size must be 512, 1024 or 2048 pixels.")
    y, x = np.mgrid[0:size, 0:size].astype(np.float64) / (size - 1)
    phase = np.random.default_rng(recipe["seed"]).uniform(0, 2 * np.pi, 4)
    flow = recipe["flow"] * 0.19
    u = x + flow * (np.sin(y * 5 + phase[0]) + 0.4 * np.sin(x * 9 + y * 4 + phase[1]))
    v = y + flow * (np.sin(x * 5 + phase[2]) + 0.4 * np.sin(y * 8 - x * 3 + phase[3]))
    colour = np.zeros((size, size, 3), dtype=np.float64)
    total = np.zeros((size, size), dtype=np.float64)
    sigma = 0.09 + recipe["softness"] * 0.45
    for point in recipe["points"]:
        weight = np.exp(-((u - point["x"]) ** 2 + (v - point["y"]) ** 2) / (2 * sigma ** 2)) * point["weight"]
        rgb = np.array([int(point["hex"][i:i + 2], 16) / 255 for i in (1, 3, 5)]) ** 2.2
        colour += weight[:, :, None] * rgb
        total += weight
    rgb = np.clip((colour / np.maximum(total[:, :, None], 1e-20)) ** (1 / 2.2), 0, 1)
    return Image.fromarray(np.rint(rgb * 255).astype(np.uint8))


def image_bytes(image, fmt="PNG"):
    out = io.BytesIO()
    kwargs = {"lossless": True, "method": 6} if fmt == "WEBP" else {"compress_level": 6}
    image.save(out, format=fmt, **kwargs)
    return out.getvalue()


def upload_source(payload):
    raw = payload.get("imageBase64", "")
    if not isinstance(raw, str) or len(raw) > MAX_IMAGE_BYTES * 1.4:
        raise ValueError("Upload a PNG or JPEG under 12 MB.")
    try:
        original = base64.b64decode(raw, validate=True)
    except (ValueError, TypeError) as error:
        raise ValueError("The uploaded image could not be read. Choose it again.") from error
    if not original or len(original) > MAX_IMAGE_BYTES:
        raise ValueError("Upload a PNG or JPEG under 12 MB.")
    try:
        with Image.open(io.BytesIO(original)) as im:
            if im.format not in {"PNG", "JPEG"}:
                raise ValueError("Choose an original PNG or JPEG. Generated WebP fallbacks are not source images.")
            if im.width != im.height or im.width < 512 or im.width * im.height > MAX_PIXELS:
                raise ValueError("Choose a square image between 512 and 4096 pixels.")
            fmt = im.format
            im = ImageOps.exif_transpose(im)
            transparent = "A" in im.getbands() or "transparency" in im.info
            if transparent:
                rgba = im.convert("RGBA")
                image = Image.new("RGB", rgba.size, "white")
                image.paste(rgba, mask=rgba.getchannel("A"))
            else:
                image = im.convert("RGB")
            image.load()
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as error:
        raise ValueError("That image could not be decoded. Try another PNG or JPEG.") from error
    return image, original, {"kind": "upload", "originalFilename": Path(str(payload.get("filename", "source"))).name[:160], "originalFormat": fmt, "originalSha256": digest(original), "normalisation": "EXIF orientation applied; RGB PNG; transparency flattened onto white" if transparent else "EXIF orientation applied; RGB PNG"}


def build_draft(payload):
    if not isinstance(payload, dict):
        raise ValueError("Send a gradient recipe or a source image.")
    if payload.get("mode", "compose") == "compose":
        recipe = validate_recipe(payload.get("recipe"))
        image = author_source(recipe)
        original = None
        origin = {"kind": "authored", "generator": VERSION, "recipeSha256": digest(json_bytes(recipe))}
    elif payload.get("mode") == "upload":
        image, original, origin = upload_source(payload)
        recipe = None
    else:
        raise ValueError("Choose Compose or Upload.")
    source = image_bytes(image)
    # Keep extraction unchanged. Flat uploads get an actionable failure rather
    # than changing the hash-locked extractor or inventing missing anchors.
    with tempfile.TemporaryDirectory(prefix="mez-gradient-preview-") as temp:
        path = Path(temp) / "source.png"
        path.write_bytes(source)
        try:
            entry = extractor.extract(path)
        except (IndexError, FloatingPointError) as error:
            raise ValueError("This image is too flat to extract a Living Core. Add more colour or tonal variation.") from error
    static = image_bytes(image, "WEBP")
    core = {"id": "draft", **extractor.canonical_core(entry, "static.webp")}
    return {"recipe": recipe, "source": source, "static": static, "original": original, "origin": origin, "core": core, "width": image.width, "height": image.height, "fingerprint": digest(source)}


def preview(payload):
    with PREVIEW_LOCK:
        d = build_draft(payload)
    return {"ok": True, "recipe": d["recipe"], "sourceUrl": encoded(d["source"]), "staticUrl": encoded(d["static"], "webp"), "core": d["core"], "fingerprint": d["fingerprint"], "width": d["width"], "height": d["height"], "origin": d["origin"], "productionAuthority": False}


def candidate_path(slug, workspace=WORKSPACE):
    if not isinstance(slug, str) or not SLUG.fullmatch(slug):
        raise ValueError("The saved candidate reference is invalid.")
    path = workspace / slug
    if path.is_symlink() or not (path / "candidate.json").is_file():
        raise ValueError("That candidate is no longer available.")
    return path


def summary(path):
    record = json.loads((path / "candidate.json").read_text())
    base = f"/brand-kit/workspace/gradient-maker/{path.name}/"
    return {**record, "slug": path.name, "sourceUrl": base + "source.png", "staticUrl": base + "static.webp", "previewUrl": base + "preview.html", "exportUrl": "/api/gradient-maker/export?slug=" + path.name, "review": json.loads((path / "review.json").read_text()) if (path / "review.json").is_file() else None}


def list_candidates(workspace=WORKSPACE):
    if not workspace.exists():
        return []
    result = []
    for path in workspace.glob("draft-*"):
        if path.is_symlink() or not (path / "candidate.json").is_file():
            continue
        try:
            result.append(summary(path))
        except (ValueError, KeyError, OSError):
            continue
    return sorted(result, key=lambda row: row["createdAt"], reverse=True)


def next_id(workspace=WORKSPACE):
    ids = json.loads((BRAND / "gradient-library/library-manifest.json").read_text())["ids"]
    ids += [row["candidateId"] for row in list_candidates(workspace)]
    for path in (BRAND / "workspace/candidates").glob("*/candidate.json"):
        try:
            ids.append(json.loads(path.read_text())["candidateId"])
        except (ValueError, KeyError, OSError):
            pass
    highest = max(int(x.split("G")[1]) for x in ids if re.fullmatch(r"MZ-G\d{2,3}", x))
    if highest >= 999:
        raise ValueError("The provisional ID range is full. Review the candidate library before creating more.")
    return f"MZ-G{highest + 1:02d}"


def save(payload, workspace=WORKSPACE):
    name = payload.get("name", "")
    if not isinstance(name, str) or not 2 <= len(name.strip()) <= 80:
        raise ValueError("Give this candidate a name between 2 and 80 characters.")
    try:
        request_id = uuid.UUID(payload.get("requestId", ""))
    except (ValueError, AttributeError, TypeError) as error:
        raise ValueError("The save request is missing its unique reference. Try saving again.") from error
    slug = "draft-" + request_id.hex
    parent = payload.get("parentSlug") or None
    # A stable request ID returns the original save after network retries.
    with LOCK:
        workspace.mkdir(parents=True, exist_ok=True)
        with (workspace / ".lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            if (workspace / slug / "candidate.json").is_file():
                return summary(workspace / slug)
            if parent:
                candidate_path(parent, workspace)
            d = build_draft(payload)
            candidate_id = next_id(workspace)
            core = {**d["core"], "id": candidate_id}
            record = {"schemaVersion": "1.0.0", "candidateId": candidate_id, "name": name.strip(), "createdAt": stamp(), "status": "research-only", "productionAuthority": False, "parentSlug": parent, "mode": payload.get("mode", "compose"), "recipe": d["recipe"], "source": {"file": "source.png", "sha256": d["fingerprint"], "width": d["width"], "height": d["height"], **d["origin"]}, "core": core, "extraction": {"clusters": extractor.K, "sample": extractor.SAMPLE, "seed": extractor.SEED, "method": "k-means++"}, "environment": {"numpy": np.__version__, "pillow": pillow_version}, "promotion": {"status": "not-promoted", "requires": ["Human review of source, static and animated result", "Separate approved library import", "Separate product assignment when applicable", "Release rebuild and validation when distributing"]}}
            temporary = Path(tempfile.mkdtemp(prefix=".building-", dir=workspace))
            try:
                (temporary / "source.png").write_bytes(d["source"])
                (temporary / "static.webp").write_bytes(d["static"])
                if d["original"]:
                    (temporary / "original-upload.bin").write_bytes(d["original"])
                if d["recipe"]:
                    (temporary / "recipe.json").write_bytes(json_bytes(d["recipe"]))
                (temporary / "candidate.json").write_bytes(json_bytes(record))
                (temporary / "mz-core.js").write_bytes(RUNTIME.read_bytes())
                (temporary / "wings.svg").write_bytes(WINGS.read_bytes())
                template = (HERE / "preview-template.html").read_text()
                embedded = json.dumps(core).replace("<", "\\u003c")
                preview_html = template.replace("{{NAME}}", html.escape(name.strip())).replace("{{ID}}", candidate_id).replace("{{CORE}}", embedded)
                (temporary / "preview.html").write_text(preview_html)
                (temporary / "README.md").write_text(f"# {name.strip()}\n\nResearch candidate {candidate_id}. Not approved or assigned to a product.\n\nServe this folder over local HTTP and open preview.html to compare the source and Living Core. source.png owns colour; static.webp preserves its RGB pixels losslessly. The animation is an approximation.\n\nThe recipe, when present, reproduces the source with generator {VERSION} in the pinned NumPy/Pillow environment recorded in candidate.json. The original upload is preserved separately when supplied.\n\nShortlisting is not promotion. Review source, static and animation, then record a separate library decision before import. Product assignment and release distribution are separate decisions.\n")
                hashes = {p.name: digest(p.read_bytes()) for p in temporary.iterdir() if p.is_file()}
                (temporary / "manifest.json").write_bytes(json_bytes({"schemaVersion": "1.0.0", "productionAuthority": False, "files": hashes}))
                temporary.rename(workspace / slug)
            except BaseException:
                shutil.rmtree(temporary, ignore_errors=True)
                raise
    return summary(workspace / slug)


def review(payload, workspace=WORKSPACE):
    path = candidate_path(payload.get("slug"), workspace)
    verdict = payload.get("verdict")
    if verdict not in {"shortlist", "revise", "reject"}:
        raise ValueError("Choose Shortlist, Needs changes or Reject.")
    note = payload.get("note", "")
    if not isinstance(note, str) or len(note) > 2000:
        raise ValueError("Keep the review note under 2000 characters.")
    record = {"verdict": verdict, "note": note.strip(), "reviewedAt": stamp(), "productionAuthority": False, "promotesCandidate": False}
    with LOCK:
        with (workspace / ".lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            with (path / "review-history.jsonl").open("ab") as history:
                history.write(json.dumps(record, ensure_ascii=False).encode() + b"\n")
            temporary = path / (".review-" + uuid.uuid4().hex)
            temporary.write_bytes(json_bytes(record))
            temporary.replace(path / "review.json")
    return record


def export_zip(slug, workspace=WORKSPACE):
    path = candidate_path(slug, workspace)
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as package:
        for item in sorted(path.iterdir()):
            if item.is_file() and not item.is_symlink() and not item.name.startswith("."):
                package.writestr(item.name, item.read_bytes())
    return out.getvalue()


def handle_http(handler):
    """Route only maker endpoints. All writes require same-origin local JSON."""
    from urllib.parse import parse_qs
    try:
        host = handler.headers.get("Host", "")
        if urlparse("http://" + host).hostname not in {"localhost", "127.0.0.1", "::1"}:
            raise ValueError("Open the maker through its local server.")
        parsed = urlparse(handler.path)
        action = parsed.path.removeprefix("/api/gradient-maker/")
        if handler.command == "GET":
            if action == "status":
                handler.json_response({"ok": True, "version": VERSION, "local": True})
            elif action == "candidates":
                handler.json_response({"ok": True, "candidates": list_candidates()})
            elif action == "export":
                data = export_zip(parse_qs(parsed.query).get("slug", [None])[0])
                handler.send_response(200)
                handler.send_header("Content-Type", "application/zip")
                handler.send_header("Content-Disposition", 'attachment; filename="mez-gradient-candidate.zip"')
                handler.send_header("Content-Length", str(len(data)))
                handler.send_header("Cache-Control", "no-store")
                handler.end_headers()
                handler.wfile.write(data)
            else:
                handler.json_response({"error": "Unknown gradient maker route."}, 404)
            return
        origin = handler.headers.get("Origin")
        if origin and (urlparse(origin).netloc != host or urlparse(origin).scheme != "http"):
            handler.json_response({"error": "Use the maker on the same local server."}, 403)
            return
        if handler.headers.get("Content-Type", "").split(";")[0] != "application/json":
            raise ValueError("Send this request as JSON.")
        payload = handler.read_request_json()
        if not isinstance(payload, dict):
            raise ValueError("Send a JSON object containing a recipe or source image.")
        if action == "preview":
            handler.json_response(preview(payload))
        elif action == "save":
            handler.json_response({"ok": True, "candidate": save(payload)}, 201)
        elif action == "review":
            handler.json_response({"ok": True, "review": review(payload)})
        else:
            handler.json_response({"error": "Unknown gradient maker route."}, 404)
    except (ValueError, TypeError) as error:
        handler.json_response({"error": str(error)}, 400)
    except (BrokenPipeError, ConnectionResetError):
        pass
    except Exception:
        handler.json_response({"error": "The local maker could not finish that operation. Your saved candidates are unchanged; try again."}, 500)
