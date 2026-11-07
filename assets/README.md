# Canonical MOSAIC cover art

The original generated `MOSAIC (Whose Windows Glow?)` cover is distributed in the ChatGPT prototype ZIP (not in Git at present). It is an **asset input**, not a prompt to produce a lookalike.

- Image path in the archive: `mosaic_film/assets/cover.png`
- Verified SHA-256: `ddf62f184784cc91d3a93c6f4ccc2f8bd9de3f2885bf1653287e2b2b7584a59f`
- Expected dimensions: 1254×1254 px
- Expected size: 3,947,189 bytes
- Import: `python scripts/import_prototype.py path/to/mosaic_film_prototype.zip`

The importer verifies exact bytes before writing `assets/cover.png`. Keep the binary out of Git until it can be committed intentionally through a binary-capable authenticated client.

Video renders are generated media. The preview and contact sheet are present in the same ZIP and can be independently regenerated after importing the cover.

No Suno song download or credit expenditure was performed for this repository.
