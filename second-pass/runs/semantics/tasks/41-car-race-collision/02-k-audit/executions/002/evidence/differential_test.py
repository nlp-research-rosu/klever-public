#!/usr/bin/env python3
"""Independent differential test of canonical.py against scratch solution.py."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
import sys
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module("trusted_canonical", Path("/reference/canonical.py"))
candidate = load_module(
    "scratch_candidate", Path("/tmp/audit-work/reconstruct/solution.py")
)

# The prompt has no explicit examples. For the count-of-cars domain, this covers
# the empty case, the first nonempty cases, a dense boundary region, large
# arbitrary-precision integers, and a deterministic broader generated sample.
documented_examples: list[int] = []
boundary_cases = [0, 1, 2, 3, 10, 41, 10**6, 10**50]
dense_cases = list(range(0, 2049))
generator = random.Random(410041)
generated_cases = [generator.randrange(0, 10**12 + 1) for _ in range(512)]

# Negative ints are outside the natural "n cars" interpretation but exercise
# the full annotated Python-int behavior that the candidate's K precondition
# actually admits.
overbroad_spec_probes = [-1, -2, -10, -(10**50)]

inputs = list(
    dict.fromkeys(
        documented_examples
        + boundary_cases
        + dense_cases
        + generated_cases
        + overbroad_spec_probes
    )
)
encoded_inputs = json.dumps(inputs, separators=(",", ":")).encode("utf-8")
print(
    json.dumps(
        {
            "documented_examples": documented_examples,
            "boundary_cases": boundary_cases,
            "dense_range": [0, 2048],
            "generated_seed": 410041,
            "generated_count": len(generated_cases),
            "generated_range_inclusive": [0, 10**12],
            "overbroad_spec_probes": overbroad_spec_probes,
            "unique_input_count": len(inputs),
            "input_list_sha256": hashlib.sha256(encoded_inputs).hexdigest(),
            "inputs": inputs,
        },
        sort_keys=True,
    )
)

mismatches = []
for value in inputs:
    expected = canonical.car_race_collision(value)
    actual = candidate.car_race_collision(value)
    if actual != expected or type(actual) is not type(expected):
        mismatches.append(
            {
                "input": value,
                "canonical": repr(expected),
                "candidate": repr(actual),
                "canonical_type": type(expected).__name__,
                "candidate_type": type(actual).__name__,
            }
        )

print(
    json.dumps(
        {
            "oracle": "/reference/canonical.py:car_race_collision",
            "subject": "/tmp/audit-work/reconstruct/solution.py:car_race_collision",
            "checked": len(inputs),
            "mismatches": mismatches,
            "mismatch_count": len(mismatches),
        },
        sort_keys=True,
    )
)
sys.exit(1 if mismatches else 0)
