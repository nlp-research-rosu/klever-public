#!/usr/bin/env python3
"""Instantiate the formal fold result and compare it with both Python entries."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sum_from(accumulator: int, values: list[int]) -> int:
    for value in values:
        accumulator += value
    return accumulator


def product_from(accumulator: int, values: list[int]) -> int:
    for value in values:
        accumulator *= value
    return accumulator


def int_list(values: list[int]) -> str:
    result = ".IntList"
    for value in reversed(values):
        result = f"iList({value}, {result})"
    return result


def main() -> int:
    canonical = load("substitution_canonical", Path("/reference/canonical.py"))
    generated = load("substitution_generated", Path("/tmp/audit-work/solution.py"))
    cases = [[], [1, 2, 3, 4], [-2, 3, 0], [10**30, -2]]
    mismatches = 0
    for values in cases:
        claimed = (sum_from(0, values), product_from(1, values))
        canonical_result = canonical.sum_product(values.copy())
        generated_result = generated.sum_product(values.copy())
        equal = claimed == canonical_result == generated_result
        mismatches += not equal
        print(
            f"XS={int_list(values)} claimed={claimed!r} "
            f"canonical={canonical_result!r} generated={generated_result!r} equal={equal}"
        )
    print(f"cases={len(cases)} mismatches={mismatches}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
