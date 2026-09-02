#!/usr/bin/env python3
"""Independent differential test for HumanEval/98 over the intended str domain."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/reconstruction")


def load(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    canonical = load(SCRATCH / "canonical.py", "trusted_canonical")
    generated = load(SCRATCH / "solution.py", "generated_solution")

    documented = [
        ("aBCdEf", 1),
        ("abcdefg", 0),
        ("dBBE", 0),
    ]
    boundaries = [
        ("", 0),
        ("A", 1),
        ("B", 0),
        ("a", 0),
        ("AA", 1),
        ("BA", 0),
        ("AB", 1),
        ("BAA", 1),
        ("ABA", 2),
        ("AAAA", 2),
        ("AEIOU", 3),
        ("AaEeIiOoUu", 5),
        ("ÅE𝔸I🙂O", 0),
        ("\x00A\nE", 0),
    ]

    checked = 0
    mismatches: list[tuple[str, object, object]] = []

    def check(value: str, explicit: int | None = None) -> None:
        nonlocal checked
        trusted = canonical.count_upper(value)
        candidate = generated.count_upper(value)
        checked += 1
        if trusted != candidate or (explicit is not None and trusted != explicit):
            mismatches.append((repr(value), trusted, candidate))

    for value, expected in documented + boundaries:
        check(value, expected)

    # Exhaust every length through 6 over categories that distinguish the branch:
    # uppercase vowel/non-vowel, lowercase vowel, digit, NUL, non-ASCII uppercase,
    # astral Unicode letter, and an unrelated symbol.
    alphabet = ("A", "E", "Z", "a", "0", "\x00", "Å", "𝔸", "🙂")
    exhaustive_count = 0
    for length in range(7):
        for chars in itertools.product(alphabet, repeat=length):
            check("".join(chars))
            exhaustive_count += 1

    rng = random.Random(980026)
    random_alphabet = (
        "AEIOU"
        "BCDFG"
        "aeiou"
        "xyz"
        "019"
        " \t\n"
        "ÅÉÖΩЖ中🙂𝔸"
        "\x00"
    )
    random_count = 10_000
    for _ in range(random_count):
        length = rng.randrange(0, 129)
        check("".join(rng.choice(random_alphabet) for _ in range(length)))

    print(f"documented_count={len(documented)}")
    print(f"boundary_count={len(boundaries)}")
    print(f"exhaustive_alphabet={alphabet!r}")
    print("exhaustive_lengths=0..6")
    print(f"exhaustive_count={exhaustive_count}")
    print(f"random_seed=980026")
    print("random_lengths=0..128")
    print(f"random_count={random_count}")
    print(f"total_checked={checked}")
    print(f"mismatch_count={len(mismatches)}")
    for mismatch in mismatches[:20]:
        print(f"MISMATCH {mismatch!r}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
