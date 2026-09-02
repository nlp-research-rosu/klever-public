#!/usr/bin/env python3
"""Independent stage-1 provenance and supplied-semantics integrity checks."""

from __future__ import annotations

import hashlib
import os
import stat
from pathlib import Path


CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISLNK(mode):
        return "symlink"
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "directory"
    return "other"


def tree(path: Path) -> dict[str, Path]:
    result = {".": path}
    for root, directories, files in os.walk(path, followlinks=False):
        root_path = Path(root)
        for name in directories + files:
            child = root_path / name
            result[str(child.relative_to(path))] = child
    return result


print("MODE_BOUNDARY")
trusted_semantics = REFERENCE / "reference-semantics"
print(f"trusted supplied semantics exists: {trusted_semantics.is_dir()}")

print("\nREQUIRED_GENERATION_RECORDS")
for name in (
    "run-input.json",
    "metrics.json",
    "codex-last.txt",
    "codex-output.log",
):
    path = CANDIDATE / name
    print(f"{name}: {kind(path) if os.path.lexists(path) else 'MISSING'}")
traces = sorted(
    {
        *CANDIDATE.glob("*trace*"),
        *CANDIDATE.glob("*.jsonl"),
    },
    key=lambda p: str(p),
)
print("structured generation trace:", [str(path) for path in traces] or "MISSING")

print("\nPROMPT_AND_TRANSLATOR")
for name in ("prompt.py", "py2mpy.py"):
    candidate = CANDIDATE / name
    reference = REFERENCE / name
    print(
        f"{name} candidate kind: "
        f"{kind(candidate) if os.path.lexists(candidate) else 'MISSING'}"
    )
    print(
        f"{name} reference kind: "
        f"{kind(reference) if os.path.lexists(reference) else 'MISSING'}"
    )
    if kind(candidate) == kind(reference) == "file":
        candidate_hash = digest(candidate)
        reference_hash = digest(reference)
        print(f"{name} candidate sha256: {candidate_hash}")
        print(f"{name} reference sha256: {reference_hash}")
        print(f"{name} byte-identical: {candidate_hash == reference_hash}")

print("\nSUPPLIED_SEMANTICS_TREE")
candidate_semantics = CANDIDATE / "reference-semantics"
trusted = tree(trusted_semantics)
submitted = tree(candidate_semantics)
integrity_failures: list[str] = []
for relative in sorted(set(trusted) | set(submitted)):
    trusted_path = trusted.get(relative)
    candidate_path = submitted.get(relative)
    if trusted_path is None:
        integrity_failures.append(f"additional candidate entry: {relative}")
        continue
    if candidate_path is None:
        integrity_failures.append(f"missing candidate entry: {relative}")
        continue
    trusted_kind = kind(trusted_path)
    candidate_kind = kind(candidate_path)
    if candidate_kind == "symlink":
        integrity_failures.append(
            f"symlinked candidate entry: {relative} -> {os.readlink(candidate_path)}"
        )
        continue
    if candidate_kind != trusted_kind:
        integrity_failures.append(
            f"mistyped candidate entry: {relative}: "
            f"candidate={candidate_kind}, trusted={trusted_kind}"
        )
        continue
    if candidate_kind == "file" and digest(candidate_path) != digest(trusted_path):
        integrity_failures.append(f"changed candidate file: {relative}")

print(f"trusted entries: {len(trusted)}")
print(f"candidate entries: {len(submitted)}")
if integrity_failures:
    print("integrity failures:")
    for failure in integrity_failures:
        print(f"- {failure}")
else:
    print("integrity failures: NONE")

print("\nALL_CANDIDATE_SYMLINKS")
symlinks = [path for path in tree(CANDIDATE).values() if kind(path) == "symlink"]
if symlinks:
    for path in symlinks:
        print(f"{path} -> {os.readlink(path)}")
else:
    print("NONE")
