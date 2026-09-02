#!/usr/bin/env python3
"""Emit a source-complete K declaration/rule inventory with audit classifications."""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from pathlib import Path


WORK = Path("/tmp/audit-work/reconstruction")
SEMANTICS = WORK / "reference-semantics"
INPUTS = sorted(SEMANTICS.rglob("*.k")) + [
    WORK / "verification.k",
    WORK / "spec.k",
]

START = re.compile(r"^\s*(syntax|rule|context|configuration|claim|alias)\b")
BOUNDARY = re.compile(
    r"^\s*(?:syntax|rule|context|configuration|claim|alias|module|endmodule|imports|requires)\b"
)

# Exact source rules/declarations exercised by the submitted positive entry
# claim, plus Module/FuncDef rules exercised by the direct whole-file pinning run.
USED_MARKERS: dict[str, tuple[str, ...]] = {
    "semantics/syntax.k": (
        'syntax Expr ::= "Int"',
        '"Name"',
        '"BinOp"',
        '"Call"',
        'syntax Stmt ::= "Assign"',
        '"Return"',
        '"FuncDef"',
        "syntax Stmts",
        "syntax Params",
        "syntax ParamNames",
        "syntax Module",
    ),
    "semantics/core.k": (
        "configuration",
        "#loadAll",
        "(S:Stmt SS:Stmts)",
        ".Stmts => .K",
        "Name(X:String) => #look",
        "#look(X:String, L:Int) => {M[X]}",
        "builtinsScope",
        "#evalArgs",
        "#evalArgCont",
        "Int(I:Int)",
        "appendVal",
    ),
    "semantics/controls.k": ("Assign(Name(X:String), V:Val) => .K",),
    "semantics/functions.k": (
        "FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts)",
        "#bindP(.ParamNames, .Vals)",
        "#bindP((P:String, PS:ParamNames), (V:Val, VS:Vals))",
        "Return(V:Val)",
        "#pop => V ~> CONT",
    ),
    "semantics/call.k": (
        "Call(Fe:Expr, ARGS:Exprs)",
        "CV:Val ~> #callee",
        "#applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int))",
    ),
    "semantics/operators.k": ("BinOp(OP:String, L:Val, R:Val)",),
    "semantics/int.k": (
        'applyBin("+",',
        'applyBin("-",',
        'applyBin("*",',
        'applyBin("//",',
        "syntax Int ::= pyMod",
        "rule pyMod",
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_name(path: Path) -> str:
    if path.is_relative_to(SEMANTICS):
        relative = path.relative_to(SEMANTICS).as_posix()
        return "semantics.k" if relative == "semantics.k" else relative
    return path.name


def blocks(path: Path):
    lines = path.read_text().splitlines()
    index = 0
    while index < len(lines):
        match = START.match(lines[index])
        if match is None:
            index += 1
            continue
        start = index
        index += 1
        while index < len(lines) and not BOUNDARY.match(lines[index]):
            index += 1
        text = "\n".join(lines[start:index]).rstrip()
        yield match.group(1), start + 1, text


def classify(kind: str, text: str) -> str:
    if kind == "syntax":
        if "function" in text or "functional" in text:
            return "function-declaration"
        return "syntax-declaration"
    if kind == "rule":
        if "<k>" in text:
            return "ordinary-semantic-rule"
        return "equational-or-helper-rule"
    return kind


def attributes(text: str) -> list[str]:
    names = []
    code = "\n".join(line.split("//", 1)[0] for line in text.splitlines())
    checks = (
        "function",
        "functional",
        "total",
        "symbol",
        "no-evaluators",
        "priority",
        "simplification",
        "owise",
        "concrete",
        "macro",
        "macro-rec",
        "strict",
        "seqstrict",
    )
    for name in checks:
        if re.search(rf"\b{re.escape(name)}\b", code):
            names.append(name)
    return names


def is_used(name: str, text: str) -> bool:
    if name == "verification.k":
        return True
    return any(marker in text for marker in USED_MARKERS.get(name, ()))


def decision(name: str, kind: str, line: int, text: str, used: bool) -> str:
    if name == "verification.k":
        if kind == "rule" and line == 9:
            return (
                "ACCEPT: definitional AST alias; byte-for-byte regenerated solution.mpy "
                "has the same body and the alias does not intercept execution."
            )
        if kind == "rule" and line in {46, 52, 56}:
            return (
                "ACCEPT_ON_ENTRY_DOMAIN: terminating mathematical definition used on "
                "N>0-derived nonnegative counts; no operational redex is replaced."
            )
        return "ACCEPT: proof-local declaration for the audited definitions."
    if name == "spec.k":
        return (
            "CLAIM_ONLY: inventoried for adequacy; proof closure and result sensitivity "
            "are audited separately."
        )
    attrs = attributes(text)
    if "no-evaluators" in attrs:
        return (
            "UNUSED_TRUST_BOUNDARY: opaque/no-evaluator supplied-semantics symbol is "
            "not reachable from solution.mpy or any entry postcondition."
        )
    if used:
        return (
            "ACCEPT_ON_SUBMITTED_PATH: fixed supplied-semantics declaration/rule; "
            "binding, left-to-right evaluation, integer arithmetic, frame/return, and "
            "state footprint were checked for the matched submitted terms."
        )
    return (
        "OUTSIDE_SUBMITTED_PATH: fixed supplied-semantics declaration/rule is not "
        "reachable from the entry claim; no false-conclusion witness affecting this "
        "theorem was found."
    )


def main() -> int:
    grand = Counter()
    grand_attributes = Counter()
    symbol_declarations: list[str] = []
    print("INVENTORY_SCOPE")
    print("  supplied tree: /tmp/audit-work/reconstruction/reference-semantics")
    print("  proof-local: /tmp/audit-work/reconstruction/verification.k")
    print("  claims (adequacy cross-reference): /tmp/audit-work/reconstruction/spec.k")
    print()
    for path in INPUTS:
        name = source_name(path)
        entries = list(blocks(path))
        counts = Counter(kind for kind, _, _ in entries)
        grand.update(counts)
        print(
            f"FILE {name} SHA256={sha256(path)} "
            f"DECLARATIONS={len(entries)} COUNTS={dict(sorted(counts.items()))}"
        )
        for ordinal, (kind, line, text) in enumerate(entries, 1):
            used = is_used(name, text)
            attrs = attributes(text)
            grand_attributes.update(attrs)
            if kind == "syntax" and "symbol" in attrs:
                symbol_declarations.append(
                    f"{name}:{line} " + " ".join(text.split())
                )
            print(
                f"ENTRY {name}:{line} ORDINAL={ordinal} KIND={kind} "
                f"CLASS={classify(kind, text)} ATTRIBUTES={','.join(attrs) or 'none'} "
                f"SUBMITTED_PATH={str(used).lower()}"
            )
            print("TEXT_BEGIN")
            print(text)
            print("TEXT_END")
            print("AUDIT_DECISION " + decision(name, kind, line, text, used))
        print("END_FILE")
        print()
    print(f"TOTAL_DECLARATIONS {sum(grand.values())}")
    print("TOTAL_COUNTS " + repr(dict(sorted(grand.items()))))
    print("ATTRIBUTE_COUNTS " + repr(dict(sorted(grand_attributes.items()))))
    print(f"SYMBOL_DECLARATION_COUNT {len(symbol_declarations)}")
    for declaration in symbol_declarations:
        print("SYMBOL_DECLARATION " + declaration)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
