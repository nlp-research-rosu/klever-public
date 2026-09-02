#!/usr/bin/env python3
"""Independent differential test for the trusted and submitted GCD entries."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
import random
from pathlib import Path


ROOT = Path("/tmp/audit-work/source")
EVIDENCE = Path("/audit-output/evidence")


def load_entry(module_name: str, source: Path):
    spec = importlib.util.spec_from_file_location(module_name, source)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {source}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.greatest_common_divisor


canonical = load_entry("trusted_canonical", ROOT / "canonical.py")
generated = load_entry("submitted_solution", ROOT / "solution.py")

curated = [
    # Documented examples.
    (3, 5),
    (25, 15),
    # Empty/zero and loop branch boundaries.
    (0, 0),
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0),
    (0, 9),
    (9, 0),
    (0, -9),
    (-9, 0),
    # Equality, unit, exact-divisibility, one-step, and coprime boundaries.
    (1, 1),
    (-1, -1),
    (7, 7),
    (-7, 7),
    (7, -7),
    (-7, -7),
    (54, 24),
    (-54, 24),
    (54, -24),
    (-54, -24),
    (24, 54),
    (5, 3),
    (6, 3),
    (6, 4),
    (35, 64),
    # Arbitrary-precision boundaries representative of Python integers.
    (2**256, 2**128),
    (2**256 - 1, 2**128 - 1),
    (-(2**256), 2**128),
    (2**256, -(2**128)),
]

small_grid = [(a, b) for a in range(-64, 65) for b in range(-64, 65)]

rng = random.Random(130013)
random_cases = [
    (rng.randint(-(10**18), 10**18), rng.randint(-(10**18), 10**18))
    for _ in range(2000)
]

structured = []
for exponent in range(0, 257, 16):
    n = 1 << exponent
    structured.extend(
        [
            (n, n - 1),
            (n, -n),
            (-n, n),
            (-n, -n),
            (3 * n, 5 * n),
        ]
    )

cases = []
seen = set()
for pair in curated + small_grid + random_cases + structured:
    if pair not in seen:
        seen.add(pair)
        cases.append(pair)

inputs_path = EVIDENCE / "stage2_inputs.tsv"
results_path = EVIDENCE / "stage2_results.tsv"
summary_path = EVIDENCE / "stage2_summary.json"

canonical_mismatches = []
math_mismatches = []
exceptions = []

with inputs_path.open("w", newline="", encoding="utf-8") as inputs_stream, results_path.open(
    "w", newline="", encoding="utf-8"
) as results_stream:
    input_writer = csv.writer(inputs_stream, delimiter="\t")
    result_writer = csv.writer(results_stream, delimiter="\t")
    input_writer.writerow(["index", "a", "b"])
    result_writer.writerow(["index", "a", "b", "canonical", "submitted", "math_gcd"])
    for index, (a, b) in enumerate(cases):
        input_writer.writerow([index, a, b])
        try:
            canonical_value = canonical(a, b)
            submitted_value = generated(a, b)
            math_value = math.gcd(a, b)
        except Exception as error:  # evidence: preserve unexpected behavior
            exceptions.append((index, a, b, type(error).__name__, str(error)))
            result_writer.writerow([index, a, b, "EXCEPTION", "EXCEPTION", "EXCEPTION"])
            continue
        result_writer.writerow([index, a, b, canonical_value, submitted_value, math_value])
        if canonical_value != submitted_value:
            canonical_mismatches.append((index, a, b, canonical_value, submitted_value))
        if submitted_value != math_value:
            math_mismatches.append((index, a, b, submitted_value, math_value))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


summary = {
    "scope": {
        "curated_count_before_deduplication": len(curated),
        "small_exhaustive_grid": "all ordered pairs in [-64,64]^2",
        "random_count_before_deduplication": len(random_cases),
        "random_seed": 130013,
        "random_range": "[-10^18,10^18] for each argument",
        "structured_arbitrary_precision_count_before_deduplication": len(structured),
        "total_unique_cases": len(cases),
    },
    "canonical_vs_submitted_mismatch_count": len(canonical_mismatches),
    "submitted_vs_math_gcd_mismatch_count": len(math_mismatches),
    "exception_count": len(exceptions),
    "first_canonical_mismatches": canonical_mismatches[:40],
    "first_submitted_math_mismatches": math_mismatches[:40],
    "exceptions": exceptions[:40],
    "inputs_sha256": sha256(inputs_path),
    "results_sha256": sha256(results_path),
}
summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

print(json.dumps(summary, indent=2))
