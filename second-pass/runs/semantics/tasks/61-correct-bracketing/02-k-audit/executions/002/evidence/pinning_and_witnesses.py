#!/usr/bin/env python3
"""Mechanical claim/program comparison and concrete claim-result witnesses."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/proof")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.correct_bracketing


def matching_parenthesis(text: str, open_index: int) -> int:
    depth = 0
    quote = False
    escaped = False
    for index in range(open_index, len(text)):
        char = text[index]
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quote = False
            continue
        if char == '"':
            quote = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return index
    raise ValueError("unbalanced constructor term")


def split_top_level_args(text: str) -> list[str]:
    args: list[str] = []
    start = 0
    depth = 0
    quote = False
    escaped = False
    for index, char in enumerate(text):
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quote = False
            continue
        if char == '"':
            quote = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0:
            args.append(text[start:index])
            start = index + 1
    args.append(text[start:])
    return args


def constructor(text: str, name: str) -> tuple[str, int, int]:
    start = text.index(name + "(")
    open_index = start + len(name)
    end = matching_parenthesis(text, open_index)
    return text[open_index + 1 : end], start, end


def normalize(text: str) -> str:
    text = re.sub(r":[A-Za-z][A-Za-z0-9]*", "", text)
    text = text.replace(".Stmts", "")
    return re.sub(r"\s+", "", text)


solution = (SCRATCH / "solution.mpy").read_text()
spec_text = (SCRATCH / "spec.k").read_text()

for_inner, for_start, for_end = constructor(solution, "For")
loop_inner, loop_start, loop_end = constructor(spec_text, "#loop")
for_args = split_top_level_args(for_inner)
loop_args = split_top_level_args(loop_inner)
assert len(for_args) == 3
assert len(loop_args) == 3

target_equal = normalize(for_args[0]) == normalize(loop_args[1])
body_equal = normalize(for_args[2]) == normalize(loop_args[2])

solution_tail_text = solution[for_end + 1 :]
spec_tail_text = spec_text[loop_end + 1 :]
solution_return, _, _ = constructor(solution_tail_text, "Return")
spec_return, _, _ = constructor(spec_tail_text, "Return")
return_equal = normalize(solution_return) == normalize(spec_return)

claim_lhs = spec_text[spec_text.index("<k>") : spec_text.index("=> correctCodes")]
omitted_terms = {
    "Module": "Module(" not in claim_lhs,
    "FuncDef": "FuncDef(" not in claim_lhs,
    "function binding name": '"correct_bracketing"' not in claim_lhs,
    "balance initialization": 'Assign(Name("balance"), Int(0))' not in claim_lhs,
    "bracket initialization": 'Assign(Name("bracket"), Str(""))' not in claim_lhs,
    "call setup": "Call(" not in claim_lhs,
}

print(f"loop_target_constructor_equal={target_equal}")
print(f"loop_body_constructor_equal_after_empty-Stmts_normalization={body_equal}")
print(f"tail_return_constructor_equal={return_equal}")
for description, omitted in omitted_terms.items():
    print(f"claim_omits_{description.replace(' ', '_')}={omitted}")
assert target_equal and body_equal and return_equal
assert all(omitted_terms.values())
print("PINNING_RESULT: the claim executes a matching loop-and-return suffix, but omits the submitted Module/FuncDef binding, both initialization statements, call setup, and the full function entry transition.")


def correct_codes(brackets: str, balance: int) -> bool:
    for char in brackets:
        if char == "(":
            balance += 1
        elif balance == 0:
            return False
        else:
            balance -= 1
    return balance == 0


canonical = load_function("trusted_canonical_witness", SCRATCH / "canonical.py")
candidate = load_function("candidate_solution_witness", SCRATCH / "solution.py")
witnesses = [
    ("", 0, ""),
    ("()", 0, "()"),
    ("(", 0, "("),
    (")", 0, ")"),
    (")", 1, "()"),
    ("())", 0, "())"),
]
print("SATISFYING_PRECONDITION: B >= 0; choose concrete scopes exactly as in spec.k with INPUT=S, OLD='', GLOBALS=.Map, HEAP=.Map, HLOC=0, CONT=.K.")
for suffix, balance, whole_input in witnesses:
    claimed = correct_codes(suffix, balance)
    canonical_value = canonical(whole_input)
    candidate_value = candidate(whole_input)
    print(
        f"WITNESS S={suffix!r} B={balance} whole_input={whole_input!r} "
        f"correctCodes={claimed} canonical={canonical_value} candidate={candidate_value}"
    )
    assert claimed == canonical_value == candidate_value
print("SUMMARY: all concrete satisfying substitutions agree with both Python implementations")
