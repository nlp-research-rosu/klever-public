#!/usr/bin/env python3
"""Independent candidate/canonical differential for HumanEval/96."""

from __future__ import annotations

import importlib.util
import json
import random
from pathlib import Path


def load(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load(
    Path("/tmp/audit-work/96-count-up-to/trusted/canonical.py"),
    "trusted_canonical",
)
candidate = load(
    Path("/tmp/audit-work/96-count-up-to/candidate/solution.py"),
    "generated_candidate",
)

documented = [5, 11, 0, 20, 1, 18]
branch_boundaries = list(range(0, 26))
fixed_representatives = [
    29,
    30,
    31,
    32,
    48,
    49,
    50,
    97,
    98,
    99,
    100,
    127,
    128,
    199,
    200,
    499,
    500,
    997,
    1000,
]
rng = random.Random(960026)
generated = [rng.randrange(0, 1001) for _ in range(64)]
inputs = list(
    dict.fromkeys(documented + branch_boundaries + fixed_representatives + generated)
)

mismatches = []
summaries = []
for n in inputs:
    expected = canonical.count_up_to(n)
    actual = candidate.count_up_to(n)
    if actual != expected:
        mismatches.append({"n": n, "canonical": expected, "candidate": actual})
    summaries.append(
        {
            "n": n,
            "count": len(actual),
            "first": actual[:5],
            "last": actual[-5:],
        }
    )

result = {
    "contract_domain": "all non-negative Python integers",
    "documented": documented,
    "branch_boundaries": branch_boundaries,
    "fixed_representatives": fixed_representatives,
    "generated_seed": 960026,
    "generated_inputs": generated,
    "unique_input_count": len(inputs),
    "mismatch_count": len(mismatches),
    "mismatches": mismatches,
    "summaries": summaries,
}
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(1 if mismatches else 0)
