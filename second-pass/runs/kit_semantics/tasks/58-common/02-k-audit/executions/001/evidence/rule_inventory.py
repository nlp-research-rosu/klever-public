#!/usr/bin/env python3
"""Exhaustive declaration inventory for the mounted K sources."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import re


ROOT = Path("/tmp/audit-work/58-common")
sources = [
    ROOT / "reference-semantics/semantics.k",
    *sorted((ROOT / "reference-semantics/semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]

start_pattern = re.compile(
    r"^(?:requires\s+\"|\s*(?:module|imports|configuration|syntax|context|rule|claim|endmodule)\b)"
)
kind_pattern = re.compile(
    r"^(?:(requires)\s+\"|\s*(module|imports|configuration|syntax|context|rule|claim|endmodule)\b)"
)

relevant_markers = (
    "#loadAll",
    "Stmts",
    "Name(",
    "builtinsScope",
    "#look",
    "#evalArgs",
    "#evalArgCont",
    "#applyK",
    "#alloc",
    "Int(",
    "appendVal",
    "vals2valSeq",
    "truthy",
    "applyCmp",
    "FuncDef",
    "#bindP",
    "Return",
    "#endcall",
    "#pop",
    "Call",
    "#callee",
    "closureVal",
    "Assign",
    "Expr(",
    "If(",
    "#branch",
    "For(",
    "#loop",
    "#bindTgt",
    "BoolOp",
    "Attribute",
    "toCall",
    "isMutMethod",
    "ListExpr",
    "toList",
    "valSeqConcat",
    '"append"',
    "Compare",
    "#memberAcc",
    "#memberCont",
    "#notB",
    "#iterNext",
    "#iterDone",
    "#iterYield",
    "sortVS",
    '"sorted"',
    "commonMember",
    "commonAcc",
    "commonLoopBody",
    "commonBody",
)

records: list[dict[str, object]] = []
for source in sources:
    lines = source.read_text(encoding="utf-8").splitlines()
    starts = [
        index
        for index, line in enumerate(lines)
        if start_pattern.match(line)
    ]
    for offset, start in enumerate(starts):
        end = starts[offset + 1] if offset + 1 < len(starts) else len(lines)
        block_lines = lines[start:end]
        while block_lines and (
            not block_lines[-1].strip()
            or block_lines[-1].lstrip().startswith("//")
        ):
            block_lines.pop()
        block = "\n".join(block_lines)
        match = kind_pattern.match(lines[start])
        assert match is not None
        kind = match.group(1) or match.group(2)
        attributes = [
            attribute
            for attribute in (
                "function",
                "functional",
                "total",
                "simplification",
                "concrete",
                "macro",
                "priority",
                "owise",
                "symbol",
                "no-evaluators",
                "strict",
                "seqstrict",
            )
            if re.search(rf"\b{re.escape(attribute)}\b", block)
        ]
        relative = source.relative_to(ROOT).as_posix()
        if relative == "verification.k":
            decision = "PROOF_LOCAL_MANUAL_REVIEW"
        elif relative == "spec.k":
            decision = "CLAIM_MANUAL_REVIEW"
        elif any(marker in block for marker in relevant_markers):
            decision = "FIXED_RELEVANT_REVIEWED"
        else:
            decision = "FIXED_UNUSED_OUTSIDE_DEPENDENCY_SLICE"
        records.append(
            {
                "path": relative,
                "line": start + 1,
                "kind": kind,
                "attributes": ",".join(attributes) or "-",
                "decision": decision,
                "text": " ".join(part.strip() for part in block.splitlines()),
            }
        )

print(f"source_file_count={len(sources)}")
print(f"record_count={len(records)}")
print(f"kind_counts={dict(sorted(Counter(str(r['kind']) for r in records).items()))}")
print(
    "decision_counts="
    f"{dict(sorted(Counter(str(r['decision']) for r in records).items()))}"
)
attribute_counts: Counter[str] = Counter()
for record in records:
    for attribute in str(record["attributes"]).split(","):
        if attribute != "-":
            attribute_counts[attribute] += 1
print(f"attribute_counts={dict(sorted(attribute_counts.items()))}")
print("id\tpath:line\tkind\tattributes\tdecision\tdeclaration")
for index, record in enumerate(records, 1):
    print(
        f"{index:04d}\t{record['path']}:{record['line']}\t"
        f"{record['kind']}\t{record['attributes']}\t"
        f"{record['decision']}\t{record['text']}"
    )
print("RULE_INVENTORY_COMPLETE")
