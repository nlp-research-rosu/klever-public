#!/usr/bin/env python3
"""Ground witnesses for the entry claim's precondition and result."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.match_parens


def good_from(text: str, initial: int = 0) -> bool:
    balance = initial
    for char in text:
        if char == "(":
            balance += 1
        else:
            balance -= 1
            if balance < 0:
                return False
    return balance == 0


def expected_answer(left: str, right: str) -> str:
    return "Yes" if good_from(left + right) or good_from(right + left) else "No"


canonical = load(Path("/reference/canonical.py"), "canonical_ground")
generated = load(
    Path("/tmp/audit-work/audit-119-match-parens/solution.py"), "generated_ground"
)

# One concrete model of the symbolic entry precondition:
# BASE=.Map, MODULELOCALS=.Map, CALLER=0, N=1, empty heap/stack,
# noRet, NoExc, and exit code 0.  The scopes map contains only module scope 0.
base_keys: set[int] = set()
module_scope_key = 0
n = 1
precondition_checks = {
    "N>=1": n >= 1,
    "N+1_not_in_BASE": n + 1 not in base_keys,
    "N_not_in_BASE_plus_scope0": n not in (base_keys | {module_scope_key}),
}
print("entry_state=BASE:.Map MODULELOCALS:.Map CALLER:0 N:1")
print("cells=heap:.Map heapLoc:0 stack:.List ret:noRet exc:NoExc exit-code:0")
print("precondition_checks=", precondition_checks)
assert all(precondition_checks.values())

cases = [
    ("", ""),
    ("(", ")"),
    (")", "("),
    ("()(", ")"),
    (")", ")"),
    ("(()", "("),
]
for left, right in cases:
    assert set(left) <= {"(", ")"}
    assert set(right) <= {"(", ")"}
    expected = expected_answer(left, right)
    canonical_result = canonical([left, right])
    generated_result = generated([left, right])
    print(
        "ground_case",
        repr([left, right]),
        "A_codes=", [ord(c) for c in left],
        "B_codes=", [ord(c) for c in right],
        "claimed=", expected,
        "canonical=", canonical_result,
        "generated=", generated_result,
    )
    assert canonical_result == generated_result == expected
