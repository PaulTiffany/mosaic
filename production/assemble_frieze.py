#!/usr/bin/env python3
"""Assemble 13 supplied still mural plates into ONE immutable master artwork.

No generative inference, animation, fake upscaling, or hidden seam repair.
Image files may be supplied by the creator's GPT Plan or any licensed artist.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def digest(path):
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            sha.update(block)
    return sha.hexdigest()


def check(manifest, assets_root=ROOT):
    from PIL import Image
    specs = manifest["assets"]
    width = manifest["layout"]["segment_px"]["width"]
    height = manifest["layout"]["segment_px"]["height"]
    rows = []
    for spec in specs:
        path = Path(assets_root) / spec["file"]
        if not path.is_file():
            raise FileNotFoundError(f"Missing supplied still-art plate: {path}")
        with Image.open(path) as img:
            actual = img.size
            if actual != (width, height):
                raise ValueError(
                    f"{spec['id']}: expected *native* {width}x{height}, got {actual}. "
                    "No silent stretch/crop/upscale."
                )
            if img.mode not in ("RGB", "RGBA"):
                raise ValueError(f"{spec['id']}: invalid pixel mode {img.mode}")
            img.verify()
        rows.append({"id": spec["id"], "path": str(path), "sha256": digest(path),
                     "native_px": [width, height]})
    if len({row["sha256"] for row in rows}) != len(rows):
        raise ValueError("Two mural plates are byte-identical; lyric-repeated choruses require new imagery.")
    return rows


def build(manifest, rows, output, seam_sheet=None):
    from PIL import Image, ImageDraw
    w, h = manifest["layout"]["segment_px"]["width"], manifest["layout"]["segment_px"]["height"]
    n = len(rows)
    expected_w = manifest["layout"]["master_px"]["width"]
    if n * w != expected_w:
        raise ValueError("Manifest target master width does not match plate count.")
    master = Image.new("RGB", (expected_w, h))
    seams = []
    previous = None
    for i, row in enumerate(rows):
        with Image.open(row["path"]) as im:
            tile = im.convert("RGB")
            master.paste(tile, (i * w, 0))
            if previous is not None:
                sample_h = min(480, h)
                band_w = min(110, w // 8)
                part = Image.new("RGB", (band_w * 2, sample_h))
                a = previous.crop((w-band_w, (h-sample_h)//2, w, (h+sample_h)//2))
                b = tile.crop((0, (h-sample_h)//2, band_w, (h+sample_h)//2))
                part.paste(a, (0, 0))
                part.paste(b, (band_w, 0))
                seams.append(part)
            previous = tile
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    master.save(output, optimize=True)
    inventory = {
        "type": "static-mural-master-v1",
        "dimensions": list(master.size),
        "master_sha256": digest(output),
        "plates": rows,
        "note": "Visually verify all joins. This script uses direct no-blend assembly."
    }
    receipt = output.with_suffix(".receipt.json")
    receipt.write_text(json.dumps(inventory, indent=2) + "\n", encoding="utf-8")
    print(f"ONE immutable artwork: {output} ({master.width}x{master.height})")
    print(f"Source hashes: {receipt}")
    if seam_sheet and seams:
        cols = min(6, len(seams))
        margin = 16
        rows_n = (len(seams) + cols - 1)//cols
        bw, bh = seams[0].size
        sheet = Image.new("RGB", (cols*(bw+margin)+margin, rows_n*(bh+margin+24)+margin),
                          (16, 16, 22))
        d = ImageDraw.Draw(sheet)
        for i, panel in enumerate(seams):
            x = margin+(i % cols)*(bw+margin)
            y = margin+(i // cols)*(bh+margin+24)
            sheet.paste(panel, (x, y))
            d.text((x, y+bh+3), f"JOIN {i:02}->{i+1:02}", fill=(225,220,205))
        sheet.save(seam_sheet)
        print(f"Review every fixed image join: {seam_sheet}")
    return inventory


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", type=Path, default=ROOT / "production" / "frieze_manifest.json")
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--output", type=Path, default=ROOT / "output" / "mosaic_master.png")
    ap.add_argument("--seam-sheet", type=Path, default=ROOT / "output" / "seam_sheet.jpg")
    ap.add_argument("--check-only", action="store_true")
    args = ap.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    rows = check(manifest, args.root)
    if args.check_only:
        print(f"Verified {len(rows)} static source plates, {len(set(x['sha256'] for x in rows))} unique.")
    else:
        build(manifest, rows, args.output, args.seam_sheet)


if __name__ == "__main__":
    main()
