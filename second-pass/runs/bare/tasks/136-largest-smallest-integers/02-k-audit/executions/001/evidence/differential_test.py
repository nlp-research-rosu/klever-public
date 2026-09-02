#!/usr/bin/env python3
"""Independent differential test for HumanEval/136."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import random
import sys


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.largest_smallest_integers


def build_cases() -> list[list[int]]:
    targeted = [
        [],
        [0],
        [-1],
        [1],
        [-2, -1],  # replace current negative extremum
        [-1, -2],  # retain current negative extremum
        [2, 1],  # replace current positive extremum
        [1, 2],  # retain current positive extremum
        [-1, -1, 0, 1, 1],
        [0, -4, 9, -2, 3, 0],
        [-(10**100), -1, 10**100, 1],
        [10**100],
        [-(10**100)],
        [0] * 40,
    ]
    exhaustive = [
        list(values)
        for length in range(6)
        for values in itertools.product(range(-3, 4), repeat=length)
    ]
    rng = random.Random(136_20260726)
    generated: list[list[int]] = []
    for _ in range(1000):
        length = rng.randrange(0, 61)
        case: list[int] = []
        for _ in range(length):
            selector = rng.randrange(5)
            if selector == 0:
                case.append(rng.randrange(-10, 11))
            elif selector == 1:
                case.append(rng.randrange(-(10**12), 10**12 + 1))
            elif selector == 2:
                case.append(rng.choice([-1, 0, 1]))
            elif selector == 3:
                case.append(rng.randrange(-(10**100), 10**100 + 1))
            else:
                case.append(rng.randrange(-1000, 1001))
        generated.append(case)
    return targeted + exhaustive + generated


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("canonical", type=Path)
    parser.add_argument("generated", type=Path)
    parser.add_argument("inputs_json", type=Path)
    args = parser.parse_args()

    canonical = load_entry(args.canonical, "trusted_canonical_136")
    generated = load_entry(args.generated, "candidate_generated_136")
    cases = build_cases()
    encoded = json.dumps(cases, separators=(",", ":")).encode()
    serialized_inputs = encoded + b"\n"
    args.inputs_json.write_bytes(serialized_inputs)

    mismatches = []
    for index, case in enumerate(cases):
        expected = canonical(list(case))
        actual = generated(list(case))
        if actual != expected or type(actual) is not type(expected):
            mismatches.append(
                {
                    "index": index,
                    "input": case,
                    "canonical": expected,
                    "generated": actual,
                }
            )
            if len(mismatches) == 20:
                break

    print("oracle=/tmp/audit-work/reconstruction/canonical.py")
    print("generated=/tmp/audit-work/reconstruction/solution.py")
    print("targeted_cases=14")
    print("exhaustive_domain=all sequences length 0..5 over integers -3..3")
    print("exhaustive_cases=19608")
    print("seed=13620260726")
    print("seeded_cases=1000 lengths 0..60 with small, 12-digit, and 100-digit ints")
    print(f"total_cases={len(cases)}")
    print(f"inputs_sha256={hashlib.sha256(serialized_inputs).hexdigest()}")
    print(f"mismatch_count={len(mismatches)}")
    if mismatches:
        print(json.dumps(mismatches, indent=2))
        return 1
    print("DIFFERENTIAL_RESULT=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
