#!/usr/bin/env python3
"""Compare a candidate tree with a trusted tree without following symlinks."""

from __future__ import annotations

import hashlib
import os
import stat
import sys
from pathlib import Path


def entries(root: Path) -> dict[str, os.stat_result]:
    result: dict[str, os.stat_result] = {".": root.lstat()}
    for current, directories, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        for name in directories + files:
            path = current_path / name
            result[path.relative_to(root).as_posix()] = path.lstat()
    return result


def kind(metadata: os.stat_result) -> str:
    mode = metadata.st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other(mode={oct(mode)})"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} TRUSTED CANDIDATE", file=sys.stderr)
        return 64

    trusted = Path(sys.argv[1])
    candidate = Path(sys.argv[2])
    trusted_entries = entries(trusted)
    candidate_entries = entries(candidate)
    failures: list[str] = []

    for relative in sorted(trusted_entries.keys() | candidate_entries.keys()):
        if relative not in candidate_entries:
            failures.append(f"MISSING {relative}")
            continue
        if relative not in trusted_entries:
            failures.append(f"ADDITIONAL {relative} ({kind(candidate_entries[relative])})")
            continue

        trusted_kind = kind(trusted_entries[relative])
        candidate_kind = kind(candidate_entries[relative])
        if candidate_kind == "symlink":
            failures.append(f"SYMLINK {relative} -> {os.readlink(candidate / relative)}")
            continue
        if trusted_kind != candidate_kind:
            failures.append(
                f"MISTYPED {relative}: trusted={trusted_kind} candidate={candidate_kind}"
            )
            continue
        if trusted_kind == "file":
            trusted_hash = digest(trusted / relative)
            candidate_hash = digest(candidate / relative)
            if trusted_hash != candidate_hash:
                failures.append(
                    f"CHANGED {relative}: trusted_sha256={trusted_hash} "
                    f"candidate_sha256={candidate_hash}"
                )

    print(f"trusted_entries={len(trusted_entries)}")
    print(f"candidate_entries={len(candidate_entries)}")
    if failures:
        print(f"integrity_failures={len(failures)}")
        print("\n".join(failures))
        return 1
    print("integrity_failures=0")
    print("TREE_IDENTICAL_NO_CANDIDATE_SYMLINKS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
