#!/usr/bin/env python3
"""Independent canonical-versus-candidate differential test for HumanEval 142."""

from __future__ import annotations

import importlib.util
from itertools import product
import json
from pathlib import Path
import random
import sys


REFERENCE_PATH = Path("/reference/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/142-sum-squares/solution.py")
INPUT_RECORD = Path("/audit-output/evidence/differential-inputs.jsonl")


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sum_squares


canonical = load_entry("trusted_humaneval_142", REFERENCE_PATH)
generated = load_entry("submitted_humaneval_142", GENERATED_PATH)


def proof_postcondition(values: list[int]) -> int:
    """Executable ground instance of sumSquares(VS, 0, 0)."""
    accumulator = 0
    for index, value in enumerate(values):
        if index % 3 == 0:
            contribution = value * value
        elif index % 4 == 0:
            contribution = value * value * value
        else:
            contribution = value
        accumulator += contribution
    return accumulator


curated: list[tuple[str, list[int]]] = [
    ("prompt-example-1", [1, 2, 3]),
    ("prompt-example-empty", []),
    ("prompt-example-negative", [-1, -5, 2, -1, -5]),
    ("index-0-square", [-3]),
    ("before-index-3", [2, -2, 3]),
    ("index-3-square", [2, -2, 3, -4]),
    ("index-4-cube", [2, -2, 3, -4, -5]),
    ("index-6-square", [1, 1, 1, 1, 1, 1, -2]),
    ("index-8-cube", [1, 1, 1, 1, 1, 1, 1, 1, -2]),
    ("index-9-square", [1, 1, 1, 1, 1, 1, 1, 1, 1, -2]),
    ("index-12-overlap-prefers-square", [1] * 12 + [-3]),
    ("large-magnitudes", [10**30, -(10**20), 0, -(10**15), 10**12]),
]

cases: list[tuple[str, list[int]]] = list(curated)
for length in range(7):
    for values in product(range(-2, 3), repeat=length):
        cases.append((f"exhaustive-length-{length}", list(values)))

generator = random.Random(142_20260723)
for case_number in range(500):
    length = generator.randrange(0, 41)
    values = [generator.randrange(-20, 21) for _ in range(length)]
    cases.append((f"generated-{case_number}", values))

mismatches: list[dict[str, object]] = []
mutation_failures: list[dict[str, object]] = []
with INPUT_RECORD.open("w", encoding="utf-8") as record:
    for case_number, (source, values) in enumerate(cases):
        canonical_argument = list(values)
        generated_argument = list(values)
        expected = canonical(canonical_argument)
        actual = generated(generated_argument)
        claimed = proof_postcondition(list(values))
        row = {
            "case": case_number,
            "source": source,
            "values": values,
            "canonical": expected,
            "generated": actual,
            "proof_postcondition_ground": claimed,
        }
        record.write(json.dumps(row, separators=(",", ":")) + "\n")
        if expected != actual or expected != claimed:
            mismatches.append(row)
        if canonical_argument != values or generated_argument != values:
            mutation_failures.append(
                {
                    "case": case_number,
                    "source": source,
                    "before": values,
                    "canonical_after": canonical_argument,
                    "generated_after": generated_argument,
                }
            )

print(f"reference={REFERENCE_PATH}")
print(f"generated={GENERATED_PATH}")
print(f"input-record={INPUT_RECORD}")
print(f"curated={len(curated)}")
print("exhaustive-domain=lengths 0..6, elements -2..2")
print("generated-domain=500 cases, seed 142_20260723, lengths 0..40, elements -20..20")
print(f"total-cases={len(cases)}")
print(f"mismatches={len(mismatches)}")
print(f"input-mutations={len(mutation_failures)}")
for source, values in curated:
    print(
        "WITNESS "
        + json.dumps(
            {
                "source": source,
                "values": values,
                "canonical": canonical(list(values)),
                "generated": generated(list(values)),
                "proof_postcondition_ground": proof_postcondition(list(values)),
            },
            separators=(",", ":"),
        )
    )

if mismatches:
    print("FIRST_MISMATCHES")
    for mismatch in mismatches[:20]:
        print(json.dumps(mismatch, separators=(",", ":")))
if mutation_failures:
    print("FIRST_INPUT_MUTATIONS")
    for mutation in mutation_failures[:20]:
        print(json.dumps(mutation, separators=(",", ":")))
sys.exit(1 if mismatches or mutation_failures else 0)
