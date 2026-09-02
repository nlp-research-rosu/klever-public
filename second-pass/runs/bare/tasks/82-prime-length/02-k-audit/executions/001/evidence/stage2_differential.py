#!/usr/bin/env python3
"""Independent canonical/generated/oracle differential for HumanEval 82."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import random
import sys
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def independent_prime_length(text: str) -> bool:
    length = len(text)
    if length < 2:
        return False
    return all(length % divisor for divisor in range(2, math.isqrt(length) + 1))


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit("usage: stage2_differential.py CANONICAL.py GENERATED.py")
    canonical = load_module("trusted_canonical", Path(sys.argv[1]))
    generated = load_module("generated_solution", Path(sys.argv[2]))

    cases: list[tuple[str, str]] = [
        ("example-Hello", "Hello"),
        ("example-abcdcba", "abcdcba"),
        ("example-kittens", "kittens"),
        ("example-orange", "orange"),
        ("empty", ""),
        ("length-1", "a"),
        ("length-2-loop-empty", "ab"),
        ("length-3-first-nonempty-prime", "abc"),
        ("length-4-first-divisor", "abcd"),
        ("length-5-prime", "abcde"),
        ("length-6-divisor-2", "abcdef"),
        ("length-9-first-divisor-3", "abcdefghi"),
        ("unicode-one-codepoint", "🙂"),
        ("unicode-two-codepoints", "é🙂"),
        ("embedded-nul-length-2", "\0a"),
    ]

    # Exhaust every length through 300. This covers the base branches, empty
    # and nonempty ranges, primes, composites, squares, and every divisor
    # position that arises in this interval.
    cases.extend((f"all-lengths-{length}", "x" * length) for length in range(301))

    # Deterministic representative content samples. Content should be
    # immaterial, but this probes Unicode, whitespace, NULs, and mixed strings.
    rng = random.Random(820082)
    alphabet = ["a", "Z", "0", " ", "\n", "\0", "é", "λ", "🙂"]
    for index in range(250):
        length = rng.randrange(0, 401)
        text = "".join(rng.choice(alphabet) for _ in range(length))
        cases.append((f"generated-{index}", text))

    mismatches = []
    results = []
    for label, text in cases:
        expected = independent_prime_length(text)
        canonical_result = canonical.prime_length(text)
        generated_result = generated.prime_length(text)
        row = {
            "label": label,
            "input": text,
            "length": len(text),
            "input_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "oracle": expected,
            "canonical": canonical_result,
            "generated": generated_result,
        }
        results.append(row)
        if not (
            type(canonical_result) is bool
            and type(generated_result) is bool
            and canonical_result == generated_result == expected
        ):
            mismatches.append(row)

    report = {
        "oracle": "independent trial division through isqrt(length)",
        "seed": 820082,
        "scope": {
            "documented_examples": 4,
            "explicit_boundaries_and_content_cases": 11,
            "exhaustive_lengths": [0, 300],
            "generated_content_cases": 250,
            "total_cases": len(cases),
        },
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "results": results,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
