#!/usr/bin/env python3
"""Reviewer-authored byte/type/symlink integrity checker."""

from __future__ import annotations

import hashlib
import os
import stat
import sys
from pathlib import Path


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def inventory(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for current, dirnames, filenames in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        for name in sorted(dirnames + filenames):
            path = current_path / name
            rel = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                result[rel] = ("symlink", os.readlink(path))
                if name in dirnames:
                    dirnames.remove(name)
            elif stat.S_ISDIR(mode):
                result[rel] = ("directory", None)
            elif stat.S_ISREG(mode):
                result[rel] = ("file", digest(path))
            else:
                result[rel] = (f"other:{stat.S_IFMT(mode):o}", None)
    return result


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: check_integrity.py TRUSTED_TREE CANDIDATE_TREE", file=sys.stderr)
        return 64
    trusted_root, candidate_root = map(Path, sys.argv[1:])
    trusted = inventory(trusted_root)
    candidate = inventory(candidate_root)
    failures: list[str] = []
    for rel in sorted(trusted.keys() - candidate.keys()):
        failures.append(f"MISSING {rel}: expected {trusted[rel][0]}")
    for rel in sorted(candidate.keys() - trusted.keys()):
        failures.append(f"ADDITIONAL {rel}: found {candidate[rel][0]}")
    for rel in sorted(trusted.keys() & candidate.keys()):
        expected = trusted[rel]
        actual = candidate[rel]
        if expected[0] != actual[0]:
            failures.append(
                f"TYPE_MISMATCH {rel}: expected {expected[0]}, found {actual[0]}"
            )
        elif expected != actual:
            if expected[0] == "file":
                failures.append(
                    f"CONTENT_MISMATCH {rel}: expected_sha256={expected[1]} "
                    f"candidate_sha256={actual[1]}"
                )
            else:
                failures.append(
                    f"ENTRY_MISMATCH {rel}: expected={expected}, found={actual}"
                )
    for rel, entry in sorted(candidate.items()):
        if entry[0] == "symlink":
            failures.append(f"SYMLINK {rel}: target={entry[1]}")
    print(f"TRUSTED_ENTRIES: {len(trusted)}")
    print(f"CANDIDATE_ENTRIES: {len(candidate)}")
    if failures:
        print(f"INTEGRITY_FAILURES: {len(failures)}")
        print(*failures, sep="\n")
        return 1
    print("INTEGRITY_FAILURES: 0")
    print("RESULT: byte-identical regular-file tree with matching entry types and no symlinks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
