#!/usr/bin/env python3
"""Ground witnesses for every candidate claim precondition and conclusion."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.make_a_pile


def pile_from(n: int, i: int) -> list[int]:
    result: list[int] = []
    while i < n:
        result.append(n + 2 * i)
        i += 1
    return result


canonical = load_function("trusted_canonical_claims", Path("/reference/canonical.py"))
candidate = load_function("candidate_claims", Path("/candidate/solution.py"))
records: list[dict[str, object]] = []

n = 1
records.append(
    {
        "claim": "invariant-initialization",
        "witness": {"N": n},
        "precondition": n > 0,
        "rhs_env": {"i": n - 1, "n": n, "result": pile_from(n, n)},
        "expected_rhs_env": {"i": 0, "n": 1, "result": []},
    }
)

n, i = 3, 1
starting_result = pile_from(n, i + 1)
after_body_result = [n + 2 * i] + starting_result
records.append(
    {
        "claim": "invariant-preservation",
        "witness": {"N": n, "I": i},
        "precondition": n > 0 and i >= 0 and i < n,
        "starting_result": starting_result,
        "after_body_env": {"i": i - 1, "n": n, "result": after_body_result},
        "claimed_rhs_env": {"i": i - 1, "n": n, "result": pile_from(n, i)},
    }
)

n = 1
records.append(
    {
        "claim": "invariant-exit",
        "witness": {"N": n},
        "precondition": n > 0,
        "returned": pile_from(n, 0),
        "canonical": canonical(n),
        "candidate": candidate(n),
    }
)

n, i = 3, 2
accumulator = pile_from(n, i + 1)
cursor = i
while cursor >= 0:
    accumulator = [n + 2 * cursor] + accumulator
    cursor -= 1
records.append(
    {
        "claim": "loop-invariant",
        "witness": {"N": n, "I": i},
        "precondition": n > 0 and i >= -1 and i < n,
        "returned": accumulator,
        "final_i": cursor,
        "claimed": pile_from(n, 0),
        "canonical": canonical(n),
        "candidate": candidate(n),
    }
)

n = 3
records.append(
    {
        "claim": "functional-correctness",
        "witness": {"N": n},
        "precondition": n > 0,
        "claimed": pile_from(n, 0),
        "canonical": canonical(n),
        "candidate": candidate(n),
    }
)

failures = 0
for record in records:
    claim = record["claim"]
    if not record["precondition"]:
        failures += 1
    if claim == "invariant-initialization":
        failures += int(record["rhs_env"] != record["expected_rhs_env"])
    elif claim == "invariant-preservation":
        failures += int(record["after_body_env"] != record["claimed_rhs_env"])
    else:
        failures += int(
            not (record["returned"] if "returned" in record else record["claimed"])
            == record["canonical"]
            == record["candidate"]
        )
    print(json.dumps(record, sort_keys=True))

print(json.dumps({"claim_witnesses": len(records), "failures": failures}, sort_keys=True))
sys.exit(1 if failures else 0)
