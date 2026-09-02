#!/usr/bin/env python3
"""Independent byte/type/symlink checks for audit stage 1."""

from __future__ import annotations

import hashlib
import os
import stat
from pathlib import Path


CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")


def kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "dir"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other(mode={oct(mode)})"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def inventory(root: Path) -> dict[str, tuple[str, str | None]]:
    found: dict[str, tuple[str, str | None]] = {}
    if not root.exists() and not root.is_symlink():
        return found
    root_kind = kind(root)
    found["."] = (root_kind, os.readlink(root) if root_kind == "symlink" else None)
    if root_kind != "dir":
        return found
    for current, dirnames, filenames in os.walk(root, followlinks=False):
        current_path = Path(current)
        for name in sorted(dirnames + filenames):
            path = current_path / name
            relative = str(path.relative_to(root))
            entry_kind = kind(path)
            detail: str | None
            if entry_kind == "file":
                detail = sha256(path)
            elif entry_kind == "symlink":
                detail = os.readlink(path)
            else:
                detail = None
            found[relative] = (entry_kind, detail)
    return found


def compare_file(candidate: Path, reference: Path, label: str) -> None:
    if not candidate.exists() and not candidate.is_symlink():
        print(f"{label}: MISSING candidate={candidate}")
        return
    candidate_kind = kind(candidate)
    reference_kind = kind(reference)
    print(
        f"{label}: candidate_kind={candidate_kind} reference_kind={reference_kind}"
    )
    if candidate_kind == reference_kind == "file":
        candidate_hash = sha256(candidate)
        reference_hash = sha256(reference)
        print(f"{label}: candidate_sha256={candidate_hash}")
        print(f"{label}: reference_sha256={reference_hash}")
        print(f"{label}: BYTE_IDENTICAL={candidate_hash == reference_hash}")
    elif candidate_kind == "symlink":
        print(f"{label}: candidate_symlink_target={os.readlink(candidate)!r}")


print("MODE_CHECK: expected=SUPPLIED_SEMANTICS")
reference_semantics = REFERENCE / "reference-semantics"
print(
    "REFERENCE_SEMANTICS_PRESENT:",
    reference_semantics.exists() and kind(reference_semantics) == "dir",
)
print("REFERENCE_SEMANTICS_KIND:", kind(reference_semantics))

required = [
    "run-input.json",
    "metrics.json",
    "codex-last.txt",
    "codex-output.log",
    "solution.py",
    "solution.mpy",
    "spec.k",
    "verification.k",
    "prompt.py",
    "py2mpy.py",
]
for relative in required:
    path = CANDIDATE / relative
    if path.exists() or path.is_symlink():
        entry_kind = kind(path)
        detail = f" target={os.readlink(path)!r}" if entry_kind == "symlink" else ""
        print(f"REQUIRED {relative}: PRESENT kind={entry_kind}{detail}")
    else:
        print(f"REQUIRED {relative}: MISSING")

trace_root = CANDIDATE / "codex-trace"
trace_entries = inventory(trace_root)
print(f"STRUCTURED_TRACE_ENTRY_COUNT: {len(trace_entries)}")
for relative, entry in sorted(trace_entries.items()):
    print(f"TRACE {relative}: {entry}")

compare_file(CANDIDATE / "prompt.py", REFERENCE / "prompt.py", "PROMPT")
compare_file(CANDIDATE / "py2mpy.py", REFERENCE / "py2mpy.py", "TRANSLATOR")

candidate_inventory = inventory(CANDIDATE / "reference-semantics")
reference_inventory = inventory(reference_semantics)
all_paths = sorted(set(candidate_inventory) | set(reference_inventory))
differences = 0
for relative in all_paths:
    candidate_entry = candidate_inventory.get(relative)
    reference_entry = reference_inventory.get(relative)
    if candidate_entry != reference_entry:
        differences += 1
        print(
            "SEMANTICS_DIFFERENCE "
            f"path={relative!r} candidate={candidate_entry!r} reference={reference_entry!r}"
        )
print(f"SEMANTICS_ENTRY_COUNT_CANDIDATE: {len(candidate_inventory)}")
print(f"SEMANTICS_ENTRY_COUNT_REFERENCE: {len(reference_inventory)}")
print(f"SEMANTICS_DIFFERENCE_COUNT: {differences}")
