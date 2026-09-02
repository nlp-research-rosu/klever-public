#!/usr/bin/env python3
"""Independent byte/type/symlink integrity checks for audit stage 1."""

from __future__ import annotations

import hashlib
import os
import stat
from pathlib import Path


CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
PROVENANCE = (
    "run-input.json",
    "metrics.json",
    "codex-last.txt",
    "codex-output.log",
)
REQUIRED_CANDIDATE = (
    "prompt.py",
    "py2mpy.py",
    "solution.py",
    "solution.mpy",
    "spec.k",
    "verification.k",
    "reference-semantics",
)


def kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other({stat.S_IFMT(mode):o})"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(131072), b""):
            digest.update(block)
    return digest.hexdigest()


def inventory(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for directory, names, files in os.walk(root, followlinks=False):
        base = Path(directory)
        for name in sorted(names + files):
            path = base / name
            rel = path.relative_to(root).as_posix()
            entry_kind = kind(path)
            payload = sha256(path) if entry_kind == "file" else None
            result[rel] = (entry_kind, payload)
    return result


def compare_file(candidate: Path, reference: Path) -> bool:
    if not candidate.exists() and not candidate.is_symlink():
        print(f"FILE {candidate.name}: MISSING")
        return False
    ckind = kind(candidate)
    rkind = kind(reference)
    if ckind != "file" or rkind != "file":
        print(f"FILE {candidate.name}: TYPE_MISMATCH candidate={ckind} reference={rkind}")
        return False
    chash = sha256(candidate)
    rhash = sha256(reference)
    equal = chash == rhash and candidate.read_bytes() == reference.read_bytes()
    print(
        f"FILE {candidate.name}: {'IDENTICAL' if equal else 'CHANGED'} "
        f"candidate_sha256={chash} reference_sha256={rhash}"
    )
    return equal


def main() -> int:
    failures = 0
    provenance_missing = 0
    print("SEMANTICS_MODE: SUPPLIED_SEMANTICS")
    trusted_semantics = REFERENCE / "reference-semantics"
    print(
        "TRUSTED_SEMANTICS_MOUNT:",
        f"{kind(trusted_semantics) if trusted_semantics.exists() else 'MISSING'}",
    )
    if not trusted_semantics.is_dir() or trusted_semantics.is_symlink():
        failures += 1

    for rel in REQUIRED_CANDIDATE:
        path = CANDIDATE / rel
        if not path.exists() and not path.is_symlink():
            print(f"REQUIRED {rel}: MISSING")
            failures += 1
        else:
            entry_kind = kind(path)
            print(f"REQUIRED {rel}: {entry_kind}")
            if entry_kind == "symlink":
                failures += 1

    for rel in PROVENANCE:
        path = CANDIDATE / rel
        if not path.exists() and not path.is_symlink():
            print(f"PROVENANCE {rel}: MISSING")
            provenance_missing += 1
        else:
            print(f"PROVENANCE {rel}: {kind(path)}")
            if kind(path) == "symlink":
                failures += 1

    if not compare_file(CANDIDATE / "prompt.py", REFERENCE / "prompt.py"):
        failures += 1
    if not compare_file(CANDIDATE / "py2mpy.py", REFERENCE / "py2mpy.py"):
        failures += 1

    candidate_tree = inventory(CANDIDATE / "reference-semantics")
    trusted_tree = inventory(trusted_semantics)
    all_paths = sorted(set(candidate_tree) | set(trusted_tree))
    for rel in all_paths:
        candidate_entry = candidate_tree.get(rel)
        trusted_entry = trusted_tree.get(rel)
        if candidate_entry is None:
            print(f"SEMANTICS {rel}: MISSING")
            failures += 1
        elif trusted_entry is None:
            print(f"SEMANTICS {rel}: ADDITIONAL candidate={candidate_entry}")
            failures += 1
        elif candidate_entry[0] == "symlink":
            print(f"SEMANTICS {rel}: SYMLINK")
            failures += 1
        elif candidate_entry != trusted_entry:
            print(
                f"SEMANTICS {rel}: MISMATCH "
                f"candidate={candidate_entry} trusted={trusted_entry}"
            )
            failures += 1
        else:
            print(f"SEMANTICS {rel}: IDENTICAL {candidate_entry[0]}")

    print(f"PROVENANCE_MISSING_COUNT: {provenance_missing}")
    print(f"SOURCE_OR_SEMANTICS_INTEGRITY_FAILURE_COUNT: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
