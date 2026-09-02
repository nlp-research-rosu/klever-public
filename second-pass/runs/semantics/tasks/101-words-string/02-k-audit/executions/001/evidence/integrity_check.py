#!/usr/bin/env python3
"""Typed/hash provenance checks for the supplied-semantics audit."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path

CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def kind(path: Path) -> str:
    if path.is_symlink():
        return "symlink"
    if path.is_dir():
        return "directory"
    if path.is_file():
        return "file"
    return "other"


def typed_tree(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for current, dirs, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        names = sorted(dirs + files)
        for name in names:
            path = current_path / name
            relative = path.relative_to(root).as_posix()
            entry_kind = kind(path)
            entry_hash = sha256(path) if entry_kind == "file" else None
            result[relative] = (entry_kind, entry_hash)
    return result


failures: list[str] = []

print("SEMANTICS_MODE: SUPPLIED_SEMANTICS")
trusted_semantics = REFERENCE / "reference-semantics"
candidate_semantics = CANDIDATE / "reference-semantics"
print(f"TRUSTED_SEMANTICS_PRESENT: {trusted_semantics.is_dir()}")
print(f"CANDIDATE_SEMANTICS_PRESENT: {candidate_semantics.is_dir()}")

trusted_tree = typed_tree(trusted_semantics) if trusted_semantics.is_dir() else {}
candidate_tree = typed_tree(candidate_semantics) if candidate_semantics.is_dir() else {}
all_paths = sorted(set(trusted_tree) | set(candidate_tree))
for relative in all_paths:
    trusted_entry = trusted_tree.get(relative)
    candidate_entry = candidate_tree.get(relative)
    if trusted_entry is None:
        failures.append(f"SEMANTICS_EXTRA: {relative} {candidate_entry}")
    elif candidate_entry is None:
        failures.append(f"SEMANTICS_MISSING: {relative} expected={trusted_entry}")
    elif trusted_entry[0] != candidate_entry[0]:
        failures.append(
            f"SEMANTICS_TYPE_MISMATCH: {relative} "
            f"expected={trusted_entry[0]} actual={candidate_entry[0]}"
        )
    elif trusted_entry[1] != candidate_entry[1]:
        failures.append(
            f"SEMANTICS_CONTENT_MISMATCH: {relative} "
            f"expected_sha256={trusted_entry[1]} actual_sha256={candidate_entry[1]}"
        )

print(f"SEMANTICS_TYPED_ENTRIES: {len(all_paths)}")
print(f"SEMANTICS_INTEGRITY_FAILURES: {sum(x.startswith('SEMANTICS_') for x in failures)}")

for relative in ("prompt.py", "py2mpy.py"):
    trusted = REFERENCE / relative
    submitted = CANDIDATE / relative
    if kind(trusted) != "file":
        failures.append(f"TRUSTED_INPUT_INVALID: {trusted} kind={kind(trusted)}")
    if kind(submitted) != "file":
        failures.append(f"CANDIDATE_INPUT_INVALID: {submitted} kind={kind(submitted)}")
    if trusted.is_file() and submitted.is_file():
        trusted_hash = sha256(trusted)
        submitted_hash = sha256(submitted)
        equal = trusted_hash == submitted_hash
        print(
            f"BYTE_COMPARE {relative}: equal={equal} "
            f"trusted_sha256={trusted_hash} candidate_sha256={submitted_hash}"
        )
        if not equal:
            failures.append(f"BYTE_MISMATCH: {relative}")

for relative in (
    "run-input.json",
    "metrics.json",
    "codex-last.txt",
    "codex-output.log",
):
    path = CANDIDATE / relative
    entry_kind = kind(path)
    print(f"PROVENANCE {relative}: {entry_kind}")
    if entry_kind != "file":
        failures.append(f"PROVENANCE_MISSING_OR_MISTYPED: {relative} kind={entry_kind}")

candidate_symlinks = sorted(
    path.relative_to(CANDIDATE).as_posix()
    for path in CANDIDATE.rglob("*")
    if path.is_symlink()
)
print(f"CANDIDATE_SYMLINKS: {candidate_symlinks}")
if candidate_symlinks:
    failures.extend(f"CANDIDATE_SYMLINK: {path}" for path in candidate_symlinks)

for failure in failures:
    print(f"FAILURE: {failure}")

print(f"TOTAL_FAILURES_REPORTED: {len(failures)}")
# Missing generation provenance is a reportable candidate omission, so return
# non-zero while keeping semantics integrity separately visible above.
raise SystemExit(1 if failures else 0)
