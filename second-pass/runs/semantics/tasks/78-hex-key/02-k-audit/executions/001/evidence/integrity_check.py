#!/usr/bin/env python3
"""Independent candidate/trusted-input integrity inventory."""

from __future__ import annotations

import hashlib
import os
import stat
from pathlib import Path


CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
REQUIRED_CANDIDATE_FILES = (
    "run-input.json",
    "metrics.json",
    "codex-last.txt",
    "codex-output.log",
    "prompt.py",
    "py2mpy.py",
    "solution.py",
    "solution.mpy",
    "spec.k",
    "verification.k",
)


def kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other(mode={oct(mode)})"


def digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def inventory(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for current_root, dirs, files in os.walk(root, followlinks=False):
        current = Path(current_root)
        for name in sorted(dirs + files):
            path = current / name
            relative = path.relative_to(root).as_posix()
            entry_kind = kind(path)
            entry_digest = digest(path) if entry_kind == "file" else None
            result[relative] = (entry_kind, entry_digest)
    return result


print("REQUIRED CANDIDATE ARTIFACTS")
for relative in REQUIRED_CANDIDATE_FILES:
    path = CANDIDATE / relative
    if not path.exists() and not path.is_symlink():
        print(f"MISSING {path}")
    else:
        print(f"{kind(path):9} {path}")

print("\nPROMPT AND TRANSLATOR BYTE IDENTITY")
for relative in ("prompt.py", "py2mpy.py"):
    candidate = CANDIDATE / relative
    trusted = REFERENCE / relative
    if kind(candidate) != "file":
        print(f"FAIL {candidate}: candidate entry is {kind(candidate)}")
        continue
    same = candidate.read_bytes() == trusted.read_bytes()
    print(
        f"{'IDENTICAL' if same else 'DIFFERENT'} {relative} "
        f"candidate_sha256={digest(candidate)} trusted_sha256={digest(trusted)}"
    )

print("\nSUPPLIED SEMANTICS RECURSIVE INVENTORY COMPARISON")
candidate_tree = inventory(CANDIDATE / "reference-semantics")
trusted_tree = inventory(REFERENCE / "reference-semantics")
all_names = sorted(candidate_tree.keys() | trusted_tree.keys())
mismatches = 0
for name in all_names:
    candidate_entry = candidate_tree.get(name)
    trusted_entry = trusted_tree.get(name)
    if candidate_entry != trusted_entry:
        mismatches += 1
        print(
            f"MISMATCH {name}: candidate={candidate_entry!r} "
            f"trusted={trusted_entry!r}"
        )
print(
    f"SUMMARY candidate_entries={len(candidate_tree)} "
    f"trusted_entries={len(trusted_tree)} mismatches={mismatches}"
)
