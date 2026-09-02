#!/usr/bin/env python3
"""Byte/type integrity checks for trusted inputs and supplied semantics."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path


CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def tree(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for current, directories, files in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        names = sorted(directories + files)
        for name in names:
            path = current_path / name
            rel = path.relative_to(root).as_posix()
            if path.is_symlink():
                result[rel] = ("symlink", os.readlink(path))
                if name in directories:
                    directories.remove(name)
            elif path.is_dir():
                result[rel] = ("directory", None)
            elif path.is_file():
                result[rel] = ("file", digest(path))
            else:
                result[rel] = ("other", None)
    return result


def compare_file(candidate: Path, trusted: Path) -> None:
    label = candidate.name
    if not candidate.exists() and not candidate.is_symlink():
        print(f"FILE {label}: MISSING candidate")
        return
    if candidate.is_symlink():
        print(f"FILE {label}: FAIL candidate is symlink -> {os.readlink(candidate)}")
        return
    if not candidate.is_file():
        print(f"FILE {label}: FAIL candidate type is not regular file")
        return
    left = digest(candidate)
    right = digest(trusted)
    print(f"FILE {label}: {'IDENTICAL' if left == right else 'CHANGED'}")
    print(f"  candidate_sha256={left}")
    print(f"  trusted_sha256={right}")


def main() -> int:
    for name in ("prompt.py", "py2mpy.py"):
        compare_file(CANDIDATE / name, REFERENCE / name)

    trusted_root = REFERENCE / "reference-semantics"
    candidate_root = CANDIDATE / "reference-semantics"
    if not trusted_root.is_dir() or trusted_root.is_symlink():
        print("SUPPLIED_SEMANTICS_BASELINE: INFRASTRUCTURE_BREACH")
        return 2
    if not candidate_root.exists() and not candidate_root.is_symlink():
        print("CANDIDATE_SEMANTICS: MISSING")
        return 1
    if candidate_root.is_symlink() or not candidate_root.is_dir():
        print("CANDIDATE_SEMANTICS: WRONG_TYPE_OR_SYMLINK")
        return 1

    trusted_entries = tree(trusted_root)
    candidate_entries = tree(candidate_root)
    problems = 0
    for rel in sorted(trusted_entries.keys() | candidate_entries.keys()):
        trusted = trusted_entries.get(rel)
        candidate = candidate_entries.get(rel)
        if trusted is None:
            print(f"SEMANTICS EXTRA: {rel}: {candidate}")
            problems += 1
        elif candidate is None:
            print(f"SEMANTICS MISSING: {rel}: expected {trusted}")
            problems += 1
        elif trusted != candidate:
            print(f"SEMANTICS MISMATCH: {rel}: candidate={candidate} trusted={trusted}")
            problems += 1
    print(
        "SEMANTICS_TREE: "
        f"{'IDENTICAL' if problems == 0 else 'FAIL'} "
        f"trusted_entries={len(trusted_entries)} "
        f"candidate_entries={len(candidate_entries)} problems={problems}"
    )

    expected = (
        "run-input.json",
        "metrics.json",
        "codex-last.txt",
        "codex-output.log",
        "solution.py",
        "solution.mpy",
        "spec.k",
        "verification.k",
    )
    for name in expected:
        path = CANDIDATE / name
        if path.is_symlink():
            print(f"ARTIFACT {name}: SYMLINK -> {os.readlink(path)}")
            problems += 1
        elif path.is_file():
            print(f"ARTIFACT {name}: REGULAR_FILE sha256={digest(path)}")
        elif path.exists():
            print(f"ARTIFACT {name}: WRONG_TYPE")
            problems += 1
        else:
            print(f"ARTIFACT {name}: MISSING")
            if name in {"run-input.json", "metrics.json", "codex-last.txt", "codex-output.log"}:
                problems += 1
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
