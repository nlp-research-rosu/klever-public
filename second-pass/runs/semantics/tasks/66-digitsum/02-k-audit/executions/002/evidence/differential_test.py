#!/usr/bin/env python3
"""Independent differential test for HumanEval/66 digitSum."""

from __future__ import annotations

import importlib.util
import json
import random
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.digitSum


canonical = load_function("trusted_canonical", Path("/reference/canonical.py"))
candidate = load_function(
    "candidate_solution", Path("/tmp/audit-work/66-digitsum-audit/solution.py")
)


def contract_oracle(value: str) -> int:
    return sum(ord(char) for char in value if char.isupper())


documented = ["", "abAB", "abcCd", "helloE", "woArBld", "aAaaaXa"]
branch_boundaries = [chr(code) for code in (64, 65, 66, 89, 90, 91)]
representative = [
    "0123!@#$abcdefghijklmnopqrstuvwxyz",
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "AaZz09",
    "É",       # U+00C9: uppercase outside ASCII
    "é",
    "Ωω",      # U+03A9 is uppercase; U+03C9 is lowercase
    "Жж",      # U+0416 is uppercase; U+0436 is lowercase
    "İi",      # U+0130 is uppercase
    "ǅ",       # titlecase, but not uppercase according to str.isupper()
    "AÉΩЖZ",
]

rng = random.Random(660066)
ascii_pool = "".join(chr(code) for code in range(128))
unicode_pool = "".join(chr(code) for code in range(0x800))
generated_ascii = [
    "".join(rng.choice(ascii_pool) for _ in range(rng.randrange(0, 25)))
    for _ in range(500)
]
generated_unicode = [
    "".join(rng.choice(unicode_pool) for _ in range(rng.randrange(0, 25)))
    for _ in range(500)
]
single_codepoints = [chr(code) for code in range(0x800)]

groups = {
    "documented": documented,
    "branch_boundaries": branch_boundaries,
    "representative": representative,
    "generated_ascii_seed_660066": generated_ascii,
    "generated_unicode_seed_660066": generated_unicode,
    "single_codepoints_U+0000_to_U+07FF": single_codepoints,
}

records = []
oracle_disagreements = []
for group, values in groups.items():
    for value in values:
        expected = contract_oracle(value)
        canonical_result = canonical(value)
        candidate_result = candidate(value)
        if canonical_result != expected:
            oracle_disagreements.append(
                {
                    "group": group,
                    "input": value,
                    "canonical": canonical_result,
                    "oracle": expected,
                }
            )
        if candidate_result != canonical_result:
            records.append(
                {
                    "group": group,
                    "input": value,
                    "codepoints": [f"U+{ord(c):04X}" for c in value],
                    "canonical": canonical_result,
                    "candidate": candidate_result,
                }
            )

print("COMMAND: python3 /audit-output/evidence/differential_test.py")
print("ENTRY_POINTS: /reference/canonical.py::digitSum vs "
      "/tmp/audit-work/66-digitsum-audit/solution.py::digitSum")
print("ORACLE: sum(ord(c) for c in s if c.isupper())")
print("INPUT_GROUP_SIZES=" + json.dumps({k: len(v) for k, v in groups.items()}))
print(f"TOTAL_CASES={sum(len(v) for v in groups.values())}")
print(f"CANONICAL_ORACLE_MISMATCHES={len(oracle_disagreements)}")
print(f"CANDIDATE_CANONICAL_MISMATCHES={len(records)}")
print("FIRST_20_MISMATCHES=" + json.dumps(records[:20], ensure_ascii=True))
print("DOCUMENTED_RESULTS=" + json.dumps([
    {
        "input": value,
        "canonical": canonical(value),
        "candidate": candidate(value),
    }
    for value in documented
], ensure_ascii=True))
print("BOUNDARY_RESULTS=" + json.dumps([
    {
        "input": value,
        "codepoint": f"U+{ord(value):04X}",
        "isupper": value.isupper(),
        "canonical": canonical(value),
        "candidate": candidate(value),
    }
    for value in branch_boundaries + ["É", "Ω", "Ж", "İ", "ǅ"]
], ensure_ascii=True))
print("EXPECTED_DIFFERENTIAL_FOUND=" + str(bool(records)))
print("EXIT_STATUS=0")
