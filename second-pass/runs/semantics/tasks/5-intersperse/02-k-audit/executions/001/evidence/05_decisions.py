#!/usr/bin/env python3
"""One assessment row for every inventoried K declaration anchor."""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path


ROOT = Path("/tmp/audit-work/candidate")
FILES = sorted((ROOT / "reference-semantics").rglob("*.k"))
FILES.append(ROOT / "verification.k")
ANCHOR = re.compile(
    r"^\s*(configuration\b|syntax\b|rule\b|claim\b|context\b|context\s+alias\b)"
)

# Exact fixed-semantics anchors exercised by, or needed to resolve overlaps on,
# the submitted program's path. All other fixed anchors are unreachable from
# this AST/control state and are retained in the ledger as F-UNREACHED.
USED: dict[str, set[int]] = {
    "reference-semantics/semantics/syntax.k": {
        9, 37, 41, 56, 57, 60, 61,
    },
    "reference-semantics/semantics/core.k": {
        14, 18, 25, 36, 37, 38, 39, 40, 41, 42, 49,
        117, 118, 124, 125, 126, 127, 130, 131, 132,
        157, 158, 185, 186, 189, 190, 191, 199, 204,
        213, 214, 215, 217, 218, 219,
    },
    "reference-semantics/semantics/iter.k": {8},
    "reference-semantics/semantics/controls.k": {
        9, 36, 48, 51, 52, 53, 54, 65, 69, 71, 72, 73, 85, 95,
    },
    "reference-semantics/semantics/functions.k": {
        8, 14, 63, 64, 78, 85,
    },
    "reference-semantics/semantics/list.k": {
        9, 10, 13, 14, 15, 18, 19, 20, 53,
    },
    "reference-semantics/semantics/call.k": {
        16, 19, 20, 21, 24, 52, 53, 56, 69,
    },
    "reference-semantics/semantics/tuple.k": {31, 32, 35},
}


writer = csv.writer(sys.stdout)
writer.writerow(("file", "line", "kind", "assessment", "basis", "source_head"))
counts: dict[str, int] = {}

for path in FILES:
    rel = str(path.relative_to(ROOT))
    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        match = ANCHOR.match(line)
        if not match:
            continue
        kind = match.group(1).split()[0]
        if rel == "verification.k":
            assessment = "P-MATH"
            basis = (
                "Proof-local declaration/equation; disjoint/exhaustive and "
                "structurally recursive as detailed in 05_static_assessment.md."
            )
        elif line_number in USED.get(rel, set()):
            assessment = "F-USED"
            basis = (
                "Selected supplied-semantics declaration on the submitted "
                "execution path or needed for an applicable overlap/priority check."
            )
        else:
            assessment = "F-UNREACHED"
            basis = (
                "Part of the selected fixed semantics but unreachable from this "
                "program AST and entry state; no target claim depends on it."
            )
        counts[assessment] = counts.get(assessment, 0) + 1
        writer.writerow(
            (rel, line_number, kind, assessment, basis, line.strip())
        )

print("# counts=" + ",".join(f"{key}:{counts[key]}" for key in sorted(counts)), file=sys.stderr)
