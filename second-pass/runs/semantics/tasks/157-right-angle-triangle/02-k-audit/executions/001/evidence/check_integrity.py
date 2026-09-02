#!/usr/bin/env python3
"""Compare candidate inputs to trusted inputs without following symlinks."""

from __future__ import annotations

import hashlib
import os
import stat
import sys
from pathlib import Path


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1024 * 1024):
            value.update(block)
    return value.hexdigest()


def inventory(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for current, dirs, files in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        entries = list(dirs) + list(files)
        for name in entries:
            path = current_path / name
            rel = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                result[rel] = ("symlink", os.readlink(path))
                if name in dirs:
                    dirs.remove(name)
            elif stat.S_ISDIR(mode):
                result[rel] = ("directory", None)
            elif stat.S_ISREG(mode):
                result[rel] = ("file", digest(path))
            else:
                result[rel] = ("other", f"mode={oct(mode)}")
    return result


def compare_trees(trusted: Path, candidate: Path) -> int:
    trusted_entries = inventory(trusted)
    candidate_entries = inventory(candidate)
    issues: list[str] = []

    for rel in sorted(set(trusted_entries) | set(candidate_entries)):
        expected = trusted_entries.get(rel)
        actual = candidate_entries.get(rel)
        if expected is None:
            issues.append(f"EXTRA {rel}: candidate={actual}")
        elif actual is None:
            issues.append(f"MISSING {rel}: trusted={expected}")
        elif expected != actual:
            issues.append(f"CHANGED_OR_MISTYPED {rel}: trusted={expected} candidate={actual}")

    print(f"TRUSTED_ROOT: {trusted}")
    print(f"CANDIDATE_ROOT: {candidate}")
    print(f"TRUSTED_ENTRY_COUNT: {len(trusted_entries)}")
    print(f"CANDIDATE_ENTRY_COUNT: {len(candidate_entries)}")
    if issues:
        print(f"INTEGRITY_ISSUES: {len(issues)}")
        print(*issues, sep="\n")
        return 1
    print("INTEGRITY_ISSUES: 0")
    print("TREES_BYTE_AND_TYPE_IDENTICAL: yes")
    return 0


def compare_file(trusted: Path, candidate: Path) -> int:
    issues: list[str] = []
    for label, path in (("trusted", trusted), ("candidate", candidate)):
        try:
            mode = path.lstat().st_mode
        except FileNotFoundError:
            issues.append(f"MISSING {label}: {path}")
            continue
        if stat.S_ISLNK(mode):
            issues.append(f"SYMLINK {label}: {path} -> {os.readlink(path)}")
        elif not stat.S_ISREG(mode):
            issues.append(f"MISTYPED {label}: {path} mode={oct(mode)}")
    if not issues:
        trusted_hash = digest(trusted)
        candidate_hash = digest(candidate)
        print(f"TRUSTED: {trusted} sha256={trusted_hash}")
        print(f"CANDIDATE: {candidate} sha256={candidate_hash}")
        if trusted_hash != candidate_hash:
            issues.append("CONTENT_CHANGED")
    if issues:
        print(*issues, sep="\n")
        return 1
    print("BYTE_IDENTICAL: yes")
    return 0


def main() -> int:
    if len(sys.argv) != 4 or sys.argv[1] not in {"file", "tree"}:
        print("usage: check_integrity.py file|tree TRUSTED CANDIDATE", file=sys.stderr)
        return 64
    action = sys.argv[1]
    trusted = Path(sys.argv[2])
    candidate = Path(sys.argv[3])
    if action == "file":
        return compare_file(trusted, candidate)
    return compare_trees(trusted, candidate)


if __name__ == "__main__":
    raise SystemExit(main())
