#!/usr/bin/env python3
"""Independently compare trusted HumanEval/60 and candidate entry points."""

from __future__ import annotations

import importlib.util
import json
import random
import sys
from pathlib import Path
from types import ModuleType


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    if len(sys.argv) != 4:
        print(
            f"usage: {sys.argv[0]} CANONICAL.py SOLUTION.py INPUTS.json",
            file=sys.stderr,
        )
        return 64

    canonical_path = Path(sys.argv[1]).resolve()
    solution_path = Path(sys.argv[2]).resolve()
    inputs_path = Path(sys.argv[3]).resolve()
    input_spec = json.loads(inputs_path.read_text(encoding="utf-8"))

    rng = random.Random(input_spec["generated_seed"])
    generated = [
        rng.randint(input_spec["generated_min"], input_spec["generated_max"])
        for _ in range(input_spec["generated_count"])
    ]
    groups = [
        ("documented_examples", input_spec["documented_examples"]),
        ("empty_and_boundaries", input_spec["empty_and_boundaries"]),
        ("representative", input_spec["representative"]),
        ("generated", generated),
    ]

    canonical = load_module("trusted_canonical_60", canonical_path)
    candidate = load_module("candidate_solution_60", solution_path)

    mismatches: list[tuple[str, int, object, object]] = []
    tested = 0
    print(f"ORACLE={canonical_path}")
    print(f"CANDIDATE={solution_path}")
    print(f"INPUT_SPEC={inputs_path}")
    for group_name, values in groups:
        print(f"GROUP {group_name} COUNT {len(values)} VALUES {values}")
        for n in values:
            expected = canonical.sum_to_n(n)
            actual = candidate.sum_to_n(n)
            status = "MATCH" if actual == expected else "MISMATCH"
            print(
                f"{status} group={group_name} n={n} "
                f"canonical={expected} candidate={actual}"
            )
            tested += 1
            if actual != expected:
                mismatches.append((group_name, n, expected, actual))

    nonnegative_mismatches = [row for row in mismatches if row[1] >= 0]
    negative_mismatches = [row for row in mismatches if row[1] < 0]
    print(f"TOTAL_TESTS={tested}")
    print(f"TOTAL_MISMATCHES={len(mismatches)}")
    print(f"NONNEGATIVE_MISMATCHES={len(nonnegative_mismatches)}")
    print(f"NEGATIVE_MISMATCHES={len(negative_mismatches)}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
