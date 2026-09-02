#!/usr/bin/env python3
"""Concrete witnesses for the entry claim and its structural result summaries."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load(Path("/reference/canonical.py"), "witness_canonical")
candidate = load(Path("/tmp/audit-work/source/solution.py"), "witness_candidate")


def int_list_term(values: list[int]) -> str:
    term = ".IntList"
    for value in reversed(values):
        term = f"intCons({value}, {term})"
    return term


def sum_from(accumulator: int, values: list[int]) -> int:
    for value in values:
        accumulator += value
    return accumulator


def product_from(accumulator: int, values: list[int]) -> int:
    for value in values:
        accumulator *= value
    return accumulator


def last_from(previous: int, values: list[int]) -> int:
    for value in values:
        previous = value
    return previous


witnesses = [[], [2, -3], [0, 5, -2]]
for values in witnesses:
    summary = (sum_from(0, values), product_from(1, values))
    expected = canonical.sum_product(list(values))
    actual = candidate.sum_product(list(values))
    print(f"INPUT={values!r}")
    print(f"  K_INPUT={int_list_term(values)}")
    print(f"  CLAIM_RESULT=tuple(vCons({summary[0]}, vCons({summary[1]}, .ValSeq)))")
    print(f"  CANONICAL={expected!r}")
    print(f"  CANDIDATE={actual!r}")
    print(f"  LOOP_LAST_FROM_0={last_from(0, values)}")
    assert summary == expected == actual

print("ALL_WITNESSES_MATCH=PASS")
