#!/usr/bin/env python3
"""Independent differential test for HumanEval 88.

The trusted canonical and submitted generated entry point are loaded from
distinct file paths. Inputs are restricted to lists of non-negative Python
integers, the documented domain.
"""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/88-sort-array")
INPUTS_OUT = Path("/audit-output/evidence/differential-inputs.json")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_array


canonical = load_function("trusted_humaneval_88", SCRATCH / "trusted_canonical.py")
generated = load_function("submitted_solution_88", SCRATCH / "solution.py")

documented = [
    [],
    [5],
    [2, 4, 3, 0, 1, 5],
    [2, 4, 3, 0, 1, 5, 6],
]

boundaries = [
    [0],
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1],
    [2, 1],
    [2, 2],
    [3, 1, 2],
    [3, 2, 2],
    [4, 0, 3],
    [4, 0, 4],
    [9, 9, 0, 9],
    [10**30, 0],
    [10**30, 1],
    [0, 10**30],
    [1, 10**30],
]

exhaustive = [
    list(values)
    for length in range(0, 6)
    for values in itertools.product(range(4), repeat=length)
]

rng = random.Random(880088)
generated_inputs = [
    [rng.randrange(0, 10**12) for _ in range(rng.randrange(0, 21))]
    for _ in range(300)
]

all_inputs = documented + boundaries + exhaustive + generated_inputs
INPUTS_OUT.write_text(
    json.dumps(
        {
            "domain": "lists of non-negative Python integers",
            "seed": 880088,
            "documented": documented,
            "boundaries": boundaries,
            "exhaustive": {
                "lengths": [0, 1, 2, 3, 4, 5],
                "values": [0, 1, 2, 3],
                "cases": exhaustive,
            },
            "generated": generated_inputs,
        },
        indent=2,
    )
    + "\n",
    encoding="utf-8",
)

mismatches = []
mutation_failures = []
copy_failures = []
ascending_branch = 0
descending_branch = 0
empty_branch = 0

for index, original in enumerate(all_inputs):
    input_for_canonical = original.copy()
    input_for_generated = original.copy()

    canonical_result = canonical(input_for_canonical)
    generated_result = generated(input_for_generated)

    if not original:
        empty_branch += 1
    elif (original[0] + original[-1]) % 2:
        ascending_branch += 1
    else:
        descending_branch += 1

    if canonical_result != generated_result:
        mismatches.append(
            {
                "index": index,
                "input": original,
                "canonical": canonical_result,
                "generated": generated_result,
            }
        )

    if input_for_canonical != original or input_for_generated != original:
        mutation_failures.append(index)

    if canonical_result is input_for_canonical or generated_result is input_for_generated:
        copy_failures.append(index)

print(f"documented_cases={len(documented)}")
print(f"boundary_cases={len(boundaries)}")
print(f"exhaustive_cases={len(exhaustive)}")
print(f"generated_cases={len(generated_inputs)} seed=880088")
print(f"total_cases={len(all_inputs)}")
print(
    "branches="
    f"empty:{empty_branch},ascending_odd:{ascending_branch},"
    f"descending_even:{descending_branch}"
)
print(f"mismatches={len(mismatches)}")
print(f"mutation_failures={len(mutation_failures)}")
print(f"copy_failures={len(copy_failures)}")

if mismatches or mutation_failures or copy_failures:
    print(
        json.dumps(
            {
                "mismatches": mismatches[:20],
                "mutation_failures": mutation_failures[:20],
                "copy_failures": copy_failures[:20],
            },
            indent=2,
        )
    )
    raise SystemExit(1)
