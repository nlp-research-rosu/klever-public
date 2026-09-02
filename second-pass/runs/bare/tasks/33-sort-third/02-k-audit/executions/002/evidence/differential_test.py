#!/usr/bin/env python3
"""Independent differential test for HumanEval/33 sort_third."""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_third


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("canonical", type=Path)
    parser.add_argument("candidate", type=Path)
    args = parser.parse_args()

    canonical = load_entry(args.canonical, "trusted_canonical")
    candidate = load_entry(args.candidate, "candidate_solution")

    named_cases = [
        ("empty", []),
        ("length-1", [7]),
        ("length-2", [7, -1]),
        ("example-1", [1, 2, 3]),
        ("first-second-third-index", [3, 20, 10, 1]),
        ("length-mod-3-2", [9, 8, 7, 6, 5]),
        ("two-selected-elements", [5, 6, 3, 4, 8, 9]),
        ("example-2", [5, 6, 3, 4, 8, 9, 2]),
        ("already-sorted-selected", [-3, 9, 8, 0, 7, 6, 4]),
        ("reverse-selected", [9, 0, -1, 8, 7, 6, 2, 5, 4, 1]),
        ("duplicates-and-equality", [2, 8, 7, 2, 6, 5, -1, 4, 3, 2]),
        ("large-magnitudes", [10**18, 2, 3, -(10**18), 5, 6, 0]),
    ]

    cases: list[tuple[str, list[int]]] = list(named_cases)
    alphabet = (-2, -1, 0, 1, 2)
    for length in range(8):
        cases.extend(
            (f"exhaustive-{length}-{index}", list(values))
            for index, values in enumerate(itertools.product(alphabet, repeat=length))
        )

    rng = random.Random(330033)
    for index in range(500):
        length = rng.randrange(0, 51)
        values = [rng.randrange(-10**6, 10**6 + 1) for _ in range(length)]
        cases.append((f"random-{index}", values))

    mismatches = []
    mutation_failures = []
    for name, values in cases:
        before = list(values)
        expected = canonical(values)
        actual = candidate(values)
        if expected != actual:
            mismatches.append((name, before, expected, actual))
        if values != before:
            mutation_failures.append((name, before, values))

    print(f"named_cases={len(named_cases)}")
    print(f"exhaustive_cases={sum(len(alphabet) ** n for n in range(8))}")
    print("random_cases=500 seed=330033 max_length=50")
    print(f"total_cases={len(cases)}")
    print(f"mismatches={len(mismatches)}")
    print(f"input_mutations={len(mutation_failures)}")
    if mismatches:
        print(f"first_mismatch={mismatches[0]!r}")
    if mutation_failures:
        print(f"first_input_mutation={mutation_failures[0]!r}")
    if mismatches or mutation_failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
