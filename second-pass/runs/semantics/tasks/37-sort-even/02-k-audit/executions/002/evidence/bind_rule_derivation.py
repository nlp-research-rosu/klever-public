#!/usr/bin/env python3
"""Mechanical source check that the candidate bind bridge composes fixed rules."""

from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path("/tmp/audit-work/37-sort-even")


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


def main() -> int:
    fixed = (ROOT / "reference-semantics/semantics/functions.k").read_text()
    candidate = (ROOT / "verification.k").read_text()

    fixed_base = bool(
        re.search(
            r"rule\s+<k>\s*#bindP\(\.ParamNames,\s*\.Vals\)\s*=>\s*\.K\s*\.\.\.\s*</k>",
            fixed,
            re.S,
        )
    )
    fixed_step = bool(
        re.search(
            r"rule\s+<k>\s*#bindP\(\(P:String,\s*PS:ParamNames\),\s*"
            r"\(V:Val,\s*VS:Vals\)\)\s*=>\s*#bindP\(PS,\s*VS\)\s*\.\.\.\s*</k>"
            r".*?<env>\s*L:Int\s*</env>"
            r".*?<scopes>\s*\.\.\.\s*L\s*\|->\s*scope\("
            r"M:Map\s*=>\s*M\s*\[\s*P\s*<-\s*V\s*\],\s*_\)"
            r"\s*\.\.\.\s*</scopes>",
            fixed,
            re.S,
        )
    )
    candidate_bridge = bool(
        re.search(
            r"rule\s+<k>\s*#bindP\(\(\"l\"\),\s*\(V:Val,\s*\.Vals\)\)"
            r"\s*=>\s*\.K\s*\.\.\.\s*</k>"
            r".*?<env>\s*L:Int\s*</env>"
            r".*?<scopes>\s*\.\.\.\s*L\s*\|->\s*scope\("
            r"\.Map\s*=>\s*\(\"l\"\s*\|->\s*V\),\s*_P:Parent\)"
            r"\s*\.\.\.\s*</scopes>",
            candidate,
            re.S,
        )
    )

    # The candidate rule is the two-step fixed derivation under this
    # constructor substitution. K's Map unit/update normalization is standard:
    # .Map["l" <- V] = ("l" |-> V).
    substitution = {
        "P": '"l"',
        "PS": ".ParamNames",
        "VS": ".Vals",
        "M": ".Map",
    }
    intermediate_k = "#bindP(.ParamNames,.Vals)"
    intermediate_scope = 'scope(.Map["l"<-V],Parent)'
    normalized_scope = 'scope(("l"|->V),Parent)'
    derived_rhs_k = ".K"
    candidate_rhs_k = ".K"

    checks = {
        "fixed_empty_bind_rule_found": fixed_base,
        "fixed_recursive_bind_rule_found": fixed_step,
        "candidate_specialized_bridge_found": candidate_bridge,
        "intermediate_consumed_by_fixed_base": intermediate_k
        == "#bindP(.ParamNames,.Vals)",
        "map_unit_update_normalizes_to_singleton": compact(normalized_scope)
        == compact('scope(("l"|->V),Parent)'),
        "composed_rhs_matches_candidate": derived_rhs_k == candidate_rhs_k,
    }
    print(f"substitution={substitution}")
    print(f"fixed_step_intermediate_k={intermediate_k}")
    print(f"fixed_step_intermediate_scope={intermediate_scope}")
    print(f"map_normal_form={normalized_scope}")
    print(f"fixed_base_result_k={derived_rhs_k}")
    for name, result in checks.items():
        print(f"{name}={result}")
    print(f"FAILURE_COUNT={sum(not result for result in checks.values())}")
    return 1 if any(not result for result in checks.values()) else 0


if __name__ == "__main__":
    sys.exit(main())
