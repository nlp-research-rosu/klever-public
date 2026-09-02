#!/usr/bin/env python3
"""Independent differential test for HumanEval 118.

Oracle: trusted /reference/canonical.py.
Implementation under audit: scratch copy of /candidate/solution.py.
"""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import random
import string
from collections import Counter
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CANONICAL = load_module(
    "trusted_canonical", Path("/tmp/audit-work/trusted/canonical.py")
)
GENERATED = load_module(
    "generated_solution", Path("/tmp/audit-work/reconstruction/solution.py")
)
VOWELS = frozenset("aeiouAEIOU")

NAMED_CASES = (
    # Four documented examples.
    ("yogurt", "u"),
    ("FULL", "U"),
    ("quick", ""),
    ("ab", ""),
    # Empty and length boundaries.
    ("", ""),
    ("a", ""),
    ("b", ""),
    ("aa", ""),
    ("ba", ""),
    ("aba", ""),
    # Beginning/end vowels do not count.
    ("abb", ""),
    ("bba", ""),
    # Interior vowel with consonant/vowel neighbors.
    ("bab", "a"),
    ("baa", ""),
    ("aab", ""),
    ("bAb", "A"),
    ("bub", "u"),
    # Search order: return the rightmost qualifying vowel.
    ("babab", "a"),
    ("bacad", "a"),
    ("bacef", "e"),
    # Rightmost interior vowel can fail while an earlier one qualifies.
    ("babaced", "e"),
    ("babaaed", "a"),
    # Case sensitivity and consonant coverage.
    ("ZUZ", "U"),
    ("zEz", "E"),
    ("zYz", ""),
)


def classify(word: str) -> str:
    if len(word) < 3:
        return "length<3"
    eligible = [
        index
        for index in range(1, len(word) - 1)
        if word[index] in VOWELS
        and word[index - 1] not in VOWELS
        and word[index + 1] not in VOWELS
    ]
    if not eligible:
        return "no-qualifier"
    if eligible[-1] == len(word) - 2:
        return "right-boundary-qualifier"
    if len(eligible) > 1:
        return "multiple-qualifiers"
    return "interior-qualifier"


def main() -> None:
    mismatches: list[tuple[str, str, str]] = []
    classes: Counter[str] = Counter()
    inputs_hash = hashlib.sha256()
    count = 0

    def check(word: str, declared: str | None = None) -> None:
        nonlocal count
        expected = CANONICAL.get_closest_vowel(word)
        actual = GENERATED.get_closest_vowel(word)
        if declared is not None:
            assert expected == declared, (
                f"reviewer named-case expectation wrong for {word!r}: "
                f"{declared!r} != {expected!r}"
            )
        if expected != actual and len(mismatches) < 20:
            mismatches.append((word, expected, actual))
        classes[classify(word)] += 1
        encoded = word.encode("ascii")
        inputs_hash.update(len(encoded).to_bytes(4, "big"))
        inputs_hash.update(encoded)
        count += 1

    print("named_cases:")
    for word, declared in NAMED_CASES:
        check(word, declared)
        print(
            f"  {word!r}: canonical={CANONICAL.get_closest_vowel(word)!r} "
            f"generated={GENERATED.get_closest_vowel(word)!r}"
        )

    exhaustive_alphabet = "aAbBZ"
    exhaustive_max_length = 8
    for length in range(exhaustive_max_length + 1):
        for letters in itertools.product(exhaustive_alphabet, repeat=length):
            check("".join(letters))

    seed = 20260729
    random_count = 20_000
    random_max_length = 200
    generator = random.Random(seed)
    for _ in range(random_count):
        length = generator.randrange(random_max_length + 1)
        check(
            "".join(
                generator.choice(string.ascii_letters) for _ in range(length)
            )
        )

    print(f"exhaustive_alphabet={exhaustive_alphabet!r}")
    print(f"exhaustive_lengths=0..{exhaustive_max_length}")
    print(
        f"random_seed={seed} random_count={random_count} "
        f"random_alphabet=string.ascii_letters random_lengths=0..{random_max_length}"
    )
    print(f"total_cases={count}")
    print(f"input_stream_sha256={inputs_hash.hexdigest()}")
    print(f"branch_class_counts={dict(sorted(classes.items()))}")
    print(f"mismatch_count={len(mismatches)}")
    for mismatch in mismatches:
        print(f"MISMATCH {mismatch!r}")
    assert not mismatches
    print("DIFFERENTIAL=PASS")


if __name__ == "__main__":
    main()
