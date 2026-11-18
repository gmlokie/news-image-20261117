#!/usr/bin/env python3
"""news-image-20261117: copy the pre-rendered front page to the output dir.

Stdlib only. No network access. The image (entry.png, 1024x1024) is rendered
offline by render.py and shipped beside this file.
"""
import os
import shutil
import struct
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    # Validate the source is a real 1024x1024 PNG before copying.
    with open(SRC, "rb") as fh:
        header = fh.read(33)
    assert header[:8] == PNG_SIGNATURE, "entry.png is not a PNG file"
    width, height = struct.unpack(">II", header[16:24])
    assert (width, height) == (1024, 1024), f"unexpected size {width}x{height}"
    shutil.copyfile(SRC, dst)
    src_size = os.path.getsize(SRC)
    dst_size = os.path.getsize(dst)
    assert dst_size == src_size, f"copy size mismatch: {dst_size} != {src_size}"
    print(f"wrote {dst} ({dst_size} bytes, {width}x{height} PNG)")


if __name__ == "__main__":
    main()
