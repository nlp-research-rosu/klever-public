#!/usr/bin/env python3
"""Compare two directory trees without following symlinks."""

from __future__ import annotations

import hashlib
import os
import stat
import sys
from pathlib import Path


def kind(mode: int) -> str:
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "dir"
    if stat.S_ISLNK(mode):
        return "symlink"
    return "other"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            value.update(block)
    return value.hexdigest()


def manifest(root: Path) -> dict[str, tuple[str, str | None]]:
    entries: dict[str, tuple[str, str | None]] = {}

    def visit(path: Path, relative: str) -> None:
        info = path.lstat()
        entry_kind = kind(info.st_mode)
        detail: str | None = None
        if entry_kind == "file":
            detail = digest(path)
        elif entry_kind == "symlink":
            detail = os.readlink(path)
        entries[relative] = (entry_kind, detail)
        if entry_kind == "dir":
            for child in sorted(path.iterdir(), key=lambda item: item.name):
                child_relative = child.name if not relative else f"{relative}/{child.name}"
                visit(child, child_relative)

    visit(root, "")
    return entries


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} TRUSTED_TREE CANDIDATE_TREE", file=sys.stderr)
        return 64
    trusted_root = Path(sys.argv[1])
    candidate_root = Path(sys.argv[2])
    trusted = manifest(trusted_root)
    candidate = manifest(candidate_root)
    problems: list[str] = []
    for name in sorted(trusted.keys() - candidate.keys()):
        problems.append(f"MISSING {name or '.'}")
    for name in sorted(candidate.keys() - trusted.keys()):
        problems.append(f"ADDITIONAL {name or '.'}")
    for name in sorted(trusted.keys() & candidate.keys()):
        if trusted[name] != candidate[name]:
            problems.append(
                f"CHANGED {name or '.'}: trusted={trusted[name]} candidate={candidate[name]}"
            )
    for problem in problems:
        print(problem)
    print(f"TRUSTED_ENTRIES: {len(trusted)}")
    print(f"CANDIDATE_ENTRIES: {len(candidate)}")
    print(f"INTEGRITY_PROBLEMS: {len(problems)}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
