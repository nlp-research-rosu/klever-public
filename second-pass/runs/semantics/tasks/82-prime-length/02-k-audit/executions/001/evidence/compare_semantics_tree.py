#!/usr/bin/env python3
"""Lstat-level supplied-semantics integrity comparison."""

from __future__ import annotations

import hashlib
import os
import stat
from pathlib import Path


CANDIDATE = Path("/candidate/reference-semantics")
TRUSTED = Path("/reference/reference-semantics")


def entries(root: Path) -> dict[str, os.stat_result]:
    result: dict[str, os.stat_result] = {}
    for directory, names, files in os.walk(root, followlinks=False):
        base = Path(directory)
        for name in sorted(names + files):
            path = base / name
            result[path.relative_to(root).as_posix()] = path.lstat()
    return result


def kind(mode: int) -> str:
    if stat.S_ISREG(mode):
        return "regular"
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other-{stat.S_IFMT(mode):o}"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


candidate = entries(CANDIDATE)
trusted = entries(TRUSTED)
failures = 0
for relative in sorted(set(candidate) | set(trusted)):
    cs = candidate.get(relative)
    ts = trusted.get(relative)
    if cs is None:
        print(f"MISSING\t{relative}")
        failures += 1
        continue
    if ts is None:
        print(f"ADDITIONAL\t{relative}")
        failures += 1
        continue
    ck, tk = kind(cs.st_mode), kind(ts.st_mode)
    if ck != tk:
        print(f"TYPE_MISMATCH\t{relative}\tcandidate={ck}\ttrusted={tk}")
        failures += 1
        continue
    if ck == "symlink":
        print(f"FORBIDDEN_SYMLINK\t{relative}")
        failures += 1
        continue
    cmode, tmode = stat.S_IMODE(cs.st_mode), stat.S_IMODE(ts.st_mode)
    if cmode != tmode:
        print(
            f"MODE_MISMATCH\t{relative}\t"
            f"candidate={cmode:o}\ttrusted={tmode:o}"
        )
        failures += 1
    if ck == "regular":
        cd, td = digest(CANDIDATE / relative), digest(TRUSTED / relative)
        if cd != td:
            print(
                f"CONTENT_MISMATCH\t{relative}\tcandidate={cd}\ttrusted={td}"
            )
            failures += 1
        else:
            print(f"MATCH\t{relative}\tsha256={cd}\tmode={cmode:o}")
    elif ck == "directory":
        print(f"MATCH_DIR\t{relative}\tmode={cmode:o}")

print(f"CANDIDATE_ENTRIES: {len(candidate)}")
print(f"TRUSTED_ENTRIES: {len(trusted)}")
print(f"FAILURES: {failures}")
raise SystemExit(1 if failures else 0)
