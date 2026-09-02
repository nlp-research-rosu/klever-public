#!/usr/bin/env python3
"""Independent differential test of trusted canonical versus candidate source."""

from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import random
from pathlib import Path


EVIDENCE = Path("/audit-output/evidence/02-program-fidelity")
CANONICAL = Path("/reference/canonical.py")
CANDIDATE = Path("/tmp/audit-work/candidate-src/solution.py")


def load(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load(CANONICAL, "trusted_canonical_41")
candidate = load(CANDIDATE, "candidate_solution_41")

boundary = [
    0,  # empty fleet in each direction
    1,
    2,
    3,
    10,
    2**31 - 1,
    2**31,
    2**63 - 1,
    2**63,
    10**100,
]
negative_extension = [
    -1,
    -2,
    -3,
    -(2**31),
    -(2**63),
    -(10**100),
]
small_exhaustive = list(range(0, 257))
rng = random.Random(410041)
generated_nonnegative = [rng.randrange(0, 10**18) for _ in range(600)]
generated_negative = [-rng.randrange(1, 10**18) for _ in range(100)]
cases = list(
    dict.fromkeys(
        boundary
        + negative_extension
        + small_exhaustive
        + generated_nonnegative
        + generated_negative
    )
)

source_tree = ast.parse(CANDIDATE.read_text())
branch_nodes = sum(
    isinstance(
        node,
        (
            ast.If,
            ast.IfExp,
            ast.For,
            ast.While,
            ast.Match,
            ast.Try,
            ast.BoolOp,
        ),
    )
    for node in ast.walk(source_tree)
)
assert branch_nodes == 0

mismatches = []
rows = []
for n in cases:
    expected = canonical.car_race_collision(n)
    actual = candidate.car_race_collision(n)
    rows.append({"n": n, "canonical": expected, "candidate": actual})
    if expected != actual or type(expected) is not type(actual):
        mismatches.append(rows[-1])

input_document = {
    "oracle": str(CANONICAL),
    "candidate": str(CANDIDATE),
    "seed": 410041,
    "documented_examples": [],
    "note": "The trusted prompt contains no explicit examples.",
    "branch_nodes": branch_nodes,
    "cases": cases,
}
(EVIDENCE / "inputs.json").write_text(
    json.dumps(input_document, indent=2, sort_keys=True) + "\n"
)
(EVIDENCE / "results.json").write_text(
    json.dumps(
        {
            "case_count": len(rows),
            "mismatch_count": len(mismatches),
            "mismatches": mismatches,
            "rows": rows,
        },
        indent=2,
        sort_keys=True,
    )
    + "\n"
)

input_hash = hashlib.sha256(
    (EVIDENCE / "inputs.json").read_bytes()
).hexdigest()
print("trusted_oracle:", CANONICAL)
print("candidate_entry_point:", CANDIDATE)
print("documented_examples:", 0)
print("branch_nodes:", branch_nodes)
print("case_count:", len(cases))
print("nonnegative_cases:", sum(n >= 0 for n in cases))
print("negative_extension_cases:", sum(n < 0 for n in cases))
print("inputs_sha256:", input_hash)
print("mismatch_count:", len(mismatches))
if mismatches:
    print(json.dumps(mismatches[:20], indent=2))
    raise SystemExit(1)
print("DIFFERENTIAL_TEST: PASS")
