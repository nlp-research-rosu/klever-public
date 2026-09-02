#!/usr/bin/env python3
"""Independent differential audit for HumanEval 19.

The trusted canonical module and candidate solution are loaded from explicit
paths under distinct module names.  Inputs contain only the ten documented
number words and ASCII space delimiters, including empty and repeated-space
boundaries.  The generated sample uses a fixed seed.
"""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path
from types import ModuleType

WORDS = (
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
)


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def outcome(module: ModuleType, value: str) -> dict[str, str]:
    try:
        return {"kind": "return", "value": module.sort_numbers(value)}
    except Exception as exc:  # Included so any behavioral divergence is visible.
        return {"kind": "exception", "value": f"{type(exc).__name__}: {exc}"}


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: differential_check.py TRUSTED_CANONICAL CANDIDATE_SOLUTION")
        return 64

    canonical = load_module("trusted_canonical", Path(sys.argv[1]))
    candidate = load_module("candidate_solution", Path(sys.argv[2]))

    labeled: list[tuple[str, str]] = [
        ("documented-example", "three one five"),
        ("empty", ""),
        ("one-space", " "),
        ("many-spaces", "     "),
        ("leading-trailing", "  three one five  "),
        ("repeated-delimiters", "nine  zero   five"),
        ("ascending-all", " ".join(WORDS)),
        ("descending-all", " ".join(reversed(WORDS))),
        ("duplicate-low", "zero zero zero"),
        ("duplicate-high", "nine nine nine"),
        ("alternating-extremes", "nine zero nine zero nine zero"),
        ("every-helper-branch", " ".join(reversed(WORDS + WORDS))),
    ]

    # Exhaustive token tuples of lengths 0, 1, and 2 cover every helper branch
    # alone and in every ordered pair.
    for length in range(3):
        for index, tokens in enumerate(itertools.product(WORDS, repeat=length)):
            labeled.append((f"exhaustive-len-{length}-{index}", " ".join(tokens)))

    rng = random.Random(190019)
    for index in range(256):
        length = rng.randint(3, 16)
        tokens = [rng.choice(WORDS) for _ in range(length)]
        # Generated inputs remain in the intended space-delimited domain, with
        # occasional extra ASCII spaces that the canonical implementation
        # explicitly removes.
        delimiter = " " * rng.randint(1, 4)
        prefix = " " * rng.randint(0, 2)
        suffix = " " * rng.randint(0, 2)
        labeled.append((f"generated-{index}", prefix + delimiter.join(tokens) + suffix))

    seen: set[str] = set()
    cases: list[tuple[str, str]] = []
    for label, value in labeled:
        if value not in seen:
            seen.add(value)
            cases.append((label, value))

    mismatches = 0
    print(
        json.dumps(
            {
                "oracle": str(Path(sys.argv[1]).resolve()),
                "candidate": str(Path(sys.argv[2]).resolve()),
                "seed": 190019,
                "case_count": len(cases),
                "domain": "ten documented words separated by zero or more ASCII spaces",
            },
            sort_keys=True,
        )
    )
    for index, (label, value) in enumerate(cases):
        expected = outcome(canonical, value)
        actual = outcome(candidate, value)
        matched = expected == actual
        mismatches += int(not matched)
        print(
            json.dumps(
                {
                    "actual": actual,
                    "expected": expected,
                    "index": index,
                    "input": value,
                    "label": label,
                    "match": matched,
                },
                ensure_ascii=True,
                sort_keys=True,
            )
        )

    print(json.dumps({"mismatches": mismatches, "tested": len(cases)}, sort_keys=True))
    return int(mismatches != 0)


if __name__ == "__main__":
    raise SystemExit(main())
