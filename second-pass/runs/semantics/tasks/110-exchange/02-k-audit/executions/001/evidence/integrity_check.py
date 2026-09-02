#!/usr/bin/env python3
"""Independent, non-following provenance and supplied-semantics integrity check."""

from __future__ import annotations

import filecmp
import os
import stat
from pathlib import Path


CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")


def kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISLNK(mode):
        return "symlink"
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "directory"
    return "other"


def manifest(root: Path) -> dict[str, tuple[str, int]]:
    result: dict[str, tuple[str, int]] = {}

    def visit(directory: Path) -> None:
        for entry in sorted(os.scandir(directory), key=lambda item: item.name):
            path = Path(entry.path)
            rel = str(path.relative_to(root))
            entry_kind = kind(path)
            result[rel] = (entry_kind, stat.S_IMODE(path.lstat().st_mode))
            if entry_kind == "directory":
                visit(path)

    visit(root)
    return result


failures: list[str] = []

for required_name in ("solution.py", "solution.mpy", "spec.k", "verification.k"):
    required_path = CANDIDATE / required_name
    if not required_path.exists() and not required_path.is_symlink():
        failures.append(f"MISSING required proof artifact: {required_path}")
    elif kind(required_path) != "file":
        failures.append(
            f"MISTYPED required proof artifact: {required_path}: {kind(required_path)}"
        )

for evidence_name in (
    "run-input.json",
    "metrics.json",
    "codex-last.txt",
    "codex-output.log",
):
    evidence_path = CANDIDATE / evidence_name
    if not evidence_path.exists() and not evidence_path.is_symlink():
        failures.append(f"MISSING generation evidence artifact: {evidence_path}")
    elif kind(evidence_path) != "file":
        failures.append(
            f"MISTYPED generation evidence artifact: {evidence_path}: {kind(evidence_path)}"
        )

for name in ("prompt.py", "py2mpy.py"):
    candidate_path = CANDIDATE / name
    reference_path = REFERENCE / name
    if not candidate_path.exists() and not candidate_path.is_symlink():
        failures.append(f"MISSING trusted-copy artifact: {candidate_path}")
    elif kind(candidate_path) != "file":
        failures.append(
            f"MISTYPED trusted-copy artifact: {candidate_path}: {kind(candidate_path)}"
        )
    elif not filecmp.cmp(candidate_path, reference_path, shallow=False):
        failures.append(f"CHANGED trusted-copy artifact: {candidate_path}")
    else:
        print(f"IDENTICAL trusted-copy artifact: {candidate_path} == {reference_path}")

trusted_semantics = REFERENCE / "reference-semantics"
candidate_semantics = CANDIDATE / "reference-semantics"
if kind(trusted_semantics) != "directory":
    raise SystemExit(
        "INFRASTRUCTURE BREACH: SUPPLIED_SEMANTICS trusted tree is not a directory"
    )
if not candidate_semantics.exists() and not candidate_semantics.is_symlink():
    failures.append(f"MISSING supplied semantics tree: {candidate_semantics}")
elif kind(candidate_semantics) != "directory":
    failures.append(
        f"MISTYPED supplied semantics tree: {candidate_semantics}: "
        f"{kind(candidate_semantics)}"
    )
else:
    trusted = manifest(trusted_semantics)
    submitted = manifest(candidate_semantics)
    for rel in sorted(trusted.keys() - submitted.keys()):
        failures.append(f"MISSING supplied semantics entry: {rel}")
    for rel in sorted(submitted.keys() - trusted.keys()):
        failures.append(f"ADDITIONAL supplied semantics entry: {rel}")
    for rel in sorted(trusted.keys() & submitted.keys()):
        trusted_kind, trusted_mode = trusted[rel]
        submitted_kind, submitted_mode = submitted[rel]
        if submitted_kind == "symlink":
            failures.append(f"SYMLINKED supplied semantics entry: {rel}")
            continue
        if trusted_kind != submitted_kind:
            failures.append(
                f"MISTYPED supplied semantics entry: {rel}: "
                f"expected {trusted_kind}, got {submitted_kind}"
            )
            continue
        if trusted_mode != submitted_mode:
            failures.append(
                f"MODE-CHANGED supplied semantics entry: {rel}: "
                f"expected {oct(trusted_mode)}, got {oct(submitted_mode)}"
            )
        if trusted_kind == "file" and not filecmp.cmp(
            trusted_semantics / rel,
            candidate_semantics / rel,
            shallow=False,
        ):
            failures.append(f"CHANGED supplied semantics entry: {rel}")

    if not any("supplied semantics" in failure for failure in failures):
        print(
            "IDENTICAL supplied semantics tree: candidate and trusted trees have "
            "the same entries, types, modes, and bytes"
        )

if failures:
    print("INTEGRITY FINDINGS:")
    for failure in failures:
        print(f"- {failure}")
else:
    print("INTEGRITY FINDINGS: none")
