#!/usr/bin/env python3
"""Ground witnesses for every candidate claim and the universal precision counterexample."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.rounded_avg


candidate = load(
    Path("/tmp/audit-work/103-rounded-avg/candidate-src/solution.py"),
    "claim_witness_candidate",
)
canonical = load(Path("/reference/canonical.py"), "claim_witness_canonical")


def encode_python(value):
    if isinstance(value, int):
        return ("intVal", value)
    if isinstance(value, str) and (value.startswith("0b") or value.startswith("-0b")):
        return ("binVal", int(value, 2))
    return ("unexpected", type(value).__name__, repr(value))


def program_record(label, n, m, precondition, claimed):
    candidate_value = candidate(n, m)
    canonical_value = canonical(n, m)
    return {
        "claim": label,
        "state": {
            "k": f"boot(roundedAvgProgram,{n},{m})",
            "env": ".Map",
            "result": "noResult",
        },
        "n": n,
        "m": m,
        "precondition": bool(precondition),
        "claimed_K_result": claimed,
        "candidate_python": {
            "raw": repr(candidate_value),
            "abstract": encode_python(candidate_value),
        },
        "canonical_python": {
            "raw": repr(canonical_value),
            "abstract": encode_python(canonical_value),
        },
        "both_match_claim": (
            encode_python(candidate_value) == tuple(claimed)
            and encode_python(canonical_value) == tuple(claimed)
        ),
    }


records = [
    program_record("reversed", 7, 5, 7 > 0 and 5 > 0 and 7 > 5, ("intVal", -1)),
    program_record(
        "integral-midpoint",
        1,
        5,
        1 > 0 and 5 > 0 and 1 <= 5 and (1 + 5) % 2 == 0,
        ("binVal", (1 + 5) // 2),
    ),
    program_record(
        "half-even-down",
        2,
        3,
        2 > 0 and 3 > 0 and 2 <= 3 and (2 + 3) % 2 == 1 and ((2 + 3) // 2) % 2 == 0,
        ("binVal", (2 + 3) // 2),
    ),
    program_record(
        "half-even-up",
        1,
        2,
        1 > 0 and 2 > 0 and 1 <= 2 and (1 + 2) % 2 == 1 and ((1 + 2) // 2) % 2 == 1,
        ("binVal", (1 + 2) // 2 + 1),
    ),
    program_record("example-1-5", 1, 5, True, ("binVal", 3)),
    program_record("example-7-5", 7, 5, True, ("intVal", -1)),
    program_record("example-10-20", 10, 20, True, ("binVal", 15)),
    program_record("example-20-33", 20, 33, True, ("binVal", 26)),
]

precision_n = 2**53 + 1
records.append(
    program_record(
        "integral-midpoint-precision-counterexample",
        precision_n,
        precision_n,
        precision_n > 0
        and precision_n > 0
        and precision_n <= precision_n
        and (precision_n + precision_n) % 2 == 0,
        ("binVal", precision_n),
    )
)

render_records = []
for label, integer, expected in (
    ("render-3", 3, "0b11"),
    ("render-15", 15, "0b1111"),
    ("render-26", 26, "0b11010"),
):
    render_records.append(
        {
            "claim": label,
            "state": {
                "k": f"renderBinary(binVal({integer}))",
                "env": ".Map",
                "result": "noResult",
            },
            "precondition": True,
            "claimed_string": expected,
            "python_bin": bin(integer),
            "matches": bin(integer) == expected,
        }
    )

for record in records:
    print(json.dumps(record, sort_keys=True))
for record in render_records:
    print(json.dumps(record, sort_keys=True))

ordinary = records[:-1]
assert all(record["precondition"] for record in ordinary)
assert all(record["both_match_claim"] for record in ordinary)
assert all(record["precondition"] for record in render_records)
assert all(record["matches"] for record in render_records)
assert records[-1]["precondition"]
assert not records[-1]["both_match_claim"]
print(
    "summary "
    + json.dumps(
        {
            "ordinary_program_claim_witnesses": len(ordinary),
            "ordinary_matches": sum(record["both_match_claim"] for record in ordinary),
            "render_claim_witnesses": len(render_records),
            "render_matches": sum(record["matches"] for record in render_records),
            "precision_counterexample_precondition": records[-1]["precondition"],
            "precision_counterexample_matches": records[-1]["both_match_claim"],
        },
        sort_keys=True,
    )
)
