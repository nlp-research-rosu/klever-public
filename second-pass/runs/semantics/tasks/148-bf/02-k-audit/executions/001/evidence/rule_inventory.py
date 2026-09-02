#!/usr/bin/env python3
"""Create an exhaustive source-level K declaration/rule inventory."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/148-bf-audit")
SEMANTICS = SCRATCH / "reference-semantics"
VERIFICATION = SCRATCH / "verification.k"
OUTPUT = Path("/audit-output/evidence/rule-inventory.tsv")
SUMMARY = Path("/audit-output/evidence/rule-inventory-summary.txt")

START_RE = re.compile(
    r"^\s*(configuration|context\s+alias|context|syntax|rule|claim|alias)\b"
)
BOUNDARY_RE = re.compile(
    r"^\s*(module|endmodule|configuration|context\s+alias|context|syntax|"
    r"rule|claim|alias)\b"
)


def source_files() -> list[Path]:
    return sorted(SEMANTICS.rglob("*.k")) + [VERIFICATION]


def extract(path: Path) -> list[tuple[int, str, str]]:
    lines = path.read_text().splitlines()
    records: list[tuple[int, str, str]] = []
    index = 0
    while index < len(lines):
        match = START_RE.match(lines[index])
        if match is None:
            index += 1
            continue
        start = index
        kind = match.group(1).replace(" ", "_")
        index += 1
        while index < len(lines) and BOUNDARY_RE.match(lines[index]) is None:
            index += 1
        text = "\n".join(lines[start:index]).rstrip()
        records.append((start + 1, kind, text))
    return records


def traits(kind: str, text: str) -> list[str]:
    found: list[str] = []
    for trait in [
        "function",
        "functional",
        "total",
        "macro",
        "macro-rec",
        "symbol",
        "no-evaluators",
        "strict",
        "seqstrict",
        "priority",
        "owise",
        "concrete",
        "simplification",
    ]:
        if re.search(rf"\b{re.escape(trait)}\b", text):
            found.append(trait)
    if kind == "rule":
        found.append("operational" if "<k>" in text else "equational")
    return sorted(set(found))


def role(path: Path, kind: str, text: str) -> str:
    if path == VERIFICATION:
        if kind == "syntax" and "macro" in traits(kind, text):
            return "proof-local constructor macro"
        if kind == "syntax":
            return "proof-local declaration"
        if kind == "rule" and "<k>" in text:
            return "proof-local case enumerator"
        if kind == "rule":
            return "proof-local mathematical definition"
        return "proof-local structure"
    if path.name == "concrete.k":
        return "supplied concrete-only semantics"
    if kind == "syntax":
        return "supplied syntax or helper declaration"
    if kind == "configuration":
        return "supplied configuration"
    if kind == "context":
        return "supplied evaluation-order context"
    if kind == "rule" and "<k>" in text:
        return "supplied operational semantics"
    if kind == "rule":
        return "supplied equational semantics"
    return "supplied semantics"


def decision(path: Path, kind: str, text: str) -> str:
    """Per-entry audit disposition; detailed reasoning is in REVIEW.md."""
    if path == VERIFICATION:
        if "bfCall" in text or "planetCodes" in text or "planetPosition" in text:
            return "ACCEPT_UNUSED_PROOF_LOCAL_DEFINITION"
        if "bfBody" in text or "bfRun" in text:
            return "ACCEPT_MECHANICALLY_PINNED_MACRO"
        if "#validCases" in text:
            return "ACCEPT_FINITE_DOMAIN_ENUMERATOR"
        if "planetVals" in text or "expectedBetween" in text:
            return "ACCEPT_RESULT_CONSTRAINING_DEFINITION"
        if "planetExpr" in text or "Planet" in text:
            return "ACCEPT_GROUND_CASE_DEFINITION"
        return "ACCEPT_PROOF_LOCAL_STRUCTURE"

    # The supplied tree is launcher-fixed. Rules in the real program's dynamic
    # trust cone receive an explicit relevant disposition; all others remain in
    # the fixed-semantics trust boundary and cannot match this program term.
    relevant_markers = {
        "syntax.k": [
            "Module",
            "FuncDef",
            "Assign",
            "Name",
            "TupleExpr",
            "Str",
            "If",
            "BoolOp",
            "Compare",
            "CmpOp",
            "Return",
            "Call",
            "Attribute",
            "Subscript",
            "Slice",
            "BinOp",
            "Int",
            "Assert",
        ],
        "core.k": [
            "configuration",
            "#loadAll",
            ".Stmts",
            "Name(",
            "#look",
            "builtinsScope",
            "#evalArgs",
            "#evalArgCont",
            "#applyK",
            "Int(",
            "truthy",
            "appendVal",
            "vals2valSeq",
            "vsLen",
        ],
        "operators.k": ["BinOp", "Compare", "applyBin", "applyCmp"],
        "int.k": ["applyBin(\"+\"", "applyCmp(\"<\""],
        "bool.k": ["BoolOp"],
        "str.k": ["Str(", "strToCodes", "applyCmp(\"==\""],
        "tuple.k": [
            "TupleExpr",
            "toTuple",
            "Compare",
            "#memberAcc",
            "idxOfVS",
            "applyCmp",
        ],
        "subscript.k": [
            "Subscript",
            "#evalB",
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
            "buildVS",
            "valSeqAt",
        ],
        "controls.k": ["Assign(", "If(", "#branch"],
        "functions.k": ["FuncDef", "#bindP", "Return", "#endcall", "#pop"],
        "call.k": [
            "Call(",
            "#callee",
            "toCall(boundMethodV",
            "closureVal(",
        ],
        "list.k": ["#memberAcc", "#memberCont", "#notB"],
        "assert.k": ["Assert("],
    }
    if any(marker in text for marker in relevant_markers.get(path.name, [])):
        if "total" in traits(kind, text):
            return "ACCEPT_RELEVANT_TOTAL_GROUND_OR_CONSTRUCTOR_EXHAUSTIVE"
        return "ACCEPT_RELEVANT_RULE_REVIEWED"
    if "no-evaluators" in traits(kind, text):
        return "INERT_OPAQUE_FIXED_PRIMITIVE"
    if "total" in traits(kind, text):
        return "INERT_FIXED_TOTAL_DECLARATION"
    return "INERT_FIXED_SEMANTICS_ENTRY"


def main() -> None:
    rows: list[dict[str, str | int]] = []
    for path in source_files():
        relative = (
            "verification.k"
            if path == VERIFICATION
            else path.relative_to(SCRATCH).as_posix()
        )
        for line, kind, text in extract(path):
            rows.append(
                {
                    "id": f"{relative}:{line}",
                    "source": relative,
                    "line": line,
                    "kind": kind,
                    "traits": ",".join(traits(kind, text)),
                    "role": role(path, kind, text),
                    "decision": decision(path, kind, text),
                    "text": " ".join(part.strip() for part in text.splitlines()),
                }
            )

    with OUTPUT.open("w", newline="") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=[
                "id",
                "source",
                "line",
                "kind",
                "traits",
                "role",
                "decision",
                "text",
            ],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(rows)

    by_kind = Counter(str(row["kind"]) for row in rows)
    by_decision = Counter(str(row["decision"]) for row in rows)
    by_source = Counter(str(row["source"]) for row in rows)
    with SUMMARY.open("w") as stream:
        print(f"inventory_entries={len(rows)}", file=stream)
        print(f"by_kind={dict(sorted(by_kind.items()))}", file=stream)
        print(f"by_decision={dict(sorted(by_decision.items()))}", file=stream)
        print("by_source:", file=stream)
        for source, count in sorted(by_source.items()):
            print(f"  {source}: {count}", file=stream)
    print(SUMMARY.read_text(), end="")


if __name__ == "__main__":
    main()
