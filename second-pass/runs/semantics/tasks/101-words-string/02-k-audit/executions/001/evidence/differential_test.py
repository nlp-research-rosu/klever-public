#!/usr/bin/env python3
"""Independent candidate/canonical differential harness for HumanEval 101."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path

CANONICAL_PATH = Path("/tmp/audit-work/trusted/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/candidate-src/solution.py")
RESULT_PATH = Path("/audit-output/evidence/differential_cases.jsonl")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module("trusted_canonical_101", CANONICAL_PATH).words_string
candidate = load_module("submitted_solution_101", CANDIDATE_PATH).words_string

named_cases = [
    ("example_1", "Hi, my name is John"),
    ("example_2", "One, two, three, four, five, six"),
    ("empty", ""),
    ("single_nonseparator", "a"),
    ("single_comma", ","),
    ("single_space", " "),
    ("comma_prefix", ",a"),
    ("comma_suffix", "a,"),
    ("space_prefix", " a"),
    ("space_suffix", "a "),
    ("adjacent_commas", "a,,b"),
    ("mixed_adjacent_separators", "a, ,b"),
    ("only_commas_and_spaces", ",,  ,,"),
    ("tab_newline_formfeed", "\ta\nb\fc"),
    ("unicode_whitespace", "α,\u2003β\u00a0γ"),
    ("unicode_non_whitespace", "你好,мир"),
    ("embedded_nul", "a\x00,b"),
]

cases: list[tuple[str, str]] = list(named_cases)
small_alphabet = ("a", "Z", ",", " ", "\t")
for length in range(0, 6):
    for chars in itertools.product(small_alphabet, repeat=length):
        cases.append((f"exhaustive_len_{length}", "".join(chars)))

rng = random.Random(101_20260724)
random_alphabet = (
    "abcXYZ019,"
    " \t\n\r\v\f"
    "αβγ你好"
    "\u00a0\u2003"
)
for index in range(2000):
    length = rng.randrange(0, 81)
    value = "".join(rng.choice(random_alphabet) for _ in range(length))
    cases.append((f"seeded_random_{index}", value))

seen: set[str] = set()
deduplicated: list[tuple[str, str]] = []
for category, value in cases:
    if value not in seen:
        seen.add(value)
        deduplicated.append((category, value))

mismatches = []
digest = hashlib.sha256()
with RESULT_PATH.open("w", encoding="utf-8") as stream:
    for index, (category, value) in enumerate(deduplicated):
        expected = canonical(value)
        actual = candidate(value)
        equal = expected == actual
        record = {
            "index": index,
            "category": category,
            "input": value,
            "canonical": expected,
            "candidate": actual,
            "equal": equal,
        }
        line = json.dumps(record, ensure_ascii=True, sort_keys=True)
        stream.write(line + "\n")
        digest.update((line + "\n").encode())
        if not equal:
            mismatches.append(record)

print(f"canonical_path={CANONICAL_PATH}")
print(f"candidate_path={CANDIDATE_PATH}")
print(f"named_case_count={len(named_cases)}")
print("exhaustive_alphabet=" + repr(small_alphabet))
print("exhaustive_lengths=0..5")
print("random_seed=101_20260724")
print("seeded_random_requested=2000")
print(f"unique_case_count={len(deduplicated)}")
print(f"result_path={RESULT_PATH}")
print(f"result_sha256={digest.hexdigest()}")
print(f"mismatch_count={len(mismatches)}")
for category, value in named_cases:
    print(
        "named="
        + json.dumps(
            {
                "category": category,
                "input": value,
                "canonical": canonical(value),
                "candidate": candidate(value),
            },
            ensure_ascii=True,
            sort_keys=True,
        )
    )

raise SystemExit(1 if mismatches else 0)
