#!/usr/bin/env python3
"""Compare two trees without following symlinks and report every discrepancy."""

from __future__ import annotations

import hashlib
import os
import stat
import sys
from pathlib import Path


def entries(root: Path) -> dict[str, os.stat_result]:
    result: dict[str, os.stat_result] = {}
    for current, dirs, files in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        for name in sorted(dirs + files):
            path = current_path / name
            result[str(path.relative_to(root))] = path.lstat()
    return result


def kind(mode: int) -> str:
    if stat.S_ISLNK(mode):
        return "symlink"
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISREG(mode):
        return "file"
    return "other"


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} TRUSTED CANDIDATE", file=sys.stderr)
        return 2

    trusted = Path(sys.argv[1])
    candidate = Path(sys.argv[2])
    problems: list[str] = []

    if not trusted.is_dir() or trusted.is_symlink():
        problems.append(f"trusted root is not a real directory: {trusted}")
    if not candidate.is_dir() or candidate.is_symlink():
        problems.append(f"candidate root is not a real directory: {candidate}")
    if problems:
        print("\n".join(problems))
        return 1

    trusted_entries = entries(trusted)
    candidate_entries = entries(candidate)
    all_paths = sorted(set(trusted_entries) | set(candidate_entries))

    for relative in all_paths:
        trusted_stat = trusted_entries.get(relative)
        candidate_stat = candidate_entries.get(relative)
        if trusted_stat is None:
            problems.append(f"ADDITIONAL {relative}")
            continue
        if candidate_stat is None:
            problems.append(f"MISSING {relative}")
            continue

        trusted_kind = kind(trusted_stat.st_mode)
        candidate_kind = kind(candidate_stat.st_mode)
        if candidate_kind == "symlink":
            problems.append(f"SYMLINK {relative}")
            continue
        if trusted_kind != candidate_kind:
            problems.append(
                f"TYPE {relative}: trusted={trusted_kind} candidate={candidate_kind}"
            )
            continue
        if trusted_kind == "file":
            trusted_path = trusted / relative
            candidate_path = candidate / relative
            trusted_digest = digest(trusted_path)
            candidate_digest = digest(candidate_path)
            if trusted_digest != candidate_digest:
                problems.append(
                    f"CONTENT {relative}: trusted={trusted_digest} "
                    f"candidate={candidate_digest}"
                )
            trusted_exec = trusted_stat.st_mode & 0o111
            candidate_exec = candidate_stat.st_mode & 0o111
            if trusted_exec != candidate_exec:
                problems.append(
                    f"EXEC_MODE {relative}: trusted={oct(trusted_exec)} "
                    f"candidate={oct(candidate_exec)}"
                )

    if problems:
        print(f"integrity_failures={len(problems)}")
        print("\n".join(problems))
        return 1

    print(f"integrity_failures=0 entries_compared={len(all_paths)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
