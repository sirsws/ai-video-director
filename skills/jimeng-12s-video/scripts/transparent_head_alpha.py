#!/usr/bin/env python3
"""Write a deterministic transparent head mask into a selected PNG."""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw


def _point(value: float, size: int, normalized: bool) -> int:
    upper = 1 if normalized else size - 1
    if not 0 <= value <= upper:
        raise ValueError(f"coordinate {value} outside 0..{upper}")
    return round(value * (size - 1)) if normalized else round(value)


def _draw_ellipse(draw: ImageDraw.ImageDraw, region: dict, size: tuple[int, int], normalized: bool) -> None:
    bbox = region.get("bbox")
    if not isinstance(bbox, list) or len(bbox) != 4:
        raise ValueError("ellipse requires bbox")
    x0, y0, x1, y1 = bbox
    if x0 >= x1 or y0 >= y1:
        raise ValueError("ellipse bbox order invalid")
    width, height = size
    pixels = (
        _point(x0, width, normalized),
        _point(y0, height, normalized),
        _point(x1, width, normalized),
        _point(y1, height, normalized),
    )
    draw.ellipse(pixels, fill=0)


def _draw_polygon(draw: ImageDraw.ImageDraw, region: dict, size: tuple[int, int], normalized: bool) -> None:
    points = region.get("points")
    if not isinstance(points, list) or len(points) < 3:
        raise ValueError("polygon requires three points")
    width, height = size
    pixels = [
        (_point(x, width, normalized), _point(y, height, normalized))
        for x, y in points
    ]
    draw.polygon(pixels, fill=0)


DRAWERS = {
    "ellipse": _draw_ellipse,
    "polygon": _draw_polygon,
}


def build_mask(width: int, height: int, spec: dict) -> Image.Image:
    coordinate_space = spec.get("coordinate_space", "normalized")
    if coordinate_space not in {"normalized", "pixel"}:
        raise ValueError("coordinate_space must be normalized/pixel")
    regions = spec.get("regions")
    if not isinstance(regions, list) or not regions:
        raise ValueError("regions cannot be empty")

    mask = Image.new("L", (width, height), 255)
    draw = ImageDraw.Draw(mask)
    for region in regions:
        drawer = DRAWERS.get(region.get("shape"))
        if drawer is None:
            raise ValueError(f"unsupported shape: {region.get('shape')!r}")
        drawer(draw, region, (width, height), coordinate_space == "normalized")
    return mask


def channel_values(channel: Image.Image) -> list:
    getter = getattr(channel, "get_flattened_data", None)
    return list(getter()) if getter else list(channel.getdata())


def composite_preview(rgba: Image.Image, color: tuple[int, int, int]) -> Image.Image:
    background = Image.new("RGB", rgba.size, color)
    background.paste(rgba.convert("RGB"), mask=rgba.getchannel("A"))
    return background


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--spec", required=True, type=Path)
    parser.add_argument("--preview-dir", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = args.input.resolve()
    output_path = args.output.resolve()
    if input_path == output_path:
        raise SystemExit("paths must differ")
    if output_path.suffix.lower() != ".png":
        raise SystemExit("output must be PNG")

    spec = json.loads(args.spec.read_text(encoding="utf-8"))
    source = Image.open(input_path).convert("RGBA")
    original_rgb = source.convert("RGB")
    original_alpha = source.getchannel("A")
    head_mask = build_mask(source.width, source.height, spec)
    updated_alpha = ImageChops.multiply(original_alpha, head_mask)
    alpha_diff = ImageChops.difference(original_alpha, updated_alpha)
    changed_pixels = source.width * source.height - alpha_diff.histogram()[0]
    if changed_pixels == 0:
        raise SystemExit("mask did not change alpha")
    if updated_alpha.getextrema() != (0, 255):
        raise SystemExit("alpha needs 0/255")
    source.putalpha(updated_alpha)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=output_path.parent, suffix=".png", delete=False) as staging:
        staged_path = Path(staging.name)
    try:
        source.save(staged_path)
        with Image.open(staged_path) as encoded:
            verified = encoded.convert("RGBA")
        alpha_values = channel_values(verified.getchannel("A"))
        values = set(alpha_values)
        if 0 not in values or 255 not in values:
            raise SystemExit("alpha needs 0/255")
        if channel_values(verified.convert("RGB")) != channel_values(original_rgb):
            raise SystemExit("RGB changed")
        staged_path.replace(output_path)
    finally:
        staged_path.unlink(missing_ok=True)

    if args.preview_dir:
        preview_dir = args.preview_dir.resolve()
        preview_dir.mkdir(parents=True, exist_ok=True)
        colors = {"black": (0, 0, 0), "white": (255, 255, 255), "green": (0, 255, 0)}
        for name, color in colors.items():
            composite_preview(verified, color).save(preview_dir / f"{name}.png")

    print(json.dumps({
        "output": str(output_path),
        "mode": verified.mode,
        "size": list(verified.size),
        "alpha_min": min(values),
        "alpha_max": max(values),
        "transparent_pixels": alpha_values.count(0),
        "changed_pixels": changed_pixels,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
