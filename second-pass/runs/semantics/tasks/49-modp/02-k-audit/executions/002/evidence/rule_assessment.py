#!/usr/bin/env python3
"""Per-record assessment layered on the exhaustive K inventory."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, "/audit-output/evidence")
from rule_inventory import FILES, WORK, classify, records  # noqa: E402


PROOF_PATH: dict[str, set[int]] = {
    "reference-semantics/semantics/syntax.k": {9, 41, 56, 57, 60, 61},
    "reference-semantics/semantics/core.k": {
        13, 14, 15, 18, 25, 36, 37, 38, 39, 40, 41, 42, 49,
        124, 125, 126, 127, 130, 131, 132, 145, 152, 157, 158,
        185, 186, 189, 190, 191, 194, 195, 196, 209, 213, 214, 215,
    },
    "reference-semantics/semantics/functions.k": {
        8, 14, 63, 64, 78, 80, 85,
    },
    "reference-semantics/semantics/call.k": {19, 20, 21, 69},
    "reference-semantics/semantics/operators.k": {12},
    "reference-semantics/semantics/int.k": {15, 17, 19, 20},
    "reference-semantics/semantics/controls.k": {48},
    "reference-semantics/semantics/str.k": {13, 14, 15, 16},
    "verification.k": {9, 10, 14, 15, 22, 23},
    "spec.k": {6},
}

# These rules faithfully encode the supplied semantics' explicitly limited
# subset, but do not cover full CPython behavior on broader source inputs.
# They are constructor-disjoint from 49-modp's proof path.
LIMITED_UNUSED: dict[tuple[str, int], str] = {
    ("reference-semantics/semantics/float.k", 61):
        "Import is intentionally modeled as a no-op; CPython witness "
        "`import definitely_missing` raises ModuleNotFoundError.",
    ("reference-semantics/semantics/controls.k", 36):
        "Non-math ImportFrom is intentionally ignored; CPython binds names "
        "or raises, rather than silently continuing.",
    ("reference-semantics/semantics/controls.k", 43):
        "Unsupported math imported names are skipped; e.g. "
        "`from math import sin` binds sin in CPython.",
    ("reference-semantics/semantics/builtins.k", 156):
        "The multi-character int-string entry lacks digit validation; "
        'witness `int("1a")` raises in CPython but enters intDigAcc here.',
    ("reference-semantics/semantics/builtins.k", 160):
        "Horner step accepts arbitrary character codes; continuing the "
        '`int("1a")` witness computes 59.',
    ("reference-semantics/semantics/builtins.k", 187):
        "eval supports only its documented restricted grammar; broader "
        'witness `eval("4/2")` is not CPython-faithful.',
    ("reference-semantics/semantics/builtins.k", 236):
        'Unknown eval operator falls back to its left argument; with "4/2" '
        "this permits 4 instead of CPython 2.0.",
    ("reference-semantics/semantics/builtins.k", 266):
        'The restricted eval tokenizer admits "/" at multiplicative level '
        "without a matching division equation.",
    ("reference-semantics/semantics/methods.k", 58):
        "encode is an ASCII-model identity for every encoding argument; "
        '`"a".encode("utf-16")` is not the one-code sequence [97] in CPython.',
    ("reference-semantics/semantics/methods.k", 86):
        "Whitespace is restricted to four ASCII codes; CPython also strips "
        'vertical tab, so `"\\vX\\v".strip()` is a boundary witness.',
    ("reference-semantics/semantics/list.k", 27):
        "Shallow ==K differs from Python numeric cross-type equality; "
        "witness `[True] == [1]` is true in CPython.",
    ("reference-semantics/semantics/list.k", 28):
        "Shallow ==K gives the corresponding `[True] != [1]` discrepancy.",
    ("reference-semantics/semantics/list.k", 63):
        "Membership uses ==K; witness `True in [1]` is true in CPython.",
    ("reference-semantics/semantics/list.k", 65):
        "Membership continuation shares the `True in [1]` limitation.",
    ("reference-semantics/semantics/tuple.k", 18):
        "Tuple shallow ==K has the same witness `(True,) == (1,)`.",
    ("reference-semantics/semantics/tuple.k", 28):
        "Tuple shallow != has the corresponding cross-type discrepancy.",
    ("reference-semantics/semantics/dict.k", 38):
        "Dict key equality uses ==K; CPython aliases True and 1 as equal keys.",
    ("reference-semantics/semantics/dict.k", 39):
        "Dict key equality uses ==K; `{True: 0, 1: 1}` has one key in CPython.",
    ("reference-semantics/semantics/dict.k", 40):
        "Dict key scan shares the True/1 key-equivalence limitation.",
}


def main() -> None:
    counts: dict[str, int] = {}
    for path in FILES:
        relative = path.relative_to(WORK).as_posix()
        for line, keyword, statement in records(path):
            tags = classify(keyword, statement)
            if line in PROOF_PATH.get(relative, set()):
                decision = "ACCEPTED_PROOF_PATH"
                rationale = (
                    "Used by the submitted constructor/control path; checked "
                    "against regenerated syntax, concrete witnesses, positive "
                    "proof, ground body mutation, and Python integer arithmetic."
                )
            elif (relative, line) in LIMITED_UNUSED:
                decision = "DOMAIN_LIMITED_UNUSED"
                rationale = LIMITED_UNUSED[(relative, line)]
            elif "no-evaluators" in tags:
                decision = "OPAQUE_TRUST_BOUNDARY_UNUSED"
                rationale = (
                    "Supplied opaque/total symbol; no occurrence or dependent "
                    "value on the 49-modp execution/postcondition path."
                )
            elif keyword in {"syntax", "configuration", "context"}:
                decision = "ACCEPTED_DECLARATION_UNUSED"
                rationale = (
                    "Well-sorted supplied declaration; constructor/context is "
                    "not selected by the submitted term unless marked proof-path."
                )
            else:
                decision = "ACCEPTED_SUPPLIED_UNUSED"
                rationale = (
                    "Rule is constructor/guard-disjoint from the submitted "
                    "execution path; review found no way for it to rewrite or "
                    "constrain this claim."
                )
            counts[decision] = counts.get(decision, 0) + 1
            first = statement.splitlines()[0].strip()
            print(
                f"{relative}:{line}\t{','.join(tags)}\t{decision}\t"
                f"{rationale}\t{first}"
            )
    print("ASSESSMENT_COUNTS")
    for decision, count in sorted(counts.items()):
        print(f"{decision} {count}")


if __name__ == "__main__":
    main()
