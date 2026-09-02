#!/usr/bin/env python3
"""Compare concrete theorem instances with the real CPython implementations."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.count_distinct_characters


def supplied_lower(code: int) -> int:
    return code + 32 if 65 <= code <= 90 else code


def supplied_result(string: str) -> int:
    lowered = [supplied_lower(ord(character)) for character in string]
    return len(dict.fromkeys(lowered))


def main() -> int:
    canonical = load(Path("/reference/canonical.py"), "canonical_witness")
    candidate = load(
        Path("/tmp/audit-work/count-distinct-audit/reconstruction/solution.py"),
        "candidate_witness",
    )
    cases = ["", "Jerry", "Σσ", "İ"]
    rows = []
    for string in cases:
        rows.append(
            {
                "input": string,
                "code_points": [ord(character) for character in string],
                "supplied_semantics_claim_result": supplied_result(string),
                "canonical_python_result": canonical(string),
                "candidate_python_result": candidate(string),
                "python_lower_code_points": [
                    ord(character) for character in string.lower()
                ],
            }
        )
    print(json.dumps(rows, ensure_ascii=False, indent=2))
    assert rows[0]["supplied_semantics_claim_result"] == 0
    assert rows[1]["supplied_semantics_claim_result"] == 4
    assert rows[2]["supplied_semantics_claim_result"] == 2
    assert rows[2]["canonical_python_result"] == 1
    assert rows[3]["supplied_semantics_claim_result"] == 1
    assert rows[3]["canonical_python_result"] == 2
    assert all(
        row["candidate_python_result"] == row["canonical_python_result"]
        for row in rows
    )
    print("SATISFYING_STATE_AND_UNICODE_WITNESSES: CONFIRMED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
