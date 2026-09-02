#!/usr/bin/env python3
"""Independently calculate the pipeline-v3 length-delimited tree digest."""

from __future__ import annotations

import hashlib
import os
import stat
import sys
from pathlib import Path


def digest_tree(root: Path) -> str:
    root_stat = root.lstat()
    if not stat.S_ISDIR(root_stat.st_mode):
        raise ValueError(f"not a real directory: {root}")

    entries: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            path = Path(entry.path)
            mode = entry.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise ValueError(f"linked or unsupported tree entry: {path}")

    digest = hashlib.sha256()
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    if len(sys.argv) < 2:
        print(f"usage: {sys.argv[0]} TREE [TREE ...]", file=sys.stderr)
        return 64
    for argument in sys.argv[1:]:
        path = Path(argument)
        print(f"{digest_tree(path)}  {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
