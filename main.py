#!/usr/bin/env python3
"""Copy the bundled entry.png to $MAKEFUN_OUTPUT_DIR/entry.png.

Scoring entrypoint: it only reads the repository and writes the
output directory, never the repository itself.
"""
import os
import shutil


def main():
    # The output directory comes from the scoring harness environment.
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        raise SystemExit("MAKEFUN_OUTPUT_DIR is not set")
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
