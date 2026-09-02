#!/usr/bin/env python3
"""Emit an exhaustive source-level K declaration/rule inventory."""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
START = re.compile(r"^  (syntax|rule|context|configuration|claim|alias)\b")
COMMENT = re.compile(r"//.*$")


def compact(lines: list[str]) -> str:
    pieces: list[str] = []
    for line in lines:
        line = COMMENT.sub("", line).strip()
        if line:
            pieces.append(line)
    return re.sub(r"\s+", " ", " ".join(pieces)).strip()


def statements(path: Path):
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))
    for position, (start, kind) in enumerate(starts):
        stop = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        while stop > start and lines[stop - 1].strip() in {"", "endmodule"}:
            stop -= 1
        yield start + 1, kind, compact(lines[start:stop])


def classify(kind: str, statement: str) -> str:
    attrs = statement.lower()
    if kind == "syntax":
        if "no-evaluators" in attrs:
            return "opaque_function_declaration"
        if "[macro" in attrs:
            return "macro_declaration"
        if "function" in attrs:
            return "function_declaration"
        return "syntax_declaration"
    if kind == "rule":
        if "<k>" in statement or re.search(r"<[A-Za-z-]+>", statement):
            return "operational_rule"
        if "[macro" in attrs:
            return "macro_rule"
        return "equational_rule"
    return kind


def attribute_list(statement: str) -> str:
    wanted = [
        "function",
        "functional",
        "total",
        "no-evaluators",
        "concrete",
        "simplification",
        "priority",
        "owise",
        "macro-rec",
        "macro",
        "strict",
        "seqstrict",
        "symbol",
    ]
    found = [attribute for attribute in wanted if attribute in statement]
    return ",".join(found) if found else "-"


def materiality(relative: str, statement: str, origin: str) -> tuple[str, str]:
    if origin == "proof-local":
        return "material", "proof-local declaration/rule used by target claims"
    if origin == "specification":
        return "material", "positive target entry claim"

    material_patterns: dict[str, list[str]] = {
        "semantics/syntax.k": [
            r"syntax Expr",
            r"syntax CmpOp",
            r"syntax Exprs",
            r"syntax Stmt",
            r"syntax Stmts",
            r"syntax Params",
            r"syntax ParamNames",
        ],
        "semantics/core.k": [
            r"syntax Val\b",
            r"syntax Parent",
            r"syntax Scope",
            r"syntax KResult",
            r"syntax Expr\b",
            r"syntax Vals",
            r"syntax Exc",
            r"syntax RetState",
            r"configuration",
            r"Name\(",
            r"#look",
            r"builtinsScope",
            r"#evalArgs",
            r"#evalArgCont",
            r"#applyK",
            r"appendVal",
            r"truthy\(",
            r"boolAsInt",
            r"isArithOp",
            r"isEqOrdOp",
        ],
        "semantics/operators.k": [
            r"BinOp\(",
            r"Compare\(",
            r"applyBin",
            r"applyCmp",
        ],
        "semantics/int.k": [
            r'applyBin\("\+"',
            r'applyBin\("\*"',
            r'applyCmp\("=="',
        ],
        "semantics/bool.k": [
            r"BoolOp",
            r"truthy",
        ],
        "semantics/float.k": [
            r"syntax Val ::= Float",
            r"Float\(F:Float\)",
            r'applyCmp\("==", F1:Float, F2:Float\)',
            r"syntax Float ::= addF",
            r"rule addF",
            r'applyBin\("\+", F1:Float, F2:Float\)',
            r"syntax Float ::= mulF",
            r"rule mulF",
            r'applyBin\("\*", F1:Float, F2:Float\)',
            r"syntax Bool ::= eqF",
            r"rule eqF",
            r"eqIF",
            r"syntax Float ::= intToF",
            r"rule intToF",
            r'applyBin\("\+", I:Int, F:Float\)',
            r'applyBin\("\+", F:Float, I:Int\)',
            r'applyBin\("\*", I:Int, F:Float\)',
            r'applyBin\("\*", F:Float, I:Int\)',
            r'applyCmp\("==", I:Int, F:Float\)',
            r'applyCmp\("==", F:Float, I:Int\)',
        ],
        "semantics/functions.k": [
            r"frame\(",
            r"#bindP",
            r"Return\(",
            r"#endcall",
            r"#pop",
        ],
        "semantics/call.k": [
            r"#callee",
            r"Call\(",
            r"toCall\(closureVal",
        ],
    }
    for file_name, patterns in material_patterns.items():
        if relative == file_name and any(re.search(pattern, statement) for pattern in patterns):
            return "material", "construct or transition reachable from the target call"
    return "unused", "constructor-disjoint from the submitted loop-free numeric function"


def decision(
    origin: str,
    relative: str,
    kind: str,
    statement: str,
    material: str,
) -> str:
    if origin == "specification":
        return "ACCEPT_TARGET_CLAIM_AFTER_ADEQUACY_REVIEW"
    if origin == "proof-local":
        if "rightAngleTriangleClosure" in statement:
            return "ACCEPT_MECHANICALLY_PINNED_DEFINITION"
        if (
            "trustedFloatEq" in statement
            and "Compare(F1:Float" in statement
        ):
            return "ACCEPT_CONDITIONAL_EXTERNAL_FLOAT_EQUALITY_BRIDGE"
        if "trustedFloatEq" in statement:
            return "ACCEPT_CONDITIONAL_EXTERNAL_FLOAT_EQUALITY_PRIMITIVE"
        if "ratSquare" in statement or "ratAdd" in statement or "ratEq" in statement or "ratExpected" in statement:
            return "ACCEPT_SORT_DISJOINT_POSTCONDITION_DEFINITION"
        return "REVIEW_PROOF_LOCAL"
    if material == "material" and relative == "semantics/float.k" and (
        "eqIF(Int, Float)" in statement
        or "eqIF(I:Int, F:Float)" in statement
        or "intToF(Int)" in statement
        or "rule intToF" in statement
        or re.search(r'applyBin\("[+*]", (I:Int, F:Float|F:Float, I:Int)\)', statement)
    ):
        return "DOCUMENTED_SUPPLIED_MODEL_OVERFLOW_OR_NONFINITE_GAP"
    if kind in {"syntax", "context", "configuration"}:
        if material == "material":
            return "ACCEPT_FIXED_MODEL_DECLARATION_ON_MATERIAL_PATH"
        return "UNUSED_FIXED_MODEL_DECLARATION"
    if material == "unused":
        return "NOT_REACHED_BY_TARGET_ACCEPT_ONLY_AS_SUPPLIED_MODEL"
    if relative == "semantics/float.k" and any(
        name in statement
        for name in ("addF", "mulF", "intToF", "eqIF", "F1 ==Float F2")
    ):
        return "ACCEPT_NAMED_SUPPLIED_NUMERIC_PRIMITIVE_BOUNDARY"
    return "ACCEPT_FIXED_MODEL_RULE_ON_MATERIAL_PATH"


def main() -> None:
    files: list[tuple[str, Path, str]] = []
    semantics_root = ROOT / "reference-semantics"
    for path in sorted(semantics_root.rglob("*.k")):
        files.append(("supplied", path, path.relative_to(semantics_root).as_posix()))
    files.append(("proof-local", ROOT / "verification.k", "verification.k"))
    files.append(("specification", ROOT / "spec.k", "spec.k"))

    counts: collections.Counter[str] = collections.Counter()
    rows = []
    row_id = 0
    for origin, path, relative in files:
        for line, source_kind, statement in statements(path):
            row_id += 1
            category = classify(source_kind, statement)
            attrs = attribute_list(statement)
            material, reason = materiality(relative, statement, origin)
            verdict = decision(origin, relative, source_kind, statement, material)
            counts[f"origin:{origin}"] += 1
            counts[f"source_kind:{source_kind}"] += 1
            counts[f"category:{category}"] += 1
            counts[f"material:{material}"] += 1
            for attribute in attrs.split(","):
                if attribute != "-":
                    counts[f"attribute:{attribute}"] += 1
            rows.append(
                (
                    row_id,
                    origin,
                    relative,
                    line,
                    source_kind,
                    category,
                    attrs,
                    material,
                    verdict,
                    reason,
                    statement,
                )
            )

    print(
        "id\torigin\tfile\tline\tsource_kind\tcategory\tattributes\t"
        "target_path\tdecision\treason\tstatement"
    )
    for row in rows:
        print("\t".join(str(field).replace("\t", " ") for field in row))
    print(f"SUMMARY total_entries={len(rows)} counts={dict(sorted(counts.items()))}")


if __name__ == "__main__":
    main()
