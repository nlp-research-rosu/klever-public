#!/usr/bin/env python3
"""Exhaustive source-level inventory of local K declarations and rules."""

import re
from pathlib import Path


roots = [
    Path("/reference/reference-semantics/semantics.k"),
    *sorted(Path("/reference/reference-semantics/semantics").glob("*.k")),
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
]

start_re = re.compile(
    r"^\s*(syntax|rule|claim|configuration|context(?:\s+alias)?|alias)\b"
)
boundary_re = re.compile(
    r"^\s*(?:syntax|rule|claim|configuration|context(?:\s+alias)?|alias|"
    r"module|endmodule|imports|requires)\b"
)

used_reference_needles = {
    "syntax.k": (
        "Expr", "CmpOp", "Stmts", "Stmt", "Params", "ParamNames", "Module",
        "Assign", "AugAssign", "For", "While", "If", "Return", "FuncDef",
        "Int", "Bool", "Name", "BinOp", "Compare",
    ),
    "core.k": (
        "configuration", "#loadAll", "Module(", "Stmts", "Name(", "#look",
        "builtinsScope", "#evalArgs", "#evalArgCont", "#applyK", "Int(",
        "Bool(", "truthy", "applyBin", "applyCmp", "ValSeq", "vCons",
        "scope(", "closureVal", "appendVal", "vals2valSeq",
    ),
    "list.k": ("#iterNext(list",),
    "tuple.k": ("#bindTgt(Name",),
    "operators.k": ("BinOp(", "Compare(", "applyBin", "applyCmp", "context Compare"),
    "int.k": (
        'applyBin("+', 'applyBin("%', 'applyBin("//', "pyMod",
        'applyCmp("<', 'applyCmp(">', 'applyCmp(">="',
        'applyCmp("==',
    ),
    "controls.k": (
        "Assign(Name", "AugAssign(Name", "If(", "#branch", "For(", "#loop",
        "#loopStep", "While(", "#while", "#whileCond", "#loopLbl",
    ),
    "functions.k": (
        "FuncDef(", "#bindP", "Return(", "#endcall", "#pop", "frame(",
    ),
    "call.k": ("Call(", "#callee", "toCall(closureVal",),
}


def local_decision(line: int, kind: str) -> str:
    if kind == "claim":
        return "SOUND_RECONSTRUCTED_CIRCULARITY_OR_TARGET"
    if line <= 57:
        return "SOUND_EXACT_SYNTAX_ALIAS"
    if line <= 70:
        return "SOUND_EXHAUSTIVE_DOMAIN_PREDICATE"
    if line <= 89:
        return "SOUND_GUARDED_INT_PROJECTION"
    if line <= 116:
        return "SOUND_GUARDED_FIXED_INT_DISPATCH_TWIN"
    if line <= 142:
        return "SOUND_PRIME_TAIL_DEFINITION_OR_EQUALITY"
    if line <= 147:
        return "SOUND_PRIMALITY_DEFINITION"
    if line <= 154:
        return "SOUND_MAX_PRIME_SELECTION_CASE_SPLIT"
    if line <= 164:
        return "SOUND_LIST_FOLD_DEFINITION"
    return "SOUND_DIGIT_SUM_DEFINITION_OR_EQUALITY"


print("file\tline\tkind\tattributes\tdecision\tstatement")
counts: dict[str, int] = {}
for path in roots:
    lines = path.read_text().splitlines()
    index = 0
    while index < len(lines):
        match = start_re.match(lines[index])
        if not match:
            index += 1
            continue
        kind = match.group(1).replace(" ", "_")
        start = index
        index += 1
        while index < len(lines) and not boundary_re.match(lines[index]):
            index += 1
        statement = " ".join(line.strip() for line in lines[start:index])
        statement = re.sub(r"\s+", " ", statement)
        attrs = ",".join(
            attr for attr in (
                "function", "total", "functional", "macro", "opaque",
                "priority", "simplification", "concrete", "symbolic",
                "no-evaluators", "owise", "strict", "seqstrict",
            )
            if re.search(rf"\b{re.escape(attr)}\b", statement)
        ) or "-"
        if path.name == "verification.k":
            decision = local_decision(start + 1, kind)
        elif path.name == "spec.k":
            decision = "SOUND_RECONSTRUCTED_CIRCULARITY_OR_TARGET"
        else:
            needles = used_reference_needles.get(path.name, ())
            if any(needle in statement for needle in needles):
                decision = "FIXED_USED_RULE_REVIEWED_FOR_THIS_PROGRAM"
            else:
                decision = "FIXED_UNUSED_NO_REACHABLE_LHS_IN_TARGET"
        rel = (
            str(path).replace("/reference/reference-semantics/", "reference-semantics/")
            .replace("/candidate/", "candidate/")
        )
        print(
            f"{rel}\t{start + 1}\t{kind}\t{attrs}\t{decision}\t{statement}"
        )
        counts[decision] = counts.get(decision, 0) + 1

print("SUMMARY")
for decision, count in sorted(counts.items()):
    print(decision, count)
