#!/usr/bin/env python3
"""Independent differential test for HumanEval 8 sum_product."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path
from types import ModuleType

CANONICAL_PATH = Path("/tmp/audit-work/trusted/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/src/solution.py")
INPUT_MANIFEST = Path("/audit-output/evidence/differential_inputs.jsonl")


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_cases() -> list[tuple[str, list[int]]]:
    cases: list[tuple[str, list[int]]] = [
        ("documented-empty", []),
        ("documented-four", [1, 2, 3, 4]),
        ("single-negative", [-1]),
        ("single-zero", [0]),
        ("single-positive", [1]),
        ("two-positive", [2, 3]),
        ("zero-first", [0, 7, -4]),
        ("zero-middle", [7, 0, -4]),
        ("zero-last", [7, -4, 0]),
        ("mixed-sign-even-negatives", [-2, 3, -4]),
        ("mixed-sign-odd-negatives", [-2, 3, 4]),
        ("all-negative", [-1, -2, -3, -4]),
        ("cancellation", [10, -10, 5, -5]),
        ("large-64-bit-like", [2**63 - 1, -(2**63), 1]),
        ("unbounded-python-int", [2**200, -(2**199), 3]),
    ]

    small_values = range(-3, 4)
    for length in range(0, 6):
        for values in itertools.product(small_values, repeat=length):
            cases.append((f"exhaustive-length-{length}", list(values)))

    rng = random.Random(0x8A11D17)
    for _ in range(5000):
        length = rng.randrange(0, 21)
        values = [rng.randint(-1_000_000, 1_000_000) for _ in range(length)]
        cases.append(("generated-seed-0x8A11D17", values))
    return cases


def main() -> int:
    canonical = load_module("trusted_canonical", CANONICAL_PATH)
    candidate = load_module("generated_candidate", CANDIDATE_PATH)

    cases = test_cases()
    failures: list[dict[str, object]] = []
    category_counts: dict[str, int] = {}
    with INPUT_MANIFEST.open("w", encoding="utf-8") as manifest:
        for index, (category, values) in enumerate(cases):
            category_counts[category] = category_counts.get(category, 0) + 1
            manifest.write(
                json.dumps(
                    {"index": index, "category": category, "input": values},
                    separators=(",", ":"),
                )
                + "\n"
            )
            expected = canonical.sum_product(values)
            actual = candidate.sum_product(values)
            if actual != expected:
                failures.append(
                    {
                        "index": index,
                        "category": category,
                        "input": values,
                        "canonical": expected,
                        "candidate": actual,
                    }
                )

    assert canonical.sum_product([]) == (0, 1)
    assert canonical.sum_product([1, 2, 3, 4]) == (10, 24)
    assert candidate.sum_product([]) == (0, 1)
    assert candidate.sum_product([1, 2, 3, 4]) == (10, 24)

    manifest_hash = hashlib.sha256(INPUT_MANIFEST.read_bytes()).hexdigest()
    print(f"canonical={CANONICAL_PATH}")
    print(f"candidate={CANDIDATE_PATH}")
    print("domain=finite Python lists whose elements are Python int values")
    print(f"case_count={len(cases)}")
    print(f"category_counts={json.dumps(category_counts, sort_keys=True)}")
    print(f"input_manifest={INPUT_MANIFEST}")
    print(f"input_manifest_sha256={manifest_hash}")
    print(f"mismatch_count={len(failures)}")
    if failures:
        for failure in failures[:20]:
            print(json.dumps(failure, sort_keys=True))
        return 1
    print("DIFFERENTIAL_RESULT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
