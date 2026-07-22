"""Generate the site's terminal-inspired favicon set using only the standard library."""

from __future__ import annotations

import binascii
import struct
import zlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
SUPERSAMPLE = 4

GLYPHS = {
    "S": (
        "11111",
        "10000",
        "10000",
        "11111",
        "00001",
        "00001",
        "11111",
    ),
    "B": (
        "11110",
        "10001",
        "10001",
        "11110",
        "10001",
        "10001",
        "11110",
    ),
}

PALETTES = {
    "light": {
        "background": (247, 244, 236, 255),
        "border": (210, 204, 192, 255),
        "s": (190, 91, 69, 255),
        "b": (48, 49, 47, 255),
    },
    "dark": {
        "background": (21, 21, 18, 255),
        "border": (68, 66, 58, 255),
        "s": (223, 146, 126, 255),
        "b": (243, 239, 229, 255),
    },
}


def inside_rounded_rect(x: int, y: int, size: int, inset: int, radius: int) -> bool:
    left = inset
    top = inset
    right = size - inset - 1
    bottom = size - inset - 1
    if not (left <= x <= right and top <= y <= bottom):
        return False

    inner_left = left + radius
    inner_right = right - radius
    inner_top = top + radius
    inner_bottom = bottom - radius
    if inner_left <= x <= inner_right or inner_top <= y <= inner_bottom:
        return True

    cx = inner_left if x < inner_left else inner_right
    cy = inner_top if y < inner_top else inner_bottom
    return (x - cx) ** 2 + (y - cy) ** 2 <= radius**2


def fill_rounded_rect(
    pixels: bytearray,
    size: int,
    inset: int,
    radius: int,
    color: tuple[int, int, int, int],
) -> None:
    for y in range(size):
        for x in range(size):
            if inside_rounded_rect(x, y, size, inset, radius):
                offset = (y * size + x) * 4
                pixels[offset : offset + 4] = bytes(color)


def fill_rect(
    pixels: bytearray,
    size: int,
    x: int,
    y: int,
    width: int,
    height: int,
    color: tuple[int, int, int, int],
) -> None:
    row = bytes(color) * width
    for py in range(y, y + height):
        start = (py * size + x) * 4
        pixels[start : start + len(row)] = row


def draw_glyph(
    pixels: bytearray,
    size: int,
    glyph: tuple[str, ...],
    x: int,
    y: int,
    scale: int,
    color: tuple[int, int, int, int],
) -> None:
    for row_index, row in enumerate(glyph):
        for column_index, cell in enumerate(row):
            if cell == "1":
                fill_rect(
                    pixels,
                    size,
                    x + column_index * scale,
                    y + row_index * scale,
                    scale,
                    scale,
                    color,
                )


def downsample(pixels: bytearray, source_size: int, target_size: int) -> bytearray:
    factor = source_size // target_size
    result = bytearray(target_size * target_size * 4)
    area = factor * factor
    for y in range(target_size):
        for x in range(target_size):
            totals = [0, 0, 0, 0]
            for sy in range(y * factor, (y + 1) * factor):
                for sx in range(x * factor, (x + 1) * factor):
                    offset = (sy * source_size + sx) * 4
                    for channel in range(4):
                        totals[channel] += pixels[offset + channel]
            target = (y * target_size + x) * 4
            result[target : target + 4] = bytes(value // area for value in totals)
    return result


def png_chunk(kind: bytes, data: bytes) -> bytes:
    return (
        struct.pack(">I", len(data))
        + kind
        + data
        + struct.pack(">I", binascii.crc32(kind + data) & 0xFFFFFFFF)
    )


def write_png(path: Path, size: int, pixels: bytearray) -> None:
    rows = b"".join(
        b"\x00" + bytes(pixels[y * size * 4 : (y + 1) * size * 4])
        for y in range(size)
    )
    payload = b"\x89PNG\r\n\x1a\n"
    payload += png_chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0))
    payload += png_chunk(b"IDAT", zlib.compress(rows, level=9))
    payload += png_chunk(b"IEND", b"")
    path.write_bytes(payload)


def generate_icon(path: Path, target_size: int, palette_name: str) -> None:
    size = target_size * SUPERSAMPLE
    palette = PALETTES[palette_name]
    pixels = bytearray(size * size * 4)

    border = max(SUPERSAMPLE, target_size // 32 * SUPERSAMPLE)
    radius = round(target_size * 0.22) * SUPERSAMPLE
    fill_rounded_rect(pixels, size, 0, radius, palette["border"])
    fill_rounded_rect(
        pixels,
        size,
        border,
        max(SUPERSAMPLE, radius - border),
        palette["background"],
    )

    glyph_scale = max(1, target_size // 14) * SUPERSAMPLE
    gap = glyph_scale
    glyph_width = 5 * glyph_scale
    total_width = glyph_width * 2 + gap
    glyph_height = 7 * glyph_scale
    start_x = (size - total_width) // 2
    start_y = (size - glyph_height) // 2
    draw_glyph(pixels, size, GLYPHS["S"], start_x, start_y, glyph_scale, palette["s"])
    draw_glyph(
        pixels,
        size,
        GLYPHS["B"],
        start_x + glyph_width + gap,
        start_y,
        glyph_scale,
        palette["b"],
    )

    write_png(path, target_size, downsample(pixels, size, target_size))


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    outputs = (
        ("favicon.png", 64, "light"),
        ("favicon-light.png", 64, "light"),
        ("favicon-dark.png", 64, "dark"),
        ("favicon-32x32.png", 32, "light"),
        ("favicon-16x16.png", 16, "light"),
        ("apple-touch-icon.png", 180, "dark"),
        ("icon-192.png", 192, "dark"),
        ("icon-512.png", 512, "dark"),
    )
    for filename, size, palette in outputs:
        generate_icon(ASSETS / filename, size, palette)


if __name__ == "__main__":
    main()
