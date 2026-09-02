#!/usr/bin/env python3
"""Independent canonical-versus-submission differential test for HumanEval 108."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
from pathlib import Path


CANONICAL_PATH = Path("/tmp/audit-work/audit-108/trusted/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/audit-108/source/solution.py")
INPUT_LOG = Path("/audit-output/evidence/differential_inputs.jsonl")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module("trusted_canonical_108", CANONICAL_PATH)
generated = load_module("generated_solution_108", GENERATED_PATH)

documented = [
    ([], 0),
    ([-1, 11, -11], 1),
    ([1, 1, 2], 3),
]

boundaries = [
    [],
    [0],
    [-1],
    [1],
    [-9, -10, -11, -12],
    [9, 10, 11],
    [-100, -99, -20, -19, -11, -10, -9, -1, 0, 1, 9, 10, 11, 19, 20, 99, 100],
    [0, 10, -10, 123, -123],
    [-12, -21, -123, -999, 100, -100],
    [10**100, -(10**100), 10**100 - 1, -(10**100 - 1)],
]

branch_values = [-101, -100, -99, -12, -11, -10, -9, -1, 0, 1, 9, 10, 11, 12, 99, 100, 101]
exhaustive = [
    list(values)
    for length in range(4)
    for values in itertools.product(branch_values, repeat=length)
]

rng = random.Random(108_2026)
generated_cases = []
for _ in range(2000):
    length = rng.randrange(0, 13)
    case = []
    for _ in range(length):
        selector = rng.randrange(4)
        if selector == 0:
            case.append(rng.choice(branch_values))
        elif selector == 1:
            case.append(rng.randint(-10**6, 10**6))
        elif selector == 2:
            case.append(rng.randint(-10**30, 10**30))
        else:
            digits = rng.randrange(1, 81)
            magnitude = rng.randrange(10 ** (digits - 1), 10**digits)
            case.append(magnitude if rng.randrange(2) else -magnitude)
    generated_cases.append(case)

all_cases = []
seen = set()
for source, cases in [
    ("documented", [case for case, _ in documented]),
    ("boundary", boundaries),
    ("exhaustive", exhaustive),
    ("generated", generated_cases),
]:
    for case in cases:
        key = tuple(case)
        if key not in seen:
            seen.add(key)
            all_cases.append((source, case))

with INPUT_LOG.open("w", encoding="utf-8") as stream:
    for index, (source, case) in enumerate(all_cases):
        stream.write(json.dumps({"index": index, "source": source, "arr": case}))
        stream.write("\n")

for case, expected in documented:
    canonical_result = canonical.count_nums(case)
    generated_result = generated.count_nums(case)
    if canonical_result != expected or generated_result != expected:
        raise AssertionError(
            f"documented mismatch case={case!r} expected={expected} "
            f"canonical={canonical_result} generated={generated_result}"
        )

mismatches = []
for index, (source, case) in enumerate(all_cases):
    canonical_result = canonical.count_nums(case)
    generated_result = generated.count_nums(case)
    if canonical_result != generated_result:
        mismatches.append(
            {
                "index": index,
                "source": source,
                "arr": case,
                "canonical": canonical_result,
                "generated": generated_result,
            }
        )
        if len(mismatches) >= 20:
            break

print(f"canonical={CANONICAL_PATH}")
print(f"generated={GENERATED_PATH}")
print("documented_examples=3 all_expected_values_match=true")
print(f"boundary_cases={len(boundaries)}")
print(f"branch_values={branch_values}")
print("exhaustive_lengths=0..3")
print(f"exhaustive_cases={len(exhaustive)}")
print("random_seed=1082026")
print("generated_case_count=2000 generated_lengths=0..12 generated_integer_digits=1..80")
print(f"unique_total_cases={len(all_cases)}")
print(f"input_log={INPUT_LOG}")
print(f"mismatch_count={len(mismatches)}")
if mismatches:
    print(json.dumps(mismatches, indent=2))
    raise SystemExit(1)
