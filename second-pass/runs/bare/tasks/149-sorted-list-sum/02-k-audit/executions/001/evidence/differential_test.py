#!/usr/bin/env python3
"""Independent differential test for HumanEval 149.

The case set is fully determined by the explicit cases, exhaustive vocabulary,
and PRNG seed below.  The printed SHA-256 identifies the exact ordered case set.
"""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
import string
import sys
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sorted_list_sum


def oracle(words: list[str]) -> list[str]:
    return sorted(
        (word for word in words if len(word) % 2 == 0),
        key=lambda word: (len(word), word),
    )


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: differential_test.py TRUSTED_CANONICAL GENERATED_SOLUTION")
        return 2

    canonical = load_function(Path(sys.argv[1]), "audit_trusted_canonical")
    generated_function = load_function(Path(sys.argv[2]), "audit_generated_solution")

    explicit = [
        [],
        ["aa", "a", "aaa"],
        ["ab", "a", "aaa", "cd"],
        [""],
        ["a"],
        ["aa"],
        ["aaa"],
        ["aaaa"],
        ["a", "b", "ccc"],
        ["aa", "bb", "cc"],
        ["ba", "ab"],
        ["ab", "ab", "aa", "ab"],
        ["aaaa", "aa", "", "bbb", "b", "zz"],
        ["zy", "ab", "x", "aa", "abcd", "ba", "ab"],
        ["😀", "é", "e\u0301", "😀😀", "éé", ""],
        ["Ωβ", "Ωα", "aa", "éa", "aé"],
    ]

    vocabulary = ["", "a", "b", "aa", "ab", "ba", "aaa", "bbbb"]
    exhaustive = [
        list(items)
        for width in range(5)
        for items in itertools.product(vocabulary, repeat=width)
    ]

    rng = random.Random(149_2026)
    alphabet = string.ascii_letters + "éΩ😀"
    random_cases = []
    for _ in range(500):
        random_cases.append(
            [
                "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 9)))
                for _ in range(rng.randrange(0, 13))
            ]
        )

    cases = explicit + exhaustive + random_cases
    encoded = json.dumps(cases, ensure_ascii=False, separators=(",", ":")).encode()

    return_mismatches = []
    canonical_oracle_mismatches = []
    generated_oracle_mismatches = []
    canonical_mutations = 0
    generated_mutations = 0
    for index, words in enumerate(cases):
        canonical_arg = list(words)
        generated_arg = list(words)
        expected = oracle(list(words))
        canonical_result = canonical(canonical_arg)
        generated_result = generated_function(generated_arg)

        if canonical_result != generated_result:
            return_mismatches.append(
                (index, words, canonical_result, generated_result)
            )
        if canonical_result != expected:
            canonical_oracle_mismatches.append(
                (index, words, canonical_result, expected)
            )
        if generated_result != expected:
            generated_oracle_mismatches.append(
                (index, words, generated_result, expected)
            )
        canonical_mutations += canonical_arg != words
        generated_mutations += generated_arg != words

    print("oracle=independent filter-even then Python tuple-key sort")
    print("explicit_cases=16")
    print(
        "exhaustive_scope=all lists of length 0..4 over "
        + json.dumps(vocabulary, ensure_ascii=False)
    )
    print("generated_scope=500 lists; seed=1492026; list length 0..12; word length 0..8")
    print(f"case_count={len(cases)}")
    print(f"ordered_cases_sha256={hashlib.sha256(encoded).hexdigest()}")
    print(f"return_mismatches={len(return_mismatches)}")
    print(f"canonical_oracle_mismatches={len(canonical_oracle_mismatches)}")
    print(f"generated_oracle_mismatches={len(generated_oracle_mismatches)}")
    print(f"canonical_argument_mutations={canonical_mutations}")
    print(f"generated_argument_mutations={generated_mutations}")
    if return_mismatches:
        print("first_return_mismatch=" + repr(return_mismatches[0]))
    if canonical_oracle_mismatches:
        print("first_canonical_oracle_mismatch=" + repr(canonical_oracle_mismatches[0]))
    if generated_oracle_mismatches:
        print("first_generated_oracle_mismatch=" + repr(generated_oracle_mismatches[0]))
    return int(
        bool(
            return_mismatches
            or canonical_oracle_mismatches
            or generated_oracle_mismatches
        )
    )


if __name__ == "__main__":
    raise SystemExit(main())
