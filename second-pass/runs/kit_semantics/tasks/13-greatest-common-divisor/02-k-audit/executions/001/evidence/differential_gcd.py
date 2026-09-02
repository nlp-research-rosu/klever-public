#!/usr/bin/env python3
"""Independent differential test for HumanEval/13."""

from __future__ import annotations

import importlib.util
import math
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.greatest_common_divisor


canonical = load_entry(
    Path("/tmp/audit-work/trusted/canonical.py"), "trusted_canonical"
)
generated = load_entry(
    Path("/tmp/audit-work/candidate/solution.py"), "generated_solution"
)

named_cases = [
    ("example-3-5", 3, 5),
    ("example-25-15", 25, 15),
    ("both-zero", 0, 0),
    ("a-zero-b-positive", 0, 7),
    ("a-zero-b-negative", 0, -7),
    ("a-positive-b-zero", 7, 0),
    ("a-negative-b-zero", -7, 0),
    ("positive-unit", 13, 1),
    ("negative-unit", 13, -1),
    ("both-negative", -25, -15),
    ("negative-positive", -25, 15),
    ("positive-negative", 25, -15),
    ("equal-positive", 19, 19),
    ("equal-negative", -19, -19),
    ("coprime", 2**61 - 1, 2**31 - 1),
    ("large-common-factor", 37 * 10**80, 37 * 10**60),
    ("bools", True, False),
]

cases: list[tuple[str, int, int]] = list(named_cases)
for a in range(-40, 41):
    for b in range(-40, 41):
        cases.append(("exhaustive-small", a, b))

rng = random.Random(130013)
for _ in range(5000):
    cases.append(
        (
            "random-signed",
            rng.randint(-(10**30), 10**30),
            rng.randint(-(10**30), 10**30),
        )
    )

canonical_generated_mismatches: list[tuple[str, int, int, int, int]] = []
canonical_math_mismatches: list[tuple[str, int, int, int, int]] = []
generated_math_mismatches: list[tuple[str, int, int, int, int]] = []
for label, a, b in cases:
    canonical_result = canonical(a, b)
    generated_result = generated(a, b)
    math_result = math.gcd(a, b)
    if canonical_result != generated_result:
        canonical_generated_mismatches.append(
            (label, a, b, canonical_result, generated_result)
        )
    if canonical_result != math_result:
        canonical_math_mismatches.append(
            (label, a, b, canonical_result, math_result)
        )
    if generated_result != math_result:
        generated_math_mismatches.append(
            (label, a, b, generated_result, math_result)
        )

print(f"total_cases={len(cases)}")
print(
    "canonical_generated_mismatches="
    f"{len(canonical_generated_mismatches)}"
)
print(f"canonical_math_mismatches={len(canonical_math_mismatches)}")
print(f"generated_math_mismatches={len(generated_math_mismatches)}")
print("first_canonical_generated_mismatches:")
for mismatch in canonical_generated_mismatches[:25]:
    print(mismatch)

# Also compare behavior outside the two-argument input domain: both definitions
# reject missing arguments with TypeError.
for argument_count, arguments in ((0, ()), (1, (1,))):
    outcomes = []
    for function in (canonical, generated):
        try:
            function(*arguments)
        except Exception as error:  # diagnostics only
            outcomes.append(type(error).__name__)
        else:
            outcomes.append("NO_EXCEPTION")
    print(f"arity_{argument_count}_outcomes={outcomes}")

# Exit nonzero on any canonical/generated difference so the command status
# cannot accidentally be interpreted as a zero-mismatch run.
raise SystemExit(1 if canonical_generated_mismatches else 0)
