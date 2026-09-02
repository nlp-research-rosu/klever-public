#!/usr/bin/env python3
"""Ground witnesses for all four entry-claim preconditions and results."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any, Callable


SCRATCH = Path("/tmp/audit-work/125-split-words")


def load_function(module_name: str, path: Path) -> Callable[[str], Any]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.split_words


candidate = load_function("witness_candidate", SCRATCH / "solution.py")
canonical = load_function("witness_canonical", SCRATCH / "canonical.py")

MODEL_WHITESPACE_CODES = {9, 10, 13, 32}
ODD_INDEX_ASCII = set("bdfhjlnprtvxz")


def model_split_ws(text: str) -> list[str]:
    result: list[str] = []
    current: list[str] = []
    for char in text:
        if ord(char) in MODEL_WHITESPACE_CODES:
            if current:
                result.append("".join(current))
                current = []
        else:
            current.append(char)
    if current:
        result.append("".join(current))
    return result


def model_branch(text: str) -> str:
    parts = model_split_ws(text)
    if not text:
        return "empty"
    if parts != [text]:
        return "whitespace"
    if "," in text:
        return "comma"
    return "count"


def model_result(text: str) -> list[str] | int:
    branch = model_branch(text)
    if branch == "whitespace":
        return model_split_ws(text)
    if branch == "comma":
        return text.split(",")
    return sum(char in ODD_INDEX_ASCII for char in text)


witnesses = [
    ("empty", ""),
    ("whitespace", "Hello world!"),
    ("comma", "Hello,world!"),
    ("count", "abcdef"),
]

for intended_branch, text in witnesses:
    observed_branch = model_branch(text)
    expected = model_result(text)
    candidate_value = candidate(text)
    canonical_value = canonical(text)
    print(
        repr(text),
        "precondition_branch=" + observed_branch,
        "claimed_result=" + repr(expected),
        "candidate=" + repr(candidate_value),
        "canonical=" + repr(canonical_value),
    )
    assert observed_branch == intended_branch
    assert candidate_value == expected
    assert canonical_value == expected

print("all_entry_preconditions_satisfiable=True")
print("all_ground_results_agree=True")
