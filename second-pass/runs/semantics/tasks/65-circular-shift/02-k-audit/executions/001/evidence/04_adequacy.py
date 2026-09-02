#!/usr/bin/env python3
"""Concrete precondition witnesses and submitted-body pinning checks."""

from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.circular_shift


def matching_paren(text: str, open_index: int) -> int:
    depth = 0
    in_string = False
    escaped = False
    for i in range(open_index, len(text)):
        ch = text[i]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return i
    raise ValueError("unmatched parenthesis")


def split_top_level(text: str) -> list[str]:
    pieces: list[str] = []
    start = 0
    depth = 0
    in_string = False
    escaped = False
    for i, ch in enumerate(text):
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif ch == "," and depth == 0:
            pieces.append(text[start:i])
            start = i + 1
    pieces.append(text[start:])
    return pieces


def normalize_mpy_body(text: str) -> str:
    """Normalize translator sugar for empty statement sequences."""
    value = re.sub(r"\s+", "", text)
    # The translator prints an empty Stmts argument as an empty comma slot.
    value = value.replace(",)", ",.Stmts)")
    return value


case = Path("/tmp/audit-work/case")
solution_mpy = normalize_mpy_body((case / "solution.mpy").read_text(encoding="utf-8"))
verification = normalize_mpy_body((case / "verification.k").read_text(encoding="utf-8"))

module_prefix = 'Module(FuncDef("circular_shift",Params("x","shift"),'
assert solution_mpy.startswith(module_prefix)
assert solution_mpy.endswith("))")
submitted_body = solution_mpy[len(module_prefix) : -2]

needle = "closureVal("
closure_start = verification.index(needle) + len("closureVal")
closure_end = matching_paren(verification, closure_start)
closure_args = split_top_level(verification[closure_start + 1 : closure_end])
assert len(closure_args) == 3
assert closure_args[0] == '("x","shift")'
assert closure_args[2] == "0"
assert closure_args[1].startswith("(") and closure_args[1].endswith(")")
embedded_body = closure_args[1][1:-1]
assert submitted_body == embedded_body

canonical = load_entry(case.parent / "trusted" / "canonical.py", "trusted_canonical_adequacy")
generated = load_entry(case / "solution.py", "submitted_solution_adequacy")


def formal_result(x: int, shift: int) -> str:
    """Python reading of circularShiftSpec's two guarded equations."""
    s = str(x)
    length = len(s)
    if shift > length:
        return s[::-1]
    if shift <= length:
        return s[-shift:] + s[:-shift]
    raise AssertionError("guards were not exhaustive")


witnesses = [
    {"claim": "normal-shift", "x": 12, "shift": 1},
    {"claim": "normal-shift", "x": 12, "shift": 2},
    {"claim": "oversize-shift", "x": 12, "shift": 3},
    {"claim": "oversize-shift", "x": -123, "shift": 5},
]

for witness in witnesses:
    x = witness["x"]
    shift = witness["shift"]
    length = len(str(x))
    if witness["claim"] == "normal-shift":
        precondition = shift >= 0 and shift <= length
    else:
        precondition = shift >= 0 and shift > length
    claimed = formal_result(x, shift)
    expected = canonical(x, shift)
    actual = generated(x, shift)
    witness.update(
        {
            "len_str_x": length,
            "precondition_satisfied": precondition,
            "formal_result": claimed,
            "canonical_result": expected,
            "generated_result": actual,
            "all_results_equal": claimed == expected == actual,
        }
    )
    assert precondition
    assert claimed == expected == actual

print(
    json.dumps(
        {
            "submitted_body_equals_embedded_closure_body": True,
            "closure_parent_scope": 0,
            "witnesses": witnesses,
        },
        indent=2,
        sort_keys=True,
    )
)
