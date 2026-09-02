#!/usr/bin/env python3
"""Independent canonical-vs-generated differential test for HumanEval 65."""

from __future__ import annotations

import importlib.util
import json
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.circular_shift


canonical = load_entry(
    Path("/tmp/audit-work/trusted/canonical.py"), "trusted_canonical"
)
generated = load_entry(Path("/tmp/audit-work/case/solution.py"), "submitted_solution")

# The contract describes a count of positions shifted right. The formal K claims
# explicitly choose the nonnegative-count domain, so that is the primary suite.
documented_and_boundaries = [
    (12, 1, "documented shift-one"),
    (12, 2, "documented shift-length"),
    (12, 0, "zero shift"),
    (12, 3, "first oversize"),
    (0, 0, "one-character zero"),
    (0, 1, "one-character length"),
    (0, 2, "one-character oversize"),
    (7, 0, "single digit zero"),
    (7, 1, "single digit length"),
    (7, 2, "single digit first oversize"),
    (12345, 4, "len-minus-one"),
    (12345, 5, "exact length"),
    (12345, 6, "len-plus-one"),
    (12345, 99, "large oversize"),
    (-123, 0, "negative-x zero"),
    (-123, 1, "negative-x normal"),
    (-123, 4, "negative-x exact string length"),
    (-123, 5, "negative-x oversize"),
]

rng = random.Random(650065)
generated_nonnegative = []
for _ in range(1200):
    x = rng.randint(-(10**30), 10**30)
    length = len(str(x))
    boundary_choices = [0, 1, max(0, length - 1), length, length + 1, length + 2]
    shift = rng.choice(boundary_choices + [rng.randint(0, length + 40)])
    generated_nonnegative.append((x, shift, "seeded-generated"))


def compare(cases):
    records = []
    mismatches = []
    for x, shift, label in cases:
        expected = canonical(x, shift)
        actual = generated(x, shift)
        record = {
            "x": x,
            "shift": shift,
            "label": label,
            "canonical": expected,
            "generated": actual,
            "match": expected == actual,
        }
        records.append(record)
        if expected != actual:
            mismatches.append(record)
    return records, mismatches


boundary_records, boundary_mismatches = compare(documented_and_boundaries)
generated_records, generated_mismatches = compare(generated_nonnegative)

# The prompt does not explicitly spell out shift >= 0. Probe negative values
# separately so the K precondition's scope restriction is visible.
negative_shift_cases = [
    (12, -1, "negative-shift-minus-one"),
    (12, -2, "negative-shift-minus-length"),
    (12345, -1, "negative-shift-minus-one-long"),
    (12345, -2, "negative-shift-minus-two"),
    (-123, -1, "negative-x-negative-shift"),
]
negative_records, negative_mismatches = compare(negative_shift_cases)

summary = {
    "primary_domain": "integer x, nonnegative integer shift",
    "boundary_case_count": len(boundary_records),
    "boundary_mismatch_count": len(boundary_mismatches),
    "generated_seed": 650065,
    "generated_case_count": len(generated_records),
    "generated_mismatch_count": len(generated_mismatches),
    "negative_shift_probe_count": len(negative_records),
    "negative_shift_mismatch_count": len(negative_mismatches),
    "boundary_records": boundary_records,
    "negative_shift_records": negative_records,
    "primary_mismatch_examples": (boundary_mismatches + generated_mismatches)[:20],
}
print(json.dumps(summary, indent=2, sort_keys=True))

if boundary_mismatches or generated_mismatches:
    raise SystemExit(1)
