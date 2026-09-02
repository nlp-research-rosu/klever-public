#!/usr/bin/env python3
"""Structural and byte-level integrity comparison without following symlinks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
from pathlib import Path


def kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISLNK(mode):
        return "symlink"
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "directory"
    return "other"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def nodes(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for current, dirnames, filenames in os.walk(root, followlinks=False):
        current_path = Path(current)
        for name in sorted(dirnames + filenames):
            path = current_path / name
            rel = path.relative_to(root).as_posix()
            node_kind = kind(path)
            detail: str | None = None
            if node_kind == "file":
                detail = sha256(path)
            elif node_kind == "symlink":
                detail = os.readlink(path)
            result[rel] = (node_kind, detail)
        dirnames[:] = [
            name
            for name in dirnames
            if kind(current_path / name) == "directory"
        ]
    return result


def compare(trusted: Path, candidate: Path) -> dict[str, object]:
    trusted_nodes = nodes(trusted)
    candidate_nodes = nodes(candidate)
    trusted_names = set(trusted_nodes)
    candidate_names = set(candidate_nodes)
    common = trusted_names & candidate_names
    missing = sorted(trusted_names - candidate_names)
    additional = sorted(candidate_names - trusted_names)
    mistyped = sorted(
        name
        for name in common
        if trusted_nodes[name][0] != candidate_nodes[name][0]
    )
    symlinked = sorted(
        name
        for name, (node_kind, _) in candidate_nodes.items()
        if node_kind == "symlink"
    )
    changed = sorted(
        name
        for name in common
        if trusted_nodes[name][0] == candidate_nodes[name][0] == "file"
        and trusted_nodes[name][1] != candidate_nodes[name][1]
    )
    return {
        "trusted": str(trusted),
        "candidate": str(candidate),
        "missing": missing,
        "additional": additional,
        "mistyped": mistyped,
        "symlinked": symlinked,
        "changed": changed,
        "ok": not (missing or additional or mistyped or symlinked or changed),
    }


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} TRUSTED CANDIDATE", file=sys.stderr)
        return 64
    result = compare(Path(sys.argv[1]), Path(sys.argv[2]))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
