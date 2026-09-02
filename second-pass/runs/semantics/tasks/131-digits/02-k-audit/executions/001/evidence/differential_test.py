#!/usr/bin/env python3
"""Independent differential test for HumanEval 131 `digits`.

Oracle: /tmp/audit-work/audit-131-digits/trusted/canonical.py
Candidate: /tmp/audit-work/audit-131-digits/candidate/solution.py
"""

from __future__ import annotations

import importlib.util
import json
import random
from pathlib import Path


WORK = Path("/tmp/audit-work/audit-131-digits")
EVIDENCE = Path("/audit-output/evidence")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def observe(function, argument):
    try:
        return {"kind": "return", "value": function(argument)}
    except Exception as error:  # evidence also records excluded-domain behavior
        return {"kind": "raise", "type": type(error).__name__, "message": str(error)}


canonical = load_module("trusted_canonical", WORK / "trusted" / "canonical.py")
candidate = load_module("generated_solution", WORK / "candidate" / "solution.py")

documented = [1, 4, 235]
branch_boundaries = [
    2,
    3,
    5,
    8,
    9,
    10,
    11,
    12,
    19,
    20,
    21,
    22,
    90,
    99,
    100,
    101,
    102,
    109,
    110,
    111,
    120,
    200,
    2468,
    10203,
    13579,
]
decimal_boundaries = []
for exponent in range(1, 81):
    power = 10**exponent
    decimal_boundaries.extend([power - 1, power, power + 1])

rng = random.Random(131)
generated = []
for _ in range(2000):
    digit_count = rng.randint(1, 120)
    lower = 1 if digit_count == 1 else 10 ** (digit_count - 1)
    upper = 10**digit_count - 1
    generated.append(rng.randint(lower, upper))

# Exhaustion of a substantial prefix reaches every control-flow combination
# many times; the other groups exercise large arbitrary-precision inputs.
intended_inputs = sorted(
    set(
        documented
        + branch_boundaries
        + decimal_boundaries
        + generated
        + list(range(1, 20001))
    )
)
outside_domain_inputs = [0, -1, -235]

(EVIDENCE / "differential_inputs.json").write_text(
    json.dumps(
        {
            "contract_domain": "positive Python integers",
            "documented": documented,
            "branch_boundaries": branch_boundaries,
            "decimal_boundaries": decimal_boundaries,
            "random_seed": 131,
            "random_count": len(generated),
            "exhaustive_prefix": [1, 20000],
            "all_intended_inputs": intended_inputs,
            "outside_domain_inputs": outside_domain_inputs,
        },
        indent=2,
    )
    + "\n",
    encoding="utf-8",
)

mismatches = []
for value in intended_inputs:
    expected = observe(canonical.digits, value)
    actual = observe(candidate.digits, value)
    if expected != actual:
        mismatches.append({"input": value, "canonical": expected, "candidate": actual})

print("ORACLE: trusted canonical.py:digits")
print("CANDIDATE: scratch-copied solution.py:digits")
print("INTENDED_DOMAIN: positive Python integers")
print(f"INTENDED_INPUT_COUNT: {len(intended_inputs)}")
print(f"INTENDED_MISMATCH_COUNT: {len(mismatches)}")
print("DOCUMENTED_AND_BRANCH_RESULTS:")
for value in documented + branch_boundaries:
    print(
        json.dumps(
            {
                "input": value,
                "canonical": observe(canonical.digits, value),
                "candidate": observe(candidate.digits, value),
            },
            sort_keys=True,
        )
    )
print("OUTSIDE_DOMAIN_RESULTS:")
for value in outside_domain_inputs:
    print(
        json.dumps(
            {
                "input": value,
                "canonical": observe(canonical.digits, value),
                "candidate": observe(candidate.digits, value),
            },
            sort_keys=True,
        )
    )
if mismatches:
    print("INTENDED_MISMATCHES:")
    for mismatch in mismatches[:100]:
        print(json.dumps(mismatch, sort_keys=True))
    raise SystemExit(1)
