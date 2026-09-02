#!/usr/bin/env python3
"""Condition-aware provenance and filesystem integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")

REQUIRED_REGULAR = [
    "run-input.json",
    "metrics.json",
    "codex-last.txt",
    "codex-output.log",
    "prompt.py",
    "py2mpy.py",
    "solution.py",
    "solution.mpy",
    "semantic.k",
    "verification.k",
    "spec.k",
    "prove.sh",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    failures: list[str] = []
    print("rendered_semantics_mode=GENERATED_SEMANTICS")
    reference_semantics = REFERENCE / "reference-semantics"
    if os.path.lexists(reference_semantics):
        failures.append(f"mode contradiction: {reference_semantics} exists")
    print(f"reference_semantics_lexists={os.path.lexists(reference_semantics)}")

    for relative in REQUIRED_REGULAR:
        path = CANDIDATE / relative
        exists = os.path.lexists(path)
        kind = "missing"
        mode = "-"
        if exists:
            metadata = path.lstat()
            mode = stat.filemode(metadata.st_mode)
            if stat.S_ISREG(metadata.st_mode):
                kind = "regular"
            elif stat.S_ISLNK(metadata.st_mode):
                kind = "symlink"
            else:
                kind = "mistyped"
        print(f"required={relative} exists={exists} kind={kind} mode={mode}")
        if kind != "regular":
            failures.append(f"required artifact is {kind}: {path}")

    symlinks = [
        str(path)
        for path in CANDIDATE.rglob("*")
        if path.is_symlink()
    ]
    print(f"candidate_symlink_count={len(symlinks)}")
    for path in symlinks:
        print(f"candidate_symlink={path}")

    trace_files = sorted((CANDIDATE / "codex-trace").rglob("*.jsonl"))
    print(f"structured_trace_count={len(trace_files)}")
    for path in trace_files:
        print(f"structured_trace={path} size={path.stat().st_size} sha256={digest(path)}")

    for name in ("prompt.py", "py2mpy.py"):
        candidate = CANDIDATE / name
        trusted = REFERENCE / name
        same = candidate.read_bytes() == trusted.read_bytes()
        print(
            f"trusted_compare={name} byte_identical={same} "
            f"candidate_sha256={digest(candidate)} trusted_sha256={digest(trusted)}"
        )
        if not same:
            failures.append(f"candidate {name} differs from trusted mount")

    root_k = sorted(path.name for path in CANDIDATE.glob("*.k"))
    print(f"candidate_root_k_files={json.dumps(root_k)}")
    unexpected_k = sorted(set(root_k) - {"semantic.k", "verification.k", "spec.k"})
    print(f"unexpected_root_k_files={json.dumps(unexpected_k)}")

    run_input = json.loads((CANDIDATE / "run-input.json").read_text(encoding="utf-8"))
    print(f"run_input_problem_id={run_input.get('problem_id')!r}")
    print(f"run_input_condition={run_input.get('condition')!r}")
    print(f"run_input_schema_version={run_input.get('schema_version')!r}")

    generated_directories = sorted(
        path.name
        for path in CANDIDATE.iterdir()
        if path.is_dir() and (path.name.endswith("-kompiled") or path.name == "__pycache__")
    )
    print(f"ignored_candidate_generated_directories={json.dumps(generated_directories)}")
    print(f"failure_count={len(failures)}")
    for failure in failures:
        print(f"FAILURE: {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
