#!/usr/bin/env python3
"""Independent candidate/canonical/oracle differential for HumanEval/0."""

from __future__ import annotations

import gzip
import hashlib
import importlib.util
import itertools
import json
import math
import random
import sys
from pathlib import Path
from typing import Callable


CANONICAL_PATH = Path("/reference/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/reconstruction/solution.py")
INPUT_ARTIFACT = Path("/audit-output/evidence/differential-inputs.jsonl.gz")
SEED = 20260723


def load_entry(path: Path, module_name: str) -> Callable[[list[float], float], bool]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.has_close_elements


def independent_oracle(numbers: list[float], threshold: float) -> bool:
    return any(
        abs(numbers[left] - numbers[right]) < threshold
        for left in range(len(numbers))
        for right in range(left + 1, len(numbers))
    )


def encoded_float(value: float) -> str:
    if math.isnan(value):
        return "NaN"
    if math.isinf(value):
        return "Infinity" if value > 0 else "-Infinity"
    return value.hex()


def encoded_case(
    label: str, numbers: list[float], threshold: float
) -> dict[str, object]:
    return {
        "label": label,
        "numbers": [encoded_float(value) for value in numbers],
        "threshold": encoded_float(threshold),
    }


def cases() -> list[tuple[str, list[float], float, bool | None]]:
    named: list[tuple[str, list[float], float, bool | None]] = [
        ("documented-false", [1.0, 2.0, 3.0], 0.5, False),
        ("documented-true", [1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3, True),
        ("empty", [], 1.0, False),
        ("single-self-index-only", [4.0], 1.0, False),
        ("distance-equals-threshold", [0.0, 1.0], 1.0, False),
        ("distance-below-threshold", [0.0, 1.0], math.nextafter(1.0, math.inf), True),
        ("distance-above-threshold", [0.0, 1.0], math.nextafter(1.0, 0.0), False),
        ("zero-threshold-duplicates", [2.0, 2.0], 0.0, False),
        ("positive-threshold-duplicates", [2.0, 2.0], 5e-324, True),
        ("negative-threshold", [0.0, 0.0], -1.0, False),
        ("true-persists-through-later-pairs", [0.0, 0.1, 100.0, 200.0], 0.2, True),
        ("signed-zero", [-0.0, 0.0], 5e-324, True),
        ("subnormal-boundary", [0.0, 5e-324], 5e-324, False),
        ("large-overflow-distance", [-sys.float_info.max, sys.float_info.max], math.inf, False),
        ("positive-infinities", [math.inf, math.inf], 1.0, False),
        ("nan-element", [0.0, math.nan, 0.1], 0.2, True),
        ("nan-threshold", [0.0, 0.0], math.nan, False),
    ]

    finite_values = [-2.0, -1.0, -0.5, -0.0, 0.5, 1.0, 2.0]
    thresholds = [
        -1.0,
        -0.0,
        5e-324,
        0.25,
        0.5,
        math.nextafter(0.5, math.inf),
        1.0,
        math.nextafter(1.0, math.inf),
        2.0,
    ]
    generated: list[tuple[str, list[float], float, bool | None]] = []
    for length in range(5):
        for values in itertools.product(finite_values, repeat=length):
            for threshold in thresholds:
                generated.append(
                    ("exhaustive-small", list(values), threshold, None)
                )

    randomizer = random.Random(SEED)
    random_values = [
        -1e308,
        -1000.0,
        -2.0,
        -1.0,
        -5e-324,
        -0.0,
        0.0,
        5e-324,
        0.1,
        0.2,
        0.3,
        1.0,
        2.0,
        1000.0,
        1e308,
    ]
    random_thresholds = [
        -1e308,
        -1.0,
        -0.0,
        5e-324,
        0.1,
        0.2,
        0.3,
        1.0,
        1e308,
        math.inf,
        math.nan,
    ]
    for _ in range(20_000):
        length = randomizer.randrange(0, 10)
        numbers = [randomizer.choice(random_values) for _ in range(length)]
        threshold = randomizer.choice(random_thresholds)
        generated.append(("seeded-random", numbers, threshold, None))
    return named + generated


def main() -> int:
    canonical = load_entry(CANONICAL_PATH, "trusted_canonical")
    candidate = load_entry(CANDIDATE_PATH, "audited_generated")
    all_cases = cases()
    digest = hashlib.sha256()
    mismatches: list[dict[str, object]] = []
    label_counts: dict[str, int] = {}

    with INPUT_ARTIFACT.open("wb") as raw:
        with gzip.GzipFile(fileobj=raw, mode="wb", mtime=0) as compressed:
            for label, numbers, threshold, expected in all_cases:
                encoded = encoded_case(label, numbers, threshold)
                line = (
                    json.dumps(encoded, sort_keys=True, separators=(",", ":"))
                    + "\n"
                ).encode()
                digest.update(line)
                compressed.write(line)
                label_counts[label] = label_counts.get(label, 0) + 1

                canonical_result = canonical(list(numbers), threshold)
                candidate_result = candidate(list(numbers), threshold)
                oracle_result = independent_oracle(list(numbers), threshold)
                if (
                    canonical_result is not candidate_result
                    or candidate_result is not oracle_result
                    or (expected is not None and candidate_result is not expected)
                ):
                    mismatches.append(
                        {
                            **encoded,
                            "canonical": canonical_result,
                            "candidate": candidate_result,
                            "oracle": oracle_result,
                            "expected": expected,
                        }
                    )

    print(f"canonical={CANONICAL_PATH}")
    print(f"candidate={CANDIDATE_PATH}")
    print("oracle=independent unordered-index-pair any(abs(a-b) < threshold)")
    print(f"seed={SEED}")
    print(f"case_count={len(all_cases)}")
    print(f"label_counts={json.dumps(label_counts, sort_keys=True)}")
    print(f"input_jsonl_sha256={digest.hexdigest()}")
    print(f"input_artifact={INPUT_ARTIFACT}")
    print(f"input_artifact_bytes={INPUT_ARTIFACT.stat().st_size}")
    print(f"mismatch_count={len(mismatches)}")
    for mismatch in mismatches[:20]:
        print(f"MISMATCH {json.dumps(mismatch, sort_keys=True)}")
    return 0 if not mismatches else 1


if __name__ == "__main__":
    raise SystemExit(main())
