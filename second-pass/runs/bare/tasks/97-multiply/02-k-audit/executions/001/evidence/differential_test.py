#!/usr/bin/env python3
"""Independent differential test for HumanEval/97 multiply."""

from __future__ import annotations

import importlib.util
import json
import random
import sys
from pathlib import Path

TRUSTED = Path("/tmp/audit-work/97-multiply/trusted/canonical.py")
CANDIDATE = Path("/tmp/audit-work/97-multiply/candidate-source/solution.py")
INPUTS_OUT = Path("/audit-output/evidence/differential_inputs.json")
RESULTS_OUT = Path("/audit-output/evidence/differential_results.json")


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.multiply


def add_case(cases, seen, a: int, b: int, category: str):
    key = (a, b)
    if key not in seen:
        seen.add(key)
        cases.append({"a": a, "b": b, "category": category})


def build_cases():
    cases = []
    seen = set()

    examples = [(148, 412), (19, 28), (2020, 1851), (14, -15)]
    for a, b in examples:
        add_case(cases, seen, a, b, "documented-example")

    # -1, 0, 1 crosses each of the two independent `x < 0` branches.
    for a in (-1, 0, 1):
        for b in (-1, 0, 1):
            add_case(cases, seen, a, b, "branch-boundary")

    # Multiples of ten and their immediate neighbors stress the unit digit,
    # including values where Python's negative modulo differs from abs(x) % 10.
    digit_boundaries = (
        -101, -100, -99, -21, -20, -19, -15, -14, -11, -10, -9,
        -1, 0, 1, 9, 10, 11, 14, 15, 19, 20, 21, 99, 100, 101,
    )
    for a in digit_boundaries:
        for b in digit_boundaries:
            add_case(cases, seen, a, b, "digit-and-sign-boundary-grid")

    large = (
        (10**100 + 7, 10**80 + 3),
        (-(10**100 + 7), 10**80 + 3),
        (10**100 + 7, -(10**80 + 3)),
        (-(10**100 + 7), -(10**80 + 3)),
    )
    for a, b in large:
        add_case(cases, seen, a, b, "unbounded-integer-representative")

    rng = random.Random(970097)
    for _ in range(250):
        add_case(
            cases,
            seen,
            rng.randint(-(10**30), 10**30),
            rng.randint(-(10**30), 10**30),
            "deterministic-generated",
        )
    return cases


def outcome(fn, a: int, b: int):
    try:
        return {"kind": "return", "value": fn(a, b)}
    except Exception as exc:  # Diagnostic symmetry; intended inputs are valid ints.
        return {"kind": "raise", "type": type(exc).__name__, "message": str(exc)}


def main() -> int:
    canonical = load_entry(TRUSTED, "audit_trusted_canonical")
    generated = load_entry(CANDIDATE, "audit_candidate_solution")
    cases = build_cases()
    INPUTS_OUT.write_text(json.dumps(cases, indent=2) + "\n", encoding="utf-8")

    rows = []
    mismatches = []
    category_counts = {}
    for case in cases:
        category_counts[case["category"]] = category_counts.get(case["category"], 0) + 1
        expected = outcome(canonical, case["a"], case["b"])
        actual = outcome(generated, case["a"], case["b"])
        row = {**case, "canonical": expected, "candidate": actual, "match": expected == actual}
        rows.append(row)
        if not row["match"]:
            mismatches.append(row)

    result = {
        "trusted_oracle": str(TRUSTED),
        "candidate_entry_point": str(CANDIDATE),
        "empty_case": "not applicable: the documented domain is a pair of integers",
        "case_count": len(cases),
        "category_counts": category_counts,
        "mismatch_count": len(mismatches),
        "rows": rows,
    }
    RESULTS_OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print(f"trusted_oracle={TRUSTED}")
    print(f"candidate_entry_point={CANDIDATE}")
    print("empty_case=not applicable: integer scalar inputs have no empty value")
    print(f"case_count={len(cases)}")
    print(f"category_counts={json.dumps(category_counts, sort_keys=True)}")
    print(f"mismatch_count={len(mismatches)}")
    for row in mismatches[:25]:
        print(
            "MISMATCH "
            f"category={row['category']} "
            f"input=({row['a']}, {row['b']}) "
            f"canonical={row['canonical']} "
            f"candidate={row['candidate']}"
        )
    if len(mismatches) > 25:
        print(f"... {len(mismatches) - 25} additional mismatches in {RESULTS_OUT}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
