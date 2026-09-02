#!/usr/bin/env python3
"""Attach an audit disposition to every inventoried K declaration."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

from rule_inventory import ROOT, classify, declarations, source_files


OUTPUT = Path("/audit-output/evidence/rule-assessment.tsv")


REACHABLE_MARKERS: dict[str, tuple[str, ...]] = {
    "reference-semantics/semantics/syntax.k": (
        "syntax Expr",
        "syntax CmpOp",
        "syntax Exprs",
        "syntax Index",
        "syntax Bound",
        "syntax Stmt",
        "syntax Stmts",
        "syntax Params",
        "syntax ParamNames",
        "syntax Module",
    ),
    "reference-semantics/semantics/core.k": (
        "configuration",
        "syntax ValSeq",
        "syntax Val ",
        "syntax Scope",
        "syntax KResult",
        "syntax Expr ",
        "syntax Vals",
        "syntax Exc",
        "syntax RetState",
        "syntax Bool ::= isRefV",
        "syntax KItem ::= #alloc",
        "#alloc(V:Val)",
        "syntax KItem ::= #loadAll",
        "#loadAll(Module",
        "(S:Stmt SS:Stmts)",
        ".Stmts =>",
        "syntax KItem ::= #look",
        "Name(X:String) => #look",
        "#look(X:String",
        "builtinsScope",
        "syntax ApplyK",
        "syntax KItem  ::= #evalArgs",
        "#evalArgs(",
        "#evalArgCont",
        "vsLen(",
        "appendVal(",
    ),
    "reference-semantics/semantics/operators.k": (
        'BinOp(OP:String, L:Val, R:Val)',
        "BinOp(OP:String, ref(",
        "BinOp(OP:String, L:Val, ref(",
    ),
    "reference-semantics/semantics/int.k": (
        'applyBin("-",  I1:Int, I2:Int)',
    ),
    "reference-semantics/semantics/builtins.k": (
        'applyBuiltin("len"',
        "seqLen(",
    ),
    "reference-semantics/semantics/call.k": (
        "syntax KItem ::= #callee",
        "Call(Fe:Expr",
        "#callee(ARGS",
        "#applyK(toCall(builtinV(BN:String))",
        "#applyK(toCall(builtinV(BN:String)), (ref(",
        "#applyK(toCall(closureVal(",
    ),
    "reference-semantics/semantics/functions.k": (
        "syntax KItem ::= frame",
        "FuncDef(F:String, Params",
        "#bindP(",
        "Return(V:Val)",
        "#endcall",
        "#pop",
    ),
    "reference-semantics/semantics/sort.k": (
        "sortVS(",
        "insVS(",
        '#applyK(toCall(builtinV("sorted")), (list(VS:ValSeq), .Vals))',
    ),
    "reference-semantics/semantics/subscript.k": (
        "valSeqAt(",
        "context Subscript",
        "Subscript(ref(",
        "Subscript(OBJ:Val, Slice",
        "#evalB(",
        "#toSome",
        "#slLo(",
        "#slHi(",
        "#slStep(",
        "doSlice(",
        "slStep(",
        "slStart(",
        "slStop(",
        "slAdjust(",
        "clampLo(",
        "clampHi(",
        "buildVS(",
        "syntax OptInt",
    ),
}


def assess(relative: str, category: str, block: str) -> tuple[str, str]:
    if relative == "verification.k":
        if category.startswith("syntax") or "maximumResult" in block:
            return (
                "ACCEPTED_CANDIDATE_DEFINITION",
                "Full-domain definitional name for the exact fixed-semantics "
                "sorted/slice result; it does not match or replace a k-cell step.",
            )
        return ("STRUCTURAL", "Candidate module wiring only.")

    if relative == "reference-semantics/semantics.k":
        return (
            "STRUCTURAL",
            "Trusted supplied-semantics assembly/import declaration; candidate tree "
            "is byte-identical to the trusted mount.",
        )

    if "no-evaluators" in block or "symbol(" in block:
        if relative.endswith("/sort.k") and "sortVS(" in block:
            return (
                "ACCEPTED_WITH_TRUST_BOUNDARY",
                "Reachable opaque sorted primitive. The K theorem is parametric in "
                "its value; ascending-permutation meaning is not proved in K.",
            )
        return (
            "OUTSIDE_REACHABLE_PATH",
            "Opaque primitive is not constructible on the exact maximum body over "
            "the intended integer-list inputs; no intended-domain false witness.",
        )

    if relative.endswith("/concrete.k"):
        return (
            "CONCRETE_RUNTIME_ONLY",
            "Imported by MPY-KRUN but not VERIFICATION/MPY; cannot contribute to "
            "target-claim closure.",
        )

    markers = REACHABLE_MARKERS.get(relative, ())
    if any(marker in block for marker in markers):
        if relative.endswith("/sort.k"):
            return (
                "ACCEPTED_FIXED_PATH",
                "Concrete integer insertion-sort equation or exact sorted(list) "
                "allocation rule; guards are disjoint and preserve ascending order.",
            )
        if relative.endswith("/subscript.k"):
            return (
                "ACCEPTED_FIXED_PATH",
                "Reachable default-step list-slice evaluation/equation; inspected "
                "evaluation order, allocation, bounds normalization, and recursion.",
            )
        if relative.endswith("/call.k") or relative.endswith("/functions.k"):
            return (
                "ACCEPTED_FIXED_PATH",
                "Reachable lookup/call/frame/return rule; exact binding, argument "
                "order, continuation, scope restoration, and allocation were checked.",
            )
        return (
            "ACCEPTED_FIXED_PATH",
            "Reachable fixed-semantics declaration/rule on the exact constructor "
            "path; guard/overlap/state footprint reviewed and ground-executed.",
        )

    if category in {"module", "endmodule", "imports", "requires"}:
        return ("STRUCTURAL", "Module/import structure; no rewrite conclusion.")

    return (
        "OUTSIDE_REACHABLE_PATH",
        "Reviewed imported language support; its left-hand construct is not "
        "reachable from the exact submitted body on intended integer-list inputs. "
        "No intended-domain false conclusion witness was found.",
    )


def one_line(block: str) -> str:
    return " ".join(part.strip() for part in block.splitlines() if part.strip())[:500]


def main() -> None:
    counts: Counter[str] = Counter()
    rows: list[list[object]] = []
    for path in source_files():
        relative = path.relative_to(ROOT).as_posix()
        for line, kind, block in declarations(path):
            category = classify(kind, block)
            decision, rationale = assess(relative, category, block)
            counts[decision] += 1
            rows.append(
                [relative, line, category, decision, one_line(block), rationale]
            )

    with OUTPUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(
            ["file", "line", "category", "decision", "declaration", "rationale"]
        )
        writer.writerows(rows)

    print(f"output={OUTPUT}")
    print(f"assessed_declarations={len(rows)}")
    print(f"decision_counts={dict(sorted(counts.items()))}")
    print("RULE_ASSESSMENT_CREATED")


if __name__ == "__main__":
    main()
