#!/usr/bin/env python3
"""Enumerate and classify every top-level K declaration/rule in the audit scope."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path


OUT = Path("/audit-output/evidence/stage5/rule-inventory.tsv")
SUMMARY = Path("/audit-output/evidence/stage5/inventory-summary.txt")

FILES = [
    Path("/reference/reference-semantics/semantics.k"),
    *sorted(Path("/reference/reference-semantics/semantics").glob("*.k")),
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
]

START = re.compile(
    r"^(?P<indent> {0,2})(?P<kind>"
    r"requires|module|imports|syntax|configuration|context|rule|claim|endmodule"
    r")\b"
)

# Exact fixed-semantics regions exercised by the symbolic function claim or its
# two helper claims.  Declarations spanning mixed used/unused alternatives are
# conservatively tagged used.
USED_LINES = {
    "semantics.k": [(34, 90)],
    "syntax.k": [(3, 62)],
    "core.k": [
        (3, 70),
        (117, 225),
    ],
    "iter.k": [(6, 9)],
    "tuple.k": [(31, 41)],
    "operators.k": [(6, 42)],
    "bool.k": [(16, 46)],
    "list.k": [(3, 20), (52, 68)],
    "controls.k": [(3, 18), (46, 75)],
    "functions.k": [(3, 20), (62, 91)],
    "call.k": [(10, 75)],
    "sort.k": [(10, 37)],
}


def line_is_used(path: Path, line: int) -> bool:
    return any(
        lo <= line <= hi for lo, hi in USED_LINES.get(path.name, [])
    )


def attributes(text: str) -> list[str]:
    code = "\n".join(line.split("//", 1)[0] for line in text.splitlines())
    attribute_text = " ".join(re.findall(r"\[([^\]]*)\]", code))
    found = []
    checks = [
        ("macro", r"(?<![-\w])macro(?![-\w])"),
        ("function", r"(?<![-\w])function(?![-\w])"),
        ("functional", r"(?<![-\w])functional(?![-\w])"),
        ("total", r"(?<![-\w])total(?![-\w])"),
        ("symbol", r"(?<![-\w])symbol\s*\("),
        ("no-evaluators", r"(?<![-\w])no-evaluators(?![-\w])"),
        ("priority", r"(?<![-\w])priority\s*\("),
        ("simplification", r"(?<![-\w])simplification(?![-\w])"),
        ("concrete", r"(?<![-\w])concrete(?![-\w])"),
        ("owise", r"(?<![-\w])owise(?![-\w])"),
        ("strict", r"(?<![-\w])strict(?![-\w])"),
        ("seqstrict", r"(?<![-\w])seqstrict(?![-\w])"),
    ]
    for name, pattern in checks:
        if re.search(pattern, attribute_text):
            found.append(name)
    return found


def disposition(path: Path, line: int, kind: str, attrs: list[str]) -> str:
    if path == Path("/candidate/verification.k"):
        if line in (8, 9, 20, 21, 27, 28):
            return "PROOF_LOCAL_EXACT_PROGRAM_MACRO_SOUND"
        return "PROOF_LOCAL_TERMINATING_MATH_DEFINITION_SOUND"
    if path == Path("/candidate/spec.k"):
        if kind == "claim":
            return "REACHABILITY_CLAIM_AUDITED_SOUND_AND_RESULT_CONSTRAINING"
        return "SPEC_ASSEMBLY_DECLARATION"

    if path.name == "list.k" and line in (63, 65):
        return "USED_MODELING_MISMATCH_PYTHON_CROSS_NUMERIC_EQUALITY_FALSE_WITNESS"
    if "no-evaluators" in attrs:
        if path.name == "sort.k" and line == 18:
            return "USED_EXTERNAL_TRUST_BOUNDARY_SORTVS"
        return "UNUSED_EXTERNAL_TRUST_BOUNDARY_INERT_FOR_THIS_PROGRAM"
    if "concrete" in attrs:
        if path.name == "sort.k" and 20 <= line <= 32:
            return "CONCRETE_VALIDATION_RULE_USED_FOR_GROUND_INT_SORT"
        return "CONCRETE_ONLY_RULE_INERT_FOR_SYMBOLIC_PROOF"
    if line_is_used(path, line):
        return "FIXED_SUPPLIED_SEMANTICS_USED_AND_REVIEWED_SOUND_ON_MATCH_DOMAIN"
    if kind in {"module", "endmodule", "imports", "requires", "syntax", "context",
                "configuration"}:
        return "FIXED_SUPPLIED_DECLARATION_OR_ASSEMBLY_INERT_OR_WELL_FORMED"
    return "FIXED_SUPPLIED_RULE_UNREACHABLE_FROM_SUBMITTED_PROGRAM"


rows = []
kind_counts: dict[str, int] = {}
attribute_counts: dict[str, int] = {}
disposition_counts: dict[str, int] = {}

for path in FILES:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = []
    for index, raw in enumerate(lines):
        match = START.match(raw)
        if match:
            starts.append((index, match.group("kind")))

    for position, (start_index, kind) in enumerate(starts):
        stop_index = (
            starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        )
        block_lines = lines[start_index:stop_index]
        while block_lines and (
            not block_lines[-1].strip()
            or block_lines[-1].lstrip().startswith("//")
        ):
            block_lines.pop()
        text = "\n".join(block_lines)
        attrs = attributes(text)
        disp = disposition(path, start_index + 1, kind, attrs)
        first_line = lines[start_index].strip()
        rows.append(
            {
                "id": f"K{len(rows) + 1:04d}",
                "file": str(path),
                "start_line": start_index + 1,
                "end_line": start_index + max(1, len(block_lines)),
                "kind": kind,
                "attributes": ",".join(attrs) if attrs else "-",
                "reachable_path": (
                    "yes"
                    if path == Path("/candidate/verification.k")
                    or path == Path("/candidate/spec.k")
                    or line_is_used(path, start_index + 1)
                    else "no"
                ),
                "disposition": disp,
                "first_line_json": json.dumps(first_line),
            }
        )
        kind_counts[kind] = kind_counts.get(kind, 0) + 1
        for attr in attrs:
            attribute_counts[attr] = attribute_counts.get(attr, 0) + 1
        disposition_counts[disp] = disposition_counts.get(disp, 0) + 1

with OUT.open("w", encoding="utf-8", newline="") as stream:
    writer = csv.DictWriter(
        stream,
        fieldnames=list(rows[0]),
        delimiter="\t",
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(rows)

with SUMMARY.open("w", encoding="utf-8") as stream:
    print(f"files={len(FILES)}", file=stream)
    print(f"records={len(rows)}", file=stream)
    print("kind_counts=" + json.dumps(kind_counts, sort_keys=True), file=stream)
    print(
        "attribute_counts=" + json.dumps(attribute_counts, sort_keys=True),
        file=stream,
    )
    print(
        "disposition_counts="
        + json.dumps(disposition_counts, sort_keys=True),
        file=stream,
    )
    print(
        "inventory_sha256_is_recorded_by_the_logged_shell_command", file=stream
    )

print(SUMMARY.read_text(encoding="utf-8"), end="")
