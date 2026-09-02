#!/usr/bin/env python3
"""Independent differential test for HumanEval 68-pluck."""

from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
from pathlib import Path
import random
import sys


def load_entry(module_name: str, path: Path):
    spec = spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.pluck


def independent_oracle(values: list[int]) -> list[int]:
    best: tuple[int, int] | None = None
    for index, value in enumerate(values):
        if value % 2 == 0 and (best is None or value < best[0]):
            best = (value, index)
    return [] if best is None else [best[0], best[1]]


def main() -> int:
    canonical = load_entry("trusted_canonical", Path("/reference/canonical.py"))
    generated = load_entry("candidate_solution", Path("/candidate/solution.py"))

    named_cases = [
        ("prompt-1", [4, 2, 3]),
        ("prompt-2", [1, 2, 3]),
        ("prompt-empty", []),
        ("prompt-4", [5, 0, 3, 0, 4, 2]),
        ("singleton-even-zero", [0]),
        ("singleton-even-positive", [8]),
        ("singleton-odd", [7]),
        ("no-even", [1, 3, 5, 9]),
        ("first-even-best", [2, 8, 5]),
        ("later-even-best", [8, 3, 2]),
        ("equal-even-tie", [4, 1, 4, 2, 2]),
        ("zero-late-tie", [9, 0, 2, 0]),
        ("large-values", [999_999_999, 1_000_000_000, 2]),
        ("max-length-all-odd", [1] * 10_000),
        ("max-length-late-zero", [3] * 9_999 + [0]),
        ("max-length-early-zero-tie", [0] + [2] * 9_998 + [0]),
    ]

    checked = 0
    mismatches: list[tuple[str, list[int], list[int], list[int], list[int]]] = []

    def check(label: str, values: list[int]) -> None:
        nonlocal checked
        expected = independent_oracle(values)
        canonical_result = canonical(list(values))
        generated_result = generated(list(values))
        checked += 1
        if canonical_result != expected or generated_result != expected:
            mismatches.append(
                (label, values, expected, canonical_result, generated_result)
            )

    for label, values in named_cases:
        check(label, values)

    # Exhaust every list of length 0..5 over values 0..6. This covers both
    # parity branches, first/later minima, and all equality/tie placements.
    exhaustive_count = 0
    for length in range(6):
        for values in product(range(7), repeat=length):
            check(f"exhaustive-{length}", list(values))
            exhaustive_count += 1

    # Deterministic broader sampling across the documented non-negative domain.
    rng = random.Random(680068)
    random_count = 2_000
    for case_index in range(random_count):
        length = rng.randrange(0, 201)
        values = [rng.randrange(0, 1_000_001) for _ in range(length)]
        check(f"random-{case_index}", values)

    print(f"named_cases={len(named_cases)}")
    print(f"exhaustive_domain=lengths_0_through_5_values_0_through_6")
    print(f"exhaustive_cases={exhaustive_count}")
    print("random_seed=680068")
    print(f"random_cases={random_count}")
    print("random_lengths=0_through_200")
    print("random_values=0_through_1000000")
    print(f"total_cases={checked}")
    print(f"mismatch_count={len(mismatches)}")
    for mismatch in mismatches[:10]:
        print(f"MISMATCH={mismatch!r}")
    return 0 if not mismatches else 1


if __name__ == "__main__":
    sys.exit(main())
