#!/usr/bin/env python3
"""Mechanical claim/body pinning and concrete formal-witness checks."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path


def load_function(module_name: str, source: Path):
    spec = importlib.util.spec_from_file_location(module_name, source)
    if spec is None or spec.loader is None:
        raise RuntimeError(source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.digitSum


def balanced_calls(text: str, symbol: str) -> list[str]:
    calls: list[str] = []
    needle = symbol + "("
    cursor = 0
    while True:
        start = text.find(needle, cursor)
        if start < 0:
            return calls
        depth = 0
        quoted = False
        escaped = False
        end = None
        for index in range(start + len(symbol), len(text)):
            char = text[index]
            if quoted:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    quoted = False
                continue
            if char == '"':
                quoted = True
            elif char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0:
                    end = index + 1
                    break
        if end is None:
            raise ValueError(f"unbalanced {symbol} at {start}")
        calls.append(text[start:end])
        cursor = end


def normalize_k_constructor(text: str) -> str:
    text = re.sub(r"\s+", "", text)
    text = text.replace(".Exprs", "")
    text = text.replace(".Stmts", "")
    text = text.replace(",)", ")")
    return text


mpy = Path("/tmp/audit-work/reconstruction/solution.regenerated.mpy").read_text()
spec_text = Path("/tmp/audit-work/reconstruction/spec.k").read_text()

functions = balanced_calls(mpy, "FuncDef")
if len(functions) != 1:
    raise AssertionError(f"expected one FuncDef, found {len(functions)}")
function = functions[0]
prefix = 'FuncDef("digitSum", Params("s"),'
if not normalize_k_constructor(function).startswith(
    normalize_k_constructor(prefix)
):
    raise AssertionError(function)

compact_function = re.sub(r"\s+", "", function)
compact_prefix = re.sub(r"\s+", "", prefix)
body = compact_function[len(compact_prefix) : -1]
expected_closure = f'closureVal(("s",.ParamNames),{body}.Stmts,0)'

closures = balanced_calls(spec_text, "closureVal")
closure_equalities = [
    normalize_k_constructor(item) == normalize_k_constructor(expected_closure)
    for item in closures
]

entry_call_present = (
    normalize_k_constructor('Call(Name("digitSum"), str(CODES:IntSeq))')
    in normalize_k_constructor(spec_text)
)
entry_result_present = (
    normalize_k_constructor("=> digitSumIS(CODES)")
    in normalize_k_constructor(spec_text)
)

canonical = load_function("adequacy_canonical", Path("/reference/canonical.py"))
candidate = load_function("adequacy_candidate", Path("/candidate/solution.py"))


def summary(codes: list[int]) -> int:
    return sum(code if 65 <= code <= 90 else 0 for code in codes)


witnesses = [
    ("empty", []),
    ("both-branches", [64, 65, 90, 91]),
    ("supplied-model-gap", [192]),
]

print(f"translated_function_count={len(functions)}")
print(f"spec_closure_count={len(closures)}")
print(f"closure_constructor_equalities={closure_equalities}")
if closures and not closure_equalities[0]:
    print(f"expected_closure_normalized={normalize_k_constructor(expected_closure)}")
    print(f"actual_closure_normalized={normalize_k_constructor(closures[0])}")
print(f"entry_call_exact={entry_call_present}")
print(f"entry_result_exact={entry_result_present}")
print(
    "loop_precondition_witness="
    "CODES=.IntSeq,TOTAL=7,INPUT=.IntSeq,CHAR=str(.IntSeq),result=7"
)
for label, codes in witnesses:
    text = "".join(chr(code) for code in codes)
    print(
        f"entry_witness={label} codes={codes!r} "
        f"digitSumIS={summary(codes)} "
        f"candidate={candidate(text)} canonical={canonical(text)}"
    )

if not all(closure_equalities) or not entry_call_present or not entry_result_present:
    raise SystemExit(1)
