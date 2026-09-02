#!/usr/bin/env python3
"""Independent differential test for trusted canonical.py vs candidate solution.py."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


CANONICAL_PATH = Path("/reference/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/reconstruction/solution.py")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.string_xor


def bit_strings(max_length: int) -> list[str]:
    values: list[str] = []
    for length in range(max_length + 1):
        values.extend("".join(bits) for bits in itertools.product("01", repeat=length))
    return values


canonical = load_function("trusted_canonical", CANONICAL_PATH)
candidate = load_function("candidate_solution", CANDIDATE_PATH)

# Explicit cases cover the documented example, empty inputs, unequal lengths,
# and all four one-character branch combinations (00, 11, 01, 10).
explicit_cases = [
    ("010", "110"),
    ("", ""),
    ("", "1"),
    ("0", ""),
    ("0", "0"),
    ("1", "1"),
    ("0", "1"),
    ("1", "0"),
    ("10", "1"),
    ("1", "10"),
    ("00000000", "11111111"),
    ("11111111", "00000000"),
]

exhaustive_values = bit_strings(6)
exhaustive_cases = list(itertools.product(exhaustive_values, repeat=2))

rng = random.Random(0x11_58_4F_52)
random_cases = [
    (
        "".join(rng.choice("01") for _ in range(rng.randrange(0, 65))),
        "".join(rng.choice("01") for _ in range(rng.randrange(0, 65))),
    )
    for _ in range(2000)
]

all_cases = explicit_cases + exhaustive_cases + random_cases
mismatches: list[tuple[str, str, str, str]] = []

print(f"canonical={CANONICAL_PATH}")
print(f"candidate={CANDIDATE_PATH}")
print(f"explicit_case_count={len(explicit_cases)}")
for a, b in explicit_cases:
    expected = canonical(a, b)
    actual = candidate(a, b)
    print(f"explicit a={a!r} b={b!r} canonical={expected!r} candidate={actual!r}")

print(
    "exhaustive_scope="
    "all ordered pairs of binary strings with each length in 0..6"
)
print(f"exhaustive_value_count={len(exhaustive_values)}")
print(f"exhaustive_case_count={len(exhaustive_cases)}")
print("random_scope=2000 deterministic pairs, each length uniformly selected in 0..64")
print("random_seed=0x11584f52")

for a, b in all_cases:
    expected = canonical(a, b)
    actual = candidate(a, b)
    if expected != actual:
        mismatches.append((a, b, expected, actual))

print(f"total_case_count={len(all_cases)}")
print(f"mismatch_count={len(mismatches)}")
for mismatch in mismatches[:20]:
    print(f"mismatch={mismatch!r}")

raise SystemExit(1 if mismatches else 0)
