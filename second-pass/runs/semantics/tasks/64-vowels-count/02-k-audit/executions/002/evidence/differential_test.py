#!/usr/bin/env python3
"""Independent differential audit of trusted canonical vs candidate Python."""

from __future__ import annotations

import importlib.util
import itertools
import pathlib
import random
import sys
from collections import Counter
from typing import Callable


def load_function(path: pathlib.Path, module_name: str) -> Callable[[str], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.vowels_count


def outcome(function: Callable[[str], int], text: str) -> tuple[str, object]:
    try:
        value = function(text)
        return ("return", value)
    except Exception as error:  # The exception class is observable behavior.
        return ("raise", type(error).__name__)


def main() -> int:
    canonical = load_function(
        pathlib.Path("/tmp/audit-work/proof/trusted/canonical.py"),
        "trusted_canonical",
    )
    generated = load_function(
        pathlib.Path("/tmp/audit-work/proof/solution.py"),
        "generated_solution",
    )

    cases: list[tuple[str, str]] = [
        ("documented", "abcde"),
        ("documented", "ACEDY"),
        ("empty", ""),
        ("branch-boundary", "a"),
        ("branch-boundary", "A"),
        ("branch-boundary", "b"),
        ("branch-boundary", "y"),
        ("branch-boundary", "Y"),
        ("branch-boundary", "ya"),
        ("branch-boundary", "ay"),
        ("branch-boundary", "yY"),
        ("branch-boundary", "AEIOU"),
        ("branch-boundary", "rhythm"),
        ("branch-boundary", "yellowy"),
        ("unicode-targeted", "\u0130"),
        ("unicode-targeted", "A\u0130"),
        ("unicode-targeted", "\u0130y"),
        ("unicode-targeted", "caf\u00e9"),
        ("unicode-targeted", "\u03a3y"),
    ]

    # Exhaust every nonempty ASCII string through length 4 over a basis that
    # reaches lowercase/uppercase vowels, terminal/internal y, and consonants.
    alphabet = "aAyYeb"
    for length in range(1, 5):
        for chars in itertools.product(alphabet, repeat=length):
            cases.append(("ascii-exhaustive-len1-4", "".join(chars)))

    # Deterministic broader ASCII words.
    generator = random.Random(640026)
    broad_alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for _ in range(5000):
        length = generator.randint(1, 32)
        text = "".join(generator.choice(broad_alphabet) for _ in range(length))
        cases.append(("ascii-random", text))

    # Exhaust every valid one-code-point Python string. This is bounded and
    # detects Unicode lowercasing behavior without relying on selected examples.
    for codepoint in range(0x110000):
        if 0xD800 <= codepoint <= 0xDFFF:
            continue
        cases.append(("unicode-single-codepoint", chr(codepoint)))

    counts: Counter[str] = Counter()
    mismatches: list[tuple[str, str, tuple[str, object], tuple[str, object]]] = []
    for scope, text in cases:
        counts[scope] += 1
        expected = outcome(canonical, text)
        actual = outcome(generated, text)
        if expected != actual:
            mismatches.append((scope, text, expected, actual))

    print("oracle=/tmp/audit-work/proof/trusted/canonical.py:vowels_count")
    print("candidate=/tmp/audit-work/proof/solution.py:vowels_count")
    print(f"total_cases={len(cases)}")
    for scope in sorted(counts):
        scoped_mismatches = sum(item[0] == scope for item in mismatches)
        print(
            f"scope={scope} cases={counts[scope]} mismatches={scoped_mismatches}"
        )
    print(f"mismatch_count={len(mismatches)}")
    for scope, text, expected, actual in mismatches[:100]:
        print(
            "MISMATCH "
            f"scope={scope} input={text!r} codepoints="
            f"{[ord(char) for char in text]!r} "
            f"canonical={expected!r} generated={actual!r}"
        )
    if len(mismatches) > 100:
        print(f"additional_mismatches_omitted={len(mismatches) - 100}")

    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
