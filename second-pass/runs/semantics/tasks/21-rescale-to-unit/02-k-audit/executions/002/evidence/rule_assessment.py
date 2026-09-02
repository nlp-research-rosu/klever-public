#!/usr/bin/env python3
"""Attach an audit disposition to every record in rule_inventory.md."""

from __future__ import annotations

import re
from pathlib import Path


inventory = Path("/audit-output/evidence/rule_inventory.md").read_text().splitlines()
file_name = ""
records: list[tuple[str, int, str, str]] = []
for line in inventory:
    file_match = re.fullmatch(r"## `([^`]+)`", line)
    if file_match:
        file_name = file_match.group(1)
        continue
    record_match = re.fullmatch(
        r"### (\S+) at line (\d+) \(attributes: (.*)\)", line
    )
    if record_match:
        records.append(
            (
                file_name,
                int(record_match.group(2)),
                record_match.group(1),
                record_match.group(3),
            )
        )

material_fixed = {
    "reference-semantics/semantics/syntax.k",
    "reference-semantics/semantics/core.k",
    "reference-semantics/semantics/iter.k",
    "reference-semantics/semantics/operators.k",
    "reference-semantics/semantics/float.k",
    "reference-semantics/semantics/list.k",
    "reference-semantics/semantics/comprehension.k",
    "reference-semantics/semantics/controls.k",
    "reference-semantics/semantics/functions.k",
    "reference-semantics/semantics/builtins.k",
    "reference-semantics/semantics/call.k",
}

verification_assessment = {
    9: (
        "REJECT_RESULT_ORACLE",
        "minVF/maxVF are total opaque program-derived extrema with no equations or bridge-free connection theorem.",
    ),
    12: (
        "REJECT_OPERATIONAL_BRIDGE",
        "Priority min interception replaces the fixed fold by unconstrained minVF over every ValSeq; the result affects the final postcondition.",
    ),
    15: (
        "REJECT_OPERATIONAL_BRIDGE",
        "Priority max interception replaces the fixed fold by unconstrained maxVF over every ValSeq; the result affects the final postcondition.",
    ),
    21: (
        "LIMITED_HELPER",
        "asFloat is declared total on Val but has only a Float equation; safe only because the target precondition establishes Float elements.",
    ),
    22: ("ACCEPT_LOCAL_EQUATION", "Identity on the Float subsort."),
    24: ("ACCEPT_LOCAL_DEFINITION", "Names the exact subF/divF expression."),
    25: ("ACCEPT_LOCAL_EQUATION", "Truthful definition of scaleF."),
    28: (
        "ACCEPT_LOCAL_DEFINITION",
        "Accumulator is structurally recursive over ValSeq.",
    ),
    29: ("ACCEPT_LOCAL_EQUATION", "Disjoint empty-tail base case."),
    30: (
        "ACCEPT_LOCAL_EQUATION",
        "Disjoint cons case, recurses on REST and appends one mapped element.",
    ),
    37: (
        "ACCEPT_LOCAL_DEFINITION",
        "Total structural Float-domain predicate.",
    ),
    38: ("ACCEPT_LOCAL_EQUATION", "Empty sequence is all-float."),
    39: (
        "ACCEPT_LOCAL_EQUATION",
        "Cons case combines isFloat(head) with recursive tail predicate.",
    ),
    44: ("ACCEPT_UNUSED_SYNTAX", "Sort-safe Float sequence syntax; unused by SPEC."),
    45: (
        "ACCEPT_UNUSED_HELPER",
        "Total injection helper; unused by SPEC.",
    ),
    46: ("ACCEPT_UNUSED_EQUATION", "Empty injection case; unused by SPEC."),
    47: ("ACCEPT_UNUSED_EQUATION", "Cons injection case; unused by SPEC."),
    54: (
        "UNJUSTIFIED_OPERATIONAL_BRIDGE",
        "Exact-expression comprehension summary has no bridge-free universal connection theorem and accepts an arbitrary continuation; no independent false-result witness was established, so this is recorded as an evidence gap rather than separately called false.",
    ),
    85: ("ACCEPT_OBSERVER_SYNTAX", "Proof-only observer marker."),
    86: (
        "ACCEPT_OBSERVER_RULE",
        "Reads the value stored at the returned list reference; exact heap match.",
    ),
    91: ("ACCEPT_WRAPPER_SYNTAX", "Proof-only program-entry wrapper."),
    92: (
        "ACCEPT_PROGRAM_WRAPPER",
        "Expands to the mechanically verified constructor-identical submitted module, call, and observer without altering other cells.",
    ),
}

output = Path("/audit-output/evidence/rule_assessment.tsv")
counts: dict[str, int] = {}
with output.open("w") as stream:
    stream.write("file\tline\tkind\tattributes\tstatus\trationale\n")
    for file_name, line, kind, attrs in records:
        if file_name.startswith("reference-semantics/"):
            if file_name in material_fixed:
                status = "ACCEPT_TRUSTED_FIXED_MATERIAL"
                rationale = (
                    "Launcher-trusted supplied-semantics declaration; byte-identical "
                    "to the mounted baseline and included in the material execution-path review."
                )
            else:
                status = "ACCEPT_TRUSTED_FIXED_UNUSED"
                rationale = (
                    "Launcher-trusted supplied-semantics declaration; byte-identical "
                    "to the baseline and unreachable from the submitted program."
                )
        elif file_name == "verification.k":
            status, rationale = verification_assessment[line]
        elif file_name == "spec.k":
            status = "REJECT_TARGET_ADEQUACY"
            rationale = (
                "Satisfiable and result-constraining only in terms of the same "
                "unconnected minVF/maxVF symbols introduced by operational bridges."
            )
        else:
            status = "UNCLASSIFIED"
            rationale = "Unexpected inventory source."
        counts[status] = counts.get(status, 0) + 1
        stream.write(
            f"{file_name}\t{line}\t{kind}\t{attrs}\t{status}\t{rationale}\n"
        )

print(f"assessment={output}")
print(f"records={len(records)}")
for status, count in sorted(counts.items()):
    print(f"{status}={count}")
unclassified = counts.get("UNCLASSIFIED", 0)
raise SystemExit(1 if unclassified or len(records) != 951 else 0)
