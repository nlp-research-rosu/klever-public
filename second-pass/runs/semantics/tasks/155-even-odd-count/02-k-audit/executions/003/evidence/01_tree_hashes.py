#!/usr/bin/env python3
"""Independent deterministic tree digest with type and symlink rejection."""

import hashlib
import os
import stat
from pathlib import Path


def tree_digest(root: Path) -> str:
    assert root.is_dir() and not root.is_symlink()
    entries = []
    pending = [root]
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
                raise AssertionError(f"linked or unsupported entry: {path}")
    digest = hashlib.sha256()
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


expected = {
    Path("/candidate"): "b6e38d7cb00a36a22416b17d9ae57f620b7cd17596b37d3d5e7d1f560ffdb563",
    Path("/candidate/reference-semantics"): "4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f",
    Path("/reference/reference-semantics"): "4e06397a1c5a2c7be4f6cc3f61490d87805523b8c9d3c1a0ecd8e1d6bde3789f",
    Path("/generation-evidence/codex-trace"): "ebf4b0a149b9a3be987159d483b392396e1402e90cbb758b7d6f5072fff24bdc",
}
for root, wanted in expected.items():
    observed = tree_digest(root)
    print(f"{observed}  {root}")
    assert observed == wanted
