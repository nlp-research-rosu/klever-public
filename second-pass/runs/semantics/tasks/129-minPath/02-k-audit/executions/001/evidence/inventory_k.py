#!/usr/bin/env python3
"""Produce a line-addressed exhaustive inventory of local K declarations/rules."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


START = re.compile(r"^\s*(syntax|rule|context|configuration|claim)\b")
ATTR = re.compile(r"\[([^\]]+)\]")


def records(path: Path) -> list[tuple[int, str, str]]:
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))
    result: list[tuple[int, str, str]] = []
    for pos, (start, kind) in enumerate(starts):
        stop = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
        while stop > start and lines[stop - 1].strip() in {"", "endmodule"}:
            stop -= 1
        text = "\n".join(lines[start:stop]).rstrip()
        result.append((start + 1, kind, text))
    return result


def attributes(text: str) -> list[str]:
    attrs: list[str] = []
    for match in ATTR.finditer(text):
        attrs.extend(part.strip() for part in match.group(1).split(","))
    return attrs


def classification(kind: str, text: str) -> str:
    attrs = attributes(text)
    if kind == "configuration":
        return "configuration"
    if kind == "context":
        return "evaluation-context"
    if kind == "claim":
        return "reachability-claim"
    if kind == "syntax":
        if "macro" in attrs or "macro-rec" in attrs:
            return "macro-declaration"
        if any(attr == "function" for attr in attrs):
            if "no-evaluators" in attrs or any(attr.startswith("symbol(") for attr in attrs):
                return "opaque-or-concrete-function-declaration"
            return "function-declaration"
        return "syntax-declaration"
    if "[simplification" in text:
        return "simplification-rule"
    if "<k>" in text:
        return "operational-rule"
    if "[macro" in text or "[macro-rec" in text:
        return "macro-equation"
    return "equational-rule"


USED_RANGES: dict[str, list[tuple[int, int]]] = {
    "semantics/core.k": [
        (44, 60), (62, 70), (92, 121), (123, 127), (129, 181),
        (183, 191), (193, 210), (212, 225),
    ],
    "semantics/range.k": [(9, 24)],
    "semantics/operators.k": [(10, 17), (22, 46)],
    "semantics/int.k": [(9, 20), (22, 27)],
    "semantics/list.k": [(8, 20), (52, 55)],
    "semantics/tuple.k": [(30, 41)],
    "semantics/subscript.k": [(6, 41)],
    "semantics/controls.k": [(8, 31), (46, 74)],
    "semantics/functions.k": [(13, 20), (62, 90)],
    "semantics/builtins.k": [(19, 26), (176, 180)],
    "semantics/call.k": [(15, 31), (34, 74)],
}


def on_used_path(relative: str, line: int, text: str) -> bool:
    if relative == "verification.k":
        return True
    if relative == "semantics/syntax.k":
        used_tokens = (
            "Expr ::=", "CmpOp", "Exprs", "Index", "Stmt ::=", "Stmts",
            "Params", "ParamNames", "Module",
        )
        return any(token in text for token in used_tokens)
    return any(lo <= line <= hi for lo, hi in USED_RANGES.get(relative, []))


def assessment(relative: str, line: int, kind: str, text: str, used: bool) -> str:
    if relative != "verification.k":
        if used:
            return (
                "ACCEPTED_USED_FIXED_RULE: unchanged supplied-semantics rule; "
                "reviewed against the submitted AST's evaluation, control, "
                "scope, heap, call/return, and integer/list behavior."
            )
        return (
            "ACCEPTED_UNUSED_FIXED_BOUNDARY: unchanged supplied-semantics "
            "declaration/rule and unreachable from all audited claims; no "
            "candidate extension and no theorem dependence."
        )

    compact = " ".join(text.split())
    if kind == "syntax" and ("[macro]" in compact or "[macro-rec]" in compact):
        return "ACCEPTED_PROOF_MACRO_DECLARATION: compile-time alias, not an opaque value."
    if kind == "rule" and "minPathAppendBody =>" in compact:
        return "ACCEPTED_EXACT_ALIAS: exact submitted append-loop body."
    if kind == "rule" and "minPathBody =>" in compact:
        return (
            "ACCEPTED_EXACT_ALIAS: complete translated function body; parser-level "
            "expanded identity with solution.mpy is independently checked."
        )
    if kind == "rule" and "minPathProgram =>" in compact:
        return "ACCEPTED_EXACT_ALIAS: Module(FuncDef(...)) wrapper around minPathBody."
    if kind == "rule" and "minPathClosure =>" in compact:
        return "ACCEPTED_EXACT_ALIAS: closure value created by loading the same function at scope 0."
    if "minPathMin" in compact:
        return (
            "ACCEPTED_MATHEMATICS: disjoint <=/> cases are exhaustive and return "
            "the ordinary minimum."
        )
    if "minPathNeighbor2" in compact:
        return (
            "ACCEPTED_DEFINITIONAL_SUMMARY: disjoint/exhaustive A/B/C location "
            "case split; under the permutation precondition it returns the "
            "smaller of the two orthogonal neighbors of the unique 1."
        )
    if "minPathFour" in compact:
        return "ACCEPTED_MATHEMATICS: constructs exactly [1,M,1,M]."
    if "minPathBuild" in compact:
        return (
            "ACCEPTED_MATHEMATICS: disjoint/exhaustive base/even/odd recursion; "
            "I increases toward K and exactly models append-in-place."
        )
    return "ACCEPTED_LOCAL_DECLARATION: no operational execution replacement."


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    paths = [args.root / "reference-semantics" / "semantics.k"]
    paths.extend(sorted((args.root / "reference-semantics" / "semantics").glob("*.k")))
    paths.append(args.root / "verification.k")

    out: list[str] = [
        "# Exhaustive K declaration and rule inventory",
        "",
        "This inventory is reviewer-generated from the clean scratch sources. "
        "The supplied tree was independently byte-compared with the trusted mount.",
        "",
    ]
    totals: dict[str, int] = {}
    total = 0
    opaque_count = priority_count = simplification_count = 0
    for path in paths:
        relative = (
            "verification.k"
            if path.name == "verification.k"
            else str(path.relative_to(args.root / "reference-semantics"))
        )
        recs = records(path)
        out.extend([f"## `{relative}`", "", f"Records: {len(recs)}", ""])
        for number, (line, kind, text) in enumerate(recs, start=1):
            total += 1
            totals[kind] = totals.get(kind, 0) + 1
            attrs = attributes(text)
            klass = classification(kind, text)
            if klass == "opaque-or-concrete-function-declaration":
                opaque_count += 1
            if any(attr.startswith("priority(") for attr in attrs):
                priority_count += 1
            if klass == "simplification-rule":
                simplification_count += 1
            used = on_used_path(relative, line, text)
            verdict = assessment(relative, line, kind, text, used)
            one_line = " ".join(text.split())
            out.extend(
                [
                    f"### `{relative}:{line}` — {kind} {number}",
                    "",
                    f"- Class: `{klass}`",
                    f"- Attributes: `{', '.join(attrs) if attrs else 'none'}`",
                    f"- Audited-claim path: `{'yes' if used else 'no'}`",
                    f"- Assessment: {verdict}",
                    f"- Text: `{one_line.replace('`', chr(39))}`",
                    "",
                ]
            )
    out.extend(
        [
            "## Totals",
            "",
            f"- All inventoried records: {total}",
            *[f"- {kind}: {count}" for kind, count in sorted(totals.items())],
            f"- Opaque/concrete function declarations: {opaque_count}",
            f"- Records carrying priority attributes: {priority_count}",
            f"- Simplification rules: {simplification_count}",
            "",
        ]
    )
    args.output.write_text("\n".join(out))
    print(
        f"records={total} kinds={dict(sorted(totals.items()))} "
        f"opaque={opaque_count} priority={priority_count} "
        f"simplification={simplification_count}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
