#!/usr/bin/env python3
"""Independent canonical-vs-generated differential test for HumanEval 12."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path
from types import ModuleType


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module("trusted_canonical", Path("/reference/canonical.py"))
generated = load_module("candidate_solution", Path("/candidate/solution.py"))

documented_and_boundaries: list[tuple[str, list[str]]] = [
    ("documented-empty", []),
    ("documented-tie", ["a", "b", "c"]),
    ("documented-increasing", ["a", "bb", "ccc"]),
    ("singleton-empty-string", [""]),
    ("singleton-nonempty", ["abc"]),
    ("strictly-longer-second", ["a", "bb"]),
    ("strictly-shorter-second", ["bb", "a"]),
    ("equal-length-second", ["aa", "bb"]),
    ("late-strictly-longer", ["aaa", "", "bbbb"]),
    ("late-tie-retains-first", ["first", "x", "later"]),
    ("all-empty-tie", ["", "", ""]),
    ("unicode-codepoints", ["é", "ab", "🧪"]),
    ("non-bmp-tie", ["🧪x", "ab", "yz"]),
]

atom_pool = ["", "a", "bb", "é", "🧪", "xyz"]
exhaustive_cases = [
    list(case)
    for length in range(0, 6)
    for case in itertools.product(atom_pool, repeat=length)
]

rng = random.Random(120012)
alphabet = ["a", "b", "é", "🧪", "\x00", "\n"]
random_cases: list[list[str]] = []
for _ in range(2000):
    case = [
        "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 17)))
        for _ in range(rng.randrange(0, 13))
    ]
    random_cases.append(case)

all_cases = [case for _, case in documented_and_boundaries]
all_cases.extend(exhaustive_cases)
all_cases.extend(random_cases)
serialized = json.dumps(all_cases, ensure_ascii=True, separators=(",", ":")).encode()

mismatches: list[dict[str, object]] = []
for index, case in enumerate(all_cases):
    expected = canonical.longest(case)
    actual = generated.longest(case)
    if actual != expected:
        mismatches.append(
            {"index": index, "input": case, "canonical": expected, "generated": actual}
        )

for label, case in documented_and_boundaries:
    print(
        json.dumps(
            {
                "label": label,
                "input": case,
                "canonical": canonical.longest(case),
                "generated": generated.longest(case),
            },
            ensure_ascii=True,
            sort_keys=True,
        )
    )

print(
    json.dumps(
        {
            "explicit_cases": len(documented_and_boundaries),
            "exhaustive_scope": {
                "atom_pool": atom_pool,
                "list_lengths": [0, 1, 2, 3, 4, 5],
                "case_count": len(exhaustive_cases),
            },
            "random_scope": {
                "seed": 120012,
                "alphabet": alphabet,
                "list_length_range": [0, 12],
                "string_length_range": [0, 16],
                "case_count": len(random_cases),
            },
            "all_inputs_sha256": hashlib.sha256(serialized).hexdigest(),
            "total_cases": len(all_cases),
            "mismatch_count": len(mismatches),
            "first_mismatches": mismatches[:20],
        },
        ensure_ascii=True,
        sort_keys=True,
    )
)
raise SystemExit(1 if mismatches else 0)
