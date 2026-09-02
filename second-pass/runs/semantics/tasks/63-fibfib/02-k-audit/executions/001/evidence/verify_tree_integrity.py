#!/usr/bin/env python3
"""Compare a candidate source tree to a trusted tree without following symlinks."""

from __future__ import annotations

import hashlib
import os
import stat
import sys
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def kind(mode: int) -> str:
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "dir"
    if stat.S_ISLNK(mode):
        return "symlink"
    return "special"


def inventory(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    pending = [root]
    while pending:
        current = pending.pop()
        for entry in os.scandir(current):
            path = Path(entry.path)
            rel = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            entry_kind = kind(mode)
            value: str | None = None
            if entry_kind == "file":
                value = sha256(path)
            elif entry_kind == "symlink":
                value = os.readlink(path)
            result[rel] = (entry_kind, value)
            if entry_kind == "dir":
                pending.append(path)
    return result


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} TRUSTED CANDIDATE", file=sys.stderr)
        return 64
    trusted_root, candidate_root = map(Path, sys.argv[1:])
    trusted = inventory(trusted_root)
    candidate = inventory(candidate_root)
    failures: list[str] = []
    for rel in sorted(trusted.keys() - candidate.keys()):
        failures.append(f"MISSING {rel}")
    for rel in sorted(candidate.keys() - trusted.keys()):
        failures.append(f"ADDITIONAL {rel}")
    for rel in sorted(trusted.keys() & candidate.keys()):
        trusted_kind, trusted_value = trusted[rel]
        candidate_kind, candidate_value = candidate[rel]
        if candidate_kind == "symlink":
            failures.append(f"SYMLINK {rel} -> {candidate_value}")
        if trusted_kind != candidate_kind:
            failures.append(
                f"TYPE {rel}: trusted={trusted_kind} candidate={candidate_kind}"
            )
        elif trusted_value != candidate_value:
            failures.append(
                f"CONTENT {rel}: trusted={trusted_value} candidate={candidate_value}"
            )
    print(f"trusted_entries={len(trusted)}")
    print(f"candidate_entries={len(candidate)}")
    if failures:
        print(f"integrity_failures={len(failures)}")
        print("\n".join(failures))
        return 1
    print("integrity_failures=0")
    print("trees are type- and byte-identical; candidate contains no symlinks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
