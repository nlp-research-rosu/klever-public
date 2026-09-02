#!/usr/bin/env python3
"""Satisfying witnesses for every submitted entry claim.

The reviewer supplies one ordinary witness for each claim and one additional
large-integer witness satisfying the submitted int-gt precondition.  The latter
exposes the exact-rational/generated-semantics mismatch with Python binary64
conversion.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any


WORK = Path("/tmp/audit-work/137-compare-one-audit")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.compare_one


def normalized(value: Any) -> dict[str, Any]:
    if isinstance(value, float):
        return {"type": "float", "hex": value.hex(), "repr": repr(value)}
    return {"type": type(value).__name__, "repr": repr(value)}


canonical = load(WORK / "trusted-canonical.py", "witness_canonical")
candidate = load(WORK / "solution.py", "witness_candidate")

witnesses = [
    {
        "claim": "int-eq",
        "precondition": "I == J",
        "bindings": {"I": 0, "J": 0},
        "python_args": (0, 0),
        "claimed_python_value": None,
    },
    {
        "claim": "int-gt",
        "precondition": "I > J",
        "bindings": {"I": 2, "J": 1},
        "python_args": (2, 1),
        "claimed_python_value": 2,
    },
    {
        "claim": "int-lt",
        "precondition": "I < J",
        "bindings": {"I": 1, "J": 2},
        "python_args": (1, 2),
        "claimed_python_value": 2,
    },
    {
        "claim": "float-eq",
        "precondition": "D1,D2 > 0 and N1*D2 == N2*D1",
        "bindings": {"N1": 1, "D1": 2, "N2": 2, "D2": 4},
        "python_args": (0.5, 0.5),
        "claimed_python_value": None,
    },
    {
        "claim": "float-gt",
        "precondition": "D1,D2 > 0 and N1*D2 > N2*D1",
        "bindings": {"N1": 3, "D1": 2, "N2": 1, "D2": 1},
        "python_args": (1.5, 1.0),
        "claimed_python_value": 1.5,
    },
    {
        "claim": "float-lt",
        "precondition": "D1,D2 > 0 and N1*D2 < N2*D1",
        "bindings": {"N1": 1, "D1": 1, "N2": 3, "D2": 2},
        "python_args": (1.0, 1.5),
        "claimed_python_value": 1.5,
    },
    {
        "claim": "example-1",
        "precondition": "ground initial configuration",
        "bindings": {},
        "python_args": (1, 2.5),
        "claimed_python_value": 2.5,
    },
    {
        "claim": "example-2",
        "precondition": "ground initial configuration",
        "bindings": {},
        "python_args": (1, "2,3"),
        "claimed_python_value": "2,3",
    },
    {
        "claim": "example-3",
        "precondition": "ground initial configuration",
        "bindings": {},
        "python_args": ("5,1", "6"),
        "claimed_python_value": "6",
    },
    {
        "claim": "example-4",
        "precondition": "ground initial configuration",
        "bindings": {},
        "python_args": ("1", 1),
        "claimed_python_value": None,
    },
    {
        "claim": "int-gt (counterexample witness)",
        "precondition": "I > J",
        "bindings": {"I": 9007199254740993, "J": 9007199254740992},
        "python_args": (9007199254740993, 9007199254740992),
        "claimed_python_value": 9007199254740993,
    },
]

records = []
for witness in witnesses:
    a, b = witness["python_args"]
    claimed = witness["claimed_python_value"]
    canonical_value = canonical(a, b)
    candidate_value = candidate(a, b)
    records.append(
        {
            "claim": witness["claim"],
            "precondition": witness["precondition"],
            "bindings": witness["bindings"],
            "python_args": [normalized(a), normalized(b)],
            "claimed_result": normalized(claimed),
            "canonical_result": normalized(canonical_value),
            "candidate_result": normalized(candidate_value),
            "claim_matches_canonical": (
                type(claimed) is type(canonical_value) and claimed == canonical_value
            ),
            "claim_matches_candidate": (
                type(claimed) is type(candidate_value) and claimed == candidate_value
            ),
        }
    )

print(json.dumps(records, indent=2, sort_keys=True))
print(
    "CLAIM_RESULT_MISMATCHES:",
    sum(not record["claim_matches_candidate"] for record in records),
)
