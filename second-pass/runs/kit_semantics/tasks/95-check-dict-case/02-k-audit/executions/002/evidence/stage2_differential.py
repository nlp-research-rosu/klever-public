#!/usr/bin/env python3
"""Independent docstring-first differential for HumanEval/95.

Oracle construction is intentionally separate from both implementations:
for a nonempty plain dict, every key must be a string and either every key
satisfies str.islower() or every key satisfies str.isupper().
"""

from __future__ import annotations

from itertools import product
import importlib.util
import random
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.check_dict_case


def contract_oracle(mapping: dict) -> bool:
    keys = list(mapping.keys())
    if not keys:
        return False
    all_lower = all(isinstance(key, str) and key.islower() for key in keys)
    all_upper = all(isinstance(key, str) and key.isupper() for key in keys)
    return all_lower or all_upper


candidate = load_function(
    "audited_candidate",
    Path("/tmp/audit-work/case95/candidate-src/solution.py"),
)
canonical = load_function(
    "trusted_canonical",
    Path("/tmp/audit-work/case95/trusted/canonical.py"),
)

documented = [
    {"a": "apple", "b": "banana"},
    {"a": "apple", "A": "banana", "B": "banana"},
    {"a": "apple", 8: "banana"},
    {"Name": "John", "Age": "36", "City": "Houston"},
    {"STATE": "NC", "ZIP": "12345"},
]

boundaries = [
    {},
    {"a": 0},
    {"A": 0},
    {"a": 0, "b": 0, 8: 0},
    {"A": 0, "B": 0, 8: 0},
    {"a": 0, "b": 0, "C": 0},
    {"A": 0, "B": 0, "c": 0},
    {"a": 0, "A": 0},
    {8: 0},
    {"": 0},
    {"1": 0},
    {"-": 0},
    {"a1": 0},
    {"A1": 0},
    {"é": 0},
    {"É": 0},
    {"ß": 0},
    {"中": 0},
    {b"a": 0},
    {("a",): 0},
    {None: 0},
]

# Exhaust every insertion sequence through length four over a branch-oriented
# pool. Repeated/equal keys deliberately exercise real dict de-duplication.
key_pool = [
    "a",
    "b",
    "A",
    "B",
    "Name",
    "",
    "1",
    "a1",
    "A1",
    "é",
    "É",
    "中",
    0,
    8,
    None,
    b"a",
    ("a",),
]
exhaustive = []
for length in range(5):
    for sequence in product(key_pool, repeat=length):
        exhaustive.append({key: index for index, key in enumerate(sequence)})

# Deterministic broader sample over arbitrary short strings and ordinary
# non-string hashable keys.
rng = random.Random(950095)
alphabet = "abABzZ09_-éÉß中"
generated = []
for _ in range(5000):
    mapping = {}
    for index in range(rng.randrange(0, 9)):
        kind = rng.randrange(5)
        if kind == 0:
            key = "".join(
                rng.choice(alphabet) for _ in range(rng.randrange(0, 7))
            )
        elif kind == 1:
            key = rng.randrange(-5, 12)
        elif kind == 2:
            key = None
        elif kind == 3:
            key = bytes([rng.randrange(0, 128)])
        else:
            key = (rng.randrange(-2, 3),)
        mapping[key] = index
    generated.append(mapping)

groups = [
    ("documented", documented),
    ("boundaries", boundaries),
    ("exhaustive_sequences", exhaustive),
    ("generated", generated),
]

candidate_mismatches = []
canonical_mismatches = []
candidate_mismatch_count = 0
canonical_mismatch_count = 0
total = 0
for group_name, cases in groups:
    group_candidate = 0
    group_canonical = 0
    for mapping in cases:
        expected = contract_oracle(mapping)
        got_candidate = candidate(mapping)
        got_canonical = canonical(mapping)
        total += 1
        if type(got_candidate) is not bool or got_candidate != expected:
            group_candidate += 1
            candidate_mismatch_count += 1
            if len(candidate_mismatches) < 20:
                candidate_mismatches.append(
                    (group_name, mapping, expected, got_candidate)
                )
        if type(got_canonical) is not bool or got_canonical != expected:
            group_canonical += 1
            canonical_mismatch_count += 1
            if len(canonical_mismatches) < 20:
                canonical_mismatches.append(
                    (group_name, mapping, expected, got_canonical)
                )
    print(
        f"GROUP {group_name} cases={len(cases)} "
        f"candidate_mismatches={group_candidate} "
        f"canonical_mismatches={group_canonical}"
    )

for index, mapping in enumerate(documented, start=1):
    print(
        f"DOCUMENTED {index} input={mapping!r} expected={contract_oracle(mapping)!r} "
        f"candidate={candidate(mapping)!r} canonical={canonical(mapping)!r}"
    )

print(f"TOTAL cases={total} candidate_mismatches={candidate_mismatch_count}")
for row in candidate_mismatches:
    print("CANDIDATE_MISMATCH", repr(row))
print("CANONICAL_MISMATCH_COUNT", canonical_mismatch_count)
for row in canonical_mismatches:
    print("CANONICAL_MISMATCH_SAMPLE", repr(row))

if candidate_mismatch_count:
    raise SystemExit(1)
