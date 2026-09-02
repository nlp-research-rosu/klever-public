#!/usr/bin/env python3
"""Independent differential test for HumanEval/0."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import random
from pathlib import Path
from typing import Any, Callable


def load_entry(path: Path, module_name: str) -> Callable[[list[float], float], bool]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.has_close_elements


def run_one(fn: Callable[..., Any], numbers: list[float], threshold: float) -> tuple[str, str]:
    try:
        return ("return", repr(fn(list(numbers), threshold)))
    except BaseException as error:  # Deliberately compare observable exceptions too.
        return ("raise", type(error).__name__)


def json_float(value: float) -> str:
    if math.isnan(value):
        return "NaN"
    if value == math.inf:
        return "Infinity"
    if value == -math.inf:
        return "-Infinity"
    return repr(value)


def encode_case(name: str, numbers: list[float], threshold: float) -> str:
    return json.dumps(
        {
            "name": name,
            "numbers": [json_float(value) for value in numbers],
            "threshold": json_float(threshold),
        },
        sort_keys=True,
    )


def main() -> int:
    canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
    generated = load_entry(
        Path("/tmp/audit-work/candidate-src/solution.py"), "generated_solution"
    )

    named_cases: list[tuple[str, list[float], float]] = [
        ("prompt_false", [1.0, 2.0, 3.0], 0.5),
        ("prompt_true", [1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3),
        ("empty", [], 1.0),
        ("singleton", [1.0], 1.0),
        ("strict_equal", [1.0, 1.5], 0.5),
        ("strict_just_above", [1.0, 1.5], 0.5000001),
        ("strict_just_below", [1.0, 1.5], 0.4999999),
        ("first_pair_true", [1.0, 1.1, 9.0], 0.2),
        ("later_pair_true", [0.0, 10.0, 10.1], 0.2),
        ("no_pair", [-10.0, 0.0, 10.0], 1.0),
        ("duplicate_positive_threshold", [2.0, 7.0, 2.0], 0.01),
        ("duplicate_zero_threshold", [2.0, 2.0], 0.0),
        ("negative_threshold", [1.0, 1.0], -1.0),
        ("negative_values", [-3.5, -3.25, 8.0], 0.3),
        ("infinite_threshold", [0.0, 1.0], math.inf),
        ("infinite_values", [math.inf, math.inf], 1.0),
        ("nan_value", [math.nan, 0.0], math.inf),
    ]

    rng = random.Random(0xC10E)
    pool = [-8.5, -3.25, -1.0, -0.0, 0.0, 0.125, 1.0, 2.75, 9.5]
    thresholds = [-1.0, 0.0, 0.125, 0.5, 2.0, 10.0]
    generated_cases: list[tuple[str, list[float], float]] = []
    for index in range(160):
        length = rng.randrange(0, 9)
        numbers = [rng.choice(pool) for _ in range(length)]
        threshold = rng.choice(thresholds)
        generated_cases.append((f"generated_{index:03d}", numbers, threshold))

    normal_mismatches: list[dict[str, Any]] = []
    corpus_lines: list[str] = []
    for name, numbers, threshold in named_cases + generated_cases:
        corpus_lines.append(encode_case(name, numbers, threshold))
        expected = run_one(canonical, numbers, threshold)
        observed = run_one(generated, numbers, threshold)
        if expected != observed:
            normal_mismatches.append(
                {
                    "name": name,
                    "numbers": [json_float(value) for value in numbers],
                    "threshold": json_float(threshold),
                    "canonical": expected,
                    "generated": observed,
                }
            )

    # The annotation states List[float] without a size bound. This case stays
    # within that domain and exposes the generated implementation's recursion
    # depth, which the canonical loop implementation does not share.
    long_case = ("long_no_pair_1050", [float(2 * i) for i in range(1050)], 0.5)
    corpus_lines.append(encode_case(*long_case))
    long_expected = run_one(canonical, long_case[1], long_case[2])
    long_observed = run_one(generated, long_case[1], long_case[2])
    long_mismatch = long_expected != long_observed

    corpus_hash = hashlib.sha256(("\n".join(corpus_lines) + "\n").encode()).hexdigest()
    print("oracle=/reference/canonical.py:has_close_elements")
    print("candidate=/tmp/audit-work/candidate-src/solution.py:has_close_elements")
    print("random_seed=0xC10E")
    print(f"named_cases={len(named_cases)}")
    print(f"generated_cases={len(generated_cases)}")
    print(f"input_corpus_sha256={corpus_hash}")
    print(f"normal_mismatches={len(normal_mismatches)}")
    for mismatch in normal_mismatches:
        print("NORMAL_MISMATCH " + json.dumps(mismatch, sort_keys=True))
    print(
        "LONG_CASE "
        + json.dumps(
            {
                "name": long_case[0],
                "length": len(long_case[1]),
                "threshold": long_case[2],
                "canonical": long_expected,
                "generated": long_observed,
                "mismatch": long_mismatch,
            },
            sort_keys=True,
        )
    )
    return 1 if normal_mismatches or long_mismatch else 0


if __name__ == "__main__":
    raise SystemExit(main())
