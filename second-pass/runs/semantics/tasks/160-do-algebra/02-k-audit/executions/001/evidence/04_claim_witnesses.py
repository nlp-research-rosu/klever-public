#!/usr/bin/env python3
"""Ground witnesses for every entry claim, checked against both Python programs."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Callable


def entry(path: str, name: str) -> Callable[[list[str], list[int]], int]:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.do_algebra


def main() -> int:
    canonical = entry("/reference/canonical.py", "witness_canonical")
    candidate = entry("/candidate/solution.py", "witness_candidate")
    witnesses = [
        ("plus", ["+"], [2, 3], 5),
        ("minus", ["-"], [2, 3], -1),
        ("times", ["*"], [2, 3], 6),
        ("floor", ["//"], [7, 3], 2),
        ("power", ["**"], [2, 5], 32),
        ("minus-assoc", ["-", "-"], [20, 5, 3], 12),
        ("floor-assoc", ["//", "//"], [20, 3, 2], 3),
        ("power-assoc", ["**", "**"], [2, 3, 2], 512),
        ("prompt-precedence", ["+", "*", "-"], [2, 3, 4, 5], 9),
        ("mixed-precedence", ["+", "*", "**", "//", "-"], [4, 3, 2, 3, 5, 1], 7),
    ]
    records = []
    failures = 0
    for label, operators, operands, claimed in witnesses:
        oracle = canonical(operators, operands)
        actual = candidate(operators, operands)
        passed = oracle == actual == claimed
        failures += int(not passed)
        records.append(
            {
                "claim": label,
                "operators": operators,
                "operands": operands,
                "claimed_result": claimed,
                "canonical_result": oracle,
                "candidate_result": actual,
                "precondition_satisfied": True,
                "match": passed,
            }
        )
    output = {"witness_count": len(records), "failure_count": failures, "witnesses": records}
    Path("/audit-output/evidence/04_claim_witnesses.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(output, indent=2, sort_keys=True))
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
