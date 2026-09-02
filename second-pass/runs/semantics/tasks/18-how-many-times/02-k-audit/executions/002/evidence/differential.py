#!/usr/bin/env python3
"""Independent differential check: trusted canonical vs generated solution."""

from __future__ import annotations

import importlib.util
import itertools
import random
import sys
from pathlib import Path
from typing import Callable


SCRATCH = Path("/tmp/audit-work/fresh")


def load_entry(module_name: str, path: Path) -> Callable[[str, str], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.how_many_times


def outcome(function: Callable[[str, str], int], string: str, substring: str):
    try:
        return ("return", function(string, substring))
    except BaseException as error:
        return ("raise", type(error).__name__, str(error))


def all_words(alphabet: str, maximum_length: int):
    for length in range(maximum_length + 1):
        for letters in itertools.product(alphabet, repeat=length):
            yield "".join(letters)


def main() -> int:
    canonical = load_entry("trusted_canonical", SCRATCH / "canonical.py")
    generated = load_entry("generated_solution", SCRATCH / "solution.py")

    cases: list[tuple[str, str, str]] = [
        ("example-empty-source", "", "a"),
        ("example-single-pattern", "aaa", "a"),
        ("example-overlap", "aaaa", "aa"),
        ("empty-empty", "", ""),
        ("empty-pattern", "abc", ""),
        ("source-empty-pattern-nonempty", "", "abc"),
        ("first-prefix-true", "abc", "ab"),
        ("first-prefix-false-later-true", "zabc", "ab"),
        ("pattern-longer", "ab", "abcd"),
        ("self-overlap", "abababa", "aba"),
        ("equal", "boundary", "boundary"),
        ("unicode-codepoints", "αβαβα", "αβα"),
        ("emoji", "🙂🙂🙂", "🙂🙂"),
        ("nul-codepoint", "a\u0000a\u0000a", "\u0000a"),
    ]

    exhaustive_strings = list(all_words("ab", 6))
    exhaustive_patterns = list(all_words("ab", 4))
    for string in exhaustive_strings:
        for substring in exhaustive_patterns:
            cases.append(("exhaustive-ab", string, substring))

    rng = random.Random(180026)
    alphabet = "abcα🙂"
    for _ in range(1000):
        string = "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 81)))
        substring = "".join(
            rng.choice(alphabet) for _ in range(rng.randrange(0, 13))
        )
        cases.append(("generated-seeded", string, substring))

    # These are ordinary values in the unrestricted `str, str` source domain.
    # They probe whether the recursive rewrite agrees with the iterative
    # canonical entry point beyond CPython's default recursion depth.
    cases.extend(
        [
            ("long-recursion-match", "a" * 1200, "a"),
            ("long-recursion-no-match", "a" * 1200, "z"),
            ("long-empty-pattern-direct", "a" * 1200, ""),
        ]
    )

    mismatches = []
    category_counts: dict[str, int] = {}
    for category, string, substring in cases:
        category_counts[category] = category_counts.get(category, 0) + 1
        expected = outcome(canonical, string, substring)
        actual = outcome(generated, string, substring)
        if expected != actual:
            mismatches.append((category, string, substring, expected, actual))

    print(f"python={sys.version.split()[0]}")
    print(f"recursion_limit={sys.getrecursionlimit()}")
    print(f"total_cases={len(cases)}")
    print(f"category_counts={category_counts}")
    print(f"mismatch_count={len(mismatches)}")
    for index, (category, string, substring, expected, actual) in enumerate(
        mismatches, 1
    ):
        bounded_string = (
            repr(string)
            if len(string) <= 100
            else repr(string[:40]) + f"...(length={len(string)})"
        )
        print(
            f"MISMATCH {index}: category={category} "
            f"string={bounded_string} substring={substring!r} "
            f"canonical={expected!r} generated={actual!r}"
        )
    return 0 if not mismatches else 1


if __name__ == "__main__":
    raise SystemExit(main())
