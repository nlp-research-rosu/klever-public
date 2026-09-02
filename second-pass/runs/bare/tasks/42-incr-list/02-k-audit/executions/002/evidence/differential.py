#!/usr/bin/env python3
"""Independent differential check for HumanEval/42 over integer lists."""

import argparse
import importlib.util
import json
import random


def load_entry(path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.incr_list


parser = argparse.ArgumentParser()
parser.add_argument("canonical")
parser.add_argument("candidate")
args = parser.parse_args()

canonical = load_entry(args.canonical, "trusted_canonical")
candidate = load_entry(args.candidate, "generated_candidate")

cases = [
    ("example-1", [1, 2, 3]),
    ("example-2", [5, 3, 5, 2, 3, 3, 9, 0, 123]),
    ("loop-zero-iterations", []),
    ("loop-first-positive-boundary", [0]),
    ("singleton-negative", [-1]),
    ("singleton-huge-positive", [10**100]),
    ("singleton-huge-negative", [-(10**100)]),
    ("mixed-signs", [-5, -1, 0, 1, 5]),
    ("duplicates", [7, 7, 7, 7]),
    ("ordered-range", list(range(-10, 11))),
    ("alternating-large", [10**30, -(10**30)] * 8),
]

rng = random.Random(424242)
population = [
    -(10**80),
    -(10**20),
    -1000,
    -2,
    -1,
    0,
    1,
    2,
    999,
    10**20,
    10**80,
]
for length in [0, 1, 2, 3, 4, 7, 8, 15, 16, 31, 32, 64, 127]:
    for sample in range(3):
        values = [rng.choice(population) for _ in range(length)]
        cases.append((f"seed-424242-length-{length}-sample-{sample}", values))

mismatches = []
for name, values in cases:
    canonical_input = list(values)
    candidate_input = list(values)
    expected = canonical(canonical_input)
    actual = candidate(candidate_input)
    record = {
        "name": name,
        "input": values,
        "canonical": expected,
        "candidate": actual,
        "same_result": actual == expected,
        "canonical_input_unchanged": canonical_input == values,
        "candidate_input_unchanged": candidate_input == values,
        "canonical_fresh_list": expected is not canonical_input,
        "candidate_fresh_list": actual is not candidate_input,
    }
    print(json.dumps(record, sort_keys=True))
    if not all(
        [
            record["same_result"],
            record["canonical_input_unchanged"],
            record["candidate_input_unchanged"],
            record["canonical_fresh_list"],
            record["candidate_fresh_list"],
        ]
    ):
        mismatches.append(record)

print(
    json.dumps(
        {
            "case_count": len(cases),
            "domain": "finite Python lists whose elements are arbitrary Python integers",
            "generator": "random.Random(424242), fixed lengths and fixed edge population",
            "mismatch_count": len(mismatches),
        },
        sort_keys=True,
    )
)
raise SystemExit(1 if mismatches else 0)
