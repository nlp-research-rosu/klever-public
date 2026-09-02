#!/usr/bin/env python3
"""Reviewer-authored provenance and supplied-semantics integrity checker."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def kind(path: Path) -> str:
    if path.is_symlink():
        return "symlink"
    if path.is_file():
        return "file"
    if path.is_dir():
        return "directory"
    return "other"


def inventory(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for current, dirs, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        for name in sorted(dirs + files):
            path = current_path / name
            rel = path.relative_to(root).as_posix()
            entry_kind = kind(path)
            entry_digest = digest(path) if entry_kind == "file" else None
            result[rel] = (entry_kind, entry_digest)
    return result


def compare_trees(trusted: Path, submitted: Path) -> int:
    trusted_entries = inventory(trusted)
    submitted_entries = inventory(submitted)
    failures = 0
    for rel in sorted(set(trusted_entries) | set(submitted_entries)):
        left = trusted_entries.get(rel)
        right = submitted_entries.get(rel)
        if left is None:
            print(f"EXTRA candidate semantics entry: {rel} ({right[0]})")
            failures += 1
        elif right is None:
            print(f"MISSING candidate semantics entry: {rel} ({left[0]})")
            failures += 1
        elif left[0] != right[0]:
            print(f"TYPE MISMATCH: {rel}: trusted={left[0]} candidate={right[0]}")
            failures += 1
        elif left[0] == "symlink" or right[0] == "symlink":
            print(f"SYMLINK FORBIDDEN: {rel}")
            failures += 1
        elif left[1] != right[1]:
            print(f"CONTENT MISMATCH: {rel}: trusted={left[1]} candidate={right[1]}")
            failures += 1
    print(
        "SEMANTICS_TREE_RESULT:",
        "IDENTICAL" if failures == 0 else f"{failures} FAILURE(S)",
    )
    return failures


def compare_file(label: str, trusted: Path, submitted: Path) -> int:
    if not submitted.exists() and not submitted.is_symlink():
        print(f"{label}: MISSING candidate file {submitted}")
        return 1
    if submitted.is_symlink() or not submitted.is_file():
        print(f"{label}: INVALID TYPE {kind(submitted)} at {submitted}")
        return 1
    trusted_hash, submitted_hash = digest(trusted), digest(submitted)
    same = trusted_hash == submitted_hash
    print(
        f"{label}: {'IDENTICAL' if same else 'CHANGED'} "
        f"trusted_sha256={trusted_hash} candidate_sha256={submitted_hash}"
    )
    return 0 if same else 1


def main() -> int:
    failures = 0
    required_reference = Path("/reference/reference-semantics")
    print(
        "SUPPLIED_SEMANTICS_REFERENCE:",
        "PRESENT_DIRECTORY"
        if required_reference.is_dir() and not required_reference.is_symlink()
        else f"INFRASTRUCTURE_BREACH kind={kind(required_reference)}",
    )
    if not required_reference.is_dir() or required_reference.is_symlink():
        return 2

    failures += compare_trees(
        required_reference, Path("/candidate/reference-semantics")
    )
    failures += compare_file(
        "PROMPT",
        Path("/reference/prompt.py"),
        Path("/candidate/prompt.py"),
    )
    failures += compare_file(
        "TRANSLATOR",
        Path("/reference/py2mpy.py"),
        Path("/candidate/py2mpy.py"),
    )
    print(f"INTEGRITY_FAILURE_COUNT: {failures}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
