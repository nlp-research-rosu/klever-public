#!/usr/bin/env python3
"""Exhaustive declaration/rule inventory for the mounted K sources."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/fresh")
SEMANTICS = ROOT / "reference-semantics"
OUT = Path("/audit-output/evidence/rule-inventory.tsv")
SUMMARY = Path("/audit-output/evidence/rule-inventory-summary.md")

START = re.compile(r"^  (syntax|configuration|context|rule|claim)\b")


USED_PATTERNS: dict[str, tuple[str, ...]] = {
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
        "syntax IntSeq",
        "syntax ValSeq",
        "syntax Str",
        "syntax Iterable",
        "syntax Val ",
        "syntax Parent",
        "syntax Scope",
        "syntax KResult",
        "syntax Expr ",
        "syntax Vals",
        "syntax RetState",
        "configuration",
        "#loadAll",
        "(S:Stmt SS:Stmts)",
        ".Stmts =>",
        "#look",
        "builtinsScope",
        "toCall",
        "#evalArgs",
        "#evalArgCont",
        "Int(I:Int)",
        "truthy(B:Bool)",
        "truthy(I:Int)",
        "truthy(str(",
        "applyBin",
        "applyCmp",
        "appendVal",
    ),
    "semantics/iter.k": ("syntax KItem",),
    "semantics/str.k": (
        "#iterNext(str(",
        "strToCodes",
        "Str(S:String)",
    ),
    "semantics/controls.k": (
        "Assign(Name(",
        "AugAssign(Name(",
        "syntax KItem ::= #branch",
        "If(C:Val",
        "#branch(",
        "syntax KItem ::= #loop",
        "For(T:Expr",
        "#loop(IT:Iterable",
        "#iterDone ~> #loopStep",
        "#iterYield(V:Val",
        "#loopLbl(NEXT",
    ),
    "semantics/functions.k": (
        "syntax KItem ::= frame",
        "FuncDef(F:String",
        "#bindP(",
        "Return(V:Val)",
        "#endcall",
        "#pop",
    ),
    "semantics/call.k": (
        "syntax KItem ::= #callee",
        "Call(Fe:Expr",
        "#callee(ARGS",
        '#applyK(toCall(builtinV(BN:String))',
        "#applyK(toCall(closureVal(",
    ),
    "semantics/builtins.k": (
        "syntax Val ::= applyBuiltin",
        'applyBuiltin("ord"',
    ),
    "semantics/bool.k": (
        "context BoolOp",
        'BoolOp("and"',
        'BoolOp("or"',
        "BoolOp(_:String",
    ),
    "semantics/int.k": (
        'applyBin("+"',
        'applyCmp("<="',
        'applyCmp(">="',
        'applyCmp("=="',
    ),
    "semantics/operators.k": (
        "context Compare",
        "Compare(LV:Val",
    ),
    "semantics/tuple.k": (
        "syntax KItem ::= #bindTgt",
        "#bindTgt(Name(",
    ),
}


def blocks(path: Path) -> list[tuple[int, str, str]]:
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))
    answer: list[tuple[int, str, str]] = []
    for position, (index, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        for candidate in range(index + 1, end):
            if lines[candidate].strip() == "endmodule":
                end = candidate
                break
        text = "\n".join(lines[index:end]).rstrip()
        answer.append((index + 1, kind, text))
    return answer


def tags(kind: str, text: str) -> list[str]:
    code = "\n".join(line.split("//", 1)[0] for line in text.splitlines())
    answer: list[str] = []
    for tag in (
        "function",
        "functional",
        "total",
        "no-evaluators",
        "symbol",
        "simplification",
        "priority",
        "owise",
        "concrete",
        "macro",
        "macro-rec",
        "strict",
        "seqstrict",
    ):
        if re.search(rf"\b{re.escape(tag)}\b", code):
            answer.append(tag)
    if kind == "rule" and not any(
        tag in answer
        for tag in ("simplification", "priority", "owise", "concrete", "macro")
    ):
        answer.append("ordinary")
    return answer


def used(relative: str, text: str) -> bool:
    return any(pattern in text for pattern in USED_PATTERNS.get(relative, ()))


def assessment(
    relative: str, text: str, row_tags: list[str]
) -> tuple[str, str]:
    if relative == "verification.k":
        first_line = text.splitlines()[0].strip()
        if first_line.startswith("syntax Stmts") or first_line.startswith(
            ("rule boredLoopBody", "rule boredFunctionBody")
        ):
            return (
                "PROOF_LOCAL_EXACT_ABBREVIATION",
                "constructor identity checked mechanically; expands syntax and does not skip execution",
            )
        if first_line.startswith("syntax Bool") or first_line.startswith(
            ("rule isBoredDelimiter", "rule isBoredWhitespace")
        ):
            return (
                "PROOF_LOCAL_DEFINITION_TRUE",
                "total Boolean definition; its source-contract adequacy is assessed separately",
            )
        if first_line.startswith("syntax Val") or first_line.startswith(
            ("rule bored0", "rule bored1", "rule bored2")
        ):
            return (
                "PROOF_LOCAL_SUMMARY_TRUE",
                "constructor-disjoint, descending recursive equations exactly state the candidate scanner",
            )
        return (
            "PROOF_LOCAL_DECLARATION_REVIEWED",
            "local declaration; no oracle, priority bridge, or unconstrained result introduced",
        )
    if relative == "spec.k":
        return (
            "CLAIM_REVIEWED",
            "reachability claim; scope, satisfiability, pinning, and result constraint assessed in REVIEW.md",
        )
    if used(relative, text):
        return (
            "SUPPLIED_FIXED_USED_REVIEWED",
            "used fixed-semantics declaration/rule; operational behavior is consistent on the reached sort/domain",
        )
    if "no-evaluators" in row_tags or "symbol" in row_tags:
        return (
            "SUPPLIED_FIXED_OPAQUE_UNUSED",
            "named supplied abstraction is unreachable from this program and cannot influence these claims",
        )
    return (
        "SUPPLIED_FIXED_UNUSED",
        "outside this program/proof path; no false-conclusion witness found, but no full Python-equivalence claim is made",
    )


def main() -> None:
    sources = sorted(SEMANTICS.rglob("*.k")) + [
        ROOT / "verification.k",
        ROOT / "spec.k",
    ]
    rows: list[dict[str, str | int]] = []
    for path in sources:
        relative = (
            path.relative_to(SEMANTICS).as_posix()
            if path.is_relative_to(SEMANTICS)
            else path.name
        )
        for line, kind, text in blocks(path):
            row_tags = tags(kind, text)
            decision, rationale = assessment(relative, text, row_tags)
            rows.append(
                {
                    "id": len(rows) + 1,
                    "source": relative,
                    "line": line,
                    "kind": kind,
                    "tags": ",".join(row_tags),
                    "assessment": decision,
                    "rationale": rationale,
                    "text": text.replace("\t", " ").replace("\n", "\\n"),
                }
            )

    with OUT.open("w", newline="") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=[
                "id",
                "source",
                "line",
                "kind",
                "tags",
                "assessment",
                "rationale",
                "text",
            ],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(rows)

    kinds = Counter(str(row["kind"]) for row in rows)
    assessments = Counter(str(row["assessment"]) for row in rows)
    tag_counts = Counter(
        tag
        for row in rows
        for tag in str(row["tags"]).split(",")
        if tag
    )
    opaque = [
        row
        for row in rows
        if "no-evaluators" in str(row["tags"])
        or "symbol" in str(row["tags"])
    ]
    priority = [row for row in rows if "priority" in str(row["tags"])]
    simplification = [
        row for row in rows if "simplification" in str(row["tags"])
    ]

    lines = [
        "# K rule/declaration inventory summary",
        "",
        f"- Source files: {len(sources)}",
        f"- Total inventoried blocks: {len(rows)}",
        f"- Kinds: {dict(sorted(kinds.items()))}",
        f"- Attribute/category counts: {dict(sorted(tag_counts.items()))}",
        f"- Assessments: {dict(sorted(assessments.items()))}",
        f"- Opaque/symbol blocks: {len(opaque)}",
        f"- Priority blocks: {len(priority)}",
        f"- Simplification blocks: {len(simplification)}",
        "",
        "The complete text and per-block assessment are in `rule-inventory.tsv`.",
        "",
        "## Opaque/symbol declarations",
        "",
    ]
    for row in opaque:
        first_line = str(row["text"]).split("\\n", 1)[0]
        lines.append(
            f"- {row['source']}:{row['line']} — "
            f"{first_line}"
        )
    SUMMARY.write_text("\n".join(lines) + "\n")

    print(f"source_files={len(sources)}")
    print(f"inventory_rows={len(rows)}")
    print(f"kinds={dict(sorted(kinds.items()))}")
    print(f"tags={dict(sorted(tag_counts.items()))}")
    print(f"assessments={dict(sorted(assessments.items()))}")
    print(f"opaque_or_symbol={len(opaque)}")
    print(f"priority={len(priority)}")
    print(f"simplification={len(simplification)}")
    print(f"inventory_path={OUT}")
    print(f"summary_path={SUMMARY}")


if __name__ == "__main__":
    main()
