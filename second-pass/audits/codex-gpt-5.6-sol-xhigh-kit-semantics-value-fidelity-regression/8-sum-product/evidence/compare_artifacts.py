#!/usr/bin/env python3
"""Strict, symlink-aware artifact comparison for the supplied-semantics audit."""

from __future__ import annotations

import hashlib
import os
import stat
import sys
from pathlib import Path


def kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other(mode={oct(mode)})"


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def entries(root: Path) -> dict[str, Path]:
    result = {".": root}
    for base, directories, files in os.walk(root, topdown=True, followlinks=False):
        base_path = Path(base)
        for name in sorted(directories + files):
            path = base_path / name
            result[str(path.relative_to(root))] = path
    return result


def compare_file(trusted: Path, candidate: Path, label: str) -> int:
    problems: list[str] = []
    if not trusted.exists():
        problems.append(f"TRUSTED_MISSING {trusted}")
    if not candidate.exists() and not candidate.is_symlink():
        problems.append(f"CANDIDATE_MISSING {candidate}")
    if problems:
        print(f"[{label}]")
        print(*problems, sep="\n")
        return 1
    trusted_kind = kind(trusted)
    candidate_kind = kind(candidate)
    if trusted_kind != "file":
        problems.append(f"TRUSTED_WRONG_TYPE expected=file actual={trusted_kind}")
    if candidate_kind != "file":
        problems.append(f"CANDIDATE_WRONG_TYPE expected=file actual={candidate_kind}")
    if not problems:
        trusted_digest = digest(trusted)
        candidate_digest = digest(candidate)
        print(f"[{label}]")
        print(f"trusted_sha256={trusted_digest}")
        print(f"candidate_sha256={candidate_digest}")
        if trusted_digest != candidate_digest:
            problems.append("CONTENT_MISMATCH")
    else:
        print(f"[{label}]")
    print(*(problems or ["IDENTICAL"]), sep="\n")
    return bool(problems)


def compare_tree(trusted: Path, candidate: Path, label: str) -> int:
    print(f"[{label}]")
    if not trusted.exists():
        print(f"TRUSTED_MISSING {trusted}")
        return 1
    if not candidate.exists() and not candidate.is_symlink():
        print(f"CANDIDATE_MISSING {candidate}")
        return 1
    if kind(trusted) != "directory" or kind(candidate) != "directory":
        print(f"ROOT_TYPE_MISMATCH trusted={kind(trusted)} candidate={kind(candidate)}")
        return 1

    trusted_entries = entries(trusted)
    candidate_entries = entries(candidate)
    problems: list[str] = []
    all_names = sorted(set(trusted_entries) | set(candidate_entries))
    compared_files = 0
    for name in all_names:
        trusted_path = trusted_entries.get(name)
        candidate_path = candidate_entries.get(name)
        if trusted_path is None:
            problems.append(f"EXTRA {name} type={kind(candidate_path)}")
            continue
        if candidate_path is None:
            problems.append(f"MISSING {name} expected_type={kind(trusted_path)}")
            continue
        trusted_kind = kind(trusted_path)
        candidate_kind = kind(candidate_path)
        if candidate_kind == "symlink":
            problems.append(
                f"SYMLINK {name} target={os.readlink(candidate_path)!r}"
            )
            continue
        if trusted_kind != candidate_kind:
            problems.append(
                f"TYPE_MISMATCH {name} trusted={trusted_kind} candidate={candidate_kind}"
            )
            continue
        if trusted_kind == "file":
            compared_files += 1
            trusted_digest = digest(trusted_path)
            candidate_digest = digest(candidate_path)
            if trusted_digest != candidate_digest:
                problems.append(
                    f"CONTENT_MISMATCH {name} "
                    f"trusted_sha256={trusted_digest} "
                    f"candidate_sha256={candidate_digest}"
                )
    print(f"entries_trusted={len(trusted_entries)}")
    print(f"entries_candidate={len(candidate_entries)}")
    print(f"files_byte_compared={compared_files}")
    print(*(problems or ["IDENTICAL"]), sep="\n")
    return bool(problems)


def main() -> int:
    if len(sys.argv) != 1:
        print(f"usage: {sys.argv[0]}", file=sys.stderr)
        return 64
    failures = 0
    failures += compare_file(
        Path("/reference/prompt.py"), Path("/candidate/prompt.py"), "prompt.py"
    )
    failures += compare_file(
        Path("/reference/py2mpy.py"), Path("/candidate/py2mpy.py"), "py2mpy.py"
    )
    failures += compare_tree(
        Path("/reference/reference-semantics"),
        Path("/candidate/reference-semantics"),
        "reference-semantics",
    )
    print(f"COMPARISON_FAILURES={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
