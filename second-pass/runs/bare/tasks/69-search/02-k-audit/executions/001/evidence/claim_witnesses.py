#!/usr/bin/env python3
"""Ground substitutions for the universal K entry claim."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Callable


def load_search(path: Path, name: str) -> Callable[[list[int]], int]:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.search


def count(item: int, values: list[int]) -> int:
    return sum(1 for value in values if value == item)


def promote(full: list[int], item: int, answer: int) -> int:
    return item if count(item, full) >= item and item > answer else answer


def scan(full: list[int], remaining: list[int], answer: int) -> int:
    for item in remaining:
        answer = promote(full, item, answer)
    return answer


def int_seq(values: list[int]) -> str:
    result = ".Ints"
    for value in reversed(values):
        result = f"cons({value}, {result})"
    return result


def main() -> int:
    canonical = load_search(
        Path("/tmp/audit-work/69-search-audit/trusted/canonical.py"),
        "claim_witness_canonical",
    )
    candidate = load_search(
        Path("/tmp/audit-work/69-search-audit/src/solution.py"),
        "claim_witness_candidate",
    )
    cases = [
        [1],
        [1, 2, 2],
        [4, 1, 2, 2, 3, 1],
        [5, 5, 4, 4, 4],
    ]
    failures = []
    records = []
    for values in cases:
        formal_value = scan(values, values, -1)
        candidate_value = candidate(values.copy())
        canonical_value = canonical(values.copy())
        record = {
            "satisfying_initial_state": {
                "k": "boot",
                "program": "searchProgram",
                "input": f"VList({int_seq(values)})",
                "env": ".Map",
                "result": "noResult",
            },
            "substitution": {"H": values[0], "T": values[1:]},
            "claimed_searchSpec_value": formal_value,
            "candidate_python": candidate_value,
            "canonical_python": canonical_value,
            "all_equal": formal_value == candidate_value == canonical_value,
        }
        records.append(record)
        if not record["all_equal"]:
            failures.append(record)
    print(json.dumps({"witnesses": records, "failure_count": len(failures)}, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
