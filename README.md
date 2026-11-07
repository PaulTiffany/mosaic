# MOSAIC — composable music-video proof of concept

Source work: [Machine Learning Street Talk interview with Alex Imas](https://www.youtube.com/watch?v=cB1GNO95iog).
Song: [MOSAIC (Whose Windows Glow?) — Suno take 1](https://suno.com/song/38f117cc-015a-4c44-98dd-cfae3f1acd89).

This is a first executable **silent visual animatic**, not a completed music video. Its visual elements reuse the original custom cover art, and its cues track Suno-provided section/word timing for take 1. We have not downloaded, uploaded, or embedded the audio. You can swap in the other Suno take by regenerating the timing map from that take's alignment.

## Files

- `assets/cover.png` — original artwork and current tile atlas (**not yet committed; see assets/README.md**).
- `sequence.json` — full-song scene/cue and interview provenance map.
- `render.py` — deterministic OpenCV tile animation and continuous camera for the opening.
- `outputs/intro_animatic_silent.mp4` — first rendered film proof (no audio; in local prototype bundle, ignored by Git).
- `outputs/contact_sheet.png` — individual frames to inspect progression (in local prototype bundle).
- `docs/DIRECTION.md` — source attribution, conceptual rules, and next stages.

## Reproduce

Requirements: Python 3, numpy, opencv-python, Pillow, ffmpeg. Example:

```sh
python render.py --seconds 48 --fps 20 --size 640 --output outputs/intro_animatic_silent.mp4 --contact-sheet outputs/contact_sheet.png
```

Rendering is intentionally reproducible: no additional inference, APIs, paid generation, OCR, or randomness without fixed seeds. The source cover is 1254×1254 and is supplied separately; the preview is 640×640. Later, render separate 16:9 / 9:16 crops from the same world rather than stretching this output.

## Next engineering milestone

1. Choose the final Suno take; import its audio and verify the actual lyric alignment before final video cuts.
2. Replace selected cover crops with independent animated tile masters (researcher, wheat field, urban windows, chart, civic, etc.). Maintain each tile's identity and anchor position.
3. Implement the remaining cues from `sequence.json` using world-space camera moves, beat grids, and timed events.
4. Overlay provenance and maintain a timestamped song-to-source index for the YouTube description.

## Asset handoff

The original album artwork and silent MP4 preview are included in the accompanying ChatGPT prototype ZIP, but they have **not** been added to GitHub by the connected API. Copy `assets/cover.png` from the prototype ZIP into this checkout before running the renderer. Do not replace the source art with a guessed or generated lookalike. Audio is not checked into Git.

## Import the canonical cover

Download the prototype ZIP provided in this chat, then run:

```sh
python scripts/import_prototype.py mosaic_film_prototype.zip
pip install -r requirements.txt
python render.py --seconds 48 --fps 20 --size 640
python -m unittest discover -s tests -v
```

The importer validates the original cover by SHA-256. No placeholder or alternative art is silently substituted.
