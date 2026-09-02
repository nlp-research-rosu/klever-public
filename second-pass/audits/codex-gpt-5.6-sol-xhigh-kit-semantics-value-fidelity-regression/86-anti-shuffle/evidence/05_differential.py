#!/usr/bin/env python3
"""Independent canonical-vs-candidate differential test for HumanEval/86."""

import importlib.util
import itertools
import json
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.anti_shuffle


canonical = load_entry("trusted_canonical_86", Path("/reference/canonical.py"))
candidate = load_entry(
    "audited_candidate_86",
    Path("/tmp/audit-work/anti-shuffle-audit/solution.py"),
)

# Named cases cover the examples and the branch boundaries in solution.py:
# outer space/non-space, empty/final word, inner-loop empty/nonempty,
# character<existing true/false/equal, inserted already true, and multiple words.
named_cases = [
    ("example_Hi", "Hi"),
    ("example_hello", "hello"),
    ("example_sentence", "Hello World!!!"),
    ("empty", ""),
    ("one_space", " "),
    ("leading_space", " ba"),
    ("trailing_space", "ba "),
    ("consecutive_spaces", "ba  dc"),
    ("all_spaces", "    "),
    ("single_nonspace", "x"),
    ("already_sorted", "!Aab"),
    ("reverse", "dcba"),
    ("less_true_then_inserted_true", "dabc"),
    ("less_false", "abcd"),
    ("equal_false_boundary", "baab"),
    ("punctuation", "z!A~"),
    ("control_codes", "\x00\n\t "),
    ("unicode_bmp", "éΩA"),
    ("unicode_astral", "😀A🂡"),
]

expected_examples = {
    "Hi": "Hi",
    "hello": "ehllo",
    "Hello World!!!": "Hello !!!Wdlor",
}

cases = []
seen = set()


def add_case(origin: str, value: str) -> None:
    if value not in seen:
        seen.add(value)
        cases.append((origin, value))


for tag, value in named_cases:
    add_case(tag, value)

# Exhaust the small strings that combine word separators, both order
# directions, equality, case, punctuation, NUL, and non-ASCII code points.
small_alphabet = [" ", "a", "b", "A", "!", "\x00", "é"]
for length in range(5):
    for chars in itertools.product(small_alphabet, repeat=length):
        add_case(f"exhaustive_len_{length}", "".join(chars))

# A broader deterministic representative sample.
rng = random.Random(860723)
random_alphabet = (
    " abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "0123456789!@#$%^&*()-_=+\t\n"
    "éΩ中😀"
)
for index in range(300):
    length = rng.randrange(0, 65)
    add_case(f"random_{index}", "".join(rng.choice(random_alphabet) for _ in range(length)))

mismatches = 0
exceptions = 0
for index, (origin, value) in enumerate(cases):
    record = {"index": index, "origin": origin, "input": value}
    try:
        expected = canonical(value)
        actual = candidate(value)
        record["canonical"] = expected
        record["candidate"] = actual
        record["match"] = (
            type(expected) is str and type(actual) is str and expected == actual
        )
        if not record["match"]:
            mismatches += 1
    except Exception as err:
        record["exception"] = f"{type(err).__name__}: {err}"
        record["match"] = False
        exceptions += 1
    print(json.dumps(record, ensure_ascii=True, sort_keys=True))

for source, expected in expected_examples.items():
    actual = candidate(source)
    if actual != expected:
        mismatches += 1
        print(
            json.dumps(
                {
                    "example_assertion": source,
                    "expected": expected,
                    "actual": actual,
                    "match": False,
                },
                ensure_ascii=True,
                sort_keys=True,
            )
        )

print(
    json.dumps(
        {
            "summary": {
                "total_unique_cases": len(cases),
                "named_case_count": len(named_cases),
                "exhaustive_alphabet": small_alphabet,
                "exhaustive_lengths": [0, 1, 2, 3, 4],
                "random_case_count": 300,
                "random_seed": 860723,
                "mismatches": mismatches,
                "exceptions": exceptions,
            }
        },
        ensure_ascii=True,
        sort_keys=True,
    )
)
raise SystemExit(1 if mismatches or exceptions else 0)
