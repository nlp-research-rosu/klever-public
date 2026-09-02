#!/usr/bin/env python3
"""Differentially compare trusted canonical.py with the submitted solution.py."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path
from types import ModuleType
from typing import Callable


def load(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--solution", type=Path, required=True)
    parser.add_argument("--inputs-out", type=Path, required=True)
    return parser.parse_args()


def add_case(
    cases: list[tuple[str, list[int]]],
    seen: set[tuple[int, ...]],
    category: str,
    values: list[int],
) -> None:
    key = tuple(values)
    if key not in seen:
        seen.add(key)
        cases.append((category, values))


def main() -> int:
    args = parse_args()
    canonical: Callable[[list[int]], int] = load(
        args.canonical, "trusted_canonical"
    ).sum_squares
    generated: Callable[[list[int]], int] = load(
        args.solution, "submitted_solution"
    ).sum_squares

    cases: list[tuple[str, list[int]]] = []
    seen: set[tuple[int, ...]] = set()

    examples = [
        ([1, 2, 3], 6),
        ([], 0),
        ([-1, -5, 2, -1, -5], -126),
    ]
    for values, expected in examples:
        assert canonical(values.copy()) == expected
        assert generated(values.copy()) == expected
        add_case(cases, seen, "documented_example", values)

    # Every list length boundary through index 13.  The values expose index
    # classes 0/12 (both multiples), 3/6/9 (multiple of 3), 4/8 (multiple of
    # 4 only), and ordinary indices.
    for length in range(15):
        add_case(cases, seen, "length_boundary_zero", [0] * length)
        add_case(cases, seen, "length_boundary_mixed", list(range(-7, -7 + length)))
        for index in range(length):
            one_hot = [0] * length
            one_hot[index] = -3 if index % 2 else 2
            add_case(cases, seen, f"one_hot_index_{index}", one_hot)

    # Exhaustive short-list coverage for negative, zero, and positive entries.
    for length in range(6):
        for values in itertools.product(range(-2, 3), repeat=length):
            add_case(cases, seen, f"exhaustive_len_{length}", list(values))

    # Reproducible wider and longer representative inputs.
    rng = random.Random(142)
    for _ in range(500):
        length = rng.randrange(0, 41)
        values = [rng.randint(-100, 100) for _ in range(length)]
        add_case(cases, seen, "seeded_random", values)

    mismatches: list[dict[str, object]] = []
    digest = hashlib.sha256()
    category_counts: dict[str, int] = {}
    args.inputs_out.parent.mkdir(parents=True, exist_ok=True)
    with args.inputs_out.open("w", encoding="utf-8") as output:
        for category, values in cases:
            expected = canonical(values.copy())
            actual = generated(values.copy())
            record = {
                "category": category,
                "input": values,
                "canonical": expected,
                "solution": actual,
            }
            encoded = json.dumps(record, separators=(",", ":"), sort_keys=True)
            output.write(encoded + "\n")
            digest.update((encoded + "\n").encode())
            category_counts[category] = category_counts.get(category, 0) + 1
            if expected != actual:
                mismatches.append(record)

    print(f"canonical={args.canonical}")
    print(f"solution={args.solution}")
    print("oracle=independently imported trusted canonical.sum_squares")
    print("formal_input_shape=finite Python lists of Python integers")
    print(f"case_count={len(cases)}")
    print(f"input_result_jsonl={args.inputs_out}")
    print(f"input_result_sha256={digest.hexdigest()}")
    print("category_counts=" + json.dumps(category_counts, sort_keys=True))
    print(f"mismatch_count={len(mismatches)}")
    if mismatches:
        print("first_mismatches=" + json.dumps(mismatches[:10], sort_keys=True))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
