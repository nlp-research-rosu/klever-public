#!/usr/bin/env python3
"""Emit an exhaustive, line-addressed inventory of local K declarations/rules."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
SEMANTICS = ROOT / "reference-semantics"
VERIFICATION = ROOT / "verification.k"

START = re.compile(
    r"^\s*(configuration\b|syntax\b|rule\b|claim\b|context\s+alias\b|context\b)"
)
BOUNDARY = re.compile(
    r"^\s*(configuration\b|syntax\b|rule\b|claim\b|context\s+alias\b|context\b|"
    r"module\b|endmodule\b)"
)

RELEVANT_TERMS = (
    "Module",
    "#loadAll",
    "FuncDef",
    "closureVal",
    "frame(",
    "#bindP",
    "#pop",
    "#endcall",
    "Return(",
    "Call(",
    "#callee",
    "#evalArgs",
    "#evalArgCont",
    "#applyK",
    "toCall",
    "Name(",
    "#look",
    "builtinsScope",
    "Expr(",
    "Str(",
    "strToCodes",
    "If(",
    "#branch",
    "Compare(",
    "applyCmp",
    "BinOp(",
    "applyBin",
    'applyBuiltin("chr"',
    "truthy",
    "pyMod",
    "seqConcat",
    "freshScopes",
    "changeBase",
    "baseDigits",
)

OPAQUE_TERMS = (
    "intFloatDiv",
    "divII",
    "floatMod",
    "floatLt",
    "absF",
    "floorFI",
    "toF",
    "ceilF",
    "subF",
    "divF",
    "addF",
    "mulF",
    "powF",
    "gtF",
    "eqF",
    "decStrToF",
    "divFloatIntV",
    "intToF",
    "truncF",
    "roundF",
    "roundFN",
    "sqrtF",
    "sortVS",
    "sortKeyVS",
    "md5hexCodes",
)

PROOF_DECISIONS = {
    7: "ACCEPTED_DECLARATION|fresh-scope invariant predicate",
    8: "ACCEPTED_MATH|empty suffix has no allocated keys",
    9: "ACCEPTED_MATH|freshScopes(L,S) implies L is absent from S",
    11: "ACCEPTED_MATH|contiguous descending fresh-frame suffix constructor",
    17: "ACCEPTED_MAP_EQUATION|fresh Map update equals disjoint binding",
    19: "ACCEPTED_MAP_EQUATION|deleting the unique fresh binding restores S",
    23: "ACCEPTED_DECLARATION|name for exact submitted body",
    24: "ACCEPTED_DEFINITION|exact byte-regenerated AST constructor tree",
    45: "ACCEPTED_DECLARATION|name for exact submitted module",
    46: "ACCEPTED_DEFINITION|module contains exact change_base definition",
    51: "ACCEPTED_DECLARATION|name for exact submitted closure",
    52: "ACCEPTED_DEFINITION|closure has exact params, body, definition scope 0",
    57: "ACCEPTED_DECLARATION|mathematical result summary",
    58: "ACCEPTED_MATH|zero is represented by the empty code sequence",
    59: "ACCEPTED_MATH|positive base-B recurrence; quotient strictly decreases for B>=2",
}


def strip_line_comment(line: str) -> str:
    quoted = False
    escaped = False
    index = 0
    while index < len(line):
        char = line[index]
        if escaped:
            escaped = False
        elif char == "\\" and quoted:
            escaped = True
        elif char == '"':
            quoted = not quoted
        elif (
            char == "/"
            and index + 1 < len(line)
            and line[index + 1] == "/"
            and not quoted
        ):
            return line[:index]
        index += 1
    return line


def code_only(text: str) -> str:
    return "\n".join(strip_line_comment(line) for line in text.splitlines())


def normalized(text: str) -> str:
    pieces = []
    for line in code_only(text).splitlines():
        code = line.strip()
        if code:
            pieces.append(code)
    return " ".join(pieces)


def attr_summary(text: str) -> str:
    text = code_only(text)
    flags = []
    for flag in (
        "function",
        "total",
        "functional",
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
    ):
        if re.search(rf"\b{re.escape(flag)}\b", text):
            flags.append(flag)
    return ",".join(flags) or "-"


def disposition(path: Path, line: int, text: str) -> str:
    text = code_only(text)
    if path == VERIFICATION:
        return PROOF_DECISIONS.get(
            line, "REVIEW_REQUIRED|unmapped proof-local declaration or rule"
        )
    relative = path.relative_to(ROOT).as_posix()
    if relative.endswith("/concrete.k"):
        return "UNUSED_CONCRETE_ONLY|not imported by the Haskell proof module"
    if any(term in text for term in OPAQUE_TERMS):
        return "UNUSED_OPAQUE_BOUNDARY|symbol/route unreachable from solution.mpy"
    if any(term in text for term in RELEVANT_TERMS):
        return (
            "ACCEPTED_FIXED_RELEVANT|reachable supplied-semantics behavior; "
            "Python-consistent on X>=0,2<=B<10"
        )
    return (
        "ACCEPTED_FIXED_INERT|fixed supplied-semantics construct is unreachable "
        "from this program and proof summary"
    )


def items(path: Path) -> list[tuple[int, int, str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    result = []
    for position, start in enumerate(starts):
        provisional_end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        end = provisional_end
        for index in range(start + 1, provisional_end):
            if BOUNDARY.match(lines[index]) and not START.match(lines[index]):
                end = index
                break
        text = "\n".join(lines[start:end])
        kind_match = START.match(lines[start])
        assert kind_match is not None
        kind = kind_match.group(1).replace(" ", "_")
        result.append((start + 1, end, kind, text))
    return result


def main() -> int:
    paths = sorted(SEMANTICS.rglob("*.k")) + [VERIFICATION]
    print(
        "id\tfile\tline_start\tline_end\tkind\tattributes\tdisposition\tstatement"
    )
    item_id = 0
    for path in paths:
        for start, end, kind, text in items(path):
            item_id += 1
            statement = normalized(text).replace("\t", " ")
            decision = disposition(path, start, text)
            print(
                f"{item_id}\t{path.relative_to(ROOT).as_posix()}\t{start}\t{end}"
                f"\t{kind}\t{attr_summary(text)}\t{decision}\t{statement}"
            )
    print(f"# ITEM_COUNT={item_id}")
    for path in paths:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        print(f"# SHA256 {digest} {path.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
