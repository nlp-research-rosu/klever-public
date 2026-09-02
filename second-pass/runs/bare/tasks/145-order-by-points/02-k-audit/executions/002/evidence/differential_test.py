#!/usr/bin/env python3
"""Independent differential test of canonical.py against candidate solution.py."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.order_by_points


def main() -> int:
    canonical = load_function(Path("/reference/canonical.py"), "trusted_canonical")
    candidate = load_function(
        Path("/tmp/audit-work/reconstruction/solution.py"), "candidate_solution"
    )

    directed = [
        [1, 11, -1, -11, -12],
        [],
        [0],
        [-1],
        [1],
        [-10, 10, 0, -9, 9],
        [12, 21, -12, 3],
        [5, 5, -5, -5, 14, 41, -14, -41],
        [99, 100, -99, -100, 10, -10],
        [10**100, -(10**100), 10**100 - 1, -(10**100 - 1)],
        [2, 11, 20, 101, -2, -11, -20, -101],
        list(range(-40, 41)),
        list(range(40, -41, -1)),
    ]

    seed = 145_2026_0726
    rng = random.Random(seed)
    generated = []
    for _ in range(5000):
        length = rng.randrange(0, 41)
        generated.append([rng.randint(-(10**12), 10**12) for _ in range(length)])
    cases = directed + generated

    serialized = json.dumps(cases, separators=(",", ":")).encode()
    case_sha = hashlib.sha256(serialized).hexdigest()
    mismatches = []
    for index, nums in enumerate(cases):
        expected = canonical(list(nums))
        actual = candidate(list(nums))
        if actual != expected:
            mismatches.append((index, nums, expected, actual))
            if len(mismatches) == 20:
                break

    print(f"directed_cases={len(directed)}")
    for index, case in enumerate(directed):
        print(
            f"directed[{index}] input={case!r} "
            f"canonical={canonical(list(case))!r} candidate={candidate(list(case))!r}"
        )
    print(f"random_seed={seed}")
    print("random_case_rule=5000 lists; length uniform [0,40]; integers uniform [-10^12,10^12]")
    print(f"all_cases_json_sha256={case_sha}")
    print(f"total_cases={len(cases)}")
    print(f"mismatch_count={len(mismatches)}")
    for mismatch in mismatches:
        print(f"MISMATCH {mismatch!r}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
