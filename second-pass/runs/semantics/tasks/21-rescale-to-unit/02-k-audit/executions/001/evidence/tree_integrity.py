#!/usr/bin/env python3
"""Compare two trees without following symlinks and report every mismatch."""

from __future__ import annotations

import hashlib
import os
import stat
import sys
from pathlib import Path


def kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other(mode={oct(mode)})"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def entries(root: Path) -> dict[str, Path]:
    found = {".": root}
    for current, directories, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        for name in directories + files:
            path = current_path / name
            found[str(path.relative_to(root))] = path
    return found


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} TRUSTED CANDIDATE", file=sys.stderr)
        return 64
    trusted = Path(sys.argv[1])
    candidate = Path(sys.argv[2])
    mismatches: list[str] = []
    if not trusted.is_dir() or trusted.is_symlink():
        print(f"trusted root invalid: {trusted}")
        return 2
    if not candidate.is_dir() or candidate.is_symlink():
        print(f"candidate root invalid: {candidate}")
        return 1

    trusted_entries = entries(trusted)
    candidate_entries = entries(candidate)
    for relative in sorted(trusted_entries.keys() - candidate_entries.keys()):
        mismatches.append(f"MISSING candidate entry: {relative}")
    for relative in sorted(candidate_entries.keys() - trusted_entries.keys()):
        mismatches.append(f"ADDITIONAL candidate entry: {relative}")
    for relative in sorted(trusted_entries.keys() & candidate_entries.keys()):
        trusted_path = trusted_entries[relative]
        candidate_path = candidate_entries[relative]
        trusted_kind = kind(trusted_path)
        candidate_kind = kind(candidate_path)
        if candidate_kind == "symlink":
            mismatches.append(
                f"SYMLINK candidate entry: {relative} -> {os.readlink(candidate_path)}"
            )
            continue
        if trusted_kind != candidate_kind:
            mismatches.append(
                f"MISTYPED candidate entry: {relative}: "
                f"trusted={trusted_kind} candidate={candidate_kind}"
            )
            continue
        if trusted_kind == "file" and digest(trusted_path) != digest(candidate_path):
            mismatches.append(f"CHANGED candidate file: {relative}")

    if mismatches:
        print(f"INTEGRITY_MISMATCH_COUNT={len(mismatches)}")
        print(*mismatches, sep="\n")
        return 1
    print(f"INTEGRITY_OK entries={len(trusted_entries)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
