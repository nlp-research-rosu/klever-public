#!/usr/bin/env python3
"""Concrete substitutions for the K entry claims and loop invariant."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, Path(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sum_squares


def contribution(value: int, index: int) -> int:
    if index % 3 == 0:
        return value * value
    if index % 4 == 0:
        return value * value * value
    return value


def claimed_sum_from(values: list[int], index: int) -> int:
    if not values:
        return 0
    return contribution(values[0], index) + claimed_sum_from(values[1:], index + 1)


def main() -> int:
    if len(sys.argv) != 3:
        return 64
    canonical = load(sys.argv[1], "witness_canonical")
    generated = load(sys.argv[2], "witness_generated")

    entry_cases = [[], [2], [2, 2, 2, 2, 2], [2] * 13, [-1, -5, 2, -1, -5]]
    for values in entry_cases:
        claimed = claimed_sum_from(values, 0)
        trusted = canonical(list(values))
        actual = generated(list(values))
        print(f"ENTRY input={values!r} claimed={claimed} canonical={trusted} generated={actual}")
        assert claimed == trusted == actual

    # A concrete state satisfying SPEC.loop-invariant's precondition.
    # Reachable after four iterations from ALL=[1,1,1,1,2,-3,4]:
    # L=1; IS=[2,-3,4]; ACC=4; INDEX=4; OLD=1; scope parent=0.
    # The claim predicts total=25 and index=7.
    suffix = [2, -3, 4]
    acc = 4
    index = 4
    final_total = acc + claimed_sum_from(suffix, index)
    final_index = index + len(suffix)
    print(
        "LOOP_WITNESS "
        f"L=1 ALL={[1, 1, 1, 1, 2, -3, 4]!r} IS={suffix!r} ACC={acc} INDEX={index} OLD=1 "
        f"predicted_total={final_total} predicted_index={final_index}"
    )
    assert (final_total, final_index) == (25, 7)
    print("CLAIM_WITNESSES_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
