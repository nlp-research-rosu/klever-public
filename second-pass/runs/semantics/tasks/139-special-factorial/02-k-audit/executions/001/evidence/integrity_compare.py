#!/usr/bin/env python3
"""Reviewer-authored recursive integrity comparison without following symlinks."""

from __future__ import annotations

import hashlib
import os
import stat
import sys
from pathlib import Path


def classify(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISLNK(mode):
        return "symlink"
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "directory"
    return f"other:{stat.S_IFMT(mode):o}"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def entries(root: Path) -> dict[str, Path]:
    result = {".": root}
    for current, directories, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        for name in directories + files:
            path = current_path / name
            result[str(path.relative_to(root))] = path
    return result


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} TRUSTED CANDIDATE", file=sys.stderr)
        return 2
    trusted_root = Path(sys.argv[1])
    candidate_root = Path(sys.argv[2])
    trusted = entries(trusted_root)
    candidate = entries(candidate_root)
    failures: list[str] = []
    for relative in sorted(trusted.keys() | candidate.keys()):
        left = trusted.get(relative)
        right = candidate.get(relative)
        if left is None:
            failures.append(f"EXTRA candidate entry: {relative} ({classify(right)})")
            continue
        if right is None:
            failures.append(f"MISSING candidate entry: {relative} ({classify(left)} expected)")
            continue
        left_type = classify(left)
        right_type = classify(right)
        if right_type == "symlink":
            failures.append(f"SYMLINK candidate entry: {relative} -> {os.readlink(right)}")
        if left_type != right_type:
            failures.append(
                f"TYPE MISMATCH: {relative}: trusted={left_type}, candidate={right_type}"
            )
            continue
        if left_type == "file":
            left_digest = digest(left)
            right_digest = digest(right)
            if left_digest != right_digest:
                failures.append(
                    f"CONTENT MISMATCH: {relative}: "
                    f"trusted_sha256={left_digest}, candidate_sha256={right_digest}"
                )
    print(f"trusted_entries={len(trusted)} candidate_entries={len(candidate)}")
    if failures:
        print(f"integrity_failures={len(failures)}")
        for failure in failures:
            print(failure)
        return 1
    print("integrity_failures=0")
    print("RESULT: exact recursive path/type/content match; no candidate symlinks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
