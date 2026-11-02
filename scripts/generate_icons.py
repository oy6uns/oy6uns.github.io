"""Resample the site's favicon / app-icon set from a single master image.

The mark itself lives in `assets/icon-master.png` (512x512, RGBA, with the
rounded-square plate already drawn and the corners transparent). This script
only resizes it, so editing the master is the way to change the icon.

App icons (apple-touch / PWA) are flattened onto the plate colour because iOS
applies its own rounded mask and renders leftover alpha as black corners.

Usage:
    python3 scripts/generate_icons.py
"""

from __future__ import annotations

import pathlib

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
MASTER = ASSETS / "icon-master.png"

PLATE = (24, 33, 52, 255)  # navy of the mark's plate, sampled from the master

OUTPUTS = (
    # filename,                size, flatten onto the plate colour
    ("favicon.png", 64, False),
    ("favicon-light.png", 64, False),
    ("favicon-dark.png", 64, False),
    ("favicon-32x32.png", 32, False),
    ("favicon-16x16.png", 16, False),
    ("apple-touch-icon.png", 180, True),
    ("icon-192.png", 192, True),
    ("icon-512.png", 512, True),
)


def main() -> None:
    if not MASTER.exists():
        raise SystemExit(f"master icon not found: {MASTER}")

    master = Image.open(MASTER).convert("RGBA")

    for name, size, flatten in OUTPUTS:
        image = master.resize((size, size), Image.LANCZOS)
        if flatten:
            plate = Image.new("RGBA", (size, size), PLATE)
            plate.alpha_composite(image)
            image = plate
        image.save(ASSETS / name, optimize=True)
        print(f"wrote assets/{name} ({size}px)")


if __name__ == "__main__":
    main()
