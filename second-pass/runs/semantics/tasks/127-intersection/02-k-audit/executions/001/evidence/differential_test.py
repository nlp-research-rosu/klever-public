#!/usr/bin/env python3
"""Independent differential and mathematical-oracle tests for 127-intersection."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
from pathlib import Path


CANONICAL_PATH = Path("/reference/canonical.py")
CANDIDATE_PATH = Path("/candidate/solution.py")
INPUTS_PATH = Path("/audit-output/evidence/05-differential-inputs.json")


def load_function(module_name: str, source_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, source_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {source_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.intersection


def independent_oracle(interval1: tuple[int, int], interval2: tuple[int, int]) -> str:
    overlap_length = min(interval1[1], interval2[1]) - max(
        interval1[0], interval2[0]
    )
    if overlap_length < 2:
        return "NO"
    for divisor in range(2, overlap_length):
        if overlap_length % divisor == 0:
            return "NO"
    return "YES"


def main() -> None:
    canonical = load_function("trusted_canonical", CANONICAL_PATH)
    candidate = load_function("submitted_solution", CANDIDATE_PATH)

    named_cases = [
        ("prompt-touch", (1, 2), (2, 3)),
        ("prompt-length-one", (-1, 1), (0, 4)),
        ("prompt-length-two", (-3, -1), (-5, 5)),
        ("both-degenerate-same", (0, 0), (0, 0)),
        ("both-degenerate-disjoint", (-2, -2), (3, 3)),
        ("strictly-disjoint", (0, 3), (10, 12)),
        ("reverse-disjoint", (10, 12), (0, 3)),
        ("overlap-length-zero", (0, 1), (1, 5)),
        ("overlap-length-one", (0, 2), (1, 5)),
        ("overlap-length-two-loop-empty", (0, 2), (-4, 8)),
        ("overlap-length-three-mod-nonzero", (0, 3), (-4, 8)),
        ("overlap-length-four-first-divisor", (0, 4), (-4, 8)),
        ("overlap-length-nine-later-divisor", (0, 9), (-4, 12)),
        ("overlap-length-five-prime", (-9, -4), (-10, 0)),
        ("overlap-length-97-prime", (-100, -3), (-1000, 1000)),
        ("overlap-length-121-composite", (-121, 0), (-500, 500)),
        ("shared-negative-endpoint", (-9, -5), (-7, -5)),
        ("contained-first", (-2, 11), (0, 7)),
        ("contained-second", (0, 7), (-2, 11)),
        ("equal-intervals", (-6, 6), (-6, 6)),
    ]

    all_cases: list[tuple[str, tuple[int, int], tuple[int, int]]] = list(named_cases)

    small_intervals = [
        (start, end)
        for start in range(-5, 6)
        for end in range(start, 6)
    ]
    for index, (interval1, interval2) in enumerate(
        itertools.product(small_intervals, repeat=2)
    ):
        all_cases.append((f"exhaustive-small-{index}", interval1, interval2))

    rng = random.Random(127)
    for index in range(2000):
        endpoints1 = sorted((rng.randint(-500, 500), rng.randint(-500, 500)))
        endpoints2 = sorted((rng.randint(-500, 500), rng.randint(-500, 500)))
        all_cases.append(
            (
                f"seeded-random-{index}",
                (endpoints1[0], endpoints1[1]),
                (endpoints2[0], endpoints2[1]),
            )
        )

    serialized_inputs = [
        {"name": name, "interval1": interval1, "interval2": interval2}
        for name, interval1, interval2 in all_cases
    ]
    INPUTS_PATH.write_text(json.dumps(serialized_inputs, indent=2) + "\n")

    mismatches = []
    named_results = []
    for name, interval1, interval2 in all_cases:
        expected = independent_oracle(interval1, interval2)
        canonical_result = canonical(interval1, interval2)
        candidate_result = candidate(interval1, interval2)
        if name.startswith(("prompt-", "both-", "strictly-", "reverse-", "overlap-",
                            "shared-", "contained-", "equal-")):
            named_results.append(
                (name, interval1, interval2, expected, canonical_result, candidate_result)
            )
        if canonical_result != expected or candidate_result != expected:
            mismatches.append(
                {
                    "name": name,
                    "interval1": interval1,
                    "interval2": interval2,
                    "oracle": expected,
                    "canonical": canonical_result,
                    "candidate": candidate_result,
                }
            )

    print(f"canonical={CANONICAL_PATH}")
    print(f"candidate={CANDIDATE_PATH}")
    print("domain=integer pairs (start,end) with start <= end")
    print(f"named_cases={len(named_cases)}")
    print(
        f"exhaustive_small_cases={len(small_intervals) ** 2} "
        "for all endpoints in [-5,5]"
    )
    print("seeded_random_cases=2000 seed=127 endpoints in [-500,500]")
    for result in named_results:
        print("NAMED", repr(result))
    print(f"total_cases={len(all_cases)}")
    print(f"mismatches={len(mismatches)}")
    if mismatches:
        print(json.dumps(mismatches[:20], indent=2))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
