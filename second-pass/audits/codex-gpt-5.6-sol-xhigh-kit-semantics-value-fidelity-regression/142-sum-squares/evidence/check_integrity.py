#!/usr/bin/env python3
"""Independent provenance and supplied-semantics integrity checks."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import stat


CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def entry_kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISLNK(mode):
        return "symlink"
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "directory"
    return f"other({mode:o})"


def tree(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for directory, directory_names, file_names in os.walk(
        root, topdown=True, followlinks=False
    ):
        directory_path = Path(directory)
        names = sorted(directory_names + file_names)
        for name in names:
            path = directory_path / name
            relative = path.relative_to(root).as_posix()
            kind = entry_kind(path)
            content_hash = digest(path) if kind == "file" else None
            if kind == "symlink":
                content_hash = os.readlink(path)
            result[relative] = (kind, content_hash)
    return result


def compare_tree(trusted: Path, submitted: Path) -> list[str]:
    trusted_entries = tree(trusted)
    submitted_entries = tree(submitted)
    differences: list[str] = []
    for name in sorted(trusted_entries.keys() - submitted_entries.keys()):
        differences.append(f"MISSING {name}: trusted={trusted_entries[name]}")
    for name in sorted(submitted_entries.keys() - trusted_entries.keys()):
        differences.append(f"ADDITIONAL {name}: submitted={submitted_entries[name]}")
    for name in sorted(trusted_entries.keys() & submitted_entries.keys()):
        if trusted_entries[name] != submitted_entries[name]:
            differences.append(
                f"CHANGED_OR_MISTYPED {name}: "
                f"trusted={trusted_entries[name]} submitted={submitted_entries[name]}"
            )
    return differences


required_files = [
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
    "prove.sh",
    "PROOF.md",
]

print("SEMANTICS_MODE=SUPPLIED_SEMANTICS")
trusted_semantics = REFERENCE / "reference-semantics"
submitted_semantics = CANDIDATE / "reference-semantics"
print(f"trusted-semantics-kind={entry_kind(trusted_semantics)}")
print(f"candidate-semantics-kind={entry_kind(submitted_semantics)}")
differences = compare_tree(trusted_semantics, submitted_semantics)
print(f"semantics-entry-count-trusted={len(tree(trusted_semantics))}")
print(f"semantics-entry-count-candidate={len(tree(submitted_semantics))}")
print(f"semantics-difference-count={len(differences)}")
for difference in differences:
    print(difference)

for name in required_files:
    path = CANDIDATE / name
    if not path.exists() and not path.is_symlink():
        print(f"REQUIRED {name}: MISSING")
    else:
        print(f"REQUIRED {name}: {entry_kind(path)}")

trace_files = sorted((CANDIDATE / "codex-trace").rglob("*"))
trace_regular = [path for path in trace_files if entry_kind(path) == "file"]
trace_bad = [
    path
    for path in trace_files
    if entry_kind(path) not in {"file", "directory"}
]
print(f"structured-trace-files={len(trace_regular)}")
for path in trace_regular:
    print(
        f"TRACE {path.relative_to(CANDIDATE)} "
        f"sha256={digest(path)} bytes={path.stat().st_size}"
    )
for path in trace_bad:
    print(f"TRACE_MISTYPED {path}: {entry_kind(path)}")

for relative, trusted in [
    ("prompt.py", REFERENCE / "prompt.py"),
    ("py2mpy.py", REFERENCE / "py2mpy.py"),
]:
    submitted = CANDIDATE / relative
    same = (
        entry_kind(submitted) == "file"
        and digest(trusted) == digest(submitted)
    )
    print(
        f"TRUSTED_COMPARE {relative}: same={same} "
        f"trusted_sha256={digest(trusted)} "
        f"candidate_sha256={digest(submitted) if submitted.is_file() else 'N/A'}"
    )

candidate_links = [
    path for path in CANDIDATE.rglob("*") if entry_kind(path) == "symlink"
]
print(f"candidate-symlink-count={len(candidate_links)}")
for path in candidate_links:
    print(f"SYMLINK {path} -> {os.readlink(path)}")

failed = bool(differences or trace_bad or candidate_links)
failed = failed or any(
    not (CANDIDATE / name).is_file() for name in required_files
)
failed = failed or any(
    digest(REFERENCE / name) != digest(CANDIDATE / name)
    for name in ("prompt.py", "py2mpy.py")
)
raise SystemExit(1 if failed else 0)
