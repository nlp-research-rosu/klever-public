#!/usr/bin/env python3
"""Independent canonical-versus-candidate differential test for reverse_delete."""

from __future__ import annotations

import importlib.util
import itertools
import pathlib
import random
import sys
from typing import Callable


WORK = pathlib.Path("/tmp/audit-work/reconstruction")


def load_function(path: pathlib.Path, module_name: str) -> Callable[[str, str], tuple[str, bool]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.reverse_delete


def call(function: Callable[[str, str], tuple[str, bool]], s: str, c: str) -> object:
    try:
        return ("return", function(s, c))
    except Exception as error:  # Included so any exception divergence is visible.
        return ("raise", type(error).__name__, str(error))


def main() -> int:
    canonical = load_function(WORK / "canonical.py", "trusted_canonical")
    candidate = load_function(WORK / "solution.py", "generated_solution")

    documented = [
        ("abcde", "ae"),
        ("abcdef", "b"),
        ("abcdedcba", "ab"),
    ]
    boundary_and_branch = [
        ("", ""),
        ("", "x"),
        ("a", ""),
        ("a", "a"),
        ("ab", ""),
        ("aa", ""),
        ("abba", ""),
        ("abc", "xyz"),
        ("aaaa", "a"),
        ("abacaba", "ab"),
        ("abcabc", "ccaa"),
        ("\x00a\x00", "\x00"),
        ("a\nb\na", "\n"),
        ("😀a😀", "a"),
        ("éée\u0301", "é"),
        ("e\u0301", "\u0301"),
    ]

    alphabet = ("a", "b", "😀")
    exhaustive = [
        ("".join(s), "".join(c))
        for s_len in range(0, 6)
        for s in itertools.product(alphabet, repeat=s_len)
        for c_len in range(0, 4)
        for c in itertools.product(alphabet, repeat=c_len)
    ]

    rng = random.Random(112)
    random_alphabet = ["a", "b", "c", "é", "😀", "\x00", "\n", "\u0301"]
    generated = [
        (
            "".join(rng.choice(random_alphabet) for _ in range(rng.randrange(0, 65))),
            "".join(rng.choice(random_alphabet) for _ in range(rng.randrange(0, 17))),
        )
        for _ in range(1000)
    ]
    long_cases = [
        ("ab😀é" * 2500, "bé"),
        ("x" * 10000, "x"),
        ("racecar" * 1000, ""),
    ]

    suites = [
        ("documented", documented),
        ("boundary_and_branch", boundary_and_branch),
        ("exhaustive_small", exhaustive),
        ("generated_seed_112", generated),
        ("long", long_cases),
    ]
    mismatches: list[tuple[str, int, str, str, object, object]] = []
    mismatch_count = 0
    total = 0
    for suite_name, cases in suites:
        suite_mismatches = 0
        for index, (s, c) in enumerate(cases):
            expected = call(canonical, s, c)
            actual = call(candidate, s, c)
            total += 1
            if expected != actual:
                suite_mismatches += 1
                mismatch_count += 1
                if len(mismatches) < 20:
                    mismatches.append((suite_name, index, s, c, expected, actual))
        print(f"{suite_name}: cases={len(cases)} mismatches={suite_mismatches}")

    print(f"total_cases={total}")
    print(f"total_mismatches={mismatch_count}")
    for mismatch in mismatches:
        print("MISMATCH", repr(mismatch))
    if mismatches:
        return 1

    # Explicit expected results independently derived from the written contract.
    expected_examples = [
        (documented[0], ("bcd", False)),
        (documented[1], ("acdef", False)),
        (documented[2], ("cdedc", True)),
    ]
    for (s, c), expected in expected_examples:
        actual = candidate(s, c)
        print(f"example s={s!r} c={c!r} result={actual!r} expected={expected!r}")
        if actual != expected:
            return 1
    print("RESULT: zero mismatches")
    return 0


if __name__ == "__main__":
    sys.exit(main())
