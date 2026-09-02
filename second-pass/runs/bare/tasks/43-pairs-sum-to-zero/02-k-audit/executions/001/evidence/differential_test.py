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


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.pairs_sum_to_zero


def cases():
    documented = [
        [1, 3, 5, 0],
        [1, 3, -2, 1],
        [1, 2, 3, 7],
        [2, 4, -5, 3, 5, 7],
        [1],
    ]
    boundaries = [
        [],
        [0],
        [0, 0],
        [1, -1],
        [-1, 1],
        [1, 2, -1],
        [1, 2, 3],
        [5, -5, 7],
        [-5, 2, 5],
        [3, 3, -3],
        [2, -2, 2, -2],
        [10**100, -(10**100)],
        [-(10**100), 1, 10**100],
        [1] * 950,
        [1] * 1000,
        [1] * 1100,
    ]
    for value in documented:
        yield "documented", value
    for value in boundaries:
        yield "boundary", value

    alphabet = range(-3, 4)
    for length in range(7):
        for value in itertools.product(alphabet, repeat=length):
            yield "exhaustive[-3,3],length<=6", list(value)

    rng = random.Random(430043)
    for _ in range(5000):
        length = rng.randrange(0, 51)
        yield "seeded-random(seed=430043,n=5000)", [
            rng.randrange(-(10**12), 10**12 + 1) for _ in range(length)
        ]


def summarize(values):
    encoded = json.dumps(values, separators=(",", ":")).encode()
    if len(values) <= 20:
        return values
    return {
        "length": len(values),
        "first10": values[:10],
        "last10": values[-10:],
        "sha256": hashlib.sha256(encoded).hexdigest(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--inputs", type=Path, required=True)
    args = parser.parse_args()

    canonical = load_function(args.canonical, "trusted_canonical")
    candidate = load_function(args.candidate, "generated_candidate")
    count = 0
    mismatches = []
    input_digest = hashlib.sha256()

    with args.inputs.open("w", encoding="utf-8") as output:
        for category, value in cases():
            record = {"category": category, "input": value}
            encoded = json.dumps(record, separators=(",", ":"), sort_keys=True)
            output.write(encoded + "\n")
            input_digest.update((encoded + "\n").encode())

            canonical_arg = list(value)
            candidate_arg = list(value)
            try:
                expected = ("return", canonical(canonical_arg))
            except Exception as error:
                expected = ("raise", type(error).__name__, str(error))
            try:
                actual = ("return", candidate(candidate_arg))
            except Exception as error:
                actual = ("raise", type(error).__name__, str(error))
            if expected != actual or canonical_arg != value or candidate_arg != value:
                mismatches.append({
                    "input": summarize(value),
                    "canonical_outcome": expected,
                    "candidate_outcome": actual,
                    "canonical_after": summarize(canonical_arg),
                    "candidate_after": summarize(candidate_arg),
                })
                if len(mismatches) >= 20:
                    break
            count += 1

    print(f"documented_cases=5")
    print(f"curated_boundary_cases=16 (including recursion-depth boundaries 950,1000,1100)")
    print(f"exhaustive_cases=137257 alphabet=-3..3 lengths=0..6")
    print(f"seeded_random_cases=5000 seed=430043 lengths=0..50 values=-10^12..10^12")
    print(f"tested={count}")
    print(f"input_sha256={input_digest.hexdigest()}")
    print(f"mismatches={len(mismatches)}")
    if mismatches:
        for mismatch in mismatches:
            print(json.dumps(mismatch, sort_keys=True))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
