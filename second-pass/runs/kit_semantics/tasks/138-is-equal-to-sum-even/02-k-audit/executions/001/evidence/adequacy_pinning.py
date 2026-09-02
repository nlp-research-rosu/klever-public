#!/usr/bin/env python3
"""Mechanical constructor pinning and concrete adequacy witnesses."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/138-audit")
SOLUTION_MPY = SCRATCH / "candidate/solution.mpy"
SPEC = SCRATCH / "candidate/spec.k"


def tokenize(text: str) -> list[str]:
    pattern = r'"(?:[^"\\]|\\.)*"|=>|~>|>=Int|==Int|andBool|\.[A-Za-z]+|#[A-Za-z]+|[A-Za-z_][A-Za-z0-9_-]*|-?[0-9]+|[(){},]|[^\s]'
    return re.findall(pattern, text)


def load_entry(path: Path, name: str):
    specification = importlib.util.spec_from_file_location(name, path)
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module.is_equal_to_sum_even


solution_tokens = tokenize(SOLUTION_MPY.read_text())
spec_text = SPEC.read_text()
spec_tokens = tokenize(spec_text)
matches = [
    index
    for index in range(len(spec_tokens) - len(solution_tokens) + 1)
    if spec_tokens[index : index + len(solution_tokens)] == solution_tokens
]
assert len(matches) == 1, f"expected one exact AST occurrence, got {matches}"
index = matches[0]
assert spec_tokens[index - 2 : index] == ["#loadAll", "("]
assert spec_tokens[index + len(solution_tokens) : index + len(solution_tokens) + 5] == [
    ")",
    "~>",
    "Call",
    "(",
    "Name",
]
assert spec_text.count("claim [") == 1
claim_conditions = re.findall(r"^\s+(requires|ensures)\s+(?!\")", spec_text, re.MULTILINE)
assert claim_conditions == [], claim_conditions

print(f"solution_constructor_token_count={len(solution_tokens)}")
print(f"spec_constructor_token_count={len(spec_tokens)}")
print(f"exact_solution_subsequence_offsets={matches}")
print("executed_term_prefix=#loadAll(exact_solution.mpy)~>Call(Name(...),Int(N))")
print("formal_precondition=none_beyond_N_sort_Int")
print("formal_postcondition=N>=Int8 andBool pyMod(N,2)==Int0")

canonical = load_entry(SCRATCH / "reference/canonical.py", "adequacy_canonical")
candidate = load_entry(SCRATCH / "candidate/solution.py", "adequacy_candidate")

initial_state = {
    "N": 8,
    "env": 0,
    "scope_0": "scope(.Map,parent(-1))",
    "scope_-1": "builtinsScope",
    "scopeLoc": 1,
    "heap": ".Map",
    "heapLoc": 0,
    "stack": ".List",
    "ret": "noRet",
    "exc": "NoExc",
    "exit-code": 0,
}
print(f"satisfying_entry_state={initial_state}")

for value in [-2, 7, 8, 9, 10]:
    claimed = value >= 8 and value % 2 == 0
    canonical_result = canonical(value)
    candidate_result = candidate(value)
    print(
        "ground_substitution "
        f"N={value} claimed={claimed} canonical={canonical_result} "
        f"candidate={candidate_result}"
    )
    assert claimed == canonical_result == candidate_result

print("ADEQUACY_PINNING=PASS")
