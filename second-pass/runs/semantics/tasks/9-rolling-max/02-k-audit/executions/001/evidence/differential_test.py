#!/usr/bin/env python3
"""Independent candidate-vs-trusted-canonical differential test."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path
from types import ModuleType
from typing import Callable, List


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_cases() -> tuple[list[list[int]], dict[str, object]]:
    named_cases = [
        [],
        [0],
        [-7],
        [10**100],
        [-(10**100)],
        [1, 2, 3, 2, 3, 4, 2],
        [-8, -9, -3, -3, -10],
        [5, 5, 4, 6, 1],
        [4, 3],  # later value below maximum
        [4, 4],  # later value equal to maximum
        [3, 4],  # later value above maximum
        [3, 1, 4],  # concrete K claim witness
        [-1, 0, -2, 1, -3],
        [9, 8, 7, 6, 5],
        [1, 2, 3, 4, 5],
    ]

    alphabet = [-2, -1, 0, 1, 2]
    exhaustive = [
        list(values)
        for length in range(0, 6)
        for values in itertools.product(alphabet, repeat=length)
    ]

    rng = random.Random(0x9A11D17)
    random_cases: list[list[int]] = []
    for length in [0, 1, 2, 3, 8, 9, 16, 32, 257]:
        for _ in range(40):
            random_cases.append(
                [rng.randint(-(10**30), 10**30) for _ in range(length)]
            )

    ordered: list[list[int]] = []
    seen: set[tuple[int, ...]] = set()
    for case in named_cases + exhaustive + random_cases:
        key = tuple(case)
        if key not in seen:
            seen.add(key)
            ordered.append(case)

    scope = {
        "named_cases": named_cases,
        "exhaustive_alphabet": alphabet,
        "exhaustive_lengths": [0, 1, 2, 3, 4, 5],
        "random_seed": "0x9A11D17",
        "random_lengths": [0, 1, 2, 3, 8, 9, 16, 32, 257],
        "random_cases_per_length": 40,
        "intended_domain": "finite Python lists whose elements are Python ints",
    }
    return ordered, scope


def outcome(function: Callable[[List[int]], List[int]], values: list[int]) -> dict[str, object]:
    try:
        result = function(list(values))
        return {"kind": "return", "value": result}
    except Exception as error:  # Evidence records exception equivalence too.
        return {
            "kind": "exception",
            "type": type(error).__qualname__,
            "message": str(error),
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--inputs-out", type=Path, required=True)
    args = parser.parse_args()

    canonical_module = load_module("trusted_canonical", args.canonical)
    candidate_module = load_module("audited_candidate", args.candidate)
    cases, scope = build_cases()

    payload = {"scope": scope, "cases": cases}
    encoded = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    args.inputs_out.write_bytes(encoded + b"\n")

    mismatches: list[dict[str, object]] = []
    for index, values in enumerate(cases):
        expected = outcome(canonical_module.rolling_max, values)
        actual = outcome(candidate_module.rolling_max, values)
        if expected != actual:
            mismatches.append(
                {
                    "index": index,
                    "input": values,
                    "canonical": expected,
                    "candidate": actual,
                }
            )

    inputs_hash = hashlib.sha256(encoded + b"\n").hexdigest()
    print(f"canonical={args.canonical}")
    print(f"candidate={args.candidate}")
    print(f"case_count={len(cases)}")
    print(f"inputs_sha256={inputs_hash}")
    print(f"mismatch_count={len(mismatches)}")
    witness = [3, 1, 4]
    print(f"witness_input={witness}")
    print(f"canonical_witness={canonical_module.rolling_max(list(witness))}")
    print(f"candidate_witness={candidate_module.rolling_max(list(witness))}")
    if mismatches:
        print(json.dumps(mismatches[:20], indent=2, sort_keys=True))
        return 1
    print("RESULT: all candidate results matched the trusted canonical")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
