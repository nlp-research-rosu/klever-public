#!/usr/bin/env python3
"""Independent path/type/content tree SHA-256 used for mounted directory checks."""
from __future__ import annotations

import hashlib
import os
import stat
from pathlib import Path


def tree_digest(root: Path) -> str:
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for item in os.scandir(directory):
            path = Path(item.path)
            mode = item.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise RuntimeError(f"linked or unsupported entry: {path}")
    digest = hashlib.sha256()
    for relative, kind, path in sorted(entries):
        digest.update(relative.encode("utf-8") + b"\0")
        digest.update(kind.encode("ascii") + b"\0")
        if kind == "file":
            digest.update(path.read_bytes())
    return digest.hexdigest()


checks = [
    Path("/candidate"),
    Path("/candidate/reference-semantics"),
    Path("/reference/reference-semantics"),
    Path("/generation-evidence/codex-trace"),
]

print("scheme=sorted relative path NUL type NUL content (reviewer-authored)")
print("note=launcher aggregate tree scheme is not inferred; recorded per-file hashes are checked separately")
for path in checks:
    actual = tree_digest(path)
    print(f"{path} reviewer_tree_sha256={actual}")
