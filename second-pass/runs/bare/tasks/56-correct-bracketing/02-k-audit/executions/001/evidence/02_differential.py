#!/usr/bin/env python3
"""Independent differential test for HumanEval 56.

The oracle is the trusted /reference/canonical.py implementation.  The tested
implementation is the scratch copy of candidate solution.py.  The intended
domain is all finite strings over the two-character alphabet "<>".
"""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path
from types import ModuleType


CANONICAL = Path("/tmp/audit-work/reconstruction/reference/canonical.py")
CANDIDATE = Path("/tmp/audit-work/reconstruction/candidate-src/solution.py")


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    oracle = load_module("trusted_canonical", CANONICAL).correct_bracketing
    generated = load_module("generated_solution", CANDIDATE).correct_bracketing

    documented_and_boundaries = [
        "<",
        "<>",
        "<<><>>",
        "><<>",
        "",
        ">",
        "<<",
        ">>",
        "><",
        "<<>>",
        "<><>",
        "<>>",
        "<<<>>>",
        "<<><>",
    ]

    exhaustive = [
        "".join(chars)
        for length in range(13)
        for chars in itertools.product("<>", repeat=length)
    ]

    rng = random.Random(560056)
    generated_inputs = [
        "".join(rng.choice("<>") for _ in range(rng.randrange(0, 257)))
        for _ in range(2_000)
    ]
    generated_inputs.extend(
        [
            "<" * 512 + ">" * 512,
            "<>" * 512,
            ">" + "<" * 1_024,
            "<" * 1_024,
            ">" * 1_024,
        ]
    )

    cases = documented_and_boundaries + exhaustive + generated_inputs
    mismatches: list[tuple[str, bool, bool]] = []
    for brackets in cases:
        expected = oracle(brackets)
        actual = generated(brackets)
        if type(expected) is not bool or type(actual) is not bool:
            raise AssertionError(
                f"non-boolean result for {brackets!r}: {expected!r}, {actual!r}"
            )
        if expected != actual:
            mismatches.append((brackets, expected, actual))

    print("oracle=/tmp/audit-work/reconstruction/reference/canonical.py")
    print("subject=/tmp/audit-work/reconstruction/candidate-src/solution.py")
    print("domain=finite strings over '<' and '>'")
    print(f"documented_and_boundary_cases={len(documented_and_boundaries)}")
    print("exhaustive_lengths=0..12")
    print(f"exhaustive_cases={len(exhaustive)}")
    print("deterministic_random_seed=560056")
    print(f"generated_cases={len(generated_inputs)}")
    print(f"total_comparisons={len(cases)}")
    print(f"mismatches={len(mismatches)}")
    for brackets in documented_and_boundaries:
        print(
            f"case={brackets!r} canonical={oracle(brackets)!r} "
            f"candidate={generated(brackets)!r}"
        )
    for mismatch in mismatches[:20]:
        print(f"mismatch={mismatch!r}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
