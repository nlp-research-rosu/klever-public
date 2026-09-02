#!/usr/bin/env python3
"""Independent canonical-vs-candidate differential test for rounded_avg."""

from __future__ import annotations

import importlib.util
import json
import random
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


CANONICAL_PATH = Path("/tmp/audit-work/reconstruction/trusted/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/reconstruction/solution.py")
INPUTS_PATH = Path("/audit-output/evidence/differential-inputs.jsonl")
RESULTS_PATH = Path("/audit-output/evidence/differential-results.jsonl")


def load_entry(path: Path, module_name: str) -> Callable[[int, int], Any]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.rounded_avg


@dataclass(frozen=True)
class Case:
    category: str
    n: int
    m: int


def outcome(function: Callable[[int, int], Any], n: int, m: int) -> dict[str, Any]:
    try:
        value = function(n, m)
        return {"kind": "return", "type": type(value).__name__, "value": value}
    except Exception as error:  # Differential evidence includes exception behavior.
        return {
            "kind": "raise",
            "type": type(error).__name__,
            "value": str(error),
        }


def main() -> int:
    canonical = load_entry(CANONICAL_PATH, "trusted_canonical")
    candidate = load_entry(CANDIDATE_PATH, "audited_candidate")

    cases: list[Case] = [
        Case("documented", 1, 5),
        Case("documented", 7, 5),
        Case("documented", 10, 20),
        Case("documented", 20, 33),
        Case("minimum-positive/equal", 1, 1),
        Case("inverted-empty-interval", 2, 1),
        Case("even-sum/integral", 1, 3),
        Case("odd-sum/half-even-up", 1, 2),
        Case("odd-sum/half-even-down", 2, 3),
        Case("branch-neighbor", 3, 4),
        Case("branch-neighbor", 4, 5),
        Case("out-of-contract-zero-boundary", 0, 0),
    ]

    # Exhaust the small positive square, including the n > m return branch.
    for n in range(1, 101):
        for m in range(1, 101):
            cases.append(Case("exhaustive-positive-1..100", n, m))

    # Deterministic representative positive inputs with bounded interval width,
    # so the independently implemented canonical loop remains practical.
    rng = random.Random(103_2026)
    for _ in range(5000):
        n = rng.randint(1, 1_000_000)
        m = max(1, n + rng.randint(-25, 25))
        cases.append(Case("generated-bounded-width", n, m))

    # Positive Python integers around the binary64 exact-integer boundary.
    # The prompt states no upper bound, so these are part of the literal domain.
    p53 = 2**53
    for n, m in [
        (p53 - 1, p53 - 1),
        (p53, p53),
        (p53 + 1, p53 + 1),
        (p53 + 1, p53 + 2),
        (p53 + 2, p53 + 3),
        (p53 + 3, p53 + 3),
    ]:
        cases.append(Case("binary64-boundary", n, m))

    mismatch_count = 0
    category_counts: dict[str, int] = {}
    category_mismatches: dict[str, int] = {}
    first_mismatches: list[dict[str, Any]] = []

    with INPUTS_PATH.open("w", encoding="utf-8") as input_file, RESULTS_PATH.open(
        "w", encoding="utf-8"
    ) as result_file:
        for case in cases:
            input_file.write(
                json.dumps(
                    {"category": case.category, "n": case.n, "m": case.m},
                    sort_keys=True,
                )
                + "\n"
            )
            left = outcome(canonical, case.n, case.m)
            right = outcome(candidate, case.n, case.m)
            matches = left == right
            record = {
                "category": case.category,
                "n": case.n,
                "m": case.m,
                "canonical": left,
                "candidate": right,
                "matches": matches,
            }
            result_file.write(json.dumps(record, sort_keys=True) + "\n")
            category_counts[case.category] = category_counts.get(case.category, 0) + 1
            if not matches:
                mismatch_count += 1
                category_mismatches[case.category] = (
                    category_mismatches.get(case.category, 0) + 1
                )
                if len(first_mismatches) < 20:
                    first_mismatches.append(record)

    print(f"canonical={CANONICAL_PATH}")
    print(f"candidate={CANDIDATE_PATH}")
    print(f"input_manifest={INPUTS_PATH}")
    print(f"result_manifest={RESULTS_PATH}")
    print(f"case_count={len(cases)}")
    print(f"category_counts={json.dumps(category_counts, sort_keys=True)}")
    print(f"mismatch_count={mismatch_count}")
    print(f"category_mismatches={json.dumps(category_mismatches, sort_keys=True)}")
    for record in first_mismatches:
        print("MISMATCH " + json.dumps(record, sort_keys=True))

    # A nonzero status deliberately makes any intended-domain divergence visible.
    return 1 if mismatch_count else 0


if __name__ == "__main__":
    sys.exit(main())
