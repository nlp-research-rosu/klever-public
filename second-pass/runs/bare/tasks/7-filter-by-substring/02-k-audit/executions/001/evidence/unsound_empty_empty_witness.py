#!/usr/bin/env python3
"""Ground witness for the generated containsString rule's false conclusion."""

from __future__ import annotations

import importlib.util
import shlex
import subprocess
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.filter_by_substring


def main() -> int:
    canonical = load(Path("/reference/canonical.py"), "canonical_witness")
    candidate = load(
        Path("/tmp/audit-work/7-filter-by-substring/solution.py"),
        "candidate_witness",
    )
    command = [
        "krun",
        "/tmp/audit-work/7-filter-by-substring/solution.mpy",
        "--definition",
        "/tmp/audit-work/7-filter-by-substring/semantic-llvm-kompiled",
        '-cFUNCTION="filter_by_substring"',
        '-cINPUT=Cons("",Nil)',
        '-cSUBSTRING=""',
    ]
    completed = subprocess.run(command, text=True, capture_output=True)

    print('INTENDED_DOMAIN_INPUT: strings=[""], substring=""')
    print(f'PYTHON_MEMBERSHIP: {"" in ""}')
    print(f"TRUSTED_CANONICAL_RESULT: {canonical([''], '')!r}")
    print(f"CANDIDATE_PYTHON_RESULT: {candidate([''], '')!r}")
    print(f"COMMAND: {shlex.join(command)}")
    print(f"KRUN_EXIT_STATUS: {completed.returncode}")
    print("KRUN_STDOUT:")
    print(completed.stdout.rstrip())
    if completed.stderr:
        print("KRUN_STDERR:")
        print(completed.stderr.rstrip())

    witnessed = (
        completed.returncode == 0
        and canonical([""], "") == [""]
        and candidate([""], "") == [""]
        and "Nil ~> .K" in completed.stdout
    )
    print(f"FALSE_CONCLUSION_WITNESSED: {str(witnessed).lower()}")
    return 0 if witnessed else 1


if __name__ == "__main__":
    raise SystemExit(main())
