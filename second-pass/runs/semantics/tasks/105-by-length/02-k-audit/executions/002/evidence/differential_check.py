#!/usr/bin/env python3
"""Independent Python differential test for HumanEval 105."""

from __future__ import annotations

from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path
from random import Random
import sys


SCRATCH = Path("/tmp/audit-work/105-by-length/recon")
WORDS = {
    1: "One",
    2: "Two",
    3: "Three",
    4: "Four",
    5: "Five",
    6: "Six",
    7: "Seven",
    8: "Eight",
    9: "Nine",
}


def import_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.by_length


def contract_oracle(values: list[int]) -> list[str]:
    return [WORDS[value] for value in sorted(values, reverse=True) if value in WORDS]


def cases() -> list[list[int]]:
    documented = [
        [2, 1, 1, 4, 5, 8, 2, 3],
        [],
        [1, -1, 55],
    ]
    boundaries = [
        [-1, 0, 1, 9, 10, 55],
        [1],
        [9],
        [0],
        [10],
        list(range(1, 10)),
        list(range(9, 0, -1)),
        [1, 1, 9, 9, 0, 10],
        [-(10**100), 10**100, 1, 9],
        [5] * 40,
    ]
    exhaustive = [
        list(values)
        for length in range(6)
        for values in product((-2, 0, 1, 2, 8, 9, 10), repeat=length)
    ]
    random = Random(105_2026)
    generated: list[list[int]] = []
    for index in range(2_000):
        length = random.randint(0, 100)
        values = [random.randint(-50, 50) for _ in range(length)]
        if index % 20 == 0:
            values.extend([-(10**100), 10**100])
        generated.append(values)
    return documented + boundaries + exhaustive + generated


def main() -> int:
    canonical = import_entry(SCRATCH / "canonical.py", "trusted_canonical")
    candidate = import_entry(SCRATCH / "solution.py", "submitted_solution")
    inputs = cases()
    serialized = json.dumps(inputs, separators=(",", ":")).encode()
    mismatch_count = 0
    for index, values in enumerate(inputs):
        expected = contract_oracle(values)
        canonical_result = canonical(values.copy())
        candidate_result = candidate(values.copy())
        if canonical_result != expected or candidate_result != expected:
            mismatch_count += 1
            if mismatch_count <= 10:
                print(
                    "MISMATCH",
                    json.dumps(
                        {
                            "index": index,
                            "input": values,
                            "oracle": expected,
                            "canonical": canonical_result,
                            "candidate": candidate_result,
                        },
                        sort_keys=True,
                    ),
                )
    print("DOMAIN: finite lists containing only Python int values (bool excluded)")
    print("DOCUMENTED_CASES: 3")
    print(
        "EXHAUSTIVE_CASES: all lengths 0..5 over "
        "[-2, 0, 1, 2, 8, 9, 10]"
    )
    print(
        "GENERATED_CASES: 2000, seed=1052026, lengths 0..100, "
        "values -50..50, periodic +/-10**100"
    )
    print(f"TOTAL_CASES: {len(inputs)}")
    print(f"INPUTS_JSON_SHA256: {sha256(serialized).hexdigest()}")
    print(f"MISMATCH_COUNT: {mismatch_count}")
    return 1 if mismatch_count else 0


if __name__ == "__main__":
    sys.exit(main())
