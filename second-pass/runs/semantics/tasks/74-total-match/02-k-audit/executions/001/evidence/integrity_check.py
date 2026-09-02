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
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISLNK(mode):
        return "symlink"
    return f"other-mode-{stat.S_IFMT(mode):o}"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def walk(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    stack = [root]
    while stack:
        directory = stack.pop()
        for entry in os.scandir(directory):
            path = Path(entry.path)
            rel = str(path.relative_to(root))
            entry_kind = kind(path)
            payload = sha256(path) if entry_kind == "file" else None
            result[rel] = (entry_kind, payload)
            if entry_kind == "directory":
                stack.append(path)
    return result


print("RENDERED_MODE: SUPPLIED_SEMANTICS")
trusted_semantics = REFERENCE / "reference-semantics"
print(f"TRUSTED_SEMANTICS_PRESENT: {trusted_semantics.exists()}")
print(f"TRUSTED_SEMANTICS_KIND: {kind(trusted_semantics)}")

required_claim_artifacts = [
    "run-input.json",
    "metrics.json",
    "codex-last.txt",
    "codex-output.log",
]
for name in required_claim_artifacts:
    path = CANDIDATE / name
    print(
        f"UNTRUSTED_CLAIM_ARTIFACT {name}: "
        f"{'present' if os.path.lexists(path) else 'missing'}"
    )

required_source_artifacts = [
    "prompt.py",
    "py2mpy.py",
    "solution.py",
    "solution.mpy",
    "spec.k",
    "verification.k",
    "reference-semantics",
]
for name in required_source_artifacts:
    path = CANDIDATE / name
    print(
        f"REQUIRED_SOURCE_ARTIFACT {name}: "
        f"{kind(path) if os.path.lexists(path) else 'missing'}"
    )

for name in ("prompt.py", "py2mpy.py"):
    candidate_path = CANDIDATE / name
    reference_path = REFERENCE / name
    same = (
        candidate_path.is_file()
        and not candidate_path.is_symlink()
        and candidate_path.read_bytes() == reference_path.read_bytes()
    )
    print(
        f"TRUSTED_FILE_COMPARE {name}: {'IDENTICAL' if same else 'DIFFERENT'} "
        f"candidate_sha256={sha256(candidate_path) if candidate_path.is_file() else 'NA'} "
        f"trusted_sha256={sha256(reference_path)}"
    )

candidate_tree = walk(CANDIDATE / "reference-semantics")
trusted_tree = walk(trusted_semantics)
all_names = sorted(candidate_tree.keys() | trusted_tree.keys())
differences = 0
for name in all_names:
    candidate_value = candidate_tree.get(name)
    trusted_value = trusted_tree.get(name)
    if candidate_value != trusted_value:
        differences += 1
        print(
            "SEMANTICS_DIFFERENCE "
            f"{name}: candidate={candidate_value!r} trusted={trusted_value!r}"
        )
print(f"SEMANTICS_ENTRY_COUNT candidate={len(candidate_tree)} trusted={len(trusted_tree)}")
print(f"SEMANTICS_DIFFERENCE_COUNT: {differences}")

print("CANDIDATE_TOP_LEVEL:")
for path in sorted(CANDIDATE.iterdir()):
    print(f"  {kind(path):12s} {path.name}")
