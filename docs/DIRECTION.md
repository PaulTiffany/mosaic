# MOSAIC — visual direction (v0.1)

**Premise.** One source artwork is a physically continuous mosaic world. Every image in the film is an addressable tile, with identity and provenance. The edit changes relationships among tiles rather than inventing disconnected background plates.

**Video grammar.** Camera in one world coordinate system. 2.5D travel, gentle parallax, illuminated edge lines, deliberate seams. Tile transformations use continuous interpolation; no unexplained teleportation or crossfades into unrelated backgrounds. Reveal the crop of the original cover when the pieces finally settle.

**Narrative structure.** Capability curve vs GDP → comparative advantage and organizations → abundant cheaper output vs access → agriculture's changing measured share → uneven opportunity and political constraints → interdisciplinary research → verification and responsibility. The visual narrative is an *interpretation* of an interview, not an endorsement or proof of a thesis.

**Provenance.** Every scene in `sequence.json` ties to an original video time and a short, source-based characterization. When published, include the machine-readable cue sheet and timestamped original-video URLs in the YouTube description. The visible in-video credit can read `SOURCE · ML STREET TALK · 03:08` (not a fake clickable video link).

**Test.** The opening uses actual Suno take-1 timings: intro words at 8.984s, first verse at 22.36s, mosaic prechorus at 40.008s. Full film must be timed to the final chosen take, never to nominal 108 BPM alone. Suno's aligner is best effort; visually verify word-level cues after attaching audio.

**Music decision.** Two Suno takes exist. The first is used only as a provisional reference: 4:36.56, approx 107.5 BPM and G major according to Suno analysis. Switching the selected song requires retiming by that song's own alignment (take 2 is 4:16.96, about 106.9 BPM).

**Sound.** This project has no embedded music yet. Suno's download endpoint reported that a download consumes one account download credit; the user has not authorized that spending. Do not imply this silent preview is music-synchronized playback; its scene cues nevertheless use measured song timing.

**Technical strategy.** Deterministic and re-renderable. Native Python/OpenCV/Pillow and ffmpeg. Keep upstream `artilect` architectural rules separate from this song's media assets and application code; integrate via versioned boundaries when a repository is nominated. The supplied cover is a single image; moving its crops is an animatic/visual prototype, not independently animated source scenes.