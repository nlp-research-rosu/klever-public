#!/usr/bin/env python3
"""Independent differential test for HumanEval 135 can_arrange."""

import hashlib
import importlib.util
import itertools
import json
import random
import sys


sys.dont_write_bytecode = True


def load_entry(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.can_arrange


canonical = load_entry("trusted_canonical_135", "/reference/canonical.py")
generated = load_entry("candidate_solution_135", "/candidate/solution.py")

documented_and_boundaries = [
    [1, 2, 4, 3, 5],
    [1, 2, 3],
    [],
    [0],
    [-1],
    [1, 2],
    [2, 1],
    [1, 3, 2],
    [3, 1, 2],
    [5, 4, 3, 2, 1],
    [-3, -1, -2, 0, -4],
]

# Exhaust all duplicate-free arrays over five small integers. This covers every
# length from empty through five and every ordering/branch pattern in that set.
small_values = [-2, -1, 0, 1, 2]
exhaustive = [
    list(items)
    for length in range(len(small_values) + 1)
    for items in itertools.permutations(small_values, length)
]

# Reproducible broader unique-integer arrays.
rng = random.Random(135)
generated_inputs = [
    rng.sample(range(-1000, 1001), rng.randrange(0, 41)) for _ in range(200)
]

cases = documented_and_boundaries + exhaustive + generated_inputs
mismatches = []
result_histogram = {}
for case in cases:
    expected = canonical(list(case))
    actual = generated(list(case))
    result_histogram[str(actual)] = result_histogram.get(str(actual), 0) + 1
    if actual != expected:
        mismatches.append(
            {"input": case, "canonical": expected, "generated": actual}
        )

serialized_inputs = json.dumps(cases, separators=(",", ":"), sort_keys=False)
report = {
    "documented_and_boundary_inputs": documented_and_boundaries,
    "exhaustive_domain": {
        "values": small_values,
        "lengths": [0, 1, 2, 3, 4, 5],
        "duplicate_free": True,
        "case_count": len(exhaustive),
    },
    "generated_domain": {
        "seed": 135,
        "population": [-1000, 1000],
        "lengths": [0, 40],
        "duplicate_free": True,
        "case_count": len(generated_inputs),
    },
    "total_case_count": len(cases),
    "inputs_sha256": hashlib.sha256(serialized_inputs.encode()).hexdigest(),
    "distinct_results": len(result_histogram),
    "mismatch_count": len(mismatches),
    "mismatches": mismatches[:20],
}
print(json.dumps(report, indent=2, sort_keys=True))
raise SystemExit(1 if mismatches else 0)
