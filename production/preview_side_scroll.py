#!/usr/bin/env python3
"""Silent 2D validation of one-way camera traversal over ONE static mural master.

This is NOT the cathedral render: it tests lyric sequence and frame legibility.
No text overlays, scene cuts, object movement, or dynamically modified image.
"""
import argparse
import json
import math
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent.parent


def x_for_song_time(t, manifest):
    """Monotonic story X; first 268.252s pan, final seconds hold for 3D pullback."""
    assets = manifest["assets"]
    end = manifest["horizontal_story_end_s"]
    t = min(max(float(t), 0.0), end)
    for i, panel in enumerate(assets):
        if t < panel["end_s"] or i == len(assets)-1:
            duration = panel["end_s"] - panel["start_s"]
            ratio = min(1.0, max(0.0, (t-panel["start_s"]) / duration))
            return (i + ratio) / len(assets)
    return 1.0


def current_panel(t, manifest):
    for p in manifest["assets"]:
        if t < p["end_s"]:
            return p
    return manifest["assets"][-1]


def render(args, manifest):
    from PIL import Image
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg is needed to encode MP4 (no audio is included).")
    with Image.open(args.master) as source:
        expected = manifest["layout"]["master_px"]
        if source.size != (expected["width"], expected["height"]):
            raise ValueError(f"Master must be {expected['width']}x{expected['height']}, got {source.size}")
        source = source.convert("RGB")
    width, height = map(int, args.size.lower().split("x"))
    if width % 2 or height % 2 or not (width>0 and height>0):
        raise ValueError("H.264 preview output size must be even positive dimensions.")
    if args.end <= args.start or args.start < 0 or args.end > manifest["song_duration_s"]+0.0001:
        raise ValueError("Choose a positive interval inside the song duration.")
    # Fixed framing in world/image coordinates; no animated surface.
    crop_h = int(source.height * 0.73)
    crop_w = round(crop_h * width / height)
    if crop_w >= source.width:
        raise ValueError("Art master is not wide enough for side-scrolling camera framing.")
    crop_h = int(crop_w * height / width)
    x_half = crop_w // 2
    y0 = (source.height-crop_h)//2
    output=Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    cmd=[
        "ffmpeg","-y","-loglevel","error",
        "-f","rawvideo","-pixel_format","rgb24",
        "-video_size",f"{width}x{height}",
        "-framerate",str(args.fps),"-i","-",
        "-an","-c:v","libx264","-preset","veryfast",
        "-crf","21","-pix_fmt","yuv420p",str(output)
    ]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    frames=math.ceil((args.end-args.start)*args.fps)
    try:
        for i in range(frames):
            t=args.start+i/args.fps
            u=x_for_song_time(t,manifest)
            cx=int(round(u*(source.width-1)))
            cx=min(max(x_half,cx),source.width-(crop_w-x_half))
            frame=source.crop((cx-x_half,y0,cx-x_half+crop_w,y0+crop_h))
            if frame.size != (width,height):
                frame=frame.resize((width,height),Image.Resampling.LANCZOS)
            proc.stdin.write(frame.tobytes())
    finally:
        if proc.stdin:
            proc.stdin.close()
        err=proc.stderr.read().decode("utf-8",errors="replace") if proc.stderr else ""
        result=proc.wait()
    if result!=0:
        raise RuntimeError(f"ffmpeg failed with exit {result}: {err[-2000:]}")
    print(f"Rendered silent ONE-DIRECTION 2D inspection: {output}")
    print("Not a photoreal cathedral. All story imagery remains static.")


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--manifest",type=Path,default=ROOT/"production"/"frieze_manifest.json")
    ap.add_argument("--master",type=Path,default=ROOT/"output"/"mosaic_master.png")
    ap.add_argument("--start",type=float,default=0.0)
    ap.add_argument("--end",type=float,default=48.0)
    ap.add_argument("--fps",type=float,default=12.0)
    ap.add_argument("--size",default="1280x720")
    ap.add_argument("--output",default=str(ROOT/"output"/"side_scroll_silent.mp4"))
    ap.add_argument("--guide",action="store_true",help="Show all lyric-linked image locations; do not render.")
    args=ap.parse_args()
    m=json.loads(args.manifest.read_text(encoding="utf-8"))
    if args.guide:
        print("Time (s) | mural X | lyric / visible scene")
        for p in m["assets"]:
            center=(p["start_s"]+p["end_s"])/2
            u=x_for_song_time(center,m)
            print(f"{center:8.2f} | {u:7.3f} | {p['lyrics'][0]} -> {p['id']}")
        return
    if args.fps<=0 or args.fps>120:
        ap.error("--fps must be in (0, 120]")
    render(args,m)


if __name__=="__main__":
    main()
