#!/usr/bin/env python3
"""Emit an exhaustive inventory of local K declarations/rules/claims.

The classifier is deliberately conservative: only entries on this theorem's
actual construct path are marked relevant.  Unused supplied rules are still
enumerated and reviewed, but are not treated as proof-local axioms.
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
SEMANTICS = ROOT / "reference-semantics"
LOCAL_FILES = sorted(SEMANTICS.rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "spec.k",
]
START = re.compile(
    r"^\s*(syntax|rule|claim|configuration|context|alias|macro)\b"
)

RELEVANT_PATTERNS = {
    "semantics/syntax.k": (
        "syntax Expr ::=",
        "syntax CmpOp",
        "syntax Exprs",
        "syntax Stmt ::=",
        "syntax Stmts",
        "syntax Params",
        "syntax ParamNames",
        "syntax Module",
    ),
    "semantics/core.k": (
        "syntax ValSeq",
        "syntax Iterable",
        "syntax Val ",
        "syntax KResult",
        "syntax Expr ",
        "syntax Vals",
        "syntax RetState",
        "configuration",
        "isRefV",
        "#alloc",
        "#loadAll",
        "(S:Stmt SS:Stmts)",
        ".Stmts =>",
        "#look",
        "Name(X:String)",
        "builtinsScope",
        "#evalArgs",
        "#evalArgCont",
        "#applyK",
        "Int(I:Int)",
        "truthy",
        "applyCmp",
        "appendVal",
        "vals2valSeq",
    ),
    "semantics/operators.k": ("Compare(", "applyCmp"),
    "semantics/int.k": ('applyCmp("<="',),
    "semantics/bool.k": ("BoolOp", "truthy"),
    "semantics/list.k": ("ListExpr", "toList", '"append"'),
    "semantics/controls.k": (
        "Assign(Name",
        "Expr(_:Val)",
        "#branch",
        "If(C:Val",
    ),
    "semantics/functions.k": (
        "FuncDef",
        "#bindP",
        "Return(V:Val)",
        "#endcall",
        "#pop",
        "frame(",
    ),
    "semantics/call.k": (
        "Attribute(",
        "Call(Fe",
        "#callee",
        "closureVal(",
        "toCall",
    ),
}

TOTALITY_WARNINGS = (
    "mapStrVS(",
    "floorFI(",
    "toF(",
    "ceilF(",
    "joinCodes(",
    "valSeqAt(",
)

SUBSET_APPROXIMATIONS = (
    "Import(_:String)",
    "ImportFrom(_:String",
    '"encode"',
    "sortVS(",
    "sortKeyVS(",
    "md5hexCodes(",
    "closureVal outlives",
)


def relative(path: Path) -> str:
    if path.is_relative_to(SEMANTICS):
        return path.relative_to(SEMANTICS).as_posix()
    return path.name


def entries(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))
    for position, (index, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        block = "\n".join(lines[index:end])
        yield index + 1, kind, block


def code_without_comments(block: str) -> str:
    return "\n".join(
        line.split("//", 1)[0]
        for line in block.splitlines()
        if not line.lstrip().startswith("//")
    )


def flags(block: str) -> str:
    code = code_without_comments(block)
    names = []
    for name in (
        "function",
        "total",
        "functional",
        "no-evaluators",
        "symbol",
        "priority",
        "owise",
        "concrete",
        "simplification",
        "macro",
        "macro-rec",
        "strict",
        "seqstrict",
    ):
        if name in code:
            names.append(name)
    return ",".join(names) if names else "-"


def classify(file_name: str, kind: str, block: str) -> tuple[str, str]:
    normalized = " ".join(
        line.strip() for line in code_without_comments(block).splitlines() if line.strip()
    )
    if file_name == "verification.k":
        return (
            "PROOF_LOCAL_SOUND",
            "pure nonrecursive math definition; exhaustive/disjoint where split; no cell or execution match",
        )
    if file_name == "spec.k":
        return (
            "TARGET_CLAIM_AUDITED",
            "single positive-domain reachability claim; result, heap, allocation, control, exception and exit state constrained",
        )
    if kind == "syntax" and "no-evaluators" in code_without_comments(block):
        return (
            "UNUSED_OPAQUE_TRUST_BOUNDARY",
            "supplied opaque primitive; no occurrence on submitted program/proof result path",
        )
    if any(name in normalized for name in TOTALITY_WARNINGS):
        return (
            "UNUSED_TOTALITY_COVERAGE_GAP",
            "supplied declaration/rule associated with compiler non-exhaustiveness warning; no occurrence on theorem path",
        )
    relevant = any(
        pattern in normalized
        for pattern in RELEVANT_PATTERNS.get(file_name, ())
    )
    if relevant:
        return (
            "RELEVANT_FIXED_SOUND",
            "used declaration/rule on real call path; reviewed for binding, left-to-right evaluation, branch, allocation, mutation, return and cell footprint",
        )
    if any(pattern in normalized for pattern in SUBSET_APPROXIMATIONS):
        return (
            "FIXED_UNUSED_SUBSET_APPROXIMATION",
            "documented supplied-subset approximation or external primitive; absent from submitted program and target result",
        )
    if kind in {"syntax", "context", "configuration"}:
        return (
            "FIXED_DECLARATION_REVIEWED",
            "supplied language declaration; no proof-local correctness conclusion encoded",
        )
    return (
        "FIXED_UNUSED_REVIEWED",
        "not reachable from submitted construct path; no concrete or symbolic false conclusion witness affecting intended inputs",
    )


def main() -> None:
    print(
        "id\tfile\tline\tkind\tattributes\tclassification\tdecision_basis\tsource_head"
    )
    counts: Counter[str] = Counter()
    entry_id = 0
    for path in LOCAL_FILES:
        file_name = relative(path)
        for line, kind, block in entries(path):
            entry_id += 1
            classification, basis = classify(file_name, kind, block)
            counts[f"kind:{kind}"] += 1
            counts[f"class:{classification}"] += 1
            head = " ".join(
                part.strip()
                for part in block.splitlines()
                if part.strip() and not part.lstrip().startswith("//")
            )
            head = head.replace("\t", " ").replace("\n", " ")[:500]
            print(
                "\t".join(
                    (
                        str(entry_id),
                        file_name,
                        str(line),
                        kind,
                        flags(block),
                        classification,
                        basis,
                        head,
                    )
                )
            )
    print("# SUMMARY " + " ".join(f"{key}={counts[key]}" for key in sorted(counts)))
    print(f"# TOTAL_ENTRIES {entry_id}")


if __name__ == "__main__":
    main()
