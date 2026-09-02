#!/usr/bin/env python3
"""Mechanical constructor-level pinning check for the submitted MPY module."""

from __future__ import annotations

import re
from pathlib import Path


root = Path("/tmp/audit-work/reconstruction")
solution_term = (root / "solution.mpy").read_text()
verification = (root / "verification.k").read_text()


def rule_rhs(symbol: str, next_marker: str) -> str:
    pattern = (
        rf"rule\s+{re.escape(symbol)}\s*=>\s*(.*?)"
        rf"(?=\n\s*{re.escape(next_marker)})"
    )
    match = re.search(pattern, verification, flags=re.DOTALL)
    if match is None:
        raise AssertionError(f"could not extract rule for {symbol}")
    return match.group(1).strip()


def normalized(term: str) -> str:
    # These terms contain no whitespace-bearing string literals.
    return re.sub(r"\s+", "", term)


result_rhs = rule_rhs("willItFlyResult", "// The translated entry point")
module_rhs = rule_rhs("willItFlyModule", 'syntax Val ::= "willItFlyClosure"')
closure_rhs = rule_rhs("willItFlyClosure", "endmodule")

expanded_module = module_rhs.replace("willItFlyResult", result_rhs)
expanded_closure = closure_rhs.replace("willItFlyResult", result_rhs)
expected_closure = (
    'closureVal(("q", "w"), Return(' + result_rhs + "), 0)"
)

assert normalized(expanded_module) == normalized(solution_term)
assert normalized(expanded_closure) == normalized(expected_closure)

print("module_alias_expands_to_solution_mpy=true")
print("prebound_closure_matches_translated_params_body_and_defining_scope=true")
print(f"normalized_module_characters={len(normalized(solution_term))}")
print("RESULT: claim term mechanically pins the submitted MPY function")
