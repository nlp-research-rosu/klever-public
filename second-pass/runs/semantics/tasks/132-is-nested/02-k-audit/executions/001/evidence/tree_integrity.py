#!/usr/bin/env python3
"""Typed, no-symlink recursive comparison for audit provenance."""

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
    return "other"


def inventory(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}

    def visit(path: Path, rel: str) -> None:
        metadata = os.lstat(path)
        entry_kind = kind(metadata.st_mode)
        digest: str | None = None
        if entry_kind == "file":
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
        elif entry_kind == "symlink":
            digest = os.readlink(path)
        result[rel] = (entry_kind, digest)
        if entry_kind == "directory":
            for name in sorted(os.listdir(path)):
                child_rel = name if rel == "." else f"{rel}/{name}"
                visit(path / name, child_rel)

    visit(root, ".")
    return result


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} TRUSTED CANDIDATE", file=sys.stderr)
        return 2
    trusted_root, candidate_root = map(Path, sys.argv[1:])
    trusted = inventory(trusted_root)
    candidate = inventory(candidate_root)
    failures = 0
    for rel in sorted(trusted.keys() | candidate.keys()):
        if rel not in candidate:
            failures += 1
            print(f"MISSING candidate entry: {rel} ({trusted[rel][0]})")
        elif rel not in trusted:
            failures += 1
            print(f"EXTRA candidate entry: {rel} ({candidate[rel][0]})")
        elif trusted[rel][0] != candidate[rel][0]:
            failures += 1
            print(
                f"TYPE MISMATCH: {rel}: trusted={trusted[rel][0]} "
                f"candidate={candidate[rel][0]}"
            )
        elif candidate[rel][0] == "symlink":
            failures += 1
            print(f"SYMLINK candidate entry: {rel} -> {candidate[rel][1]}")
        elif trusted[rel][1] != candidate[rel][1]:
            failures += 1
            print(
                f"CONTENT MISMATCH: {rel}: trusted_sha256={trusted[rel][1]} "
                f"candidate_sha256={candidate[rel][1]}"
            )
    print(f"SUMMARY trusted_entries={len(trusted)} candidate_entries={len(candidate)} failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
