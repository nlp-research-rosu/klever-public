#!/usr/bin/env python3
"""Strict, non-following comparison of a candidate tree to a trusted tree."""

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


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def inventory(root: Path, candidate: bool) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            path = Path(entry.path)
            rel = str(path.relative_to(root))
            info = entry.stat(follow_symlinks=False)
            entry_kind = kind(info.st_mode)
            detail: str | None = None
            if entry_kind == "symlink":
                detail = os.readlink(path)
                if candidate:
                    print(f"INTEGRITY_FAILURE candidate symlink: {rel} -> {detail}")
            elif entry_kind == "file":
                detail = digest(path)
            elif entry_kind == "directory":
                pending.append(path)
            result[rel] = (entry_kind, detail)
    return result


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit("usage: compare_trees.py CANDIDATE TRUSTED")
    candidate_root = Path(sys.argv[1])
    trusted_root = Path(sys.argv[2])
    failures = 0
    for label, root in (("candidate", candidate_root), ("trusted", trusted_root)):
        if not root.exists():
            print(f"INTEGRITY_FAILURE missing {label} root: {root}")
            return 1
        if root.is_symlink() or not root.is_dir():
            print(f"INTEGRITY_FAILURE mistyped {label} root: {root}")
            return 1

    candidate = inventory(candidate_root, candidate=True)
    trusted = inventory(trusted_root, candidate=False)
    for rel in sorted(trusted.keys() - candidate.keys()):
        print(f"INTEGRITY_FAILURE missing candidate entry: {rel}")
        failures += 1
    for rel in sorted(candidate.keys() - trusted.keys()):
        print(f"INTEGRITY_FAILURE additional candidate entry: {rel}")
        failures += 1
    for rel in sorted(candidate.keys() & trusted.keys()):
        candidate_kind, candidate_detail = candidate[rel]
        trusted_kind, trusted_detail = trusted[rel]
        if candidate_kind != trusted_kind:
            print(
                "INTEGRITY_FAILURE mistyped candidate entry: "
                f"{rel}: candidate={candidate_kind} trusted={trusted_kind}"
            )
            failures += 1
        elif candidate_kind == "file" and candidate_detail != trusted_detail:
            print(
                "INTEGRITY_FAILURE changed candidate file: "
                f"{rel}: candidate_sha256={candidate_detail} "
                f"trusted_sha256={trusted_detail}"
            )
            failures += 1
        elif candidate_kind == "symlink":
            failures += 1
    if failures:
        print(f"RESULT mismatches={failures}")
        return 1
    print(f"RESULT exact_tree_match entries={len(candidate)} symlinks=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
