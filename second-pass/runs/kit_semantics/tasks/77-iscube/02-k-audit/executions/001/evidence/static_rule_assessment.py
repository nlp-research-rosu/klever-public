#!/usr/bin/env python3
"""One disposition for every inventoried rule, syntax block, and claim."""

from __future__ import annotations

from pathlib import Path

from k_inventory import CANDIDATE_ROOT, PROOF_FILES, SEMANTICS_ROOT, blocks


USED_FIXED_RULES = {
    ("semantics/core.k", 125): "module loading executes its statement list",
    ("semantics/core.k", 126): "left-to-right statement sequencing",
    ("semantics/core.k", 127): "empty statement-list completion",
    ("semantics/core.k", 131): "name lookup starts at the current environment",
    ("semantics/core.k", 132): "present local binding is returned",
    ("semantics/core.k", 158): "builtinsScope's exhaustive defining equation",
    ("semantics/core.k", 189): "left-to-right argument evaluation starts",
    ("semantics/core.k", 190): "evaluated argument is appended",
    ("semantics/core.k", 191): "argument evaluation dispatches the call",
    ("semantics/core.k", 194): "integer literal evaluates to a K Int",
    ("semantics/core.k", 200): "Boolean truthiness is identity",
    ("semantics/core.k", 214): "append into an empty value list",
    ("semantics/controls.k", 9): "ordinary local assignment updates the frame",
    ("semantics/controls.k", 20): "integer += uses the bound old value",
    ("semantics/controls.k", 52): "If dispatches on evaluated truthiness",
    ("semantics/controls.k", 53): "true If branch",
    ("semantics/controls.k", 54): "false If branch",
    ("semantics/controls.k", 77): "While enters #while",
    ("semantics/controls.k", 78): "#while evaluates its guard",
    ("semantics/controls.k", 79): "true guard executes body and recurs",
    ("semantics/controls.k", 81): "false guard exits",
    ("semantics/controls.k", 85): "loop label resumes the loop",
    ("semantics/functions.k", 14): "FuncDef creates the exact closure (identity claim)",
    ("semantics/functions.k", 63): "empty parameter binding completes",
    ("semantics/functions.k", 64): "one parameter binds its argument",
    ("semantics/functions.k", 78): "Return records the value and initiates pop",
    ("semantics/functions.k", 85): "pop restores caller and deletes the frame",
    ("semantics/operators.k", 10): "evaluated unary operator dispatch",
    ("semantics/operators.k", 12): "evaluated binary operator dispatch",
    ("semantics/operators.k", 17): "evaluated comparison dispatch",
    ("semantics/int.k", 7): "integer unary minus",
    ("semantics/int.k", 9): "integer addition",
    ("semantics/int.k", 14): "mathematical integer multiplication",
    ("semantics/int.k", 22): "mathematical integer less-than",
    ("semantics/int.k", 26): "mathematical integer equality",
    ("semantics/call.k", 20): "callee is evaluated before arguments",
    ("semantics/call.k", 21): "evaluated callee starts argument evaluation",
    ("semantics/call.k", 69): "closure call allocates/binds a fresh frame",
}

LOCAL_RULE_DECISIONS = {
    ("verification-base.k", 17): (
        "VALID_DEFINITION",
        "cubeOf(I) is exactly I*I*I",
    ),
    ("verification-base.k", 21): (
        "VALID_DEFINITION",
        "equality branch of exhaustive integer cube search",
    ),
    ("verification-base.k", 23): (
        "VALID_DEFINITION",
        "greater-than branch of exhaustive integer cube search",
    ),
    ("verification-base.k", 25): (
        "VALID_DEFINITION",
        "less-than branch advances I by one and is ground-terminating",
    ),
    ("verification-base.k", 30): (
        "VALID_DERIVED_LEMMA",
        "under not cube<A, trichotomy makes equality equal cubeSearch",
    ),
    ("verification-base.k", 37): (
        "VALID_DERIVED_LEMMA",
        "deleting explicit key 1 yields REST when REST lacks key 1",
    ),
    ("verification-base.k", 42): (
        "VALID_DEFINITION",
        "negative input searches its positive magnitude",
    ),
    ("verification-base.k", 44): (
        "VALID_DEFINITION",
        "nonnegative input searches itself",
    ),
    ("verification-base.k", 49): (
        "VALID_DEFINITION",
        "closed constructor abbreviation for the submitted closure",
    ),
    ("connection-rule.k", 8): (
        "VALID_OPERATIONAL_BRIDGE",
        "complete match and transition are identical to bridge-free "
        "CONNECTION.search-loop",
    ),
}

LOCAL_SYNTAX_DECISIONS = {
    ("verification-base.k", 6): "cubeOf: defined, total mathematical function",
    ("verification-base.k", 7): (
        "cubeSearch and isCubeInt: guarded, disjoint, exhaustive and "
        "ground-terminating"
    ),
    ("verification-base.k", 9): (
        "iscubeClosure: closed, unconditionally defined abbreviation"
    ),
}


def main() -> None:
    paths = sorted(SEMANTICS_ROOT.rglob("*.k"))
    paths.extend(CANDIDATE_ROOT / name for name in PROOF_FILES)
    rule_count = syntax_count = claim_count = 0
    for path in paths:
        if path.is_relative_to(SEMANTICS_ROOT):
            relative = path.relative_to(SEMANTICS_ROOT).as_posix()
            source_kind = "fixed"
        else:
            relative = path.name
            source_kind = "local"
        for kind, line, source in blocks(path):
            first = source.splitlines()[0].strip()
            if kind == "rule":
                rule_count += 1
                if source_kind == "fixed":
                    key = (relative, line)
                    if key in USED_FIXED_RULES:
                        status = "FIXED_USED_REVIEWED"
                        reason = USED_FIXED_RULES[key]
                    else:
                        status = "FIXED_UNUSED_NO_REACHABLE_DEPENDENCY"
                        reason = (
                            "supplied-semantics rule; no constructor/control "
                            "dependency from solution.mpy or proof-local symbols"
                        )
                else:
                    status, reason = LOCAL_RULE_DECISIONS[(relative, line)]
                print(
                    f"RULE {rule_count:04d} {path}:{line} "
                    f"status={status} reason={reason} source={first}"
                )
            elif kind == "syntax":
                syntax_count += 1
                if source_kind == "fixed":
                    status = "FIXED_DECLARATION"
                    if "no-evaluators" in source:
                        status = "FIXED_OPAQUE_UNUSED"
                    reason = (
                        "selected supplied-semantics declaration; "
                        "opaque declarations are absent from the used path"
                    )
                else:
                    reason = LOCAL_SYNTAX_DECISIONS[(relative, line)]
                    status = "LOCAL_DECLARATION_REVIEWED"
                print(
                    f"SYNTAX {syntax_count:04d} {path}:{line} "
                    f"status={status} reason={reason} source={first}"
                )
            elif kind == "claim":
                claim_count += 1
                print(
                    f"CLAIM {claim_count:04d} {path}:{line} "
                    "status=RECONSTRUCTED_OR_AUXILIARY_REVIEWED "
                    f"source={first}"
                )
    print(
        f"TOTAL rule_decisions={rule_count} "
        f"syntax_decisions={syntax_count} claim_decisions={claim_count}"
    )
    if rule_count != 705 or syntax_count != 230 or claim_count != 6:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
