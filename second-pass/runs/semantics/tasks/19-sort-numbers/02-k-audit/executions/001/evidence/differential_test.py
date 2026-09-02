#!/usr/bin/env python3
"""Differentially compare the trusted canonical and submitted entry points."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path


CANONICAL_PATH = Path("/tmp/audit-work/audit19/canonical.py")
SUBMITTED_PATH = Path("/tmp/audit-work/audit19/solution.py")
WORDS = (
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    canonical = load_module("trusted_canonical", CANONICAL_PATH)
    submitted = load_module("submitted_solution", SUBMITTED_PATH)

    named_cases = {
        "documented": "three one five",
        "empty": "",
        "one-boundary": "zero",
        "nine-fallthrough-boundary": "nine",
        "ascending": "zero one two three four five six seven eight nine",
        "descending": "nine eight seven six five four three two one zero",
        "duplicates": "nine zero nine two one zero five five",
        "leading-trailing-spaces": "  three one five  ",
        "multiple-space-delimiters": "nine   zero one  nine",
    }

    cases: list[tuple[str, str]] = list(named_cases.items())
    for word in WORDS:
        cases.append((f"singleton-{word}", word))

    for length in range(5):
        for index, seq in enumerate(itertools.product(WORDS, repeat=length)):
            cases.append((f"exhaustive-len-{length}-{index}", " ".join(seq)))

    rng = random.Random(190019)
    for index in range(2000):
        length = rng.randrange(0, 31)
        seq = [rng.choice(WORDS) for _ in range(length)]
        separator = " " * rng.randrange(1, 5)
        prefix = " " * rng.randrange(0, 4)
        suffix = " " * rng.randrange(0, 4)
        cases.append((f"generated-{index}", prefix + separator.join(seq) + suffix))

    mismatches: list[dict[str, str]] = []
    digest = hashlib.sha256()
    for label, value in cases:
        expected = canonical.sort_numbers(value)
        actual = submitted.sort_numbers(value)
        record = {
            "label": label,
            "input": value,
            "canonical": expected,
            "submitted": actual,
        }
        digest.update(
            json.dumps(record, sort_keys=True, ensure_ascii=True).encode("utf-8")
        )
        digest.update(b"\n")
        if expected != actual:
            mismatches.append(record)

    helper_results = {word: submitted.number_value(word) for word in WORDS}
    helper_expected = {word: index for index, word in enumerate(WORDS)}
    helper_mismatches = {
        word: (helper_expected[word], helper_results[word])
        for word in WORDS
        if helper_expected[word] != helper_results[word]
    }

    print(f"canonical_path={CANONICAL_PATH}")
    print(f"submitted_path={SUBMITTED_PATH}")
    print("intended_domain=space-delimited sequences over zero..nine")
    print("documented_case=" + json.dumps(named_cases["documented"]))
    print("named_and_singleton_cases=19")
    print("exhaustive_sequences=lengths 0..4 over 10 words (11111 cases)")
    print("generated_cases=2000 seed=190019 lengths 0..30, 1..4 spaces")
    print(f"total_cases={len(cases)}")
    print(f"case_record_sha256={digest.hexdigest()}")
    print(f"mismatch_count={len(mismatches)}")
    if mismatches:
        print("first_mismatches=" + json.dumps(mismatches[:20], sort_keys=True))
    print("helper_results=" + json.dumps(helper_results, sort_keys=True))
    print(f"helper_mismatch_count={len(helper_mismatches)}")
    if helper_mismatches:
        print("helper_mismatches=" + json.dumps(helper_mismatches, sort_keys=True))
    return 1 if mismatches or helper_mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
