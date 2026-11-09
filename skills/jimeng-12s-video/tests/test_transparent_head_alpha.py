from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

from PIL import Image

SCRIPTS = pathlib.Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from transparent_head_alpha import _point, build_mask, channel_values, composite_preview


class TransparentHeadAlphaTests(unittest.TestCase):
    def test_coordinate_boundaries_map_to_valid_edge_pixels(self) -> None:
        self.assertEqual(_point(0.0, 64, True), 0)
        self.assertEqual(_point(1.0, 64, True), 63)
        self.assertEqual(_point(63, 64, False), 63)
        with self.assertRaises(ValueError):
            _point(64, 64, False)

    def test_ellipse_mask_preserves_rgb(self) -> None:
        source = Image.new("RGBA", (64, 64), (120, 80, 40, 255))
        spec = {
            "coordinate_space": "normalized",
            "regions": [{"name": "head", "shape": "ellipse", "bbox": [0.25, 0.10, 0.75, 0.55]}],
        }
        source.putalpha(build_mask(64, 64, spec))
        values = set(channel_values(source.getchannel("A")))
        self.assertEqual((min(values), max(values)), (0, 255))
        self.assertEqual(source.convert("RGB").getpixel((0, 0)), (120, 80, 40))
        self.assertEqual(composite_preview(source, (0, 255, 0)).mode, "RGB")

    def test_polygon_mask(self) -> None:
        spec = {
            "coordinate_space": "pixel",
            "regions": [{"name": "head", "shape": "polygon", "points": [[8, 8], [24, 8], [16, 24]]}],
        }
        values = set(channel_values(build_mask(32, 32, spec)))
        self.assertEqual((min(values), max(values)), (0, 255))

    def test_invalid_coordinate_is_rejected(self) -> None:
        spec = {
            "coordinate_space": "normalized",
            "regions": [{"name": "bad", "shape": "ellipse", "bbox": [-0.1, 0.1, 0.5, 0.5]}],
        }
        with self.assertRaises(ValueError):
            build_mask(32, 32, spec)

    def test_cli_preserves_existing_alpha_and_writes_previews(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = pathlib.Path(temp_dir)
            input_path = root / "input.png"
            output_path = root / "output.png"
            spec_path = root / "mask.json"
            preview_dir = root / "previews" / "person-a"

            source = Image.new("RGBA", (32, 32), (120, 80, 40, 255))
            source.putpixel((0, 0), (120, 80, 40, 128))
            source.putpixel((1, 1), (120, 80, 40, 0))
            source.save(input_path)
            spec_path.write_text(json.dumps({
                "coordinate_space": "pixel",
                "regions": [{"name": "head", "shape": "ellipse", "bbox": [8, 4, 24, 20]}],
            }), encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "transparent_head_alpha.py"),
                    "--input", str(input_path),
                    "--output", str(output_path),
                    "--spec", str(spec_path),
                    "--preview-dir", str(preview_dir),
                ],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

            report = json.loads(result.stdout)
            output = Image.open(output_path).convert("RGBA")
            self.assertEqual(report["alpha_min"], 0)
            self.assertEqual(report["alpha_max"], 255)
            self.assertGreater(report["changed_pixels"], 0)
            self.assertEqual(output.getpixel((0, 0))[3], 128)
            self.assertEqual(output.getpixel((1, 1))[3], 0)
            self.assertEqual(output.getpixel((16, 12))[3], 0)
            for name in ("black", "white", "green"):
                self.assertTrue((preview_dir / f"{name}.png").is_file())

    def test_cli_rejects_mask_that_changes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = pathlib.Path(temp_dir)
            input_path = root / "input.png"
            output_path = root / "output.png"
            spec_path = root / "mask.json"
            spec = {
                "coordinate_space": "pixel",
                "regions": [{"name": "head", "shape": "ellipse", "bbox": [8, 4, 24, 20]}],
            }

            source = Image.new("RGBA", (32, 32), (120, 80, 40, 255))
            source.putalpha(build_mask(32, 32, spec))
            source.save(input_path)
            spec_path.write_text(json.dumps(spec), encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "transparent_head_alpha.py"),
                    "--input", str(input_path),
                    "--output", str(output_path),
                    "--spec", str(spec_path),
                ],
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("mask did not change alpha", result.stderr)
            self.assertFalse(output_path.exists())

    def test_cli_rejects_fully_transparent_result_without_touching_output(self) -> None:
        for output_exists in (False, True):
            with self.subTest(output_exists=output_exists), tempfile.TemporaryDirectory() as temp_dir:
                root = pathlib.Path(temp_dir)
                input_path = root / "input.png"
                output_path = root / "output.png"
                spec_path = root / "mask.json"
                Image.new("RGBA", (8, 8), (120, 80, 40, 255)).save(input_path)
                original_input = input_path.read_bytes()
                spec_path.write_text(json.dumps({
                    "coordinate_space": "normalized",
                    "regions": [{"shape": "polygon", "points": [[0, 0], [1, 0], [1, 1], [0, 1]]}],
                }), encoding="utf-8")
                if output_exists:
                    Image.new("RGBA", (8, 8), (10, 20, 30, 255)).save(output_path)
                    original_output = output_path.read_bytes()

                result = subprocess.run(
                    [sys.executable, str(SCRIPTS / "transparent_head_alpha.py"),
                     "--input", str(input_path), "--output", str(output_path), "--spec", str(spec_path)],
                    check=False, capture_output=True, text=True, encoding="utf-8",
                )

                self.assertNotEqual(result.returncode, 0)
                self.assertIn("alpha needs 0/255", result.stderr)
                self.assertEqual(input_path.read_bytes(), original_input)
                if output_exists:
                    self.assertEqual(output_path.read_bytes(), original_output)
                else:
                    self.assertFalse(output_path.exists())


if __name__ == "__main__":
    unittest.main()
