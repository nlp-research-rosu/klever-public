#!/usr/bin/env python3
"""Deterministically inventory and hash a directory without following symlinks."""

from __future__ import annotations

import argparse
import hashlib
import os
import stat
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    args = parser.parse_args()
    root = args.root
    digest = hashlib.sha256()
    bad_types: list[str] = []

    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        current = Path(dirpath)
        names = sorted(dirnames + filenames)
        for name in names:
            path = current / name
            rel = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISREG(mode):
                kind = "file"
                data_hash = hashlib.sha256(path.read_bytes()).hexdigest()
                record = f"{kind}\t{rel}\t{data_hash}\n"
            elif stat.S_ISDIR(mode):
                kind = "dir"
                record = f"{kind}\t{rel}\n"
            elif stat.S_ISLNK(mode):
                kind = "symlink"
                record = f"{kind}\t{rel}\t{os.readlink(path)}\n"
                bad_types.append(record.rstrip())
            else:
                kind = "other"
                record = f"{kind}\t{rel}\t{stat.S_IFMT(mode):o}\n"
                bad_types.append(record.rstrip())
            print(record, end="")
            digest.update(record.encode())
        dirnames[:] = [
            name
            for name in sorted(dirnames)
            if not (current / name).is_symlink()
        ]

    print(f"TREE_INVENTORY_SHA256\t{digest.hexdigest()}")
    print(f"NON_REGULAR_OR_DIRECTORY_COUNT\t{len(bad_types)}")
    return 1 if bad_types else 0


if __name__ == "__main__":
    raise SystemExit(main())
