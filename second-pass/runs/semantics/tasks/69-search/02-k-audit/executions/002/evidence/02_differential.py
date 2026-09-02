#!/usr/bin/env python3
"""Independent differential test for HumanEval 69-search."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path
from types import ModuleType


ROOT = Path("/tmp/audit-work/69-search")


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module("trusted_canonical_69", ROOT / "canonical.py")
generated = load_module("generated_solution_69", ROOT / "solution.py")

documented = [
    [4, 1, 2, 2, 3, 1],
    [1, 2, 2, 3, 3, 3, 4, 4, 4],
    [5, 5, 4, 4, 4],
]

branch_boundaries = [
    [1],                    # smallest positive; exactly qualifying
    [2],                    # no value qualifies
    [2, 2],                 # frequency == value
    [2, 2, 2],              # frequency > value
    [3, 3],                 # frequency one below value
    [3, 3, 3],              # frequency exactly value
    [1, 2, 2, 3, 3, 3],    # multiple qualifiers; select greatest
    [4, 4, 4, 4, 2, 2],    # later/smaller qualifying duplicate
    [7, 7, 7, 7, 7, 7],    # large candidate one below threshold
    [7, 7, 7, 7, 7, 7, 7], # large candidate exactly threshold
    [1000],                 # sparse large value; no qualifier
]


def compare(values: list[int], label: str) -> None:
    expected = canonical.search(list(values))
    actual = generated.search(list(values))
    if expected != actual:
        raise AssertionError(
            f"mismatch label={label} input={values!r} canonical={expected} generated={actual}"
        )


for index, values in enumerate(documented, 1):
    compare(values, f"documented-{index}")
    print(
        f"documented-{index}: input={values!r} "
        f"canonical={canonical.search(values)} generated={generated.search(values)}"
    )

for index, values in enumerate(branch_boundaries, 1):
    compare(values, f"boundary-{index}")
    print(
        f"boundary-{index}: input={values!r} "
        f"canonical={canonical.search(values)} generated={generated.search(values)}"
    )

exhaustive_count = 0
for length in range(1, 6):
    for values_tuple in itertools.product(range(1, 6), repeat=length):
        compare(list(values_tuple), "exhaustive")
        exhaustive_count += 1
print(f"exhaustive_intended_domain_cases={exhaustive_count} mismatches=0")

rng = random.Random(690026)
random_count = 0
for _ in range(2000):
    length = rng.randint(1, 30)
    values = [rng.randint(1, 50) for _ in range(length)]
    compare(values, "seeded-random")
    random_count += 1
print(f"seeded_random_cases={random_count} seed=690026 mismatches=0")

# Empty/non-positive lists are outside the source precondition. Record the
# behavior explicitly without treating outside-domain divergence as a defect.
for values in ([], [0], [-1], [0, 1, 1], [-2, 2, 2]):
    outcomes: list[str] = []
    for name, fn in (("canonical", canonical.search), ("generated", generated.search)):
        try:
            outcomes.append(f"{name}=return:{fn(list(values))!r}")
        except Exception as err:  # noqa: BLE001 - the exception type is evidence
            outcomes.append(f"{name}=exception:{type(err).__name__}:{err}")
    print(f"outside-domain input={values!r} {' '.join(outcomes)}")

print("DIFFERENTIAL_CHECK=PASS")
