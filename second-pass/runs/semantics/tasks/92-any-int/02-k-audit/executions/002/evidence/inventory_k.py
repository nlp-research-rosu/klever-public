#!/usr/bin/env python3
"""Emit an exhaustive statement inventory for the imported K source tree."""

from __future__ import annotations

from collections import Counter
import csv
from pathlib import Path
import re
import sys


ROOT = Path("/tmp/audit-work/92-any-int")
FILES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "spec.k",
]

START = re.compile(
    r"^\s*(configuration|syntax|context|rule|claim)\b"
)
BOUNDARY = re.compile(
    r"^\s*(configuration|syntax|context|rule|claim|module|endmodule)\b"
)

DIRECT_MARKERS = (
    "#loadAll",
    "Module(",
    "FuncDef(",
    "Return(",
    "#pop",
    "#endcall",
    "#bindP",
    "closureVal(",
    "#applyK",
    "toCall",
    "Call(",
    "#callee",
    "#evalArgs",
    "#evalArgCont",
    "Name(",
    "#look",
    "builtinsScope",
    'builtinV("isinstance")',
    'typeV("int")',
    'applyBuiltin("isinstance"',
    "isIntV",
    "BoolOp(",
    "truthy(",
    "BinOp(",
    "Compare(",
    "CmpOp(",
    "applyBin",
    "applyCmp",
    'applyBin("+"',
    'applyCmp("=="',
    "Int(",
    "Float(",
    "Bool(",
    "anyIntBody",
    "#anyInt",
    "sumCondition",
)


def chunks(path: Path):
    lines = path.read_text().splitlines()
    starts = [
        index for index, line in enumerate(lines)
        if START.match(line)
    ]
    for number, index in enumerate(starts):
        end = len(lines)
        for probe in range(index + 1, len(lines)):
            if BOUNDARY.match(lines[probe]):
                end = probe
                break
        yield index + 1, "\n".join(lines[index:end]).strip()


rows: list[dict[str, str]] = []
for path in FILES:
    rel = path.relative_to(ROOT).as_posix()
    for line, text in chunks(path):
        code_lines = [source_line.split("//", 1)[0] for source_line in text.splitlines()]
        code = "\n".join(source_line for source_line in code_lines if source_line.strip())
        first = code.splitlines()[0].strip()
        kind = START.match(first).group(1)
        attributes: list[str] = []
        for attribute in (
            "function",
            "total",
            "functional",
            "macro",
            "owise",
            "priority",
            "simplification",
            "concrete",
            "no-evaluators",
            "symbol",
            "strict",
            "seqstrict",
        ):
            if re.search(rf"\b{re.escape(attribute)}\b", code):
                attributes.append(attribute)
        if rel == "verification.k":
            scope = "candidate-proof-local"
            decision = "ACCEPTED_MANUAL_REVIEW"
            basis = "truthful body macro, exact call harness, or arithmetic definition"
        elif rel == "spec.k":
            scope = "candidate-claim"
            decision = "AUDITED_ENTRY_CLAIM"
            basis = "precondition, postcondition, satisfiability, and coverage reviewed"
        elif any(marker in code for marker in DIRECT_MARKERS):
            scope = "fixed-supplied-direct-slice"
            decision = "ACCEPTED_FIXED_USED_SLICE"
            basis = "integrity-locked supplied rule; used behavior reviewed for this program"
        else:
            scope = "fixed-supplied-imported-unused"
            decision = "NO_MATCH_IN_PROOF_CONE"
            basis = "integrity-locked supplied rule; lhs construct absent from executed claim term"
        rows.append(
            {
                "id": f"{rel}:{line}",
                "file": rel,
                "line": str(line),
                "kind": kind,
                "attributes": ",".join(attributes) or "-",
                "scope": scope,
                "audit_decision": decision,
                "basis": basis,
                "statement": " ".join(code.split()),
            }
        )

writer = csv.DictWriter(
    sys.stdout,
    fieldnames=(
        "id",
        "file",
        "line",
        "kind",
        "attributes",
        "scope",
        "audit_decision",
        "basis",
        "statement",
    ),
    delimiter="\t",
    lineterminator="\n",
)
writer.writeheader()
writer.writerows(rows)

counts = Counter((row["scope"], row["kind"]) for row in rows)
print("# COUNTS", file=sys.stderr)
for key, count in sorted(counts.items()):
    print(f"# {key[0]}\t{key[1]}\t{count}", file=sys.stderr)
print(f"# TOTAL\t{len(rows)}", file=sys.stderr)
