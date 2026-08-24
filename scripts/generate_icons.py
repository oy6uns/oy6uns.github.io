"""Generate the site's favicon / app-icon set: an "SB" monogram.

Design
------
The mark echoes the site: a circle (like the avatar and the theme toggle) in the
accent navy, with a tight "SB" monogram in Inter SemiBold. The dark-theme
favicon inverts to a light-blue disc with near-black letters so it stays legible
against a dark browser chrome. App icons (apple-touch / PWA) use a full-bleed
rounded square instead, since the OS supplies its own mask.

Requirements
------------
    pip install pillow fonttools brotli

The Inter TTF is built on the fly from the `@fontsource/inter` npm package if it
is not already present next to this script:

    npm pack @fontsource/inter@5

Then point --font at the extracted `inter-latin-600-normal.woff2`, or drop an
`Inter-SemiBold.ttf` in this directory.

Usage
-----
    python3 scripts/generate_icons.py [--font PATH]
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
HERE = Path(__file__).resolve().parent

SUPERSAMPLE = 8
TRACKING = -0.03  # em, tightens the pair the way the site's headings are tracked

NAVY = (47, 93, 138, 255)
SKY = (134, 179, 220, 255)
WHITE = (255, 255, 255, 255)
INK = (22, 24, 28, 255)

PALETTES = {
    # name:      (disc colour, letter colour, shape)
    "light": (NAVY, WHITE, "circle"),
    "dark": (SKY, INK, "circle"),
    "app": (NAVY, WHITE, "squircle"),
}

OUTPUTS = (
    ("favicon.png", 64, "light"),
    ("favicon-light.png", 64, "light"),
    ("favicon-dark.png", 64, "dark"),
    ("favicon-32x32.png", 32, "light"),
    ("favicon-16x16.png", 16, "light"),
    ("apple-touch-icon.png", 180, "app"),
    ("icon-192.png", 192, "app"),
    ("icon-512.png", 512, "app"),
)


def find_font(explicit: str | None) -> Path:
    candidates = []
    if explicit:
        candidates.append(Path(explicit))
    candidates += [
        HERE / "Inter-SemiBold.ttf",
        ROOT / "Inter-SemiBold.ttf",
        Path("/tmp/Inter-SemiBold.ttf"),
    ]
    for candidate in candidates:
        if candidate.suffix in {".woff", ".woff2"} and candidate.exists():
            from fontTools.ttLib import TTFont

            out = HERE / "Inter-SemiBold.ttf"
            font = TTFont(str(candidate))
            font.flavor = None
            font.save(str(out))
            return out
        if candidate.exists():
            return candidate
    raise SystemExit(
        "Inter SemiBold not found. See the module docstring for how to fetch it, "
        "then pass --font."
    )


def draw_mark(size: int, palette_name: str, font_path: Path) -> Image.Image:
    disc, letters, shape = PALETTES[palette_name]
    canvas = size * SUPERSAMPLE
    image = Image.new("RGBA", (canvas, canvas), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    if shape == "circle":
        # A hair of inset keeps the antialiased edge off the very last pixel.
        inset = max(1, canvas // 64)
        draw.ellipse((inset, inset, canvas - inset - 1, canvas - inset - 1), fill=disc)
        cap_fraction = 0.42
    else:
        radius = round(canvas * 0.22)
        draw.rounded_rectangle((0, 0, canvas - 1, canvas - 1), radius=radius, fill=disc)
        cap_fraction = 0.40

    # Size the type by cap height so every icon reads identically.
    probe = ImageFont.truetype(str(font_path), 100)
    cap_at_100 = probe.getbbox("H")[3] - probe.getbbox("H")[1]
    px = round(100 * canvas * cap_fraction / cap_at_100)
    font = ImageFont.truetype(str(font_path), px)

    tracking = round(px * TRACKING)
    glyphs = "SB"
    widths = [draw.textlength(ch, font=font) for ch in glyphs]
    total = sum(widths) + tracking * (len(glyphs) - 1)

    # Centre on the cap-height box, not on the font's line box.
    box = font.getbbox(glyphs)
    x = (canvas - total) / 2
    y = (canvas - (box[3] - box[1])) / 2 - box[1]

    for ch, advance in zip(glyphs, widths):
        draw.text((x, y), ch, font=font, fill=letters)
        x += advance + tracking

    return image.resize((size, size), Image.LANCZOS)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--font", help="Path to Inter SemiBold (.ttf/.woff2)")
    args = parser.parse_args()

    font_path = find_font(args.font)
    ASSETS.mkdir(exist_ok=True)
    for filename, size, palette in OUTPUTS:
        draw_mark(size, palette, font_path).save(ASSETS / filename)
        print(f"wrote assets/{filename} ({size}px, {palette})")


if __name__ == "__main__":
    main()
