#!/usr/bin/env python3
"""Independent differential test of trusted canonical.py and candidate solution.py."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/130-tri-audit")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module("trusted_canonical", SCRATCH / "canonical.trusted.py")
candidate = load_module("candidate_solution", SCRATCH / "solution.py")

# Explicitly includes the documented example, empty result boundary n=0,
# initialization/no-loop boundary n=1, first even branch n=2, first odd branch
# n=3, subsequent branch boundaries, and medium-sized representatives.
fixed_inputs = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 16, 17, 31, 32, 50, 99, 100, 127, 256]
rng = random.Random(130)
generated_inputs = sorted(set(rng.randrange(0, 1001) for _ in range(120)))
inputs = sorted(set(fixed_inputs + generated_inputs))

mismatches: list[tuple[int, object, object]] = []
shape_mismatches: list[tuple[int, list[type], list[type]]] = []
contract_failures: list[str] = []


def mathematical_value(index: int, prefix: list[int]) -> int:
    if index == 0:
        return 1
    if index == 1:
        return 3
    if index % 2 == 0:
        return 1 + index // 2
    return prefix[index - 1] + prefix[index - 2] + 1 + (index + 1) // 2


for n in inputs:
    trusted_result = canonical.tri(n)
    candidate_result = candidate.tri(n)
    if trusted_result != candidate_result:
        mismatches.append((n, trusted_result, candidate_result))
    if [type(item) for item in trusted_result] != [type(item) for item in candidate_result]:
        shape_mismatches.append(
            (n, [type(item) for item in trusted_result], [type(item) for item in candidate_result])
        )
    if len(candidate_result) != n + 1:
        contract_failures.append(f"n={n}: length={len(candidate_result)}")
    expected_prefix: list[int] = []
    for index, actual in enumerate(candidate_result):
        expected_prefix.append(mathematical_value(index, expected_prefix))
        if actual != expected_prefix[-1]:
            contract_failures.append(
                f"n={n} index={index}: actual={actual!r} expected={expected_prefix[-1]!r}"
            )

print(f"INPUT_COUNT {len(inputs)}")
print(f"INPUTS {inputs}")
print(f"VALUE_MISMATCH_COUNT {len(mismatches)}")
for mismatch in mismatches[:10]:
    print(f"VALUE_MISMATCH {mismatch!r}")
print(f"TYPE_SHAPE_MISMATCH_COUNT {len(shape_mismatches)}")
print(
    "TYPE_SHAPE_EXAMPLE "
    + repr(
        (
            3,
            [type(item).__name__ for item in canonical.tri(3)],
            [type(item).__name__ for item in candidate.tri(3)],
        )
    )
)
print(f"CONTRACT_FAILURE_COUNT {len(contract_failures)}")
for failure in contract_failures[:10]:
    print(f"CONTRACT_FAILURE {failure}")
print(f"DOCUMENTED_EXAMPLE candidate={candidate.tri(3)!r} trusted={canonical.tri(3)!r}")

if mismatches or contract_failures:
    raise SystemExit(1)
