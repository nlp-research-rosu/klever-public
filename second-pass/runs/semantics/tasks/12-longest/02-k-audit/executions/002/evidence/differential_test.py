#!/usr/bin/env python3
"""Independent differential test for HumanEval/12 longest."""

from __future__ import annotations

from itertools import product
import importlib.util
from pathlib import Path
import random
import sys


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.longest


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: differential_test.py CANONICAL.py SOLUTION.py", file=sys.stderr)
        return 2
    canonical = load_entry(Path(sys.argv[1]), "trusted_canonical")
    generated = load_entry(Path(sys.argv[2]), "generated_solution")

    documented_and_boundaries = [
        [],
        ["a", "b", "c"],
        ["a", "bb", "ccc"],
        [""],
        ["", ""],
        ["a"],
        ["long", "x"],
        ["x", "long"],
        ["first", "later"],
        ["a", "bbb", "cc", "ddd"],
        ["é", "e\u0301"],
        ["🙂", "ab"],
        ["\x00", ""],
    ]

    alphabet = ["", "a", "b", "aa", "ab", "é", "🙂"]
    cases: list[list[str]] = list(documented_and_boundaries)
    for list_length in range(5):
        cases.extend([list(items) for items in product(alphabet, repeat=list_length)])

    rng = random.Random(1200260726)
    unicode_pool = ["a", "é", "🙂", "\x00", "\n", "e\u0301", "中"]
    for _ in range(1000):
        list_length = rng.randrange(0, 21)
        cases.append(
            [
                "".join(rng.choice(unicode_pool) for _ in range(rng.randrange(0, 31)))
                for _ in range(list_length)
            ]
        )

    mismatches: list[tuple[list[str], object, object]] = []
    for strings in cases:
        expected = canonical(list(strings))
        actual = generated(list(strings))
        if actual != expected or (actual is None) != (expected is None):
            mismatches.append((strings, expected, actual))
            if len(mismatches) >= 20:
                break

    print(f"documented_and_boundary_cases={len(documented_and_boundaries)}")
    print("exhaustive_lists=all lengths 0..4 over 7 fixed strings")
    print("deterministic_generated_lists=1000 lengths 0..20")
    print(f"total_cases={len(cases)}")
    print(f"mismatches={len(mismatches)}")
    for strings, expected, actual in mismatches:
        print(f"MISMATCH input={strings!r} canonical={expected!r} generated={actual!r}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
