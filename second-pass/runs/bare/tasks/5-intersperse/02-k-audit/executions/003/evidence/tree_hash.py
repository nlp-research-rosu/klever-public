#!/usr/bin/env python3
"""Independent implementation of the launcher's declared tree digest format."""

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
                raise RuntimeError(f"unsupported or linked entry: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            data = path.read_bytes()
            digest.update(len(data).to_bytes(8, "big"))
            digest.update(data)
    return digest.hexdigest()


def main() -> int:
    if len(sys.argv) < 2:
        return 64
    for argument in sys.argv[1:]:
        root = Path(argument)
        print(f"{tree_hash(root)}  {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
