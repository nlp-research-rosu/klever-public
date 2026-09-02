#!/usr/bin/env python3
"""Independent differential and contract test for HumanEval/159."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import random
import sys


def load_eat(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.eat


canonical = load_eat("trusted_canonical_159", Path(sys.argv[1]))
generated = load_eat("candidate_solution_159", Path(sys.argv[2]))

documented = [
    ((5, 6, 10), [11, 4]),
    ((4, 8, 9), [12, 1]),
    ((1, 10, 10), [11, 0]),
    ((2, 11, 5), [7, 0]),
]
zero_and_boundary = [
    (0, 0, 0),
    (0, 0, 1000),
    (0, 1000, 0),
    (1000, 0, 0),
    (1000, 1000, 1000),
    (1000, 999, 1000),
    (1000, 1000, 999),
    (0, 1, 0),
    (0, 0, 1),
    (0, 500, 500),
    (0, 501, 500),
]

mismatches: list[tuple] = []
checks = 0


def expected(number: int, need: int, remaining: int) -> list[int]:
    eaten_now = min(need, remaining)
    return [number + eaten_now, remaining - eaten_now]


def check(case: tuple[int, int, int], explicit: list[int] | None = None) -> None:
    global checks
    checks += 1
    trusted_value = canonical(*case)
    generated_value = generated(*case)
    contract_value = expected(*case)
    wanted = contract_value if explicit is None else explicit
    if not (
        trusted_value == generated_value == contract_value == wanted
        and type(trusted_value) is list
        and type(generated_value) is list
        and all(type(x) is int for x in trusted_value + generated_value)
    ):
        mismatches.append(
            (case, trusted_value, generated_value, contract_value, wanted)
        )


for case, wanted in documented:
    check(case, wanted)
for case in zero_and_boundary:
    check(case)

# Exhaust all (need, remaining) branch combinations and both sides of every
# need <= remaining boundary for representative values of the independent
# additive input `number`.
number_sample = [0, 1, 500, 999, 1000]
for number in number_sample:
    for need in range(1001):
        for remaining in range(1001):
            check((number, need, remaining))

# Broader generated triples across the full documented cube.
seed = 159_2026
rng = random.Random(seed)
random_count = 20_000
for _ in range(random_count):
    check(tuple(rng.randint(0, 1000) for _ in range(3)))

print(f"documented_cases={len(documented)}")
print(f"zero_and_boundary_cases={len(zero_and_boundary)}")
print(
    "exhaustive_grid="
    f"number in {number_sample}; need and remaining each in 0..1000"
)
print(f"generated_cases={random_count}; seed={seed}; domain=0..1000 cubed")
print(f"total_checks={checks}")
print(f"mismatches={len(mismatches)}")
for mismatch in mismatches[:20]:
    print(f"MISMATCH={mismatch!r}")

raise SystemExit(1 if mismatches else 0)
