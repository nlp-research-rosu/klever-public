#!/usr/bin/env python3
"""Generate a complete statement/attribute inventory for the audited K sources.

This is a lexical inventory, not a parser. K top-level declarations in these
sources consistently start at two spaces; continuation lines are folded into
the declaration that precedes them.
"""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
OUTPUT = Path("/audit-output/evidence/05_rule_inventory.md")

sources = [ROOT / "reference-semantics" / "semantics.k"]
sources += sorted((ROOT / "reference-semantics" / "semantics").glob("*.k"))
sources += [ROOT / "verification.k", ROOT / "spec.k"]

start_re = re.compile(r"^  (syntax|rule|context|configuration|claim)\b")
attr_re = re.compile(
    r"\[(?:[^\]]*\b(?:function|total|functional|simplification|concrete|"
    r"priority|symbol|no-evaluators|opaque)\b[^\]]*)\]"
)


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def entries(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [
        index
        for index, line in enumerate(lines)
        if start_re.match(line)
    ]
    for pos, index in enumerate(starts):
        end = starts[pos + 1] if pos + 1 < len(starts) else len(lines)
        body_lines = []
        for line in lines[index:end]:
            stripped = line.strip()
            if stripped == "endmodule":
                break
            if stripped.startswith("//") or not stripped:
                continue
            body_lines.append(stripped)
        text = " ".join(body_lines)
        text = re.sub(r"\s+", " ", text)
        yield index + 1, start_re.match(lines[index]).group(1), text


used_fragments = {
    "semantics/syntax.k": (
        "syntax Expr",
        "syntax CmpOp",
        "syntax Exprs",
        "syntax Stmt",
        "syntax Stmts",
        "syntax Params",
        "syntax ParamNames",
        "syntax Module",
    ),
    "semantics/core.k": (
        "syntax Val ",
        "syntax Parent",
        "syntax Scope ",
        "syntax KResult",
        "syntax Expr ",
        "syntax Vals",
        "syntax Exc",
        "syntax RetState",
        "configuration",
        "syntax KItem ::= #loadAll",
        "#loadAll(Module",
        "(S:Stmt SS:Stmts)",
        ".Stmts =>",
        "syntax KItem ::= #look",
        "Name(X:String) => #look",
        "#look(X:String, L:Int) => {M[X]}",
        "#look(X:String, L:Int) => #look(X, P)",
        "syntax Scope ::= \"builtinsScope\"",
        "rule builtinsScope",
        "syntax ApplyK ::= toCall",
        "syntax KItem ::= #evalArgs",
        "#evalArgs((A:Expr",
        "#evalArgCont(REST",
        "#evalArgs(.Exprs",
        "syntax Bool ::= truthy",
        "truthy(B:Bool)",
        "syntax Val ::= applyUn",
        "syntax Val ::= applyBin",
        "syntax Bool ::= applyCmp",
        "syntax Vals ::= appendVal",
        "appendVal(.Vals",
        "appendVal((V0:Val",
    ),
    "semantics/functions.k": (
        "syntax KItem ::= frame",
        "FuncDef(F:String",
        "#bindP(.ParamNames",
        "#bindP((P:String",
        "Return(V:Val)",
        "#endcall =>",
        "#pop =>",
    ),
    "semantics/call.k": (
        "syntax KItem ::= #callee",
        "Call(Fe:Expr",
        "CV:Val ~> #callee",
        "#applyK(toCall(builtinV(BN:String)), ACC:Vals)",
        "#applyK(toCall(closureVal(",
    ),
    "semantics/operators.k": (
        "UnaryOp(OP:String",
        "BinOp(OP:String",
        "context Compare",
        "Compare(LV:Val",
    ),
    "semantics/bool.k": (
        "context BoolOp",
        "BoolOp(",
    ),
    "semantics/int.k": (
        'applyBin("+"',
        'applyCmp("=="',
    ),
    "semantics/builtins.k": (
        "syntax Val ::= applyBuiltin",
        'applyBuiltin("isinstance"',
        "syntax Bool ::= isIntV",
        "isIntV(",
    ),
}


def assess(path: Path, kind: str, text: str) -> str:
    rel = relative(path)
    if rel == "verification.k":
        if text.startswith("syntax Stmts ::= \"anyIntBody\""):
            return "CANDIDATE-DEF-OK"
        if text.startswith("rule anyIntBody"):
            return "CANDIDATE-DEF-OK"
        if text.startswith("syntax KItem ::= \"#anyInt\""):
            return "CANDIDATE-BRIDGE-GAP"
        if text.startswith("rule <k> #anyInt"):
            return "CANDIDATE-BRIDGE-GAP"
        if "sumCondition" in text:
            return "CANDIDATE-DEF-OK"
        return "CANDIDATE-REVIEW"
    if rel == "spec.k":
        if kind == "claim":
            return "RESULT-CONSTRAINING-CLAIM"
        return "SPEC-REVIEW"
    if "symbol(" in text or "no-evaluators" in text or "[concrete]" in text:
        return "FIXED-UNREACHABLE-OPAQUE/CONCRETE"
    if kind == "rule" and (
        "ref(" in text
        or "cellRef" in text
        or '"$cells"' in text
        or "closureValC" in text
    ):
        return "FIXED-UNREACHABLE"
    if rel == "reference-semantics/semantics/builtins.k":
        if "isIntV(_:Val)" in text:
            return "USED-FALSE-PYTHON-BRIDGE"
        if 'typeV("str")' in text or "isStrV(" in text:
            return "FIXED-UNREACHABLE"
        if "isIntV" in text or 'applyBuiltin("isinstance"' in text:
            return "USED-MODEL-GAP-PATH"
    short_rel = rel.removeprefix("reference-semantics/")
    for fragment in used_fragments.get(short_rel, ()):
        if fragment in text:
            if "#loadAll" in text or "FuncDef(F:String" in text:
                return "REAL-LOAD-PATH-BYPASSED"
            return "USED-ALIGNS-WITH-SUBSET"
    return "FIXED-UNREACHABLE"


all_entries = []
attributes = []
for source in sources:
    for line, kind, text in entries(source):
        all_entries.append(
            (relative(source), line, kind, assess(source, kind, text), text)
        )
    for line_number, raw in enumerate(
        source.read_text(encoding="utf-8").splitlines(), 1
    ):
        code = raw.split("//", 1)[0]
        for match in attr_re.finditer(code):
            attributes.append((relative(source), line_number, match.group(0)))

counts = collections.Counter(kind for _, _, kind, _, _ in all_entries)
assessments = collections.Counter(item[3] for item in all_entries)

with OUTPUT.open("w", encoding="utf-8") as out:
    out.write("# Exhaustive K declaration and rule inventory\n\n")
    out.write(
        "Generated from the clean source-only reconstruction. Every top-level "
        "`syntax`, `configuration`, `context`, `rule`, and `claim` statement is "
        "listed once; multiline statements are folded into one row.\n\n"
    )
    out.write("## Counts\n\n")
    out.write(f"- Files: {len(sources)}\n")
    out.write(f"- Statements: {len(all_entries)}\n")
    for name in ("syntax", "configuration", "context", "rule", "claim"):
        out.write(f"- {name}: {counts[name]}\n")
    out.write(f"- attribute occurrences: {len(attributes)}\n\n")
    out.write("Assessment legend:\n\n")
    out.write(
        "- `USED-ALIGNS-WITH-SUBSET`: reachable on this program and, except for "
        "the separately flagged Bool relation, matches its declared MPY subset.\n"
        "- `USED-MODEL-GAP-PATH` / `USED-FALSE-PYTHON-BRIDGE`: reachable "
        "`isinstance(..., int)` path; the latter has the concrete Bool witness.\n"
        "- `REAL-LOAD-PATH-BYPASSED`: fixed rules that would load/bind the real "
        "module but that `#anyInt` does not exercise.\n"
        "- `CANDIDATE-DEF-OK`: truthful proof-local equation checked against the "
        "submitted AST or ordinary integer mathematics.\n"
        "- `CANDIDATE-BRIDGE-GAP`: proof-local operational bridge with no "
        "bridge-free connection theorem to module load/name lookup.\n"
        "- `RESULT-CONSTRAINING-CLAIM`: entry claim with a concrete, non-free "
        "Boolean destination.\n"
        "- `FIXED-UNREACHABLE` and `FIXED-UNREACHABLE-OPAQUE/CONCRETE`: supplied "
        "semantics statements not reachable from this submitted AST; no "
        "unsoundness conclusion is asserted for these unused rules.\n\n"
    )
    out.write("## Statements\n\n")
    out.write("| Source:line | Kind | Assessment | Statement |\n")
    out.write("|---|---|---|---|\n")
    for rel, line, kind, assessment, text in all_entries:
        escaped = text.replace("|", "\\|")
        out.write(
            f"| `{rel}:{line}` | {kind} | {assessment} | `{escaped}` |\n"
        )

    out.write("\n## Function/total/opaque/priority and related attributes\n\n")
    out.write("| Source:line | Attribute |\n")
    out.write("|---|---|\n")
    for rel, line, attribute in attributes:
        out.write(f"| `{rel}:{line}` | `{attribute}` |\n")

    out.write("\n## Assessment totals\n\n")
    for assessment, count in sorted(assessments.items()):
        out.write(f"- {assessment}: {count}\n")

print(f"output={OUTPUT}")
print(f"files={len(sources)}")
print(f"statements={len(all_entries)}")
for name in ("syntax", "configuration", "context", "rule", "claim"):
    print(f"{name}={counts[name]}")
print(f"attribute_occurrences={len(attributes)}")
for assessment, count in sorted(assessments.items()):
    print(f"{assessment}={count}")
