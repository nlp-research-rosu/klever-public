#!/usr/bin/env python3
"""Independent lstat/byte-integrity checks for the supplied-semantics audit."""

from __future__ import annotations

import hashlib
import os
import stat
from pathlib import Path

CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")

REQUIRED = (
    "run-input.json",
    "metrics.json",
    "codex-last.txt",
    "codex-output.log",
    "prompt.py",
    "py2mpy.py",
    "solution.py",
    "solution.mpy",
    "spec.k",
    "verification.k",
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
        return "dir"
    return f"other(mode={oct(mode)})"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        current = Path(dirpath)
        for name in sorted(dirnames + filenames):
            path = current / name
            rel = path.relative_to(root).as_posix()
            path_kind = kind(path)
            file_hash = digest(path) if path_kind == "file" else None
            result[rel] = (path_kind, file_hash)
    return result


def main() -> int:
    failures: list[str] = []
    print("REQUIRED CANDIDATE ARTIFACTS")
    for name in REQUIRED:
        path = CANDIDATE / name
        path_kind = kind(path)
        print(f"{name}: {path_kind}")
        if path_kind != "file":
            failures.append(f"required artifact {name}: {path_kind}")

    print("\nTRUSTED MOUNT MODE CHECK")
    trusted_semantics = REFERENCE / "reference-semantics"
    print(f"/reference/reference-semantics: {kind(trusted_semantics)}")
    if kind(trusted_semantics) != "dir":
        failures.append("SUPPLIED_SEMANTICS trusted tree is absent or mistyped")

    print("\nTRUSTED FILE COMPARISONS")
    for name in ("prompt.py", "py2mpy.py"):
        candidate_path = CANDIDATE / name
        trusted_path = REFERENCE / name
        same = (
            kind(candidate_path) == "file"
            and kind(trusted_path) == "file"
            and candidate_path.read_bytes() == trusted_path.read_bytes()
        )
        print(f"{name}: {'BYTE_IDENTICAL' if same else 'DIFFERENT'}")
        if not same:
            failures.append(f"{name} differs from trusted file")

    print("\nSUPPLIED SEMANTICS TREE COMPARISON")
    candidate_root = CANDIDATE / "reference-semantics"
    if kind(candidate_root) != "dir":
        failures.append(
            f"candidate reference-semantics is {kind(candidate_root)}, expected dir"
        )
    else:
        candidate_tree = tree(candidate_root)
        trusted_tree = tree(trusted_semantics)
        all_paths = sorted(set(candidate_tree) | set(trusted_tree))
        for rel in all_paths:
            candidate_item = candidate_tree.get(rel)
            trusted_item = trusted_tree.get(rel)
            if candidate_item == trusted_item:
                continue
            if candidate_item is None:
                issue = f"MISSING {rel}: trusted={trusted_item}"
            elif trusted_item is None:
                issue = f"ADDITIONAL {rel}: candidate={candidate_item}"
            else:
                issue = (
                    f"CHANGED_OR_MISTYPED {rel}: "
                    f"candidate={candidate_item} trusted={trusted_item}"
                )
            print(issue)
            failures.append(issue)
        if not any(" " in item for item in failures if item.startswith(
            ("MISSING", "ADDITIONAL", "CHANGED_OR_MISTYPED")
        )):
            print(f"BYTE_IDENTICAL_TREE entries={len(trusted_tree)}")

    print("\nSYMLINK CHECKS")
    source_roots = [
        CANDIDATE / "reference-semantics",
        *(CANDIDATE / name for name in REQUIRED),
    ]
    symlinks: list[Path] = []
    for root in source_roots:
        if kind(root) == "symlink":
            symlinks.append(root)
        elif kind(root) == "dir":
            for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
                for name in dirnames + filenames:
                    path = Path(dirpath) / name
                    if kind(path) == "symlink":
                        symlinks.append(path)
    if symlinks:
        for path in symlinks:
            print(f"SYMLINK {path} -> {os.readlink(path)}")
            failures.append(f"symlinked source artifact {path}")
    else:
        print("NONE")

    print("\nRESULT")
    if failures:
        for failure in failures:
            print(f"FAILURE: {failure}")
        print(f"INTEGRITY_FAILURE_COUNT={len(failures)}")
        return 1
    print("INTEGRITY_FAILURE_COUNT=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
