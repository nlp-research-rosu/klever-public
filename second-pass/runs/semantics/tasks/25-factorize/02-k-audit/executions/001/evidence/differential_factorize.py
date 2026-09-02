#!/usr/bin/env python3
"""Independent differential/contract test for HumanEval problem 25."""

from __future__ import annotations

import importlib.util
import json
import math
import random
import sys
from pathlib import Path

sys.dont_write_bytecode = True

CANONICAL = Path("/reference/canonical.py")
GENERATED = Path("/tmp/audit-work/25-factorize-audit/solution.py")


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.factorize


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    return all(value % divisor for divisor in range(2, math.isqrt(value) + 1))


def contract_holds(n: int, factors: list[int]) -> bool:
    return (
        factors == sorted(factors)
        and all(is_prime(factor) for factor in factors)
        and math.prod(factors) == n
    )


def main() -> int:
    canonical = load_entry(CANONICAL, "trusted_canonical")
    generated = load_entry(GENERATED, "candidate_generated")

    documented = [8, 25, 70]
    boundaries_and_branches = [
        1,  # loop false immediately; empty factor list
        2,  # loop true; divisible branch; then exit
        3,  # non-divisible branch followed by divisible branch
        4,  # repeated factor / divisible branch retained at same divisor
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        15,
        16,
        17,
        25,
        27,
        32,
        49,
        64,
        81,
        97,
        121,
        169,
        256,
        360,
        997,
    ]
    exhaustive_small = list(range(1, 1001))
    rng = random.Random(250025)
    generated_inputs = [rng.randint(1, 50_000) for _ in range(128)]

    inputs = sorted(
        set(documented + boundaries_and_branches + exhaustive_small + generated_inputs)
    )
    print("INPUTS_JSON=" + json.dumps(inputs, separators=(",", ":")))
    print(
        "SCOPE="
        + json.dumps(
            {
                "domain": "positive Python integers",
                "documented_examples": documented,
                "small_exhaustive": [1, 1000],
                "random_seed": 250025,
                "random_count": 128,
                "random_range": [1, 50_000],
                "unique_input_count": len(inputs),
            },
            sort_keys=True,
        )
    )

    mismatches: list[dict[str, object]] = []
    contract_failures: list[dict[str, object]] = []
    for n in inputs:
        expected = canonical(n)
        actual = generated(n)
        if actual != expected:
            mismatches.append({"n": n, "canonical": expected, "generated": actual})
        if not contract_holds(n, actual):
            contract_failures.append({"n": n, "generated": actual})

    print("MISMATCH_COUNT=" + str(len(mismatches)))
    print("CONTRACT_FAILURE_COUNT=" + str(len(contract_failures)))
    if mismatches:
        print("MISMATCHES=" + json.dumps(mismatches, sort_keys=True))
    if contract_failures:
        print("CONTRACT_FAILURES=" + json.dumps(contract_failures, sort_keys=True))
    print("RESULT=" + ("PASS" if not mismatches and not contract_failures else "FAIL"))
    return 0 if not mismatches and not contract_failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
