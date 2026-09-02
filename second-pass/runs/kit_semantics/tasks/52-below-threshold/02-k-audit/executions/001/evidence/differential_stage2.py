#!/usr/bin/env python3
"""Reviewer-authored differential for HumanEval 52 (docstring-first oracle)."""

from __future__ import annotations

import importlib.util
import itertools
import math
import random
from pathlib import Path


def load_function(path: str, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.below_threshold


candidate = load_function("/candidate/solution.py", "audit_candidate_solution")
canonical = load_function("/reference/canonical.py", "audit_trusted_canonical")


def contract_oracle(values, threshold):
    # Direct executable reading of "all numbers ... are below threshold".
    return all(value < threshold for value in values)


def outcome(function, values, threshold):
    try:
        return ("return", function(list(values), threshold))
    except Exception as error:  # observations for underdetermined/exotic cases
        return ("raise", type(error).__name__)


cases: list[tuple[str, tuple[object, ...], int]] = [
    ("doc-example-true", (1, 2, 4, 10), 100),
    ("doc-example-false", (1, 20, 4, 10), 5),
    ("empty", (), 0),
    ("singleton-below", (4,), 5),
    ("singleton-equal", (5,), 5),
    ("singleton-above", (6,), 5),
    ("late-equal", (-10, 0, 5), 5),
    ("late-above", (-10, 0, 6), 5),
    ("negative-threshold", (-4, -3, -2), -2),
    ("bools", (False, True), 2),
    ("finite-floats", (-2.5, 0.5, 4.5), 5),
    ("positive-infinity", (math.inf,), 5),
    ("negative-infinity", (-math.inf,), 5),
    ("nan", (math.nan,), 5),
    ("nan-after-below", (0, math.nan), 5),
]

# Exhaust all short sequences around the strict comparison boundary.
elements = (-2, -1, 0, 1, 2, False, True, -0.5, 0.5)
for length in range(5):
    for values in itertools.product(elements, repeat=length):
        for threshold in range(-2, 3):
            cases.append(("exhaustive-short", values, threshold))

# Independently seeded broader integer sample, including long lists and huge ints.
rng = random.Random(5200730)
for _ in range(5000):
    length = rng.randrange(0, 51)
    values = tuple(rng.randrange(-10**30, 10**30) for _ in range(length))
    threshold = rng.randrange(-10**30, 10**30)
    cases.append(("random-int", values, threshold))

candidate_contract_mismatches = []
canonical_contract_mismatches = []
candidate_canonical_divergences = []
label_counts: dict[str, int] = {}

for label, values, threshold in cases:
    label_counts[label] = label_counts.get(label, 0) + 1
    expected = outcome(contract_oracle, values, threshold)
    got_candidate = outcome(candidate, values, threshold)
    got_canonical = outcome(canonical, values, threshold)
    record = (label, values, threshold, expected, got_candidate, got_canonical)
    if got_candidate != expected:
        candidate_contract_mismatches.append(record)
    if got_canonical != expected:
        canonical_contract_mismatches.append(record)
    if got_candidate != got_canonical:
        candidate_canonical_divergences.append(record)

print(f"total_cases={len(cases)}")
print(f"label_counts={label_counts}")
print(f"candidate_contract_mismatches={len(candidate_contract_mismatches)}")
print(f"canonical_contract_mismatches={len(canonical_contract_mismatches)}")
print(f"candidate_canonical_divergences={len(candidate_canonical_divergences)}")
for record in candidate_canonical_divergences[:20]:
    print(f"divergence={record!r}")

if candidate_contract_mismatches:
    for record in candidate_contract_mismatches[:20]:
        print(f"candidate_contract_mismatch={record!r}")
    raise SystemExit(1)

