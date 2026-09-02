#!/usr/bin/env python3
"""Independent differential test for problem 127-intersection.

The trusted canonical implementation and the submitted implementation are
loaded from explicit paths.  The third comparison is a small independent
contract oracle which uses exhaustive divisor search, not the submitted
square-root loop.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import random
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def contract_oracle(interval1: tuple[int, int], interval2: tuple[int, int]) -> str:
    left = max(interval1[0], interval2[0])
    right = min(interval1[1], interval2[1])
    length = right - left
    if length < 2:
        return "NO"
    for divisor in range(2, length):
        if length % divisor == 0:
            return "NO"
    return "YES"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--solution", type=Path, required=True)
    parser.add_argument("--inputs-out", type=Path, required=True)
    args = parser.parse_args()

    canonical = load_module("trusted_canonical", args.canonical)
    submitted = load_module("submitted_solution", args.solution)

    curated = [
        ("prompt-example-touch", (1, 2), (2, 3)),
        ("prompt-example-length-one", (-1, 1), (0, 4)),
        ("prompt-example-prime-two", (-3, -1), (-5, 5)),
        ("canonical-doc-example-prime-five", (-3, 9), (-1, 4)),
        ("disjoint-gap", (0, 1), (2, 3)),
        ("equal-singletons", (7, 7), (7, 7)),
        ("same-length-two", (0, 2), (0, 2)),
        ("same-length-three", (0, 3), (0, 3)),
        ("same-length-four", (0, 4), (0, 4)),
        ("same-length-five", (0, 5), (0, 5)),
        ("square-nine", (0, 9), (0, 9)),
        ("composite-fifteen", (0, 15), (0, 15)),
        ("c-gt-a-e-lt-b", (0, 10), (2, 8)),
        ("c-gt-a-e-eq-b", (0, 8), (2, 8)),
        ("c-gt-a-e-gt-b", (0, 8), (2, 10)),
        ("c-eq-a-e-lt-b", (0, 10), (0, 8)),
        ("c-lt-a-e-lt-b", (2, 10), (0, 8)),
        ("c-eq-a-e-eq-b", (0, 8), (0, 8)),
        ("c-lt-a-e-gt-b", (2, 8), (0, 10)),
        ("negative-coordinates", (-20, -7), (-17, -10)),
        ("large-prime-length", (0, 997), (0, 997)),
        ("large-composite-length", (-500, 500), (-500, 500)),
    ]

    cases: list[tuple[str, tuple[int, int], tuple[int, int]]] = list(curated)
    small_intervals = [
        (start, end)
        for start in range(-8, 9)
        for end in range(start, 9)
    ]
    cases.extend(
        ("exhaustive[-8,8]", first, second)
        for first in small_intervals
        for second in small_intervals
    )

    rng = random.Random(127_20260722)
    for _ in range(2000):
        a, b = sorted((rng.randint(-1000, 1000), rng.randint(-1000, 1000)))
        c, e = sorted((rng.randint(-1000, 1000), rng.randint(-1000, 1000)))
        cases.append(("seeded-random", (a, b), (c, e)))

    serializable_inputs = [
        {"label": label, "interval1": first, "interval2": second}
        for label, first, second in cases
    ]
    args.inputs_out.write_text(json.dumps(serializable_inputs, indent=2) + "\n")

    mismatches = []
    label_counts: dict[str, int] = {}
    for label, first, second in cases:
        label_counts[label] = label_counts.get(label, 0) + 1
        expected = contract_oracle(first, second)
        canonical_result = canonical.intersection(first, second)
        submitted_result = submitted.intersection(first, second)
        if not (canonical_result == submitted_result == expected):
            mismatches.append(
                {
                    "label": label,
                    "interval1": first,
                    "interval2": second,
                    "canonical": canonical_result,
                    "submitted": submitted_result,
                    "oracle": expected,
                }
            )

    print(f"curated_cases={len(curated)}")
    print(f"exhaustive_intervals={len(small_intervals)}")
    print(f"exhaustive_pairs={len(small_intervals) ** 2}")
    print("seeded_random_cases=2000 seed=12720260722 endpoint_range=[-1000,1000]")
    print(f"total_cases={len(cases)}")
    print(f"mismatches={len(mismatches)}")
    print("curated_results:")
    for label, first, second in curated:
        print(
            f"  {label}: {first}, {second} -> "
            f"canonical={canonical.intersection(first, second)} "
            f"submitted={submitted.intersection(first, second)} "
            f"oracle={contract_oracle(first, second)}"
        )
    if mismatches:
        print(json.dumps(mismatches[:20], indent=2))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
