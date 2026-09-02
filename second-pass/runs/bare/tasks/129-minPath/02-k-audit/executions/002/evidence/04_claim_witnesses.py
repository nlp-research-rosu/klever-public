#!/usr/bin/env python3
"""Exhibit a concrete satisfying state for all eleven entry claims."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


sys.dont_write_bytecode = True
OUTPUT = Path("/audit-output/evidence/04_claim_witnesses.json")


def load(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.minPath


def valid_tail(a: int, b: int, c: int) -> bool:
    return (
        2 <= a <= 4
        and 2 <= b <= 4
        and 2 <= c <= 4
        and len({a, b, c}) == 3
    )


def path5(m: int) -> list[int]:
    return [1, m, 1, m, 1]


def main() -> None:
    canonical = load("witness_canonical", Path("/reference/canonical.py"))
    generated = load(
        "witness_generated", Path("/tmp/audit-work/candidate-src/solution.py")
    )
    claims = [
        (1, [[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3, [1, 2, 1], "fixed"),
        (2, [[5, 9, 3], [4, 1, 6], [7, 8, 2]], 1, [1], "fixed"),
        (3, [[5, 9, 3], [4, 1, 6], [7, 8, 2]], 6, [1, 4, 1, 4, 1, 4], "fixed"),
    ]
    symbolic_shapes = [
        (4, lambda a, b, c: [[1, a], [b, c]], "a_lt_b"),
        (5, lambda a, b, c: [[1, a], [b, c]], "b_lt_a"),
        (6, lambda a, b, c: [[a, 1], [c, b]], "a_lt_b"),
        (7, lambda a, b, c: [[a, 1], [c, b]], "b_lt_a"),
        (8, lambda a, b, c: [[a, c], [1, b]], "a_lt_b"),
        (9, lambda a, b, c: [[a, c], [1, b]], "b_lt_a"),
        (10, lambda a, b, c: [[c, a], [b, 1]], "a_lt_b"),
        (11, lambda a, b, c: [[c, a], [b, 1]], "b_lt_a"),
    ]
    for number, shape, ordering in symbolic_shapes:
        if ordering == "a_lt_b":
            a, b, c = 2, 3, 4
            selected = a
            ordering_holds = a < b
        else:
            a, b, c = 3, 2, 4
            selected = b
            ordering_holds = b < a
        assert valid_tail(a, b, c) and ordering_holds
        claims.append(
            (
                number,
                shape(a, b, c),
                5,
                path5(selected),
                f"A={a},B={b},C={c};validTail=true;{ordering}=true",
            )
        )

    records = []
    for number, grid, k, expected, precondition in claims:
        generated_value = generated(grid, k)
        canonical_value = canonical(grid, k)
        record = {
            "claim": number,
            "precondition_witness": precondition,
            "grid": grid,
            "k": k,
            "claimed_result": expected,
            "generated_result": generated_value,
            "canonical_result": canonical_value,
            "all_equal": expected == generated_value == canonical_value,
        }
        records.append(record)
        print(json.dumps(record, sort_keys=True))
        assert record["all_equal"]
    OUTPUT.write_text(json.dumps(records, indent=2, sort_keys=True) + "\n")
    print(f"witnesses={len(records)}")
    print(f"output={OUTPUT}")
    print("ALL_ENTRY_PRECONDITIONS_SATISFIABLE")


if __name__ == "__main__":
    main()
