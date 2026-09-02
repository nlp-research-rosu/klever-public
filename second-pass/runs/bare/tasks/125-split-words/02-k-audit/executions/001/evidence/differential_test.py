#!/usr/bin/env python3
"""Independent candidate-vs-trusted-canonical differential test.

The fixed cases cover the prompt examples, empty input, both sides of each
branch test, leading/trailing/repeated separators, whitespace precedence, and
ASCII/Unicode character-count boundaries.  The generated scope is every
string of length 0..4 over the explicitly printed nine-character alphabet.
"""

from __future__ import annotations

import importlib.util
import itertools
import json
from pathlib import Path
from typing import Any, Callable


EVIDENCE_DIR = Path("/audit-output/evidence")
CANONICAL_PATH = Path("/tmp/audit-work/fresh/trusted/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/fresh/candidate/solution.py")
FIXTURE_PATH = EVIDENCE_DIR / "differential_inputs.json"
ALPHABET = ("a", "b", "c", ",", " ", "\t", "A", "1", "ä")
MAX_GENERATED_LENGTH = 4


def load_entry(path: Path, module_name: str) -> Callable[[str], Any]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    entry = getattr(module, "split_words")
    return entry


def classify(value: str) -> str:
    if " " in value:
        return "canonical-space-branch"
    if "," in value:
        return "canonical-comma-branch"
    return "canonical-count-branch"


def main() -> int:
    canonical = load_entry(CANONICAL_PATH, "trusted_canonical")
    generated = load_entry(GENERATED_PATH, "candidate_generated")
    fixed_inputs = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    generated_inputs = (
        "".join(chars)
        for length in range(MAX_GENERATED_LENGTH + 1)
        for chars in itertools.product(ALPHABET, repeat=length)
    )

    seen: set[str] = set()
    ordered_inputs: list[tuple[str, str]] = []
    for source, values in (("fixed", fixed_inputs), ("generated", generated_inputs)):
        for value in values:
            if value not in seen:
                seen.add(value)
                ordered_inputs.append((source, value))

    mismatches: list[dict[str, Any]] = []
    branch_totals: dict[str, int] = {}
    branch_mismatches: dict[str, int] = {}
    fixed_results: list[dict[str, Any]] = []
    for source, value in ordered_inputs:
        expected = canonical(value)
        actual = generated(value)
        branch = classify(value)
        branch_totals[branch] = branch_totals.get(branch, 0) + 1
        record = {
            "source": source,
            "input": value,
            "branch": branch,
            "canonical": expected,
            "generated": actual,
            "equal": type(expected) is type(actual) and expected == actual,
        }
        if source == "fixed":
            fixed_results.append(record)
        if not record["equal"]:
            mismatches.append(record)
            branch_mismatches[branch] = branch_mismatches.get(branch, 0) + 1

    print("ORACLE:", CANONICAL_PATH)
    print("GENERATED:", GENERATED_PATH)
    print("FIXTURE_FILE:", FIXTURE_PATH)
    print("GENERATED_ALPHABET:", json.dumps(ALPHABET, ensure_ascii=True))
    print("GENERATED_LENGTHS: 0..", MAX_GENERATED_LENGTH, sep="")
    print("UNIQUE_INPUTS:", len(ordered_inputs))
    print("BRANCH_TOTALS:", json.dumps(branch_totals, sort_keys=True))
    print("MISMATCH_COUNT:", len(mismatches))
    print("BRANCH_MISMATCHES:", json.dumps(branch_mismatches, sort_keys=True))
    print("FIXED_RESULTS:")
    for record in fixed_results:
        print(json.dumps(record, ensure_ascii=True, sort_keys=True))
    print("FIRST_120_MISMATCHES:")
    for record in mismatches[:120]:
        print(json.dumps(record, ensure_ascii=True, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
