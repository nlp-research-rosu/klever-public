#!/usr/bin/env python3
"""Exhibit satisfying entry states and substitute them into the claimed result."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


WORDS = ("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine")
RANK = {word: rank for rank, word in enumerate(WORDS)}


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_numbers


canonical = load("audit_canonical", "/reference/canonical.py")
candidate = load("audit_solution", "/candidate/solution.py")


def codes(word: str) -> str:
    result = ".IntSeq"
    for code in reversed([ord(char) for char in word]):
        result = f"iCons({code}, {result})"
    return result


def val_seq(tokens: list[str]) -> str:
    result = ".ValSeq"
    for word in reversed(tokens):
        result = f"vCons(str({codes(word)}), {result})"
    return result


examples = [
    [],
    ["three", "one", "five"],
    ["nine", "zero", "five", "one", "one"],
]
rows = []
for tokens in examples:
    joined = " ".join(tokens)
    symbolic_vs = val_seq(tokens)
    interpreted_sort_key = sorted(tokens, key=RANK.__getitem__)
    interpreted_claimed_result = " ".join(interpreted_sort_key)
    rows.append({
        "VS": symbolic_vs,
        "validNumberWords": all(token in RANK for token in tokens),
        "input_from_joinCodes_space": joined,
        "formal_rhs_after_substitution": (
            "str(joinCodes(iCons(32, .IntSeq), "
            f"sortKeyVS({symbolic_vs}, numberKeyFunction)))"
        ),
        "rhs_under_supplied_sortKeyVS_contract": interpreted_claimed_result,
        "canonical_python": canonical(joined),
        "candidate_python": candidate(joined),
        "all_interpreted_results_equal": (
            interpreted_claimed_result == canonical(joined) == candidate(joined)
        ),
    })

print(json.dumps(rows, indent=2, sort_keys=True))
raise SystemExit(0 if all(row["all_interpreted_results_equal"] for row in rows) else 1)
