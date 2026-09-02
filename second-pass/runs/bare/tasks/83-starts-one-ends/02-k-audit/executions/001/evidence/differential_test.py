#!/usr/bin/env python3
"""Independent differential and finite intent checks for HumanEval/83."""

from __future__ import annotations

import importlib.util
import json
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.starts_one_ends


def brute_count(n: int) -> int:
    low = 10 ** (n - 1)
    high = 10**n
    return sum(str(value).startswith("1") or str(value).endswith("1")
               for value in range(low, high))


canonical = load_entry("trusted_canonical", Path("/reference/canonical.py"))
generated = load_entry(
    "generated_solution", Path("/tmp/audit-work/review-83/solution.py")
)

# No examples are present in prompt.py. These cover the singleton branch,
# the adjacent branch boundary, small exhaustive/brute-force cases, ordinary
# values, and deterministic generated positive integers.
fixed_inputs = [1, 2, 3, 4, 5, 6, 10, 20, 50, 100]
rng = random.Random(830083)
generated_inputs = [rng.randint(1, 120) for _ in range(80)]
positive_inputs = sorted(set(fixed_inputs + list(range(1, 31)) + generated_inputs))

mismatches = []
rows = []
for n in positive_inputs:
    expected = canonical(n)
    actual = generated(n)
    rows.append({"n": n, "canonical": expected, "generated": actual})
    if expected != actual:
        mismatches.append(rows[-1])

brute_rows = []
for n in range(1, 6):
    oracle = brute_count(n)
    canonical_value = canonical(n)
    generated_value = generated(n)
    row = {
        "n": n,
        "brute_force": oracle,
        "canonical": canonical_value,
        "generated": generated_value,
    }
    brute_rows.append(row)
    if not (oracle == canonical_value == generated_value):
        mismatches.append(row)

# Nonpositive integers are outside the documented domain. Record them only as
# boundary diagnostics; they are not verdict-bearing comparisons.
out_of_domain = []
for n in [0, -1, -2]:
    out_of_domain.append(
        {"n": n, "canonical": canonical(n), "generated": generated(n)}
    )

report = {
    "documented_examples": "none in trusted prompt.py",
    "intended_domain": "positive integers",
    "positive_input_count": len(positive_inputs),
    "positive_inputs": positive_inputs,
    "positive_rows": rows,
    "brute_force_rows": brute_rows,
    "out_of_domain_diagnostics": out_of_domain,
    "mismatch_count": len(mismatches),
    "mismatches": mismatches,
}
print(json.dumps(report, indent=2, sort_keys=True))
raise SystemExit(1 if mismatches else 0)
