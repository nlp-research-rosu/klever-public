#!/usr/bin/env python3
"""Independent finite differential check for HumanEval/28 concatenate."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/28-concatenate")


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.concatenate


canonical = load_entry("trusted_humaneval28_canonical", SCRATCH / "canonical.py")
generated = load_entry("candidate_humaneval28_solution", SCRATCH / "solution.py")

# Named cases cover the two documented examples plus the zero-, one-, and
# many-iteration boundaries; empty pieces; embedded NUL/newline; Unicode; and
# a larger payload.
named_cases = [
    [],
    ["a", "b", "c"],
    [""],
    ["x"],
    ["", ""],
    ["a", "", "b"],
    ["", "prefix", ""],
    ["\0", "x\0y"],
    ["line\n", "break"],
    ["é", "中", "🙂"],
    ["a" * 4096, "", "b" * 4096],
]

# Exhaust all lists of length 0..4 over representative string atoms.
atoms = ["", "a", "bc", "\0", "é", "🙂", "line\nbreak"]
generated_cases = [
    list(items)
    for length in range(5)
    for items in itertools.product(atoms, repeat=length)
]

# Add deterministic broader cases with varied list and element lengths.
rng = random.Random(280028)
alphabet = ["", "a", "Z", "0", " ", "\n", "\0", "é", "中", "🙂"]
random_cases = []
for _ in range(2000):
    pieces = []
    for _ in range(rng.randrange(0, 21)):
        pieces.append("".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 17))))
    random_cases.append(pieces)

cases = named_cases + generated_cases + random_cases
mismatches = []
digest = hashlib.sha256()

for index, strings in enumerate(cases):
    before = list(strings)
    expected = canonical(strings)
    actual = generated(strings)
    if strings != before:
        mismatches.append(
            {"index": index, "input": before, "kind": "input-mutated", "after": strings}
        )
    if type(actual) is not str or actual != expected:
        mismatches.append(
            {
                "index": index,
                "input": strings,
                "expected": expected,
                "actual": actual,
                "actual_type": type(actual).__name__,
            }
        )
    digest.update(
        json.dumps([strings, expected, actual], ensure_ascii=True, separators=(",", ":")).encode()
    )

print(f"documented_cases=2")
print(f"named_cases={len(named_cases)}")
print(f"exhaustive_generated_cases={len(generated_cases)}")
print(f"seeded_random_cases={len(random_cases)}")
print(f"total_cases={len(cases)}")
print(f"mismatches={len(mismatches)}")
print(f"case_result_sha256={digest.hexdigest()}")
if mismatches:
    print(json.dumps(mismatches[:20], ensure_ascii=True, indent=2))
    raise SystemExit(1)
