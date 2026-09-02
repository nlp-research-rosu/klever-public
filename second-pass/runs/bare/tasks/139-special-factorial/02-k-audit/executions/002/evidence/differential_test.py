#!/usr/bin/env python3
"""Independent CPython differential for HumanEval/139.

The canonical and candidate modules are loaded from explicit scratch paths and
share no implementation code. The test records both returned values and
exceptions, including the recursion boundary of the generated implementation.
"""

from __future__ import annotations

import importlib.util
import random
import sys
from pathlib import Path


CANONICAL = Path("/tmp/audit-work/trusted/canonical.py")
CANDIDATE = Path("/tmp/audit-work/candidate-src/solution.py")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def outcome(function, n: int):
    try:
        return ("return", function(n))
    except Exception as error:  # Record semantic divergence, do not hide it.
        return ("raise", type(error).__name__, str(error))


def compact(value):
    if value[0] == "raise":
        return value
    integer = value[1]
    return (
        "return",
        f"bits={integer.bit_length()}",
        f"mod_1000000007={integer % 1_000_000_007}",
    )


def main() -> int:
    canonical = load_module("trusted_canonical_139", CANONICAL).special_factorial
    candidate = load_module("generated_solution_139", CANDIDATE).special_factorial
    print(f"python={sys.version.split()[0]} recursion_limit={sys.getrecursionlimit()}")
    print("contract_domain=positive integers (n > 0)")
    print("empty_case=not applicable: the contract takes one scalar integer")

    # Explicit examples, branch boundary, ordinary points, and off-contract
    # observations. The random sample is deterministic and documented.
    in_domain = {
        1,
        2,
        3,
        4,
        5,
        6,
        10,
        20,
        40,
        60,
        100,
        250,
        500,
        750,
        900,
        950,
        975,
        990,
        995,
        996,
        997,
        998,
        999,
        1000,
        1001,
    }
    in_domain.update(range(1, 81))
    rng = random.Random(139)
    in_domain.update(rng.randint(1, 1001) for _ in range(40))

    mismatches = []
    for n in sorted(in_domain):
        trusted = outcome(canonical, n)
        generated = outcome(candidate, n)
        if trusted != generated:
            mismatches.append((n, trusted, generated))
            print(
                f"MISMATCH n={n} canonical={compact(trusted)} "
                f"candidate={compact(generated)}"
            )

    for n in (-2, -1, 0):
        trusted = outcome(canonical, n)
        generated = outcome(candidate, n)
        print(
            f"OUTSIDE_DOMAIN n={n} canonical={compact(trusted)} "
            f"candidate={compact(generated)} equal={trusted == generated}"
        )

    print("DOCUMENTED_EXAMPLE n=4 expected=288")
    print(f"  canonical={canonical(4)} candidate={candidate(4)}")
    print(
        f"SUMMARY in_domain_cases={len(in_domain)} "
        f"mismatches={len(mismatches)}"
    )
    # This exits nonzero on any intended-domain divergence so the transcript
    # itself cannot be mistaken for a passing differential.
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
