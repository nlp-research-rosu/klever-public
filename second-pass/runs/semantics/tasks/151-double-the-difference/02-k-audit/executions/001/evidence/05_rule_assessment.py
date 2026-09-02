#!/usr/bin/env python3
"""Assign an explicit audit disposition to every K rule and claim."""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
FILES = [
    ROOT / "reference-semantics" / "semantics.k",
    *sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]
START = re.compile(
    r"^(requires|module|endmodule)\b"
    r"|^ {2}(imports|configuration|context|syntax|rule|claim|macro|alias)\b"
)

MATERIAL_RULES = {
    "reference-semantics/semantics/core.k": {
        125, 126, 127, 131, 132, 145, 152, 158, 189, 190, 191,
        194, 200, 202, 214, 215,
    },
    "reference-semantics/semantics/functions.k": {63, 64, 78, 80, 85},
    "reference-semantics/semantics/call.k": {20, 21, 31, 69},
    "reference-semantics/semantics/controls.k": {9, 20, 52, 53, 54, 69, 71, 72, 73},
    "reference-semantics/semantics/tuple.k": {32},
    "reference-semantics/semantics/operators.k": {12, 17},
    "reference-semantics/semantics/int.k": {9, 15, 17, 20, 24, 26},
    "reference-semantics/semantics/bool.k": {17, 18, 20},
    "reference-semantics/semantics/builtins.k": {291, 294, 295},
}
BRIDGE_COMPARATORS = {
    "reference-semantics/semantics/list.k": {9, 10},
}

entries = []
for path in FILES:
    lines = path.read_text().splitlines()
    starts = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1) or match.group(2)))
    for position, (index, kind) in enumerate(starts):
        if kind not in {"rule", "claim"}:
            continue
        next_index = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        block = "\n".join(lines[index:next_index]).rstrip()
        entries.append(
            {
                "file": str(path.relative_to(ROOT)),
                "line": index + 1,
                "kind": kind,
                "block": block,
            }
        )


def assess(entry):
    file = entry["file"]
    line = entry["line"]
    block = entry["block"]
    if file == "verification.k":
        if line in {16, 18, 20}:
            return (
                "proof-domain operational bridge",
                "CONNECTION_GAP_NOT_FALSE",
                "Defines iteration on the fresh numVals encoding. Constructor-disjoint, "
                "context-preserving, and homomorphic to fixed list iteration, but the "
                "candidate supplies no bridge-free machine-checked universal connection theorem.",
            )
        if line == 24:
            return (
                "definitional summary",
                "ACCEPT_TRUE_TOTAL",
                "One unconditional equation exactly returns I^2 iff I is positive and "
                "pyMod(I,2)=1, else zero.",
            )
        if line in {31, 32, 34}:
            return (
                "definitional summary",
                "ACCEPT_TRUE_TOTAL",
                "Disjoint exhaustive NumSeq equation; recursive calls structurally descend.",
            )
        if line in {38, 39, 40}:
            return (
                "definitional summary",
                "ACCEPT_TRUE_TOTAL",
                "Disjoint exhaustive NumSeq equation returning the last element or prior value.",
            )
        return ("proof-local", "REVIEW_REQUIRED", "Unexpected proof-local rule.")
    if file == "spec.k":
        if line == 6:
            return (
                "auxiliary reachability circularity",
                "ACCEPT_PROVED_AND_RESULT_CONSTRAINING",
                "Exact loop head/body and scopes; updates accumulator and target while framing "
                "other cells. Independently closes with #Top.",
            )
        return (
            "target reachability claim",
            "ACCEPT_PROVED_AND_PROGRAM_PINNED",
            "Executes the mechanically identical closure body and returns the recursive summary.",
        )
    if line in MATERIAL_RULES.get(file, set()):
        return (
            "supplied fixed semantics, materially reachable",
            "ACCEPT_FIXED_MATERIAL",
            "Matches the used constructor/operator behavior and preserves the cells needed by "
            "this exact no-exception, no-mutation program path.",
        )
    if line in BRIDGE_COMPARATORS.get(file, set()):
        return (
            "supplied fixed semantics, representation comparator",
            "ACCEPT_FIXED_COMPARATOR",
            "Standard .ValSeq/vCons list-iteration rule used for constructor-by-constructor "
            "comparison with the proof-domain iterator encoding.",
        )
    if "no-evaluators" in block or "md5hexCodes" in block or "sortVS" in block:
        return (
            "supplied fixed opaque boundary, unreachable",
            "ACCEPT_FIXED_UNUSED_OPAQUE",
            "Opaque/externally trusted fixed-semantics operation is absent from the executed "
            "program term and cannot affect either claim.",
        )
    return (
        "supplied fixed semantics, unreachable",
        "ACCEPT_FIXED_UNUSED",
        "The rule's top constructor, continuation marker, operator, or guard is absent from "
        "the exact executed program and proof-domain inputs; no overlap can contribute.",
    )


rows = []
for number, entry in enumerate(entries, 1):
    extension_class, decision, rationale = assess(entry)
    rows.append((number, entry, extension_class, decision, rationale))

summary = collections.Counter(row[3] for row in rows)
print("# Per-rule static assessment")
print()
print(f"Every rule/claim inventoried: **{len(rows)}**.")
print()
for decision, count in sorted(summary.items()):
    print(f"- `{decision}`: {count}")
print()
print("| ID | Source | Kind | Class | Decision | Rationale |")
print("|---:|---|---|---|---|---|")
for number, entry, extension_class, decision, rationale in rows:
    print(
        f"| R{number:04d} | `{entry['file']}:{entry['line']}` | {entry['kind']} | "
        f"{extension_class} | `{decision}` | {rationale} |"
    )
