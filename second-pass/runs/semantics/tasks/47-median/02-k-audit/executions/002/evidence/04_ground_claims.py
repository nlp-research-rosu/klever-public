#!/usr/bin/env python3
"""Exhibit satisfying claim states and interpret each claimed result."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any, Callable


SCRATCH = Path("/tmp/audit-work/reconstruction")


def load(path: Path, name: str) -> Callable[[list], Any]:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.median


def py_mod(left: int, right: int) -> int:
    return ((left % right) + right) % right


def check(values: list[int], branch: str) -> dict[str, Any]:
    ordered = sorted(values)
    length = len(values)
    all_ints = all(type(item) is int for item in values)
    if branch == "odd":
        precondition = all_ints and length > 0 and py_mod(length, 2) == 1
        index = (length - 1) // 2
        interpreted_claim_result = ordered[index]
        formula = f"sorted(values)[({length}-1)//2]"
    elif branch == "even":
        precondition = all_ints and length >= 4 and py_mod(length, 2) == 0
        index = length // 2
        interpreted_claim_result = (ordered[index] + ordered[index + 1]) / 2.0
        formula = f"(sorted(values)[{length}//2] + sorted(values)[{length}//2+1]) / 2.0"
    else:
        raise ValueError(branch)
    candidate = load(SCRATCH / "solution.py", f"candidate_{branch}_{length}")
    canonical = load(SCRATCH / "canonical.py", f"canonical_{branch}_{length}")
    return {
        "branch": branch,
        "input": values,
        "allInts": all_ints,
        "length": length,
        "pyMod(length,2)": py_mod(length, 2),
        "precondition_satisfied": precondition,
        "formula": formula,
        "interpreted_claim_result": interpreted_claim_result,
        "candidate_python": candidate(list(values)),
        "canonical_python": canonical(list(values)),
    }


def main() -> int:
    records = [
        check([3, 1, 2], "odd"),
        check([4, 1, 3, 2], "even"),
        check([-10, 4, 6, 1000, 10, 20], "even"),
    ]
    for record in records:
        print(json.dumps(record, sort_keys=True))
    if not all(record["precondition_satisfied"] for record in records):
        print("RESULT FAIL: a witness does not satisfy its entry precondition")
        return 1
    print("RESULT PASS: every witness satisfies its entry precondition")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
