#!/usr/bin/env python3
"""Mechanical provenance and artifact-type checks for the audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
TRACE = (
    CANDIDATE
    / "codex-trace/2026/07/22"
    / "rollout-2026-07-22T04-25-08-019f8924-a678-7523-92c2-c4d5490703c0.jsonl"
)

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
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def kind(path: Path) -> str:
    try:
        mode = path.lstat().st_mode
    except FileNotFoundError:
        return "missing"
    if stat.S_ISLNK(mode):
        return "symlink"
    if stat.S_ISREG(mode):
        return "regular"
    if stat.S_ISDIR(mode):
        return "directory"
    return "other"


def main() -> int:
    required = {name: kind(CANDIDATE / name) for name in REQUIRED_REGULAR}
    all_symlinks = [
        str(path)
        for path in CANDIDATE.rglob("*")
        if path.is_symlink()
    ]
    boundary = kind(REFERENCE / "reference-semantics")

    with (CANDIDATE / "run-input.json").open(encoding="utf-8") as stream:
        run_input = json.load(stream)
    with (CANDIDATE / "metrics.json").open(encoding="utf-8") as stream:
        metrics = json.load(stream)

    trace_records = 0
    trace_bad_json = 0
    with TRACE.open(encoding="utf-8") as stream:
        for line in stream:
            trace_records += 1
            try:
                json.loads(line)
            except json.JSONDecodeError:
                trace_bad_json += 1

    report = {
        "required_candidate_artifact_kinds": required,
        "candidate_symlinks_recursive": all_symlinks,
        "generated_semantics_boundary_reference_semantics_kind": boundary,
        "trusted_comparisons": {
            "prompt": {
                "candidate_sha256": digest(CANDIDATE / "prompt.py"),
                "reference_sha256": digest(REFERENCE / "prompt.py"),
                "byte_identical": (CANDIDATE / "prompt.py").read_bytes()
                == (REFERENCE / "prompt.py").read_bytes(),
            },
            "translator": {
                "candidate_sha256": digest(CANDIDATE / "py2mpy.py"),
                "reference_sha256": digest(REFERENCE / "py2mpy.py"),
                "byte_identical": (CANDIDATE / "py2mpy.py").read_bytes()
                == (REFERENCE / "py2mpy.py").read_bytes(),
            },
        },
        "untrusted_claim_files": {
            "run_input": run_input,
            "metrics": metrics,
            "codex_last_sha256": digest(CANDIDATE / "codex-last.txt"),
            "codex_output_sha256": digest(CANDIDATE / "codex-output.log"),
            "structured_trace": str(TRACE),
            "structured_trace_sha256": digest(TRACE),
            "structured_trace_records": trace_records,
            "structured_trace_bad_json_records": trace_bad_json,
        },
        "top_level_entries": sorted(path.name for path in CANDIDATE.iterdir()),
    }
    print(json.dumps(report, indent=2, sort_keys=True))

    failures = []
    failures.extend(
        name for name, entry_kind in required.items() if entry_kind != "regular"
    )
    if all_symlinks:
        failures.append("recursive symlink(s)")
    if boundary != "missing":
        failures.append("forbidden /reference/reference-semantics")
    for comparison in report["trusted_comparisons"].values():
        if not comparison["byte_identical"]:
            failures.append("trusted-input mismatch")
    if trace_bad_json:
        failures.append("malformed trace record(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
