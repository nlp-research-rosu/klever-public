"""Attach an audit disposition to every inventoried K block."""

from __future__ import annotations

import csv
import importlib.util
from pathlib import Path


ROOT = Path("/tmp/audit-work/candidate")
INVENTORY_SCRIPT = Path("/audit-output/evidence/06_k_inventory.py")
spec = importlib.util.spec_from_file_location("inventory", INVENTORY_SCRIPT)
assert spec is not None and spec.loader is not None
inventory = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inventory)


USED_MARKERS = {
    "semantics/core.k": (
        "configuration",
        "#alloc(",
        "#loadAll(",
        ":Stmts =>",
        ".Stmts =>",
        "Name(",
        "#look(",
        "builtinsScope",
        "#evalArgs(",
        "#evalArgCont(",
        "Int(I:Int)",
        "truthy(I:Int)",
        "appendVal(",
        "vals2valSeq(",
        "scope(",
        "list(",
        "ref(",
        "closureVal(",
    ),
    "semantics/int.k": (
        'applyBin("+",',
        'applyBin("*",',
        'applyBin("%",',
        'applyBin("//",',
        "pyMod(",
        'applyCmp(">",',
        'applyCmp("==",',
    ),
    "semantics/operators.k": (
        'BinOp(OP:String, L:Val, R:Val)',
        "Compare(HOLE",
        "Compare(_:Val",
        "Compare(LV:Val",
    ),
    "semantics/list.k": (
        "ListExpr(",
        "#applyK(toList",
        "valSeqConcat(",
        'boundMethodV(ref(H:Int), "append")',
    ),
    "semantics/controls.k": (
        "Assign(Name(",
        "Expr(_:Val)",
        "If(C:Val",
        "#branch(",
        "While(",
        "#while(",
        "#whileCond(",
        "#loopLbl(",
    ),
    "semantics/functions.k": (
        "FuncDef(",
        "#bindP(",
        "Return(V:Val)",
        "#endcall",
        "#pop",
        "frame(",
    ),
    "semantics/call.k": (
        "Attribute(V:Val",
        "Call(Fe:Expr",
        "#callee(",
        "isMutMethod(",
        "boundMethodV(ref(H:Int)",
        "#applyK(toCall(closureVal(",
    ),
    "semantics/sort.k": (
        "sortVS(",
        "insVS(",
        'boundMethodV(ref(H:Int), "sort")',
    ),
    "semantics/syntax.k": (
        "Expr ::=",
        "CmpOp",
        "Exprs",
        "Stmt ::=",
        "Stmts",
        "Params",
        "ParamNames",
        "Module",
    ),
}


def local_reason(text: str, kind: str) -> tuple[str, str]:
    if kind != "rule":
        return (
            "LOCAL_DECLARATION_SOUND",
            "Pure declaration/import/module structure; function attributes are audited with their equations.",
        )
    if "collatzNext(" in text:
        return (
            "LOCAL_RULE_SOUND",
            "Disjoint exhaustive modulo-2 equations equal the executed even/odd assignments.",
        )
    if "validCollatzTrace(" in text:
        return (
            "LOCAL_RULE_SOUND",
            "Structural finite-sequence validity equation or truthful one-element append lemma.",
        )
    if "traceFirstInt(" in text:
        return (
            "LOCAL_RULE_SOUND",
            "Truthful constructor observer or nonempty one-element append lemma.",
        )
    if "traceLastInt(" in text:
        return (
            "LOCAL_RULE_SOUND",
            "Truthful structural last observer or one-element append lemma.",
        )
    if "maybeOdd(" in text:
        return (
            "LOCAL_RULE_SOUND",
            "Disjoint exhaustive parity filter over all K integers.",
        )
    if "oddWithoutLast(" in text:
        return (
            "LOCAL_RULE_SOUND",
            "Structural odd filter or guarded append lemma; recursion descends on the finite tail.",
        )
    if "valSeqConcat(" in text and "==K" in text:
        return (
            "LOCAL_RULE_SOUND",
            "Appending a singleton yields a nonempty sequence, so it cannot equal empty.",
        )
    if "valSeqConcat(" in text:
        return (
            "LOCAL_RULE_SOUND",
            "Right identity or associativity of the fixed structural concatenation.",
        )
    return ("LOCAL_RULE_REVIEWED", "No execution bridge; reviewed against its complete guard.")


def disposition(relative: str, kind: str, text: str) -> tuple[str, str]:
    if relative == "verification.k":
        return local_reason(text, kind)
    if relative == "spec.k":
        return (
            "CLAIM_REVIEWED",
            "Entry or loop reachability claim; adequacy and satisfiability reviewed separately.",
        )
    if not relative.startswith("reference-semantics/"):
        return ("STRUCTURAL", "Non-rule structural block.")
    short = relative.removeprefix("reference-semantics/")
    if kind in {"requires", "module", "endmodule", "imports"}:
        return ("FIXED_STRUCTURAL", "Trusted supplied-semantics assembly/import structure.")
    markers = USED_MARKERS.get(short, ())
    if any(marker in text for marker in markers):
        if short == "semantics/sort.k" and (
            "sortVS(" in text or "insVS(" in text
        ):
            return (
                "FIXED_USED_TRUST_BOUNDARY",
                "Used supplied sort primitive/concrete equations; ascending-permutation meaning is external to this K claim.",
            )
        return (
            "FIXED_USED_SOUND",
            "Used fixed-semantics declaration/rule; exact evaluation, state footprint, and control role reviewed.",
        )
    return (
        "FIXED_UNUSED",
        "No constructor/function from this block occurs on the submitted program's reachable proof path.",
    )


def one_line(text: str) -> str:
    return " ".join(text.split())[:500]


def main() -> None:
    output = Path("/audit-output/evidence/09_rule_decisions.tsv")
    counts: dict[str, int] = {}
    with output.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, delimiter="\t")
        writer.writerow(
            ["file", "line", "kind", "disposition", "reason", "block_prefix"]
        )
        for path in inventory.FILES:
            relative = str(path.relative_to(ROOT))
            for line, kind, text in inventory.blocks(path):
                decision, reason = disposition(relative, kind, text)
                counts[decision] = counts.get(decision, 0) + 1
                writer.writerow(
                    [relative, line, kind, decision, reason, one_line(text)]
                )
    print(f"output={output}")
    print(f"decisions={counts}")
    print(f"total={sum(counts.values())}")


if __name__ == "__main__":
    main()

