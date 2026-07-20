#!/usr/bin/env python3
"""
Play Orb builder.

Reads Mez Systems gradient PNGs, extracts each one's palette and composition,
and generates a self-contained animated orb per gradient plus a comparison
board showing them side by side.

Usage
-----
    python3 build.py                       # rebuild everything from DEFAULT_IDS
    python3 build.py MZ-G06 MZ-G13         # only these gradients
    python3 build.py --keep-palettes       # reuse palettes.json, skip extraction
                                           # (use after hand-editing the JSON)

Outputs
-------
    palettes.json        extracted data, safe to hand-edit
    orbs/<ID>.html       one standalone orb per gradient
    index.html           expression board (the main one)
    compare.html         raw gradient comparison

Requires: pillow, numpy. No API keys, no network.
"""

import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
GRADIENT_DIR = Path.home() / "Downloads" / "all-gradients"
TEMPLATE = HERE / "orb-template.html"
PALETTES = HERE / "palettes.json"
ORB_DIR = HERE / "orbs"

DEFAULT_IDS = ["MZ-G13", "MZ-G20", "MZ-G06", "MZ-G15"]

# The four product cores, per the Figma brand kit (locked 12 Jul 2026).
# AI OS = MZ-G13 is LOCKED. The other three are current picks, status
# CANDIDATE, so changing a gradient here is a one-line edit by design.
#
# PUBLIC BUILD: only the locked flagship is named. Cores 02 to 04 are
# deliberately generic because their product names are still candidates and
# this board is published to a public repo. Swap the name/sub/body back in
# once those names are ratified.
PRODUCTS = [
    {"id": "aios",   "gradient": "MZ-G13", "name": "AI OS",
     "sub": "AI Operating System",
     "body": "The flagship. Every workflow, every agent, one operating system."},
    {"id": "core02", "gradient": "MZ-G20", "name": "Core 02",
     "sub": "Warm spectrum",
     "body": "Coral through amber. The warm end of the library."},
    {"id": "core03", "gradient": "MZ-G06", "name": "Core 03",
     "sub": "Violet spectrum",
     "body": "Mint through violet. The widest hue travel of the four."},
    {"id": "core04", "gradient": "MZ-G15", "name": "Core 04",
     "sub": "Green spectrum",
     "body": "Teal through lime. The coolest and calmest of the set."},
]

EXPR_TEMPLATE = HERE / "expressions-template.html"

# Number of colour clusters to pull from each gradient. Four become the mesh
# anchors and one becomes the shading colour, which is what the shader expects.
K = 5
SAMPLE = 160          # working resolution for clustering
SEED = 7              # fixed so rebuilds are reproducible


# ---------------------------------------------------------------------------
# Palette extraction
# ---------------------------------------------------------------------------

def kmeans(points, k, seed=SEED, iters=40):
    """Plain k-means++ over RGB. Returns (labels, centres).

    Deliberately dependency-light: sklearn would be a heavier install for a
    job this small, and the fixed seed matters more here than convergence
    speed, because rebuilds need to produce identical palettes.
    """
    rng = np.random.default_rng(seed)
    n = len(points)

    # k-means++ seeding. Random seeding regularly collapses two centres onto
    # the same colour on smooth gradients, which silently costs an anchor.
    centres = [points[rng.integers(n)]]
    for _ in range(k - 1):
        d2 = np.min(
            ((points[:, None, :] - np.array(centres)[None, :, :]) ** 2).sum(-1),
            axis=1,
        )
        total = d2.sum()
        probs = d2 / total if total > 0 else np.full(n, 1 / n)
        centres.append(points[rng.choice(n, p=probs)])
    centres = np.array(centres, dtype=float)

    labels = np.zeros(n, dtype=int)
    for _ in range(iters):
        d2 = ((points[:, None, :] - centres[None, :, :]) ** 2).sum(-1)
        new_labels = d2.argmin(axis=1)
        if (new_labels == labels).all():
            break
        labels = new_labels
        for j in range(k):
            member = points[labels == j]
            if len(member):
                centres[j] = member.mean(axis=0)
    return labels, centres


def relative_luminance(rgb):
    """Rec.709 luma on 0..1 RGB."""
    r, g, b = rgb
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def extract(path):
    """Extract anchors + shade + composition from one gradient PNG."""
    im = Image.open(path).convert("RGB").resize((SAMPLE, SAMPLE), Image.LANCZOS)
    arr = np.asarray(im, dtype=float) / 255.0

    ys, xs = np.mgrid[0:SAMPLE, 0:SAMPLE]
    pts = arr.reshape(-1, 3)
    labels, centres = kmeans(pts, K)

    clusters = []
    for j in range(K):
        mask = labels == j
        share = float(mask.mean())
        if share < 0.005:            # a cluster this small is noise, not a colour
            continue
        cx = float(xs.reshape(-1)[mask].mean()) / (SAMPLE - 1)
        cy = float(ys.reshape(-1)[mask].mean()) / (SAMPLE - 1)
        clusters.append({
            "rgb": [round(float(v), 4) for v in centres[j]],
            "share": round(share, 4),
            # Shader uv space: origin at centre, +y upwards. Image y runs
            # downwards, hence the flip. Scaled to 0.82 so anchors stay inside
            # the inscribed disc rather than parking out in the dead corners
            # of the source square.
            "pos": [round((cx - 0.5) * 0.82, 4), round((0.5 - cy) * 0.82, 4)],
            "lum": round(relative_luminance(centres[j]), 4),
        })

    # The darkest cluster becomes the shading colour. Every one of these
    # gradients has a dark region and it is what gives the orb its sphere
    # read, so it is pulled out rather than left as a fifth flat anchor.
    clusters.sort(key=lambda c: c["lum"])
    shade = clusters[0]
    rest = clusters[1:]

    # Anchors ordered light to dark, then padded if a gradient was so flat
    # that clustering found fewer than four usable colours.
    rest.sort(key=lambda c: -c["share"])
    anchors = rest[:4]
    while len(anchors) < 4:
        anchors.append(dict(anchors[-1]))

    return {"anchors": anchors, "shade": shade}


# ---------------------------------------------------------------------------
# Code generation
# ---------------------------------------------------------------------------

def hexstr(rgb):
    return "#%02X%02X%02X" % tuple(max(0, min(255, round(v * 255))) for v in rgb)


def glsl_vec3(rgb):
    return "vec3(%.3f, %.3f, %.3f)" % tuple(rgb)


def palette_glsl(entry):
    """Emit the per-gradient block the shader template splices in."""
    a = entry["anchors"]
    s = entry["shade"]
    lines = []

    for i, c in enumerate(a):
        lines.append(
            "      vec3 C%d = toLinear(%s);  // %s  %.0f%% of source"
            % (i, glsl_vec3(c["rgb"]), hexstr(c["rgb"]), c["share"] * 100)
        )
    lines.append(
        "      vec3 SHADE = toLinear(%s);  // %s  darkest cluster, drives sphere shading"
        % (glsl_vec3(s["rgb"]), hexstr(s["rgb"]))
    )
    lines.append("")

    # Orbit rates are fixed rather than derived. They only need to be mutually
    # non-repeating, and holding them constant means every gradient animates at
    # the same cadence, so a comparison is of colour and nothing else.
    rates = [(0.113, 0.131, 0.0), (0.091, 0.107, 1.9),
             (0.127, 0.083, 3.6), (0.079, 0.119, 5.2)]
    for i, (c, (rx, ry, ph)) in enumerate(zip(a, rates)):
        lines.append(
            "      vec2 A%d = anchor(vec2(%.3f, %.3f), %.3f, %.3f, %.1f, t);"
            % (i, c["pos"][0], c["pos"][1], rx, ry, ph)
        )
    lines.append("")

    # Weight multipliers track how much of the source each colour covered, so a
    # colour that was a small accent stays an accent. Compressed by a 0.6 power
    # and clamped: raw share is far too aggressive, and one 60% cluster would
    # otherwise flatten the orb to a single tone.
    mean = sum(c["share"] for c in a) / len(a)
    for i, c in enumerate(a):
        mult = (c["share"] / mean) ** 0.6 if mean > 0 else 1.0
        mult = max(0.55, min(1.75, mult))
        lines.append("      float W%d = %.3f;" % (i, mult))
    lines.append("")

    # The bloom keys off whichever anchor is lightest, which is the one that
    # reads as the lit part of the fluid. Tinted by that colour rather than a
    # fixed cream, or a cool gradient would bloom inexplicably warm.
    warm = max(range(len(a)), key=lambda i: relative_luminance(a[i]["rgb"]))
    tint = [min(1.0, v * 0.35 + 0.65) for v in a[warm]["rgb"]]
    lines.append("      #define BLOOM_W w%d" % warm)
    lines.append("      vec3 BLOOM_TINT = toLinear(%s);  // %s"
                 % (glsl_vec3(tint), hexstr(tint)))
    return "\n".join(lines)


def build_one(gid, entry, template):
    anchors = entry["anchors"]
    boot = hexstr(max(anchors, key=lambda c: c["share"])["rgb"])
    fallback = (
        "'radial-gradient(70%% 80%% at 22%% 18%%, %s 0%%, transparent 58%%),' +\n"
        "      'radial-gradient(65%% 70%% at 82%% 30%%, %s 0%%, transparent 60%%),' +\n"
        "      'radial-gradient(75%% 75%% at 60%% 88%%, %s 0%%, transparent 62%%),' +\n"
        "      '%s';"
        % (hexstr(anchors[0]["rgb"]), hexstr(anchors[1]["rgb"]),
           hexstr(anchors[2]["rgb"]), hexstr(anchors[3]["rgb"]))
    )
    return (template
            .replace("{{TITLE}}", gid)
            .replace("{{LABEL}}", gid)
            .replace("{{PALETTE_GLSL}}", palette_glsl(entry))
            .replace("{{BOOT_BG}}", boot)
            .replace("{{FALLBACK_CSS}}", fallback))


COMPARE_HEAD = """<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Play Orb / gradient comparison</title>
<style>
  :root { --stage:#efedec; --ink:#1a1720; --ink-dim:#8e8998; }
  * { box-sizing: border-box; }
  body {
    margin: 0; min-height: 100vh; padding: 4.5rem 2rem 5rem;
    background: var(--stage); color: var(--ink);
    font-family: ui-monospace, "SF Mono", SFMono-Regular, Menlo, monospace;
    display: flex; flex-direction: column; align-items: center; gap: 3.5rem;
  }
  .masthead { text-align: center; display: grid; gap: .75rem; }
  .masthead h1 {
    margin: 0; font-size: .8125rem; font-weight: 600;
    letter-spacing: .28em; text-transform: uppercase;
  }
  .masthead p { margin: 0; font-size: .6875rem; letter-spacing: .1em; color: var(--ink-dim); }
  .grid {
    display: grid; gap: 3.25rem 2.5rem; width: 100%; max-width: 1180px;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    justify-items: center;
  }
  .cell { display: grid; justify-items: center; gap: 1.1rem; }
  .meta { display: grid; justify-items: center; gap: .5rem; }
  .meta b { font-size: .75rem; font-weight: 600; letter-spacing: .16em; }
  .swatches { display: flex; gap: 4px; }
  .swatches i {
    width: 22px; height: 8px; border-radius: 2px; display: block;
    box-shadow: inset 0 0 0 1px rgba(0,0,0,.10);
  }
</style>
</head>
<body>
  <header class="masthead">
    <h1>Play Orb &middot; gradient comparison</h1>
    <p>Built by Claude Code from Mez Systems gradients. Hover any orb.</p>
  </header>
  <main class="grid">
"""

COMPARE_TAIL = """  </main>
</body>
</html>
"""


def build_compare(ids, palettes):
    """Comparison board.

    Each orb runs in its own iframe. Four live WebGL contexts in one document
    is within every browser's limit, but sharing one document would also mean
    sharing one visibility and resize path; iframes keep each orb byte-identical
    to its standalone file, so what is being compared is the gradient and
    nothing else.
    """
    cells = []
    for gid in ids:
        sw = "".join(
            '<i style="background:%s"></i>' % hexstr(c["rgb"])
            for c in palettes[gid]["anchors"]
        )
        sw += '<i style="background:%s"></i>' % hexstr(palettes[gid]["shade"]["rgb"])
        cells.append(
            '    <section class="cell">\n'
            '      <iframe src="orbs/%s.html?bare" title="%s" scrolling="no"\n'
            '              style="width:300px;height:300px;border:0;background:transparent;'
            'color-scheme:light"></iframe>\n'
            '      <div class="meta"><b>%s</b><div class="swatches">%s</div></div>\n'
            '    </section>' % (gid, gid, gid, sw)
        )
    return COMPARE_HEAD + "\n".join(cells) + "\n" + COMPARE_TAIL


def build_expressions(palettes):
    """Emit the expression board.

    Everything the page needs is inlined as one PRODUCTS array: colours in
    sRGB (the shader converts to linear itself), anchor positions, weights,
    and a one-hot selector picking the bloom anchor. Same numbers the
    standalone orbs use, so a disc here and a disc there are identical.
    """
    out = []
    for prod in PRODUCTS:
        gid = prod["gradient"]
        if gid not in palettes:
            sys.exit("Product %s needs gradient %s, which is not in palettes.json"
                     % (prod["id"], gid))
        entry = palettes[gid]
        a = entry["anchors"]

        mean = sum(c["share"] for c in a) / len(a)
        weights = []
        for c in a:
            mult = (c["share"] / mean) ** 0.6 if mean > 0 else 1.0
            weights.append(round(max(0.55, min(1.75, mult)), 3))

        warm = max(range(len(a)), key=lambda i: relative_luminance(a[i]["rgb"]))
        tint = [round(min(1.0, v * 0.35 + 0.65), 4) for v in a[warm]["rgb"]]

        out.append({
            "id": prod["id"],
            "name": prod["name"],
            "sub": prod["sub"],
            "body": prod["body"],
            "gradient": gid,
            "c": [c["rgb"] for c in a],
            "a": [c["pos"] for c in a],
            "w": weights,
            "shade": entry["shade"]["rgb"],
            "bloom": tint,
            "bloomSel": [1.0 if i == warm else 0.0 for i in range(4)],
            "hex": [hexstr(c["rgb"]) for c in a],
        })

    tpl = EXPR_TEMPLATE.read_text()
    html = tpl.replace("{{PRODUCTS_JSON}}", json.dumps(out, indent=2))
    # Written as index.html so a bare /play-orb/ URL lands on the main board
    # rather than on the raw gradient comparison.
    (HERE / "index.html").write_text(html)
    return out


# ---------------------------------------------------------------------------

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    keep = "--keep-palettes" in sys.argv
    ids = args or DEFAULT_IDS

    if not TEMPLATE.exists():
        sys.exit("Missing template: %s" % TEMPLATE)

    if keep:
        if not PALETTES.exists():
            sys.exit("--keep-palettes given but %s does not exist" % PALETTES)
        palettes = json.loads(PALETTES.read_text())
        missing = [g for g in ids if g not in palettes]
        if missing:
            sys.exit("Not in palettes.json: %s" % ", ".join(missing))
        print("Reusing palettes.json")
    else:
        palettes = json.loads(PALETTES.read_text()) if PALETTES.exists() else {}
        for gid in ids:
            src = GRADIENT_DIR / ("%s.png" % gid)
            if not src.exists():
                sys.exit("Gradient not found: %s" % src)
            palettes[gid] = extract(src)
            swatch = " ".join(hexstr(c["rgb"]) for c in palettes[gid]["anchors"])
            print("  %-8s %s  shade %s"
                  % (gid, swatch, hexstr(palettes[gid]["shade"]["rgb"])))
        PALETTES.write_text(json.dumps(palettes, indent=2) + "\n")
        print("Wrote %s" % PALETTES.name)

    template = TEMPLATE.read_text()
    ORB_DIR.mkdir(exist_ok=True)
    for gid in ids:
        out = ORB_DIR / ("%s.html" % gid)
        out.write_text(build_one(gid, palettes[gid], template))
        print("Wrote orbs/%s.html" % gid)

    (HERE / "compare.html").write_text(build_compare(ids, palettes))
    print("Wrote compare.html  (gradient comparison)")

    if EXPR_TEMPLATE.exists():
        prods = build_expressions(palettes)
        print("Wrote index.html  (expression board, %s: %s)"
              % (len(prods), ", ".join("%s=%s" % (p["name"], p["gradient"])
                                       for p in prods)))
    else:
        print("Skipped expression board (no %s)" % EXPR_TEMPLATE.name)


if __name__ == "__main__":
    main()
