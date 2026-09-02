#!/usr/bin/env python3
"""Independent differential test for HumanEval/131.

The tested implementation and oracle are loaded from separate scratch copies.
Inputs consist of explicit contract examples and branch/boundary witnesses,
every positive integer from 1 through 5,000, and 500 deterministic generated
positive integers up to 120 decimal digits.
"""

from __future__ import annotations

import hashlib
import importlib.util
import random
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/131-digits")


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.digits


canonical = load_entry(SCRATCH / "trusted" / "canonical.py", "trusted_canonical")
generated = load_entry(
    SCRATCH / "candidate-src" / "solution.py", "candidate_generated"
)

explicit = [
    0,  # boundary outside the positive-integer contract
    1,
    2,
    3,
    4,
    5,
    8,
    9,
    10,
    11,
    20,
    21,
    22,
    30,
    101,
    111,
    135,
    200,
    222,
    235,
    2468,
    10203,
    100000000000000000000000000000000000000000000000001,
    999999999999999999999999999999999999999999999999999,
]

rng = random.Random(131_2026)
generated_inputs = []
for _ in range(500):
    digits = rng.randint(1, 120)
    first = str(rng.randint(1, 9))
    rest = "".join(str(rng.randint(0, 9)) for _ in range(digits - 1))
    generated_inputs.append(int(first + rest))

inputs = explicit + list(range(1, 5001)) + generated_inputs
input_bytes = "".join(f"{n}\n" for n in inputs).encode()
input_sha256 = hashlib.sha256(input_bytes).hexdigest()

mismatches = []
for n in inputs:
    expected = canonical(n)
    actual = generated(n)
    if actual != expected:
        mismatches.append((n, expected, actual))

print("oracle=/tmp/audit-work/131-digits/trusted/canonical.py:digits")
print("subject=/tmp/audit-work/131-digits/candidate-src/solution.py:digits")
print(f"explicit_inputs={len(explicit)} (includes n=0 outside contract)")
print("exhaustive_positive_range=1..5000")
print("random_seed=1312026")
print("random_count=500")
print("random_decimal_digits=1..120")
print(f"total_executions={len(inputs)}")
print(f"serialized_input_sha256={input_sha256}")
print(f"mismatch_count={len(mismatches)}")
for mismatch in mismatches[:20]:
    print("MISMATCH", mismatch)

raise SystemExit(1 if mismatches else 0)
