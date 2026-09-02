#!/usr/bin/env python3
"""Independent deterministic differential test for HumanEval 33."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path
from typing import Any, Callable


def load_entry(path: Path, module_name: str) -> Callable[[list[Any]], list[Any]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_third


def cases() -> list[list[Any]]:
    documented_and_boundaries = [
        [1, 2, 3],
        [5, 6, 3, 4, 8, 9, 2],
        [],
        [9],
        [9, 8],
        [9, 8, 7],
        [9, 8, 7, 6],
        [9, 8, 7, 6, 5],
        [9, 8, 7, 6, 5, 4],
        [9, 8, 7, 6, 5, 4, 3],
        [9, 8, 7, 6, 5, 4, 3, 2],
        [3, 0, 0, 2, 0, 0, 1],
        [1, 0, 0, 2, 0, 0, 3],
        [2, 0, 0, 2, 0, 0, 2],
        [-1, 7, 8, -3, 9, 10, -2],
        [10**100, 1, 2, -(10**100), 3, 4, 0],
        ["z", "keep-1", "keep-2", "a", "keep-4", "keep-5", "m"],
        [3.5, 1.0, 2.0, -1.25, 4.0, 5.0, 2.75],
        [(2, 0), (8, 8), (9, 9), (0, 1), (7, 7), (6, 6), (1, 5)],
    ]

    # Exhaustive small integer lists cover slice-length boundaries, duplicate
    # values, negatives, and both insertion-sort comparison branches.
    exhaustive = [
        list(values)
        for length in range(7)
        for values in itertools.product(range(-2, 3), repeat=length)
    ]

    rng = random.Random(330033)
    generated = [
        [rng.randint(-10_000, 10_000) for _ in range(rng.randint(7, 60))]
        for _ in range(500)
    ]

    return documented_and_boundaries + exhaustive + generated


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("canonical", type=Path)
    parser.add_argument("candidate", type=Path)
    args = parser.parse_args()

    canonical = load_entry(args.canonical, "trusted_canonical")
    candidate = load_entry(args.candidate, "generated_candidate")
    all_cases = cases()
    serialized = json.dumps(all_cases, separators=(",", ":")).encode()
    mismatches: list[dict[str, object]] = []

    for index, original in enumerate(all_cases):
        canonical_input = list(original)
        candidate_input = list(original)
        try:
            expected = canonical(canonical_input)
            expected_exc: object = None
        except Exception as exc:  # pragma: no cover - retained for clear evidence
            expected = None
            expected_exc = (type(exc).__name__, str(exc))
        try:
            actual = candidate(candidate_input)
            actual_exc: object = None
        except Exception as exc:  # pragma: no cover - retained for clear evidence
            actual = None
            actual_exc = (type(exc).__name__, str(exc))

        if (
            expected != actual
            or expected_exc != actual_exc
            or canonical_input != original
            or candidate_input != original
        ):
            mismatches.append(
                {
                    "index": index,
                    "input": original,
                    "canonical": expected,
                    "candidate": actual,
                    "canonical_exception": expected_exc,
                    "candidate_exception": actual_exc,
                    "canonical_input_after": canonical_input,
                    "candidate_input_after": candidate_input,
                }
            )

    print("ORACLE=/tmp/audit-work/33-sort-third/canonical.py")
    print("CANDIDATE=/tmp/audit-work/33-sort-third/solution.py")
    print("SCOPE=documented cases; explicit lengths 0..8; branch witnesses;")
    print("      representative orderable string, float, and tuple lists;")
    print("      exhaustive lists of lengths 0..6 over integers -2..2;")
    print("      500 seeded lists of lengths 7..60 over integers -10000..10000")
    print("SEED=330033")
    print(f"CASE_COUNT={len(all_cases)}")
    print(f"INPUTS_SHA256={hashlib.sha256(serialized).hexdigest()}")
    print(f"MISMATCH_COUNT={len(mismatches)}")
    if mismatches:
        print(json.dumps(mismatches[:20], indent=2))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
