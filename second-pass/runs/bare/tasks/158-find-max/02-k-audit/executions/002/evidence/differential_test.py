#!/usr/bin/env python3
"""Independent Python differential test for HumanEval 158."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import random


CANONICAL = Path("/tmp/audit-work/reference/canonical.py")
CANDIDATE = Path("/tmp/audit-work/candidate-src/solution.py")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def outcome(function, words: list[str]) -> tuple[str, str]:
    try:
        return ("return", repr(function(list(words))))
    except Exception as error:  # The empty boundary intentionally reaches this.
        return ("raise", type(error).__name__)


def generated_cases() -> list[list[str]]:
    rng = random.Random(158)
    alphabet = ["", "a", "b", "c", "aa", "ab", "ba", "abc", "cba", "aaaa"]
    unicode_pool = ["é", "e\u0301", "λ", "😀", "😀a", "\x00", "𐐀", "ß", "東京"]
    pool = alphabet + unicode_pool
    cases: list[list[str]] = []

    # Exhaustive ordered nonempty lists, without repeated words, over a small pool.
    for size in range(1, 5):
        cases.extend([list(words) for words in itertools.permutations(alphabet[:5], size)])

    # Reproducible broader samples, still respecting the "different words" contract.
    for _ in range(2000):
        size = rng.randint(1, min(10, len(pool)))
        cases.append(rng.sample(pool, size))
    return cases


def main() -> int:
    canonical = load_module("trusted_canonical", CANONICAL)
    candidate = load_module("candidate_solution", CANDIDATE)

    fixed = [
        ("example-1", ["name", "of", "string"]),
        ("example-2", ["name", "enam", "game"]),
        ("example-3", ["aaaaaaa", "bb", "cc"]),
        ("empty-boundary", []),
        ("singleton-empty-word", [""]),
        ("singleton", ["abc"]),
        ("greater-first", ["abcd", "a"]),
        ("greater-later", ["a", "abcd"]),
        ("tie-lex-later", ["ab", "ba"]),
        ("tie-lex-earlier-later", ["ba", "ab"]),
        ("all-repeat", ["zzzz", "yy", "x"]),
        ("combining-and-precomposed", ["é", "e\u0301"]),
        ("unicode", ["😀a", "東京", "λλ"]),
        ("nul-character", ["\x00a", "\x00"]),
    ]
    mismatches: list[tuple[str, list[str], tuple[str, str], tuple[str, str]]] = []
    for label, words in fixed:
        expected = outcome(canonical.find_max, words)
        actual = outcome(candidate.find_max, words)
        print(
            json.dumps(
                {
                    "label": label,
                    "words": words,
                    "canonical": expected,
                    "candidate": actual,
                },
                ensure_ascii=True,
                sort_keys=True,
            )
        )
        if expected != actual:
            mismatches.append((label, words, expected, actual))

    generated = generated_cases()
    encoded = json.dumps(generated, ensure_ascii=True, separators=(",", ":")).encode()
    generated_mismatches = 0
    for index, words in enumerate(generated):
        expected = outcome(canonical.find_max, words)
        actual = outcome(candidate.find_max, words)
        if expected != actual:
            generated_mismatches += 1
            if generated_mismatches <= 20:
                print(
                    "GENERATED_MISMATCH "
                    + repr((index, words, expected, actual))
                )
    print(f"generated_case_count={len(generated)}")
    print(f"generated_case_sha256={hashlib.sha256(encoded).hexdigest()}")
    print(f"generated_mismatches={generated_mismatches}")
    print(f"fixed_mismatches={len(mismatches)}")
    print(f"fixed_mismatch_details={mismatches!r}")

    # The trusted canonical deliberately indexes [0], so the empty list has no
    # normal result. Judge agreement over the nonempty source-contract domain.
    intended_domain_mismatches = [
        mismatch for mismatch in mismatches if mismatch[0] != "empty-boundary"
    ]
    print(f"intended_domain_mismatches={len(intended_domain_mismatches)}")
    return 0 if not intended_domain_mismatches and generated_mismatches == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
