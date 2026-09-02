#!/usr/bin/env python3
"""Produce a reviewer-defined, deterministic SHA-256 manifest for a tree."""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path


def digest_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root")
    args = parser.parse_args()
    root = Path(args.root)
    lines: list[str] = []

    if root.is_symlink():
        print(f"SYMLINK_ROOT\t{root}\t{os.readlink(root)}")
        return 2
    if not root.is_dir():
        print(f"NOT_DIRECTORY\t{root}")
        return 2

    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            lines.append(f"L\t{rel}\t{os.readlink(path)}")
        elif path.is_dir():
            lines.append(f"D\t{rel}\t-")
        elif path.is_file():
            lines.append(f"F\t{rel}\t{digest_file(path)}")
        else:
            lines.append(f"O\t{rel}\t-")

    aggregate = hashlib.sha256()
    for line in lines:
        print(line)
        aggregate.update(line.encode("utf-8"))
        aggregate.update(b"\n")
    print(f"REVIEWER_TREE_SHA256\t{aggregate.hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
