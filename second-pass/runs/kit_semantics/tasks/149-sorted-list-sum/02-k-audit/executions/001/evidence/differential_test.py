#!/usr/bin/env python3
"""Reviewer-authored differential test for HumanEval/149.

The test imports the trusted canonical entry point and the submitted Python
entry point independently.  Its third oracle uses a single sort with the pair
key (length, text), rather than either implementation's two-stage strategy.
"""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
from pathlib import Path


CANONICAL_PATH = Path("/reference/canonical.py")
GENERATED_PATH = Path("/candidate/solution.py")


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sorted_list_sum


def oracle(values: list[str]) -> list[str]:
    return sorted((word for word in values if len(word) % 2 == 0), key=lambda word: (len(word), word))


def cases() -> list[list[str]]:
    explicit = [
        ["aa", "a", "aaa"],
        ["ab", "a", "aaa", "cd"],
        [],
        [""],
        ["a"],
        ["aa"],
        ["", "a", "aa"],
        ["aa", "aa"],
        ["bb", "aa", "bb", "aa"],
        ["zz", "aa", "b", "cccc", "dddd", "ccc"],
        ["bbaa", "aaaa", "zz", "aa"],
        ["ββ", "a", "😀😀", "éé"],
        ["", "", "x", "yy", "zzz", "wwww"],
        ["odd", "seven77", "x"],
        ["eight888", "six666"],
    ]

    # Exhaust every list of length 0..3 over representatives whose lengths
    # cross the empty/odd/even boundaries and include an alphabetical tie.
    alphabet = ["", "a", "aa", "bb", "ccc"]
    exhaustive = [
        list(items)
        for size in range(4)
        for items in itertools.product(alphabet, repeat=size)
    ]

    # Broader deterministic generated cases include duplicates, mixed lengths,
    # and lexicographic ties.
    rng = random.Random(149)
    pool = ["", "q", "ab", "ba", "xyz", "wxyz", "αβ", "😀", "😀😀"]
    generated = [
        [rng.choice(pool) for _ in range(rng.randrange(0, 13))]
        for _ in range(200)
    ]
    return explicit + exhaustive + generated


def main() -> int:
    canonical = load_function(CANONICAL_PATH, "trusted_humaneval_149")
    generated = load_function(GENERATED_PATH, "submitted_humaneval_149")
    test_cases = cases()
    failures = []
    canonical_input_mutations = 0
    generated_input_mutations = 0

    for index, original in enumerate(test_cases):
        canonical_input = list(original)
        generated_input = list(original)
        canonical_result = canonical(canonical_input)
        generated_result = generated(generated_input)
        expected = oracle(list(original))
        if canonical_input != original:
            canonical_input_mutations += 1
        if generated_input != original:
            generated_input_mutations += 1
        if canonical_result != generated_result or generated_result != expected:
            failures.append(
                {
                    "index": index,
                    "input": original,
                    "canonical": canonical_result,
                    "generated": generated_result,
                    "oracle": expected,
                    "canonical_post_input": canonical_input,
                    "generated_post_input": generated_input,
                }
            )

    scope = {
        "documented_examples": 2,
        "explicit_boundary_and_branch_cases": 13,
        "exhaustive_alphabet": ["", "a", "aa", "bb", "ccc"],
        "exhaustive_lengths": [0, 1, 2, 3],
        "deterministic_random_seed": 149,
        "generated_case_count": 200,
        "generated_max_list_length": 12,
        "total_cases": len(test_cases),
    }
    print("scope=" + json.dumps(scope, ensure_ascii=False, sort_keys=True))
    print(f"mismatches={len(failures)}")
    print(f"canonical_input_mutations={canonical_input_mutations}")
    print(f"generated_input_mutations={generated_input_mutations}")
    for failure in failures[:20]:
        print("FAIL " + json.dumps(failure, ensure_ascii=False, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
