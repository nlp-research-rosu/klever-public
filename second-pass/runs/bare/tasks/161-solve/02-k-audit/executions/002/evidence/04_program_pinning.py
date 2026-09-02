#!/usr/bin/env python3
"""Mechanically show that the regenerated ground Program is an instance of the claim LHS."""

from __future__ import annotations

import json
from pathlib import Path


def label_name(term):
    if term.get("node") != "KApply":
        return None
    return term["label"]["name"]


def find_apply(term, wanted):
    if isinstance(term, dict):
        if label_name(term) == wanted:
            return term
        for value in term.values():
            found = find_apply(value, wanted)
            if found is not None:
                return found
    elif isinstance(term, list):
        for value in term:
            found = find_apply(value, wanted)
            if found is not None:
                return found
    return None


substitution = {}


def unify(pattern, ground, path="$"):
    if isinstance(pattern, dict) and pattern.get("node") == "KVariable":
        name = pattern["name"]
        previous = substitution.get(name)
        if previous is not None and previous != ground:
            raise AssertionError(f"inconsistent substitution for {name} at {path}")
        substitution[name] = ground
        return
    if type(pattern) is not type(ground):
        raise AssertionError(f"type mismatch at {path}")
    if isinstance(pattern, dict):
        if set(pattern) != set(ground):
            raise AssertionError(f"key mismatch at {path}")
        for key in pattern:
            unify(pattern[key], ground[key], f"{path}.{key}")
        return
    if isinstance(pattern, list):
        if len(pattern) != len(ground):
            raise AssertionError(f"length mismatch at {path}")
        for index, (left, right) in enumerate(zip(pattern, ground)):
            unify(left, right, f"{path}[{index}]")
        return
    if pattern != ground:
        raise AssertionError(f"value mismatch at {path}: {pattern!r} != {ground!r}")


spec = json.loads(
    Path("/tmp/audit-work/k-proof/spec-compiled.json").read_text()
)["term"]
solution = json.loads(
    Path("/tmp/audit-work/k-proof/solution-ast.json").read_text()
)["term"]

k_cell = find_apply(spec, "<k>")
if k_cell is None:
    raise AssertionError("no <k> cell in compiled claim")
rewrite = k_cell["args"][0]
if rewrite.get("node") != "KRewrite":
    raise AssertionError("claim <k> cell does not contain a rewrite")
claim_program_pattern = rewrite["lhs"]

unify(claim_program_pattern, solution)

variables_in_ground = []


def collect_variables(term):
    if isinstance(term, dict):
        if term.get("node") == "KVariable":
            variables_in_ground.append(term["name"])
        for value in term.values():
            collect_variables(value)
    elif isinstance(term, list):
        for value in term:
            collect_variables(value)


collect_variables(solution)
print("ground_solution_has_variables:", bool(variables_in_ground))
print("claim_program_unifies_with_ground_solution: True")
print("claim_pattern_substitution_count:", len(substitution))
for name, value in sorted(substitution.items()):
    print(
        "substitution",
        name,
        "node=",
        value.get("node"),
        "label=",
        label_name(value),
        "arity=",
        value.get("arity"),
    )

expected_vars = {"_ISALPHA_ARGS", "_SWAPCASE_ARGS"}
print("only_expected_argument_wildcards:", set(substitution) == expected_vars)
empty_exprs_label = '.List{"_,__MPY-SYNTAX_Exprs_Expr_Exprs"}_Exprs'
both_empty = all(
    label_name(value) == empty_exprs_label and value.get("arity") == 0
    for value in substitution.values()
)
print("both_actual_argument_lists_are_empty:", both_empty)

raise SystemExit(
    0
    if not variables_in_ground
    and set(substitution) == expected_vars
    and both_empty
    else 1
)
