#!/usr/bin/env python3
"""Independent differential and contract checks for HumanEval/25."""

from __future__ import annotations

import importlib.util
import math
import random
from pathlib import Path


WORK = Path("/tmp/audit-work/25-factorize")


def load_function(module_name: str, source: Path):
    spec = importlib.util.spec_from_file_location(module_name, source)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.factorize


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 1
    return True


def contract_holds(n: int, factors: list[int]) -> bool:
    return (
        factors == sorted(factors)
        and all(is_prime(factor) for factor in factors)
        and math.prod(factors) == n
    )


def main() -> int:
    canonical = load_function("trusted_canonical", WORK / "canonical.py")
    generated = load_function("candidate_solution", WORK / "solution.py")

    documented = [8, 25, 70]
    boundary_and_branches = [
        1,       # empty factor list and loop guard initially false
        2, 3,    # smallest prime and first non-divisible trial step
        4, 6,    # repeated divisible branch and divisible/non-divisible mix
        7, 8, 9, 10, 11, 12,
        16, 17, 18, 24, 25, 26, 27,
        49, 64, 81, 97, 121, 169, 360, 997, 1024,
        9991, 65536, 99991,
    ]
    outside_positive_domain_observations = [-17, -1, 0]
    rng = random.Random(250025)
    generated_inputs = list(range(1, 2001))
    generated_inputs += [rng.randint(1, 100_000) for _ in range(250)]
    positive_inputs = sorted(set(documented + boundary_and_branches + generated_inputs))

    mismatches: list[tuple[int, list[int], list[int]]] = []
    contract_failures: list[tuple[int, list[int]]] = []
    for n in positive_inputs:
        expected = canonical(n)
        actual = generated(n)
        if actual != expected:
            mismatches.append((n, expected, actual))
        if n >= 1 and not contract_holds(n, actual):
            contract_failures.append((n, actual))

    expected_examples = {8: [2, 2, 2], 25: [5, 5], 70: [2, 5, 7]}
    example_failures = {
        n: generated(n)
        for n, expected in expected_examples.items()
        if generated(n) != expected
    }

    outside_observations: list[tuple[int, str, str]] = []
    for n in outside_positive_domain_observations:
        outcomes = []
        for function in (canonical, generated):
            try:
                outcomes.append(f"value:{function(n)!r}")
            except Exception as err:
                outcomes.append(f"exception:{type(err).__name__}:{err}")
        outside_observations.append((n, outcomes[0], outcomes[1]))

    print(f"positive_input_count={len(positive_inputs)}")
    print(f"positive_input_min={min(positive_inputs)} positive_input_max={max(positive_inputs)}")
    print(f"documented_examples={documented}")
    print(f"branch_boundary_inputs={boundary_and_branches}")
    print(f"outside_positive_domain_observations={outside_observations}")
    print("generated_scope=all integers 1..2000 plus 250 deterministic pseudorandom integers 1..100000")
    print(f"example_failures={example_failures}")
    print(f"differential_mismatch_count={len(mismatches)}")
    print(f"differential_mismatches={mismatches[:20]}")
    print(f"positive_domain_contract_failure_count={len(contract_failures)}")
    print(f"positive_domain_contract_failures={contract_failures[:20]}")
    return 0 if not (example_failures or mismatches or contract_failures) else 1


if __name__ == "__main__":
    raise SystemExit(main())
