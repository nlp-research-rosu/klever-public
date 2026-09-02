#!/usr/bin/env python3
"""Independent candidate/canonical differential test for HumanEval 35."""

from __future__ import annotations

import importlib.util
import itertools
import math
import random
from pathlib import Path
from typing import Any, Callable

WORK = Path("/tmp/audit-work/work")


def load_entry(path: Path, module_name: str) -> Callable[[list], Any]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.max_element


canonical = load_entry(WORK / "canonical.py", "audit_canonical")
candidate = load_entry(WORK / "solution.py", "audit_candidate")

named_cases: list[tuple[str, list[Any]]] = [
    ("prompt-example-1", [1, 2, 3]),
    ("prompt-example-2", [5, 3, -5, 2, -3, 3, 9, 0, 123, 1, -10]),
    ("singleton-zero", [0]),
    ("singleton-negative", [-7]),
    ("all-equal", [4, 4, 4]),
    ("strictly-descending", [5, 4, 3, 2, 1]),
    ("update-at-first-boundary", [1, 2, 0]),
    ("update-at-last-boundary", [1, 0, 2]),
    ("negative-duplicate-max", [-9, -2, -14, -2]),
    ("large-magnitude", [-(10**100), 10**100, 0]),
    ("booleans", [False, True, False]),
    ("mixed-int-float", [1, 2.5, -3, 2.25]),
    ("strings", ["aa", "z", "ab"]),
    ("float-infinities", [-math.inf, 0.0, math.inf]),
]

rng = random.Random(350035)
generated_integer_cases = [
    [rng.randint(-10**6, 10**6) for _ in range(rng.randint(1, 30))]
    for _ in range(1000)
]
exhaustive_integer_cases = [
    list(values)
    for size in range(1, 6)
    for values in itertools.product(range(-2, 3), repeat=size)
]

mismatches: list[str] = []
tested = 0
for name, values in named_cases:
    expected = canonical(values.copy())
    actual = candidate(values.copy())
    tested += 1
    print(f"NAMED {name}: input={values!r} canonical={expected!r} candidate={actual!r}")
    if actual != expected or type(actual) is not type(expected):
        mismatches.append(f"{name}: {expected!r}/{type(expected)} != {actual!r}/{type(actual)}")

for family, cases in (
    ("exhaustive", exhaustive_integer_cases),
    ("seeded-random", generated_integer_cases),
):
    family_mismatches = 0
    for index, values in enumerate(cases):
        expected = canonical(values.copy())
        actual = candidate(values.copy())
        tested += 1
        if actual != expected or type(actual) is not type(expected):
            family_mismatches += 1
            mismatches.append(f"{family}[{index}] {values!r}: {expected!r} != {actual!r}")
    print(f"FAMILY {family}: cases={len(cases)} mismatches={family_mismatches}")

print("EMPTY boundary (outside the non-empty maximum contract):")
for label, implementation in (("canonical", canonical), ("candidate", candidate)):
    try:
        implementation([])
    except Exception as error:  # noqa: BLE001 - exception type is the observation.
        print(f"  {label}: {type(error).__name__}: {error}")
    else:
        mismatches.append(f"{label} unexpectedly returned on []")

print(f"SUMMARY tested_nonempty={tested} mismatches={len(mismatches)}")
if mismatches:
    print("\n".join(mismatches[:20]))
    raise SystemExit(1)
