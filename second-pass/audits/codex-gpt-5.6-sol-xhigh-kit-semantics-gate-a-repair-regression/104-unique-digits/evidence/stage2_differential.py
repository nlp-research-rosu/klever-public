#!/usr/bin/env python3
"""Independent differential test for HumanEval 104.

The tested inputs are completely determined by this file: named boundary cases,
all positive singleton values 1..2000, and 1,000 lists from Random(104).
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
from pathlib import Path


CANONICAL_PATH = Path("/reference/canonical.py")
GENERATED_PATH = Path(
    "/tmp/audit-work/104-unique-digits-audit/candidate-source/solution.py"
)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_cases() -> list[tuple[str, list[int]]]:
    named = [
        ("prompt-example-1", [15, 33, 1422, 1]),
        ("prompt-example-2", [152, 323, 1422, 10]),
        ("empty-list", []),
        ("single-minimum-odd", [1]),
        ("single-even", [2]),
        ("single-largest-one-digit-odd", [9]),
        ("decimal-boundary-10", [10]),
        ("all-odd-two-digit", [11]),
        ("late-even-digit", [12]),
        ("early-even-digit-short-circuit", [21]),
        ("zero-digit", [101]),
        ("all-odd-three-digit", [135]),
        ("mixed-append-and-reject", [22, 1, 135, 246, 9]),
        ("reverse-sort", [99, 77, 55, 33, 11, 1]),
        ("duplicates", [33, 1, 33, 2, 1]),
        ("large-all-odd", [999999999999999999999999999999999999999]),
        ("large-leading-even", [299999999999999999999999999999999999999]),
        ("large-trailing-even", [999999999999999999999999999999999999998]),
    ]
    exhaustive = [(f"singleton-{value}", [value]) for value in range(1, 2001)]
    generator = random.Random(104)
    generated = []
    for case_index in range(1000):
        length = generator.randrange(0, 25)
        values = [
            generator.randrange(1, 10 ** generator.randrange(1, 31))
            for _ in range(length)
        ]
        generated.append((f"seed104-random-{case_index}", values))
    return named + exhaustive + generated


def main() -> int:
    canonical = load_module("trusted_canonical", CANONICAL_PATH)
    generated = load_module("candidate_generated", GENERATED_PATH)
    cases = build_cases()
    mismatches = []

    explicit_expected = {
        "prompt-example-1": [1, 15, 33],
        "prompt-example-2": [],
        "empty-list": [],
        "duplicates": [1, 1, 33, 33],
    }

    encoded_inputs = json.dumps(cases, separators=(",", ":")).encode()
    for label, values in cases:
        canonical_result = canonical.unique_digits(values.copy())
        generated_result = generated.unique_digits(values.copy())
        if label in explicit_expected and canonical_result != explicit_expected[label]:
            raise AssertionError(
                f"trusted canonical disagrees with documented expected result for {label}"
            )
        if canonical_result != generated_result:
            mismatches.append(
                {
                    "label": label,
                    "input": values,
                    "canonical": canonical_result,
                    "generated": generated_result,
                }
            )

    print(f"CANONICAL_PATH: {CANONICAL_PATH}")
    print(f"GENERATED_PATH: {GENERATED_PATH}")
    print("INPUT_SCOPE: 18 named + singleton 1..2000 + 1000 Random(104) lists")
    print(f"INPUTS_SHA256: {hashlib.sha256(encoded_inputs).hexdigest()}")
    print(f"CASES: {len(cases)}")
    print(f"MISMATCHES: {len(mismatches)}")
    for mismatch in mismatches[:20]:
        print("MISMATCH:", json.dumps(mismatch, sort_keys=True))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
