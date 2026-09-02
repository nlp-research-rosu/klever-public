#!/usr/bin/env python3
"""Independent canonical-versus-generated differential and contract checks."""

from __future__ import annotations

import argparse
import importlib.util
import math
import random
from pathlib import Path
from types import ModuleType


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def is_prime(value: int) -> bool:
    return value >= 2 and all(
        value % divisor != 0
        for divisor in range(2, math.isqrt(value) + 1)
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", required=True)
    parser.add_argument("--generated", required=True)
    args = parser.parse_args()
    canonical = load_module("trusted_canonical", Path(args.canonical))
    generated = load_module("generated_solution", Path(args.generated))

    documented = [8, 25, 70]
    empty_result_boundary = [1]
    branch_boundaries = [
        2, 3, 4, 5, 6, 7, 9, 10, 15, 16, 17, 24, 26, 27, 32, 48,
        49, 64, 81, 97, 121, 125, 127, 169, 221,
    ]
    larger = [9973, 65536, 99991]
    rng = random.Random(2500729)
    generated_inputs = [rng.randint(1, 20_000) for _ in range(300)]
    inputs = sorted(set(
        documented
        + empty_result_boundary
        + branch_boundaries
        + larger
        + list(range(1, 301))
        + generated_inputs
    ))

    mismatches: list[tuple[int, object, object]] = []
    contract_failures: list[tuple[int, list[int], str]] = []
    for value in inputs:
        expected = canonical.factorize(value)
        actual = generated.factorize(value)
        if actual != expected:
            mismatches.append((value, actual, expected))
        if actual != sorted(actual):
            contract_failures.append((value, actual, "not nondecreasing"))
        if not all(is_prime(factor) for factor in actual):
            contract_failures.append((value, actual, "contains non-prime"))
        if math.prod(actual) != value:
            contract_failures.append((value, actual, "wrong product"))

    print(f"documented_inputs={documented}")
    print(f"empty_result_boundary={empty_result_boundary}")
    print(f"branch_boundaries={branch_boundaries}")
    print(f"larger_inputs={larger}")
    print("generated_seed=2500729 generated_count=300 generated_range=[1,20000]")
    print(f"unique_positive_inputs={len(inputs)}")
    print(f"mismatch_count={len(mismatches)}")
    print(f"contract_failure_count={len(contract_failures)}")
    if mismatches:
        print(f"mismatches={mismatches[:20]}")
    if contract_failures:
        print(f"contract_failures={contract_failures[:20]}")

    for value in [0, -1]:
        observations: dict[str, str] = {}
        for label, function in [
            ("canonical", canonical.factorize),
            ("generated", generated.factorize),
        ]:
            try:
                observations[label] = f"return {function(value)!r}"
            except Exception as error:
                observations[label] = f"raise {type(error).__name__}: {error}"
        print(f"outside_positive_domain n={value}: {observations}")

    if mismatches or contract_failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
