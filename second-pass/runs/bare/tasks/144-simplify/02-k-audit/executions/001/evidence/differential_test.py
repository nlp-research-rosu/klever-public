#!/usr/bin/env python3
"""Independent differential and contract test for HumanEval 144."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


CANONICAL_PATH = Path("/tmp/audit-work/review-144/reference/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/review-144/source/solution.py")


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.simplify


def observe(function, x: str, n: str):
    try:
        return ("return", function(x, n))
    except Exception as err:  # Invalid/off-domain cases are recorded, not hidden.
        return ("exception", type(err).__name__)


def math_oracle(x: str, n: str) -> bool:
    a_text, b_text = x.split("/")
    c_text, d_text = n.split("/")
    a, b, c, d = map(int, (a_text, b_text, c_text, d_text))
    return (a * c) % (b * d) == 0


def main() -> int:
    canonical = load_entry("trusted_canonical_144", CANONICAL_PATH)
    generated = load_entry("generated_solution_144", GENERATED_PATH)

    named_valid = [
        ("example_true", "1/5", "5/1"),
        ("example_false_one", "1/6", "2/1"),
        ("example_false_two", "7/10", "10/2"),
        ("minimum_values", "1/1", "1/1"),
        ("remainder_zero_boundary", "1/2", "2/1"),
        ("remainder_one_boundary", "1/2", "3/1"),
        ("proper_fraction", "1/2", "1/1"),
        ("improper_integer", "6/3", "1/1"),
        ("cross_cancel_integer", "2/3", "3/2"),
        ("float_precision_witness", "9007199254740993/2", "1/1"),
        ("large_exact_integer", "9007199254740993/1", "1/1"),
        ("very_large_python_int", f"{10**400}/3", "1/1"),
    ]
    invalid = [
        ("empty_x", "", "1/1"),
        ("empty_n", "1/1", ""),
        ("zero_denominator_x", "1/0", "1/1"),
        ("zero_denominator_n", "1/1", "1/0"),
        ("missing_slash", "11", "1/1"),
        ("extra_slash", "1/2/3", "1/1"),
    ]

    valid_cases = [(label, x, n) for label, x, n in named_valid]
    for a in range(1, 13):
        for b in range(1, 13):
            for c in range(1, 13):
                for d in range(1, 13):
                    valid_cases.append(
                        (f"exhaustive_1_12_{a}_{b}_{c}_{d}", f"{a}/{b}", f"{c}/{d}")
                    )

    rng = random.Random(144)
    for index in range(2000):
        a, b, c, d = (rng.randint(1, 1_000_000) for _ in range(4))
        valid_cases.append((f"random_{index}", f"{a}/{b}", f"{c}/{d}"))

    generated_contract_mismatches = []
    canonical_generated_mismatches = []
    for label, x, n in valid_cases:
        expected = ("return", math_oracle(x, n))
        canonical_result = observe(canonical, x, n)
        generated_result = observe(generated, x, n)
        if generated_result != expected:
            generated_contract_mismatches.append(
                (label, x, n, expected, generated_result)
            )
        if canonical_result != generated_result:
            canonical_generated_mismatches.append(
                (label, x, n, canonical_result, generated_result, expected)
            )

    print(f"canonical={CANONICAL_PATH}")
    print(f"generated={GENERATED_PATH}")
    print("oracle=(a*c) % (b*d) == 0 over positive base-10 integers")
    print(f"named_valid_cases={len(named_valid)}")
    print("exhaustive_scope=a,b,c,d in 1..12")
    print("random_scope=2000 cases, seed=144, each component in 1..1000000")
    print(f"total_valid_cases={len(valid_cases)}")
    print(f"generated_contract_mismatches={len(generated_contract_mismatches)}")
    print(f"canonical_generated_mismatches={len(canonical_generated_mismatches)}")
    for mismatch in canonical_generated_mismatches[:20]:
        print(f"canonical_generated_mismatch={mismatch!r}")

    print(f"invalid_cases={len(invalid)}")
    for label, x, n in invalid:
        print(
            f"invalid_case={label!r}, x={x!r}, n={n!r}, "
            f"canonical={observe(canonical, x, n)!r}, "
            f"generated={observe(generated, x, n)!r}"
        )

    if generated_contract_mismatches:
        for mismatch in generated_contract_mismatches[:20]:
            print(f"generated_contract_mismatch={mismatch!r}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
