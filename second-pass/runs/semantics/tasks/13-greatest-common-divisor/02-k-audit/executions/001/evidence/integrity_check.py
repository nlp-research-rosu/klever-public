#!/usr/bin/env python3
"""Independent byte/type/symlink integrity checks for audit stage 1."""

from __future__ import annotations

import hashlib
import os
import stat
from pathlib import Path


CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
REQUIRED_CLAIM_ARTIFACTS = (
    "run-input.json",
    "metrics.json",
    "codex-last.txt",
    "codex-output.log",
)


def kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "dir"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other({stat.S_IFMT(mode):#o})"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def inventory(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for current, dirs, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        for name in sorted(dirs + files):
            path = current_path / name
            rel = str(path.relative_to(root))
            path_kind = kind(path)
            if path_kind == "file":
                result[rel] = (path_kind, digest(path))
            elif path_kind == "symlink":
                result[rel] = (path_kind, os.readlink(path))
            else:
                result[rel] = (path_kind, None)
    return result


def compare_file(candidate: Path, reference: Path, label: str) -> None:
    print(f"[{label}]")
    for role, path in (("candidate", candidate), ("reference", reference)):
        if not path.exists() and not path.is_symlink():
            print(f"{role}: MISSING {path}")
        else:
            print(f"{role}: {kind(path)} sha256={digest(path) if kind(path) == 'file' else '-'} {path}")
    if (
        candidate.exists()
        and reference.exists()
        and kind(candidate) == "file"
        and kind(reference) == "file"
    ):
        print(f"byte_identical={candidate.read_bytes() == reference.read_bytes()}")


print("[rendered semantics boundary]")
trusted_semantics = REFERENCE / "reference-semantics"
print(f"trusted_tree_exists={trusted_semantics.exists()}")
print(f"trusted_tree_kind={kind(trusted_semantics) if trusted_semantics.exists() else 'MISSING'}")

print("[required untrusted generation artifacts]")
for name in REQUIRED_CLAIM_ARTIFACTS:
    path = CANDIDATE / name
    exists = path.exists() or path.is_symlink()
    print(f"{name}: {'present ' + kind(path) if exists else 'MISSING'}")
trace_candidates = sorted(
    str(path.relative_to(CANDIDATE))
    for path in CANDIDATE.rglob("*")
    if "trace" in path.name.lower()
)
print(f"structured_trace_candidates={trace_candidates}")

compare_file(CANDIDATE / "prompt.py", REFERENCE / "prompt.py", "prompt provenance")
compare_file(CANDIDATE / "py2mpy.py", REFERENCE / "py2mpy.py", "translator provenance")

print("[supplied semantics recursive comparison]")
candidate_inventory = inventory(CANDIDATE / "reference-semantics")
reference_inventory = inventory(trusted_semantics)
all_entries = sorted(set(candidate_inventory) | set(reference_inventory))
failures = 0
for rel in all_entries:
    candidate_value = candidate_inventory.get(rel)
    reference_value = reference_inventory.get(rel)
    if candidate_value != reference_value:
        failures += 1
        print(f"MISMATCH {rel}: candidate={candidate_value} reference={reference_value}")
print(f"candidate_entries={len(candidate_inventory)}")
print(f"reference_entries={len(reference_inventory)}")
print(f"integrity_failures={failures}")
