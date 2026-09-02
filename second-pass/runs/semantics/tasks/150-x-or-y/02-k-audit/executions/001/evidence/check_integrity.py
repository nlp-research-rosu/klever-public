#!/usr/bin/env python3
"""Type- and byte-exact comparison used by the independent auditor."""

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
        return "directory"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other(mode={oct(mode)})"


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def inventory(root: Path) -> dict[str, tuple[str, str | None]]:
    found: dict[str, tuple[str, str | None]] = {}
    pending = [root]
    while pending:
        current = pending.pop()
        metadata = os.lstat(current)
        current_kind = kind(metadata.st_mode)
        relative = "." if current == root else current.relative_to(root).as_posix()
        value: str | None = None
        if current_kind == "file":
            value = digest(current)
        elif current_kind == "symlink":
            value = os.readlink(current)
        found[relative] = (current_kind, value)
        if current_kind == "directory":
            pending.extend(sorted(current.iterdir(), reverse=True))
    return found


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} TRUSTED CANDIDATE", file=sys.stderr)
        return 64
    trusted_root, candidate_root = map(Path, sys.argv[1:])
    trusted = inventory(trusted_root)
    candidate = inventory(candidate_root)
    failures: list[str] = []

    for relative in sorted(trusted.keys() - candidate.keys()):
        failures.append(f"MISSING candidate entry: {relative}")
    for relative in sorted(candidate.keys() - trusted.keys()):
        failures.append(f"ADDITIONAL candidate entry: {relative}")
    for relative in sorted(trusted.keys() & candidate.keys()):
        if trusted[relative] != candidate[relative]:
            failures.append(
                f"CHANGED candidate entry: {relative}: "
                f"trusted={trusted[relative]} candidate={candidate[relative]}"
            )
    for relative, (entry_kind, target) in sorted(candidate.items()):
        if entry_kind == "symlink":
            failures.append(f"SYMLINK candidate entry: {relative} -> {target}")

    print(f"trusted entries: {len(trusted)}")
    print(f"candidate entries: {len(candidate)}")
    if failures:
        print("integrity failures:")
        print(*failures, sep="\n")
        return 1
    print("RESULT: exact type-and-byte identity; no candidate symlinks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
