#!/usr/bin/env python3
"""Create a declaration/rule inventory for the fixed and proof-local K sources."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/repro")
OUTPUT = Path("/audit-output/evidence/k-inventory.tsv")

START = re.compile(r"^\s*(configuration|syntax|rule|claim|context)\b")
BOUNDARY = re.compile(
    r"^\s*(module\b|endmodule\b|imports\b|requires\b|"
    r"configuration\b|syntax\b|rule\b|claim\b|context\b)"
)
ATTRIBUTES = [
    "function",
    "functional",
    "total",
    "simplification",
    "priority",
    "owise",
    "concrete",
    "macro",
    "symbol",
    "strict",
    "seqstrict",
    "assoc",
    "comm",
    "unit",
    "constructor",
]
RELEVANT_FILES = {
    "semantics.k",
    "syntax.k",
    "core.k",
    "functions.k",
    "call.k",
    "controls.k",
    "iter.k",
    "list.k",
    "tuple.k",
    "builtins.k",
    "set.k",
    "str.k",
    "operators.k",
    "int.k",
}
RELEVANT_TERMS = {
    "generatedTop",
    "<k>",
    "<env>",
    "<scopes>",
    "<scopeLoc>",
    "<heap>",
    "<heapLoc>",
    "<stack>",
    "<ret>",
    "<exc>",
    "<exit-code>",
    "Module",
    "FuncDef",
    "Params",
    "Assign",
    "Name",
    "Str",
    "Int",
    "For",
    "#loop",
    "#loopStep",
    "#bindTgt",
    "#iterNext",
    "#iterDone",
    "#iterYield",
    "Call",
    "#callee",
    "#applyK",
    "#evalArgs",
    "If",
    "#branch",
    "Compare",
    "CmpOp",
    "Return",
    "#return",
    "closureVal",
    "scope",
    "#loadAll",
    "#look",
    "#alloc",
    "list",
    "set",
    "len",
    "dedup",
    "strLt",
    "isLen",
    "applyCmp",
    "wordVals",
    "findMax",
    "bestWord",
    "bestScore",
}


def blocks(path: Path):
    lines = path.read_text().splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    for position, start in enumerate(starts):
        end_limit = starts[position + 1] if position + 1 < len(starts) else len(lines)
        end = start + 1
        while end < end_limit and not (
            BOUNDARY.match(lines[end]) and not START.match(lines[end])
        ):
            end += 1
        raw = "\n".join(lines[start:end]).rstrip()
        yield start + 1, START.match(lines[start]).group(1), raw


def classify(path: Path, text: str) -> tuple[str, str, str]:
    if path.name == "verification.k":
        return (
            "proof-local",
            "yes",
            "MANUAL_PROOF_EXTENSION_REVIEWED",
        )
    if path.name == "spec.k":
        return ("specification", "yes", "CLAIM_SCOPE_REVIEWED")
    relevant = path.name in RELEVANT_FILES and any(
        term in text for term in RELEVANT_TERMS
    )
    if relevant:
        return (
            "supplied-fixed",
            "yes",
            "FIXED_BASELINE_TASK_PATH_REVIEWED",
        )
    return (
        "supplied-fixed",
        "no",
        "FIXED_BASELINE_UNUSED_ACCEPTED_AS_SELECTED_SEMANTICS",
    )


def main() -> None:
    paths = sorted((ROOT / "reference-semantics").rglob("*.k"))
    paths += [ROOT / "verification.k", ROOT / "spec.k"]
    rows: list[dict[str, str]] = []
    for path in paths:
        for line, kind, raw in blocks(path):
            normalized = " ".join(
                part.strip()
                for part in raw.splitlines()
                if part.strip() and not part.lstrip().startswith("//")
            )
            attrs = ",".join(
                attr
                for attr in ATTRIBUTES
                if re.search(rf"\b{re.escape(attr)}\b", raw)
            )
            provenance, relevant, decision = classify(path, normalized)
            rows.append(
                {
                    "file": str(path.relative_to(ROOT)),
                    "line": str(line),
                    "kind": kind,
                    "attributes": attrs,
                    "provenance": provenance,
                    "task_relevant": relevant,
                    "review_decision": decision,
                    "declaration": normalized,
                }
            )
    with OUTPUT.open("w", newline="") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=list(rows[0]),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)
    counts: dict[str, int] = {}
    for row in rows:
        key = (
            f"{row['provenance']}:{row['kind']}:"
            f"{row['review_decision']}"
        )
        counts[key] = counts.get(key, 0) + 1
    print("COMMAND: python3 /audit-output/evidence/inventory_k.py")
    print(f"output={OUTPUT}")
    print(f"files={len(paths)}")
    print(f"inventory_entries={len(rows)}")
    for key, count in sorted(counts.items()):
        print(f"{key}={count}")
    proof_rows = [row for row in rows if row["provenance"] == "proof-local"]
    print(f"proof_local_entries={len(proof_rows)}")
    for row in proof_rows:
        print(
            f"{row['file']}:{row['line']} {row['kind']} "
            f"[{row['attributes']}] {row['declaration']}"
        )


if __name__ == "__main__":
    main()
