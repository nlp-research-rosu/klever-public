#!/usr/bin/env python3
"""Create a deterministic, symlink-sensitive content manifest for a tree."""

from __future__ import annotations

import argparse
import hashlib
import os
import stat
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    root = args.root
    records = []
    symlinks = 0
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            kind = "symlink"
            value = os.readlink(path)
            digest = hashlib.sha256(value.encode()).hexdigest()
            size = len(value.encode())
            symlinks += 1
        elif stat.S_ISREG(mode):
            kind = "file"
            data = path.read_bytes()
            digest = hashlib.sha256(data).hexdigest()
            size = len(data)
        elif stat.S_ISDIR(mode):
            kind = "directory"
            digest = "-"
            size = 0
        else:
            kind = "other"
            digest = "-"
            size = path.lstat().st_size
        records.append(f"{kind}\t{size}\t{digest}\t{relative}")

    payload = ("\n".join(records) + "\n").encode()
    overall = hashlib.sha256(payload).hexdigest()
    header = [
        f"root\t{root}",
        f"entries\t{len(records)}",
        f"symlinks\t{symlinks}",
        f"manifest_sha256\t{overall}",
    ]
    args.output.write_text("\n".join(header + records) + "\n")
    print(f"root={root}")
    print(f"entries={len(records)}")
    print(f"symlinks={symlinks}")
    print(f"manifest_sha256={overall}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
