> **NO LOOKAHEAD AT IMAGE INFERENCE:** The whole storyboard is DIRECTOR-ONLY context. For each image call, supply just the CURRENT lyric and specific visual target, the literal locked right-edge pixels of the cumulative ACCEPTED mural and a concise invariant style brief. Do not provide preceding lyrics, next lyrics, scene forecasts, or the full 106-frame map to the image model. Do not "bridge toward" future content. The inference prompt is generated from [LINE_GENERATION_PLAN.json](production/LINE_GENERATION_PLAN.json), which records this boundary and is checked in CI. A prior reference image alone does not ensure pixel preservation; enforce masks or composite original protected pixels back with verification.

> **CURRENT GENERATION CONTRACT:** Read [production/STORYBOARD_MAP.md](production/STORYBOARD_MAP.md) and [production/LINE_GENERATION_PLAN.json](production/LINE_GENERATION_PLAN.json) FIRST. The owner wants the entire 106-line visual map reviewed before image creation. Then produce **ONE distinct sequential generation per sung lyric**, always supplying the previous accepted image's right edge as locked left-side pixel context for the next generation. Grow the picture rightward by controlled outpainting; no blind independent shots, alpha crossfades, repeated scenes, or fake seamlessness. The 13 old art plates are storage bins only. Existing 13-plate render scripts have not been validated for 106-shot ingestion.

# MOSAIC — Creative production contract

Read [production/FULL_SONG_STORYBOARD.md](production/FULL_SONG_STORYBOARD.md) FIRST. It contains EVERY lyric as a visual beat at actual Sung Suno time. Then read [production/LINEAR_BASELINE.md](production/LINEAR_BASELINE.md). It overrides the earlier serpentine/three-register plan and any contradictory narrative path. Then read [docs/CATHEDRAL_DIRECTION.md](docs/CATHEDRAL_DIRECTION.md) and [production/camera_route.json](production/camera_route.json).

## Non-negotiable visual invariant

**Only the camera moves.** The original complete mosaic is a **single immutable image mapped to one flat surface** inside a photorealistic **three-dimensional cathedral**. Every object in the cathedral, the mosaic image, lighting, reflections, windows, text and all decoration remain static over time. No animated tiles, no moving layers, no luminous pulses, no object morphing, no particle movement and no moving overlays. Use real camera translation/orientation through a static world; camera motion may be beat/word aligned.

## Correct order of operations

1. Plan and produce a single source-grounded wide mural master depicting the entire song in spatially meaningful symbols. Original cover art serves as identity and style reference only.
2. Verify exact lyric-to-pixel narrative with lyric-timed crop previews; reject thematic collages, cathedral-framed images, and art lacking scene adjacency. Keep an annotated static atlas with mural coordinates tied to interview timestamps.
3. Build a physically coherent static cathedral scene and mount the image as a single UV-mapped planar artwork.
4. Animate only the 3D camera. Produce a short real-camera proof from that scene and inspect before undertaking the full 4:36.56 timeline.
5. Align to the selected song take's measured timings, which are best-effort until listening confirms cuts/sections. Spend no download credits without approval.
6. Preserve licenses, artist credits, timestamps, and exact software revisions, and fulfill Artilect's rules for **actually used** direct upstream Git submodules before claiming compliance.

## Provenance

- Source interview: https://www.youtube.com/watch?v=cB1GNO95iog
- Song take 1: https://suno.com/song/38f117cc-015a-4c44-98dd-cfae3f1acd89
- Source cue ledger: [docs/PROVENANCE.md](docs/PROVENANCE.md)
- This branch contains design maps, an unvalidated 13-plate stitcher and camera scaffold, and a blockout of cathedral geometry. There is NO finished mural, photoreal cathedral asset, verified 106-shot rendering pipeline, or proof video. Do not represent planning assets as a render receipt.
