#!/usr/bin/env python3
"""news-image-20261123 entry: write the day's front page to the output.

The repository holds the finished front-page image in entry.png (drawn
by build_image.py from cross-checked reporting of Monday 23 November
2026). This program copies it, byte for byte, to entry.png inside the
output directory: MAKEFUN_OUTPUT_DIR when set (local runs), otherwise
/output (the grader). Standard library only, no network, and the copy
is exact, so two runs write identical bytes.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, out_dir / "entry.png")


if __name__ == "__main__":
    main()
