#!/usr/bin/env python3
"""Independent CPython differential test for HumanEval 118."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
from pathlib import Path
import random
import string
import sys


SCRATCH = Path("/tmp/audit-work/reconstruction")
INPUT_RECORD = Path("/audit-output/evidence/differential_inputs.txt")


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_closest_vowel


def build_cases() -> list[str]:
    documented_and_boundaries = [
        "yogurt",
        "FULL",
        "quick",
        "ab",
        "",
        "a",
        "b",
        "aa",
        "ba",
        "bab",
        "bAb",
        "aba",
        "bbb",
        "be",
        "bed",
        "beat",
        "baed",
        "BAZZE",
        "abecid",
        "baced",
        "zzAzzEzz",
        "xAy",
        "xay",
        "aXa",
        "xAE",
        "AEz",
        "zEA",
    ]

    # Exhaust every string through length five over a branch-sensitive alphabet:
    # lowercase/uppercase vowels and consonants, including y.
    small_alphabet = "abEyZ"
    exhaustive = [
        "".join(chars)
        for length in range(0, 6)
        for chars in itertools.product(small_alphabet, repeat=length)
    ]

    # Deterministic broader English-letter cases, including long recursion depths.
    rng = random.Random(118)
    random_cases = [
        "".join(rng.choice(string.ascii_letters) for _ in range(rng.randrange(0, 129)))
        for _ in range(5000)
    ]
    long_cases: list[str] = []
    for n in [0, 1, 2, 3, 4, 10, 50, 200, 500, 995, 1000, 1100, 2000]:
        long_cases.extend(
            [
                "b" * n,
                "a" * n,
                ("ba" * (n // 2 + 1))[:n],
                "bAb" + "x" * n,
                "x" * n + "u" + "z",
            ]
        )

    # Preserve stable order while removing duplicates.
    return list(dict.fromkeys(documented_and_boundaries + exhaustive + random_cases + long_cases))


def main() -> int:
    canonical = load_entry("trusted_canonical_118", SCRATCH / "canonical.py")
    generated = load_entry("generated_solution_118", SCRATCH / "solution.py")
    cases = build_cases()
    INPUT_RECORD.write_text("".join(f"{word!r}\n" for word in cases), encoding="utf-8")

    digest = hashlib.sha256()
    mismatches: list[tuple[str, object, object]] = []
    exceptions: list[tuple[str, str, str]] = []
    for word in cases:
        digest.update(word.encode("ascii"))
        digest.update(b"\0")
        try:
            expected = canonical(word)
        except Exception as err:
            exceptions.append((word, "canonical", repr(err)))
            continue
        try:
            actual = generated(word)
        except Exception as err:
            exceptions.append((word, "generated", repr(err)))
            continue
        if expected != actual:
            mismatches.append((word, expected, actual))

    print("oracle=/tmp/audit-work/reconstruction/canonical.py:get_closest_vowel")
    print("subject=/tmp/audit-work/reconstruction/solution.py:get_closest_vowel")
    print("domain=English-letter strings")
    print(
        "scope=prompt examples; lengths 0/1/2/3; all branch patterns over "
        "'abEyZ' through length 5; 5000 seeded ASCII-letter strings of length "
        "0..128; patterned strings through length 2003, including CPython's "
        "recursion boundary"
    )
    print(f"case_count={len(cases)}")
    print(f"input_sequence_sha256={digest.hexdigest()}")
    print(f"preserved_inputs={INPUT_RECORD}")
    print(f"exception_count={len(exceptions)}")
    print(f"mismatch_count={len(mismatches)}")
    for item in exceptions[:20]:
        print(f"EXCEPTION {item!r}")
    for item in mismatches[:20]:
        print(f"MISMATCH {item!r}")
    return 0 if not mismatches and not exceptions else 1


if __name__ == "__main__":
    sys.exit(main())
