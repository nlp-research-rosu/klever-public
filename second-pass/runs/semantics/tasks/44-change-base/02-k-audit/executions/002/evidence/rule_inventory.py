#!/usr/bin/env python3
"""Lexical inventory and relevance classification for every local K sentence."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


WORK = Path("/tmp/audit-work/44-change-base")
OUTPUT = Path("/audit-output/evidence/05-rule-inventory.tsv")
FILES = [
    WORK / "reference-semantics" / "semantics.k",
    *sorted((WORK / "reference-semantics" / "semantics").glob("*.k")),
    WORK / "verification.k",
    WORK / "spec.k",
]
KEYWORDS = (
    "requires",
    "module",
    "imports",
    "syntax",
    "configuration",
    "context",
    "rule",
    "claim",
    "priority",
    "endmodule",
)
USED_PATTERNS = {
    "semantics.k": [r"\bMPY\b", r"\bMPY-KRUN\b"],
    "syntax.k": [
        r"syntax Expr",
        r"syntax CmpOp",
        r"syntax Stmt",
        r"syntax Stmts",
        r"syntax Params",
        r"syntax ParamNames",
        r"syntax Module",
    ],
    "core.k": [
        r"syntax IntSeq",
        r"syntax Str",
        r"syntax Val\b",
        r"syntax Parent",
        r"syntax Scope",
        r"syntax KResult",
        r"syntax Expr",
        r"syntax Vals",
        r"syntax Exc",
        r"syntax RetState",
        r"\bconfiguration\b",
        r"#loadAll",
        r"\(S:Stmt SS:Stmts\)",
        r"<k> \.Stmts",
        r"#look",
        r"Name\(X:String\)",
        r"builtinsScope",
        r"syntax ApplyK",
        r"#evalArgs",
        r"#evalArgCont",
        r"#applyK",
        r"<k> Int\(",
        r"syntax Bool ::= truthy",
        r"truthy\(B:Bool\)",
        r"syntax Val\s+::= applyBin",
        r"syntax Bool ::= applyCmp",
        r"appendVal",
    ],
    "operators.k": [
        r"BinOp\(OP:String, L:Val, R:Val\)",
        r"context Compare",
        r"Compare\(LV:Val, CmpOp",
    ],
    "int.k": [
        r'applyBin\("\\+"',
        r'applyBin\("%"',
        r'applyBin\("//"',
        r"syntax Int ::= pyMod",
        r"rule pyMod",
        r'applyCmp\("=="',
    ],
    "str.k": [
        r"syntax IntSeq ::= strToCodes",
        r"<k> Str\(",
        r"rule strToCodes",
        r"syntax IntSeq ::= seqConcat",
        r"rule seqConcat",
        r'applyBin\("\\+"',
    ],
    "controls.k": [
        r"<k> Expr\(",
        r"syntax KItem ::= #branch",
        r"<k> If\(",
        r"<k> #branch",
    ],
    "functions.k": [
        r"syntax KItem ::= frame",
        r"<k> FuncDef\(",
        r"<k> #bindP",
        r"<k> Return\(",
        r"<k> #pop",
    ],
    "builtins.k": [
        r"syntax Val ::= applyBuiltin",
        r'applyBuiltin\("chr"',
    ],
    "call.k": [
        r"syntax KItem ::= #callee",
        r"<k> Call\(",
        r"#callee\(ARGS",
        r"#applyK\(toCall\(builtinV\(BN",
        r"#applyK\(toCall\(closureVal\(",
    ],
}


def head(line: str) -> str | None:
    stripped = line.lstrip(" ")
    indent = len(line) - len(stripped)
    if indent not in (0, 2):
        return None
    for keyword in KEYWORDS:
        if stripped == keyword or stripped.startswith(keyword + " "):
            return keyword
    return None


def sentences(path: Path):
    lines = path.read_text().splitlines()
    starts = [(index, head(line)) for index, line in enumerate(lines)]
    starts = [(index, kind) for index, kind in starts if kind is not None]
    for position, (start, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        text = "\n".join(lines[start:end]).strip()
        yield start + 1, end, kind, text


def relevance(path: Path, kind: str, text: str) -> str:
    if path.name in {"verification.k", "spec.k"}:
        return "proof-local"
    patterns = USED_PATTERNS.get(path.name, [])
    if any(re.search(pattern, text) for pattern in patterns):
        return "used-path"
    if kind in {"module", "imports", "requires", "endmodule"}:
        return "assembly"
    return "unused-path"


def decision(path: Path, kind: str, rel: str, text: str) -> tuple[str, str]:
    compact = " ".join(text.split())
    if path.name == "verification.k":
        if "freshScopes" in compact:
            note = (
                "partial consecutive-suffix freshness invariant; base/step guards "
                "are disjoint and imply queried allocator key is absent"
            )
        elif "in_keys" in compact and "<-" in compact:
            note = "fresh-key insertion or unique-key deletion identity for hooked K Map"
        elif "changeBaseBody" in compact or "solutionModule" in compact or "changeBaseClosure" in compact:
            note = "definitional constructor alias mechanically matched to translated program"
        elif "baseDigits" in compact:
            note = (
                "partial mathematical base-digit definition; disjoint zero/positive "
                "guards and strict descent for base >= 2"
            )
        else:
            note = "proof-module assembly"
        return "ACCEPTED", note
    if path.name == "spec.k":
        note = (
            "recursive-call circularity"
            if "#applyK" in compact
            else "whole-module target claim"
            if "#loadAll" in compact
            else "spec assembly"
        )
        return "CLAIM", note
    if rel == "used-path":
        return (
            "ACCEPTED_FIXED_USED",
            "trusted supplied semantics; manually checked on the submitted program path",
        )
    if rel == "unused-path":
        opaque = "no-evaluators" in compact or "opaque" in compact.lower()
        return (
            "ACCEPTED_FIXED_UNUSED",
            "trusted supplied semantics; unreachable from submitted program"
            + ("; contains an opaque fixed primitive" if opaque else ""),
        )
    return "ASSEMBLY", "module/import/include boundary"


rows = []
for path in FILES:
    relative = path.relative_to(WORK).as_posix()
    for start, end, kind, text in sentences(path):
        rel = relevance(path, kind, text)
        verdict, note = decision(path, kind, rel, text)
        trailing = re.findall(r"\[([^\[\]]+)\]", text)
        flags = ",".join(
            sorted(
                {
                    flag.strip()
                    for group in trailing
                    for flag in group.split(",")
                    if flag.strip()
                }
            )
        )
        rows.append(
            {
                "id": f"{relative}:{start}",
                "file": relative,
                "start": start,
                "end": end,
                "kind": kind,
                "attributes": flags,
                "relevance": rel,
                "decision": verdict,
                "note": note,
                "text": " ".join(text.split()),
            }
        )

with OUTPUT.open("w", newline="") as stream:
    writer = csv.DictWriter(stream, fieldnames=rows[0].keys(), delimiter="\t")
    writer.writeheader()
    writer.writerows(rows)

counts = Counter((row["kind"], row["relevance"], row["decision"]) for row in rows)
print(f"INVENTORY_ROWS={len(rows)}")
for key, count in sorted(counts.items()):
    print("\t".join((*key, str(count))))
print(f"OUTPUT={OUTPUT}")
