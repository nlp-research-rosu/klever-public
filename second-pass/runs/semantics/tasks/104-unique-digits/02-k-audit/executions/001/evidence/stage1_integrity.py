#!/usr/bin/env python3
"""Byte/type/symlink integrity checks for trusted audit inputs."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import stat


CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")


def kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISLNK(mode):
        return "symlink"
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "dir"
    return f"other:{stat.S_IFMT(mode):o}"


def entries(root: Path) -> dict[str, Path]:
    result = {".": root}
    for parent, dirs, files in os.walk(root, followlinks=False):
        parent_path = Path(parent)
        for name in dirs + files:
            path = parent_path / name
            result[path.relative_to(root).as_posix()] = path
    return result


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def compare_trees(candidate: Path, reference: Path) -> list[str]:
    problems: list[str] = []
    candidate_entries = entries(candidate)
    reference_entries = entries(reference)
    for relative in sorted(reference_entries.keys() - candidate_entries.keys()):
        problems.append(f"MISSING {relative}")
    for relative in sorted(candidate_entries.keys() - reference_entries.keys()):
        problems.append(f"ADDITIONAL {relative}")
    for relative in sorted(candidate_entries.keys() & reference_entries.keys()):
        candidate_path = candidate_entries[relative]
        reference_path = reference_entries[relative]
        candidate_kind = kind(candidate_path)
        reference_kind = kind(reference_path)
        if candidate_kind == "symlink":
            problems.append(f"SYMLINK {relative} -> {os.readlink(candidate_path)}")
            continue
        if candidate_kind != reference_kind:
            problems.append(
                f"MISTYPED {relative}: candidate={candidate_kind} "
                f"reference={reference_kind}"
            )
            continue
        if candidate_kind == "file" and sha256(candidate_path) != sha256(reference_path):
            problems.append(f"CHANGED {relative}")
    return problems


def compare_file(name: str) -> None:
    candidate = CANDIDATE / name
    reference = REFERENCE / name
    if not candidate.exists() and not candidate.is_symlink():
        print(f"{name}: MISSING")
        return
    if kind(candidate) == "symlink":
        print(f"{name}: SYMLINK -> {os.readlink(candidate)}")
        return
    if kind(candidate) != kind(reference):
        print(
            f"{name}: MISTYPED candidate={kind(candidate)} "
            f"reference={kind(reference)}"
        )
        return
    if sha256(candidate) == sha256(reference):
        print(f"{name}: BYTE_IDENTICAL sha256={sha256(candidate)}")
    else:
        print(
            f"{name}: CHANGED candidate_sha256={sha256(candidate)} "
            f"reference_sha256={sha256(reference)}"
        )


def main() -> int:
    print("SEMANTICS_MODE: SUPPLIED_SEMANTICS")
    semantics = REFERENCE / "reference-semantics"
    print(f"trusted_semantics_present: {semantics.is_dir()}")
    if not semantics.is_dir():
        print("INFRASTRUCTURE_BREACH: trusted reference semantics missing")
        return 3

    for name in ("prompt.py", "py2mpy.py"):
        compare_file(name)

    print("REQUIRED_CANDIDATE_SOURCE_ARTIFACTS:")
    for name in (
        "solution.py",
        "solution.mpy",
        "spec.k",
        "verification.k",
        "prompt.py",
        "py2mpy.py",
    ):
        path = CANDIDATE / name
        if not path.exists() and not path.is_symlink():
            print(f"{name}: MISSING")
        else:
            print(f"{name}: {kind(path)}")

    candidate_symlinks = sorted(
        path.relative_to(CANDIDATE).as_posix()
        for path in CANDIDATE.rglob("*")
        if path.is_symlink()
    )
    print(f"candidate_symlinks: {candidate_symlinks}")

    candidate_semantics = CANDIDATE / "reference-semantics"
    if not candidate_semantics.exists() and not candidate_semantics.is_symlink():
        print("reference-semantics: MISSING")
    elif kind(candidate_semantics) == "symlink":
        print(
            "reference-semantics: SYMLINK -> "
            f"{os.readlink(candidate_semantics)}"
        )
    elif kind(candidate_semantics) != "dir":
        print(f"reference-semantics: MISTYPED {kind(candidate_semantics)}")
    else:
        problems = compare_trees(candidate_semantics, semantics)
        if problems:
            print("reference-semantics: INTEGRITY_FAILURE")
            for problem in problems:
                print(problem)
        else:
            print("reference-semantics: EXACT_TREE_MATCH")

    print("PROVENANCE_ARTIFACTS:")
    expected = (
        "run-input.json",
        "metrics.json",
        "codex-last.txt",
        "codex-output.log",
    )
    for name in expected:
        path = CANDIDATE / name
        if not path.exists() and not path.is_symlink():
            print(f"{name}: MISSING")
        else:
            print(f"{name}: {kind(path)}")

    traces = sorted(
        path.relative_to(CANDIDATE).as_posix()
        for path in CANDIDATE.rglob("*")
        if path.is_file() and "trace" in path.name.lower()
    )
    print(f"structured_generation_trace_candidates: {traces}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
