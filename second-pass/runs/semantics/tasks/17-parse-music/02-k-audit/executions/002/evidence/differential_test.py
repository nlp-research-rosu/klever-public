#!/usr/bin/env python3
"""Independent candidate-vs-canonical differential tests for HumanEval/17."""

from __future__ import annotations

import importlib.util
import itertools
import json
from pathlib import Path
from typing import Any, Callable


CANONICAL_PATH = Path("/tmp/audit-work/trusted/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/reconstruction/solution.py")


def load_entry(path: Path, module_name: str) -> Callable[[str], list[int]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.parse_music


def outcome(function: Callable[[str], Any], value: str) -> dict[str, Any]:
    try:
        return {"kind": "return", "value": function(value)}
    except Exception as err:
        return {"kind": "raise", "type": type(err).__name__, "message": str(err)}


def main() -> int:
    canonical = load_entry(CANONICAL_PATH, "trusted_canonical")
    candidate = load_entry(CANDIDATE_PATH, "generated_candidate")

    cases: list[tuple[str, str, bool]] = [
        (
            "documented-example",
            "o o| .| o| o| .| .| .| .| o o",
            True,
        ),
        ("empty", "", True),
        ("whole-branch", "o", True),
        ("half-branch", "o|", True),
        ("quarter-else-branch", ".|", True),
        ("first-to-second-boundary", "o o|", True),
        ("second-to-else-boundary", "o| .|", True),
        ("first-to-else-boundary", "o .|", True),
        ("ground-proof-witness", "o o| .|", True),
        ("leading-trailing-spaces", "   o o| .|   ", True),
        ("repeated-spaces", "o   .|  o|", True),
        # Diagnostic cases outside the valid space-delimited note language.
        ("invalid-token", "x", False),
        ("concatenated-invalid", "oo", False),
        ("tab-delimited-extension", "o\t.|", False),
        ("newline-delimited-extension", "o\n.|", False),
    ]

    notes = ("o", "o|", ".|")
    for length in range(0, 7):
        for index, sequence in enumerate(itertools.product(notes, repeat=length)):
            cases.append((f"generated-valid-len-{length}-{index}", " ".join(sequence), True))

    seen: set[str] = set()
    records: list[dict[str, Any]] = []
    intended_mismatches = 0
    diagnostic_mismatches = 0
    for label, value, intended in cases:
        key = json.dumps([label, value, intended])
        if key in seen:
            continue
        seen.add(key)
        expected = outcome(canonical, value)
        actual = outcome(candidate, value)
        match = expected == actual
        if not match and intended:
            intended_mismatches += 1
        if not match and not intended:
            diagnostic_mismatches += 1
        record = {
            "label": label,
            "input": value,
            "intended_valid_space_delimited": intended,
            "canonical": expected,
            "candidate": actual,
            "match": match,
        }
        records.append(record)
        if not match or not label.startswith("generated-valid-"):
            print(json.dumps(record, sort_keys=True))

    summary = {
        "cases": len(records),
        "intended_valid_cases": sum(r["intended_valid_space_delimited"] for r in records),
        "diagnostic_out_of_domain_cases": sum(
            not r["intended_valid_space_delimited"] for r in records
        ),
        "intended_mismatches": intended_mismatches,
        "diagnostic_mismatches": diagnostic_mismatches,
        "oracle": str(CANONICAL_PATH),
        "candidate": str(CANDIDATE_PATH),
        "generated_scope": "all 3^n note sequences for n=0..6, single ASCII spaces",
    }
    print("SUMMARY " + json.dumps(summary, sort_keys=True))
    return 1 if intended_mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
