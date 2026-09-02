#!/usr/bin/env python3
"""Independent contract/differential checks for HumanEval 144."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path
from typing import Callable


def load_entry(path: Path, module_name: str) -> Callable[[str, str], bool]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.simplify


def exact_contract(x: str, n: str) -> bool:
    a_text, b_text = x.split("/")
    c_text, d_text = n.split("/")
    a, b, c, d = map(int, (a_text, b_text, c_text, d_text))
    return (a * c) % (b * d) == 0


def main() -> int:
    canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical_144")
    generated = load_entry(Path("/candidate/solution.py"), "generated_solution_144")

    documented = [
        ("1/5", "5/1", True),
        ("1/6", "2/1", False),
        ("7/10", "10/2", False),
    ]
    boundary_and_branches = [
        ("1/1", "1/1", True),
        ("1/2", "1/1", False),
        ("1/2", "2/1", True),
        ("2/3", "3/2", True),
        ("1/2", "3/1", False),
        ("0001/0002", "0002/0001", True),
        ("999999/1000000", "1000000/999999", True),
    ]
    intended = documented + boundary_and_branches
    generated_contract_mismatches: list[tuple[str, str, bool, bool]] = []
    canonical_contract_mismatches: list[tuple[str, str, bool, bool]] = []
    differential_mismatches: list[tuple[str, str, bool, bool]] = []

    def check(x: str, n: str) -> None:
        expected = exact_contract(x, n)
        actual_generated = generated(x, n)
        actual_canonical = canonical(x, n)
        if actual_generated != expected:
            generated_contract_mismatches.append((x, n, actual_generated, expected))
        if actual_canonical != expected:
            canonical_contract_mismatches.append((x, n, actual_canonical, expected))
        if actual_generated != actual_canonical:
            differential_mismatches.append((x, n, actual_generated, actual_canonical))

    print("DOCUMENTED_AND_BOUNDARY_CASES")
    for x, n, stated in intended:
        expected = exact_contract(x, n)
        generated_value = generated(x, n)
        canonical_value = canonical(x, n)
        print(
            f"{x} * {n}: stated={stated} exact={expected} "
            f"generated={generated_value} canonical={canonical_value}"
        )
        check(x, n)

    exhaustive_count = 0
    for a in range(1, 13):
        for b in range(1, 13):
            for c in range(1, 13):
                for d in range(1, 13):
                    check(f"{a}/{b}", f"{c}/{d}")
                    exhaustive_count += 1

    rng = random.Random(144)
    random_count = 5000
    for _ in range(random_count):
        a, b, c, d = (rng.randint(1, 1_000_000) for _ in range(4))
        check(f"{a}/{b}", f"{c}/{d}")

    print(f"EXHAUSTIVE_SCOPE a,b,c,d in 1..12 count={exhaustive_count}")
    print(f"RANDOM_SCOPE seed=144 count={random_count} components=1..1000000")
    print(f"generated_contract_mismatches={len(generated_contract_mismatches)}")
    print(f"canonical_contract_mismatches_moderate={len(canonical_contract_mismatches)}")
    print(f"generated_vs_canonical_mismatches_moderate={len(differential_mismatches)}")

    # This is an intended-domain precision boundary, not a malformed input:
    # exact quotient is 4503599627370496.5. CPython float division rounds it to
    # an integer-valued float, while the exact candidate and the stated
    # whole-number contract correctly return False.
    large_x = "9007199254740993/1"
    large_n = "1/2"
    large_expected = exact_contract(large_x, large_n)
    large_generated = generated(large_x, large_n)
    large_canonical = canonical(large_x, large_n)
    print(
        "LARGE_FLOAT_PRECISION_BOUNDARY "
        f"{large_x} * {large_n}: exact={large_expected} "
        f"generated={large_generated} canonical={large_canonical}"
    )

    invalid_cases = [
        ("", "1/1"),
        ("1/1", ""),
        ("1/0", "1/1"),
    ]
    print("OUT_OF_CONTRACT_INVALID_CASES")
    for x, n in invalid_cases:
        outcomes = []
        for label, function in (("generated", generated), ("canonical", canonical)):
            try:
                outcomes.append(f"{label}=value:{function(x, n)!r}")
            except Exception as err:  # audit records exception class only
                outcomes.append(f"{label}=exception:{type(err).__name__}")
        print(f"{x!r}, {n!r}: " + " ".join(outcomes))

    ok = (
        not generated_contract_mismatches
        and not canonical_contract_mismatches
        and not differential_mismatches
        and large_generated == large_expected
        and large_canonical != large_expected
    )
    print(f"EXPECTED_LARGE_CANONICAL_FLOAT_DIVERGENCE={large_canonical != large_expected}")
    print(f"OVERALL_EXPECTATIONS_MET={ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
