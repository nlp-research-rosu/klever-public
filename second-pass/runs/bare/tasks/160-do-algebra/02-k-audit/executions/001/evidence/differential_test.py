#!/usr/bin/env python3
"""Independent differential check for HumanEval 160 do_algebra."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path


REFERENCE_PATH = Path("/reference/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/reconstruction/solution.py")
INPUTS_PATH = Path("/audit-output/evidence/differential-inputs.json")


def load_entry(module_name: str, source_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, source_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {source_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.do_algebra


def outcome(function, operators, operands):
    try:
        result = function(list(operators), list(operands))
        return {
            "kind": "return",
            "type": type(result).__name__,
            "value": result,
        }
    except Exception as error:  # Differentially compare intended boundary errors.
        return {
            "kind": "raise",
            "type": type(error).__name__,
            "message": str(error),
        }


def add_case(cases, seen, group, label, operators, operands):
    key = (tuple(operators), tuple(operands))
    if key in seen:
        return
    seen.add(key)
    cases.append(
        {
            "group": group,
            "label": label,
            "operators": list(operators),
            "operands": list(operands),
        }
    )


def build_cases():
    cases = []
    seen = set()
    curated = [
        ("documented", "prompt-example", ["+", "*", "-"], [2, 3, 4, 5]),
        ("boundary", "minimum-add", ["+"], [0, 0]),
        ("boundary", "minimum-subtract", ["-"], [0, 1]),
        ("boundary", "minimum-multiply", ["*"], [0, 7]),
        ("boundary", "minimum-floor", ["//"], [7, 3]),
        ("boundary", "floor-by-zero", ["//"], [7, 0]),
        ("boundary", "minimum-power", ["**"], [0, 0]),
        ("boundary", "power-zero", ["**"], [9, 0]),
        ("precedence", "right-associative-power", ["**", "**"], [2, 3, 2]),
        ("precedence", "left-associative-floor", ["//", "//"], [20, 3, 2]),
        ("precedence", "left-associative-subtract", ["-", "-"], [10, 3, 2]),
        ("precedence", "multiply-before-add", ["+", "*"], [2, 3, 4]),
        ("precedence", "floor-before-add", ["//", "+"], [7, 3, 2]),
        (
            "precedence",
            "all-levels",
            ["+", "**", "*", "-", "//"],
            [2, 3, 2, 4, 5, 2],
        ),
        ("boundary", "powered-zero-divisor", ["//", "**"], [7, 0, 1]),
        ("boundary", "zero-to-zero-divisor-is-one", ["//", "**"], [7, 0, 0]),
        ("out-of-domain", "no-operator-one-operand", [], [7]),
        ("out-of-domain", "empty-operands", [], []),
    ]
    for group, label, operators, operands in curated:
        add_case(cases, seen, group, label, operators, operands)

    operators = ["+", "-", "*", "//", "**"]
    for operator in operators:
        for operands in itertools.product(range(5), repeat=2):
            add_case(
                cases,
                seen,
                "exhaustive-one-operator",
                "all-ops-values-0-through-4",
                [operator],
                operands,
            )
    for operator_pair in itertools.product(operators, repeat=2):
        for operands in itertools.product(range(4), repeat=3):
            add_case(
                cases,
                seen,
                "exhaustive-two-operators",
                "all-op-pairs-values-0-through-3",
                operator_pair,
                operands,
            )

    generator = random.Random(160)
    for index in range(500):
        count = generator.randint(3, 4)
        generated_operators = [generator.choice(operators) for _ in range(count)]
        generated_operands = [generator.randint(0, 2) for _ in range(count + 1)]
        add_case(
            cases,
            seen,
            "deterministic-generated",
            f"seed-160-index-{index}",
            generated_operators,
            generated_operands,
        )
    return cases


def main() -> int:
    reference = load_entry("trusted_canonical", REFERENCE_PATH)
    candidate = load_entry("generated_solution", CANDIDATE_PATH)
    cases = build_cases()
    INPUTS_PATH.write_text(json.dumps(cases, indent=2) + "\n", encoding="utf-8")

    mismatches = []
    outcome_counts = {}
    curated_results = []
    for case in cases:
        reference_outcome = outcome(
            reference, case["operators"], case["operands"]
        )
        candidate_outcome = outcome(
            candidate, case["operators"], case["operands"]
        )
        count_key = (
            reference_outcome["kind"],
            reference_outcome["type"],
        )
        outcome_counts[count_key] = outcome_counts.get(count_key, 0) + 1
        if case["group"] in {"documented", "boundary", "precedence", "out-of-domain"}:
            curated_results.append(
                {
                    "label": case["label"],
                    "operators": case["operators"],
                    "operands": case["operands"],
                    "outcome": reference_outcome,
                }
            )
        if reference_outcome != candidate_outcome:
            mismatches.append(
                {
                    "case": case,
                    "reference": reference_outcome,
                    "candidate": candidate_outcome,
                }
            )

    print(f"reference={REFERENCE_PATH}")
    print(f"candidate={CANDIDATE_PATH}")
    print(f"inputs_file={INPUTS_PATH}")
    print(f"case_count={len(cases)}")
    print(f"outcome_counts={outcome_counts}")
    print("curated_results=")
    print(json.dumps(curated_results, indent=2))
    print(f"mismatch_count={len(mismatches)}")
    if mismatches:
        print(json.dumps(mismatches[:20], indent=2))
        return 1
    print("RESULT: all reference and candidate outcomes match")
    return 0


if __name__ == "__main__":
    sys.exit(main())
