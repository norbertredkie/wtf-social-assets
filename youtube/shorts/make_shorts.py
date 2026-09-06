#!/usr/bin/env python3
"""Deterministic, zero-spend Shorts builder for wtf.life (Rule 30: local tools only).

Three derivations, all from bytes already ratified for Instagram:

  reel     <date>-igr-*/igr-*.mp4          -> passthrough (already 1080x1920, <=3 min)
  stories  <date>-igs-*/igs-*-{1..4}.mp4   -> concat 1..4 in order (stream copy, no re-encode)
  carousel <date>-ig-*/slide-{1..7}.mp4    -> concat + pad 1080x1350 -> 1080x1920 (re-encode)

Nothing here publishes. Output is a candidate file + a proof sidecar
(sha256 of output, sha256 of every input, duration, geometry) so the
S-15 gate (a different mechanism than the producer) can judge it.

Usage:
  make_shorts.py --list                      # what would be built
  make_shorts.py --build 2026-09-03-igs-0745 # one folder -> youtube/shorts/out/
  make_shorts.py --build-all                 # everything (~60 files, ~250 MB)
  make_shorts.py --check youtube/shorts/out/<file>.mp4   # re-verify a sidecar
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # repo root (wtf-social-assets)
OUT = Path(__file__).resolve().parent / "out"
SHORTS_MAX_S = 180.0                                  # YouTube Shorts hard cap (3 min)
TARGET_W, TARGET_H = 1080, 1920


def ffmpeg() -> str:
    exe = os.environ.get("FFMPEG")
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"


def ffprobe_json(path: Path) -> dict:
    """ffprobe is not always shipped with imageio-ffmpeg; parse ffmpeg -i instead."""
    out = subprocess.run([ffmpeg(), "-hide_banner", "-i", str(path)],
                         capture_output=True, text=True).stderr
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", out)
    dur = int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3]) if m else 0.0
    g = re.search(r"Video: .*?, (\d{3,4})x(\d{3,4})", out)
    a = "Audio:" in out
    return {"duration_s": round(dur, 2), "width": int(g[1]) if g else 0,
            "height": int(g[2]) if g else 0, "has_audio": a}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def classify(folder: Path) -> tuple[str, list[Path]] | None:
    name = folder.name
    mp4s = sorted(folder.glob("*.mp4"), key=lambda p: [int(t) if t.isdigit() else t
                                                         for t in re.split(r"(\d+)", p.name)])
    if not mp4s:
        return None
    if re.search(r"-igr-\d{4}", name) and len(mp4s) == 1:
        return "reel", mp4s
    if re.search(r"-igs-\d{4}", name) or "stories" in name:
        return "stories", mp4s
    if re.search(r"-ig-\d{4}", name) or "carousel" in name:
        return "carousel", mp4s
    return None


def plan() -> list[dict]:
    rows = []
    for folder in sorted(p for p in ROOT.iterdir() if p.is_dir() and p.name[:4] == "2026"):
        c = classify(folder)
        if not c:
            continue
        kind, files = c
        probes = [ffprobe_json(f) for f in files]
        total = round(sum(p["duration_s"] for p in probes), 2)
        geo = {(p["width"], p["height"]) for p in probes}
        rows.append({"folder": folder.name, "kind": kind, "inputs": [str(f.relative_to(ROOT)) for f in files],
                     "total_s": total, "geometries": sorted(geo), "audio": all(p["has_audio"] for p in probes),
                     "fits_shorts": total <= SHORTS_MAX_S})
    return rows


def build(folder_name: str) -> Path:
    folder = ROOT / folder_name
    c = classify(folder)
    if not c:
        raise SystemExit(f"{folder_name}: nothing to build")
    kind, files = c
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / f"{folder_name}-short.mp4"
    ff = ffmpeg()
    if kind == "reel":
        subprocess.run([ff, "-y", "-loglevel", "error", "-i", str(files[0]), "-c", "copy",
                        "-movflags", "+faststart", str(out)], check=True)
    else:
        lst = OUT / f"{folder_name}.concat.txt"
        lst.write_text("".join(f"file '{f.resolve()}'\n" for f in files))
        if kind == "stories":
            subprocess.run([ff, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
                            "-c", "copy", "-movflags", "+faststart", str(out)], check=True)
        else:  # carousel: 1080x1350 -> letterbox onto 1080x1920, keep audio
            vf = (f"scale={TARGET_W}:-2,pad={TARGET_W}:{TARGET_H}:(ow-iw)/2:(oh-ih)/2:color=0x0a0a0a,"
                  "format=yuv420p")
            subprocess.run([ff, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
                            "-vf", vf, "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "23", "-maxrate", "2500k", "-bufsize", "5000k",
                            "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", str(out)], check=True)
        lst.unlink()
    probe = ffprobe_json(out)
    proof = {
        "producer": "youtube/shorts/make_shorts.py", "kind": kind, "source_folder": folder_name,
        "inputs": [{"path": str(f.relative_to(ROOT)), "sha256": sha256(f)} for f in files],
        "output": str(out.relative_to(ROOT)), "video_sha256": sha256(out), **probe,
        "geometry_ok": (probe["width"], probe["height"]) == (TARGET_W, TARGET_H),
        "duration_ok": probe["duration_s"] <= SHORTS_MAX_S, "has_audio": probe["has_audio"],
        "spend_usd": 0.0,
        # S-15: geometry is never acceptance. These flags are preconditions only;
        # a vision/audio gate run by a different mechanism must still pass.
        "acceptance": "PRECONDITIONS_ONLY",
    }
    out.with_suffix(".json").write_text(json.dumps(proof, indent=1, ensure_ascii=False))
    return out


def check(path: Path) -> int:
    side = path.with_suffix(".json")
    if not side.exists():
        print("no sidecar"); return 2
    proof = json.loads(side.read_text())
    ok = proof["video_sha256"] == sha256(path)
    print(f"{path.name}: hash {'OK' if ok else 'MISMATCH'}, {proof['duration_s']}s, "
          f"{proof['width']}x{proof['height']}, audio={proof['has_audio']}")
    return 0 if ok and proof["geometry_ok"] and proof["duration_ok"] and proof["has_audio"] else 1


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--build")
    ap.add_argument("--build-all", action="store_true")
    ap.add_argument("--check")
    a = ap.parse_args()
    if a.list:
        for r in plan():
            print(f"{r['folder']:<48} {r['kind']:<8} {r['total_s']:>7.1f}s  {r['geometries']}  "
                  f"audio={r['audio']}  shorts={'OK' if r['fits_shorts'] else 'TOO LONG'}")
    elif a.build:
        print(build(a.build))
    elif a.build_all:
        for r in plan():
            if r["fits_shorts"]:
                print(build(r["folder"]))
    elif a.check:
        sys.exit(check(Path(a.check)))
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
