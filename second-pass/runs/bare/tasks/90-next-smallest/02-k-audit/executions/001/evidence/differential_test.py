#!/usr/bin/env python3
"""Independent differential test of trusted canonical.py versus solution.py."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.next_smallest


def main() -> int:
    if len(sys.argv) != 4:
        print(
            f"usage: {Path(sys.argv[0]).name} CANONICAL.py SOLUTION.py RESULTS.json",
            file=sys.stderr,
        )
        return 2

    canonical_path, solution_path, output_path = map(Path, sys.argv[1:])
    canonical = load_entry(canonical_path, "trusted_canonical")
    generated = load_entry(solution_path, "submitted_solution")

    documented = [
        [1, 2, 3, 4, 5],
        [5, 1, 4, 3, 2],
        [],
        [1, 1],
    ]
    branch_boundaries = [
        [7],
        [7, 7, 7],
        [1, 2],
        [2, 1],
        [-2, -1],
        [-1, -2],
        [0, -1, -1, 0],
        [3, 1, 2, 1],
        [-1, -4, -4, -2],
        [2, 2, 1, 3, 1],
        [10**100, -(10**100), 0],
    ]
    exhaustive = [
        list(values)
        for length in range(6)
        for values in itertools.product(range(-2, 3), repeat=length)
    ]
    rng = random.Random(9020260723)
    generated_cases = [
        [rng.randint(-100, 100) for _ in range(rng.randint(0, 20))]
        for _ in range(500)
    ]

    cases: list[tuple[str, list[int]]] = []
    cases.extend(("documented", case) for case in documented)
    cases.extend(("branch-boundary", case) for case in branch_boundaries)
    cases.extend(("exhaustive-small", case) for case in exhaustive)
    cases.extend(("generated-seeded", case) for case in generated_cases)

    rows = []
    mismatch_count = 0
    for category, values in cases:
        expected = canonical(values.copy())
        actual = generated(values.copy())
        mismatch = expected != actual or type(expected) is not type(actual)
        mismatch_count += int(mismatch)
        rows.append(
            {
                "category": category,
                "input": values,
                "canonical": expected,
                "solution": actual,
                "mismatch": mismatch,
            }
        )

    serialized_cases = json.dumps(
        [row["input"] for row in rows], separators=(",", ":"), ensure_ascii=False
    ).encode()
    report = {
        "oracle": str(canonical_path),
        "subject": str(solution_path),
        "scope": {
            "documented": len(documented),
            "branch_boundary": len(branch_boundaries),
            "exhaustive_small": len(exhaustive),
            "generated_seeded": len(generated_cases),
            "generated_seed": 9020260723,
            "total": len(rows),
        },
        "ordered_inputs_sha256": hashlib.sha256(serialized_cases).hexdigest(),
        "mismatch_count": mismatch_count,
        "cases": rows,
    }
    output_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({key: report[key] for key in report if key != "cases"}, indent=2))
    if mismatch_count:
        for row in rows:
            if row["mismatch"]:
                print("MISMATCH " + json.dumps(row, ensure_ascii=False))
        return 1
    print("all differential cases matched")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
