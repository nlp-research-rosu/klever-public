#!/usr/bin/env python3
"""Independent differential test against the trusted HumanEval canonical entry."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
from pathlib import Path


CANONICAL_PATH = Path("/reference/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/solution.py")
INPUTS_PATH = Path("/audit-output/evidence/differential-inputs.json")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_cases() -> list[list[int]]:
    # Examples plus loop, sign, zero, parity, singleton, and big-int boundaries.
    explicit = [
        [],
        [1, 2, 3, 4],
        [0],
        [1],
        [-1],
        [2],
        [-2],
        [0, 0],
        [-2, 3],
        [-2, -3],
        [-2, 3, 0],
        [10**100, -(10**100), 1],
        [-(10**80), -(10**80), 0, 7],
    ]
    exhaustive = [
        list(values)
        for length in range(6)
        for values in itertools.product(range(-3, 4), repeat=length)
    ]
    rng = random.Random(8008)
    generated: list[list[int]] = []
    for _ in range(500):
        length = rng.randrange(0, 31)
        generated.append([rng.randrange(-(10**12), 10**12 + 1) for _ in range(length)])
    # Preserve the exact deterministic test corpus, with source categories.
    payload = {
        "explicit": explicit,
        "exhaustive_definition": {"lengths": [0, 1, 2, 3, 4, 5], "values": [-3, -2, -1, 0, 1, 2, 3]},
        "random_seed": 8008,
        "generated": generated,
    }
    INPUTS_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return explicit + exhaustive + generated


def main() -> int:
    canonical = load_module("trusted_canonical", CANONICAL_PATH)
    generated = load_module("audited_generated", GENERATED_PATH)
    cases = build_cases()
    mismatches = []
    for numbers in cases:
        canonical_result = canonical.sum_product(numbers.copy())
        generated_result = generated.sum_product(numbers.copy())
        if canonical_result != generated_result:
            mismatches.append((numbers, canonical_result, generated_result))
    print(f"canonical={CANONICAL_PATH}")
    print(f"generated={GENERATED_PATH}")
    print(f"documented_examples=2")
    print(f"explicit_boundary_cases=13")
    print(f"exhaustive_small_cases={sum(7**length for length in range(6))}")
    print("representative_generated_cases=500 seed=8008 max_length=30")
    print(f"total_cases={len(cases)}")
    print(f"mismatches={len(mismatches)}")
    for mismatch in mismatches[:20]:
        print(repr(mismatch))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
