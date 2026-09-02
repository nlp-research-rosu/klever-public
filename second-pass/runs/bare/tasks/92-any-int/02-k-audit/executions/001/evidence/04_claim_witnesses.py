#!/usr/bin/env python3
"""Ground witnesses for every entry-claim precondition."""

from __future__ import annotations

import importlib.util
import re
import subprocess
from pathlib import Path


DEFINITION = Path("/tmp/audit-work/92-any-int/concrete-kompiled")


def load_function(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.any_int


canonical = load_function(
    "claim_witness_canonical",
    Path("/tmp/audit-work/92-any-int/trusted/canonical.py"),
)
generated = load_function(
    "claim_witness_generated",
    Path("/tmp/audit-work/92-any-int/src/solution.py"),
)

witnesses = [
    (
        "int-first",
        (1, 2, 3),
        "RunAnyInt(intVal(1), intVal(2), intVal(3))",
        True,
        "1 + 2 == 3",
    ),
    (
        "int-second",
        (1, 3, 2),
        "RunAnyInt(intVal(1), intVal(3), intVal(2))",
        True,
        "not (1 + 3 == 2) and 1 + 2 == 3",
    ),
    (
        "int-third",
        (3, 1, 2),
        "RunAnyInt(intVal(3), intVal(1), intVal(2))",
        True,
        "not (3 + 1 == 2) and not (3 + 2 == 1) and 1 + 2 == 3",
    ),
    (
        "int-none",
        (1, 1, 1),
        "RunAnyInt(intVal(1), intVal(1), intVal(1))",
        False,
        "all three pair-sum equalities are false",
    ),
    (
        "nonint-first",
        (1.5, 1, 2),
        "RunAnyInt(floatVal(1.5), intVal(1), intVal(2))",
        False,
        "first argument has sort NonIntVal",
    ),
    (
        "nonint-second",
        (1, 1.5, 2),
        "RunAnyInt(intVal(1), floatVal(1.5), intVal(2))",
        False,
        "first argument IntVal and second NonIntVal",
    ),
    (
        "nonint-third",
        (1, 2, 3.0),
        "RunAnyInt(intVal(1), intVal(2), floatVal(3.0))",
        False,
        "first two arguments IntVal and third NonIntVal",
    ),
]

failures = 0
for label, args, term, claimed, precondition in witnesses:
    command = ["krun", "-d", str(DEFINITION), f"-cPGM={term}"]
    completed = subprocess.run(
        command,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    match = re.search(r"boolVal\s*\(\s*(true|false)\s*\)", completed.stdout)
    k_result = None if match is None else match.group(1) == "true"
    generated_result = generated(*args)
    canonical_result = canonical(*args)
    accepted = (
        completed.returncode == 0
        and k_result is claimed
        and generated_result is claimed
        and canonical_result is claimed
    )
    print(f"CLAIM: {label}")
    print(f"PRECONDITION_WITNESS: {precondition}")
    print(f"PYTHON_ARGS: {args!r}")
    print(f"CLAIMED_RESULT: {claimed!r}")
    print(f"GENERATED_PYTHON_RESULT: {generated_result!r}")
    print(f"CANONICAL_PYTHON_RESULT: {canonical_result!r}")
    print("COMMAND:", " ".join(command))
    print(f"EXIT_STATUS: {completed.returncode}")
    print(f"K_RESULT: {k_result!r}")
    print(f"ALL_AGREE: {accepted}")
    if not accepted:
        failures += 1

print(f"SUMMARY: witnesses={len(witnesses)} failures={failures}")
raise SystemExit(1 if failures else 0)
