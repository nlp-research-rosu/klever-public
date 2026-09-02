#!/usr/bin/env python3
"""Independent provenance and tree-integrity checker for this audit."""

from __future__ import annotations

import hashlib
import os
import stat
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other(mode={oct(mode)})"


def manifest(root: Path) -> dict[str, tuple[str, str | None]]:
    entries: dict[str, tuple[str, str | None]] = {}
    for parent, directories, files in os.walk(root, followlinks=False):
        parent_path = Path(parent)
        for name in sorted([*directories, *files]):
            path = parent_path / name
            relative = path.relative_to(root).as_posix()
            entry_kind = kind(path)
            value: str | None = None
            if entry_kind == "file":
                value = sha256(path)
            elif entry_kind == "symlink":
                value = os.readlink(path)
            entries[relative] = (entry_kind, value)
    return entries


def compare(label: str, candidate: Path, trusted: Path) -> int:
    print(f"[{label}]")
    if not candidate.exists() and not candidate.is_symlink():
        print(f"MISSING ROOT: {candidate}")
        return 1
    if not trusted.exists() and not trusted.is_symlink():
        print(f"TRUSTED ROOT MISSING: {trusted}")
        return 1
    candidate_entries = manifest(candidate)
    trusted_entries = manifest(trusted)
    failures = 0
    for relative in sorted(trusted_entries.keys() - candidate_entries.keys()):
        failures += 1
        print(f"MISSING: {relative} expected={trusted_entries[relative]}")
    for relative in sorted(candidate_entries.keys() - trusted_entries.keys()):
        failures += 1
        print(f"EXTRA: {relative} actual={candidate_entries[relative]}")
    for relative in sorted(candidate_entries.keys() & trusted_entries.keys()):
        actual = candidate_entries[relative]
        expected = trusted_entries[relative]
        if actual != expected:
            failures += 1
            print(f"CHANGED_OR_MISTYPED: {relative} actual={actual} expected={expected}")
        if actual[0] == "symlink":
            failures += 1
            print(f"SYMLINK_FORBIDDEN: {relative} target={actual[1]}")
    print(f"RESULT: {'MATCH' if failures == 0 else 'MISMATCH'} failures={failures}")
    return failures


def compare_file(label: str, candidate: Path, trusted: Path) -> int:
    print(f"[{label}]")
    if not candidate.exists() and not candidate.is_symlink():
        print(f"MISSING: {candidate}")
        return 1
    candidate_kind = kind(candidate)
    trusted_kind = kind(trusted)
    if candidate_kind != "file" or trusted_kind != "file":
        print(f"MISTYPED: candidate={candidate_kind} trusted={trusted_kind}")
        return 1
    candidate_hash = sha256(candidate)
    trusted_hash = sha256(trusted)
    print(f"candidate_sha256={candidate_hash}")
    print(f"trusted_sha256={trusted_hash}")
    print(f"RESULT: {'MATCH' if candidate_hash == trusted_hash else 'MISMATCH'}")
    return int(candidate_hash != trusted_hash)


def main() -> int:
    failures = 0
    required_claim_files = [
        "run-input.json",
        "metrics.json",
        "codex-last.txt",
        "codex-output.log",
    ]
    print("[required untrusted generation records]")
    for name in required_claim_files:
        path = Path("/candidate") / name
        if not path.exists() and not path.is_symlink():
            failures += 1
            print(f"MISSING: {name}")
        else:
            entry_kind = kind(path)
            if entry_kind != "file":
                failures += 1
                print(f"MISTYPED: {name} kind={entry_kind}")
            else:
                print(f"PRESENT: {name} sha256={sha256(path)}")
    failures += compare_file(
        "prompt.py", Path("/candidate/prompt.py"), Path("/reference/prompt.py")
    )
    failures += compare_file(
        "py2mpy.py", Path("/candidate/py2mpy.py"), Path("/reference/py2mpy.py")
    )
    failures += compare(
        "reference-semantics",
        Path("/candidate/reference-semantics"),
        Path("/reference/reference-semantics"),
    )
    print(f"TOTAL_INTEGRITY_FAILURES={failures}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
