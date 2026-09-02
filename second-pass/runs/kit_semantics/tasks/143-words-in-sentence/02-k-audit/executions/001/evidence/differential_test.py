#!/usr/bin/env python3
"""Independent differential test of trusted canonical.py versus solution.py."""

from __future__ import annotations

import importlib.util
import itertools
import random
import string
import sys
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.words_in_sentence


def prime(n: int) -> bool:
    return n >= 2 and all(n % divisor for divisor in range(2, int(n**0.5) + 1))


def independent_oracle(sentence: str) -> str:
    return " ".join(word for word in sentence.split() if prime(len(word)))


def build_cases() -> list[tuple[str, str]]:
    cases: list[tuple[str, str]] = [
        ("example-1", "This is a test"),
        ("example-2", "lets go for swimming"),
        ("empty-outside-prompt", ""),
        ("one-letter-min", "a"),
        ("two-letter-prime", "aa"),
        ("three-letter-prime", "bbb"),
        ("four-letter-composite", "cccc"),
        ("leading-spaces", "  aa bbb"),
        ("trailing-spaces", "aa bbb  "),
        ("repeated-spaces", "aa  bbb    cccc"),
        ("all-spaces", "    "),
        ("max-single-prime-97", "a" * 97),
        ("max-single-composite-100", "a" * 100),
        ("max-sentence-mixed", "aa " + "b" * 97),
    ]

    # Every possible single-word length, exercising each prime/composite boundary.
    cases.extend((f"single-length-{length}", "a" * length) for length in range(1, 101))

    # Adjacent values around every prime in the bounded source domain.
    primes = [n for n in range(1, 101) if prime(n)]
    boundary_lengths = sorted({n for p in primes for n in (p - 1, p, p + 1) if 1 <= n <= 100})
    cases.extend((f"prime-boundary-{length}", "b" * length) for length in boundary_lengths)

    # Representative pairs with exact total length at most 100.
    pair_lengths = (1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 13, 17, 19, 23, 29, 31, 47)
    for left, right in itertools.product(pair_lengths, repeat=2):
        sentence = "a" * left + " " + "b" * right
        if 1 <= len(sentence) <= 100:
            cases.append((f"pair-{left}-{right}", sentence))

    rng = random.Random(14320260729)
    alphabet = string.ascii_letters + " "
    for index in range(2500):
        length = rng.randint(1, 100)
        sentence = "".join(rng.choice(alphabet) for _ in range(length))
        cases.append((f"generated-{index}", sentence))
    return cases


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/audit-work/audit-143")
    canonical = load_entry(root / "canonical.py", "trusted_canonical")
    generated = load_entry(root / "solution.py", "generated_solution")
    cases = build_cases()
    mismatches: list[tuple[str, str, str, str, str]] = []
    for label, sentence in cases:
        canonical_result = canonical(sentence)
        generated_result = generated(sentence)
        oracle_result = independent_oracle(sentence)
        if canonical_result != generated_result or canonical_result != oracle_result:
            mismatches.append((label, sentence, canonical_result, generated_result, oracle_result))

    print("DIFFERENTIAL_ORACLE=trusted canonical.py plus independently coded trial division")
    print("INPUT_SCOPE=examples, empty, spacing, lengths 1..100, prime adjacencies, bounded pairs, 2500 seeded letter/space strings")
    print(f"DIFFERENTIAL_CASES={len(cases)}")
    print(f"DIFFERENTIAL_MISMATCHES={len(mismatches)}")
    for label, sentence, expected, actual, oracle in mismatches[:20]:
        print(
            f"MISMATCH label={label} input={sentence!r} "
            f"canonical={expected!r} generated={actual!r} oracle={oracle!r}"
        )
    for label in ("example-1", "example-2", "one-letter-min", "two-letter-prime", "max-single-composite-100"):
        sentence = next(value for case_label, value in cases if case_label == label)
        print(f"WITNESS {label} input={sentence!r} output={generated(sentence)!r}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
