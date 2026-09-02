#!/usr/bin/env python3
"""Independent CPython differential for HumanEval 104.

The oracle is loaded only from the trusted canonical.py.  The implementation
under audit is loaded independently from the submitted solution.py.
"""

from __future__ import annotations

import importlib.util
import json
import random
import sys
from pathlib import Path
from types import ModuleType


def load(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def directed_inputs() -> list[tuple[str, list[int], list[int] | None]]:
    return [
        ("documented-example-1", [15, 33, 1422, 1], [1, 15, 33]),
        ("documented-example-2", [152, 323, 1422, 10], []),
        ("empty", [], []),
        ("minimum-positive", [1], [1]),
        ("single-even-digit-2", [2], []),
        ("single-even-digit-4", [4], []),
        ("single-even-digit-6", [6], []),
        ("single-even-digit-8", [8], []),
        ("zero-character-branch", [101], []),
        ("two-character-branch", [121], []),
        ("four-character-branch", [141], []),
        ("six-character-branch", [161], []),
        ("eight-character-branch", [181], []),
        ("all-odd-digit-boundaries", [9, 7, 5, 3, 1, 11, 13579], [1, 3, 5, 7, 9, 11, 13579]),
        ("duplicates-and-order", [33, 1, 33, 20, 15, 3, 15], [1, 3, 15, 15, 33, 33]),
        ("forbidden-at-first-middle-last", [211, 121, 112, 411, 141, 114, 611, 161, 116, 811, 181, 118], []),
        ("large-positive-integers", [999999999999999999, 1357908642, 777777777777777777, 2468], [777777777777777777, 999999999999999999]),
    ]


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} TRUSTED_CANONICAL.py CANDIDATE_SOLUTION.py", file=sys.stderr)
        return 64
    canonical = load(Path(sys.argv[1]), "trusted_canonical_104")
    candidate = load(Path(sys.argv[2]), "candidate_solution_104")
    cases: list[tuple[str, list[int], list[int] | None]] = directed_inputs()

    # Every positive integer through 10,000 is tested as a singleton.  This
    # systematically crosses every decimal digit and length transition in that
    # range and makes sorting irrelevant for the predicate comparison.
    cases.extend((f"singleton-{value}", [value], None) for value in range(1, 10001))

    # Sliding lists test filtering stability, duplicates, and sorting over the
    # same boundary range.
    for start in range(1, 10001, 37):
        values = list(range(start, min(start + 23, 10001)))
        cases.append((f"sliding-{start}", list(reversed(values)) + values[:3], None))

    seed = 104104
    rng = random.Random(seed)
    lengths = [0, 1, 2, 3, 7, 20, 50]
    for index in range(1000):
        length = lengths[index % len(lengths)]
        values = [rng.randint(1, 10**18) for _ in range(length)]
        if index % 11 == 0 and values:
            values[-1] = values[0]
        cases.append((f"random-{index}", values, None))

    mismatches: list[dict[str, object]] = []
    documented_failures: list[dict[str, object]] = []
    for name, values, documented_expected in cases:
        oracle_result = canonical.unique_digits(list(values))
        candidate_result = candidate.unique_digits(list(values))
        if documented_expected is not None and oracle_result != documented_expected:
            documented_failures.append(
                {"name": name, "input": values, "expected": documented_expected, "canonical": oracle_result}
            )
        if oracle_result != candidate_result:
            mismatches.append(
                {"name": name, "input": values, "canonical": oracle_result, "candidate": candidate_result}
            )

    print("ORACLE: trusted /reference/canonical.py unique_digits")
    print("CANDIDATE: submitted solution.py unique_digits")
    print("INTENDED_DOMAIN: finite lists of positive Python integers")
    print("DIRECTED_INPUTS=" + json.dumps([(name, values) for name, values, _ in directed_inputs()]))
    print("SYSTEMATIC_SCOPE: singleton integers 1..10000 inclusive; reversed sliding windows start=1..10000 step=37 width<=23 with three duplicates")
    print(f"RANDOM_SCOPE: seed={seed}; cases=1000; lengths={lengths}; values=1..10**18; deterministic duplicate injection every 11th nonempty case")
    print(f"TOTAL_CASES: {len(cases)}")
    print(f"DOCUMENTED_EXPECTATION_FAILURES: {len(documented_failures)}")
    print(f"MISMATCHES: {len(mismatches)}")
    for failure in documented_failures[:20]:
        print("DOCUMENTED_FAILURE=" + json.dumps(failure, sort_keys=True))
    for mismatch in mismatches[:20]:
        print("MISMATCH=" + json.dumps(mismatch, sort_keys=True))
    return 1 if documented_failures or mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
