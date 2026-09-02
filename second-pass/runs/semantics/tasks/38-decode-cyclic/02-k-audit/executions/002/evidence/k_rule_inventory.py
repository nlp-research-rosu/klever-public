#!/usr/bin/env python3
"""Exhaustive top-level K declaration/rule inventory with theorem-slice tags."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


SEM_ROOT = Path("/tmp/audit-work/38-decode-cyclic/reference-semantics")
SCRATCH = Path("/tmp/audit-work/38-decode-cyclic")
OUTPUT = Path("/audit-output/evidence/k-rule-inventory.md")


def source_files() -> list[Path]:
    return (
        [SEM_ROOT / "semantics.k"]
        + sorted((SEM_ROOT / "semantics").glob("*.k"))
        + [SCRATCH / "verification.k", SCRATCH / "spec.k"]
    )


START = re.compile(r"^  (syntax|configuration|context|rule|claim|macro|priority)\b")


def declarations(path: Path) -> list[tuple[int, str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))
    result: list[tuple[int, str, str]] = []
    for pos, (start, kind) in enumerate(starts):
        end = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
        while end > start and lines[end - 1].strip() in {"", "endmodule"}:
            end -= 1
        block = "\n".join(lines[start:end]).strip()
        result.append((start + 1, kind, block))
    return result


def classify(kind: str, block: str) -> str:
    attrs: list[str] = []
    for attr in [
        "macro",
        "function",
        "total",
        "functional",
        "simplification",
        "priority",
        "concrete",
        "owise",
        "symbol",
        "no-evaluators",
        "strict",
        "seqstrict",
    ]:
        if re.search(rf"\b{re.escape(attr)}\b", block):
            attrs.append(attr)
    if kind == "rule":
        if "simplification" in attrs:
            base = "simplification rule"
        elif "priority" in attrs:
            base = "priority semantic rule"
        elif "concrete" in attrs:
            base = "concrete-only equation"
        elif "macro" in attrs:
            base = "macro expansion rule"
        else:
            base = "ordinary rule/equation"
    elif kind == "syntax" and "no-evaluators" in attrs:
        base = "opaque symbol declaration"
    else:
        base = f"{kind} declaration"
    return base + (f"; attrs={','.join(attrs)}" if attrs else "")


# This is the transitive fixed-semantics slice reached by decodeBody and by
# concrete module loading. A block tagged "fixed/outside slice" is still
# inventoried; it cannot contribute to the target proof because no used
# constructor/control term routes to it.
RELEVANT_PATTERNS: dict[str, tuple[str, ...]] = {
    "semantics.k": ("module MPY",),
    "syntax.k": (
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
    "core.k": (
        "syntax IntSeq",
        "syntax Str",
        "syntax Val ",
        "syntax Parent",
        "syntax Scope",
        "syntax KResult",
        "syntax Expr ",
        "syntax Vals",
        "syntax Exc",
        "syntax RetState",
        "configuration",
        "#loadAll",
        "(S:Stmt SS:Stmts)",
        ".Stmts",
        "#look",
        "builtinsScope",
        "#evalArgs",
        "#evalArgCont",
        "#applyK",
        "Int(I:Int)",
        "truthy",
        "applyBin",
        "applyCmp",
        "appendVal",
        "isLen",
    ),
    "int.k": ("applyCmp(\"<\"",),
    "operators.k": ("BinOp", "Compare",),
    "str.k": (
        "strToCodes",
        "seqConcat",
        "applyBin(\"+\"",
    ),
    "subscript.k": (
        "intSeqAt",
        "normIdx",
        "Subscript",
        "#evalB",
        "#toSome",
        "#slLo",
        "#slHi",
        "#slStep",
        "doSlice",
        "slStep",
        "slStart",
        "slStop",
        "slAdjust",
        "clampLo",
        "clampHi",
        "buildIS",
    ),
    "controls.k": ("Expr(_:Val)", "#branch", "If(C:Val",),
    "functions.k": (
        "frame(",
        "#bindP",
        "#pop",
        "#endcall",
        "Return(V:Val)",
    ),
    "builtins.k": ("applyBuiltin", "seqLen",),
    "call.k": (
        "#callee",
        "#applyK(toCall(builtinV",
        "#applyK(toCall(closureVal",
    ),
}


def theorem_slice(path: Path, block: str) -> str:
    if path.name in {"verification.k", "spec.k"}:
        return "proof-local/claim"
    patterns = RELEVANT_PATTERNS.get(path.name, ())
    if any(pattern in block for pattern in patterns):
        return "fixed/used theorem slice"
    return "fixed/outside theorem slice"


def one_line(block: str) -> str:
    compact = re.sub(r"\s+", " ", block)
    compact = compact.replace("|", "\\|")
    return compact if len(compact) <= 220 else compact[:217] + "..."


def main() -> None:
    rows: list[tuple[str, int, str, str, str, str]] = []
    for path in source_files():
        relative = (
            path.relative_to(SEM_ROOT).as_posix()
            if path.is_relative_to(SEM_ROOT)
            else path.name
        )
        for line, kind, block in declarations(path):
            rows.append(
                (
                    relative,
                    line,
                    kind,
                    classify(kind, block),
                    theorem_slice(path, block),
                    one_line(block),
                )
            )

    kind_counts = Counter(row[2] for row in rows)
    class_counts = Counter(row[3].split(";")[0] for row in rows)
    slice_counts = Counter(row[4] for row in rows)
    output: list[str] = [
        "# Exhaustive K declaration and rule inventory",
        "",
        "Generated from the independently copied, integrity-checked supplied "
        "semantics plus the submitted `verification.k` and `spec.k`.",
        "",
        f"- Source files: {len(source_files())}",
        f"- Inventory entries: {len(rows)}",
        f"- Kinds: `{dict(sorted(kind_counts.items()))}`",
        f"- Classes: `{dict(sorted(class_counts.items()))}`",
        f"- Slice tags: `{dict(sorted(slice_counts.items()))}`",
        "",
        "| # | Source | Line | Kind/class | Slice | Declaration or rule |",
        "|---:|---|---:|---|---|---|",
    ]
    for index, (source, line, _kind, klass, slice_tag, summary) in enumerate(rows, 1):
        output.append(
            f"| {index} | `{source}` | {line} | {klass} | {slice_tag} | "
            f"`{summary}` |"
        )
    OUTPUT.write_text("\n".join(output) + "\n", encoding="utf-8")
    print(f"wrote={OUTPUT}")
    print(f"entries={len(rows)}")
    print(f"kinds={dict(sorted(kind_counts.items()))}")
    print(f"classes={dict(sorted(class_counts.items()))}")
    print(f"slice_tags={dict(sorted(slice_counts.items()))}")


if __name__ == "__main__":
    main()
