> **UPDATE — production baseline (November 7, 2026):** The user explicitly chose a **one-direction left-to-right lyric side-scroller** as the baseline. Start with [LINEAR_BASELINE.md](../production/LINEAR_BASELINE.md), [frieze_manifest.json](../production/frieze_manifest.json) and [ASSET_HANDOFF.md](../production/ASSET_HANDOFF.md). Any statement below implying a serpentine path, initial full-wall reveal, or arbitrary scenic discovery is SUPERSEDED. Begin close on the first maker; each new lyrical scene is farther RIGHT. After the final lyric, the 3D camera may pull away without horizontal backtracking. The real asset target is a 39m×2m fixed frieze and its supplied cathedral; built-in Blender geometry is only a blockout.

# MOSAIC — Cathedral mural film direction (accepted concept)

## Creative premise

**One completed, immovable mosaic; one photoreal cathedral; one moving camera.**

The film treats the 4:36.56 song as a guided exploration of a *single finished work of art* mounted on one plane inside a believable three-dimensional cathedral. The mosaic visually tells the entire song at once. The music controls where the camera looks, how long it lingers, and how close it gets. A viewer could stand in the cathedral and inspect the same entire mosaic without the song.

**No story is accomplished by animating the picture.** No individually moving tiles, assembling mosaic, pulsing/glowing windows, time-varying chart, particle movement, light changes, separate parallax layers, moving text, or crossfades between artwork panels. The ONLY animated transform is the camera's position, orientation and (if necessary) focus/lens settings; use one continuous camera move if possible.

## Physical space

- Photoreal Gothic-inspired stone cathedral interior: nave, pillars, carved ribs, static warm/cool daylight, believable material response. The wall, floor, pews, ornament, lighting, and mural are *static* scene geometry.
- A huge flat mosaic image is UV-mapped to a **single planar wall surface** (not scattered tiles). Ceramic/glass surface detail may come from fixed material roughness and normal maps; the imagery itself never changes.
- The mural occupies an architecturally convincing site: a monumental wall behind the apse, spanning enough width to support prolonged glides and close inspection. The original cover art is a mood/branding reference, not a sufficiently detailed source texture for this final mural.
- The camera starts from the nave where the viewer understands that the full completed mural exists, advances, surveys narrative regions in a deliberately smooth route, and withdraws at the end so the whole mural and its seams can be seen.
- Lighting and exposure are constant. Vary apparent scale and framing through camera movement alone; any architectural parallax results naturally from camera translation in 3D space.

## Design of ONE large texture

The actual master should be a single high-resolution, aspect-consistent image (target to be set based on desired crop magnification, preliminarily 12–16k pixels across). It is one integrated narrative, not a sequence of pasted unrelated pictures. Sections are compositional landmarks, not separately animated panels.

1. **Capability versus measurement:** intersecting rising capability line and restrained macroeconomic graph, human street beneath.
2. **Organization/mosaic intelligence:** differentiated craftworkers, collaborators, AI motifs, mutually complementary skills; a collective organization that surpasses any individual, WITHOUT a literal giant robot.
3. **Abundance and prices:** harvest, factory, shelves that are full, smaller price markers, and ordinary people. More output does not automatically map to measured GDP.
4. **Demand and uneven windows:** a city of inhabited windows, some bright and some dark, fixed into the artwork. The question is who can afford the output—not whether every room can be illuminated by a visual effect.
5. **Agricultural structural change:** expanding wheatfield and shrinking slice of an economic pie, both simultaneously visible.
6. **Wages, opportunities, political economy:** multiple doorways into established and new markets; human institutions and public life occupy real visual weight, not an obstacle that machines demolish.
7. **Research beyond borders:** researcher at desk opening unfamiliar scientific territories, cross-disciplinary diagrams, verification, provenance, hand-written final argument.
8. **Visible seams:** grout and deliberate compositional joints are always present; at the final bridge these become the subject. The last wide shot shows one complete picture that does not imply a solved future.

Source claims are **interpretations of the original interview**, not predictions, direct artist endorsements or demonstrated economic results. See `PROVENANCE.md` and `camera_route.json`.

## Cinematography

- One camera travelling in actual 3D. Camera-only motion. Prefer a single continuous take over cuts; no crossfades, zoompan-on-a-JPEG pretending to be cathedral geometry, or moving artwork.
- Aesthetic: reverent museum/cathedral exploration, not kinetic lyric visualization. Start with the architecture; move close enough for glass tesserae and images to be legible; end revealing the whole physical composition.
- The song provides **timing**, not permission to add motion to the world. Faster musical passages can produce an *incrementally faster camera glide*; quiet passages hold nearly still.
- Use authored look-at/position keyframes with smooth interpolation; enforce physically plausible motion, avoid wall collision and lurching.
- 16:9 delivery, 1080p target for first render. Maintain original rectangular mural texture at full detail; no stretched square cover used as final mural.
- Do not add karaoke unless requested: words can inspire the camera's target without appearing as motion graphics.

## Important distinctions

The earlier draft PR #1 used flying tile pieces and a synthetic camera pan. The user rejected that direction. It must NOT be merged or used as visual reference for the moving-mosaic idea. The original cover remains relevant to color, imagery and branding only.

The previous silent animatic and song-time map are historical artifacts; their existence does **not** demonstrate this cathedral concept. This is a newly approved production direction, not yet a rendered film.

## Technical path — evidence before claims

1. Design/approve the complete, readable mural master in a single 2D flat projection. Do not fabricate high-resolution readability merely by resampling low-resolution cover art.
2. Build or adopt a photoreal cathedral set and place the master art on a single textured plane (a real camera-space asset).
3. Create the continuous camera spline using the timed semantic regions in `camera_route.json`; save fixed lens/exposure/render settings.
4. Render 10–20 seconds of *actual cathedral + static mural* footage and inspect framing, legibility and architectural continuity **before** committing to the whole runtime.
5. Select a Suno take, obtain its finished audio with the user's consent if a download credit is needed, and align the path with measured timing. Suno alignment is best-effort; verify manually.
6. Render the complete video, verify no image motion and no invented shot cuts, create delivery and source/provenance receipts.
7. Artilect compliance is a separate gate: record real tool authors/licensing, pinned direct upstream technology submodules, scripts, exact dependencies and receipts. Never call it compliant prematurely.

## Audio reference

Take 1: https://suno.com/song/38f117cc-015a-4c44-98dd-cfae3f1acd89

Measured length: 276.56 s. Section and lyrics are sourced from Suno's analysis/alignment. Source interview: https://www.youtube.com/watch?v=cB1GNO95iog

No audio has been downloaded or embedded for this new concept.
