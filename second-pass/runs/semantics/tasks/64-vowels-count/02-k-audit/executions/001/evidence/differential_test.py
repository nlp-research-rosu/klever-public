#!/usr/bin/env python3
"""Independent candidate-versus-canonical differential test for HumanEval 64."""

from __future__ import annotations

import importlib.util
import itertools
import random
import string
import sys
from collections.abc import Iterable
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.vowels_count


CANONICAL = load_function("trusted_canonical", Path("/reference/canonical.py"))
GENERATED = load_function(
    "generated_solution", Path("/tmp/audit-work/fresh/solution.py")
)


def outcome(function, value: str):
    try:
        result = function(value)
        return ("return", type(result).__name__, result)
    except Exception as err:  # The exception kind is observable behavior.
        return ("raise", type(err).__name__)


def unique(values: Iterable[str]):
    seen: set[str] = set()
    for value in values:
        if value not in seen:
            seen.add(value)
            yield value


def compare_group(name: str, values: Iterable[str]):
    checked = 0
    mismatches = []
    for value in unique(values):
        checked += 1
        expected = outcome(CANONICAL, value)
        actual = outcome(GENERATED, value)
        if expected != actual:
            mismatches.append((value, expected, actual))
    print(f"{name}: checked={checked} mismatches={len(mismatches)}")
    for value, expected, actual in mismatches[:20]:
        print(
            f"  input={value!r} codepoints="
            f"{[f'U+{ord(c):04X}' for c in value]} "
            f"canonical={expected!r} generated={actual!r}"
        )
    if len(mismatches) > 20:
        print(f"  ... {len(mismatches) - 20} additional mismatches omitted")
    return mismatches


def main() -> int:
    documented = ["abcde", "ACEDY"]
    empty_boundary = [""]
    branch_boundaries = [
        "a",
        "e",
        "i",
        "o",
        "u",
        "A",
        "E",
        "I",
        "O",
        "U",
        "y",
        "Y",
        "by",
        "bY",
        "yb",
        "Yb",
        "b",
        "rhythm",
        "AEIOU",
        "aeiouy",
        "yellowy",
        "yyyy",
        "aY",
        "Ya",
    ]

    alphabet = "aeybAEYB"
    exhaustive_ascii = (
        "".join(chars)
        for length in range(1, 6)
        for chars in itertools.product(alphabet, repeat=length)
    )

    rng = random.Random(640064)
    random_alphabet = string.ascii_letters + string.digits + string.punctuation
    random_ascii = [
        "".join(rng.choice(random_alphabet) for _ in range(rng.randint(1, 64)))
        for _ in range(10_000)
    ]

    unicode_one_letter_words = (
        chr(codepoint)
        for codepoint in range(sys.maxunicode + 1)
        if not 0xD800 <= codepoint <= 0xDFFF
        and chr(codepoint).isalpha()
    )
    targeted_unicode = [
        "İ",  # LATIN CAPITAL LETTER I WITH DOT ABOVE; lower() expands to i + dot.
        "İy",
        "xİ",
        "CAFÉ",
        "naïve",
        "ΑΕΙΟΥ",
        "Ы",
    ]

    groups = [
        ("documented_examples", documented),
        ("empty_boundary", empty_boundary),
        ("branch_boundaries", branch_boundaries),
        ("exhaustive_ascii_length_1_to_5", exhaustive_ascii),
        ("seeded_random_ascii_10000", random_ascii),
        ("targeted_unicode", targeted_unicode),
        ("all_single_unicode_letters", unicode_one_letter_words),
    ]

    all_mismatches = {}
    for name, values in groups:
        all_mismatches[name] = compare_group(name, values)

    nonempty_mismatch_count = sum(
        len(mismatches)
        for name, mismatches in all_mismatches.items()
        if name != "empty_boundary"
    )
    total_mismatch_count = nonempty_mismatch_count + len(
        all_mismatches["empty_boundary"]
    )
    print(f"total_mismatches={total_mismatch_count}")
    print(f"nonempty_mismatches={nonempty_mismatch_count}")
    print(
        "oracle=trusted /reference/canonical.py; "
        "subject=/tmp/audit-work/fresh/solution.py"
    )
    return 1 if total_mismatch_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
