#!/usr/bin/env python3
"""Independent differential check of trusted canonical.py and candidate solution.py."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path


EVIDENCE_DIR = Path("/audit-output/evidence")
SCRATCH_DIR = Path("/tmp/audit-work/62-derivative")


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.derivative


def main() -> int:
    config = json.loads((EVIDENCE_DIR / "differential_cases.json").read_text())
    canonical = load_function(SCRATCH_DIR / "canonical.py", "trusted_canonical")
    generated = load_function(SCRATCH_DIR / "solution.py", "candidate_solution")

    cases: list[tuple[str, list[object], list[object] | None]] = []
    for item in config["documented_examples"]:
        cases.append(("documented", item["xs"], item["expected"]))
    for xs in config["boundary_and_branch_cases"]:
        cases.append(("boundary", xs, None))
    for xs in config["extended_numeric_cases"]:
        cases.append(("extended_numeric", xs, None))

    exhaustive = config["exhaustive_generator"]
    values = exhaustive["coefficient_values"]
    for length in exhaustive["lengths"]:
        for coefficients in itertools.product(values, repeat=length):
            cases.append(("exhaustive", list(coefficients), None))

    seeded = config["seeded_generator"]
    rng = random.Random(seeded["seed"])
    lo_length, hi_length = seeded["length_range"]
    lo_value, hi_value = seeded["coefficient_range"]
    for _ in range(seeded["count"]):
        length = rng.randint(lo_length, hi_length)
        cases.append(
            (
                "seeded",
                [rng.randint(lo_value, hi_value) for _ in range(length)],
                None,
            )
        )

    mismatches = []
    expected_failures = []
    category_counts: dict[str, int] = {}
    for category, xs, expected in cases:
        category_counts[category] = category_counts.get(category, 0) + 1
        trusted_result = canonical(list(xs))
        generated_result = generated(list(xs))
        if expected is not None and trusted_result != expected:
            expected_failures.append(
                {"xs": xs, "trusted": trusted_result, "expected": expected}
            )
        if trusted_result != generated_result:
            mismatches.append(
                {"xs": xs, "trusted": trusted_result, "generated": generated_result}
            )

    print(f"PYTHON_VERSION: {sys.version.split()[0]}")
    print("ORACLE: /reference/canonical.py copied byte-for-byte into scratch")
    print("SUBJECT: /candidate/solution.py copied byte-for-byte into scratch")
    print(f"CATEGORY_COUNTS: {json.dumps(category_counts, sort_keys=True)}")
    print(f"TOTAL_CASES: {len(cases)}")
    print(f"DOCUMENTED_EXPECTED_FAILURES: {len(expected_failures)}")
    print(f"MISMATCH_COUNT: {len(mismatches)}")
    if expected_failures:
        print(f"EXPECTED_FAILURE_SAMPLE: {expected_failures[:5]!r}")
    if mismatches:
        print(f"MISMATCH_SAMPLE: {mismatches[:5]!r}")
    return 0 if not expected_failures and not mismatches else 1


if __name__ == "__main__":
    raise SystemExit(main())
