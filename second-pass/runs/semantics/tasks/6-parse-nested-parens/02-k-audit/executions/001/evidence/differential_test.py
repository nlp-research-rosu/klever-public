#!/usr/bin/env python3
"""Independent canonical-vs-submission differential test for HumanEval/6."""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
from pathlib import Path
from types import ModuleType


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def balanced_groups(pairs: int) -> list[str]:
    groups: list[str] = []

    def visit(prefix: str, opened: int, closed: int) -> None:
        if opened == pairs and closed == pairs:
            groups.append(prefix)
            return
        if opened < pairs:
            visit(prefix + "(", opened + 1, closed)
        if closed < opened:
            visit(prefix + ")", opened, closed + 1)

    visit("", 0, 0)
    return groups


def case_set() -> list[tuple[str, str]]:
    documented = [
        ("documented", "(()()) ((())) () ((())()())"),
    ]
    empty_and_boundaries = [
        ("empty", ""),
        ("space-only", " "),
        ("leading-space", " ()"),
        ("trailing-space", "() "),
        ("double-separator", "()  ()"),
        ("single-open", "("),
        ("single-close", ")"),
        ("unbalanced-open", "((()"),
        ("unbalanced-close", "()))"),
        ("other-character", "(x)"),
    ]
    branch_boundaries = [
        ("one-level", "()"),
        ("nested", "(())"),
        ("maximum-no-update-after-close", "(())()"),
        ("maximum-updates-late", "()((()))"),
        ("siblings", "(()())"),
        ("three-groups", "() (()) ((()))"),
    ]

    generated: list[tuple[str, str]] = []
    groups = [
        group
        for pair_count in range(1, 5)
        for group in balanced_groups(pair_count)
    ]
    for group in groups:
        generated.append(("generated-single-balanced-1..4-pairs", group))

    short_groups = [
        group
        for pair_count in range(1, 4)
        for group in balanced_groups(pair_count)
    ]
    for left, right in itertools.product(short_groups, repeat=2):
        generated.append(("generated-pair-single-separator-1..3-pairs", f"{left} {right}"))

    cases = documented + empty_and_boundaries + branch_boundaries + generated
    seen: set[str] = set()
    unique: list[tuple[str, str]] = []
    for category, value in cases:
        if value not in seen:
            seen.add(value)
            unique.append((category, value))
    return unique


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--submission", type=Path, required=True)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--inputs", type=Path, required=True)
    args = parser.parse_args()

    canonical = load_module("trusted_canonical", args.canonical)
    submission = load_module("submitted_solution", args.submission)
    cases = case_set()

    args.inputs.write_text(
        json.dumps(
            [{"category": category, "input": value} for category, value in cases],
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    mismatches: list[dict[str, object]] = []
    rows: list[str] = ["category\tinput_json\tcanonical_json\tsubmission_json\tmatch"]
    for category, value in cases:
        expected = canonical.parse_nested_parens(value)
        actual = submission.parse_nested_parens(value)
        match = expected == actual
        rows.append(
            "\t".join(
                [
                    category,
                    json.dumps(value, ensure_ascii=False),
                    json.dumps(expected),
                    json.dumps(actual),
                    str(match).lower(),
                ]
            )
        )
        if not match:
            mismatches.append(
                {
                    "category": category,
                    "input": value,
                    "canonical": expected,
                    "submission": actual,
                }
            )
    args.results.write_text("\n".join(rows) + "\n", encoding="utf-8")

    print(f"total_cases={len(cases)}")
    print(f"mismatch_count={len(mismatches)}")
    for mismatch in mismatches:
        print("MISMATCH " + json.dumps(mismatch, ensure_ascii=False, sort_keys=True))
    print(f"results_file={args.results}")
    print(f"inputs_file={args.inputs}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
