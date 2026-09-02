#!/usr/bin/env python3
"""Independent candidate-versus-canonical differential for HumanEval 47."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
import sys
from collections import Counter
from pathlib import Path


CANONICAL_PATH = Path("/tmp/audit-work/47-median/trusted/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/47-median/candidate-src/solution.py")
SEED = 470047
EXHAUSTIVE_VALUES = tuple(range(-2, 3))
EXHAUSTIVE_LENGTHS = tuple(range(0, 7))
RANDOM_CASES = 500
RANDOM_LENGTH_RANGE = (0, 20)
RANDOM_VALUE_RANGE = (-10_000, 10_000)


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.median


def outcome(fn, values: list[int]):
    try:
        value = fn(values.copy())
    except Exception as exc:  # Exceptions are observable outcomes.
        return ("exception", type(exc).__name__, str(exc))
    return ("return", type(value).__name__, repr(value))


def main() -> int:
    canonical = load_entry(CANONICAL_PATH, "trusted_canonical_47")
    candidate = load_entry(CANDIDATE_PATH, "candidate_solution_47")

    named = [
        ("prompt-odd", [3, 1, 2, 4, 5]),
        ("prompt-even", [-10, 4, 6, 1000, 10, 20]),
        ("empty", []),
        ("length-1", [7]),
        ("length-2", [1, 2]),
        ("length-3", [3, 1, 2]),
        ("length-4", [4, 1, 3, 2]),
        ("even-duplicates", [1, 1, 1, 9]),
        ("even-negatives", [-9, -7, -3, -1]),
        ("rounding-large", [0, 1, 2**54, 2**54 + 1]),
        ("overflow-even", [10**400, 10**400, 10**400, 10**400]),
    ]

    rng = random.Random(SEED)
    generated: list[tuple[str, list[int]]] = []
    for length in EXHAUSTIVE_LENGTHS:
        for values in itertools.product(EXHAUSTIVE_VALUES, repeat=length):
            generated.append((f"exhaustive-n{length}", list(values)))
    for _ in range(RANDOM_CASES):
        length = rng.randint(*RANDOM_LENGTH_RANGE)
        values = [rng.randint(*RANDOM_VALUE_RANGE) for _ in range(length)]
        generated.append((f"random-seed-{SEED}-n{length}", values))

    cases = named + generated
    mismatch_samples = []
    mismatch_kinds: Counter[str] = Counter()
    totals: Counter[str] = Counter()

    print(
        "SCOPE "
        + json.dumps(
            {
                "canonical": str(CANONICAL_PATH),
                "candidate": str(CANDIDATE_PATH),
                "named_inputs": named,
                "exhaustive_values": EXHAUSTIVE_VALUES,
                "exhaustive_lengths": EXHAUSTIVE_LENGTHS,
                "random_seed": SEED,
                "random_cases": RANDOM_CASES,
                "random_length_range": RANDOM_LENGTH_RANGE,
                "random_value_range": RANDOM_VALUE_RANGE,
            },
            sort_keys=True,
        )
    )

    for label, values in cases:
        expected = outcome(canonical, values)
        actual = outcome(candidate, values)
        totals[label.split("-n", 1)[0]] += 1
        if expected != actual:
            mismatch_kinds[label.split("-n", 1)[0]] += 1
            if len(mismatch_samples) < 30:
                mismatch_samples.append(
                    {
                        "label": label,
                        "input": values,
                        "canonical": expected,
                        "candidate": actual,
                    }
                )

    print("TOTAL_CASES", len(cases))
    print("TOTALS_BY_SOURCE", json.dumps(totals, sort_keys=True))
    print("MISMATCHES", sum(mismatch_kinds.values()))
    print("MISMATCHES_BY_SOURCE", json.dumps(mismatch_kinds, sort_keys=True))
    print("MISMATCH_SAMPLES", json.dumps(mismatch_samples, sort_keys=True))

    for label, values in named:
        print(
            "NAMED_RESULT "
            + json.dumps(
                {
                    "label": label,
                    "input": values,
                    "canonical": outcome(canonical, values),
                    "candidate": outcome(candidate, values),
                },
                sort_keys=True,
            )
        )

    return 1 if mismatch_kinds else 0


if __name__ == "__main__":
    sys.exit(main())
