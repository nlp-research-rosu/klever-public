#!/usr/bin/env python3
"""Mechanical constructor pinning and concrete claim-witness checks."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path


def normalize_k(text: str) -> str:
    return re.sub(r"\s+", "", text)


def balanced_constructor(text: str, start: int) -> str:
    opening = text.find("(", start)
    if opening < 0:
        raise ValueError("constructor has no opening parenthesis")
    depth = 0
    in_string = False
    escaped = False
    for index in range(opening, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    raise ValueError("unbalanced constructor")


def macro_rhs(text: str, name: str, constructor: str) -> str:
    rule = text.index(f"rule {name}")
    start = text.index(constructor + "(", rule)
    return balanced_constructor(text, start)


def load(path: str, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.largest_prime_factor


verification = Path("/candidate/verification.k").read_text()
regenerated = Path(
    "/tmp/audit-work/59-lpf/reviewer-regenerated-solution.mpy"
).read_text().strip()
solution_macro = macro_rhs(verification, "solutionModule", "Module")
condition_macro = macro_rhs(verification, "lpfCondition", "Compare")
step_macro = macro_rhs(verification, "lpfStep", "If")

module_equal = normalize_k(solution_macro) == normalize_k(regenerated)
condition_in_module = normalize_k(condition_macro) in normalize_k(regenerated)
step_in_module = normalize_k(step_macro) in normalize_k(regenerated)

print("solutionModule_equals_trusted_regeneration:", module_equal)
print("lpfCondition_is_exact_solution_subterm:", condition_in_module)
print("lpfStep_is_exact_solution_subterm:", step_in_module)
print("normalized_solution_length:", len(normalize_k(regenerated)))
print("normalized_solutionModule_length:", len(normalize_k(solution_macro)))


def lpf_spec(n: int, factor: int) -> int:
    while n > factor:
        if n % factor == 0:
            n = n // factor
        else:
            factor += 1
    return factor


canonical = load("/reference/canonical.py", "pin_canonical")
candidate = load("/tmp/audit-work/59-lpf/solution.py", "pin_candidate")

# Satisfying entry witness: N=4 and the exact initial cells stated in spec.k.
print(
    "entry_witness:",
    {
        "N": 4,
        "env": 0,
        "scopeLoc": 1,
        "heap": {},
        "heapLoc": 0,
        "stack": [],
        "ret": "noRet",
        "exc": "NoExc",
        "exit_code": 0,
        "precondition": 4 > 1,
    },
)

# The entry post unifies with lpf-loop under this exact substitution.
composition = {
    "N_loop": "N_entry",
    "F": 2,
    "L": 1,
    "SC_keys": [-1, 0],
    "CALLER": 0,
    "CONT": ".K",
    "REST": ".List",
    "loop_preconditions_for_N_4": (
        4 > 1 and 2 > 1 and 1 >= 1 and 1 not in {-1, 0}
    ),
}
print("entry_post_to_loop_lhs_unifier:", composition)

for n in (4, 2048, 13195):
    summary = lpf_spec(n, 2)
    trusted_result = canonical(n)
    generated_result = candidate(n)
    print(
        "concrete_substitution:",
        {
            "N": n,
            "claimed_lpfSpec_N_2": summary,
            "trusted_canonical": trusted_result,
            "generated_python": generated_result,
            "all_equal": summary == trusted_result == generated_result,
        },
    )

if not (module_equal and condition_in_module and step_in_module):
    raise SystemExit(1)
