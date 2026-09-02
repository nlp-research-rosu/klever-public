#!/usr/bin/env python3
"""Build a source-derived inventory of every K declaration/rule in the audit scope."""

from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


START = re.compile(r"^\s*(configuration|syntax|rule|context|claim|alias)\b")
COMMENT = re.compile(r"//.*$")


@dataclass
class Item:
    path: Path
    line: int
    kind: str
    body: str


def logical_items(path: Path) -> list[Item]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))
    items = []
    for position, (start, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        body_lines = []
        for line in lines[start:end]:
            stripped = COMMENT.sub("", line).strip()
            if stripped in {"", "endmodule"} or stripped.startswith("module ") or stripped.startswith("imports "):
                continue
            body_lines.append(stripped)
        body = " ".join(body_lines)
        body = re.sub(r"\s+", " ", body).strip()
        items.append(Item(path, start + 1, kind, body))
    return items


def attributes(item: Item) -> list[str]:
    attrs = []
    for label, pattern in (
        ("function", r"\bfunction\b"),
        ("total", r"\btotal\b"),
        ("functional", r"\bfunctional\b"),
        ("opaque/no-evaluators", r"\bno-evaluators\b"),
        ("symbol", r"\bsymbol\s*\("),
        ("priority", r"\bpriority\s*\("),
        ("owise", r"\bowise\b"),
        ("concrete", r"\bconcrete\b"),
        ("macro", r"\bmacro(?:-rec)?\b"),
        ("strict", r"\b(?:seqstrict|strict)\s*(?:\(|\])"),
        ("simplification", r"\bsimplification\b"),
    ):
        if re.search(pattern, item.body):
            attrs.append(label)
    return attrs


REACHED_PATTERNS: dict[str, tuple[str, ...]] = {
    "semantics/syntax.k": (
        "Int\"", "Float\"", "Bool\"", "Name\"", "BinOp\"", "Call\"", "Compare\"",
        "CmpOp", "Assign\"", "ImportFrom\"", "AugAssign\"", "For\"", "If\"", "Return\"",
        "FuncDef\"", "Stmts", "Params", "ParamNames", "Module",
    ),
    "semantics/core.k": (
        "configuration", "syntax Val ", "syntax KResult", "syntax Expr ::= Val", "builtinsScope",
        "#loadAll(Module", "(S:Stmt SS:Stmts)", ".Stmts =>", "Name(X:String) => #look",
        "#look(X:String", "#evalArgs", "#evalArgCont", "#applyK", "Int(I:Int)", "Bool(B:Bool)",
        "truthy(B:Bool)", "appendVal",
    ),
    "semantics/functions.k": (
        "FuncDef(F:String, Params", "#bindP(.ParamNames", "#bindP((P:String", "Return(V:Val)", "#pop",
    ),
    "semantics/call.k": (
        "Call(Fe:Expr", "CV:Val ~> #callee", "builtinV(BN:String)", "closureVal(PNS:ParamNames",
    ),
    "semantics/controls.k": (
        "Assign(Name(X:String), V:Val)", "AugAssign(Name(X:String)", "ImportFrom(_:String",
        "If(C:Val", "#branch(", "For(T:Expr", "#loop(IT:Iterable", "#iterDone ~> #loopStep",
        "#iterYield(V:Val, REST:Iterable)", "#loopLbl(NEXT:K)",
    ),
    "semantics/operators.k": (
        "BinOp(OP:String", "context Compare", "Compare(LV:Val",
    ),
    "semantics/int.k": (
        "applyBin(\"+\", I1:Int", "applyCmp(\"!=\", I1:Int",
    ),
    "semantics/float.k": (
        "Float(F:Float)", "floatLt(Float, Float)", "floatLt(F1:Float", "applyCmp(\"<\", F1:Float",
        "absF(Float)", "absF(F:Float)", "applyBuiltin(\"abs\", F:Float", "subF(Float, Float)",
        "subF(F1:Float", "applyBin(\"-\", F1:Float",
    ),
    "semantics/list.k": ("#iterNext(list(",),
    "semantics/tuple.k": ("#bindTgt(Name(X:String)",),
    "semantics/builtins.k": ("syntax Val ::= applyBuiltin",),
}


def assessment(item: Item, relative: str) -> str:
    if relative == "verification.k":
        return "CANDIDATE-LOCAL (manual rule-by-rule assessment in REVIEW.md)"
    if relative == "spec.k":
        return "CLAIM (manual pre/post and adequacy assessment in REVIEW.md)"
    pattern_key = relative.removeprefix("reference-semantics/")
    if item.kind in {"configuration", "syntax", "context"}:
        patterns = REACHED_PATTERNS.get(pattern_key, ())
        if any(pattern in item.body for pattern in patterns):
            return "SUPPLIED-REACHED declaration/evaluation-order mechanism"
        return "SUPPLIED-UNREACHED declaration"
    patterns = REACHED_PATTERNS.get(pattern_key, ())
    if any(pattern in item.body for pattern in patterns):
        return "SUPPLIED-REACHED rule (fixed baseline; manually audited on submitted path)"
    return "SUPPLIED-UNREACHED rule (fixed baseline; no matching redex on submitted path)"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    files = sorted((args.root / "reference-semantics").rglob("*.k"))
    files += [args.root / "verification.k", args.root / "spec.k"]
    all_items: list[Item] = []
    by_file: dict[str, list[Item]] = {}
    for path in files:
        relative = str(path.relative_to(args.root))
        items = logical_items(path)
        by_file[relative] = items
        all_items.extend(items)

    counts = Counter(item.kind for item in all_items)
    attr_counts: Counter[str] = Counter()
    for item in all_items:
        attr_counts.update(attributes(item))

    output = []
    output.append("# Exhaustive K source inventory")
    output.append("")
    output.append(f"Files: {len(files)}; inventoried items: {len(all_items)}")
    output.append("")
    output.append(f"Kinds: {dict(sorted(counts.items()))}")
    output.append("")
    output.append(f"Attributes: {dict(sorted(attr_counts.items()))}")
    output.append("")
    output.append("No item is omitted: entries begin at every top-level `configuration`, `syntax`, `rule`, `context`, `claim`, or `alias` source line.")
    output.append("")

    for relative, items in by_file.items():
        output.append(f"## `{relative}`")
        output.append("")
        if not items:
            output.append("No local configuration/syntax/rule/context/claim/alias declarations.")
            output.append("")
            continue
        for item in items:
            attrs = attributes(item)
            attr_text = ", ".join(attrs) if attrs else "none"
            output.append(
                f"- L{item.line} — {item.kind}; attributes: {attr_text}; assessment: {assessment(item, relative)}"
            )
            output.append("")
            output.append(f"  `{item.body.replace('`', chr(39))}`")
            output.append("")

    args.output.write_text("\n".join(output) + "\n", encoding="utf-8")
    print(f"output={args.output}")
    print(f"files={len(files)} items={len(all_items)} kinds={dict(sorted(counts.items()))}")
    print(f"attributes={dict(sorted(attr_counts.items()))}")
    print(f"bytes={args.output.stat().st_size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
