#!/usr/bin/env python3
"""Independent differential oracle for HumanEval 117-select-words."""

from __future__ import annotations

import importlib.util
import itertools
import random
import string
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    canonical = load_module(
        "trusted_canonical", Path("/tmp/audit-work/fresh/trusted/canonical.py")
    )
    candidate = load_module(
        "submitted_solution", Path("/tmp/audit-work/fresh/solution.py")
    )

    documented_and_boundaries = [
        ("Mary had a little lamb", 4),
        ("Mary had a little lamb", 3),
        ("simple white space", 2),
        ("Hello world", 4),
        ("Uncle sam", 3),
        ("", 0),
        ("", 1),
        (" ", 0),
        ("     ", 0),
        ("  a  b  ", 0),
        ("  a  b  ", 1),
        ("aeiou AEIOU", 0),
        ("bcdfg XYZ", 3),
        ("bcdfg XYZ", 5),
        ("a b c d", 1),
        ("a b c d", 2),
        ("Aba BAB bbb", 1),
        ("Aba BAB bbb", 2),
        ("Aba BAB bbb", 3),
        ("x" * 200 + " " + "a" * 200, 0),
        ("x" * 200 + " " + "a" * 200, 200),
        ("é", 0),
        ("é", 1),
        ("É İ Ω Ж 你", 1),
    ]

    mismatch_count = 0
    case_count = 0

    def check(s: str, n: int, origin: str) -> None:
        nonlocal mismatch_count, case_count
        expected = canonical.select_words(s, n)
        actual = candidate.select_words(s, n)
        case_count += 1
        if actual != expected:
            mismatch_count += 1
            if mismatch_count <= 20:
                print(
                    f"MISMATCH origin={origin} s={s!r} n={n} "
                    f"canonical={expected!r} candidate={actual!r}"
                )

    for s, n in documented_and_boundaries:
        check(s, n, "documented-or-boundary")

    exhaustive_strings = 0
    alphabet = "aAbB "
    for length in range(7):
        for letters in itertools.product(alphabet, repeat=length):
            s = "".join(letters)
            exhaustive_strings += 1
            for n in range(8):
                check(s, n, "exhaustive-aAbB-space-length-0-through-6")

    rng = random.Random(117)
    random_cases = 5_000
    random_alphabet = string.ascii_letters + " "
    for _ in range(random_cases):
        length = rng.randrange(0, 81)
        s = "".join(rng.choice(random_alphabet) for _ in range(length))
        n = rng.randrange(0, 31)
        check(s, n, "seeded-random-ascii-letters-and-space")

    unicode_random_cases = 1_000
    unicode_alphabet = "aéÉİΩЖ你 "
    for _ in range(unicode_random_cases):
        length = rng.randrange(0, 21)
        s = "".join(rng.choice(unicode_alphabet) for _ in range(length))
        n = rng.randrange(0, 11)
        check(s, n, "seeded-random-unicode-letters-and-space")

    print(f"documented_and_boundary_cases={len(documented_and_boundaries)}")
    print(f"exhaustive_alphabet={alphabet!r}")
    print("exhaustive_lengths=0..6")
    print("exhaustive_n=0..7")
    print(f"exhaustive_strings={exhaustive_strings}")
    print(f"seeded_random_seed=117")
    print(f"seeded_random_cases={random_cases}")
    print("seeded_random_lengths=0..80")
    print("seeded_random_n=0..30")
    print(f"seeded_unicode_random_alphabet={unicode_alphabet!r}")
    print(f"seeded_unicode_random_cases={unicode_random_cases}")
    print("seeded_unicode_random_lengths=0..20")
    print("seeded_unicode_random_n=0..10")
    print(f"total_cases={case_count}")
    print(f"mismatch_count={mismatch_count}")
    return 1 if mismatch_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
