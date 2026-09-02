#!/usr/bin/env python3
"""Independent candidate-vs-trusted-canonical differential test."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_odd_collatz


canonical = load_entry(
    "trusted_canonical", Path("/tmp/audit-work/reference/canonical.py")
)
candidate = load_entry(
    "candidate_solution", Path("/tmp/audit-work/candidate-src/solution.py")
)

# n=1 is the zero-iteration boundary; n=2 enters the even branch; n=3 enters
# the odd branch. The other fixed cases include the documented example and
# short/long mixed-parity paths.
fixed_inputs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 19, 27, 97, 871, 1000]

rng = random.Random(123_123)
generated_inputs = [rng.randint(1, 1_000_000) for _ in range(250)]
inputs = list(range(1, 1001)) + generated_inputs

mismatches: list[dict[str, object]] = []
property_failures: list[dict[str, object]] = []
all_results: list[tuple[int, list[int]]] = []

for n in inputs:
    expected = canonical(n)
    actual = candidate(n)
    if actual != expected:
        mismatches.append({"n": n, "canonical": expected, "candidate": actual})
    if actual != sorted(actual) or any(x % 2 != 1 for x in actual):
        property_failures.append({"n": n, "candidate": actual})
    all_results.append((n, actual))

for n in fixed_inputs:
    print(
        "fixed "
        + json.dumps(
            {"n": n, "canonical": canonical(n), "candidate": candidate(n)},
            separators=(",", ":"),
        )
    )

serialized = json.dumps(all_results, separators=(",", ":"), sort_keys=False)
print(f"scope=all integers 1..1000 plus 250 PRNG inputs in 1..1000000")
print("prng_seed=123123")
print("generated_inputs=" + json.dumps(generated_inputs, separators=(",", ":")))
print(f"comparison_count={len(inputs)}")
print(f"results_sha256={hashlib.sha256(serialized.encode()).hexdigest()}")
print(f"mismatch_count={len(mismatches)}")
print(f"property_failure_count={len(property_failures)}")

if mismatches:
    print("mismatches=" + json.dumps(mismatches, separators=(",", ":")))
if property_failures:
    print(
        "property_failures="
        + json.dumps(property_failures, separators=(",", ":"))
    )

raise SystemExit(1 if mismatches or property_failures else 0)
