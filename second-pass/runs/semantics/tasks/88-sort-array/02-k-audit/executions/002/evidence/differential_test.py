#!/usr/bin/env python3
"""Independent differential and input-preservation tests for HumanEval/88."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("trusted_canonical_88", Path("/reference/canonical.py"))
generated = load("candidate_solution_88", Path("/tmp/audit-work/88-sort-array/solution.py"))

documented = [
    [],
    [5],
    [2, 4, 3, 0, 1, 5],
    [2, 4, 3, 0, 1, 5, 6],
]
boundaries = [
    [0],
    [1],
    [2],
    [10**30],
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1],
    [2, 0],
    [2, 1],
    [1, 2],
    [3, 3],
    [10**30, 0, 10**30],
    [10**30, 1, 10**30],
]

exhaustive = [
    list(values)
    for length in range(0, 6)
    for values in itertools.product(range(6), repeat=length)
]

rng = random.Random(880088)
generated_inputs: list[list[int]] = []
for _ in range(300):
    length = rng.randrange(0, 65)
    generated_inputs.append([rng.randrange(0, 10**12) for _ in range(length)])

inputs = documented + boundaries + exhaustive + generated_inputs
odd_nonempty = 0
even_nonempty = 0
for index, original in enumerate(inputs):
    left_input = list(original)
    right_input = list(original)
    left_before = list(left_input)
    right_before = list(right_input)

    expected = canonical.sort_array(left_input)
    actual = generated.sort_array(right_input)

    assert left_input == left_before, ("canonical mutated input", index, original)
    assert right_input == right_before, ("candidate mutated input", index, original)
    assert expected == actual, ("result mismatch", index, original, expected, actual)
    assert expected is not left_input, ("canonical failed copy contract", index, original)
    assert actual is not right_input, ("candidate failed copy contract", index, original)

    if original:
        if (original[0] + original[-1]) % 2:
            odd_nonempty += 1
            assert actual == sorted(original)
        else:
            even_nonempty += 1
            assert actual == sorted(original, reverse=True)
    else:
        assert actual == []

print(f"documented_cases={len(documented)}")
print(f"explicit_boundary_cases={len(boundaries)}")
print(f"exhaustive_cases={len(exhaustive)} domain=length_0_through_5 values_0_through_5")
print(f"generated_cases={len(generated_inputs)} seed=880088 max_length=64 values_0_through_999999999999")
print(f"total_cases={len(inputs)} odd_nonempty={odd_nonempty} even_nonempty={even_nonempty}")
print("mismatches=0 mutations=0 copy_contract_failures=0")
print("DIFFERENTIAL_TEST=PASS")
