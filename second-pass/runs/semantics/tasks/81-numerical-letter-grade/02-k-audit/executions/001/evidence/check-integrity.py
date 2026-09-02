#!/usr/bin/env python3
"""Compare required candidate inputs with trusted mounted inputs without following symlinks."""

from __future__ import annotations

import hashlib
import os
import stat
from pathlib import Path


CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other(mode={oct(mode)})"


def compare_file(candidate: Path, trusted: Path) -> list[str]:
    findings: list[str] = []
    if not os.path.lexists(candidate):
        return [f"MISSING {candidate}"]
    if kind(candidate) != "file":
        return [f"BAD_TYPE {candidate}: {kind(candidate)}; expected file"]
    if not trusted.is_file() or trusted.is_symlink():
        return [f"TRUSTED_INPUT_BAD_TYPE {trusted}: {kind(trusted)}"]
    candidate_hash = digest(candidate)
    trusted_hash = digest(trusted)
    if candidate_hash != trusted_hash:
        findings.append(
            f"CONTENT_MISMATCH {candidate} trusted={trusted} "
            f"candidate_sha256={candidate_hash} trusted_sha256={trusted_hash}"
        )
    else:
        findings.append(
            f"MATCH {candidate} trusted={trusted} sha256={candidate_hash}"
        )
    return findings


def tree_entries(root: Path) -> dict[str, tuple[str, str | None]]:
    entries: dict[str, tuple[str, str | None]] = {}
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        current = Path(dirpath)
        for name in sorted(dirnames + filenames):
            path = current / name
            relative = path.relative_to(root).as_posix()
            entry_kind = kind(path)
            entry_hash = digest(path) if entry_kind == "file" else None
            entries[relative] = (entry_kind, entry_hash)
    return entries


def compare_tree(candidate: Path, trusted: Path) -> list[str]:
    findings: list[str] = []
    if not os.path.lexists(candidate):
        return [f"MISSING_TREE {candidate}"]
    if kind(candidate) != "directory":
        return [f"BAD_TREE_TYPE {candidate}: {kind(candidate)}; expected directory"]
    if not trusted.is_dir() or trusted.is_symlink():
        return [f"TRUSTED_TREE_BAD_TYPE {trusted}: {kind(trusted)}"]

    candidate_entries = tree_entries(candidate)
    trusted_entries = tree_entries(trusted)
    names = sorted(set(candidate_entries) | set(trusted_entries))
    for name in names:
        candidate_item = candidate_entries.get(name)
        trusted_item = trusted_entries.get(name)
        if candidate_item is None:
            findings.append(f"MISSING_ENTRY {candidate / name}")
        elif trusted_item is None:
            findings.append(f"EXTRA_ENTRY {candidate / name} type={candidate_item[0]}")
        elif candidate_item[0] != trusted_item[0]:
            findings.append(
                f"TYPE_MISMATCH {candidate / name}: candidate={candidate_item[0]} "
                f"trusted={trusted_item[0]}"
            )
        elif candidate_item[0] == "symlink":
            findings.append(f"SYMLINK_ENTRY {candidate / name}")
        elif candidate_item[0] == "file" and candidate_item[1] != trusted_item[1]:
            findings.append(
                f"CONTENT_MISMATCH {candidate / name} "
                f"candidate_sha256={candidate_item[1]} trusted_sha256={trusted_item[1]}"
            )

    if not findings:
        findings.append(
            f"TREE_MATCH {candidate} trusted={trusted} entries={len(names)}"
        )
    return findings


def main() -> int:
    findings: list[str] = []
    print("MODE_CHECK supplied_semantics_reference_tree_present="
          f"{(REFERENCE / 'reference-semantics').is_dir()}")
    findings.extend(compare_file(CANDIDATE / "prompt.py", REFERENCE / "prompt.py"))
    findings.extend(compare_file(CANDIDATE / "py2mpy.py", REFERENCE / "py2mpy.py"))
    findings.extend(
        compare_tree(
            CANDIDATE / "reference-semantics",
            REFERENCE / "reference-semantics",
        )
    )

    for name in (
        "run-input.json",
        "metrics.json",
        "codex-last.txt",
        "codex-output.log",
    ):
        path = CANDIDATE / name
        present = os.path.lexists(path)
        print(f"GENERATION_METADATA {name}: {'present' if present else 'missing'}")
        if present:
            print(f"GENERATION_METADATA_TYPE {name}: {kind(path)}")

    trace_names = sorted(
        path.name
        for path in CANDIDATE.iterdir()
        if "trace" in path.name.lower()
    )
    print(f"STRUCTURED_TRACE_CANDIDATES: {trace_names}")

    for finding in findings:
        print(finding)

    integrity_failures = [
        finding
        for finding in findings
        if not finding.startswith(("MATCH ", "TREE_MATCH "))
    ]
    print(f"INTEGRITY_FAILURE_COUNT: {len(integrity_failures)}")
    return 1 if integrity_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
