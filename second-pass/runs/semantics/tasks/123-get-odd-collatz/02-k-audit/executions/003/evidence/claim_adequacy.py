#!/usr/bin/env python3
"""Ground witnesses and formal-domain checks for every candidate entry claim."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path
from typing import Callable


def load_entry(name: str, path: Path) -> Callable[[int], list[int]]:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_odd_collatz


def odd_trace(n: int) -> list[int]:
    values: list[int] = []
    while True:
        if n % 2 == 1:
            values.append(n)
        if n == 1:
            return values
        n = 3 * n + 1 if n % 2 else n // 2


candidate = load_entry("candidate_for_claim_witness", Path("/candidate/solution.py"))
canonical = load_entry("canonical_for_claim_witness", Path("/reference/canonical.py"))
spec_text = Path("/candidate/spec.k").read_text()
verification_text = Path("/candidate/verification.k").read_text()

print("LOCAL_CLAIM_WITNESSES")
print(
    "odd-step: N=3, A=.ValSeq; pyMod(3,2)=1; "
    "one real iteration gives N'=10, A'=[3]"
)
print(
    "even-step: N=2, A=[7]; pyMod(2,2)=0; "
    "one real iteration gives N'=1, A'=[7]"
)
print(
    "exit-step: N=1, A=[3,5], M=.Map; 'sorted' is absent from M; "
    "tail gives unsorted [3,5,1] and returns its sorted result [1,3,5]"
)
assert 3 > 1 and 3 % 2 == 1
assert 2 > 1 and not (2 % 2 == 1)
assert "sorted" not in {}

print("FIXED_END_TO_END_CLAIM_WITNESSES")
expected_unsorted = {
    1: [1],
    5: [5, 1],
    6: [3, 5, 1],
    7: [7, 11, 17, 13, 5, 1],
}
for n, expected_trace in expected_unsorted.items():
    trace = odd_trace(n)
    candidate_result = candidate(n)
    canonical_result = canonical(n)
    print(
        f"case-{n}: precondition=exact initial configuration; "
        f"unsorted_odd_trace={trace}; "
        f"candidate={candidate_result}; canonical={canonical_result}"
    )
    assert trace == expected_trace
    assert candidate_result == sorted(expected_trace)
    assert canonical_result == sorted(expected_trace)

entries = re.findall(r"#getOddCollatz\(([^)]+)\)", spec_text)
labels = re.findall(r"\[label\(([^)]+)\)\]", spec_text)
claim_blocks = re.findall(r"\bclaim\b(.*?)(?=\n\s*claim\b|\nendmodule)", spec_text, re.S)
blocks_by_label = {
    re.search(r"\[label\(([^)]+)\)\]", block).group(1): block
    for block in claim_blocks
}
odd_lhs_k = re.search(r"<k>(.*?)=>", blocks_by_label["odd-step"], re.S).group(1)
even_lhs_k = re.search(r"<k>(.*?)=>", blocks_by_label["even-step"], re.S).group(1)
print(f"CLAIM_LABELS={labels}")
print(f"SPEC_GET_ODD_COLLATZ_ARGUMENTS={entries}")
print(f"SPEC_COLLatzResult_OCCURRENCES={spec_text.count('collatzResult')}")
print(
    "VERIFICATION_COLLatzResult_OCCURRENCES="
    f"{verification_text.count('collatzResult')}"
)
print(
    "SYMBOLIC_END_TO_END_ENTRY_PRESENT="
    f"{any(not entry.strip().lstrip('-').isdigit() for entry in entries)}"
)
print(
    "FULL_RESULT_CONSTRAINT_LABELS="
    f"{[label for label in labels if label.startswith('case-')]}"
)
print(
    "LOCAL_ONLY_LABELS="
    f"{[label for label in labels if label.endswith('-step')]}"
)
print(
    "ODD_STEP_REAL_CONTEXT_MISMATCHES="
    f"missing_k_suffix={'~>' not in odd_lhs_k}, "
    f"empty_module_scope={'0 |-> scope(.Map' in blocks_by_label['odd-step']}, "
    f"empty_stack={'<stack> .List </stack>' in blocks_by_label['odd-step']}"
)
print(
    "EVEN_STEP_REAL_CONTEXT_MISMATCHES="
    f"missing_k_suffix={'~>' not in even_lhs_k}, "
    f"empty_module_scope={'0 |-> scope(.Map' in blocks_by_label['even-step']}, "
    f"empty_stack={'<stack> .List </stack>' in blocks_by_label['even-step']}"
)

assert labels == [
    "odd-step",
    "even-step",
    "exit-step",
    "case-1",
    "case-5",
    "case-6",
    "case-7",
]
assert entries == ["1", "5", "6", "7"]
assert spec_text.count("collatzResult") == 0
assert "~>" not in odd_lhs_k and "~>" not in even_lhs_k
assert "0 |-> scope(.Map" in blocks_by_label["odd-step"]
assert "0 |-> scope(.Map" in blocks_by_label["even-step"]
assert "<stack> .List </stack>" in blocks_by_label["odd-step"]
assert "<stack> .List </stack>" in blocks_by_label["even-step"]
