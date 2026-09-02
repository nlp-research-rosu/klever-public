#!/usr/bin/env python3
"""Reviewer-authored provenance and supplied-semantics integrity check."""

from __future__ import annotations

import hashlib
import os
import stat
from pathlib import Path


CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")

REQUIRED_FILES = (
    "run-input.json",
    "metrics.json",
    "codex-last.txt",
    "codex-output.log",
    "prompt.py",
    "py2mpy.py",
    "solution.py",
    "solution.mpy",
    "verification.k",
    "spec.k",
    "prove.sh",
    "PROOF.md",
)


def kind(path: Path) -> str:
    try:
        mode = path.lstat().st_mode
    except FileNotFoundError:
        return "missing"
    if stat.S_ISLNK(mode):
        return "symlink"
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "directory"
    return "other"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_entries(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    if kind(root) != "directory":
        return result
    for current, directories, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        for name in sorted(directories + files):
            path = current_path / name
            rel = path.relative_to(root).as_posix()
            entry_kind = kind(path)
            digest = sha256(path) if entry_kind == "file" else None
            result[rel] = (entry_kind, digest)
    return result


failures: list[str] = []

print("REQUIRED_ARTIFACT_TYPES")
for rel in REQUIRED_FILES:
    path = CANDIDATE / rel
    entry_kind = kind(path)
    print(f"{rel}\t{entry_kind}")
    if entry_kind != "file":
        failures.append(f"required artifact {rel}: expected file, found {entry_kind}")

trace_root = CANDIDATE / "codex-trace"
trace_kind = kind(trace_root)
trace_files = (
    sorted(path for path in trace_root.rglob("*") if kind(path) == "file")
    if trace_kind == "directory"
    else []
)
print(f"codex-trace\t{trace_kind}\tfiles={len(trace_files)}")
if trace_kind == "symlink":
    failures.append("codex-trace is symlinked")
for path in trace_files:
    print(f"trace-file\t{path.relative_to(CANDIDATE).as_posix()}")

print("TRUSTED_FILE_COMPARISONS")
for candidate_rel, reference_rel in (
    ("prompt.py", "prompt.py"),
    ("py2mpy.py", "py2mpy.py"),
):
    candidate_path = CANDIDATE / candidate_rel
    reference_path = REFERENCE / reference_rel
    candidate_kind = kind(candidate_path)
    reference_kind = kind(reference_path)
    equal = (
        candidate_kind == reference_kind == "file"
        and candidate_path.read_bytes() == reference_path.read_bytes()
    )
    candidate_hash = sha256(candidate_path) if candidate_kind == "file" else "-"
    reference_hash = sha256(reference_path) if reference_kind == "file" else "-"
    print(
        f"{candidate_rel}\tequal={str(equal).lower()}"
        f"\tcandidate_sha256={candidate_hash}\treference_sha256={reference_hash}"
    )
    if not equal:
        failures.append(f"{candidate_rel} differs from trusted {reference_rel}")

candidate_semantics = CANDIDATE / "reference-semantics"
trusted_semantics = REFERENCE / "reference-semantics"
candidate_root_kind = kind(candidate_semantics)
trusted_root_kind = kind(trusted_semantics)
print("SEMANTICS_ROOTS")
print(f"candidate\t{candidate_root_kind}")
print(f"trusted\t{trusted_root_kind}")
if candidate_root_kind != "directory":
    failures.append(
        f"candidate reference-semantics root: expected directory, found {candidate_root_kind}"
    )
if trusted_root_kind != "directory":
    failures.append(
        f"trusted reference-semantics root: expected directory, found {trusted_root_kind}"
    )

candidate_tree = tree_entries(candidate_semantics)
trusted_tree = tree_entries(trusted_semantics)
print("SEMANTICS_TREE_COMPARISON")
for rel in sorted(set(candidate_tree) | set(trusted_tree)):
    candidate_entry = candidate_tree.get(rel)
    trusted_entry = trusted_tree.get(rel)
    if candidate_entry is None:
        status_text = "missing-candidate"
        failures.append(f"semantics entry missing from candidate: {rel}")
    elif trusted_entry is None:
        status_text = "extra-candidate"
        failures.append(f"semantics entry additional in candidate: {rel}")
    elif candidate_entry[0] == "symlink":
        status_text = "candidate-symlink"
        failures.append(f"semantics entry symlinked in candidate: {rel}")
    elif candidate_entry[0] != trusted_entry[0]:
        status_text = f"type-mismatch:{candidate_entry[0]}!={trusted_entry[0]}"
        failures.append(f"semantics entry type mismatch: {rel}: {status_text}")
    elif candidate_entry[0] == "file" and candidate_entry[1] != trusted_entry[1]:
        status_text = "content-mismatch"
        failures.append(f"semantics file changed in candidate: {rel}")
    else:
        status_text = "identical"
    print(
        f"{rel}\t{status_text}\tcandidate={candidate_entry}\ttrusted={trusted_entry}"
    )

print("SUMMARY")
print(f"candidate_semantics_entries={len(candidate_tree)}")
print(f"trusted_semantics_entries={len(trusted_tree)}")
print(f"integrity_failures={len(failures)}")
for failure in failures:
    print(f"FAILURE\t{failure}")

raise SystemExit(1 if failures else 0)
