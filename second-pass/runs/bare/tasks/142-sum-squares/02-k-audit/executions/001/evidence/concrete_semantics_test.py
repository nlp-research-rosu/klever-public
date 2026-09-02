#!/usr/bin/env python3
"""Run the freshly built generated K semantics and compare with Python."""

from __future__ import annotations

import importlib.util
import pathlib
import re
import shlex
import subprocess


WORK = pathlib.Path("/tmp/audit-work/reconstruction")
DEFINITION = WORK / "semantic-llvm-kompiled"
PROGRAM = WORK / "regenerated-solution.mpy"


def load_entry(name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sum_squares


canonical = load_entry(
    "concrete_canonical",
    pathlib.Path("/tmp/audit-work/differential/trusted_canonical.py"),
)
candidate = load_entry(
    "concrete_candidate",
    pathlib.Path("/tmp/audit-work/differential/generated_solution.py"),
)


def listval(values):
    if not values:
        return "ListVal(.Ints)"
    return "ListVal(" + ", ".join(str(item) for item in values) + ")"


cases = [
    ("empty", []),
    ("example-positive", [1, 2, 3]),
    ("example-negative", [-1, -5, 2, -1, -5]),
    ("index-zero-square", [-4]),
    ("index-four-cube", [0, 0, 0, 0, -3]),
    ("index-twelve-square-precedence", [0] * 12 + [-3]),
    ("large-integers", [10**30, -(10**30), 0, -1, 1]),
    ("cpython-recursion-boundary", [1] * 1000),
]

failures = 0
for name, values in cases:
    command = [
        "krun",
        str(PROGRAM),
        "--definition",
        str(DEFINITION),
        "-cARGS=" + listval(values),
    ]
    print(f"CASE {name} length={len(values)}")
    print("COMMAND " + shlex.join(command))
    try:
        run = subprocess.run(
            command,
            cwd=WORK,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=45,
            check=False,
        )
    except subprocess.TimeoutExpired:
        print("K_EXIT timeout")
        failures += 1
        continue
    print(f"K_EXIT {run.returncode}")
    matches = re.findall(r"<k>\s*VInt\s*\(\s*(-?\d+)\s*\)\s*~>\s*\.K", run.stdout)
    if not matches:
        matches = re.findall(r"<k>\s*VInt\s*\(\s*(-?\d+)\s*\)", run.stdout)
    k_result = int(matches[-1]) if matches else None
    print(f"K_RESULT {k_result!r}")
    if run.returncode != 0 or k_result is None:
        print("K_OUTPUT " + " ".join(run.stdout.split())[:1000])
        failures += 1

    canonical_result = canonical(list(values))
    print(f"CANONICAL_RESULT {canonical_result!r}")
    try:
        candidate_result = ("return", candidate(list(values)))
    except Exception as error:
        candidate_result = ("exception", type(error).__name__, str(error))
    print(f"CANDIDATE_RESULT {candidate_result!r}")

    if k_result != canonical_result:
        failures += 1
        print("K_CANONICAL_MISMATCH")
    if candidate_result == ("return", canonical_result):
        print("K_CANDIDATE_NORMAL_RETURN_MATCH")
    else:
        print("K_CANDIDATE_REAL_EXECUTION_DIVERGENCE")

print(f"FAILURES {failures}")
raise SystemExit(1 if failures else 0)
