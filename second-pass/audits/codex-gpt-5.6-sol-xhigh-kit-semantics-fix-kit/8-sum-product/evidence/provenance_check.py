#!/usr/bin/env python3
"""Reviewer-owned integrity check; never imports or executes candidate code."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path


CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
REQUIRED_FILES = (
    "run-input.json",
    "metrics.json",
    "codex-last.txt",
    "codex-output.log",
    "prompt.py",
    "py2mpy.py",
    "solution.py",
    "solution.mpy",
    "verification.k",
    "spec.k",
    "prove.sh",
    "PROOF.md",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def entry_kind(path: Path) -> str:
    if path.is_symlink():
        return "symlink"
    if path.is_file():
        return "file"
    if path.is_dir():
        return "directory"
    return "other"


def manifest(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for current, directories, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        for name in sorted(directories + files):
            path = current_path / name
            relative = str(path.relative_to(root))
            kind = entry_kind(path)
            result[relative] = (kind, sha256(path) if kind == "file" else None)
    return result


def main() -> int:
    failures: list[str] = []
    print("rendered_semantics_mode=SUPPLIED_SEMANTICS")
    trusted_semantics = REFERENCE / "reference-semantics"
    candidate_semantics = CANDIDATE / "reference-semantics"
    print(f"trusted_semantics_kind={entry_kind(trusted_semantics)}")
    print(f"candidate_semantics_kind={entry_kind(candidate_semantics)}")
    if entry_kind(trusted_semantics) != "directory":
        failures.append("trusted reference-semantics is not a directory")
    if entry_kind(candidate_semantics) != "directory":
        failures.append("candidate reference-semantics is not a directory")

    for relative in REQUIRED_FILES:
        path = CANDIDATE / relative
        kind = entry_kind(path)
        print(f"required {relative}: {kind}")
        if kind != "file":
            failures.append(f"required artifact {relative} has kind {kind}")

    trace_paths = sorted((CANDIDATE / "codex-trace").rglob("*.jsonl"))
    print(f"structured_trace_count={len(trace_paths)}")
    for path in trace_paths:
        print(f"structured_trace={path} kind={entry_kind(path)} sha256={sha256(path)}")
        if entry_kind(path) != "file":
            failures.append(f"structured trace is not a regular file: {path}")

    comparisons = (
        (CANDIDATE / "prompt.py", REFERENCE / "prompt.py", "prompt"),
        (CANDIDATE / "py2mpy.py", REFERENCE / "py2mpy.py", "translator"),
    )
    for candidate_path, reference_path, label in comparisons:
        candidate_hash = sha256(candidate_path)
        reference_hash = sha256(reference_path)
        equal = candidate_hash == reference_hash
        print(
            f"{label}_candidate_sha256={candidate_hash}\n"
            f"{label}_reference_sha256={reference_hash}\n"
            f"{label}_byte_equal={str(equal).lower()}"
        )
        if not equal:
            failures.append(f"{label} differs from trusted input")

    if entry_kind(trusted_semantics) == entry_kind(candidate_semantics) == "directory":
        trusted_manifest = manifest(trusted_semantics)
        candidate_manifest = manifest(candidate_semantics)
        all_names = sorted(set(trusted_manifest) | set(candidate_manifest))
        for relative in all_names:
            trusted_entry = trusted_manifest.get(relative)
            candidate_entry = candidate_manifest.get(relative)
            same = trusted_entry == candidate_entry
            print(
                f"semantics_entry {relative}: trusted={trusted_entry} "
                f"candidate={candidate_entry} equal={str(same).lower()}"
            )
            if not same:
                failures.append(f"semantics integrity mismatch: {relative}")

    print(f"integrity_failure_count={len(failures)}")
    for failure in failures:
        print(f"INTEGRITY_FAILURE: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
