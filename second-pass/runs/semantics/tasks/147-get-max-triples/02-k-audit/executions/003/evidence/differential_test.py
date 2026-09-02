#!/usr/bin/env python3
"""Independent differential test for HumanEval 147.

Run from the clean scratch directory containing canonical.py and solution.py.
"""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_max_triples


def independent_oracle(n: int) -> int:
    values = [i * i - i + 1 for i in range(1, n + 1)]
    return sum(
        (values[i] + values[j] + values[k]) % 3 == 0
        for i, j, k in itertools.combinations(range(n), 3)
    )


root = Path.cwd()
canonical = load_function(root / "canonical.py", "trusted_canonical")
generated = load_function(root / "solution.py", "generated_solution")

documented = {5: 1}
empty_outside_contract = [0]
positive_boundaries = list(range(1, 16))
branch_boundaries = sorted(
    {
        value
        for q in range(0, 21)
        for value in (3 * q - 1, 3 * q, 3 * q + 1, 3 * q + 2)
        if 0 <= value <= 64
    }
)
rng = random.Random(147)
generated_inputs = [rng.randint(1, 64) for _ in range(100)]
inputs = sorted(
    set(documented)
    | set(empty_outside_contract)
    | set(positive_boundaries)
    | set(branch_boundaries)
    | set(generated_inputs)
    | {20, 32, 48, 64}
)

mismatches = []
for n in inputs:
    trusted = canonical(n)
    candidate = generated(n)
    independent = independent_oracle(n)
    if trusted != candidate or trusted != independent:
        mismatches.append((n, trusted, candidate, independent))

print(f"documented={documented}")
print(f"empty_outside_contract={empty_outside_contract}")
print(f"positive_boundaries={positive_boundaries}")
print(f"branch_boundary_count={len(branch_boundaries)}")
print(f"generated_seed=147 generated_draws={len(generated_inputs)}")
print(f"tested_unique_inputs={len(inputs)} range=[{min(inputs)},{max(inputs)}]")
print(f"sample_results={[(n, generated(n)) for n in (0, 1, 2, 3, 4, 5, 8, 20, 64)]}")
print(f"mismatch_count={len(mismatches)}")
if mismatches:
    print(f"mismatches={mismatches}")
    raise SystemExit(1)
