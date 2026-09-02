#!/usr/bin/env python3
"""Concrete satisfying witnesses for every submitted SPEC claim."""

from __future__ import annotations

import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


def load_module(path: Path, module_name: str) -> Any:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def before_eq(left: int, right: int) -> bool:
    return (left.bit_count(), left) <= (right.bit_count(), right)


def intended(values: list[int]) -> list[int]:
    return sorted(values, key=lambda value: (value.bit_count(), value))


def record(
    claim: str,
    witness: object,
    precondition: bool,
    actual: object,
    claimed: object,
    canonical: object | None = None,
) -> dict[str, object]:
    item: dict[str, object] = {
        "claim": claim,
        "witness": witness,
        "precondition_satisfied": precondition,
        "actual": actual,
        "claimed": claimed,
        "actual_equals_claimed": actual == claimed,
    }
    if canonical is not None:
        item["trusted_canonical"] = canonical
        item["actual_equals_trusted_canonical"] = actual == canonical
    return item


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: precondition_witnesses.py CANDIDATE.py CANONICAL.py")
        return 64
    candidate = load_module(Path(sys.argv[1]), "candidate_witnesses")
    canonical = load_module(Path(sys.argv[2]), "canonical_witnesses")

    records: list[dict[str, object]] = []
    records.append(
        record(
            "count-correct",
            {"N": -5},
            True,
            candidate.count_ones(-5),
            2,
        )
    )
    records.append(
        record(
            "comparator-correct",
            {"A": 1, "B": 3},
            1 >= 0 and 3 >= 0,
            candidate.comes_before(1, 3),
            before_eq(1, 3),
        )
    )
    records.append(
        record(
            "insert-empty",
            {"X": 3, "values": []},
            True,
            candidate.insert_sorted(3, []),
            [3],
        )
    )
    records.append(
        record(
            "insert-at-front",
            {"X": 1, "Y": 3, "YS": [2]},
            before_eq(1, 3),
            candidate.insert_sorted(1, [3, 2]),
            [1, 3, 2],
        )
    )

    symbolic_sort_cases = [
        ("sort-empty-symbolic", [], True),
        ("sort-singleton-symbolic", [3], True),
        ("sort-pair-before", [1, 3], before_eq(1, 3)),
        ("sort-pair-after", [3, 1], not before_eq(3, 1)),
        (
            "sort-triple-abc",
            [0, 1, 2],
            before_eq(1, 2) and before_eq(0, 1),
        ),
        (
            "sort-triple-bac",
            [2, 1, 4],
            before_eq(1, 4)
            and not before_eq(2, 1)
            and before_eq(2, 4),
        ),
        (
            "sort-triple-bca",
            [4, 1, 2],
            before_eq(1, 2)
            and not before_eq(4, 1)
            and not before_eq(4, 2),
        ),
        (
            "sort-triple-acb",
            [1, 4, 2],
            not before_eq(4, 2) and before_eq(1, 2),
        ),
        (
            "sort-triple-cab",
            [2, 4, 1],
            not before_eq(4, 1)
            and not before_eq(2, 1)
            and before_eq(2, 4),
        ),
        (
            "sort-triple-cba",
            [4, 2, 1],
            not before_eq(2, 1)
            and not before_eq(4, 1)
            and not before_eq(4, 2),
        ),
    ]
    for claim, values, precondition in symbolic_sort_cases:
        records.append(
            record(
                claim,
                {"input": values},
                precondition,
                candidate.sort_array(values.copy()),
                intended(values),
                canonical.sort_array(values.copy()),
            )
        )

    concrete_cases = [
        ("example-one", [1, 5, 2, 3, 4]),
        ("example-three", [1, 0, 2, 3, 4]),
        ("empty", []),
        ("duplicates", [3, 1, 3, 0, 1]),
        ("wide-popcounts", [7, 8, 3, 2, 1, 0]),
        ("negative-extension", [-2, -3, -4, -5, -6]),
    ]
    for claim, values in concrete_cases:
        claimed = (
            intended(values)
            if all(value >= 0 for value in values)
            else sorted(values, key=lambda value: (abs(value).bit_count(), value))
        )
        records.append(
            record(
                claim,
                {"input": values},
                True,
                candidate.sort_array(values.copy()),
                claimed,
                canonical.sort_array(values.copy()),
            )
        )

    ordered_input = [1, 5, 2, 3, 4]
    ordered_output = intended(ordered_input)
    records.append(
        record(
            "example-ordered",
            {"input": ordered_input, "sortModel": ordered_output},
            True,
            all(
                before_eq(ordered_output[index], ordered_output[index + 1])
                for index in range(len(ordered_output) - 1)
            ),
            True,
        )
    )
    records.append(
        record(
            "example-permutation",
            {"input": ordered_input, "sortModel": ordered_output},
            True,
            Counter(ordered_input) == Counter(ordered_output),
            True,
        )
    )

    failures = 0
    for item in records:
        print(json.dumps(item, sort_keys=True))
        if not item["precondition_satisfied"] or not item["actual_equals_claimed"]:
            failures += 1
        if (
            "actual_equals_trusted_canonical" in item
            and not item["actual_equals_trusted_canonical"]
        ):
            failures += 1
    print(f"SUMMARY claims={len(records)} failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
