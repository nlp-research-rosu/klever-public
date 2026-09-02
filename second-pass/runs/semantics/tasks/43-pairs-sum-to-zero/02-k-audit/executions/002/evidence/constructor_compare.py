#!/usr/bin/env python3
"""Mechanical constructor-level comparison of solution.mpy and pairsBody."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path("/tmp/audit-work")
solution = (ROOT / "solution.mpy").read_text()
verification = (ROOT / "verification.k").read_text()
spec = (ROOT / "spec.k").read_text()

prefix = 'Module(\n  FuncDef("pairs_sum_to_zero", Params("l"),'
assert solution.startswith(prefix), "translated module/function binding changed"
assert solution.rstrip().endswith("))"), "unexpected translated module suffix"
submitted_body = solution.rstrip()[len(prefix):-2].strip()

match = re.search(
    r"rule\s+pairsBody\s*=>\s*(.*?)\n\n\s*// Mathematical oracle:",
    verification,
    re.DOTALL,
)
assert match is not None, "could not extract pairsBody equation"
alias_rhs = match.group(1).strip()


def parse_module(expression: str) -> object:
    completed = subprocess.run(
        [
            "kast",
            "--definition",
            str(ROOT / "reviewer-verification-kompiled"),
            "--module",
            "PAIRS-VERIFICATION",
            "--sort",
            "Module",
            "--output",
            "json",
            "--expression",
            expression,
        ],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    parsed = json.loads(completed.stdout)
    return parsed["term"]


# K-definition source spells empty list sorts explicitly; the external `.mpy`
# constructor language uses the corresponding empty concrete-list notation.
# Convert only those notational differences, then ask the trusted compiled
# parser for both full Module constructor trees.
alias_external = alias_rhs.replace("ListExpr(.Exprs)", "ListExpr()")
alias_external = re.sub(
    r"\(\s*(Name\(\"value\"\))\s*,\s*\.Exprs\s*\)",
    r"\1",
    alias_external,
)
alias_external = alias_external.replace(".Stmts", "")
submitted_module = solution.strip()
alias_module = (
    'Module(\n  FuncDef("pairs_sum_to_zero", Params("l"),\n'
    + alias_external
    + "))"
)
submitted_ast = parse_module(submitted_module)
alias_ast = parse_module(alias_module)


def stable_hash(term: object) -> str:
    encoded = json.dumps(term, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


closure_term = 'closureVal(("l", .ParamNames), pairsBody, 0)'
entry_labels = ["bounded-empty", "bounded-one", "bounded-two", "all-integer-lists"]
for label in entry_labels:
    label_at = spec.index(f"claim [{label}]")
    next_at = spec.find("claim [", label_at + 1)
    section = spec[label_at:] if next_at < 0 else spec[label_at:next_at]
    assert closure_term in section, f"{label} does not execute the generated closure signature"

print('translated_function_name="pairs_sum_to_zero"')
print('translated_params=("l", .ParamNames)')
print("translated_definition_environment=0")
print(f"submitted_body_kast_sha256={stable_hash(submitted_ast)}")
print(f"pairsBody_rhs_kast_sha256={stable_hash(alias_ast)}")
print(f"constructor_ast_equal={submitted_ast == alias_ast}")
print(f"entry_claims_checked={entry_labels}")
print(f"entry_closure_term={closure_term}")
