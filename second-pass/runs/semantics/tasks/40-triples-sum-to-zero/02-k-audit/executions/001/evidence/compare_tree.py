#!/usr/bin/env python3
"""Strict, non-dereferencing comparison of a candidate tree to a trusted tree."""

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


def entries(root: Path) -> dict[str, tuple[str, str | None]]:
    found: dict[str, tuple[str, str | None]] = {}
    for current, dirs, files in os.walk(root, topdown=True, followlinks=False):
        base = Path(current)
        names = sorted(dirs + files)
        for name in names:
            path = base / name
            rel = path.relative_to(root).as_posix()
            st = path.lstat()
            entry_kind = kind(st.st_mode)
            digest: str | None = None
            if entry_kind == "file":
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
            elif entry_kind == "symlink":
                digest = os.readlink(path)
            found[rel] = (entry_kind, digest)
        dirs[:] = [
            name
            for name in dirs
            if not stat.S_ISLNK((base / name).lstat().st_mode)
        ]
    return found


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: compare_tree.py CANDIDATE TRUSTED", file=sys.stderr)
        return 64
    candidate = Path(sys.argv[1])
    trusted = Path(sys.argv[2])
    if not candidate.is_dir() or not trusted.is_dir():
        print(f"ROOT_ERROR candidate_dir={candidate.is_dir()} trusted_dir={trusted.is_dir()}")
        return 2

    cand = entries(candidate)
    trust = entries(trusted)
    failures: list[str] = []

    for rel in sorted(trust.keys() - cand.keys()):
        failures.append(f"MISSING {rel} trusted={trust[rel][0]}")
    for rel in sorted(cand.keys() - trust.keys()):
        failures.append(f"ADDITIONAL {rel} candidate={cand[rel][0]}")
    for rel in sorted(cand.keys() & trust.keys()):
        ck, cv = cand[rel]
        tk, tv = trust[rel]
        if ck == "symlink":
            failures.append(f"SYMLINK {rel} target={cv!r}")
        if ck != tk:
            failures.append(f"TYPE_MISMATCH {rel} candidate={ck} trusted={tk}")
        elif cv != tv:
            failures.append(f"CONTENT_MISMATCH {rel} candidate={cv} trusted={tv}")

    print(f"CANDIDATE_ENTRY_COUNT {len(cand)}")
    print(f"TRUSTED_ENTRY_COUNT {len(trust)}")
    if failures:
        for failure in failures:
            print(failure)
        print(f"INTEGRITY_FAILURE_COUNT {len(failures)}")
        return 1
    print("INTEGRITY_OK exact entry/type/content match; no candidate symlinks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
