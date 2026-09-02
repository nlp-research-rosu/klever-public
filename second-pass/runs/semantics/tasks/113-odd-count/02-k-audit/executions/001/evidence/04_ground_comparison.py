#!/usr/bin/env python3
"""Ground witnesses for all claim preconditions and the entry postcondition."""

import importlib.util
from pathlib import Path


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, Path(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("canonical_ground", "/reference/canonical.py")
generated = load("generated_ground", "/tmp/audit-work/audit-113/solution.py")

states = {
    "digit-loop": {
        "CS": [49],
        "N": 0,
        "precondition": "allDigit(iCons(49,.IntSeq)) = true",
    },
    "outer-empty": {
        "input": [],
        "precondition": "none (therefore satisfiable)",
    },
    "outer-loop": {
        "CS": [49],
        "REST": [],
        "precondition": (
            "allDigit(iCons(49,.IntSeq)) andBool "
            "validDigitStrings(.ValSeq) = true"
        ),
    },
    "target": {
        "input": ["1"],
        "formal_input": (
            "vCons(str(iCons(49,.IntSeq)),.ValSeq)"
        ),
        "precondition": "validDigitStrings(formal_input) = true",
    },
}

expected_literal = (
    "the number of odd elements 1n the str1ng 1 of the 1nput."
)
canonical_result = canonical.odd_count(["1"])
generated_result = generated.odd_count(["1"])

print(f"satisfying_states={states!r}")
print("formal_ground_reduction=oddCountSpec([str([49])]) -> [oddText(1)]")
print(f"intended_literal={expected_literal!r}")
print(f"canonical_result={canonical_result!r}")
print(f"generated_result={generated_result!r}")
print(f"canonical_matches_literal={canonical_result == [expected_literal]}")
print(f"generated_matches_literal={generated_result == [expected_literal]}")
if canonical_result != [expected_literal] or generated_result != [expected_literal]:
    raise SystemExit(1)
print("EXIT_STATUS=0")
