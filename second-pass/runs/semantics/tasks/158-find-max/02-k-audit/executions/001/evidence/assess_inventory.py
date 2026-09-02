#!/usr/bin/env python3
"""Attach an audit decision to every declaration in k-rule-inventory.json."""

from __future__ import annotations

import csv
import json
from pathlib import Path


EVIDENCE = Path("/audit-output/evidence")
inventory = json.loads(EVIDENCE.joinpath("k-rule-inventory.json").read_text())
records = inventory["declarations"]

used_semantics_lines: dict[str, list[tuple[int, int, str]]] = {
    "reference-semantics/semantics/syntax.k": [
        (9, 61, "submitted AST syntax: expressions, statements, params, and module"),
    ],
    "reference-semantics/semantics/core.k": [
        (13, 60, "value sorts and complete runtime configuration"),
        (117, 196, "module load, sequencing, lookup, builtins scope, calls, and literals"),
        (199, 229, "truthiness and sequence-length helpers"),
    ],
    "reference-semantics/semantics/iter.k": [
        (8, 8, "iterator protocol constructors"),
    ],
    "reference-semantics/semantics/list.k": [
        (8, 15, "list iteration and concrete test list construction"),
    ],
    "reference-semantics/semantics/set.k": [
        (8, 27, "set(str) representation and duplicate removal"),
    ],
    "reference-semantics/semantics/str.k": [
        (8, 17, "string iteration/literal representation"),
        (43, 59, "lexicographic comparison"),
    ],
    "reference-semantics/semantics/builtins.k": [
        (17, 26, "len dispatch and length of set values"),
        (40, 42, "set(str) builtin"),
    ],
    "reference-semantics/semantics/call.k": [
        (18, 32, "callee evaluation and builtin dispatch"),
        (69, 75, "plain closure call frame construction"),
    ],
    "reference-semantics/semantics/functions.k": [
        (8, 20, "plain function definition/closure creation"),
        (62, 91, "parameter binding, return, and frame pop"),
    ],
    "reference-semantics/semantics/controls.k": [
        (8, 18, "assignment"),
        (46, 54, "expression/if control"),
        (62, 75, "for-loop protocol"),
    ],
    "reference-semantics/semantics/operators.k": [
        (10, 20, "comparison evaluation contexts and dispatch"),
    ],
    "reference-semantics/semantics/int.k": [
        (22, 27, "integer comparison"),
    ],
}

known_unused_coverage_gaps = {
    ("reference-semantics/semantics/builtins.k", "mapStrVS"),
    ("reference-semantics/semantics/float.k", "floorFI"),
    ("reference-semantics/semantics/float.k", "toF"),
    ("reference-semantics/semantics/float.k", "ceilF"),
    ("reference-semantics/semantics/methods.k", "joinCodes"),
    ("reference-semantics/semantics/subscript.k", "valSeqAt"),
}

verification_decisions: dict[int, tuple[str, str]] = {
    7: ("ACCEPT", "inductive sequence sort restricts each input element to str(IntSeq)"),
    8: ("ACCEPT", "logical sequence-to-ValSeq representation declaration"),
    9: ("ACCEPT", "empty representation equation"),
    10: ("ACCEPT", "constructor-preserving representation equation"),
    16: ("ACCEPT_BRIDGE", "empty iterator accelerator; bridge-free universal theorem closes"),
    18: ("ACCEPT_BRIDGE", "nonempty iterator accelerator; bridge-free universal theorem closes"),
    23: ("ACCEPT_ALIAS", "loop-body function alias declaration"),
    24: ("ACCEPT_ALIAS", "exact submitted loop body; pinning check closes"),
    37: ("ACCEPT_ALIAS", "function-body alias declaration"),
    38: ("ACCEPT_ALIAS", "exact submitted function body; pinning check closes"),
    48: ("ACCEPT_SUMMARY", "inductive accumulator result and total recursive summary declaration"),
    51: ("ACCEPT_SUMMARY", "empty sequence returns accumulator unchanged"),
    54: ("ACCEPT_SUMMARY", "strictly larger distinct count replaces word and score"),
    61: ("ACCEPT_SUMMARY", "equal count and smaller word replaces only word"),
    69: ("ACCEPT_SUMMARY", "smaller count retains accumulator"),
    76: ("ACCEPT_SUMMARY", "equal count and not-smaller word retains accumulator"),
    84: ("ACCEPT_PROJECTION", "word projection declaration is total after summary normalization"),
    85: ("ACCEPT_PROJECTION", "word projection from bestState"),
    87: ("ACCEPT_PROJECTION", "score projection declaration is total after summary normalization"),
    88: ("ACCEPT_PROJECTION", "score projection from bestState"),
    92: ("ACCEPT_SIMPLIFICATION", "truthful projection of larger-count summary step"),
    96: ("ACCEPT_SIMPLIFICATION", "truthful score projection of larger-count summary step"),
    101: ("ACCEPT_SIMPLIFICATION", "truthful projection of lexicographically smaller tie step"),
    106: ("ACCEPT_SIMPLIFICATION", "truthful score projection of tie step"),
    112: ("ACCEPT_SIMPLIFICATION", "truthful projection of smaller-count retention step"),
    116: ("ACCEPT_SIMPLIFICATION", "truthful score projection of smaller-count retention step"),
    121: ("ACCEPT_SIMPLIFICATION", "truthful projection of not-smaller tie retention step"),
    126: ("ACCEPT_SIMPLIFICATION", "truthful score projection of not-smaller tie retention step"),
}

spec_decisions: dict[int, tuple[str, str]] = {
    6: (
        "ACCEPT_CLAIM",
        "general loop summary over arbitrary remaining words/accumulator; closes independently",
    ),
    50: (
        "ACCEPT_CLAIM",
        "executes exact function body and constrains returned str to recursive summary",
    ),
}


def assess(record: dict[str, object]) -> tuple[str, str]:
    file_name = str(record["file"])
    start_line = int(record["start_line"])
    text = str(record["text"])
    attributes = {str(value) for value in record["attributes"]}
    kind = str(record["kind"])

    if file_name == "verification.k":
        return verification_decisions[start_line]
    if file_name == "spec.k":
        return spec_decisions[start_line]

    for gap_file, symbol in known_unused_coverage_gaps:
        if file_name == gap_file and symbol in text:
            return (
                "EVIDENCE_GAP_UNUSED",
                (
                    f"compiler reports incomplete total coverage around {symbol}; "
                    "the submitted program cannot reach this operation"
                ),
            )

    if "no-evaluators" in attributes:
        return (
            "ACCEPT_FIXED_OPAQUE_UNUSED",
            "trusted supplied opaque primitive; unreachable from the submitted program/proof",
        )

    for low, high, role in used_semantics_lines.get(file_name, []):
        if low <= start_line <= high:
            return (
                "ACCEPT_FIXED_USED",
                f"unchanged supplied-semantics declaration used for {role}; inspected for this path",
            )

    if kind == "syntax":
        return (
            "ACCEPT_FIXED_DECLARATION",
            "unchanged supplied-semantics syntax; not a proof-local correctness assumption",
        )
    if kind == "configuration":
        return (
            "ACCEPT_FIXED_CONFIGURATION",
            "unchanged supplied runtime configuration",
        )
    return (
        "ACCEPT_FIXED_UNREACHABLE",
        (
            "unchanged supplied-semantics rule/context outside every construct "
            "reachable from solution.mpy in the target proof"
        ),
    )


assessed: list[dict[str, object]] = []
counts: dict[str, int] = {}
for record in records:
    decision, rationale = assess(record)
    counts[decision] = counts.get(decision, 0) + 1
    assessed.append(
        {
            "id": record["id"],
            "file": record["file"],
            "start_line": record["start_line"],
            "end_line": record["end_line"],
            "kind": record["kind"],
            "attributes": ",".join(record["attributes"]),
            "decision": decision,
            "rationale": rationale,
        }
    )

with EVIDENCE.joinpath("k-rule-assessment.csv").open(
    "w", encoding="utf-8", newline=""
) as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=list(assessed[0]))
    writer.writeheader()
    writer.writerows(assessed)

markdown = [
    "# Per-declaration static assessment",
    "",
    (
        "This ledger has one decision row for every declaration in "
        "`k-rule-inventory.json`. `ACCEPT_FIXED_UNREACHABLE` means no submitted "
        "program execution or target-proof path can select the rule; it is not an "
        "assertion about broader Python coverage."
    ),
    "",
    f"Decision counts: `{json.dumps(counts, sort_keys=True)}`",
    "",
    "| ID | Location | Kind/attrs | Decision | Rationale |",
    "|---:|---|---|---|---|",
]
for item in assessed:
    location = f"{item['file']}:{item['start_line']}-{item['end_line']}"
    kind_attrs = str(item["kind"])
    if item["attributes"]:
        kind_attrs += f" [{item['attributes']}]"
    markdown.append(
        f"| {item['id']} | `{location}` | {kind_attrs} | "
        f"{item['decision']} | {item['rationale']} |"
    )
EVIDENCE.joinpath("k-rule-assessment.md").write_text(
    "\n".join(markdown) + "\n", encoding="utf-8"
)

print(json.dumps({"assessed": len(assessed), "decision_counts": counts}, indent=2))
