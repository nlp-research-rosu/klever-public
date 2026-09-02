#!/usr/bin/env python3
"""Independent differential test for HumanEval 44 candidate vs. canonical."""

from __future__ import annotations

import importlib.util
import pathlib
import random
import sys
from typing import Callable


CANONICAL_PATH = pathlib.Path("/reference/canonical.py")
CANDIDATE_PATH = pathlib.Path(
    "/tmp/audit-work/44-change-base.Cjtazd/candidate-src/solution.py"
)


def load_entry(path: pathlib.Path, module_name: str) -> Callable[[int, int], str]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.change_base


def outcome(function: Callable[[int, int], str], x: int, base: int) -> tuple:
    try:
        return ("return", function(x, base))
    except Exception as error:  # noqa: BLE001 - exceptions are compared as outcomes.
        return ("exception", type(error).__name__, str(error))


def build_cases() -> list[tuple[str, int, int]]:
    cases: list[tuple[str, int, int]] = [
        ("example", 8, 3),
        ("example", 8, 2),
        ("example", 7, 2),
    ]
    for base in range(2, 10):
        for x in (
            0,
            1,
            base - 1,
            base,
            base + 1,
            base * base - 1,
            base * base,
            base * base + 1,
        ):
            cases.append(("branch-boundary", x, base))
    for base in range(2, 10):
        for x in range(0, 65):
            cases.append(("exhaustive-small", x, base))
    rng = random.Random(440044)
    for _ in range(200):
        cases.append(("generated-seed-440044", rng.randrange(0, 10**9), rng.randrange(2, 10)))
    for x in (1234, 10**6, 10**18, 2**100):
        for base in (2, 3, 7, 9):
            cases.append(("representative-large", x, base))
    cases.append(("python-recursion-boundary", 2**900, 2))
    cases.append(("python-recursion-boundary", 2**1100, 2))

    # Deduplicate exact calls while retaining the earliest reason label.
    deduplicated: list[tuple[str, int, int]] = []
    seen: set[tuple[int, int]] = set()
    for reason, x, base in cases:
        if (x, base) not in seen:
            seen.add((x, base))
            deduplicated.append((reason, x, base))
    return deduplicated


def main() -> int:
    canonical = load_entry(CANONICAL_PATH, "trusted_canonical_44")
    candidate = load_entry(CANDIDATE_PATH, "candidate_solution_44")
    cases = build_cases()
    mismatches = 0

    print(f"CANONICAL: {CANONICAL_PATH}")
    print(f"CANDIDATE: {CANDIDATE_PATH}")
    print("DOMAIN: integer x >= 0; integer base in [2, 9]")
    print("GENERATED_SEED: 440044")
    print(f"UNIQUE_CASES: {len(cases)}")
    for index, (reason, x, base) in enumerate(cases, 1):
        expected = outcome(canonical, x, base)
        actual = outcome(candidate, x, base)
        matches = expected == actual
        mismatches += int(not matches)
        print(
            f"CASE {index:04d} reason={reason} x={x} base={base} "
            f"canonical={expected!r} candidate={actual!r} match={matches}"
        )

    print(f"MISMATCHES: {mismatches}")
    return 0 if mismatches == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
