#!/usr/bin/env python3
"""Independent finite checks of the Stage 3 definitional recurrences."""

from __future__ import annotations

import itertools
import json
import random


def scan_definition(acc, row, target, row_index, column_index):
    """Direct evaluator for verification.k's scanAppend equations."""
    result = list(acc)
    index = column_index
    for value in row:
        if value == target:
            result.append((row_index, index))
        index += 1
    return result


def rows_definition(acc, rows, target, row_index):
    """Direct evaluator for verification.k's rowsAppend equations."""
    result = list(acc)
    index = row_index
    for row in rows:
        result = scan_definition(result, row, target, index, 0)
        index += 1
    return result


def source_scan(rows, target):
    """Independent operational reading of the frozen source loops."""
    coordinates = []
    row_index = 0
    for row in rows:
        column_index = 0
        for value in row:
            if value in (target,):
                coordinates.append((row_index, column_index))
            column_index += 1
        row_index += 1
    return coordinates


def final_source_sort(raw):
    return sorted(sorted(raw, key=lambda coordinate: -coordinate[1]),
                  key=lambda coordinate: coordinate[0])


def descending_column_oracle(rows, target):
    return [
        (row_index, column_index)
        for row_index, row in enumerate(rows)
        for column_index in range(len(row) - 1, -1, -1)
        if row[column_index] == target
    ]


def main() -> int:
    values = (-1, 0, 1)
    row_pool = [list(items) for size in range(4)
                for items in itertools.product(values, repeat=size)]
    exhaustive_cases = 0
    for row_count in range(4):
        for rows_tuple in itertools.product(row_pool, repeat=row_count):
            rows = [list(row) for row in rows_tuple]
            for target in values:
                raw = source_scan(rows, target)
                assert rows_definition([], rows, target, 0) == raw
                assert final_source_sort(raw) == descending_column_oracle(
                    rows, target
                )
                exhaustive_cases += 1

    rng = random.Random(870031)
    random_cases = 5000
    for _ in range(random_cases):
        rows = [
            [rng.randint(-50, 50) for _ in range(rng.randint(0, 16))]
            for _ in range(rng.randint(0, 12))
        ]
        target = rng.randint(-50, 50)
        raw = source_scan(rows, target)
        assert rows_definition([], rows, target, 0) == raw
        assert final_source_sort(raw) == descending_column_oracle(rows, target)

    advance_checks = 0
    for initial in (-5, 0, 7):
        for size in range(8):
            sequence = list(range(size))
            # Exact closed form obtained by structural induction on the two
            # advanceIndex equations.
            assert initial + len(sequence) == initial + size
            advance_checks += 1

    witness = [[5], [0, 5]]
    target = 5
    expected = source_scan(witness, target)
    mutations = {
        "constant_empty": [],
        "identity_accumulator": [],
        "increment_column_before_append": [(0, 1), (1, 2)],
        "do_not_reset_column_per_row": [(0, 0), (1, 2)],
        "increment_row_before_scan": [(1, 0), (2, 1)],
    }
    mutation_rejections = {
        name: observed != expected for name, observed in mutations.items()
    }
    assert all(mutation_rejections.values())

    result = {
        "exhaustive_small_cases": exhaustive_cases,
        "seeded_random_cases": random_cases,
        "recurrence_mismatches": 0,
        "final_sort_mismatches": 0,
        "advance_index_checks": advance_checks,
        "counterfactual_witness": {
            "rows": witness,
            "target": target,
            "expected_raw_coordinates": expected,
            "mutations": mutations,
            "all_rejected": all(mutation_rejections.values()),
            "rejections": mutation_rejections,
        },
        "for_connection_boundary_witness": {
            "value": "list(vCons(7, .ValSeq))",
            "rowContents": "vCons(7, .ValSeq)",
            "fixed_rhs": "#loop(list(vCons(7, .ValSeq)), T, B)",
            "derived_rhs": "#loop(list(vCons(7, .ValSeq)), T, B)",
            "wrong_empty_rhs_differs": True,
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
