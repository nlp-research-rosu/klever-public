#!/usr/bin/env python3
"""Emit an exhaustive, line-addressed K declaration/rule inventory.

Every top-level configuration, syntax declaration, context, rule, and claim in
the supplied semantics, candidate verification module, and candidate spec is
listed.  Multi-line declarations are normalized to one TSV line without
discarding their guards, cells, or attributes.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/run-118")
files = [ROOT / "reference-semantics" / "semantics.k"]
files += sorted((ROOT / "reference-semantics" / "semantics").glob("*.k"))
files += [ROOT / "verification.k", ROOT / "spec.k"]

start_re = re.compile(r"^\s*(configuration|syntax|context|rule|claim)\b")
attr_re = re.compile(r"\[([^\]]+)\]")
attribute_word_re = re.compile(
    r"\b(function|functional|total|simplification|priority|concrete|"
    r"no-evaluators|symbol|macro|macro-rec|strict|seqstrict|owise)\b"
)
used_tokens = {
    "Module", "FuncDef", "Params", "If", "Compare", "Call", "Name", "Int",
    "Return", "Str", "Assign", "Subscript", "Slice", "NoBound", "BoolOp",
    "#applyK", "closureVal", "#bindP", "#pop", "truthy", "applyCmp",
    "strContains", "strToCodes", "isLen", "seqLen", "builtinsScope",
}


def decision(path: Path, line: int, kind: str, text: str) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith("reference-semantics/"):
        if kind == "syntax":
            return "ACCEPT_FIXED_BASELINE_DECLARATION"
        if kind == "configuration":
            return "ACCEPT_FIXED_BASELINE_CONFIGURATION"
        if kind == "context":
            return "ACCEPT_FIXED_BASELINE_EVALUATION_CONTEXT"
        return "ACCEPT_FIXED_BASELINE_RULE"
    if rel == "spec.k":
        return "TARGET_REACHABILITY_CLAIM"
    if rel == "verification.k":
        if kind == "syntax":
            return "ACCEPT_PROOF_LOCAL_DECLARATION"
        if line == 8:
            return "ACCEPT_EXACT_PROGRAM_BODY_MACRO"
        if line in {34, 41}:
            return "ACCEPT_TRUTHFUL_MATHEMATICAL_EQUATION"
        if line in {50, 52, 53, 54, 55, 58, 62}:
            return "ACCEPT_TRUTHFUL_RECURSIVE_SPECIFICATION_EQUATION"
        if line == 69:
            return "ACCEPT_DERIVABLE_SLICE_BRIDGE_CONNECTION_NOT_SUBMITTED"
        if line == 75:
            return "ACCEPT_VOWEL_CODE_MACRO"
        if line == 80:
            return "ACCEPT_DERIVED_STRING_MEMBERSHIP_EQUATION"
        if line == 87:
            return "REJECT_CIRCULAR_RESULT_BEARING_OPERATIONAL_AXIOM"
        if line in {97, 98, 99}:
            return "ACCEPT_STRUCTURAL_LENGTH_ARITHMETIC_SIMPLIFICATION"
        if line == 105:
            return "ACCEPT_FRESH_MAP_UPDATE_NORMALIZATION"
        return "REVIEW_PROOF_LOCAL_DECLARATION"
    return "UNCLASSIFIED"


rows = []
for path in files:
    lines = path.read_text().splitlines()
    starts = []
    for index, line_text in enumerate(lines):
        match = start_re.match(line_text)
        if match:
            starts.append((index, match.group(1)))
    for pos, (index, kind) in enumerate(starts):
        next_index = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
        block_lines = []
        for block_line in lines[index:next_index]:
            if block_line.strip() == "endmodule":
                break
            if block_line.lstrip().startswith("//"):
                continue
            block_lines.append(block_line.strip())
        normalized = " ".join(part for part in block_lines if part)
        normalized = re.sub(r"\s+", " ", normalized)
        attrs = ",".join(
            re.sub(r"\s+", " ", value.strip())
            for value in attr_re.findall(normalized)
            if attribute_word_re.search(value)
        )
        relevance = "USED_PATH" if any(token in normalized for token in used_tokens) else "UNUSED_PATH"
        rows.append(
            {
                "id": f"K{len(rows) + 1:04d}",
                "file": path.relative_to(ROOT).as_posix(),
                "line": index + 1,
                "kind": kind,
                "attributes": attrs,
                "program_relevance": relevance,
                "decision": decision(path, index + 1, kind, normalized),
                "declaration": normalized,
            }
        )

writer = csv.DictWriter(
    __import__("sys").stdout,
    fieldnames=[
        "id", "file", "line", "kind", "attributes",
        "program_relevance", "decision", "declaration",
    ],
    dialect="excel-tab",
    lineterminator="\n",
)
writer.writeheader()
writer.writerows(rows)
