#!/usr/bin/env python3
"""Independent differential test for HumanEval/98.

The oracle is the trusted canonical implementation.  The candidate is imported
from the clean source copy, not from /candidate or its bytecode cache.
"""

from __future__ import annotations

import importlib.util
import itertools
import random
import sys
from pathlib import Path
from types import ModuleType
from typing import Callable


SCRATCH = Path("/tmp/audit-work/98-count-upper-audit-20260726")


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def outcome(function: Callable[[str], int], value: str) -> tuple[str, object]:
    try:
        return ("return", function(value))
    except BaseException as error:  # An exception is an observable divergence.
        return ("raise", type(error).__name__)


def main() -> int:
    canonical = load_module("trusted_canonical", SCRATCH / "canonical.py")
    generated = load_module("generated_solution", SCRATCH / "solution.py")

    documented = [
        ("aBCdEf", 1),
        ("abcdefg", 0),
        ("dBBE", 0),
    ]
    boundaries = [
        ("", 0),
        ("A", 1),
        ("E", 1),
        ("Z", 0),
        ("a", 0),
        ("xA", 0),
        ("Ax", 1),
        ("xAx", 0),
        ("xXA", 1),
        ("AEIOU", 3),
        ("aEiOu", 0),
        ("😀A😀E", 0),
        ("A😀E😀", 2),
        ("ÀÉÎÖÜ", 0),
    ]

    cases: list[tuple[str, str, int | None]] = []
    cases.extend(("documented", value, expected) for value, expected in documented)
    cases.extend(("boundary", value, expected) for value, expected in boundaries)

    alphabet = ("A", "E", "U", "Z", "a", "😀")
    for length in range(0, 6):
        for chars in itertools.product(alphabet, repeat=length):
            cases.append(("exhaustive-length-0-through-5", "".join(chars), None))

    generator = random.Random(980026)
    random_alphabet = "AEIOUZaeiouxyz09😀é"
    for _ in range(300):
        length = generator.randrange(0, 121)
        value = "".join(generator.choice(random_alphabet) for _ in range(length))
        cases.append(("deterministic-random-length-0-through-120", value, None))

    # The prompt has no length bound.  These cases cross CPython's default
    # recursion-depth boundary for the candidate's two-character recursion.
    cases.extend(
        [
            ("unrestricted-domain-long", "a" * 1995, None),
            ("unrestricted-domain-long", "A" * 2001, None),
            ("unrestricted-domain-long", ("aA" * 1100), None),
        ]
    )

    mismatches: list[tuple[str, str, tuple[str, object], tuple[str, object]]] = []
    expectation_errors: list[tuple[str, int, tuple[str, object]]] = []
    category_counts: dict[str, int] = {}
    for category, value, expected in cases:
        category_counts[category] = category_counts.get(category, 0) + 1
        canonical_outcome = outcome(canonical.count_upper, value)
        generated_outcome = outcome(generated.count_upper, value)
        if expected is not None and canonical_outcome != ("return", expected):
            expectation_errors.append((value, expected, canonical_outcome))
        if canonical_outcome != generated_outcome:
            mismatches.append((category, value, canonical_outcome, generated_outcome))

    print(f"python={sys.version.split()[0]}")
    print(f"recursion_limit={sys.getrecursionlimit()}")
    print(f"total_cases={len(cases)}")
    for category, count in sorted(category_counts.items()):
        print(f"category[{category}]={count}")
    print(f"documented_expectation_errors={len(expectation_errors)}")
    print(f"mismatch_count={len(mismatches)}")
    for category, value, expected, actual in mismatches[:20]:
        display = repr(value) if len(value) <= 80 else repr(value[:40]) + f"...(len={len(value)})"
        print(
            f"MISMATCH category={category} input={display} "
            f"canonical={expected!r} generated={actual!r}"
        )
    return 1 if expectation_errors or mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
