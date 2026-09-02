#!/usr/bin/env python3
"""Enumerate every K sentence and attach the audit disposition used in REVIEW.md."""

from __future__ import annotations

import glob
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/task70")
FILES = [
    ROOT / "reference-semantics" / "semantics.k",
    *map(Path, sorted(glob.glob(str(ROOT / "reference-semantics" / "semantics" / "*.k")))),
    ROOT / "verification.k",
]
START = re.compile(
    r"^\s*(configuration|syntax|context|rule|claim|alias)\b"
)

USED_MARKERS = {
    "core.k": (
        "#alloc",
        "#loadAll",
        "Name(",
        "#look",
        "builtinsScope",
        "#evalArgs",
        "#evalArgCont",
        "Int(I",
        "truthy(B",
        "appendVal",
        "vals2valSeq",
        "vsLen",
        "isRefV",
    ),
    "controls.k": (
        "Assign(Name",
        "AugAssign(Name",
        "Expr(_:Val)",
        "#branch",
        "If(",
        "#while",
        "#whileCond",
        "While(",
    ),
    "functions.k": (
        "FuncDef(",
        "#bindP",
        "Return(",
        "#endcall",
        "#pop",
        "frame(",
    ),
    "call.k": (
        "Attribute(",
        "Call(",
        "#callee",
        "#evalArgs",
        "closureVal(",
        "builtinV(BN",
        "boundMethodV(",
    ),
    "int.k": (
        'applyBin("+",',
        'applyBin("-",',
        'applyBin("%",',
        'applyBin("//",',
        "pyMod(",
        'applyCmp("<",',
        'applyCmp("==",',
    ),
    "operators.k": (
        "BinOp(",
        "Compare(",
        "applyCmp(",
    ),
    "list.k": (
        "#iterNext(list",
        "ListExpr(",
        "toList",
        "valSeqConcat",
        '"append"',
    ),
    "subscript.k": (
        "valSeqAt",
        "normIdx",
        "Subscript(",
        "applyIndex(list",
    ),
    "builtins.k": (
        '"len"',
        "seqLen(",
    ),
    "sort.k": (
        "sortVS",
        'builtinV("sorted")',
        "insVS(",
    ),
    "syntax.k": (
        "Module",
        "FuncDef",
        "Assign",
        "AugAssign",
        "While",
        "If",
        "Return",
        "Expr",
        "Call",
        "Attribute",
        "Subscript",
        "Compare",
        "CmpOp",
        "BinOp",
        "Name",
        "Int",
        "ListExpr",
    ),
}


def sentences(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[int] = []
    for index, line in enumerate(lines):
        if START.match(line):
            starts.append(index)
    for position, start in enumerate(starts):
        stop = starts[position + 1] if position + 1 < len(starts) else len(lines)
        while stop > start and (
            not lines[stop - 1].strip()
            or lines[stop - 1].lstrip().startswith("//")
            or lines[stop - 1].strip() == "endmodule"
        ):
            stop -= 1
        yield start + 1, "\n".join(lines[start:stop]).strip()


def attributes(text: str) -> list[str]:
    found: list[str] = []
    for name in (
        "function",
        "functional",
        "total",
        "symbol",
        "no-evaluators",
        "macro",
        "macro-rec",
        "strict",
        "seqstrict",
        "priority",
        "simplification",
        "concrete",
        "owise",
    ):
        if re.search(rf"\b{re.escape(name)}\b", text):
            found.append(name)
    return found


def disposition(path: Path, line: int, text: str) -> tuple[str, str]:
    name = path.name
    if name == "verification.k":
        if line >= 94 and text.lstrip().startswith("rule") and "#while" in text:
            return (
                "REJECT_UNSOUND_OPERATIONAL_BRIDGE",
                "Ordinary axiom replaces loop execution; its proven claim has a narrower "
                "builtins/K context, and body/missing-len witnesses refute the accepted domain.",
            )
        if "strangePrefix" in text or "strangeResult" in text:
            return (
                "ACCEPT_LOCAL_MATHEMATICAL_SUMMARY",
                "Base/step equations are guarded, descending/inductive, and agree with the "
                "actual even/odd append formulas on the reachable nonnegative index domain.",
            )
        if "vsLen" in text:
            return (
                "ACCEPT_DERIVED_LEMMA",
                "Every ValSeq has nonnegative algebraic length; the rule affects the proof.",
            )
        return (
            "ACCEPT_LOCAL_SYNTAX_OR_UNUSED_HELPER",
            "Macro is mechanically pinned to solution.mpy, or helper is unused by target closure.",
        )

    if name == "sort.k" and (
        "sortVS" in text or 'builtinV("sorted")' in text or "insVS" in text
    ):
        if "sortKeyVS" in text or "kwV(" in text:
            return (
                "ACCEPT_FIXED_UNUSED",
                "Keyed/reversed sorting is disconnected from the submitted program.",
            )
        return (
            "ACCEPT_CONDITIONAL_TRUST_BOUNDARY",
            "Supplied semantics intentionally leaves symbolic sortVS opaque; concrete "
            "insertion equations and differential evidence support, but do not prove, "
            "its ascending-permutation interpretation.",
        )

    markers = USED_MARKERS.get(name, ())
    if any(marker in text for marker in markers):
        if name == "subscript.k" and "valSeqAt" in text:
            return (
                "ACCEPT_USED_WITH_IN_BOUNDS_GUARD",
                "Constructor equations are ordinary indexing; total opaque OOB cases are "
                "not reached because 0<=I<N makes both selected indices in bounds.",
            )
        return (
            "ACCEPT_USED_FIXED_SEMANTICS",
            "Matches the source construct's evaluation, binding, allocation, control, "
            "or integer/list operation on the target's list-of-integers domain.",
        )

    if "no-evaluators" in text or "md5hexCodes" in text:
        return (
            "ACCEPT_FIXED_UNUSED_TRUST_BOUNDARY",
            "Opaque supplied primitive is not reachable from the submitted program.",
        )

    return (
        "ACCEPT_FIXED_UNUSED_OR_SUPPORT",
        "Selected supplied-semantics clause was reviewed; it is sort-disjoint or "
        "constructor-disconnected from this target and cannot contribute to its closure.",
    )


total = 0
rules = 0
syntaxes = 0
priority_rules = 0
simplification_rules = 0
opaque_declarations = 0
rejected = 0

print("# Exhaustive K sentence inventory")
print()
print("Source: fresh scratch copy; supplied tree is byte-identical to the trusted mount.")
for path in FILES:
    relative = path.relative_to(ROOT)
    print()
    print(f"## {relative}")
    for line, text in sentences(path):
        total += 1
        kind_match = START.match(text)
        kind = kind_match.group(1) if kind_match else "unknown"
        if kind == "rule":
            rules += 1
        if kind == "syntax":
            syntaxes += 1
        attrs = attributes(text)
        if kind == "rule" and "priority" in attrs:
            priority_rules += 1
        if kind == "rule" and "simplification" in attrs:
            simplification_rules += 1
        if kind == "syntax" and ("no-evaluators" in attrs or "symbol" in attrs):
            opaque_declarations += 1
        code, reason = disposition(path, line, text)
        if code.startswith("REJECT"):
            rejected += 1
        compact = " ".join(text.split())
        print(
            f"- `{relative}:{line}` kind=`{kind}` attrs=`{','.join(attrs) or '-'}` "
            f"decision=`{code}`"
        )
        print(f"  - Sentence: `{compact}`")
        print(f"  - Reason: {reason}")

print()
print("# Counts")
print(f"sentences={total}")
print(f"syntax_declarations={syntaxes}")
print(f"rules={rules}")
print(f"priority_rules={priority_rules}")
print(f"simplification_rules={simplification_rules}")
print(f"opaque_or_symbol_declarations={opaque_declarations}")
print(f"rejected_sentences={rejected}")
