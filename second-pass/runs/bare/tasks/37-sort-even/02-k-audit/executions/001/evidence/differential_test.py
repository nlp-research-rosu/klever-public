#!/usr/bin/env python3
"""Independent differential and direct-contract tests for HumanEval 37."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_even


def direct_contract(values: list[int]) -> list[int]:
    result = list(values)
    result[::2] = sorted(values[::2])
    return result


def make_cases() -> tuple[list[list[int]], dict[str, int]]:
    documented = [[1, 2, 3], [5, 6, 3, 4]]
    boundary = [
        [],
        [0],
        [2, 9],
        [2, 9, 1],
        [1, 9, 2],
        [2, 9, 1, 8],
        [1, 9, 2, 8],
        [2, 9, 2, 8],
        [-1, 7, -3, 6, 0],
        [10**18, 0, -(10**18), 1, 0],
        # Resource boundary: the submitted recursive implementation reaches
        # CPython's recursion limit although the trusted iterative canonical
        # implementation still returns normally.
        list(range(2000, 0, -1)),
    ]
    # Exhaustive small integer lists hit both insertion branches, equality,
    # duplicates, negative values, empty/base cases, and both input parities.
    exhaustive = [
        list(items)
        for length in range(0, 7)
        for items in itertools.product(range(-2, 3), repeat=length)
    ]
    rng = random.Random(370037)
    generated = [
        [rng.randint(-10**6, 10**6) for _ in range(rng.randint(0, 25))]
        for _ in range(1000)
    ]
    cases = documented + boundary + exhaustive + generated
    counts = {
        "documented": len(documented),
        "boundary": len(boundary),
        "exhaustive": len(exhaustive),
        "generated_seed_370037": len(generated),
        "total_with_duplicates": len(cases),
    }
    return cases, counts


def capture(function, argument: list[int]):
    try:
        return {"kind": "result", "value": function(argument)}
    except Exception as err:
        return {
            "kind": "exception",
            "type": type(err).__name__,
            "message": str(err),
        }


def input_summary(values: list[int]):
    if len(values) <= 30:
        return values
    return {
        "length": len(values),
        "first_five": values[:5],
        "last_five": values[-5:],
    }


def outcome_summary(outcome):
    if outcome.get("kind") != "result":
        return outcome
    value = outcome["value"]
    return {"kind": "result", "value": input_summary(value)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", required=True, type=Path)
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--dump-inputs", type=Path)
    args = parser.parse_args()

    canonical = load_entry("trusted_canonical_37", args.canonical)
    candidate = load_entry("submitted_solution_37", args.candidate)
    cases, counts = make_cases()

    if args.dump_inputs:
        args.dump_inputs.write_text(
            json.dumps({"counts": counts, "cases": cases}, separators=(",", ":"))
            + "\n",
            encoding="utf-8",
        )

    mismatches = []
    mutation_failures = []
    digest = hashlib.sha256()
    for case_id, original in enumerate(cases):
        canonical_arg = list(original)
        candidate_arg = list(original)
        canonical_outcome = capture(canonical, canonical_arg)
        candidate_outcome = capture(candidate, candidate_arg)
        expected = direct_contract(original)
        digest.update(
            json.dumps(
                [original, canonical_outcome, candidate_outcome, expected],
                separators=(",", ":"),
            ).encode()
        )
        if canonical_arg != original or candidate_arg != original:
            mutation_failures.append(
                {
                    "id": case_id,
                    "input": original,
                    "canonical_after": canonical_arg,
                    "candidate_after": candidate_arg,
                }
            )
        expected_outcome = {"kind": "result", "value": expected}
        if (
            canonical_outcome != expected_outcome
            or candidate_outcome != expected_outcome
        ):
            mismatches.append(
                {
                    "id": case_id,
                    "input": input_summary(original),
                    "canonical": outcome_summary(canonical_outcome),
                    "candidate": outcome_summary(candidate_outcome),
                    "direct_contract_kind": "result",
                    "direct_contract_length": len(expected),
                }
            )

    print(json.dumps(counts, sort_keys=True))
    print(f"result_digest_sha256={digest.hexdigest()}")
    print(f"mismatch_count={len(mismatches)}")
    print(f"input_mutation_failure_count={len(mutation_failures)}")
    if mismatches:
        print(json.dumps(mismatches[:20], sort_keys=True))
    if mutation_failures:
        print(json.dumps(mutation_failures[:20], sort_keys=True))
    return int(bool(mismatches or mutation_failures))


if __name__ == "__main__":
    raise SystemExit(main())
