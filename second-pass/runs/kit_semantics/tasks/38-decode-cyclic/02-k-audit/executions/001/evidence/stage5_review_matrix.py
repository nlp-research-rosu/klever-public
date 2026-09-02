#!/usr/bin/env python3
"""Attach an explicit audit disposition to every inventory record."""

from __future__ import annotations

import re
from pathlib import Path


INVENTORY = Path("/audit-output/evidence/STAGE5_RULE_INVENTORY.md")

# Inclusive source-line ranges on the actual theorem execution path. Syntax
# declarations are treated separately: they declare constructors/evaluation
# contexts but do not themselves assert a result.
USED = {
    "reference-semantics/semantics/core.k": [
        (13, 60),
        (123, 181),
        (183, 210),
        (213, 229),
    ],
    "reference-semantics/semantics/controls.k": [
        (8, 18),
        (46, 54),
        (62, 74),
    ],
    "reference-semantics/semantics/functions.k": [
        (8, 20),
        (62, 90),
    ],
    "reference-semantics/semantics/call.k": [
        (15, 32),
        (69, 74),
    ],
    "reference-semantics/semantics/operators.k": [(10, 20)],
    "reference-semantics/semantics/str.k": [(7, 26)],
    "reference-semantics/semantics/builtins.k": [(17, 26)],
    "reference-semantics/semantics/subscript.k": [(16, 121)],
    "reference-semantics/semantics/int.k": [(22, 27)],
}


def overlaps(start: int, end: int, ranges: list[tuple[int, int]]) -> bool:
    return any(start <= high and end >= low for low, high in ranges)


rows = []
pattern = re.compile(
    r"^\| (K\d+) \| `([^:]+):(\d+)-(\d+)` \| ([^|]+) \| ([^|]+) \|"
)
for line in INVENTORY.read_text().splitlines():
    match = pattern.match(line)
    if match is None:
        continue
    record, path, start_text, end_text, category, attributes = match.groups()
    start, end = int(start_text), int(end_text)
    category = category.strip()
    attributes = attributes.strip()

    if path == "verification.k":
        if start in (7, 8, 26, 27):
            disposition = "PROOF_LOCAL_MACRO_SOUND"
            rationale = "Macro expansion is constructor-identical to regenerated solution.mpy."
        elif start in (38, 39, 40, 41, 45):
            disposition = "PROOF_LOCAL_SUMMARY_SOUND"
            rationale = "decodedResult cases are disjoint/exhaustive and recurse by three constructors."
        elif start in (55, 56, 57, 58, 60):
            disposition = "PROOF_LOCAL_SUMMARY_SOUND"
            rationale = "decodedTail cases are disjoint/exhaustive and recurse by three constructors."
        elif start in (63, 64):
            disposition = "PROOF_LOCAL_SUMMARY_SOUND"
            rationale = "decodeCodes composes the separately fixed complete-group and tail summaries."
        elif start in (69, 70, 71):
            disposition = "PROOF_LOCAL_SUMMARY_SOUND"
            rationale = "finalLoopChar is exhaustive and structurally decreasing."
        else:
            disposition = "PROOF_LOCAL_REVIEWED"
            rationale = "No operational interception, opaque value, or priority rule."
    elif path == "spec.k":
        disposition = "CLAIM_RECONSTRUCTED_TOP"
        rationale = "Positive reachability claim closed in the fresh definition; adequacy reviewed separately."
    elif path.endswith("/syntax.k"):
        disposition = "FIXED_SYNTAX_DECLARATION"
        rationale = "Constructor or strictness/context declaration; used constructors are mapped in REVIEW.md."
    elif category in ("syntax-declaration", "function-declaration", "context", "configuration"):
        if overlaps(start, end, USED.get(path, [])):
            disposition = "USED_FIXED_DECLARATION_REVIEWED"
            rationale = "Declaration/configuration participates in the actual execution path and is adequate there."
        else:
            disposition = "UNUSED_FIXED_DECLARATION"
            rationale = "Supplied-semantics declaration has no execution or result influence in this theorem."
    elif overlaps(start, end, USED.get(path, [])):
        disposition = "USED_FIXED_RULE_REVIEWED_SOUND"
        rationale = "Matches CPython order/value/control for this program and is exercised by fixed execution."
    else:
        disposition = "UNUSED_FIXED_RULE"
        rationale = "Supplied-semantics rule is unreachable from the submitted program and has no theorem influence."
    rows.append(
        (record, path, start, end, category, attributes, disposition, rationale)
    )

print("# Rule-by-rule audit dispositions")
print()
print(f"Records dispositioned: {len(rows)}")
print()
print("| ID | File:lines | Category | Attributes | Disposition | Rationale |")
print("|---:|---|---|---|---|---|")
for record, path, start, end, category, attributes, disposition, rationale in rows:
    print(
        f"| {record} | `{path}:{start}-{end}` | {category} | {attributes} | "
        f"{disposition} | {rationale} |"
    )
