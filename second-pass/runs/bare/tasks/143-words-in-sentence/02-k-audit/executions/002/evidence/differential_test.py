#!/usr/bin/env python3
"""Independent differential/oracle checks for HumanEval 143."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
import string
import sys
from pathlib import Path


CANONICAL = Path("/tmp/audit-work/clean/reference/canonical.py")
CANDIDATE = Path("/tmp/audit-work/clean/candidate/solution.py")


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.words_in_sentence


def is_prime(number: int) -> bool:
    if number < 2:
        return False
    divisor = 2
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 1
    return True


def independent_oracle(sentence: str) -> str:
    return " ".join(word for word in sentence.split() if is_prime(len(word)))


def main() -> int:
    canonical = load_entry(CANONICAL, "trusted_humaneval_143")
    candidate = load_entry(CANDIDATE, "generated_humaneval_143")

    documented = [
        "This is a test",
        "lets go for swimming",
    ]
    empty_and_boundaries = [
        "",
        "a",
        "aa",
        "aaa",
        "aaaa",
        "aaaaa",
        "aaaaaa",
        "aaaaaaa",
        "aaaaaaaa",
        "a aa",  # first selected word takes the empty-result branch
        "aa aaa",  # subsequent selected word takes the append branch
        "a aaaa",  # no selected word
        "aa " + "a" * 97,  # length exactly 100
        "a" * 98,
        "a" * 99,
        "a" * 100,
        "éé λλλ",  # non-ASCII letters, with Python character lengths 2 and 3
    ]
    spacing_observations = [
        "  aa",
        "aa  aaa",
        "aa ",
        "\taa\tbbb",
    ]

    generated: list[str] = []
    # Exhaust every possible one-word length under the stated length bound.
    generated.extend("a" * size for size in range(1, 101))
    # Exhaust every pair of positive word lengths under the total bound.
    for left in range(1, 100):
        for right in range(1, 100):
            if left + 1 + right <= 100:
                generated.append("a" * left + " " + "b" * right)

    rng = random.Random(143)
    for _ in range(5000):
        target_length = rng.randint(1, 100)
        words: list[str] = []
        used = 0
        while used < target_length:
            separator_cost = 1 if words else 0
            room = target_length - used - separator_cost
            if room <= 0:
                break
            word_length = rng.randint(1, room)
            word = "".join(rng.choice(string.ascii_letters) for _ in range(word_length))
            words.append(word)
            used += separator_cost + word_length
        generated.append(" ".join(words))

    inputs = documented + empty_and_boundaries + generated
    inputs = list(dict.fromkeys(inputs))
    mismatches = []
    for sentence in inputs:
        expected = independent_oracle(sentence)
        canonical_result = canonical(sentence)
        candidate_result = candidate(sentence)
        if canonical_result != expected or candidate_result != expected:
            mismatches.append(
                {
                    "input": sentence,
                    "length": len(sentence),
                    "oracle": expected,
                    "canonical": canonical_result,
                    "candidate": candidate_result,
                }
            )

    corpus_json = json.dumps(inputs, ensure_ascii=False, separators=(",", ":"))
    print(f"canonical={CANONICAL}")
    print(f"candidate={CANDIDATE}")
    print("oracle=independent trial-division primality plus Python str.split")
    print(
        "scope=documented examples; empty input; branch/boundary witnesses; "
        "all single-word lengths 1..100; all two-word positive-length pairs "
        "within total length 100; 5000 deterministic generated inputs; "
        "four spacing observations"
    )
    print(f"unique_inputs={len(inputs)}")
    print(f"corpus_sha256={hashlib.sha256(corpus_json.encode()).hexdigest()}")
    print(f"mismatch_count={len(mismatches)}")
    for mismatch in mismatches[:20]:
        print(json.dumps(mismatch, ensure_ascii=False, sort_keys=True))

    print("outside_domain_spacing_observations:")
    for sentence in spacing_observations:
        expected = canonical(sentence)
        actual = candidate(sentence)
        print(
            json.dumps(
                {
                    "input": sentence,
                    "canonical": expected,
                    "candidate": actual,
                    "equal": expected == actual,
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
    return 0 if not mismatches else 1


if __name__ == "__main__":
    sys.exit(main())
