#!/usr/bin/env python3
"""Reviewer-authored source/provenance integrity checks for 23-strlen."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path


CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def classify(path: Path) -> str:
    if not path.exists() and not path.is_symlink():
        return "missing"
    if path.is_symlink():
        return "symlink"
    if path.is_file():
        return "file"
    if path.is_dir():
        return "directory"
    return "other"


def tree(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for parent, dirs, files in os.walk(root, followlinks=False):
        for name in sorted(dirs + files):
            path = Path(parent) / name
            rel = str(path.relative_to(root))
            kind = classify(path)
            result[rel] = (kind, digest(path) if kind == "file" else None)
    return result


failures: list[str] = []

for rel, (kind, sha256) in sorted(tree(CANDIDATE).items()):
    print(f"CANDIDATE_ENTRY {rel} kind={kind} sha256={sha256}")

for candidate_name, reference_name in (
    ("prompt.py", "prompt.py"),
    ("py2mpy.py", "py2mpy.py"),
):
    candidate_path = CANDIDATE / candidate_name
    reference_path = REFERENCE / reference_name
    if classify(candidate_path) != "file":
        failures.append(f"{candidate_path}: required regular file missing or mistyped")
        continue
    if candidate_path.read_bytes() != reference_path.read_bytes():
        failures.append(f"{candidate_path}: differs from {reference_path}")
    print(
        f"MATCH {candidate_path} {reference_path} "
        f"sha256={digest(candidate_path)}"
    )

trusted_semantics = REFERENCE / "reference-semantics"
candidate_semantics = CANDIDATE / "reference-semantics"
print(f"SEMANTICS_ROOT {trusted_semantics}: {classify(trusted_semantics)}")
print(f"SEMANTICS_ROOT {candidate_semantics}: {classify(candidate_semantics)}")
if classify(trusted_semantics) != "directory":
    failures.append("trusted supplied-semantics tree is absent or mistyped")
if classify(candidate_semantics) != "directory":
    failures.append("candidate supplied-semantics tree is absent or mistyped")
else:
    trusted_tree = tree(trusted_semantics)
    candidate_tree = tree(candidate_semantics)
    for rel in sorted(set(trusted_tree) | set(candidate_tree)):
        trusted_entry = trusted_tree.get(rel)
        candidate_entry = candidate_tree.get(rel)
        print(f"SEMANTICS_ENTRY {rel} trusted={trusted_entry} candidate={candidate_entry}")
        if trusted_entry != candidate_entry:
            failures.append(
                f"reference-semantics/{rel}: trusted={trusted_entry}, "
                f"candidate={candidate_entry}"
            )

required_candidate_sources = (
    "solution.py",
    "solution.mpy",
    "spec.k",
    "verification.k",
)
for name in required_candidate_sources:
    path = CANDIDATE / name
    kind = classify(path)
    print(f"REQUIRED_SOURCE {path}: {kind}")
    if kind != "file":
        failures.append(f"{path}: required regular source file missing or mistyped")

for name in (
    "run-input.json",
    "metrics.json",
    "codex-last.txt",
    "codex-output.log",
):
    path = CANDIDATE / name
    print(f"GENERATION_RECORD {path}: {classify(path)}")

traces = sorted(
    str(path)
    for path in CANDIDATE.iterdir()
    if path.is_file()
    and ("trace" in path.name.lower() or path.suffix in {".json", ".jsonl"})
)
print(f"STRUCTURED_TRACE_CANDIDATES {traces}")

print(f"INTEGRITY_FAILURE_COUNT {len(failures)}")
for failure in failures:
    print(f"INTEGRITY_FAILURE {failure}")
raise SystemExit(1 if failures else 0)
