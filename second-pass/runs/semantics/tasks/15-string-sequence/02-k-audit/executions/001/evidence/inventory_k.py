#!/usr/bin/env python3
"""Enumerate every K declaration/rule/context/configuration in the audit sources."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
FILES = [
    ROOT / "reference-semantics" / "semantics.k",
    *sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")),
    ROOT / "verification.k",
]
START = re.compile(r"^\s*(configuration|syntax|rule|context|claim)\b")
STOP = re.compile(r"^\s*(?:module|endmodule)\b")
ATTR_NAMES = (
    "function",
    "total",
    "functional",
    "macro",
    "simplification",
    "concrete",
    "priority",
    "owise",
    "injective",
    "symbol",
    "no-evaluators",
    "strict",
    "seqstrict",
)
USED_TERMS = (
    "Module",
    "#loadAll",
    "FuncDef",
    "closureVal",
    "Call",
    "#callee",
    "#evalArgs",
    "#applyK",
    "#bindP",
    "frame",
    "#endcall",
    "#pop",
    "Expr(",
    "Str(",
    "strToCodes",
    "Name(",
    "#look",
    "Int(",
    "BinOp",
    "applyBin",
    "Compare",
    "applyCmp",
    "If(",
    "#branch",
    "Assign(",
    "For(",
    "#loop",
    "#iterNext",
    "rangeObj",
    "inRange",
    'applyBuiltin("range"',
    'applyBuiltin("str"',
    "Return(",
    "sequenceCodes",
    "seqConcat",
    "sequenceLoopBody",
    "sequenceBody",
)


def blocks(path: Path):
    lines = path.read_text().splitlines()
    i = 0
    while i < len(lines):
        match = START.match(lines[i])
        if not match:
            i += 1
            continue
        start = i
        i += 1
        while i < len(lines):
            if START.match(lines[i]) or STOP.match(lines[i]):
                break
            i += 1
        yield start + 1, match.group(1), "\n".join(lines[start:i]).strip()


def compact(text: str) -> str:
    return " ".join(part.strip() for part in text.splitlines())


rows = []
counter = 0
for path in FILES:
    relative = path.relative_to(ROOT)
    for line, kind, text in blocks(path):
        counter += 1
        attrs = [name for name in ATTR_NAMES if re.search(rf"\b{re.escape(name)}\b", text)]
        if kind == "rule":
            subtype = "operational rule" if "<k>" in text else "equational rule"
        elif kind == "syntax":
            subtype = "syntax/function declaration" if "function" in attrs else "syntax declaration"
        else:
            subtype = kind
        source_class = (
            "candidate proof extension"
            if relative == Path("verification.k")
            else "trusted supplied semantics"
        )
        relevance = "used path" if any(term in text for term in USED_TERMS) else "unused by solution.mpy"
        if source_class == "trusted supplied semantics":
            decision = (
                "ACCEPTED AS FIXED SEMANTICS; byte-identical trusted baseline; "
                + ("manually traced on the program path" if relevance == "used path" else "off program path")
            )
        else:
            decision = "MANUAL DECISION IN REVIEW.md STAGE 5"
        rows.append(
            {
                "id": f"K{counter:04d}",
                "file": str(relative),
                "line": line,
                "kind": subtype,
                "attributes": ",".join(attrs) if attrs else "-",
                "relevance": relevance,
                "source_class": source_class,
                "decision": decision,
                "text": compact(text),
            }
        )

writer = csv.DictWriter(
    __import__("sys").stdout,
    fieldnames=[
        "id",
        "file",
        "line",
        "kind",
        "attributes",
        "relevance",
        "source_class",
        "decision",
        "text",
    ],
    dialect="excel-tab",
    lineterminator="\n",
)
writer.writeheader()
writer.writerows(rows)
