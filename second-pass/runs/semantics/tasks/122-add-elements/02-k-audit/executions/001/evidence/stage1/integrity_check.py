#!/usr/bin/env python3
"""Independent byte/type integrity checks for trusted inputs and supplied semantics."""

from __future__ import annotations

import hashlib
import os
import stat
from pathlib import Path

CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other({stat.S_IFMT(mode):o})"


def compare_file(candidate: Path, trusted: Path, label: str) -> int:
    problems = 0
    if not candidate.exists() and not candidate.is_symlink():
        print(f"FAIL {label}: candidate path missing: {candidate}")
        return 1
    if candidate.is_symlink():
        print(f"FAIL {label}: candidate path is symlink: {candidate}")
        return 1
    if kind(candidate) != "file":
        print(f"FAIL {label}: expected regular file, got {kind(candidate)}: {candidate}")
        return 1
    same = candidate.read_bytes() == trusted.read_bytes()
    print(
        f"{'PASS' if same else 'FAIL'} {label}: "
        f"candidate_sha256={digest(candidate)} trusted_sha256={digest(trusted)}"
    )
    return 0 if same else 1


def tree_entries(root: Path) -> dict[Path, Path]:
    entries: dict[Path, Path] = {}
    for directory, dirnames, filenames in os.walk(root, followlinks=False):
        base = Path(directory)
        for name in sorted(dirnames + filenames):
            path = base / name
            entries[path.relative_to(root)] = path
    return entries


def compare_tree(candidate_root: Path, trusted_root: Path) -> int:
    problems = 0
    candidate_entries = tree_entries(candidate_root)
    trusted_entries = tree_entries(trusted_root)
    for rel in sorted(set(candidate_entries) | set(trusted_entries)):
        candidate = candidate_entries.get(rel)
        trusted = trusted_entries.get(rel)
        if candidate is None:
            print(f"FAIL semantics missing candidate entry: {rel}")
            problems += 1
            continue
        if trusted is None:
            print(f"FAIL semantics additional candidate entry: {rel}")
            problems += 1
            continue
        candidate_kind = kind(candidate)
        trusted_kind = kind(trusted)
        if candidate_kind == "symlink":
            print(f"FAIL semantics symlinked candidate entry: {rel}")
            problems += 1
            continue
        if candidate_kind != trusted_kind:
            print(
                f"FAIL semantics mistyped entry: {rel}: "
                f"candidate={candidate_kind} trusted={trusted_kind}"
            )
            problems += 1
            continue
        if candidate_kind == "file":
            same = candidate.read_bytes() == trusted.read_bytes()
            print(
                f"{'PASS' if same else 'FAIL'} semantics file: {rel}: "
                f"candidate_sha256={digest(candidate)} trusted_sha256={digest(trusted)}"
            )
            problems += int(not same)
        else:
            print(f"PASS semantics directory: {rel}")
    return problems


def main() -> int:
    problems = 0
    print("MODE_CHECK: SUPPLIED_SEMANTICS")
    trusted_semantics = REFERENCE / "reference-semantics"
    if not trusted_semantics.is_dir() or trusted_semantics.is_symlink():
        print(
            "INFRASTRUCTURE_BREACH: trusted /reference/reference-semantics "
            "is absent, mistyped, or symlinked"
        )
        return 100
    print("PASS trusted supplied-semantics mount is a real directory")

    problems += compare_file(
        CANDIDATE / "prompt.py", REFERENCE / "prompt.py", "prompt byte identity"
    )
    problems += compare_file(
        CANDIDATE / "py2mpy.py",
        REFERENCE / "py2mpy.py",
        "translator byte identity",
    )
    problems += compare_tree(CANDIDATE / "reference-semantics", trusted_semantics)

    print("UNTRUSTED_GENERATION_CLAIM_ARTIFACTS:")
    for name in (
        "run-input.json",
        "metrics.json",
        "codex-last.txt",
        "codex-output.log",
    ):
        path = CANDIDATE / name
        if path.is_symlink():
            print(f"FAIL claim artifact symlinked: {name}")
            problems += 1
        elif path.is_file():
            print(f"PRESENT claim artifact: {name} sha256={digest(path)}")
        elif path.exists():
            print(f"FAIL claim artifact mistyped: {name} kind={kind(path)}")
            problems += 1
        else:
            print(f"MISSING claim artifact: {name}")

    trace_names = sorted(
        path.name
        for path in CANDIDATE.iterdir()
        if "trace" in path.name.lower()
    )
    print(f"STRUCTURED_TRACE_CANDIDATES: {trace_names}")
    print(f"INTEGRITY_PROBLEMS: {problems}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
