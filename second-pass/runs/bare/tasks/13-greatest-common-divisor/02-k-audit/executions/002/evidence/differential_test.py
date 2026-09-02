#!/usr/bin/env python3
"""Independent candidate/canonical/contract differential for HumanEval 13."""

from __future__ import annotations

import importlib.util
import math
import random
from pathlib import Path
from typing import Callable


def load_entry(path: Path) -> Callable[[int, int], int]:
    spec = importlib.util.spec_from_file_location(f"loaded_{path.stem}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.greatest_common_divisor


canonical = load_entry(Path("/reference/canonical.py"))
candidate = load_entry(Path("/tmp/audit-work/reconstruction/solution.py"))

named_cases = [
    ("documented-3-5", 3, 5),
    ("documented-25-15", 25, 15),
    ("both-zero", 0, 0),
    ("left-zero", 0, 1),
    ("right-zero", 1, 0),
    ("left-negative-boundary", -1, 0),
    ("right-negative-boundary", 0, -1),
    ("both-negative-boundary", -1, -1),
    ("left-negative", -25, 15),
    ("right-negative", 25, -15),
    ("both-negative", -25, -15),
    ("equal", 17, 17),
    ("coprime", 101, 103),
    ("multiple", 144, 12),
    ("large", 2**61 - 1, 2**31 - 1),
]

cases: list[tuple[str, int, int]] = list(named_cases)
for a in range(-20, 21):
    for b in range(-20, 21):
        cases.append(("grid", a, b))
rng = random.Random(130013)
for _ in range(500):
    cases.append(
        (
            "seeded-random",
            rng.randint(-(10**12), 10**12),
            rng.randint(-(10**12), 10**12),
        )
    )

candidate_canonical_mismatches: list[tuple[str, int, int, int, int]] = []
candidate_contract_mismatches: list[tuple[str, int, int, int, int]] = []
canonical_contract_mismatches: list[tuple[str, int, int, int, int]] = []
for label, a, b in cases:
    canonical_result = canonical(a, b)
    candidate_result = candidate(a, b)
    contract_result = math.gcd(a, b)
    if candidate_result != canonical_result:
        candidate_canonical_mismatches.append(
            (label, a, b, candidate_result, canonical_result)
        )
    if candidate_result != contract_result:
        candidate_contract_mismatches.append(
            (label, a, b, candidate_result, contract_result)
        )
    if canonical_result != contract_result:
        canonical_contract_mismatches.append(
            (label, a, b, canonical_result, contract_result)
        )

print(f"case_count={len(cases)}")
print(
    "candidate_vs_canonical_mismatch_count="
    f"{len(candidate_canonical_mismatches)}"
)
print(
    "candidate_vs_math_gcd_mismatch_count="
    f"{len(candidate_contract_mismatches)}"
)
print(
    "canonical_vs_math_gcd_mismatch_count="
    f"{len(canonical_contract_mismatches)}"
)
print("candidate_vs_canonical_first_20=")
for row in candidate_canonical_mismatches[:20]:
    print(row)
print("candidate_vs_math_gcd_first_20=")
for row in candidate_contract_mismatches[:20]:
    print(row)

if candidate_contract_mismatches:
    raise SystemExit("candidate diverges from the ordinary nonnegative GCD contract")
if candidate_canonical_mismatches:
    raise SystemExit(
        "candidate and canonical diverge; all observed divergences are also "
        "canonical-vs-math.gcd divergences"
    )
