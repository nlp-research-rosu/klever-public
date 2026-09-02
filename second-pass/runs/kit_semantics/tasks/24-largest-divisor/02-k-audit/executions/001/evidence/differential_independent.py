#!/usr/bin/env python3
"""Independent differential audit of canonical.py and solution.py."""

from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import random


SCRATCH = Path("/tmp/audit-work/audit-24")


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.largest_divisor


def mathematical_oracle(n: int) -> int:
    """Largest positive proper divisor via the least prime factor."""
    factor = 2
    while factor * factor <= n:
        if n % factor == 0:
            return n // factor
        factor += 1
    return 1


def proof_summary_equations(n: int, d: int) -> int:
    """Executable reading of verification.k's two guarded equations."""
    while n % d != 0:
        d -= 1
    return d


def main() -> None:
    canonical = load_entry("trusted_canonical", SCRATCH / "canonical.py")
    generated = load_entry("generated_solution", SCRATCH / "solution.py")

    documented_and_boundaries = [
        15,  # documented example
        2,   # minimum valid input; while condition initially false
        3,   # one loop iteration, then divisor 1
        4,   # one loop iteration, then divisor 2
        5,   # prime
        6,   # composite with two loop iterations
        7,   # prime
        8,   # prime-power composite
        9,   # odd square
        10,
        25,
        49,
        97,
        100,
        997,
        1000,
        1999,
        2000,
    ]
    exhaustive = list(range(2, 2001))
    generator = random.Random(240024)
    generated_inputs = [generator.randint(2, 10000) for _ in range(256)]
    inputs = sorted(set(documented_and_boundaries + exhaustive + generated_inputs))

    mismatches = []
    for n in inputs:
        expected = mathematical_oracle(n)
        summary_result = proof_summary_equations(n, n - 1)
        canonical_result = canonical(n)
        generated_result = generated(n)
        if not (
            canonical_result == generated_result == summary_result == expected
            and 1 <= generated_result < n
            and n % generated_result == 0
        ):
            mismatches.append(
                (
                    n,
                    canonical_result,
                    generated_result,
                    summary_result,
                    expected,
                )
            )

    encoded_inputs = ",".join(map(str, inputs)).encode()
    print("intended_domain=n>=2")
    print("empty_case=not-applicable (the contract takes one integer)")
    print("documented_example=15 expected=5")
    print("branch_boundaries=2(initial false),3(one iteration to 1),4(one iteration to 2)")
    print("exhaustive_scope=2..2000 inclusive")
    print("generated_scope=256 draws from [2,10000], seed=240024")
    print(f"unique_inputs={len(inputs)}")
    print(f"input_list_sha256={hashlib.sha256(encoded_inputs).hexdigest()}")
    for n in documented_and_boundaries:
        print(
            f"boundary n={n} canonical={canonical(n)} "
            f"generated={generated(n)} "
            f"proof_summary={proof_summary_equations(n, n - 1)} "
            f"oracle={mathematical_oracle(n)}"
        )
    print(f"mismatches={len(mismatches)}")
    if mismatches:
        for mismatch in mismatches[:20]:
            print(f"MISMATCH {mismatch}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
