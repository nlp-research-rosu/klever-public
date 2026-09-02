#!/usr/bin/env python3
"""Independent differential test for HumanEval 105 by_length."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path


sys.dont_write_bytecode = True

CANONICAL_PATH = Path("/reference/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/105-by-length/candidate/solution.py")
INPUTS_PATH = Path("/audit-output/evidence/differential-inputs.json")


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.by_length


def contract_oracle(values: list[int]) -> list[str]:
    names = {
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
    return [names[value] for value in sorted(values, reverse=True) if 1 <= value <= 9]


def build_cases() -> list[list[int]]:
    documented = [
        [2, 1, 1, 4, 5, 8, 2, 3],
        [],
        [1, -1, 55],
    ]
    boundaries = [
        [-1],
        [0],
        [1],
        [2],
        [8],
        [9],
        [10],
        [11],
        [0, 1],
        [1, 9],
        [9, 10],
        [10, 9, 1, 0],
        [9, 9, 1, 1, 0, 10],
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [9, 8, 7, 6, 5, 4, 3, 2, 1],
        [10**100, 9, -(10**100), 1],
    ]

    alphabet = [-1, 0, 1, 2, 8, 9, 10]
    exhaustive = [
        list(values)
        for length in range(5)
        for values in itertools.product(alphabet, repeat=length)
    ]

    rng = random.Random(0x105)
    generated = []
    for _ in range(256):
        length = rng.randrange(0, 33)
        generated.append([rng.randint(-1000, 1000) for _ in range(length)])

    cases: list[list[int]] = []
    seen: set[tuple[int, ...]] = set()
    for values in documented + boundaries + exhaustive + generated:
        key = tuple(values)
        if key not in seen:
            seen.add(key)
            cases.append(values)
    return cases


def main() -> int:
    canonical = load_entry("trusted_canonical_105", CANONICAL_PATH)
    generated = load_entry("submitted_solution_105", GENERATED_PATH)
    cases = build_cases()
    INPUTS_PATH.write_text(json.dumps(cases, indent=2) + "\n", encoding="utf-8")

    mismatches = []
    digest = hashlib.sha256(INPUTS_PATH.read_bytes()).hexdigest()
    print(f"canonical={CANONICAL_PATH}")
    print(f"generated={GENERATED_PATH}")
    print(f"input_file={INPUTS_PATH}")
    print(f"input_sha256={digest}")
    print(f"case_count={len(cases)}")
    print(
        "scope=documented examples; empty; explicit -1/0/1/2/8/9/10/11 "
        "boundaries; duplicates/orders/huge integers; all length-0..4 lists "
        "over [-1,0,1,2,8,9,10]; 256 seed-0x105 integer lists"
    )

    for index, values in enumerate(cases):
        expected = contract_oracle(values)
        try:
            canonical_result = canonical(list(values))
            canonical_error = None
        except Exception as error:  # evidence records unexpected intended-domain errors
            canonical_result = None
            canonical_error = f"{type(error).__name__}: {error}"
        try:
            generated_result = generated(list(values))
            generated_error = None
        except Exception as error:
            generated_result = None
            generated_error = f"{type(error).__name__}: {error}"

        if (
            canonical_error is not None
            or generated_error is not None
            or canonical_result != generated_result
            or canonical_result != expected
        ):
            mismatches.append(
                {
                    "index": index,
                    "input": values,
                    "contract": expected,
                    "canonical": canonical_result,
                    "canonical_error": canonical_error,
                    "generated": generated_result,
                    "generated_error": generated_error,
                }
            )

    print(f"mismatch_count={len(mismatches)}")
    for mismatch in mismatches[:20]:
        print(json.dumps(mismatch, sort_keys=True))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
