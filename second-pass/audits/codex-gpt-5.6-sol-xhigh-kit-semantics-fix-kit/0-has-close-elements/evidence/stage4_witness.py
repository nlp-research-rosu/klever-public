#!/usr/bin/env python3
"""Instantiate the entry theorem's summary and compare both Python implementations."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
from typing import Callable


EntryPoint = Callable[[list[float], float], bool]


def load_entry(path: Path, module_name: str) -> EntryPoint:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, "has_close_elements")


def unfold_has_close(numbers: list[float], threshold: float) -> bool:
    # Direct finite unfolding of closeOuter/closeInner/closeV.
    return any(
        i != j and abs(x - y) < threshold
        for i, x in enumerate(numbers)
        for j, y in enumerate(numbers)
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", required=True, type=Path)
    parser.add_argument("--generated", required=True, type=Path)
    args = parser.parse_args()
    canonical = load_entry(args.canonical, "stage4_canonical")
    generated = load_entry(args.generated, "stage4_generated")

    cases = [
        ("satisfying_close_witness", [1.0, 1.125], 0.25),
        ("strict_false_boundary", [1.0, 1.5], 0.5),
        ("empty_boundary", [], 0.5),
    ]
    mismatch_count = 0
    for label, numbers, threshold in cases:
        claimed = unfold_has_close(numbers, threshold)
        trusted = canonical(numbers, threshold)
        actual = generated(numbers, threshold)
        print(
            f"{label}: numbers={numbers!r} threshold={threshold!r} "
            f"unfolded_hasClose={claimed!r} canonical={trusted!r} generated={actual!r}"
        )
        if not (claimed == trusted == actual):
            mismatch_count += 1
    print(f"mismatch_count={mismatch_count}")
    return 1 if mismatch_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
