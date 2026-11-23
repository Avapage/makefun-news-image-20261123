#!/usr/bin/env python3
"""Copy the finished front page into the output directory.

The entry image lives in this repository as entry.png (rendered by
build_image.py from reporting of Monday 23 November 2026). This program
writes an exact copy to entry.png in the output directory: the
MAKEFUN_OUTPUT_DIR environment variable when set, else /output. It uses
only the standard library, touches no network, and copies byte for byte,
so a second run writes the same bytes as the first. Deterministic by
construction: the source file never changes between runs.
"""

import os
import shutil

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def run():
    dest = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(dest, exist_ok=True)
    shutil.copyfile(SRC, os.path.join(dest, "entry.png"))


if __name__ == "__main__":
    run()
