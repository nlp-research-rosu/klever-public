#!/usr/bin/env python3
"""Independent type, symlink, and byte-integrity checks for the audit inputs."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import stat


CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def entry_kind(path: Path) -> str:
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
    return f"other(mode={oct(mode)})"


def compare_file(label: str, candidate: Path, reference: Path) -> bool:
    candidate_kind = entry_kind(candidate)
    reference_kind = entry_kind(reference)
    equal = (
        candidate_kind == "file"
        and reference_kind == "file"
        and candidate.read_bytes() == reference.read_bytes()
    )
    print(
        f"{label}: candidate_kind={candidate_kind} "
        f"reference_kind={reference_kind} byte_equal={equal}"
    )
    if candidate_kind == "file":
        print(f"  candidate_sha256={sha256(candidate)}")
    if reference_kind == "file":
        print(f"  reference_sha256={sha256(reference)}")
    return equal


def tree_entries(root: Path) -> dict[str, Path]:
    entries: dict[str, Path] = {}
    for current, directory_names, file_names in os.walk(root, followlinks=False):
        current_path = Path(current)
        for name in directory_names + file_names:
            path = current_path / name
            entries[str(path.relative_to(root))] = path
    return entries


def compare_tree(candidate_root: Path, reference_root: Path) -> list[str]:
    issues: list[str] = []
    candidate_entries = tree_entries(candidate_root)
    reference_entries = tree_entries(reference_root)
    for relative in sorted(set(candidate_entries) | set(reference_entries)):
        candidate = candidate_entries.get(relative)
        reference = reference_entries.get(relative)
        candidate_kind = entry_kind(candidate) if candidate else "missing"
        reference_kind = entry_kind(reference) if reference else "missing"
        if candidate_kind != reference_kind:
            issues.append(
                f"{relative}: candidate={candidate_kind}, reference={reference_kind}"
            )
            continue
        if candidate_kind == "symlink":
            issues.append(f"{relative}: candidate entry is a forbidden symlink")
            continue
        if candidate_kind == "file" and candidate and reference:
            if candidate.read_bytes() != reference.read_bytes():
                issues.append(
                    f"{relative}: changed bytes "
                    f"(candidate={sha256(candidate)}, reference={sha256(reference)})"
                )
    return issues


def main() -> int:
    print("MODE_CHECK: SUPPLIED_SEMANTICS")
    print(
        "trusted_reference_semantics_kind="
        f"{entry_kind(REFERENCE / 'reference-semantics')}"
    )

    print("\nNAMED_GENERATION_RECORDS")
    for name in (
        "run-input.json",
        "metrics.json",
        "codex-last.txt",
        "codex-output.log",
    ):
        print(f"{name}: {entry_kind(CANDIDATE / name)}")
    trace_candidates = sorted(
        path.name
        for path in CANDIDATE.iterdir()
        if "trace" in path.name.lower()
    )
    print(f"structured_trace_candidates={trace_candidates}")

    print("\nREQUIRED_CANDIDATE_ARTIFACT_TYPES")
    for name in (
        "prompt.py",
        "py2mpy.py",
        "solution.py",
        "solution.mpy",
        "spec.k",
        "verification.k",
        "reference-semantics",
    ):
        print(f"{name}: {entry_kind(CANDIDATE / name)}")

    print("\nPROMPT_AND_TRANSLATOR")
    prompt_ok = compare_file(
        "prompt.py", CANDIDATE / "prompt.py", REFERENCE / "prompt.py"
    )
    translator_ok = compare_file(
        "py2mpy.py", CANDIDATE / "py2mpy.py", REFERENCE / "py2mpy.py"
    )

    print("\nSUPPLIED_SEMANTICS_TREE")
    issues = compare_tree(
        CANDIDATE / "reference-semantics",
        REFERENCE / "reference-semantics",
    )
    if issues:
        for issue in issues:
            print(f"INTEGRITY_FAILURE: {issue}")
    else:
        print("TREE_IDENTICAL_NO_SYMLINKS: true")

    passed = (
        entry_kind(REFERENCE / "reference-semantics") == "directory"
        and prompt_ok
        and translator_ok
        and not issues
    )
    print(f"\nINTEGRITY_BASELINE_PASSED={passed}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
