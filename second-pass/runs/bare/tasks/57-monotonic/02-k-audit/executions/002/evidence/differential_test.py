#!/usr/bin/env python3
"""Independent differential test for HumanEval/57.

The oracle uses adjacent comparisons and does not reuse either implementation's
sorting formulation.  Imports are from the trusted and candidate mounts.
"""

from __future__ import annotations

import importlib.util
import itertools
from pathlib import Path
from typing import Any, Callable


def load_entry(path: Path, module_name: str) -> Callable[[list[Any]], bool]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.monotonic


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical_57")
generated = load_entry(Path("/candidate/solution.py"), "candidate_solution_57")


def independent_oracle(items: list[Any]) -> bool:
    nondecreasing = all(left <= right for left, right in zip(items, items[1:]))
    nonincreasing = all(left >= right for left, right in zip(items, items[1:]))
    return nondecreasing or nonincreasing


EXPLICIT_CASES: list[tuple[str, list[Any]]] = [
    ("prompt-increasing", [1, 2, 4, 20]),
    ("prompt-nonmonotonic", [1, 20, 4, 10]),
    ("prompt-decreasing", [4, 1, 0, -10]),
    ("empty-both-directions", []),
    ("singleton-both-directions", [0]),
    ("two-equal-both-directions", [1, 1]),
    ("two-increasing-first-disjunct", [1, 2]),
    ("two-decreasing-second-disjunct", [2, 1]),
    ("peak-neither-disjunct", [1, 2, 1]),
    ("valley-neither-disjunct", [2, 1, 2]),
    ("nondecreasing-with-duplicates", [-2, -2, 0, 3, 3]),
    ("nonincreasing-with-duplicates", [3, 3, 0, -2, -2]),
    ("large-mathematical-integers", [-(10**100), 0, 10**100]),
    ("mixed-int-float-orderable", [-2, -0.5, 3]),
    ("float-decreasing", [3.25, 3.25, -1.5]),
    ("string-increasing", ["a", "b", "z"]),
    ("string-decreasing", ["z", "b", "a"]),
    ("string-nonmonotonic", ["a", "z", "b"]),
]


def check_case(
    label: str,
    items: list[Any],
    mismatches: list[tuple[str, list[Any], object, object, object]],
) -> None:
    expected = independent_oracle(items)
    canonical_result = canonical(list(items))
    generated_result = generated(list(items))
    if (
        canonical_result != expected
        or generated_result != expected
        or type(canonical_result) is not bool
        or type(generated_result) is not bool
    ):
        mismatches.append(
            (label, items, expected, canonical_result, generated_result)
        )


def main() -> int:
    mismatches: list[tuple[str, list[Any], object, object, object]] = []

    print("EXPLICIT_CASES_BEGIN")
    for label, items in EXPLICIT_CASES:
        expected = independent_oracle(items)
        canonical_result = canonical(list(items))
        generated_result = generated(list(items))
        print(
            f"{label}: input={items!r} oracle={expected!r} "
            f"canonical={canonical_result!r} generated={generated_result!r}"
        )
        check_case(label, items, mismatches)
    print("EXPLICIT_CASES_END")

    generated_scopes = [
        ("ints", (-2, -1, 0, 1, 2), range(0, 8)),
        ("floats", (-1.5, 0.0, 0.25), range(0, 6)),
        ("strings", ("a", "b", "c"), range(0, 6)),
    ]
    total_generated = 0
    for scope_name, alphabet, lengths in generated_scopes:
        scope_count = 0
        for length in lengths:
            for values in itertools.product(alphabet, repeat=length):
                check_case(f"{scope_name}-generated", list(values), mismatches)
                scope_count += 1
        total_generated += scope_count
        print(
            f"generated_scope={scope_name} alphabet={alphabet!r} "
            f"lengths={list(lengths)!r} cases={scope_count}"
        )

    print(f"explicit_cases={len(EXPLICIT_CASES)}")
    print(f"generated_cases={total_generated}")
    print(f"mismatch_count={len(mismatches)}")
    for mismatch in mismatches[:20]:
        print(f"MISMATCH {mismatch!r}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
