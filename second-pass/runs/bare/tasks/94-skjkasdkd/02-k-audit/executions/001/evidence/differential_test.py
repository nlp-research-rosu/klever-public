#!/usr/bin/env python3
"""Independent candidate/canonical differential for HumanEval/94."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path
from typing import Callable


def load_function(path: Path, module_name: str) -> Callable[[list[int]], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.skjkasdkd


canonical = load_function(Path("/reference/canonical.py"), "trusted_canonical_94")
candidate = load_function(
    Path("/tmp/audit-work/94-skjkasdkd/source/solution.py"),
    "candidate_solution_94",
)


def contract_oracle(values: list[int]) -> int:
    """Largest mathematical prime's digit sum; return 0 if there is no prime."""

    def is_prime(value: int) -> bool:
        if value < 2:
            return False
        divisor = 2
        while divisor * divisor <= value:
            if value % divisor == 0:
                return False
            divisor += 1
        return True

    primes = [value for value in values if is_prime(value)]
    return sum(int(digit) for digit in str(max(primes))) if primes else 0


def outcome(function: Callable[[list[int]], int], values: list[int]) -> tuple[str, object]:
    try:
        return ("return", function(list(values)))
    except BaseException as error:  # record semantic divergence, including RecursionError
        return ("raise", f"{type(error).__name__}: {error}")


prompt_examples = [
    ([0, 3, 2, 1, 3, 5, 7, 4, 5, 5, 5, 2, 181, 32, 4, 32, 3, 2, 32, 324, 4, 3], 10),
    ([1, 0, 1, 8, 2, 4597, 2, 1, 3, 40, 1, 2, 1, 2, 4, 2, 5, 1], 25),
    ([1, 3, 1, 32, 5107, 34, 83278, 109, 163, 23, 2323, 32, 30, 1, 9, 3], 13),
    ([0, 724, 32, 71, 99, 32, 6, 0, 5, 91, 83, 0, 5, 6], 11),
    ([0, 81, 12, 3, 1, 21], 3),
    ([0, 8, 1, 2, 1, 7], 7),
]

named_cases = [
    ("empty", []),
    ("negative-only", [-9, -2, -1]),
    ("zero", [0]),
    ("one-only", [1]),
    ("zero-and-one", [0, 1]),
    ("first-prime-boundary", [2]),
    ("first-odd-prime", [3]),
    ("small-square", [4]),
    ("prime-vs-composite", [4, 5]),
    ("divisor-square-equality", [9, 25, 49]),
    ("strict-square-cutoff", [7, 11, 23]),
    ("duplicate-largest", [11, 3, 11, 7]),
    ("larger-prime-left", [13, 11]),
    ("larger-prime-right", [11, 13]),
    ("single-digit-sum", [7]),
    ("two-digit-sum", [11]),
    ("embedded-zero-digit", [101]),
    ("four-digit-prime", [9973]),
    ("large-composite-fast-divisor", [1_000_000]),
    ("large-prime-recursion-boundary", [1_000_003]),
    ("mixed-sign", [-11, 0, 1, 2, 4]),
    ("no-prime-composites", [0, 4, 6, 8, 9, 10]),
]

small_values = (-2, -1, 0, 1, 2, 3, 4, 5, 8, 9, 10, 11)
exhaustive_cases = [
    list(values)
    for length in range(5)
    for values in itertools.product(small_values, repeat=length)
]

seed = 940094
rng = random.Random(seed)
generated_cases = [
    [rng.randint(-100, 10_000) for _ in range(rng.randint(0, 30))]
    for _ in range(1_000)
]

long_cases = [
    ("length-950", [2] * 950),
    ("length-990", [2] * 990),
    ("length-1000", [2] * 1000),
    ("length-1100", [2] * 1100),
]

all_regular = (
    [(f"prompt-{index}", values) for index, (values, _expected) in enumerate(prompt_examples, 1)]
    + named_cases
    + [(f"exhaustive-{index}", values) for index, values in enumerate(exhaustive_cases)]
    + [(f"generated-{index}", values) for index, values in enumerate(generated_cases)]
)

candidate_canonical_mismatches: list[tuple[str, list[int], object, object, int]] = []
candidate_oracle_mismatches: list[tuple[str, list[int], object, int]] = []
canonical_oracle_mismatches: list[tuple[str, list[int], object, int]] = []

print("DOCUMENTED_EXAMPLES")
for index, (values, expected) in enumerate(prompt_examples, 1):
    can = outcome(canonical, values)
    cand = outcome(candidate, values)
    oracle = contract_oracle(values)
    print(
        f"prompt-{index}: expected={expected} canonical={can!r} "
        f"candidate={cand!r} oracle={oracle}"
    )

for label, values in all_regular + long_cases:
    can = outcome(canonical, values)
    cand = outcome(candidate, values)
    oracle = contract_oracle(values)
    if cand != can:
        candidate_canonical_mismatches.append((label, values, cand, can, oracle))
    if cand != ("return", oracle):
        candidate_oracle_mismatches.append((label, values, cand, oracle))
    if can != ("return", oracle):
        canonical_oracle_mismatches.append((label, values, can, oracle))

print("INPUT_SCOPE")
print(f"small_values={small_values!r}")
print("exhaustive_lengths=0..4")
print(f"exhaustive_count={len(exhaustive_cases)}")
print(f"random_seed={seed}")
print("generated_count=1000 generated_length=0..30 generated_values=-100..10000")
print("long_lengths=950,990,1000,1100 values_all_2")
print(f"total_executed={len(all_regular) + len(long_cases)}")

print("MISMATCH_COUNTS")
print(f"candidate_vs_canonical={len(candidate_canonical_mismatches)}")
print(f"candidate_vs_contract_oracle={len(candidate_oracle_mismatches)}")
print(f"canonical_vs_contract_oracle={len(canonical_oracle_mismatches)}")

for heading, mismatches in (
    ("CANDIDATE_CANONICAL_FIRST_40", candidate_canonical_mismatches),
    ("CANDIDATE_ORACLE_FIRST_40", candidate_oracle_mismatches),
    ("CANONICAL_ORACLE_FIRST_40", canonical_oracle_mismatches),
):
    print(heading)
    for record in mismatches[:40]:
        label, values, *rest = record
        bounded_values = values if len(values) <= 40 else values[:40] + ["..."]
        print(f"{label}: input={bounded_values!r} outcomes={rest!r}")

if candidate_canonical_mismatches:
    raise SystemExit(1)
