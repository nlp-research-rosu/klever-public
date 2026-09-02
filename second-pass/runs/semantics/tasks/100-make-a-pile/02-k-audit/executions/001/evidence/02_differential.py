#!/usr/bin/env python3
"""Independent candidate-vs-canonical differential test for make_a_pile."""

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
    return module.make_a_pile


canonical = load_entry("trusted_canonical", Path("/reference/canonical.py"))
generated = load_entry("scratch_solution", Path("/tmp/audit-work/solution.py"))

# The contract says positive integers. Zero is the empty/loop-false boundary;
# -1 is an explicitly out-of-domain robustness observation.
documented_and_boundaries = [-1, 0, 1, 2, 3, 4, 5, 10, 99, 100]
rng = random.Random(100)
representative_generated = [rng.randint(1, 500) for _ in range(128)]
inputs = documented_and_boundaries + representative_generated

mismatches = []
case_digests = []
for n in inputs:
    expected = canonical(n)
    actual = generated(n)
    if expected != actual:
        mismatches.append({"n": n, "canonical": expected, "generated": actual})
    encoded = json.dumps(
        {"n": n, "canonical": expected, "generated": actual},
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    case_digests.append(hashlib.sha256(encoded).hexdigest())

print("ORACLE=/reference/canonical.py:make_a_pile")
print("GENERATED=/tmp/audit-work/solution.py:make_a_pile")
print("FORMAL_DOMAIN=positive integers")
print("OUT_OF_DOMAIN_OBSERVATIONS=[-1,0]")
print("INPUTS=" + json.dumps(inputs))
print(f"CASE_COUNT={len(inputs)}")
print(f"MISMATCH_COUNT={len(mismatches)}")
print("MISMATCHES=" + json.dumps(mismatches, sort_keys=True))
print(
    "EXPLICIT_BOUNDARY_RESULTS="
    + json.dumps(
        {
            str(n): {
                "canonical": canonical(n),
                "generated": generated(n),
            }
            for n in [-1, 0, 1, 2, 3, 4, 10]
        },
        sort_keys=True,
    )
)
print(
    "RESULT_DIGEST="
    + hashlib.sha256("".join(case_digests).encode()).hexdigest()
)

raise SystemExit(1 if mismatches else 0)
