#!/usr/bin/env python3
from __future__ import annotations

import hashlib
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
    return f"other({mode:o})"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compare_file(candidate: Path, trusted: Path) -> list[str]:
    problems: list[str] = []
    if not candidate.exists() and not candidate.is_symlink():
        return [f"MISSING {candidate}"]
    if kind(candidate) != "file":
        return [f"MISTYPED {candidate}: {kind(candidate)} (expected file)"]
    if kind(trusted) != "file":
        return [f"INFRASTRUCTURE trusted input mistyped {trusted}: {kind(trusted)}"]
    same = candidate.read_bytes() == trusted.read_bytes()
    print(
        f"COMPARE {candidate} {trusted}: "
        f"{'IDENTICAL' if same else 'CHANGED'} "
        f"candidate_sha256={digest(candidate)} trusted_sha256={digest(trusted)}"
    )
    if not same:
        problems.append(f"CHANGED {candidate} versus {trusted}")
    return problems


def tree_entries(root: Path) -> dict[Path, tuple[str, str | None]]:
    entries: dict[Path, tuple[str, str | None]] = {}
    for current, dirs, files in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        for name in sorted(dirs + files):
            path = current_path / name
            relative = path.relative_to(root)
            entry_kind = kind(path)
            fingerprint = digest(path) if entry_kind == "file" else None
            entries[relative] = (entry_kind, fingerprint)
    return entries


def compare_tree(candidate: Path, trusted: Path) -> list[str]:
    problems: list[str] = []
    if not candidate.exists() or kind(candidate) != "directory":
        return [f"MISSING_OR_MISTYPED_TREE {candidate}"]
    if not trusted.exists() or kind(trusted) != "directory":
        return [f"INFRASTRUCTURE missing_or_mistyped_tree {trusted}"]
    candidate_entries = tree_entries(candidate)
    trusted_entries = tree_entries(trusted)
    all_paths = sorted(set(candidate_entries) | set(trusted_entries))
    print(
        f"TREE_COUNTS candidate={len(candidate_entries)} trusted={len(trusted_entries)}"
    )
    for relative in all_paths:
        candidate_record = candidate_entries.get(relative)
        trusted_record = trusted_entries.get(relative)
        if candidate_record is None:
            problems.append(f"MISSING {candidate / relative}")
        elif trusted_record is None:
            problems.append(f"ADDITIONAL {candidate / relative}")
        elif candidate_record[0] != trusted_record[0]:
            problems.append(
                f"MISTYPED {candidate / relative}: {candidate_record[0]} "
                f"(trusted {trusted_record[0]})"
            )
        elif candidate_record[0] == "symlink":
            problems.append(f"SYMLINKED {candidate / relative}")
        elif candidate_record[1] != trusted_record[1]:
            problems.append(f"CHANGED {candidate / relative}")
    return problems


def main() -> int:
    problems: list[str] = []
    required_claim_artifacts = [
        "run-input.json",
        "metrics.json",
        "codex-last.txt",
        "codex-output.log",
    ]
    for name in required_claim_artifacts:
        path = CANDIDATE / name
        if not path.exists() and not path.is_symlink():
            problems.append(f"MISSING {path}")
        elif kind(path) != "file":
            problems.append(f"MISTYPED {path}: {kind(path)} (expected file)")
        else:
            print(f"PRESENT {path} type=file size={path.stat().st_size}")

    trace_candidates = sorted(
        path
        for path in CANDIDATE.iterdir()
        if "trace" in path.name.lower()
        and (path.exists() or path.is_symlink())
    )
    if trace_candidates:
        for path in trace_candidates:
            print(f"STRUCTURED_TRACE_CANDIDATE {path} type={kind(path)}")
    else:
        problems.append("MISSING structured generation trace (no trace-named root artifact)")

    problems += compare_file(CANDIDATE / "prompt.py", REFERENCE / "prompt.py")
    problems += compare_file(CANDIDATE / "py2mpy.py", REFERENCE / "py2mpy.py")
    problems += compare_tree(
        CANDIDATE / "reference-semantics",
        REFERENCE / "reference-semantics",
    )

    print(f"PROBLEM_COUNT {len(problems)}")
    for problem in problems:
        print(f"PROBLEM {problem}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
