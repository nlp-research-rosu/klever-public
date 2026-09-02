#!/usr/bin/env python3
"""Independent provenance and supplied-semantics integrity checks."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path


CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")


def kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if path.is_symlink():
        return "symlink"
    if path.is_file():
        return "file"
    if path.is_dir():
        return "dir"
    return f"other({mode:o})"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def tree(root: Path) -> dict[str, tuple[str, str | None]]:
    entries: dict[str, tuple[str, str | None]] = {}
    for current, directories, files in os.walk(root, followlinks=False):
        base = Path(current)
        for name in sorted(directories + files):
            path = base / name
            relative = path.relative_to(root).as_posix()
            entry_kind = kind(path)
            entries[relative] = (
                entry_kind,
                digest(path) if entry_kind == "file" else None,
            )
    return entries


def compare_file(label: str, candidate: Path, trusted: Path) -> None:
    if not candidate.exists() and not candidate.is_symlink():
        print(f"{label}: MISSING candidate={candidate}")
        return
    if kind(candidate) != "file":
        print(f"{label}: MISTYPED candidate={candidate} kind={kind(candidate)}")
        return
    if not trusted.is_file() or trusted.is_symlink():
        print(f"{label}: TRUSTED_INPUT_INVALID trusted={trusted} kind={kind(trusted)}")
        return
    candidate_hash = digest(candidate)
    trusted_hash = digest(trusted)
    status = "IDENTICAL" if candidate_hash == trusted_hash else "CHANGED"
    print(
        f"{label}: {status} candidate_sha256={candidate_hash} "
        f"trusted_sha256={trusted_hash}"
    )


required_claim_artifacts = [
    "run-input.json",
    "metrics.json",
    "codex-last.txt",
    "codex-output.log",
    "solution.py",
    "solution.mpy",
    "spec.k",
    "verification.k",
    "prompt.py",
    "py2mpy.py",
]

print("MODE: SUPPLIED_SEMANTICS")
trusted_semantics = REFERENCE / "reference-semantics"
print(
    "TRUSTED_SEMANTICS_PRESENT:",
    trusted_semantics.is_dir() and not trusted_semantics.is_symlink(),
    f"path={trusted_semantics}",
)

for relative in required_claim_artifacts:
    path = CANDIDATE / relative
    if not path.exists() and not path.is_symlink():
        print(f"REQUIRED_ARTIFACT {relative}: MISSING")
    else:
        print(f"REQUIRED_ARTIFACT {relative}: PRESENT kind={kind(path)}")

compare_file("PROMPT", CANDIDATE / "prompt.py", REFERENCE / "prompt.py")
compare_file("TRANSLATOR", CANDIDATE / "py2mpy.py", REFERENCE / "py2mpy.py")

candidate_semantics = CANDIDATE / "reference-semantics"
if not candidate_semantics.exists() and not candidate_semantics.is_symlink():
    print("SEMANTICS_ROOT: MISSING")
elif kind(candidate_semantics) != "dir":
    print(f"SEMANTICS_ROOT: MISTYPED kind={kind(candidate_semantics)}")
else:
    candidate_tree = tree(candidate_semantics)
    trusted_tree = tree(trusted_semantics)
    for relative in sorted(set(candidate_tree) | set(trusted_tree)):
        candidate_entry = candidate_tree.get(relative)
        trusted_entry = trusted_tree.get(relative)
        if candidate_entry is None:
            print(f"SEMANTICS {relative}: MISSING")
        elif trusted_entry is None:
            print(
                f"SEMANTICS {relative}: ADDITIONAL "
                f"candidate_kind={candidate_entry[0]}"
            )
        elif candidate_entry[0] != trusted_entry[0]:
            print(
                f"SEMANTICS {relative}: MISTYPED "
                f"candidate_kind={candidate_entry[0]} trusted_kind={trusted_entry[0]}"
            )
        elif candidate_entry[0] == "symlink":
            print(f"SEMANTICS {relative}: SYMLINK")
        elif candidate_entry[1] != trusted_entry[1]:
            print(
                f"SEMANTICS {relative}: CHANGED "
                f"candidate_sha256={candidate_entry[1]} "
                f"trusted_sha256={trusted_entry[1]}"
            )
        else:
            print(
                f"SEMANTICS {relative}: IDENTICAL "
                f"kind={candidate_entry[0]} sha256={candidate_entry[1] or '-'}"
            )
