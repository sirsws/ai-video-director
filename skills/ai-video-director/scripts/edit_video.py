#!/usr/bin/env python3
"""Deterministic local trim/concat/captions/audio placement. See post-production.md."""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def run(args: list[str], cwd: Path | None = None) -> str:
    result = subprocess.run(args, cwd=cwd, capture_output=True, text=True,
                            encoding="utf-8", errors="replace")
    if result.returncode:
        raise ValueError(f"Command failed ({result.returncode}):\n{result.stderr[-7000:]}")
    return result.stdout


def number(value, name: str, minimum: float = 0) -> float:
    value = float(value)
    if not math.isfinite(value) or value < minimum:
        raise ValueError(f"{name} must be finite and >= {minimum}")
    return value


def keys(data: dict, allowed: set[str], where: str):
    if not isinstance(data, dict):
        raise ValueError(f"{where} must be an object")
    unknown = set(data) - allowed
    if unknown:
        raise ValueError(f"{where}: unknown fields {sorted(unknown)}")


def resolve_file(value: str, base: Path) -> Path:
    path = Path(value)
    path = (base / path if not path.is_absolute() else path).resolve(strict=True)
    if not path.is_file():
        raise ValueError(f"Not a file: {path}")
    return path


def probe(path: Path) -> dict:
    return json.loads(run(["ffprobe", "-v", "error", "-show_streams", "-show_format",
                           "-of", "json", str(path)]))


def media_duration(info: dict) -> float:
    duration = info.get("format", {}).get("duration")
    if duration is None:
        duration = max(float(s.get("duration", 0)) for s in info["streams"])
    return number(duration, "media duration")


def stream(info: dict, kind: str) -> dict | None:
    return next((s for s in info["streams"] if s["codec_type"] == kind), None)


def audio_duration(info: dict) -> float:
    """Use the selected audio stream's own extent, never the container length."""
    audio = stream(info, "audio")
    if audio is None:
        raise ValueError("No selected audio stream")
    if audio.get("duration_ts") not in (None, "N/A") and audio.get("time_base"):
        duration = float(Fraction(str(audio["duration_ts"])) * Fraction(audio["time_base"]))
    elif audio.get("duration") not in (None, "N/A"):
        duration = float(audio["duration"])
    else:
        raise ValueError("Audio stream duration is unknown; use explicit FFmpeg verification")
    duration = number(duration, "audio stream duration")
    if duration <= 0:
        raise ValueError("Audio stream duration is unavailable; use explicit FFmpeg verification")
    return duration


def fps_of(video: dict) -> Fraction:
    return Fraction(video.get("avg_frame_rate") or video["r_frame_rate"])


def geometry(video: dict) -> tuple[int, int]:
    width, height = video["width"], video["height"]
    rotation = next((d.get("rotation", 0) for d in video.get("side_data_list", [])
                     if "rotation" in d), 0)
    if int(rotation) % 180:
        width, height = height, width
    return width, height


def digest(path: Path) -> str:
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def video_frames(path: Path, video: dict, fps: Fraction) -> int:
    """Check actual decoded timestamps; average rate alone does not prove CFR."""
    info = json.loads(run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                           "-show_frames", "-show_entries",
                           "frame=best_effort_timestamp_time", "-of", "json", str(path)]))
    frames = info.get("frames", [])
    if not frames:
        raise ValueError(f"No readable video frames: {path}")
    tolerance = max(0.000001, float(Fraction(video["time_base"])) * 1.1)
    for i, frame in enumerate(frames):
        pts = number(frame["best_effort_timestamp_time"], "video frame timestamp")
        if abs(pts - float(i / fps)) > tolerance:
            raise ValueError(f"Irregular video timestamps need explicit FFmpeg mapping: {path}")
    return len(frames)


def execute(plan_path: Path, output: Path) -> dict:
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise ValueError("ffmpeg and ffprobe must be on PATH")
    plan_path = plan_path.resolve(strict=True)
    output = output.resolve()
    report_path = output.with_suffix(".edit.json")
    if output.suffix.lower() != ".mp4":
        raise ValueError("Use a new .mp4 output")
    if output.exists() or report_path.exists():
        raise ValueError("Output or its .edit.json already exists; choose a new version")
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    keys(plan, {"cuts", "size", "fps", "subtitles", "font_file", "font_size", "audio"},
         "plan")
    cuts = plan.get("cuts", [])
    if not isinstance(cuts, list) or not cuts:
        raise ValueError("cuts must be a non-empty list")
    base = plan_path.parent
    sources: dict[Path, dict] = {}
    source_frame_counts: dict[Path, int] = {}

    def source(value: str) -> tuple[Path, dict]:
        path = resolve_file(value, base)
        if path == output or path == report_path:
            raise ValueError("An output cannot replace source media")
        if path not in sources:
            info = probe(path)
            relevant = [s for s in info["streams"] if s["codec_type"] in ("audio", "video")]
            timed = [info.get("format", {}), *relevant]
            if any(abs(float(s.get("start_time", 0))) > 0.000001 for s in timed):
                raise ValueError(f"Non-zero source start_time needs explicit FFmpeg mapping: {path}")
            audios = [s for s in relevant if s["codec_type"] == "audio"]
            if len(audios) > 1 or any(int(s.get("channels", 0)) not in (1, 2) for s in audios):
                raise ValueError(f"Multiple audio streams or multichannel audio need explicit mapping: {path}")
            if sum(s["codec_type"] == "video" for s in relevant) > 1:
                raise ValueError(f"Multiple video streams need explicit mapping: {path}")
            sources[path] = info
        return path, sources[path]

    prepared = []
    for cut in cuts:
        keys(cut, {"source", "in", "out", "audio_gain"}, "cut")
        path, info = source(cut["source"])
        video = stream(info, "video")
        if video is None:
            raise ValueError(f"No video stream: {path}")
        if video.get("sample_aspect_ratio", "1:1") not in ("1:1", "N/A", "0:1"):
            raise ValueError("Non-square pixels require an explicit FFmpeg adaptation")
        source_fps = fps_of(video)
        nominal_fps = Fraction(video.get("r_frame_rate", str(source_fps)))
        if source_fps <= 0 or source_fps != nominal_fps:
            raise ValueError("Variable-rate footage needs a deliberate FFmpeg time mapping")
        if path not in source_frame_counts:
            source_frame_counts[path] = video_frames(path, video, source_fps)
        video_end = float(source_frame_counts[path] / source_fps)
        start = number(cut["in"], "cut in")
        end = number(cut["out"], "cut out")
        if end <= start or end > video_end + 0.000001:
            raise ValueError(f"Invalid cut interval {start}..{end}: {path}")
        # Editing is frame-based. Keep requested times in the report and snap
        # to the nearest source frame (half-frame ties go forward).
        start = float(math.floor(start * source_fps + 0.5) / source_fps)
        end = float(math.floor(end * source_fps + 0.5) / source_fps)
        if end <= start or end > video_end + 0.000001:
            raise ValueError("Cut is empty or beyond the source after frame alignment")
        prepared.append((path, info, video, start, end,
                         number(cut.get("audio_gain", 1), "audio_gain")))
    fps = Fraction(str(plan["fps"])) if "fps" in plan else fps_of(prepared[0][2])
    if fps <= 0 or fps > 240:
        raise ValueError("fps must be > 0 and <= 240")
    if any(fps_of(c[2]) != fps for c in prepared):
        raise ValueError("Different source/output frame rates need explicit FFmpeg time mapping")
    size = tuple(plan["size"]) if "size" in plan else geometry(prepared[0][2])
    if len(size) != 2 or any(not isinstance(x, int) or x < 2 or x % 2 for x in size):
        raise ValueError("size must be two positive even integers")
    if "size" not in plan and any(geometry(c[2]) != size for c in prepared):
        raise ValueError("Source sizes differ; choose size explicitly (fit with padding)")
    frame_counts = [round((c[4] - c[3]) * fps) for c in prepared]
    if any(n < 1 for n in frame_counts):
        raise ValueError("Every cut must contain at least one output frame")
    total = float(sum(frame_counts) / fps)
    subtitles = plan.get("subtitles", [])
    extras = plan.get("audio", [])
    font = None
    if subtitles:
        font = resolve_file(plan["font_file"], base)
    font_size = int(plan.get("font_size", round(size[1] * 0.055)))
    if font_size < 1:
        raise ValueError("font_size must be positive")
    for subtitle in subtitles:
        keys(subtitle, {"start", "end", "text"}, "subtitle")
        start = number(subtitle["start"], "subtitle start")
        end = number(subtitle["end"], "subtitle end")
        if end <= start or end > total + 0.001 or not isinstance(subtitle["text"], str):
            raise ValueError("Invalid subtitle text or interval")
    extra_inputs = []
    for extra in extras:
        keys(extra, {"source", "in", "out", "at", "gain"}, "audio")
        path, info = source(extra["source"])
        if stream(info, "audio") is None:
            raise ValueError(f"No audio stream: {path}")
        start, end = number(extra["in"], "audio in"), number(extra["out"], "audio out")
        at, gain = number(extra["at"], "audio at"), number(extra.get("gain", 1), "audio gain")
        if end <= start or end > audio_duration(info) + 0.000001 or at + end - start > total + 0.001:
            raise ValueError("Extra audio interval is outside source or output")
        extra_inputs.append((path, start, end, at, gain))
    audios = [stream(info, "audio") for info in sources.values() if stream(info, "audio")]
    rate = int(audios[0].get("sample_rate", 48000)) if audios else 48000
    channels = max(int(s["channels"]) for s in audios) if audios else 2
    layout = "mono" if channels == 1 else "stereo"
    before = {str(path): digest(path) for path in sources}
    output.parent.mkdir(parents=True, exist_ok=True)
    fps_text = str(fps)
    graph = []
    args = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin", "-n"]
    actual_cuts = []
    cursor = 0.0
    for i, (path, info, video, start, end, gain) in enumerate(prepared):
        args += ["-i", str(path)]
        duration = float(frame_counts[i] / fps)
        filters = (f"[{i}:v:0]trim=start_frame={round(start * fps)}:end_frame={round(end * fps)},"
                   f"setpts=PTS-STARTPTS,fps={fps_text}")
        if geometry(video) != size:
            filters += (f",scale={size[0]}:{size[1]}:force_original_aspect_ratio=decrease,"
                        f"pad={size[0]}:{size[1]}:(ow-iw)/2:(oh-ih)/2")
        # All sources share one constant frame rate; snapped source boundaries
        # give an integer frame span without adding holds or truncating a cut.
        filters += f",setpts=N/({fps_text}*TB)"
        graph.append(filters + f",setsar=1,format=yuv420p[v{i}]")
        audio_format = f"aresample={rate},aformat=channel_layouts={layout}"
        if stream(info, "audio"):
            graph.append(
                f"[{i}:a:0]aresample={rate}:async=1:first_pts=0,"
                f"atrim=start={start:.9f}:end={end:.9f},asetpts=PTS-STARTPTS,"
                f"{audio_format},volume={gain},apad,"
                f"atrim=duration={duration:.9f}[a{i}]")
        else:
            graph.append(f"anullsrc=r={rate}:cl={layout},atrim=duration={duration:.9f}[a{i}]")
        actual_cuts.append({"source": str(path), "in": start, "out": end,
                            "requested_in": cuts[i]["in"], "requested_out": cuts[i]["out"],
                            "timeline_start": cursor, "frames": frame_counts[i],
                            "timeline_duration": duration, "original_audio_gain": gain,
                            "source_has_audio": bool(stream(info, "audio"))})
        cursor += duration
    joined = "".join(f"[v{i}][a{i}]" for i in range(len(prepared)))
    graph.append(f"{joined}concat=n={len(prepared)}:v=1:a=1[video][original]")
    audio_labels = ["[original]"]
    for i, (path, start, end, at, gain) in enumerate(extra_inputs, len(prepared)):
        args += ["-i", str(path)]
        # Sample-based delay avoids millisecond rounding of intentionally placed sounds.
        delay = round(at * rate)
        graph.append(f"[{i}:a:0]atrim=start={start:.9f}:end={end:.9f},"
                     f"asetpts=PTS-STARTPTS,aresample={rate},"
                     f"aformat=channel_layouts={layout},volume={gain},"
                     f"adelay={delay}S:all=1[extra{i}]")
        audio_labels.append(f"[extra{i}]")
    graph.append("".join(audio_labels) +
                 f"amix=inputs={len(audio_labels)}:duration=first:normalize=0,"
                 f"atrim=duration={total:.9f}[audio]")
    with tempfile.TemporaryDirectory(prefix="next-edit-") as folder:
        scratch = Path(folder)
        video_label = "[video]"
        if font is not None:
            font_name = "font" + font.suffix
            shutil.copyfile(font, scratch / font_name)
            for i, subtitle in enumerate(subtitles):
                name = f"caption-{i}.txt"
                (scratch / name).write_text(subtitle["text"], encoding="utf-8")
                next_label = f"[caption{i}]"
                graph.append(
                    video_label + f"drawtext=fontfile='{font_name}':textfile='{name}':"
                    f"expansion=none:fontsize={font_size}:fontcolor=white:"
                    "box=1:boxcolor=black@0.5:boxborderw=8:x=(w-text_w)/2:y=h-text_h-h*0.08:"
                    f"enable='gte(t,{subtitle['start']})*lt(t,{subtitle['end']})'" + next_label)
                video_label = next_label
        graph_path = scratch / "filter.txt"
        graph_path.write_text(";\n".join(graph), encoding="utf-8")
        args += ["-filter_complex_script", str(graph_path), "-map", video_label,
                 "-map", "[audio]", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                 "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", str(rate),
                 "-frames:v", str(sum(frame_counts)), "-t", f"{total:.9f}",
                 "-movflags", "+faststart", str(output)]
        run(args, scratch)
    actual = probe(output)
    if abs(media_duration(actual) - total) > max(0.06, 1 / float(fps)):
        raise ValueError("Export duration differs from the edit plan; inspect output")
    actual_video_frames = video_frames(output, stream(actual, "video"), fps)
    if actual_video_frames != sum(frame_counts):
        raise ValueError("Export video frame count differs from the edit plan; inspect output")
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin", "-i",
         str(output), "-map", "0", "-f", "null", "-"])
    unchanged = all(digest(Path(path)) == value for path, value in before.items())
    report = {"output": str(output), "plan": str(plan_path), "cuts": actual_cuts,
              "expected_duration": total, "video_frame_count": actual_video_frames,
              "fps": fps_text, "size": size,
              "subtitles": subtitles, "additional_audio": extras,
              "source_sha256": before, "source_hashes_unchanged": unchanged,
              "output_probe": actual, "decoded_without_error": True,
              "visual_review": "not_performed_by_script",
              "subjective_audio_review": "not_performed_by_script",
              "audio_note": "Original audio follows cuts; no automatic loudness normalization or ducking."}
    with report_path.open("x", encoding="utf-8") as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    if not unchanged:
        raise ValueError("A source changed during execution; inspect before delivery")
    return {"output": str(output), "report": str(report_path), "duration": total,
            "decoded_without_error": True, "source_hashes_unchanged": unchanged}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path, help="UTF-8 JSON edit plan")
    parser.add_argument("output", type=Path, help="New MP4 path; never overwritten")
    args = parser.parse_args()
    try:
        print(json.dumps(execute(args.plan, args.output), ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError, ZeroDivisionError) as error:
        print(f"edit_video: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

