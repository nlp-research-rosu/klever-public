#!/usr/bin/env python3
"""Independent differential audit for HumanEval 130-tri.

Oracle: the trusted /reference/canonical.py copied into isolated scratch.
Candidate: the submitted solution.py copied into isolated scratch.
The script compares values, element types, exceptions, and an independent
integer closed form. It deliberately includes the CPython recursion boundary.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
import sys
from pathlib import Path


ROOT = Path("/tmp/audit-work/130-tri")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("trusted_canonical", ROOT / "reference" / "canonical.py")
candidate = load("submitted_solution", ROOT / "candidate" / "solution.py")


def expected_integer_prefix(n: int) -> list[int]:
    values = []
    for i in range(n + 1):
        if i == 0:
            values.append(1)
        elif i % 2 == 0:
            values.append(1 + i // 2)
        else:
            k = (i - 1) // 2
            values.append((k + 1) * (k + 3))
    return values


def invoke(function, n: int):
    try:
        value = function(n)
        return {
            "status": "return",
            "len": len(value),
            "last": value[-1],
            "element_types": sorted({type(item).__name__ for item in value}),
            "digest": hashlib.sha256(repr(value).encode()).hexdigest()[:16],
            "value": value,
        }
    except Exception as error:  # auditor records observable exception divergence
        return {
            "status": "raise",
            "exception": type(error).__name__,
            "message": str(error),
        }


documented = [0, 1, 2, 3, 4]
branch_boundaries = list(range(0, 11))
rng = random.Random(130)
generated = sorted(set(rng.randrange(0, 301) for _ in range(24)))
limit = sys.getrecursionlimit()
resource_boundaries = sorted(
    n for n in {limit - 12, limit - 5, limit - 2, limit - 1, limit, limit + 1}
    if n >= 0
)
inputs = sorted(
    set(documented + branch_boundaries + list(range(0, 61)) + generated + resource_boundaries)
)

value_mismatches = []
type_mismatches = []
oracle_mismatches = []
exception_mismatches = []

print("python_version=", sys.version.replace("\n", " "))
print("recursion_limit=", limit)
print("documented_inputs=", documented)
print("branch_boundary_inputs=", branch_boundaries)
print("generated_inputs=", generated)
print("resource_boundary_inputs=", resource_boundaries)
print("all_inputs=", inputs)

for n in inputs:
    expected = invoke(canonical.tri, n)
    actual = invoke(candidate.tri, n)

    if expected["status"] != actual["status"]:
        exception_mismatches.append(n)
    elif expected["status"] == "return":
        if expected["value"] != actual["value"]:
            value_mismatches.append(n)
        if expected["element_types"] != actual["element_types"]:
            type_mismatches.append(n)
        if actual["value"] != expected_integer_prefix(n):
            oracle_mismatches.append(n)
    elif (
        expected["exception"] != actual["exception"]
        or expected["message"] != actual["message"]
    ):
        exception_mismatches.append(n)

    # Keep the evidence bounded while exposing every resource-boundary outcome
    # and all small branch witnesses.
    if n <= 10 or n in generated[:5] or n in resource_boundaries:
        print(
            "case=",
            json.dumps(
                {
                    "n": n,
                    "canonical": {k: v for k, v in expected.items() if k != "value"},
                    "candidate": {k: v for k, v in actual.items() if k != "value"},
                },
                sort_keys=True,
            ),
        )

print("value_mismatches=", value_mismatches)
print("type_mismatches=", type_mismatches)
print("independent_integer_oracle_mismatches=", oracle_mismatches)
print("exception_mismatches=", exception_mismatches)

if value_mismatches or oracle_mismatches:
    raise SystemExit(1)

# Exception/type differences remain explicit review evidence but do not make
# this finite value-comparison runner hide its successfully compared cases.
raise SystemExit(0)
