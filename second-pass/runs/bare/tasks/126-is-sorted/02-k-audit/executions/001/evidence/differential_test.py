#!/usr/bin/env python3
"""Independent differential test for HumanEval 126 over its integer-list domain."""

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


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_case(
    values: list[int],
    canonical: Callable[[list[int]], bool],
    candidate: Callable[[list[int]], bool],
) -> tuple[bool, str]:
    left_input = list(values)
    right_input = list(values)
    expected = canonical(left_input)
    actual = candidate(right_input)
    if left_input != values or right_input != values:
        return False, f"mutation input={values!r} canonical_after={left_input!r} candidate_after={right_input!r}"
    if type(expected) is not bool or type(actual) is not bool:
        return False, f"type input={values!r} canonical={type(expected)} candidate={type(actual)}"
    if actual != expected:
        return False, f"result input={values!r} canonical={expected!r} candidate={actual!r}"
    return True, ""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("canonical")
    parser.add_argument("candidate")
    args = parser.parse_args()

    canonical_module = load_module("trusted_canonical", Path(args.canonical))
    candidate_module = load_module("generated_entry_point", Path(args.candidate))
    canonical = canonical_module.is_sorted
    candidate = candidate_module.is_sorted

    documented = [
        [5],
        [1, 2, 3, 4, 5],
        [1, 3, 2, 4, 5],
        [1, 2, 3, 4, 5, 6],
        [1, 2, 3, 4, 5, 6, 7],
        [1, 3, 2, 4, 5, 6, 7],
        [1, 2, 2, 3, 3, 4],
        [1, 2, 2, 2, 3, 4],
    ]
    boundaries = [
        [],
        [0],
        [0, 0],
        [0, 0, 0],
        [0, 1],
        [1, 0],
        [0, 1, 0],
        [2, 2, 3],
        [2, 2, 2, 3],
        [0, 1, 2, 3, 2],
        [0, 2, 1, 3],
        [1_000_000],
        [0, 1_000_000],
        [1_000_000, 0],
    ]

    corpus: list[list[int]] = []
    corpus.extend(documented)
    corpus.extend(boundaries)
    # Exhaust all lists of lengths 0..6 over representative non-negative values.
    for length in range(7):
        corpus.extend([list(items) for items in itertools.product(range(5), repeat=length)])
    # Deterministic broad sample, including longer lists and large non-negative ints.
    generator = random.Random(126)
    for _ in range(5000):
        length = generator.randrange(0, 25)
        corpus.append([generator.randrange(0, 10_001) for _ in range(length)])

    seen: set[tuple[int, ...]] = set()
    digest = hashlib.sha256()
    mismatches: list[str] = []
    counts = {"documented": len(documented), "boundaries": len(boundaries)}
    tested = 0
    true_count = 0
    false_count = 0
    for values in corpus:
        key = tuple(values)
        if key in seen:
            continue
        seen.add(key)
        ok, detail = check_case(values, canonical, candidate)
        expected = canonical(list(values))
        digest.update(json.dumps([values, expected], separators=(",", ":")).encode())
        digest.update(b"\n")
        tested += 1
        true_count += int(expected)
        false_count += int(not expected)
        if not ok:
            mismatches.append(detail)

    print("DOCUMENTED_INPUTS=" + json.dumps(documented, separators=(",", ":")))
    print("BOUNDARY_INPUTS=" + json.dumps(boundaries, separators=(",", ":")))
    print("EXHAUSTIVE_SCOPE=lengths_0_through_6_values_0_through_4")
    print("GENERATED_SCOPE=seed_126_count_5000_length_0_through_24_values_0_through_10000")
    print(f"UNIQUE_INPUTS_TESTED={tested}")
    print(f"TRUE_RESULTS={true_count}")
    print(f"FALSE_RESULTS={false_count}")
    print(f"INPUT_OUTPUT_CORPUS_SHA256={digest.hexdigest()}")
    print(f"MISMATCHES={len(mismatches)}")
    for mismatch in mismatches[:20]:
        print("MISMATCH " + mismatch)
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
