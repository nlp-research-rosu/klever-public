#!/usr/bin/env python3
"""Independently reproduce the launcher tree digest and reject non-file entries."""

from __future__ import annotations

import hashlib
import os
import stat
import sys
from pathlib import Path


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    pending = [root]
    entries: list[tuple[str, str, Path]] = []

    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            path = Path(child.path)
            mode = child.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise RuntimeError(f"linked or unsupported entry: {path}")

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


for argument in sys.argv[1:]:
    path = Path(argument)
    print(f"{tree_hash(path)}  {path}")
