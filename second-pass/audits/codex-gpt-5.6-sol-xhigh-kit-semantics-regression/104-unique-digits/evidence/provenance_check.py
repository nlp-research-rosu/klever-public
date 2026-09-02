#!/usr/bin/env python3
"""Reviewer-authored, symlink-safe provenance and supplied-semantics check."""

from __future__ import annotations

import hashlib
import os
import stat
from pathlib import Path


CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "dir"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other:{stat.S_IFMT(mode):o}"


def entries(root: Path) -> dict[str, Path]:
    result: dict[str, Path] = {}
    pending = [root]
    while pending:
        directory = pending.pop()
        with os.scandir(directory) as scan:
            for item in scan:
                path = Path(item.path)
                rel = str(path.relative_to(root))
                result[rel] = path
                if item.is_dir(follow_symlinks=False):
                    pending.append(path)
    return result


def compare_file(candidate: Path, trusted: Path, label: str) -> int:
    failures = 0
    candidate_kind = kind(candidate) if candidate.exists() or candidate.is_symlink() else "missing"
    trusted_kind = kind(trusted) if trusted.exists() or trusted.is_symlink() else "missing"
    same = False
    if candidate_kind == trusted_kind == "file":
        same = digest(candidate) == digest(trusted)
    print(
        f"{label}: candidate_kind={candidate_kind} trusted_kind={trusted_kind} "
        f"candidate_sha256={digest(candidate) if candidate_kind == 'file' else '-'} "
        f"trusted_sha256={digest(trusted) if trusted_kind == 'file' else '-'} "
        f"byte_identical={same}"
    )
    if not same:
        failures += 1
    return failures


def main() -> int:
    failures = 0
    print("MODE_BOUNDARY rendered=SUPPLIED_SEMANTICS")
    trusted_semantics = REFERENCE / "reference-semantics"
    print(
        "trusted_reference_semantics:",
        f"kind={kind(trusted_semantics) if trusted_semantics.exists() else 'missing'}",
    )
    if not trusted_semantics.is_dir() or trusted_semantics.is_symlink():
        print("INFRASTRUCTURE_BREACH trusted supplied semantics absent or mistyped")
        return 2

    failures += compare_file(CANDIDATE / "prompt.py", REFERENCE / "prompt.py", "prompt.py")
    failures += compare_file(CANDIDATE / "py2mpy.py", REFERENCE / "py2mpy.py", "py2mpy.py")

    candidate_semantics = CANDIDATE / "reference-semantics"
    trusted_entries = entries(trusted_semantics)
    candidate_entries = entries(candidate_semantics) if candidate_semantics.is_dir() else {}
    all_names = sorted(set(trusted_entries) | set(candidate_entries))
    for rel in all_names:
        candidate_path = candidate_entries.get(rel)
        trusted_path = trusted_entries.get(rel)
        if candidate_path is None:
            print(f"SEMANTICS {rel}: MISSING_FROM_CANDIDATE trusted_kind={kind(trusted_path)}")
            failures += 1
            continue
        if trusted_path is None:
            print(f"SEMANTICS {rel}: EXTRA_IN_CANDIDATE candidate_kind={kind(candidate_path)}")
            failures += 1
            continue
        candidate_kind = kind(candidate_path)
        trusted_kind = kind(trusted_path)
        if candidate_kind != trusted_kind:
            print(
                f"SEMANTICS {rel}: TYPE_MISMATCH "
                f"candidate_kind={candidate_kind} trusted_kind={trusted_kind}"
            )
            failures += 1
        elif candidate_kind == "symlink":
            print(f"SEMANTICS {rel}: SYMLINK_IN_TREE")
            failures += 1
        elif candidate_kind == "file":
            same = digest(candidate_path) == digest(trusted_path)
            print(
                f"SEMANTICS {rel}: file byte_identical={same} "
                f"candidate_sha256={digest(candidate_path)} trusted_sha256={digest(trusted_path)}"
            )
            failures += int(not same)
        else:
            print(f"SEMANTICS {rel}: {candidate_kind} matched")

    required = [
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
    ]
    for rel in required:
        path = CANDIDATE / rel
        actual = kind(path) if path.exists() or path.is_symlink() else "missing"
        print(f"REQUIRED {rel}: kind={actual}")
        if actual != "file":
            failures += 1

    trace_files = sorted((CANDIDATE / "codex-trace").rglob("*"))
    trace_regular = [path for path in trace_files if path.is_file() and not path.is_symlink()]
    trace_bad = [path for path in trace_files if path.is_symlink() or not (path.is_file() or path.is_dir())]
    print(f"STRUCTURED_TRACE regular_files={len(trace_regular)} bad_entries={len(trace_bad)}")
    for path in trace_regular:
        print(
            f"TRACE {path.relative_to(CANDIDATE)}: size={path.stat().st_size} "
            f"sha256={digest(path)}"
        )
    for path in trace_bad:
        print(f"TRACE_BAD {path.relative_to(CANDIDATE)}: kind={kind(path)}")
        failures += 1

    all_candidate = entries(CANDIDATE)
    symlinks = sorted(rel for rel, path in all_candidate.items() if kind(path) == "symlink")
    special = sorted(
        rel for rel, path in all_candidate.items() if kind(path) not in {"file", "dir", "symlink"}
    )
    print(f"CANDIDATE_TREE symlinks={symlinks} special={special}")
    print(f"PROVENANCE_FAILURES={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
