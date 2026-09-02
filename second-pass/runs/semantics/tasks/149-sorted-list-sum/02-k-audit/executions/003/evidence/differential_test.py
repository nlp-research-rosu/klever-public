#!/usr/bin/env python3
"""Independent result differential for trusted canonical.py vs candidate solution.py."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("trusted_canonical", "/reference/canonical.py").sorted_list_sum
candidate = load("candidate_solution", "/candidate/solution.py").sorted_list_sum

named_cases = [
    ("documented_1", ["aa", "a", "aaa"]),
    ("documented_2", ["ab", "a", "aaa", "cd"]),
    ("empty_list", []),
    ("empty_string_even_boundary", [""]),
    ("odd_length_boundary", ["a"]),
    ("even_length_boundary", ["aa"]),
    ("both_filter_branches", ["a", "aa"]),
    ("duplicates", ["bb", "aa", "bb", "x"]),
    ("length_then_lexical", ["zz", "a", "bbbb", "aa", "cc", "odd"]),
    ("all_odd", ["a", "bbb", "ccccc"]),
    ("all_even", ["bbbb", "zz", "", "aa"]),
    ("unicode", ["éé", "Ω", "αα", "aa", "🙂🙂"]),
]

pool = ["", "a", "b", "aa", "ab", "ba", "bbb", "zzzz"]
generated_cases = [
    (f"exhaustive_{length}_{index}", list(words))
    for length in range(5)
    for index, words in enumerate(itertools.product(pool, repeat=length))
]

rng = random.Random(149)
alphabet = ["a", "b", "c", "z", "é", "Ω"]
for index in range(1000):
    words = []
    for _ in range(rng.randrange(0, 13)):
        words.append("".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 9))))
    generated_cases.append((f"seed149_random_{index}", words))

mismatches = []
canonical_mutations = 0
candidate_mutations = 0
case_digest = hashlib.sha256()
for label, original in named_cases + generated_cases:
    case_digest.update(json.dumps([label, original], ensure_ascii=False, separators=(",", ":")).encode())
    canonical_input = original.copy()
    candidate_input = original.copy()
    expected = canonical(canonical_input)
    actual = candidate(candidate_input)
    canonical_mutations += canonical_input != original
    candidate_mutations += candidate_input != original
    if actual != expected or type(actual) is not type(expected):
        mismatches.append(
            {
                "label": label,
                "input": original,
                "canonical_result": expected,
                "candidate_result": actual,
                "canonical_type": type(expected).__name__,
                "candidate_type": type(actual).__name__,
            }
        )

print(f"named_cases={len(named_cases)}")
print(f"generated_cases={len(generated_cases)}")
print(f"total_cases={len(named_cases) + len(generated_cases)}")
print(f"case_stream_sha256={case_digest.hexdigest()}")
print(f"result_mismatches={len(mismatches)}")
print(f"canonical_input_mutations={canonical_mutations}")
print(f"candidate_input_mutations={candidate_mutations}")
print("first_mismatches=" + json.dumps(mismatches[:10], ensure_ascii=False, sort_keys=True))
raise SystemExit(1 if mismatches else 0)
