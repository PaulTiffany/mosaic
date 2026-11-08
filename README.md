> **CURRENT FIRST DELIVERABLE — [VIEW ALL 106 STORYBOARD FRAMES](production/STORYBOARD_MAP.md)**. First inspect/edit the whole film's 106 line-specific scene map. Next, make **one image generation per lyric**, each outpainting to the RIGHT from a PIXEL-LOCKED overlap of the previous accepted image. [Full 106-job generation plan](production/LINE_GENERATION_PLAN.json). The previous suggestion to independently generate 13 chapter pictures or three pilot chapters was superseded. The 13 chapters are only organizational/rendering groups; final wall dimensions are provisional until per-line legibility is tested. The existing 13-plate assembler/Blender scaffold is NOT YET upgraded to consume 106 outpainted scenes.

# MOSAIC — one-dimensional lyric film inside a static 3D cathedral

**Creative baseline:** one finished panoramic mural, read from LEFT to RIGHT in the exact order of the sung lyrics. A photorealistic cathedral is **static geometry**. The **only animated thing is a real 3D camera** moving along the mural and pulling back at the end.

- [Listen to Suno take 1](https://suno.com/song/38f117cc-015a-4c44-98dd-cfae3f1acd89) — reference for current timing (4:36.56)
- **[THE ENTIRE SONG AS ONE STORYBOARD — 106 lyrics, 12 instrumental passages](production/FULL_SONG_STORYBOARD.md)** — master visual plan, with exact model-produced lyric timings and positions.
- [Machine-readable complete storyboard](production/FULL_SONG_STORYBOARD.json)
- [Lyric beats and exact Suno alignment times](production/take1_word_anchors.json) — 49 phrase occurrences recovered from Suno's word alignment.
- [Complete 13-chapter visual story](production/frieze_manifest.json) — each time range specifies what MUST be drawn, plus left/right scene continuity.
- [Provider-ready art prompts](production/ASSET_HANDOFF.md) — for your GPT Plan or another artist.
- [Creative baseline](production/LINEAR_BASELINE.md) — monotonic left-to-right, no backtracking, static painting.
- [Source interview and provenance](docs/PROVENANCE.md) — ML Street Talk conversation with Alex Imas.

## Honest status

**Real production scripts and automated checks exist. Finished mural imagery and a real cathedral render DO NOT yet exist.** The original square album cover is a palette/style reference, not a substitute for the 39-metre lyric story. We explicitly rejected the earlier animated tile collage and unrelated single-image cathedral collage.

This branch includes executable image assembly, a silent baseline 2D camera test, and a Blender 4.x scene-builder with a **blockout** cathedral. We have not claimed to run Blender in this environment or obtained any new image assets. The new art is to be supplied externally, possibly through the user's GPT Plan.

## Asset inputs (artist / GPT Plan)

First use [FULL_SONG_STORYBOARD.md](production/FULL_SONG_STORYBOARD.md) to make **ONE low-detail storyboard of the entire continuous 39-metre story, including all 106 moments**. Review its visual geography from beginning to end. **Only after this single full-song storyboard works**, use [ASSET_HANDOFF.md](production/ASSET_HANDOFF.md) to produce **13 adjacent, front-facing stills**, each native **3072×2048** px if the generation service can provide that genuine detail. If not, report the actual native dimensions; do not silently upscale.

Place each image at its exact path under `assets/incoming/`, according to `production/frieze_manifest.json`. The images must connect visually across their edges. They are **not** clips, sprites, renders of cathedral interiors, or standalone covers.

The logical master panorama is **39,936×2,048 px**, physically mapped to a **39 m × 2 m** wall. In Blender, the single static mesh uses 13 fixed material regions to avoid oversized GPU textures. This backend tiling is **not** an animation of individual tiles.

### Production commands

Run with Python 3.11+, Pillow, ffmpeg and (for the real cathedral shot) Blender 4.x:

```sh
python -m pip install "Pillow>=10,<13"
python -m unittest discover -s tests -v

# With all 13 creator-supplied plates at the declared locations:
python production/assemble_frieze.py --check-only
python production/assemble_frieze.py

# Quick SILENT story/camera check, without architecture:
python production/preview_side_scroll.py --guide
python production/preview_side_scroll.py --start 0 --end 48 --fps 12

# Blender must be installed externally. Creates an actual .blend with a
# one-way 3D camera moving over the still mosaic. Does NOT render a movie.
blender --background --python production/blender_cathedral.py -- \
  --save output/mosaic_cathedral_blockout.blend

# If you already have a photoreal static cathedral .glb:
blender --background --python production/blender_cathedral.py -- \
  --cathedral /path/to/cathedral.glb \
  --save output/mosaic_cathedral_asset.blend
```

The supplied cathedral must have its **mural wall at y≈0, facing negative Y**, in the scene's meter-scale coordinates, or be aligned before render. The generated geometry alone is a blockout, not a finished photoreal asset. The full song is only 3D-renderable after importing the actual art.

## Verifiability and rights

- `production/suno_take1_alignment.json` preserves the actual model-derived 655-word alignment, with success flags. It is **best effort**, to be spot-checked against singing.
- `production/take1_word_anchors.json` connects 49 distinct lyric occurrences to monotonic X positions. Repeated choruses occupy NEW mural territory.
- `production/assemble_frieze.py` refuses missing, wrong-sized or duplicate art; exports SHA-256 source and master receipts and a seam-review sheet.
- `tests/test_frieze_spec.py` verifies spatial direction, continuity, source timing and assembly via tiny colored **test fixtures**, which are NOT creative output.
- `output/` and `assets/incoming/` are ignored by Git by default. Record actual artist/model, license, source and cost for each imported asset.

No Suno download credits have been spent. No video publishing or Artilect submission has occurred. To satisfy Artilect later, upstream source projects used in the *actual production* must be credited and pinned as direct submodules.

**Goal:** the lyric tells the story, X tells the order, the still artwork carries the meaning, and the real 3D camera reveals it.
