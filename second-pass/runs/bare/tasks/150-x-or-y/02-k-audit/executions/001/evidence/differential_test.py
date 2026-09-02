#!/usr/bin/env python3
"""Independent candidate/canonical/contract differential test for HumanEval 150."""
import importlib.util
import math
import random
from pathlib import Path

BUILD = Path("/tmp/audit-work/build")


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.x_or_y


canonical = load_entry(BUILD / "canonical.py", "trusted_canonical")
generated = load_entry(BUILD / "solution.py", "generated_solution")


def contract_is_prime(n: int) -> bool:
    """Independent mathematical oracle: primes are integers >= 2 with no proper divisor."""
    if n < 2:
        return False
    return all(n % divisor for divisor in range(2, math.isqrt(n) + 1))


def expected(n: int, x: int, y: int) -> int:
    return x if contract_is_prime(n) else y


named = [
    ("prompt-prime", 7, 34, 12),
    ("prompt-composite", 15, 8, 5),
    ("negative", -5, 101, -202),
    ("zero", 0, 102, -203),
    ("below-prime-boundary", 1, 103, -204),
    ("smallest-prime", 2, 104, -205),
    ("loop-initially-false-prime", 3, 105, -206),
    ("first-divisor", 4, 106, -207),
    ("nondividing-iteration-then-exit", 5, 107, -208),
    ("loop-boundary-below-square", 8, 108, -209),
    ("odd-perfect-square", 9, 109, -210),
    ("loop-boundary-above-square", 10, 110, -211),
    ("later-divisor", 25, 111, -212),
    ("larger-perfect-square", 49, 112, -213),
    ("larger-prime", 97, 113, -214),
    ("larger-composite", 121, 114, -215),
    ("equal-results", 17, 77, 77),
]

rng = random.Random(150)
generated_cases = [
    (f"generated-{index}", n, rng.randint(-10_000, 10_000), rng.randint(-10_000, 10_000))
    for index, n in enumerate(range(-20, 501))
]
cases = named + generated_cases

generated_contract_mismatches = []
positive_canonical_mismatches = []
nonpositive_canonical_mismatches = []
for tag, n, x, y in cases:
    got_generated = generated(n, x, y)
    got_canonical = canonical(n, x, y)
    want = expected(n, x, y)
    row = (tag, n, x, y, got_generated, got_canonical, want)
    if got_generated != want:
        generated_contract_mismatches.append(row)
    if got_generated != got_canonical:
        if n >= 1:
            positive_canonical_mismatches.append(row)
        else:
            nonpositive_canonical_mismatches.append(row)

print("scalar function: no collection-valued empty case exists; n=0 is the numeric empty boundary")
print(f"documented_and_boundary_cases={len(named)}")
print(f"deterministic_generated_cases={len(generated_cases)} n_range=-20..500 seed=150")
print(f"generated_vs_contract_mismatches={len(generated_contract_mismatches)}")
print(f"generated_vs_canonical_mismatches_for_n>=1={len(positive_canonical_mismatches)}")
print(f"generated_vs_canonical_mismatches_for_n<=0={len(nonpositive_canonical_mismatches)}")
for tag, n, x, y in named:
    print(
        "NAMED",
        (tag, n, x, y, generated(n, x, y), canonical(n, x, y), expected(n, x, y)),
    )
for row in nonpositive_canonical_mismatches[:25]:
    print("EXPECTED_CANONICAL_CONTRACT_DISCREPANCY", row)

assert not generated_contract_mismatches
assert not positive_canonical_mismatches
assert nonpositive_canonical_mismatches
assert all(row[4] == row[6] and row[5] != row[6] for row in nonpositive_canonical_mismatches)
print("RESULT: generated implementation matches the stated primality contract on all tested integers")
print("RESULT: canonical differs only at tested n<=0, where it returns x for a non-prime")
