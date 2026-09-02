#!/usr/bin/env python3
"""Ground substitutions for the universal K postcondition."""

from __future__ import annotations

import importlib.util
from collections import Counter
from pathlib import Path
from typing import Callable


def load_entry(path: Path, module_name: str) -> Callable[[list[int]], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.search


def k_search_spec(values: list[int]) -> int:
    """Direct transcription of promote/scan/searchSpec equations."""
    answer = -1
    full = list(values)
    for value in values:
        frequency = sum(1 for item in full if item == value)
        if frequency >= value and value > answer:
            answer = value
    return answer


def contract_oracle(values: list[int]) -> int:
    frequencies = Counter(values)
    qualifiers = [
        value
        for value, frequency in frequencies.items()
        if value > 0 and frequency >= value
    ]
    return max(qualifiers, default=-1)


def main() -> None:
    generated = load_entry(
        Path("/tmp/audit-work/candidate-src/solution.py"),
        "generated_python_ground_69",
    )
    canonical = load_entry(
        Path("/tmp/audit-work/trusted/canonical.py"),
        "canonical_python_ground_69",
    )
    cases = [
        [1],
        [2],
        [2, 2, 1],
        [3, 3, 3],
        [4, 1, 2, 2, 3, 1],
        [1, 2, 2, 3, 3, 3, 4, 4, 4],
        [5, 5, 4, 4, 4],
    ]
    for values in cases:
        head, tail = values[0], values[1:]
        claimed = k_search_spec(values)
        oracle = contract_oracle(values)
        generated_result = generated(list(values))
        canonical_result = canonical(list(values))
        print(
            f"SUBSTITUTION H={head} T={tail} "
            f"claimed_searchSpec={claimed} contract_oracle={oracle} "
            f"generated_python={generated_result} "
            f"canonical_python={canonical_result}"
        )
        assert claimed == oracle == generated_result == canonical_result
    print("GROUND_POSTCONDITION_SUBSTITUTIONS_PASS")


if __name__ == "__main__":
    main()
