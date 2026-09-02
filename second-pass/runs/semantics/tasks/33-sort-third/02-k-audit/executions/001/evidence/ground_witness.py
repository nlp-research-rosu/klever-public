#!/usr/bin/env python3
"""Concrete satisfiability/result witness for the entry claim."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


WORK = Path("/tmp/audit-work/audit-33-sort-third")
INPUT = [5, 6, 3, 4, 8, 9, 2]


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_third


def oracle(values: list[int]) -> list[int]:
    result = list(values)
    indices = list(range(0, len(values), 3))
    replacements = sorted(values[index] for index in indices)
    for index, replacement in zip(indices, replacements):
        result[index] = replacement
    return result


def val_seq(values: list[int]) -> str:
    term = ".ValSeq"
    for value in reversed(values):
        term = f"vCons({value}, {term})"
    return term


def main() -> int:
    canonical = load(WORK / "canonical.py", "witness_canonical")
    generated = load(WORK / "solution.py", "witness_generated")
    expected = oracle(INPUT)
    canonical_result = canonical(INPUT)
    generated_result = generated(INPUT)
    result = {
        "entry_requires": "true (the entry claim has no requires clause)",
        "formal_INPUT_substitution": val_seq(INPUT),
        "formal_claimed_heap_location_2": f"list(sortThird({val_seq(INPUT)}))",
        "concrete_expected_ValSeq": val_seq(expected),
        "input": INPUT,
        "independent_oracle": expected,
        "trusted_canonical": canonical_result,
        "submitted_generated": generated_result,
        "all_equal": expected == canonical_result == generated_result,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["all_equal"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
