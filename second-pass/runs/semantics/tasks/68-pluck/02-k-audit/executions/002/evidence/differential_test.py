#!/usr/bin/env python3
"""Independent differential test for trusted canonical.py and candidate solution.py."""

from __future__ import annotations

import importlib.util
import json
import random
from pathlib import Path


CANONICAL_PATH = Path("/reference/canonical.py")
CANDIDATE_PATH = Path("/candidate/solution.py")
CORPUS_PATH = Path("/audit-output/evidence/differential_corpus.json")
SEED = 680068


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.pluck


def independent_oracle(values: list[int]) -> list[int]:
    even_pairs = [
        (value, index)
        for index, value in enumerate(values)
        if value % 2 == 0
    ]
    if not even_pairs:
        return []
    value, index = min(even_pairs)
    return [value, index]


def main() -> None:
    canonical = load_function(CANONICAL_PATH, "trusted_canonical_68")
    candidate = load_function(CANDIDATE_PATH, "candidate_solution_68")
    fixed_cases: list[dict[str, object]] = [
        {"label": "prompt-example-1", "input": [4, 2, 3], "expected": [2, 1]},
        {"label": "prompt-example-2", "input": [1, 2, 3], "expected": [2, 1]},
        {"label": "prompt-empty", "input": [], "expected": []},
        {
            "label": "prompt-example-4-duplicate-zero",
            "input": [5, 0, 3, 0, 4, 2],
            "expected": [0, 1],
        },
        {"label": "singleton-zero", "input": [0], "expected": [0, 0]},
        {"label": "singleton-even", "input": [2], "expected": [2, 0]},
        {"label": "singleton-odd", "input": [1], "expected": []},
        {"label": "no-even", "input": [1, 3, 5, 7], "expected": []},
        {"label": "first-even-sentinel-branch", "input": [9, 8], "expected": [8, 1]},
        {"label": "later-smaller-update", "input": [8, 9, 6], "expected": [6, 2]},
        {"label": "later-greater-no-update", "input": [2, 9, 8], "expected": [2, 0]},
        {"label": "equal-tie-no-update", "input": [4, 7, 4], "expected": [4, 0]},
        {"label": "zero-after-positive-even", "input": [8, 0], "expected": [0, 1]},
        {
            "label": "arbitrary-precision-values",
            "input": [10**100 + 1, 10**100 + 2, 0, 10**100],
            "expected": [0, 2],
        },
        {
            "label": "maximum-documented-length",
            "input": [9999] * 9999 + [2],
            "expected": [2, 9999],
        },
    ]

    rng = random.Random(SEED)
    generated_inputs: list[list[int]] = []
    for _ in range(2000):
        length = rng.randrange(0, 129)
        generated_inputs.append([rng.randrange(0, 10001) for _ in range(length)])
    for _ in range(20):
        length = rng.randrange(1000, 10001)
        generated_inputs.append([rng.randrange(0, 1000001) for _ in range(length)])

    corpus = {
        "domain": "finite lists of nonnegative Python integers",
        "seed": SEED,
        "fixed_cases": fixed_cases,
        "generated_inputs": generated_inputs,
    }
    CORPUS_PATH.write_text(json.dumps(corpus, separators=(",", ":")) + "\n")

    mismatch_count = 0
    for case in fixed_cases:
        values = case["input"]
        expected = case["expected"]
        assert isinstance(values, list)
        canonical_result = canonical(list(values))
        candidate_result = candidate(list(values))
        oracle_result = independent_oracle(list(values))
        ok = canonical_result == candidate_result == oracle_result == expected
        print(
            f"FIXED label={case['label']} length={len(values)} "
            f"canonical={canonical_result} candidate={candidate_result} "
            f"oracle={oracle_result} expected={expected} ok={ok}"
        )
        mismatch_count += int(not ok)

    for index, values in enumerate(generated_inputs):
        canonical_result = canonical(list(values))
        candidate_result = candidate(list(values))
        oracle_result = independent_oracle(list(values))
        if not (canonical_result == candidate_result == oracle_result):
            mismatch_count += 1
            print(
                f"MISMATCH generated_index={index} input={values!r} "
                f"canonical={canonical_result!r} candidate={candidate_result!r} "
                f"oracle={oracle_result!r}"
            )

    print(f"seed={SEED}")
    print(f"fixed_case_count={len(fixed_cases)}")
    print(f"generated_case_count={len(generated_inputs)}")
    print(f"total_case_count={len(fixed_cases) + len(generated_inputs)}")
    print(f"mismatch_count={mismatch_count}")
    if mismatch_count:
        raise SystemExit(1)
    print("DIFFERENTIAL=PASS")


if __name__ == "__main__":
    main()
