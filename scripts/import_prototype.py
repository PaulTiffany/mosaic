#!/usr/bin/env python3
"""Install the exact original MOSAIC cover art from the prototype ZIP.

No substitution, external generation, network access, or music download.
"""
import hashlib
from pathlib import Path
import sys
import zipfile

EXPECTED_SHA256 = "ddf62f184784cc91d3a93c6f4ccc2f8bd9de3f2885bf1653287e2b2b7584a59f"
ZIP_MEMBER = "mosaic_film/assets/cover.png"
DEST = Path(__file__).resolve().parent.parent / "assets" / "cover.png"


def main(zip_path):
    with zipfile.ZipFile(zip_path) as archive:
        art = archive.read(ZIP_MEMBER)
    actual = hashlib.sha256(art).hexdigest()
    if actual != EXPECTED_SHA256:
        raise ValueError(f"Cover checksum mismatch: expected {EXPECTED_SHA256}, got {actual}")
    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.write_bytes(art)
    print(f"Verified original artwork: {DEST} ({len(art)} bytes)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/import_prototype.py mosaic_film_prototype.zip")
    main(sys.argv[1])
