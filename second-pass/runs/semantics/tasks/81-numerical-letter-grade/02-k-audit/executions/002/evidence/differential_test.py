#!/usr/bin/env python3
"""Independent differential oracle for HumanEval/81."""

from __future__ import annotations

import importlib.util
import math
import random
from pathlib import Path
from typing import Any, Callable


def load_entry(path: Path, module_name: str) -> Callable[[list[Any]], list[str]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.numerical_letter_grade


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
generated = load_entry(Path("/candidate/solution.py"), "generated_solution")


def outcome(function: Callable[[list[Any]], list[str]], values: list[Any]) -> tuple:
    try:
        return ("return", function(values))
    except Exception as error:  # diagnostic parity includes exception type
        return ("raise", type(error).__name__, str(error))


thresholds = [4.0, 3.7, 3.3, 3.0, 2.7, 2.3, 2.0, 1.7, 1.3, 1.0, 0.7, 0.0]
boundary_scalars: list[float] = []
for threshold in thresholds:
    boundary_scalars.extend(
        [
            math.nextafter(threshold, -math.inf),
            threshold,
            math.nextafter(threshold, math.inf),
        ]
    )

documented = [4.0, 3, 1.7, 2, 3.5]
documented_expected = ["A+", "B", "C-", "C", "A-"]
assert canonical(documented) == documented_expected
assert generated(documented) == documented_expected

cases: list[tuple[str, list[Any]]] = [
    ("empty", []),
    ("documented", documented),
    ("all-boundaries", boundary_scalars),
    ("special-floats", [math.nan, math.inf, -math.inf, -0.0]),
]
cases.extend((f"boundary-singleton-{index}", [value]) for index, value in enumerate(boundary_scalars))
cases.extend((f"small-int-{value}", [value]) for value in range(-8, 10))

rng = random.Random(810081)
for index in range(1000):
    size = rng.randrange(0, 25)
    values = [rng.uniform(-2.0, 6.0) for _ in range(size)]
    if index % 5 == 0:
        values.extend(rng.randrange(-8, 10) for _ in range(rng.randrange(0, 6)))
    cases.append((f"generated-{index}", values))

mismatches = []
scalar_values = 0
for name, values in cases:
    scalar_values += len(values)
    trusted = outcome(canonical, list(values))
    candidate = outcome(generated, list(values))
    if trusted != candidate:
        mismatches.append((name, values, trusted, candidate))

print("ORACLE=/reference/canonical.py:numerical_letter_grade")
print("CANDIDATE=/candidate/solution.py:numerical_letter_grade")
print(
    "SCOPE=empty; documented example; each threshold and adjacent IEEE-754 "
    "neighbors; small integers; NaN/infinities; 1000 deterministic lists "
    "of mixed finite floats/small integers in [-2,6]"
)
print(f"CASES={len(cases)}")
print(f"SCALAR_VALUES={scalar_values}")
print(f"MISMATCHES={len(mismatches)}")
for mismatch in mismatches[:20]:
    print(f"MISMATCH={mismatch!r}")

# A deliberate out-of-GPA diagnostic exposes the implementation's float()
# conversion boundary. It is reported separately and is not included in the
# finite GPA-domain differential count above.
huge_integer = 10**1000
print(
    "OUT_OF_GPA_DIAGNOSTIC huge-int "
    f"canonical={outcome(canonical, [huge_integer])!r} "
    f"candidate={outcome(generated, [huge_integer])!r}"
)

if mismatches:
    raise SystemExit(1)
print("DIFFERENTIAL_OK")
