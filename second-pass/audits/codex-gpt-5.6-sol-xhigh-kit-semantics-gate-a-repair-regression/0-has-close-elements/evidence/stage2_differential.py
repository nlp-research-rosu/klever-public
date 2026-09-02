#!/usr/bin/env python3
"""Independent differential audit for HumanEval 0."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import math
import random
import sys
from pathlib import Path


CANONICAL_PATH = Path("/reference/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/reconstruction/solution.py")
ENTRY_POINT = "has_close_elements"
SEED = 0xC105E
RANDOM_CASES = 2500


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, ENTRY_POINT)


def outcome(fn, numbers: list[float], threshold: float):
    try:
        result = fn(list(numbers), threshold)
        return ("return", type(result).__name__, result)
    except Exception as exc:  # Differentially compare unexpected boundary behavior.
        return ("raise", type(exc).__name__, str(exc))


def describe_float(value: float) -> str:
    if math.isnan(value):
        return "nan"
    if math.isinf(value):
        return "inf" if value > 0 else "-inf"
    return value.hex()


def iter_cases():
    min_subnormal = math.nextafter(0.0, 1.0)
    max_finite = sys.float_info.max
    curated = [
        ("prompt-false", [1.0, 2.0, 3.0], 0.5),
        ("prompt-true", [1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3),
        ("empty", [], 1.0),
        ("singleton", [1.0], 1.0),
        ("outer-enters-inner-does-not", [1.0, 2.0], 0.5),
        ("strict-equality-is-false", [1.0, 1.5], 0.5),
        ("just-over-boundary-is-true", [1.0, 1.5], math.nextafter(0.5, math.inf)),
        ("first-pair-true", [0.0, min_subnormal, 10.0], 2 * min_subnormal),
        ("later-pair-true", [0.0, 10.0, 10.25], 0.5),
        ("last-outer-row-true", [0.0, 10.0, 20.0, 20.25], 0.5),
        ("duplicate-zero-threshold", [0.0, -0.0], 0.0),
        ("duplicate-positive-threshold", [0.0, -0.0], min_subnormal),
        ("negative-threshold", [1.0, 1.0], -1.0),
        ("nan-threshold", [1.0, 1.0], math.nan),
        ("nan-element", [math.nan, 0.0, min_subnormal], 1.0),
        ("finite-under-infinite-threshold", [-max_finite, max_finite], math.inf),
        ("same-positive-infinity", [math.inf, math.inf], math.inf),
        ("opposite-infinities", [-math.inf, math.inf], math.inf),
        ("overflowing-subtraction", [-max_finite, max_finite], max_finite),
    ]
    for label, numbers, threshold in curated:
        yield label, numbers, threshold

    grid_values = [
        -math.inf,
        -1.0,
        -0.0,
        0.0,
        min_subnormal,
        0.5,
        1.0,
        math.inf,
        math.nan,
    ]
    thresholds = [
        -math.inf,
        -1.0,
        -0.0,
        0.0,
        min_subnormal,
        0.5,
        1.0,
        math.nextafter(1.0, math.inf),
        math.inf,
        math.nan,
    ]
    for length in range(5):
        for values in itertools.product(grid_values, repeat=length):
            for threshold in thresholds:
                yield f"grid-len-{length}", list(values), threshold

    rng = random.Random(SEED)
    specials = grid_values + [-sys.float_info.max, sys.float_info.max]
    for index in range(RANDOM_CASES):
        length = rng.randrange(0, 9)
        numbers = [
            rng.choice(specials)
            if rng.random() < 0.25
            else rng.uniform(-1.0e6, 1.0e6)
            for _ in range(length)
        ]
        threshold = (
            rng.choice(thresholds)
            if rng.random() < 0.35
            else rng.uniform(-10.0, 1.0e6)
        )
        yield f"random-{index}", numbers, threshold


def main() -> int:
    canonical = load_entry("trusted_canonical", CANONICAL_PATH)
    generated = load_entry("audited_generated", GENERATED_PATH)
    tested = 0
    mismatches = []
    label_counts: dict[str, int] = {}

    for label, numbers, threshold in iter_cases():
        expected = outcome(canonical, numbers, threshold)
        actual = outcome(generated, numbers, threshold)
        tested += 1
        family = label.split("-", 1)[0]
        label_counts[family] = label_counts.get(family, 0) + 1
        if expected != actual and len(mismatches) < 20:
            mismatches.append(
                {
                    "label": label,
                    "numbers": [describe_float(v) for v in numbers],
                    "threshold": describe_float(threshold),
                    "canonical": repr(expected),
                    "generated": repr(actual),
                }
            )

    print(f"canonical={CANONICAL_PATH}")
    print(f"generated={GENERATED_PATH}")
    print(f"generated_sha256={hashlib.sha256(GENERATED_PATH.read_bytes()).hexdigest()}")
    print(
        "scope=19 curated cases; Cartesian lengths 0..4 over 9 boundary values "
        "x 10 thresholds; 2500 deterministic random cases of lengths 0..8"
    )
    print(f"random_seed={SEED}")
    print(f"tested={tested}")
    print(f"mismatches={len(mismatches)}")
    for mismatch in mismatches:
        print(f"MISMATCH {mismatch}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
