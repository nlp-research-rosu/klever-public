#!/usr/bin/env python3
"""Require the fresh false result mutation to fail for the expected reason."""

from __future__ import annotations

import importlib.util
import shlex
import subprocess
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    root = Path("/tmp/audit-work/fresh")
    canonical = load_module("trusted_canonical_vacuity", root / "trusted/canonical.py")
    candidate = load_module("submitted_solution_vacuity", root / "solution.py")
    print(f"SATISFYING_INPUT: s='b', n=1")
    print(f"CANONICAL_RESULT: {canonical.select_words('b', 1)!r}")
    print(f"CANDIDATE_RESULT: {candidate.select_words('b', 1)!r}")
    print("MUTATED_REQUIRED_RESULT: []")

    command = [
        "kprove",
        "spec-vacuity-audit.k",
        "--definition",
        "verification-kompiled",
        "--spec-module",
        "SPEC-VACUITY-AUDIT",
    ]
    print(f"COMMAND: {shlex.join(command)}")
    completed = subprocess.run(
        command,
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(f"EXIT: {completed.returncode}")
    print(completed.stdout.rstrip())
    expected_failure = (
        canonical.select_words("b", 1) == ["b"]
        and candidate.select_words("b", 1) == ["b"]
        and completed.returncode != 0
        and "WarnStuckClaimState" in completed.stdout
        and "cannot be rewritten further" in completed.stdout
        and 'WCons ( "b" , .Words )' in completed.stdout
    )
    print(f"EXPECTED_UNMET_RESULT_OBLIGATION: {expected_failure}")
    return 0 if expected_failure else 1


if __name__ == "__main__":
    raise SystemExit(main())
