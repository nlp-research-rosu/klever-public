#!/usr/bin/env python3
"""Independent differential test for HumanEval 34's unique entry point."""

from __future__ import annotations

import copy
import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def outcome(function, value):
    try:
        return ("return", function(copy.deepcopy(value)))
    except Exception as error:  # Compare observable exception classes too.
        return ("raise", type(error).__name__, str(error))


def main() -> int:
    if len(sys.argv) != 4:
        print(
            "usage: differential_unique.py CANONICAL.py SOLUTION.py INPUTS.json",
            file=sys.stderr,
        )
        return 64

    canonical = load_module("trusted_canonical", Path(sys.argv[1]))
    generated = load_module("generated_solution", Path(sys.argv[2]))

    curated = [
        ("documented-example", [5, 3, 5, 2, 3, 3, 9, 0, 123]),
        ("empty-loop-boundary", []),
        ("singleton-new-branch", [1]),
        ("duplicate-branch", [1, 1]),
        ("new-then-new", [1, 2]),
        ("sorting-reversal", [2, 1]),
        ("negative-and-duplicates", [-1, 3, -1, 2, 3]),
        ("already-sorted", [-3, -2, -1, 0, 1, 2, 3]),
        ("reverse-sorted", [3, 2, 1, 0, -1, -2, -3]),
        ("alternating-branches", [0, 1, 0, 2, 1, 3, 2, 3]),
        ("integer-boundaries", [-(2**63), 2**63 - 1, -(2**63), 0]),
        ("unbounded-integers", [10**100, -(10**100), 10**100, 7]),
        ("bool-int-equality", [True, 1, False, 0, 2]),
        ("homogeneous-strings", ["z", "a", "z", "", "a"]),
        ("homogeneous-tuples", [(2, 0), (1, 9), (2, 0), (1, 3)]),
    ]

    exhaustive = [
        (f"exhaustive-small-int-len-{length}", list(values))
        for length in range(0, 6)
        for values in itertools.product([-2, -1, 0, 1, 2], repeat=length)
    ]

    random_source = random.Random(340034)
    generated_cases = [
        (
            "seeded-random-int",
            [
                random_source.randint(-10**6, 10**6)
                for _ in range(random_source.randint(0, 40))
            ],
        )
        for _ in range(250)
    ]

    cases = curated + exhaustive + generated_cases
    corpus = [
        {"ordinal": ordinal, "category": category, "input_repr": repr(value)}
        for ordinal, (category, value) in enumerate(cases)
    ]
    Path(sys.argv[3]).write_text(
        json.dumps(corpus, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    mismatches = []
    for ordinal, (category, value) in enumerate(cases):
        expected = outcome(canonical.unique, value)
        actual = outcome(generated.unique, value)
        if expected != actual:
            mismatches.append(
                {
                    "ordinal": ordinal,
                    "category": category,
                    "input": repr(value),
                    "canonical": repr(expected),
                    "generated": repr(actual),
                }
            )

    print(f"oracle=/reference/canonical.py:unique")
    print(f"subject=/candidate/solution.py:unique (scratch copy)")
    print(f"curated_cases={len(curated)}")
    print(
        "exhaustive_scope=all integer lists of lengths 0..5 "
        "over alphabet [-2,-1,0,1,2]"
    )
    print(f"exhaustive_cases={len(exhaustive)}")
    print("random_scope=250 seeded integer lists; seed=340034; lengths=0..40")
    print(f"generated_cases={len(generated_cases)}")
    print(f"total_cases={len(cases)}")
    print(f"mismatch_count={len(mismatches)}")
    for ground in ([], [1], [2, 1, 2], [5, 3, 5, 2, 3, 3, 9, 0, 123]):
        print(
            f"ground={ground!r} "
            f"canonical={outcome(canonical.unique, ground)!r} "
            f"generated={outcome(generated.unique, ground)!r}"
        )
    if mismatches:
        print(json.dumps(mismatches[:10], indent=2, sort_keys=True))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
