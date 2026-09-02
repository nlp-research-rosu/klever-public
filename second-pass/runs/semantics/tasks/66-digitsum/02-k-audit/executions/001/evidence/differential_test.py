#!/usr/bin/env python3
"""Independent differential test for HumanEval 66 digitSum."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
from pathlib import Path


TRUSTED = Path("/tmp/audit-work/66-digitsum.dlRQYF/trusted/canonical.py")
CANDIDATE = Path("/tmp/audit-work/66-digitsum.dlRQYF/candidate/solution.py")
INPUTS_OUT = Path("/audit-output/evidence/differential-inputs.json")
RESULTS_OUT = Path("/audit-output/evidence/differential-results.json")


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.digitSum


canonical = load_function(TRUSTED, "trusted_canonical")
candidate = load_function(CANDIDATE, "candidate_solution")

documented = ["", "abAB", "abcCd", "helloE", "woArBld", "aAaaaXa"]
branch_boundaries = [
    chr(code)
    for code in (0, 48, 64, 65, 66, 89, 90, 91, 96, 97, 122, 127)
]
unicode_cases = [
    "É",
    "Ω",
    "Ж",
    "Ａ",
    "𝐀",
    "éÉ",
    "aΩZ",
    "ǅ",  # titlecase: a useful isupper() negative control
]

small_alphabet = ["@", "A", "Z", "[", "a", "0", "é", "É"]
exhaustive_small = [
    "".join(chars)
    for length in range(5)
    for chars in itertools.product(small_alphabet, repeat=length)
]

rng = random.Random(660024)
random_alphabet = [
    chr(code)
    for code in (
        0,
        9,
        32,
        48,
        57,
        64,
        65,
        66,
        89,
        90,
        91,
        96,
        97,
        122,
        127,
        201,
        233,
        937,
        1046,
        65313,
        119808,
        128578,
    )
]
generated = [
    "".join(rng.choice(random_alphabet) for _ in range(rng.randrange(0, 33)))
    for _ in range(5000)
]

inputs = list(
    dict.fromkeys(
        documented
        + branch_boundaries
        + unicode_cases
        + exhaustive_small
        + generated
    )
)

records = []
for value in inputs:
    expected = canonical(value)
    actual = candidate(value)
    if expected != actual:
        records.append(
            {
                "input": value,
                "codepoints": [ord(char) for char in value],
                "canonical": expected,
                "candidate": actual,
            }
        )

INPUTS_OUT.write_text(
    json.dumps(
        {
            "documented": documented,
            "branch_boundaries": branch_boundaries,
            "unicode_cases": unicode_cases,
            "small_alphabet": small_alphabet,
            "exhaustive_small_lengths": [0, 1, 2, 3, 4],
            "random_seed": 660024,
            "random_alphabet_codepoints": [ord(char) for char in random_alphabet],
            "random_case_count": len(generated),
            "all_inputs": inputs,
        },
        indent=2,
        ensure_ascii=True,
    )
    + "\n",
    encoding="utf-8",
)
RESULTS_OUT.write_text(
    json.dumps(
        {
            "input_count": len(inputs),
            "mismatch_count": len(records),
            "mismatches": records,
        },
        indent=2,
        ensure_ascii=True,
    )
    + "\n",
    encoding="utf-8",
)

print(f"input_count={len(inputs)}")
print(f"mismatch_count={len(records)}")
for record in records[:20]:
    print(json.dumps(record, ensure_ascii=True, sort_keys=True))

raise SystemExit(1 if records else 0)
