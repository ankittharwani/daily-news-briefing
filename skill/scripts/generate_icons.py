#!/usr/bin/env python3
"""
Generates the site's favicon / apple-touch-icon / manifest icon set: a serif
"A" mark on the masthead's ink color, matching Ankit's Morning Briefing's
typography (Georgia/Times-style serif headline face). Run once (or whenever
the mark needs a redesign) and commit the output — these are static assets,
not rebuilt per edition.

Usage:
    python3 generate_icons.py --out-dir site/public

Outputs into --out-dir:
    favicon.svg              scalable, used by modern browsers
    favicon-16.png           legacy 16x16 <link> favicon
    favicon-32.png           legacy 32x32 <link> favicon
    favicon.ico              multi-res (16/32/48) for very old browsers
    apple-touch-icon.png     180x180, opaque, for iOS "Add to Home Screen"
    favicon-192.png          Android/manifest icon
    favicon-512.png          Android/manifest icon (maskable-safe padding)
    site.webmanifest         name/icons for Android "Add to Home Screen"
"""
import argparse
import os

from PIL import Image, ImageDraw, ImageFont

INK = "#2E2C27"
MARK = "#F9F9F7"  # matches --wash, a warm off-white, echoes the masthead-on-wash look
WHITE = "#FCFCFB"

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
]


def find_font():
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            return p
    raise RuntimeError("No serif bold font found; install liberation-fonts or dejavu-fonts.")


def render_master(size=1024, corner_ratio=0.22):
    """Renders the mark at high resolution; every other size is downsampled from this."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    radius = int(size * corner_ratio)
    draw.rounded_rectangle([(0, 0), (size - 1, size - 1)], radius=radius, fill=INK)

    font_path = find_font()
    # Binary-search a font size so the "A" glyph's own bounding box fills a
    # consistent, generous fraction of the canvas (bold serif caps render
    # visually smaller than their point size suggests).
    target = size * 0.62
    lo, hi = 10, int(size * 1.4)
    best = lo
    while lo <= hi:
        mid = (lo + hi) // 2
        font = ImageFont.truetype(font_path, mid)
        bbox = draw.textbbox((0, 0), "A", font=font)
        h = bbox[3] - bbox[1]
        if h <= target:
            best = mid
            lo = mid + 1
        else:
            hi = mid - 1
    font = ImageFont.truetype(font_path, best)
    bbox = draw.textbbox((0, 0), "A", font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (size - w) / 2 - bbox[0]
    y = (size - h) / 2 - bbox[1]
    draw.text((x, y), "A", font=font, fill=MARK)
    return img


def flatten_on(img, bg):
    """Composites an RGBA image onto an opaque background (Apple touch icons
    must not carry alpha, or iOS renders a black-filled icon)."""
    flat = Image.new("RGB", img.size, bg)
    flat.paste(img, mask=img.split()[3])
    return flat


def write_ico(master, path, sizes=(16, 32, 48)):
    imgs = [master.resize((s, s), Image.LANCZOS) for s in sizes]
    imgs[0].save(path, format="ICO", sizes=[(s, s) for s in sizes], append_images=imgs[1:])


def write_svg(path):
    # A hand-written vector twin of the raster mark, for browsers that prefer
    # an SVG favicon (crisp at any size, incl. the retina tab-strip render).
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" rx="14" fill="{INK}"/>
  <text x="32" y="46" text-anchor="middle"
        font-family="Georgia, 'Times New Roman', Times, serif" font-weight="700"
        font-size="38" fill="{MARK}">A</text>
</svg>
'''
    with open(path, "w") as f:
        f.write(svg)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)

    master = render_master(1024)

    # Legacy <link> favicons and the .ico fallback can keep transparency.
    master.resize((16, 16), Image.LANCZOS).save(os.path.join(args.out_dir, "favicon-16.png"))
    master.resize((32, 32), Image.LANCZOS).save(os.path.join(args.out_dir, "favicon-32.png"))
    write_ico(master, os.path.join(args.out_dir, "favicon.ico"))
    write_svg(os.path.join(args.out_dir, "favicon.svg"))

    # iOS requires an opaque apple-touch-icon (transparency renders as black).
    touch = flatten_on(master, INK).resize((180, 180), Image.LANCZOS)
    touch.save(os.path.join(args.out_dir, "apple-touch-icon.png"))

    # Android/manifest sizes — also opaque, for the same reason on some launchers.
    flatten_on(master, INK).resize((192, 192), Image.LANCZOS).save(
        os.path.join(args.out_dir, "favicon-192.png"))
    flatten_on(master, INK).resize((512, 512), Image.LANCZOS).save(
        os.path.join(args.out_dir, "favicon-512.png"))

    manifest = f'''{{
  "name": "Ankit's Morning Briefing",
  "short_name": "Morning Briefing",
  "start_url": ".",
  "display": "standalone",
  "background_color": "{WHITE}",
  "theme_color": "{INK}",
  "icons": [
    {{"src": "favicon-192.png", "sizes": "192x192", "type": "image/png"}},
    {{"src": "favicon-512.png", "sizes": "512x512", "type": "image/png"}}
  ]
}}
'''
    with open(os.path.join(args.out_dir, "site.webmanifest"), "w") as f:
        f.write(manifest)

    print(f"Wrote icon set to {args.out_dir}")


if __name__ == "__main__":
    main()
