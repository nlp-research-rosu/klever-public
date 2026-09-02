#!/usr/bin/env python3
"""Independent CPython differential test for HumanEval/9."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import random
import sys


CANONICAL_PATH = Path("/reference/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/candidate/solution.py")
CASES_PATH = Path("/audit-output/evidence/stage2_cases.json")


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.rolling_max


def main() -> int:
    canonical = load_function(CANONICAL_PATH, "trusted_canonical")
    generated = load_function(GENERATED_PATH, "candidate_solution")
    named_cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))

    cases: list[tuple[str, list[int]]] = [
        (case["name"], case["numbers"]) for case in named_cases
    ]

    # Exhaust every list through length six over a small alphabet. This crosses
    # the first-element branch and both outcomes of the subsequent comparison.
    alphabet = (-2, -1, 0, 1, 2)
    for length in range(7):
        for values in itertools.product(alphabet, repeat=length):
            cases.append((f"exhaustive_len_{length}", list(values)))

    # Deterministic broad representatives include arbitrary-precision integers.
    rng = random.Random(0x9A11D17)
    for index in range(2000):
        length = rng.randrange(0, 65)
        values = [
            rng.randrange(-(10**80), 10**80)
            if index % 7 == 0
            else rng.randrange(-10**9, 10**9)
            for _ in range(length)
        ]
        cases.append((f"random_{index}", values))

    digest = hashlib.sha256()
    mismatches: list[dict[str, object]] = []
    for name, numbers in cases:
        expected = canonical(numbers.copy())
        actual = generated(numbers.copy())
        record = {
            "name": name,
            "numbers": numbers,
            "canonical": expected,
            "generated": actual,
        }
        digest.update(
            json.dumps(record, sort_keys=True, separators=(",", ":")).encode("utf-8")
        )
        if actual != expected:
            mismatches.append(record)
            if len(mismatches) >= 20:
                break

    print("oracle:", CANONICAL_PATH)
    print("generated:", GENERATED_PATH)
    print("named_cases:", len(named_cases))
    print("exhaustive_scope: alphabet=-2..2, lengths=0..6")
    print("deterministic_random_scope: seed=0x9A11D17, count=2000, lengths=0..64")
    print("total_cases_executed:", len(cases) if not mismatches else "stopped early")
    print("result_digest_sha256:", digest.hexdigest())
    print("mismatch_count:", len(mismatches))
    if mismatches:
        print(json.dumps(mismatches, indent=2))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
