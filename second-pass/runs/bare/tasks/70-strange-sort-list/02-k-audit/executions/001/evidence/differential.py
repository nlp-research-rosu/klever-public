#!/usr/bin/env python3
"""Independent differential test for HumanEval/70.

The oracle is /reference/canonical.py.  The candidate implementation is loaded
from the clean scratch copy, never from /candidate.  The complete deterministic
input corpus can be serialized with --inputs-out.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_cases() -> list[dict[str, object]]:
    cases: list[dict[str, object]] = []

    def add(scope: str, values: list[int]) -> None:
        cases.append({"scope": scope, "input": values})

    # Prompt examples.
    add("prompt", [1, 2, 3, 4])
    add("prompt", [5, 5, 5, 5])
    add("prompt", [])

    # Every generated implementation branch and recursion boundary: lengths
    # 0, 1, and >=2, with both even and odd recursive tails.
    for values in (
        [0],
        [-1],
        [2, 1],
        [1, 1],
        [3, 1, 2],
        [4, 1, 3, 2],
        [3, -1, 2, 3, 0],
        [9, -9, 8, -8, 7, -7],
        [2, 2, 1, 1, 2, 1, 0],
    ):
        add("branch-boundary", values)

    # Integer boundaries relevant to the mathematical-Int versus Python-int
    # bridge, including arbitrary precision values and duplicates.
    huge = 10**100
    for values in (
        [huge],
        [-huge, huge],
        [huge, 0, -huge],
        [huge, huge, -huge, -huge],
        [-(2**63), 2**63 - 1, 0, -1, 1],
    ):
        add("integer-boundary", values)

    # Exhaustive small corpus: 1 + 5 + ... + 5^6 = 19,531 inputs.
    alphabet = (-2, -1, 0, 1, 2)
    for length in range(7):
        for values in itertools.product(alphabet, repeat=length):
            add("exhaustive[-2,2]/len<=6", list(values))

    # Broader reproducible generated corpus, including lengths outside every
    # symbolic K claim in spec.k.
    rng = random.Random(70070)
    for _ in range(500):
        length = rng.randrange(0, 21)
        add(
            "random(seed=70070,len<=20)",
            [rng.randrange(-10**9, 10**9 + 1) for _ in range(length)],
        )

    # Deduplicate while preserving the first scope assignment.
    unique: list[dict[str, object]] = []
    seen: set[tuple[int, ...]] = set()
    for case in cases:
        key = tuple(case["input"])  # type: ignore[arg-type]
        if key not in seen:
            seen.add(key)
            unique.append(case)
    return unique


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputs-out",
        type=Path,
        default=Path("/audit-output/evidence/differential-inputs.json"),
    )
    args = parser.parse_args()

    canonical = load_module("trusted_canonical", Path("/reference/canonical.py"))
    candidate = load_module(
        "scratch_candidate", Path("/tmp/audit-work/src/solution.py")
    )
    cases = build_cases()
    encoded = json.dumps(cases, sort_keys=True, separators=(",", ":")).encode()
    args.inputs_out.write_bytes(encoded + b"\n")
    input_digest = hashlib.sha256(encoded + b"\n").hexdigest()

    mismatches: list[dict[str, object]] = []
    scope_counts: dict[str, int] = {}
    for case in cases:
        scope = str(case["scope"])
        values = list(case["input"])  # type: ignore[arg-type]
        scope_counts[scope] = scope_counts.get(scope, 0) + 1
        expected = canonical.strange_sort_list(values.copy())
        actual = candidate.strange_sort_list(values.copy())
        if actual != expected:
            mismatches.append(
                {
                    "scope": scope,
                    "input": values,
                    "canonical": expected,
                    "candidate": actual,
                }
            )

    print(f"canonical=/reference/canonical.py")
    print(f"candidate=/tmp/audit-work/src/solution.py")
    print(f"input_file={args.inputs_out}")
    print(f"input_sha256={input_digest}")
    print(f"scope_counts={json.dumps(scope_counts, sort_keys=True)}")
    print(f"total_cases={len(cases)}")
    print(f"mismatches={len(mismatches)}")
    if mismatches:
        print(json.dumps(mismatches[:20], sort_keys=True))
        return 1
    print("RESULT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
