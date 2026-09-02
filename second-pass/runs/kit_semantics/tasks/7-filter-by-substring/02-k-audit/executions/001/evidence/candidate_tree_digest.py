#!/usr/bin/env python3
"""Reviewer-defined canonical digest over every mounted candidate entry."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


ROOT = Path("/candidate")


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    entries = []
    total_bytes = 0
    type_counts: dict[str, int] = {}
    for current, directories, files in os.walk(ROOT, topdown=True, followlinks=False):
        base = Path(current)
        for name in sorted(directories + files):
            path = base / name
            rel = path.relative_to(ROOT).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                kind = "symlink"
                value = os.readlink(path)
            elif stat.S_ISDIR(mode):
                kind = "directory"
                value = None
            elif stat.S_ISREG(mode):
                kind = "file"
                value = file_hash(path)
                total_bytes += path.lstat().st_size
            else:
                kind = "other"
                value = oct(mode)
            type_counts[kind] = type_counts.get(kind, 0) + 1
            entries.append((rel, kind, value))
    encoded = json.dumps(entries, ensure_ascii=False, separators=(",", ":")).encode()
    print(f"root={ROOT}")
    print(f"entries={len(entries)}")
    print(f"regular_file_bytes={total_bytes}")
    print(f"type_counts={json.dumps(type_counts, sort_keys=True)}")
    print(f"reviewer_canonical_manifest_sha256={hashlib.sha256(encoded).hexdigest()}")
    print("launcher_recorded_candidate_tree_sha256=13b129186233722eb47336bb008d877176227cc312b1fb71d4144a2c454df851")
    print("launcher_recorded_workspace_sha256=4247d334d98f7c24b67dd9ce59ba8c0be544897429b8b4e5e3a84e800e3bfcb6")
    print("note=launcher tree serialization is unspecified; digests are not directly comparable")
    return 1 if type_counts.get("symlink", 0) or type_counts.get("other", 0) else 0


if __name__ == "__main__":
    raise SystemExit(main())
