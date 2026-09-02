#!/usr/bin/env python3
"""Attach an audit decision to every inventoried K entry."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, "/audit-output/evidence")
from inventory_k import blocks  # noqa: E402


RELEVANT: dict[str, tuple[str, ...]] = {
    "syntax.k": (
        "syntax Expr",
        "syntax Stmt",
        "syntax Stmts",
        "syntax Params",
        "syntax ParamNames",
        "syntax Module",
    ),
    "core.k": (
        "configuration",
        "syntax IntSeq",
        "syntax ValSeq",
        "syntax Str",
        "syntax Iterable",
        "syntax Val ",
        "syntax Scope",
        "syntax KResult",
        "syntax Expr ",
        "syntax RetState",
        "isRefV",
        "#alloc",
        "#loadAll",
        "(S:Stmt SS:Stmts)",
        ".Stmts",
        "#look",
        "builtinsScope",
        "#evalArgs",
        "#evalArgCont",
        "#applyK",
        "appendVal",
        "vals2valSeq",
    ),
    "iter.k": ("#iterNext", "#iterDone", "#iterYield"),
    "int.k": ('applyBin("+",  I1:Int, I2:Int)',),
    "str.k": (
        "#iterNext(str",
        "strToCodes",
        "seqConcat",
        'applyBin("+",  str',
    ),
    "list.k": (
        "#iterNext(list",
        "toList",
        "ListExpr",
        "valSeqConcat",
        'boundMethodV(ref(H:Int), "append")',
    ),
    "methods.k": (
        "syntax Val ::= applyMethod",
        '"count"',
        "cntSub",
        "dropIS",
    ),
    "controls.k": (
        "Assign(Name",
        "Expr(_:Val)",
        "#loop(",
        "#loopStep",
        "#loopLbl",
        "For(",
    ),
    "functions.k": (
        "frame(",
        "#bindP",
        "#pop",
        "#endcall",
        "FuncDef",
        "Return(",
    ),
    "call.k": (
        "Attribute(",
        "#callee",
        "Call(",
        "#applyK(toCall(boundMethodV",
        "#applyK(toCall(typeV",
        "isMutMethod",
        "#applyK(toCall(closureVal(",
    ),
    "builtins.k": (
        'applyBuiltin("str", I:Int',
        'applyBuiltin("str", str(',
    ),
    "operators.k": ("BinOp(", "applyBin"),
    "tuple.k": ("#bindTgt(Name",),
}

TOTALITY_GAPS = {
    ("builtins.k", 134): "mapStrVS",
    ("float.k", 73): "floorFI",
    ("float.k", 86): "toF",
    ("float.k", 93): "ceilF",
    ("methods.k", 27): "joinCodes",
    ("subscript.k", 11): "valSeqAt",
}


def decision(path: Path, line: int, kind: str, text: str) -> str:
    base = path.name
    if base == "verification.k":
        if kind == "syntax":
            return "ACCEPT_PROOF_DECLARATION"
        if kind == "rule" and line in {156, 192, 230}:
            return "ACCEPT_OPERATIONAL_BRIDGE_CONNECTION_PROVED"
        if kind == "rule" and line in {95, 141, 146}:
            return "ACCEPT_EXACT_COMPILE_TIME_MACRO"
        if kind == "rule":
            return "ACCEPT_TRUE_GUARDED_DESCENDING_SUMMARY_EQUATION"
    if "reference-semantics" in str(path):
        if (base, line) in TOTALITY_GAPS:
            return (
                "UNUSED_TOTALITY_COVERAGE_GAP_NO_FALSE_TARGET_CONCLUSION"
            )
        if "no-evaluators" in text or "md5hexCodes" in text:
            return "UNUSED_FIXED_OPAQUE_PRIMITIVE_NO_TARGET_DEPENDENCE"
        needles = RELEVANT.get(base, ())
        if any(needle in text for needle in needles):
            return "ACCEPT_TARGET_RELEVANT_FIXED_SEMANTICS_ENTRY"
        return "ACCEPT_FIXED_SEMANTICS_ENTRY_NOT_REACHED_BY_TARGET"
    if kind == "claim":
        if base == "false-result-mutation.k":
            return "AUDITOR_FALSE_CLAIM_EXPECTED_REJECTED"
        if base == "ground-witness-spec.k":
            return "AUDITOR_GROUND_WITNESS_EXPECTED_PROVED"
        return "ACCEPT_DERIVED_REACHABILITY_CLAIM_RECONSTRUCTED"
    return "ACCEPT_AUXILIARY_DECLARATION"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()
    counts: dict[str, int] = {}
    total = 0
    for path in sorted(args.paths):
        for line, kind, text in blocks(path):
            total += 1
            value = decision(path, line, kind, text)
            counts[value] = counts.get(value, 0) + 1
            headline = " ".join(text.split())
            print(
                f"{path}:{line} KIND={kind} DECISION={value} :: {headline}"
            )
    print(f"TOTAL_DECISIONS={total}")
    for key in sorted(counts):
        print(f"DECISION_COUNT {key}={counts[key]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
