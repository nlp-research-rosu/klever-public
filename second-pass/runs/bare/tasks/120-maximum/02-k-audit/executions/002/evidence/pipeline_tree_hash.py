#!/usr/bin/env python3
"""Recompute the recorded legacy pipeline tree digests independently."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


def sha256_tree(root: Path) -> str:
    if root.is_symlink() or not root.is_dir():
        raise ValueError(f"not a real directory: {root}")
    entries: list[tuple[str, str, Path]] = []
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
                raise ValueError(f"unsupported entry: {path}")
    digest = hashlib.sha256()
    for relative, entry_kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(entry_kind.encode() + b"\0")
        if entry_kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                while chunk := stream.read(1024 * 1024):
                    digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    result = json.loads(Path("/generation-result.json").read_text())
    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    candidate_actual = sha256_tree(Path("/candidate"))
    candidate_expected = result["outputs"]["workspace_sha256"]
    trace_actual = sha256_tree(Path("/generation-evidence/codex-trace"))
    trace_expected = usage["source_trace_sha256"]
    print(
        f"candidate_pipeline_tree expected={candidate_expected} "
        f"actual={candidate_actual} match={candidate_actual == candidate_expected}"
    )
    print(
        f"trace_pipeline_tree expected={trace_expected} "
        f"actual={trace_actual} match={trace_actual == trace_expected}"
    )


if __name__ == "__main__":
    main()
