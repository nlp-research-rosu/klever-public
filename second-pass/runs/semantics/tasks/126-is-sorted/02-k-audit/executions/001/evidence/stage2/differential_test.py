#!/usr/bin/env python3
"""Independent differential test for HumanEval/126 is_sorted."""

from __future__ import annotations

import importlib.util
import itertools
import random
import sys
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_sorted


def branch_features(values: list[int]) -> set[str]:
    features: set[str] = {"empty"} if not values else set()
    previous = 0
    repeats = 0
    for number in values:
        features.add("number_lt_previous:true" if number < previous
                     else "number_lt_previous:false")
        features.add("number_eq_previous:true" if number == previous
                     else "number_eq_previous:false")
        if number == previous:
            repeats += 1
        else:
            repeats = 1
        if repeats < 2:
            features.add("repeats:below_2")
        elif repeats == 2:
            features.add("repeats:at_2")
        elif repeats == 3:
            features.add("repeats:at_3")
        features.add("repeats_gt_2:true" if repeats > 2
                     else "repeats_gt_2:false")
        previous = number
    return features


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} CANONICAL.py SOLUTION.py", file=sys.stderr)
        return 64

    canonical = load_function(Path(sys.argv[1]), "trusted_canonical")
    generated = load_function(Path(sys.argv[2]), "submitted_generated")

    documented = [
        ([5], True),
        ([1, 2, 3, 4, 5], True),
        ([1, 3, 2, 4, 5], False),
        ([1, 2, 3, 4, 5, 6], True),
        ([1, 2, 3, 4, 5, 6, 7], True),
        ([1, 3, 2, 4, 5, 6, 7], False),
        ([1, 2, 2, 3, 3, 4], True),
        ([1, 2, 2, 2, 3, 4], False),
    ]
    boundaries = [
        [],
        [0],
        [1],
        [0, 0],
        [0, 0, 0],
        [1, 1],
        [1, 1, 1],
        [0, 1],
        [1, 0],
        [0, 1, 1, 2, 2],
        [0, 1, 1, 1, 2],
        [0, 2, 1],
        [2, 1, 2],
        [2, 2, 1, 1],
    ]

    mismatches: list[tuple[list[int], bool, bool]] = []
    observed_features: set[str] = set()
    total = 0

    def check(values: list[int]) -> None:
        nonlocal total
        expected = canonical(list(values))
        actual = generated(list(values))
        total += 1
        observed_features.update(branch_features(values))
        if expected != actual:
            mismatches.append((values, expected, actual))

    for values, documented_expected in documented:
        canonical_value = canonical(list(values))
        generated_value = generated(list(values))
        if canonical_value != documented_expected or generated_value != documented_expected:
            mismatches.append((values, canonical_value, generated_value))
        check(values)
    for values in boundaries:
        check(values)

    # Exhaust all nonnegative lists through length 7 over a small alphabet.
    exhaustive_count = 0
    for length in range(8):
        for values in itertools.product(range(5), repeat=length):
            check(list(values))
            exhaustive_count += 1

    # Deterministic broader coverage over longer lists and larger values.
    rng = random.Random(126)
    random_count = 10_000
    for _ in range(random_count):
        length = rng.randrange(0, 31)
        check([rng.randrange(0, 21) for _ in range(length)])

    required_features = {
        "empty",
        "number_lt_previous:true",
        "number_lt_previous:false",
        "number_eq_previous:true",
        "number_eq_previous:false",
        "repeats:below_2",
        "repeats:at_2",
        "repeats:at_3",
        "repeats_gt_2:true",
        "repeats_gt_2:false",
    }
    missing_features = sorted(required_features - observed_features)

    print(f"documented_cases={len(documented)}")
    print(f"explicit_boundary_cases={len(boundaries)}")
    print(f"exhaustive_domain=values[0..4],length[0..7]")
    print(f"exhaustive_count={exhaustive_count}")
    print("random_domain=seed126,values[0..20],length[0..30]")
    print(f"random_count={random_count}")
    print(f"total_comparisons={total}")
    print(f"observed_branch_features={sorted(observed_features)}")
    print(f"missing_branch_features={missing_features}")
    print(f"in_domain_mismatches={len(mismatches)}")
    for mismatch in mismatches[:20]:
        print(f"MISMATCH {mismatch}")

    # Negative integers are outside the promised domain. This witness records
    # why the nonnegative precondition is material.
    negative_witness = [-1]
    print(
        "out_of_domain_negative_witness="
        f"{negative_witness},canonical={canonical(negative_witness)},"
        f"generated={generated(negative_witness)}"
    )

    return 0 if not mismatches and not missing_features else 1


if __name__ == "__main__":
    raise SystemExit(main())
