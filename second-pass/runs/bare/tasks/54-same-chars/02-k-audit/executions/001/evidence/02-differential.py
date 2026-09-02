#!/usr/bin/env python3
"""Independent differential test for HumanEval/54.

Oracle: /tmp/audit-work/trusted/canonical.py, copied from the trusted mount.
Subject: /tmp/audit-work/fresh/solution.py, copied from the candidate.

The complete input scope is reproducible from the literal cases, alphabet,
length bound, random seed, alphabet, and iteration count below.
"""

from __future__ import annotations

import hashlib
import importlib.util
import inspect
import itertools
import json
import random
from pathlib import Path


TRUSTED = Path("/tmp/audit-work/trusted/canonical.py")
SUBJECT = Path("/tmp/audit-work/fresh/solution.py")
SEED = 540054
EXHAUSTIVE_ALPHABET = ("a", "b", "é")
EXHAUSTIVE_MAX_LENGTH = 4
RANDOM_ALPHABET = ("a", "b", "A", "é", "😀", "\u0301", "\x00", "\n")
RANDOM_PAIRS = 2000

DOCUMENTED = [
    ("eabcdzzzz", "dddzzzzzzzddeddabc", True),
    ("abcd", "dddddddabc", True),
    ("dddddddabc", "abcd", True),
    ("eabcd", "dddddddabc", False),
    ("abcd", "dddddddabce", False),
    ("eabcdzzzz", "dddzzzzzzzddddabc", False),
]

BOUNDARIES = [
    ("", "", True),
    ("", "a", False),
    ("a", "", False),
    ("a", "a", True),
    ("a", "aaaa", True),
    ("ab", "ba", True),
    ("ab", "aa", False),
    ("Aa", "aA", True),
    ("Aa", "aa", False),
    ("é", "e\u0301", False),
    ("😀😀", "😀", True),
    ("\x00a", "a\x00\x00", True),
    ("\n", "", False),
]


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def strings(alphabet: tuple[str, ...], max_length: int):
    for length in range(max_length + 1):
        for chars in itertools.product(alphabet, repeat=length):
            yield "".join(chars)


def main() -> int:
    canonical = load(TRUSTED, "trusted_canonical")
    subject = load(SUBJECT, "candidate_solution")
    oracle = canonical.same_chars
    generated = subject.same_chars

    exhaustive_strings = list(strings(EXHAUSTIVE_ALPHABET, EXHAUSTIVE_MAX_LENGTH))
    pairs: list[tuple[str, str, bool | None, str]] = [
        (left, right, expected, "documented")
        for left, right, expected in DOCUMENTED
    ]
    pairs.extend(
        (left, right, expected, "boundary")
        for left, right, expected in BOUNDARIES
    )
    pairs.extend(
        (left, right, None, "exhaustive")
        for left in exhaustive_strings
        for right in exhaustive_strings
    )

    rng = random.Random(SEED)
    for index in range(RANDOM_PAIRS):
        left = "".join(
            rng.choice(RANDOM_ALPHABET) for _ in range(rng.randrange(0, 25))
        )
        if index % 2 == 0:
            chars = list(left)
            rng.shuffle(chars)
            right = "".join(chars)
            if chars:
                right += rng.choice(chars) * rng.randrange(0, 4)
        else:
            right = "".join(
                rng.choice(RANDOM_ALPHABET) for _ in range(rng.randrange(0, 25))
            )
        pairs.append((left, right, None, "random"))

    corpus_encoding = json.dumps(
        [(left, right, label) for left, right, _, label in pairs],
        ensure_ascii=True,
        separators=(",", ":"),
    ).encode()
    corpus_sha256 = hashlib.sha256(corpus_encoding).hexdigest()

    mismatches = []
    expected_failures = []
    oracle_true = 0
    oracle_false = 0
    for index, (left, right, expected, label) in enumerate(pairs):
        oracle_result = oracle(left, right)
        subject_result = generated(left, right)
        oracle_true += oracle_result is True
        oracle_false += oracle_result is False
        if expected is not None and oracle_result is not expected:
            expected_failures.append(
                (index, left, right, expected, oracle_result, label)
            )
        if subject_result != oracle_result or type(subject_result) is not bool:
            mismatches.append(
                (index, left, right, oracle_result, subject_result, label)
            )

    print(f"trusted={TRUSTED}")
    print(f"subject={SUBJECT}")
    print(f"trusted_signature={inspect.signature(oracle)}")
    print(f"subject_signature={inspect.signature(generated)}")
    print(f"documented_cases={len(DOCUMENTED)}")
    print(f"boundary_cases={len(BOUNDARIES)}")
    print(
        "exhaustive_recipe="
        f"alphabet={EXHAUSTIVE_ALPHABET!r}, max_length={EXHAUSTIVE_MAX_LENGTH}, "
        f"strings={len(exhaustive_strings)}, pairs={len(exhaustive_strings) ** 2}"
    )
    print(
        "random_recipe="
        f"seed={SEED}, alphabet={RANDOM_ALPHABET!r}, pairs={RANDOM_PAIRS}, "
        "lengths=range(0,25), even indices preserve the left character set"
    )
    print(f"total_pairs={len(pairs)}")
    print(f"corpus_sha256={corpus_sha256}")
    print(f"oracle_true={oracle_true}")
    print(f"oracle_false={oracle_false}")
    print(f"documented_expected_failures={len(expected_failures)}")
    print(f"mismatches={len(mismatches)}")
    if expected_failures:
        print(f"first_expected_failure={expected_failures[0]!r}")
    if mismatches:
        print(f"first_mismatch={mismatches[0]!r}")
    return 1 if expected_failures or mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
