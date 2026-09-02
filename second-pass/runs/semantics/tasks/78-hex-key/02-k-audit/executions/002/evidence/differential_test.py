#!/usr/bin/env python3
"""Independent differential test for HumanEval/78 over valid uppercase hex strings."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/hex-key-audit")
ALPHABET = "0123456789ABCDEF"
PRIME_DIGITS = frozenset("2357BD")


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.hex_key


def direct_contract(value: str) -> int:
    return sum(1 for char in value if char in PRIME_DIGITS)


def main() -> int:
    canonical = load_function(SCRATCH / "canonical.py", "trusted_canonical_78")
    generated = load_function(SCRATCH / "solution.py", "generated_solution_78")

    documented = [
        ("AB", 1),
        ("1077E", 2),
        ("ABED1A33", 4),
        ("123456789ABCDEF0", 6),
        ("2020", 2),
    ]
    boundaries = [
        ("", 0),
        *[(char, int(char in PRIME_DIGITS)) for char in ALPHABET],
        ("22222222", 8),
        ("00000000", 0),
        ("2357BD", 6),
        ("014689ACEF", 0),
        ("D0B1F2A3C5E7", 6),
        (ALPHABET * 256, 6 * 256),
    ]

    rng = random.Random(0x78)
    random_cases = [
        "".join(rng.choice(ALPHABET) for _ in range(rng.randrange(0, 257)))
        for _ in range(5_000)
    ]
    exhaustive_cases = (
        "".join(chars)
        for length in range(4)
        for chars in itertools.product(ALPHABET, repeat=length)
    )

    mismatches: list[tuple[str, int, int, int]] = []
    total = 0

    def check(value: str, expected: int | None = None) -> None:
        nonlocal total
        total += 1
        contract_value = direct_contract(value)
        canonical_value = canonical(value)
        generated_value = generated(value)
        wanted = contract_value if expected is None else expected
        if not (contract_value == wanted == canonical_value == generated_value):
            mismatches.append((value, wanted, canonical_value, generated_value))

    for value, expected in documented:
        check(value, expected)
    for value, expected in boundaries:
        check(value, expected)
    for value in exhaustive_cases:
        check(value)
    for value in random_cases:
        check(value)

    print("oracle: independently loaded trusted canonical.py plus direct contract count")
    print("domain: valid strings over 0123456789ABCDEF")
    print("documented_examples: 5")
    print("boundaries: empty, all 16 singleton branch cases, repeated true/false, mixed, length 4096")
    print("exhaustive_generated: all lengths 0..3 (4369 strings)")
    print("random_generated: 5000 strings, lengths 0..256, seed 0x78")
    print(f"total_checks: {total}")
    print(f"mismatch_count: {len(mismatches)}")
    for mismatch in mismatches[:20]:
        print("MISMATCH", repr(mismatch))
    print("satisfying_witness_empty: input='' expected=0")
    print("satisfying_witness_mixed: input='2A3D' expected=3")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
