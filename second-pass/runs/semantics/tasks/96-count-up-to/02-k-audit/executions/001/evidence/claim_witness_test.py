#!/usr/bin/env python3
"""Ground witnesses for each formal claim and its result summary."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.count_up_to


canonical = load_entry(Path("/reference/canonical.py"), "canonical_witness")
generated = load_entry(
    Path("/tmp/audit-work/96-count-up-to/source/solution.py"),
    "generated_witness",
)


def no_divisor(c: int, d: int, hi: int) -> bool:
    """Ground evaluator of verification.k's noDivisor equations."""
    while d < hi:
        if c % d == 0:
            return False
        d += 1
    return True


def append_if_prime(values: list[int], i: int, prime: bool) -> list[int]:
    return values + [i] if prime else values


def primes_acc(values: list[int], i: int, n: int) -> list[int]:
    """Ground evaluator of verification.k's primesAcc equations."""
    while i < n:
        values = append_if_prime(values, i, no_divisor(i, 2, i))
        i += 1
    return values


inner_witnesses = [
    # (candidate C, divisor D, incoming B, expected outgoing B)
    (5, 2, True, True),
    (6, 2, True, False),
    (6, 3, False, False),
]
for c, d, incoming, expected in inner_witnesses:
    actual = incoming and no_divisor(c, d, c)
    assert actual is expected

outer_witness = {"VS": [], "I": 2, "N": 5}
outer_result = primes_acc(
    outer_witness["VS"][:], outer_witness["I"], outer_witness["N"]
)
assert outer_result == [2, 3]

entry_witnesses = [2, 3, 5, 11, 20]
boundary_witnesses = [0, 1]
rows = []
for n in entry_witnesses:
    formal = primes_acc([], 2, n)
    trusted = canonical(n)
    actual = generated(n)
    assert formal == trusted == actual
    rows.append((n, "N >= 2", formal, trusted, actual))
for n in boundary_witnesses:
    formal = []
    trusted = canonical(n)
    actual = generated(n)
    assert formal == trusted == actual
    rows.append((n, "0 <= N < 2", formal, trusted, actual))

print(f"INNER_WITNESSES={inner_witnesses}")
print(f"OUTER_WITNESS={outer_witness}; FORMAL_RESULT={outer_result}")
for n, domain, formal, trusted, actual in rows:
    print(
        f"ENTRY_WITNESS N={n} DOMAIN={domain} "
        f"FORMAL={formal} CANONICAL={trusted} GENERATED={actual}"
    )
print("MISMATCH_COUNT=0")
