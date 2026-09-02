#!/usr/bin/env python3
"""Compare fresh generated-semantics executions with trusted Python."""

import importlib.util
import json
import shlex
import subprocess
import sys
from pathlib import Path


def load_entry(path: Path):
    spec = importlib.util.spec_from_file_location("trusted_canonical_for_krun", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.circular_shift


canonical = load_entry(Path("/reference/canonical.py"))
program = "/tmp/audit-work/candidate-src/solution.mpy"
definition = "/tmp/audit-work/build/semantic-kompiled"
cases = [
    (12, 1),       # documented normal case
    (12, 2),       # shift == rendered length
    (12, 3),       # first oversized shift
    (1234, 0),     # zero shift
    (1234, 3),     # last non-equality ordinary rotation
    (1234, 4),     # branch boundary
    (1234, 5),     # oversized/reversal branch
    (0, 0),        # smallest nonnegative integer
    (0, 1),        # one-character boundary
    (-12, 1),      # sign is part of Python's string
    (-12, 4),      # negative x, oversized branch
    (1234, -1),    # uncovered-by-spec but executable boundary
]

failures = []
for index, (x, shift) in enumerate(cases):
    expected = canonical(x, shift)
    command = [
        "krun",
        program,
        "--definition",
        definition,
        f'-cENTRY="circular_shift"',
        f"-cARGS=VInt({x}), VInt({shift})",
    ]
    completed = subprocess.run(
        command,
        cwd="/tmp/audit-work/candidate-src",
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    needle = f'VString ( {json.dumps(expected)} )'
    matched = completed.returncode == 0 and needle in completed.stdout
    print(f"CASE {index}: x={x} shift={shift} expected={expected!r}")
    print(f"COMMAND: {shlex.join(command)}")
    print(completed.stdout, end="" if completed.stdout.endswith("\n") else "\n")
    print(f"KRUN_EXIT_STATUS: {completed.returncode}")
    print(f"EXPECTED_RESULT_FRAGMENT: {needle}")
    print(f"MATCH: {matched}")
    if not matched:
        failures.append(
            {
                "index": index,
                "x": x,
                "shift": shift,
                "expected": expected,
                "returncode": completed.returncode,
            }
        )

print(
    json.dumps(
        {"case_count": len(cases), "failure_count": len(failures), "failures": failures},
        sort_keys=True,
    )
)
sys.exit(1 if failures else 0)
