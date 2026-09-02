#!/usr/bin/env python3
"""Independent deterministic differential test for HumanEval/52."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/52-below-threshold")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.below_threshold


canonical = load_function("trusted_canonical", SCRATCH / "trusted/canonical.py")
generated = load_function("submitted_solution", SCRATCH / "solution.py")

named_cases: list[tuple[str, list[float | int], int]] = [
    ("doc-true", [1, 2, 4, 10], 100),
    ("doc-false", [1, 20, 4, 10], 5),
    ("empty", [], 0),
    ("equal-boundary", [5], 5),
    ("one-below", [4], 5),
    ("one-above", [6], 5),
    ("negative-equal", [-3], -3),
    ("negative-below", [-4, -10], -3),
    ("early-failure", [5, -100, -100], 5),
    ("middle-failure", [-100, 5, -100], 5),
    ("late-failure", [-100, -100, 5], 5),
    ("all-below-zero", [-3, -2, -1], 0),
    ("large-integers", [-(10**100), 10**100 - 1], 10**100),
    ("float-below", [4.5, -2.25], 5),
    ("float-equal", [5.0], 5),
    ("mixed-numeric", [-1.5, 0, 2.75], 3),
]

cases: list[tuple[str, list[float | int], int]] = list(named_cases)

# Exhaust all lists of length 0..5 over values that exercise below/equal/above
# for several thresholds.
for threshold in (-2, 0, 7):
    alphabet = (threshold - 1, threshold, threshold + 1)
    for length in range(6):
        for values in itertools.product(alphabet, repeat=length):
            cases.append((f"exhaustive-t{threshold}-n{length}", list(values), threshold))

# Broader representative integer and finite-float samples, independently
# generated from a fixed seed.
rng = random.Random(520052)
for index in range(500):
    threshold = rng.randint(-10_000, 10_000)
    length = rng.randint(0, 25)
    values: list[float | int] = []
    for _ in range(length):
        if rng.randrange(4) == 0:
            values.append(rng.randint(-40_000, 40_000) / 4)
        else:
            values.append(rng.randint(-40_000, 40_000))
    cases.append((f"seeded-{index}", values, threshold))

mismatches = []
serialized_inputs = []
for label, values, threshold in cases:
    expected = canonical(list(values), threshold)
    actual = generated(list(values), threshold)
    serialized_inputs.append([label, values, threshold])
    if actual != expected or type(actual) is not type(expected):
        mismatches.append(
            {
                "label": label,
                "values": values,
                "threshold": threshold,
                "canonical": expected,
                "generated": actual,
            }
        )

encoded_inputs = json.dumps(
    serialized_inputs, separators=(",", ":"), ensure_ascii=True
).encode()
print("oracle=/tmp/audit-work/52-below-threshold/trusted/canonical.py")
print("subject=/tmp/audit-work/52-below-threshold/solution.py")
print("documented_and_named_cases=", len(named_cases))
print("exhaustive_scope=thresholds[-2,0,7], lengths[0..5], alphabet[t-1,t,t+1]")
print("random_scope=seed=520052, count=500, lengths[0..25], int_and_quarter_float_values")
print("total_cases=", len(cases))
print("input_manifest_sha256=", hashlib.sha256(encoded_inputs).hexdigest())
print("mismatch_count=", len(mismatches))
if mismatches:
    print(json.dumps(mismatches[:20], indent=2, sort_keys=True))
    raise SystemExit(1)
