#!/usr/bin/env python3
"""Render the 26 November 2026 front page and write it to /output/entry.png.

Stdlib + Pillow. The image is drawn fresh on every run by gen_image.py,
so the two platform runs produce identical bytes. No network is used.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from gen_image import build

DEFAULT_DEST = "/output"


def main():
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_DEST
    os.makedirs(chosen, exist_ok=True)
    target = os.path.join(chosen, "entry.png")
    build(target)
    size = os.path.getsize(target)
    print("wrote " + target + " (" + str(size) + " bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
