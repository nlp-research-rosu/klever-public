#!/usr/bin/env python3
"""Compare fresh generated-semantics execution with independent Python."""

from __future__ import annotations

from collections import Counter
import importlib.util
from pathlib import Path
import re
import shlex
import subprocess
import sys


SCRATCH = Path("/tmp/audit-work/candidate-fresh")
DEFINITION = SCRATCH / "semantic-llvm-kompiled"


def load_entry(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_sorted


canonical = load_entry(Path("/reference/canonical.py"), "canonical_stage3")
candidate = load_entry(SCRATCH / "solution.py", "candidate_stage3")


def oracle(values: list[int]) -> bool:
    counts = Counter(values)
    return all(
        values[index - 1] <= values[index] for index in range(1, len(values))
    ) and all(value <= 2 for value in counts.values())


def k_list(values: list[int]) -> str:
    result = "Nil"
    for value in reversed(values):
        result = f"Cons({value}, {result})"
    return f"PyList({result})"


cases = [
    [],
    [5],
    [0, 0],
    [0, 0, 0],
    [0, 1, 1],
    [0, 1, 1, 1],
    [2, 1],
    [1, 3, 2, 4, 5],
    [1, 2, 2, 3, 3, 4],
    [1, 2, 2, 2, 3, 4],
    [0, 10**40],
    [10**40, 0],
]

failures: list[str] = []
for values in cases:
    argument = k_list(values)
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        str(DEFINITION),
        f"-cARGS={argument}",
    ]
    print(f"COMMAND: {shlex.join(command)}")
    completed = subprocess.run(
        command,
        cwd=SCRATCH,
        text=True,
        capture_output=True,
        check=False,
    )
    print(f"KRUN_EXIT_STATUS={completed.returncode}")
    print("KRUN_STDOUT_BEGIN")
    print(completed.stdout.rstrip())
    print("KRUN_STDOUT_END")
    if completed.stderr:
        print("KRUN_STDERR_BEGIN")
        print(completed.stderr.rstrip())
        print("KRUN_STDERR_END")
    match = re.search(r"BoolVal\s*\(\s*(true|false)\s*\)", completed.stdout)
    k_result = None if match is None else match.group(1) == "true"
    canonical_result = canonical(values.copy())
    candidate_result = candidate(values.copy())
    oracle_result = oracle(values)
    print(
        f"RESULT input={values!r} K={k_result!r} canonical={canonical_result!r} "
        f"candidate={candidate_result!r} oracle={oracle_result!r}"
    )
    if (
        completed.returncode != 0
        or k_result is None
        or not (
            k_result == canonical_result == candidate_result == oracle_result
        )
    ):
        failures.append(f"mismatch or execution failure on {values!r}")

print(f"CASE_COUNT={len(cases)}")
print(f"FAILURE_COUNT={len(failures)}")
for failure in failures:
    print(f"FAIL: {failure}")
sys.exit(1 if failures else 0)
