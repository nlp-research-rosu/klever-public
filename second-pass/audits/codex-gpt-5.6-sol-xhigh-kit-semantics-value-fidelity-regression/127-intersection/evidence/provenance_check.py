#!/usr/bin/env python3
"""Independent provenance/type/hash comparison for the audit."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path


CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
REQUIRED = [
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


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def tree_manifest(root: Path) -> dict[str, tuple[str, str]]:
    result: dict[str, tuple[str, str]] = {}
    for current, dirs, files in os.walk(root, followlinks=False):
        base = Path(current)
        for name in sorted(dirs + files):
            path = base / name
            rel = path.relative_to(root).as_posix()
            if path.is_symlink():
                kind, value = "symlink", os.readlink(path)
            elif path.is_dir():
                kind, value = "dir", "-"
            elif path.is_file():
                kind, value = "file", digest(path)
            else:
                kind, value = "other", "-"
            result[rel] = (kind, value)
    return result


failures: list[str] = []
print("MODE: SUPPLIED_SEMANTICS")
trusted_semantics = REFERENCE / "reference-semantics"
print(f"trusted semantics present: {trusted_semantics.is_dir()}")
if not trusted_semantics.is_dir():
    failures.append("trusted reference-semantics is absent or not a directory")

for rel in REQUIRED:
    path = CANDIDATE / rel
    if path.is_symlink():
        status = f"SYMLINK->{os.readlink(path)}"
        failures.append(f"{rel}: symlink")
    elif path.is_file():
        status = f"file sha256={digest(path)}"
    elif path.exists():
        status = "wrong-type"
        failures.append(f"{rel}: wrong type")
    else:
        status = "missing"
        failures.append(f"{rel}: missing")
    print(f"required {rel}: {status}")

traces = sorted((CANDIDATE / "codex-trace").rglob("*.jsonl"))
print(f"structured traces: {len(traces)}")
for path in traces:
    if path.is_symlink() or not path.is_file():
        failures.append(f"trace wrong type: {path}")
    print(f"trace {path.relative_to(CANDIDATE)}: file={path.is_file()} symlink={path.is_symlink()} sha256={digest(path) if path.is_file() and not path.is_symlink() else '-'}")

for name in ("prompt.py", "py2mpy.py"):
    left = CANDIDATE / name
    right = REFERENCE / name
    same = left.is_file() and right.is_file() and left.read_bytes() == right.read_bytes()
    print(f"candidate {name} byte-identical to trusted: {same}")
    if not same:
        failures.append(f"{name}: differs from trusted")

candidate_manifest = tree_manifest(CANDIDATE / "reference-semantics")
trusted_manifest = tree_manifest(trusted_semantics)
all_names = sorted(set(candidate_manifest) | set(trusted_manifest))
print(f"candidate semantics entries: {len(candidate_manifest)}")
print(f"trusted semantics entries: {len(trusted_manifest)}")
for rel in all_names:
    c = candidate_manifest.get(rel)
    r = trusted_manifest.get(rel)
    if c != r:
        print(f"SEMANTICS MISMATCH {rel}: candidate={c} trusted={r}")
        failures.append(f"reference-semantics/{rel}: candidate={c} trusted={r}")
print(f"semantics trees recursively identical in paths/types/bytes: {candidate_manifest == trusted_manifest}")

print(f"FAILURE COUNT: {len(failures)}")
for failure in failures:
    print(f"FAILURE: {failure}")
raise SystemExit(1 if failures else 0)
