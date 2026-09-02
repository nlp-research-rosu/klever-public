#!/usr/bin/env python3
"""Concrete satisfying substitutions for every submitted positive claim."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.filter_by_substring


def main() -> int:
    canonical = load(Path("/reference/canonical.py"), "canonical_claim_witness")
    candidate = load(
        Path("/tmp/audit-work/7-filter-by-substring/solution.py"),
        "candidate_claim_witness",
    )
    witnesses = [
        (
            "UNIVERSAL-PROGRAM-REDUCTION",
            ["a"],
            "a",
            "sort-only precondition: INPUT=Cons(\"a\",Nil), SUBSTRING=\"a\"",
        ),
        (
            "UNIVERSAL-BASE",
            [],
            "a",
            "sort-only precondition: INPUT=Nil, SUBSTRING=\"a\"",
        ),
        (
            "UNIVERSAL-STEP-KEEP",
            ["a"],
            "a",
            "HEAD=\"a\", TAIL=Nil; contains=true and tail equality []==[]",
        ),
        (
            "UNIVERSAL-STEP-DROP",
            ["b"],
            "a",
            "HEAD=\"b\", TAIL=Nil; not-contains=true and tail equality []==[]",
        ),
        (
            "EMPTY-EXAMPLE",
            [],
            "a",
            "ground claim; no requires clause",
        ),
        (
            "PROMPT-EXAMPLE",
            ["abc", "bacd", "cde", "array"],
            "a",
            "ground claim; no requires clause",
        ),
    ]

    mismatches = 0
    for label, strings, substring, precondition in witnesses:
        oracle_result = canonical(strings, substring)
        candidate_result = candidate(strings, substring)
        agrees = oracle_result == candidate_result
        print(f"CLAIM: {label}")
        print(f"SATISFYING_STATE: strings={strings!r}, substring={substring!r}")
        print(f"PRECONDITION_CHECK: {precondition}")
        print(f"TRUSTED_CANONICAL_RESULT: {oracle_result!r}")
        print(f"CANDIDATE_PYTHON_RESULT: {candidate_result!r}")
        print(f"PYTHON_RESULTS_AGREE: {str(agrees).lower()}")
        print()
        if not agrees:
            mismatches += 1

    # A separate satisfying state exposes that the universal entry claim's RHS
    # is not the intended postcondition under the submitted semantics.
    print("ENTRY_BOUNDARY_STATE: strings=[''], substring=''")
    print("ENTRY_BOUNDARY_PRECONDITION: sort-only; satisfied")
    print(f"TRUSTED_CANONICAL_RESULT: {canonical([''], '')!r}")
    print(f"CANDIDATE_PYTHON_RESULT: {candidate([''], '')!r}")
    print("FRESH_K_RESULT: [] (see stage5-unsound-empty-empty-witness.log)")
    print()
    print(f"claim_witness_count={len(witnesses)}")
    print(f"python_mismatches={mismatches}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
