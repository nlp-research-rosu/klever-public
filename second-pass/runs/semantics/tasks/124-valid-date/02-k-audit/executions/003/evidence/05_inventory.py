#!/usr/bin/env python3
"""Build an exhaustive source-level K declaration/rule inventory."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


WORK = Path("/tmp/audit-work/124-valid-date")
OUT = Path("/audit-output/evidence/05_rule_inventory.tsv")

sources = sorted((WORK / "reference-semantics").rglob("*.k"))
sources += [WORK / "verification.k", WORK / "spec.k"]

start_re = re.compile(
    r"^  (?P<kind>configuration|syntax|rule|claim|context(?: alias)?)\b"
)

material_symbols = {
    "semantics/syntax.k": [
        "syntax Expr",
        "syntax CmpOp",
        "syntax Exprs",
        "syntax Stmt",
        "syntax Stmts",
        "syntax Params",
        "syntax ParamNames",
        "syntax Module",
    ],
    "semantics/core.k": [
        "syntax IntSeq",
        "syntax Str",
        "syntax Val ",
        "syntax KResult",
        "syntax Expr ",
        "syntax Vals",
        "syntax Exc",
        "syntax RetState",
        "configuration",
        "#loadAll",
        "(S:Stmt SS:Stmts)",
        ".Stmts =>",
        "Name(X:String)",
        "#look(",
        "builtinsScope",
        "#evalArgs",
        "#evalArgCont",
        "#applyK(ApplyK",
        "Int(I:Int)",
        "Bool(B:Bool)",
        "truthy(B:Bool)",
        "applyBin(String",
        "applyCmp(String",
        "appendVal",
        "isLen",
    ],
    "semantics/controls.k": [
        "Assign(Name",
        "syntax KItem ::= #branch",
        "If(C:Val",
        "#branch(true",
        "#branch(false",
    ],
    "semantics/functions.k": [
        "FuncDef(F:String, Params",
        "#bindP(.ParamNames",
        "#bindP((P:String",
        "Return(V:Val)",
        "#endcall",
        "#pop =>",
    ],
    "semantics/call.k": [
        "Call(Fe:Expr",
        "#callee(",
        "#applyK(toCall(builtinV(BN:String))",
        "#applyK(toCall(closureVal(",
    ],
    "semantics/builtins.k": [
        "syntax Val ::= applyBuiltin",
        'applyBuiltin("len"',
        "seqLen(str",
        'applyBuiltin("ord"',
    ],
    "semantics/subscript.k": [
        "intSeqAt",
        "normIdx",
        "context Subscript",
        "Subscript(OBJ:Val, I:Int)",
        "syntax Val ::= applyIndex",
        "applyIndex(str",
    ],
    "semantics/operators.k": [
        "BinOp(OP:String",
        "context Compare",
        "Compare(LV:Val",
    ],
    "semantics/int.k": [
        'applyBin("+"',
        'applyBin("-"',
        'applyBin("*"',
        'applyCmp("<"',
        'applyCmp("<="',
        'applyCmp(">"',
        'applyCmp("=="',
        'applyCmp("!="',
    ],
    "semantics/bool.k": [
        "context BoolOp",
        'BoolOp("or"',
        "BoolOp(_:String",
    ],
}


def rel_name(path: Path) -> str:
    if path == WORK / "verification.k":
        return "verification.k"
    if path == WORK / "spec.k":
        return "spec.k"
    return path.relative_to(WORK / "reference-semantics").as_posix()


def compact(block: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"//[^\n]*", "", block)).strip()


rows: list[dict[str, str]] = []
for path in sources:
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = start_re.match(line)
        if match:
            starts.append((index, match.group("kind")))
    for pos, (start, kind) in enumerate(starts):
        end = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
        for candidate_end in range(start + 1, end):
            if lines[candidate_end].startswith("endmodule"):
                end = candidate_end
                break
        block = "\n".join(lines[start:end]).rstrip()
        item = compact(block)
        attributes = ",".join(
            part.strip()
            for group in re.findall(r"\[([^\]]+)\]", block)
            for part in group.split(",")
        )
        flags: list[str] = []
        if "function" in attributes.split(","):
            flags.append("function")
        if "total" in attributes.split(","):
            flags.append("total")
        if "functional" in attributes.split(","):
            flags.append("functional")
        if "no-evaluators" in attributes.split(","):
            flags.append("opaque")
        if "priority(" in block:
            flags.append("priority")
        if "simplification" in attributes.split(","):
            flags.append("simplification")
        if "[concrete]" in block:
            flags.append("concrete")
        if "[owise]" in block:
            flags.append("owise")
        if "[macro" in block:
            flags.append("macro")

        if kind == "rule":
            rule_class = "operational" if "<k>" in block else "equational"
            if "simplification" in flags:
                rule_class = "simplification"
        elif kind == "syntax":
            rule_class = "declaration"
        elif kind.startswith("context"):
            rule_class = "evaluation-context"
        elif kind == "claim":
            rule_class = "reachability-claim"
        else:
            rule_class = "configuration"

        rel = rel_name(path)
        if rel in {"verification.k", "spec.k"}:
            material = "yes"
        else:
            material = (
                "yes"
                if any(symbol in block for symbol in material_symbols.get(rel, []))
                else "no"
            )

        if rel == "verification.k":
            if any(
                name in block
                for name in ("validDateBody", "validDateClosure", "validDateModule")
            ):
                assessment = "SOUND_EXACT_DEFINITIONAL_PROGRAM_TERM"
            else:
                assessment = "SOUND_TOTAL_MATHEMATICAL_SUMMARY"
        elif rel == "spec.k":
            assessment = "TARGET_RESULT_CONSTRAINING_CLAIM"
        elif material == "yes":
            assessment = "ACCEPT_MATERIAL_FIXED_SEMANTICS_RULE"
        elif "opaque" in flags:
            assessment = "UNUSED_OPAQUE_FIXED_TRUST_BOUNDARY"
        else:
            assessment = "REVIEWED_UNUSED_FIXED_SEMANTICS_ITEM"

        if rel == "semantics/builtins.k" and (
            'applyBuiltin("int", str(CS:IntSeq)' in block
            or "intDigAcc(iCons" in block
        ):
            assessment = "UNUSED_PYTHON_FIDELITY_GAP_INT_STRING"
        if rel == "semantics/controls.k" and (
            'ImportFrom(_:String' in block
            or "#bindImports((N:String" in block
        ):
            assessment = "UNUSED_SUBSET_IMPORT_APPROXIMATION"
        if rel == "semantics/float.k" and "Import(_:String)" in block:
            assessment = "UNUSED_SUBSET_IMPORT_APPROXIMATION"

        rows.append(
            {
                "id": str(len(rows) + 1),
                "path": rel,
                "start": str(start + 1),
                "end": str(end),
                "kind": kind,
                "class": rule_class,
                "flags": ",".join(flags),
                "material": material,
                "assessment": assessment,
                "text": item,
            }
        )

columns = [
    "id",
    "path",
    "start",
    "end",
    "kind",
    "class",
    "flags",
    "material",
    "assessment",
    "text",
]
with OUT.open("w") as stream:
    stream.write("\t".join(columns) + "\n")
    for row in rows:
        stream.write("\t".join(row[column].replace("\t", " ") for column in columns) + "\n")

kind_counts = Counter(row["kind"] for row in rows)
class_counts = Counter(row["class"] for row in rows)
flag_counts = Counter(
    flag for row in rows for flag in row["flags"].split(",") if flag
)
assessment_counts = Counter(row["assessment"] for row in rows)
path_counts = Counter(row["path"] for row in rows)
print(f"source_count={len(sources)}")
print(f"inventory_item_count={len(rows)}")
print(f"kind_counts={dict(sorted(kind_counts.items()))}")
print(f"class_counts={dict(sorted(class_counts.items()))}")
print(f"flag_counts={dict(sorted(flag_counts.items()))}")
print(f"assessment_counts={dict(sorted(assessment_counts.items()))}")
print("path_counts:")
for path, count in sorted(path_counts.items()):
    print(f"  {path}={count}")
print("candidate_verification_inventory:")
for row in rows:
    if row["path"] in {"verification.k", "spec.k"}:
        print(
            f"  id={row['id']} path={row['path']} lines={row['start']}-{row['end']} "
            f"kind={row['kind']} class={row['class']} flags={row['flags']} "
            f"assessment={row['assessment']} text={row['text'][:240]}"
        )
print("RULE_INVENTORY=COMPLETE")
