#!/usr/bin/env python3
"""Compare candidate inputs to trusted inputs without following symlinks."""

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
    return "other"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def manifest(root: Path) -> dict[str, tuple[str, str | None, str | None]]:
    result: dict[str, tuple[str, str | None, str | None]] = {}
    for current, dirnames, filenames in os.walk(root, followlinks=False):
        current_path = Path(current)
        entries = sorted(dirnames + filenames)
        for name in entries:
            path = current_path / name
            relative = path.relative_to(root).as_posix()
            path_kind = kind(path)
            if path_kind == "file":
                result[relative] = (path_kind, digest(path), None)
            elif path_kind == "symlink":
                result[relative] = (path_kind, None, os.readlink(path))
                if name in dirnames:
                    dirnames.remove(name)
            else:
                result[relative] = (path_kind, None, None)
    return result


def compare_tree(candidate: Path, trusted: Path) -> int:
    errors = 0
    candidate_manifest = manifest(candidate)
    trusted_manifest = manifest(trusted)
    all_names = sorted(set(candidate_manifest) | set(trusted_manifest))
    for name in all_names:
        c_entry = candidate_manifest.get(name)
        t_entry = trusted_manifest.get(name)
        if c_entry is None:
            print(f"MISSING candidate entry: {name} trusted={t_entry}")
            errors += 1
        elif t_entry is None:
            print(f"EXTRA candidate entry: {name} candidate={c_entry}")
            errors += 1
        elif c_entry[0] == "symlink":
            print(f"SYMLINK candidate entry: {name} target={c_entry[2]!r}")
            errors += 1
        elif c_entry[0] != t_entry[0]:
            print(f"TYPE MISMATCH: {name} candidate={c_entry[0]} trusted={t_entry[0]}")
            errors += 1
        elif c_entry[0] == "file" and c_entry[1] != t_entry[1]:
            print(
                f"CONTENT MISMATCH: {name} "
                f"candidate_sha256={c_entry[1]} trusted_sha256={t_entry[1]}"
            )
            errors += 1
    print(
        "TREE SUMMARY: "
        f"candidate_entries={len(candidate_manifest)} "
        f"trusted_entries={len(trusted_manifest)} integrity_failures={errors}"
    )
    return errors


def compare_file(label: str, candidate: Path, trusted: Path) -> int:
    errors = 0
    if not candidate.exists() and not candidate.is_symlink():
        print(f"MISSING candidate {label}: {candidate}")
        return 1
    if candidate.is_symlink():
        print(f"SYMLINK candidate {label}: {candidate} -> {os.readlink(candidate)!r}")
        return 1
    if kind(candidate) != "file":
        print(f"TYPE MISMATCH candidate {label}: {candidate} kind={kind(candidate)}")
        return 1
    if kind(trusted) != "file":
        print(f"INFRASTRUCTURE trusted {label} is not a regular file: {trusted}")
        return 1
    candidate_digest = digest(candidate)
    trusted_digest = digest(trusted)
    if candidate_digest != trusted_digest:
        print(
            f"CONTENT MISMATCH {label}: "
            f"candidate_sha256={candidate_digest} trusted_sha256={trusted_digest}"
        )
        errors += 1
    else:
        print(f"MATCH {label}: sha256={candidate_digest}")
    return errors


def main() -> int:
    print("MODE CHECK:")
    semantics = REFERENCE / "reference-semantics"
    print(
        f"trusted_reference_semantics_exists={semantics.exists()} "
        f"kind={kind(semantics) if semantics.exists() else 'missing'}"
    )
    if not semantics.exists() or kind(semantics) != "dir":
        print("INFRASTRUCTURE BREACH: supplied reference semantics is absent or mistyped")
        return 2

    print("\nTOP-LEVEL REQUIRED/CLAIMED ARTIFACT TYPES:")
    required = [
        "prompt.py",
        "py2mpy.py",
        "solution.py",
        "solution.mpy",
        "spec.k",
        "verification.k",
        "run-input.json",
        "metrics.json",
        "codex-last.txt",
        "codex-output.log",
    ]
    for name in required:
        path = CANDIDATE / name
        if path.exists() or path.is_symlink():
            suffix = f" -> {os.readlink(path)!r}" if path.is_symlink() else ""
            print(f"{name}: {kind(path)}{suffix}")
        else:
            print(f"{name}: MISSING")

    print("\nTRUSTED FILE COMPARISONS:")
    errors = 0
    errors += compare_file(
        "prompt.py", CANDIDATE / "prompt.py", REFERENCE / "prompt.py"
    )
    errors += compare_file(
        "py2mpy.py", CANDIDATE / "py2mpy.py", REFERENCE / "py2mpy.py"
    )

    print("\nSUPPLIED SEMANTICS TREE COMPARISON:")
    candidate_semantics = CANDIDATE / "reference-semantics"
    if (
        not candidate_semantics.exists()
        or candidate_semantics.is_symlink()
        or kind(candidate_semantics) != "dir"
    ):
        print(
            "CANDIDATE INTEGRITY FAILURE: reference-semantics missing, symlinked, "
            "or not a directory"
        )
        errors += 1
    else:
        errors += compare_tree(candidate_semantics, semantics)

    print(f"\nTOTAL CANDIDATE INTEGRITY FAILURES: {errors}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
