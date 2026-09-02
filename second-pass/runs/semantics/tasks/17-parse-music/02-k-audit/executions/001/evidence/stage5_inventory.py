#!/usr/bin/env python3
"""Produce a source-located inventory of every local K declaration and rule."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


SOURCES = sorted(Path("/reference/reference-semantics").rglob("*.k")) + [
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
]
OUTPUT = Path("/audit-output/evidence/stage5_rule_inventory.tsv")
SUMMARY = Path("/audit-output/evidence/stage5_rule_inventory_summary.txt")

START = re.compile(
    r"^\s*(requires|module|imports|configuration|syntax|context|rule|claim|endmodule)\b"
)
DECL = re.compile(r"^\s*(configuration|syntax|context|rule|claim)\b")
ATTR = re.compile(r"\[([^\]]+)\]")
KNOWN_ATTRIBUTE_MARKERS = (
    "function",
    "functional",
    "total",
    "simplification",
    "priority",
    "concrete",
    "owise",
    "macro",
    "macro-rec",
    "no-evaluators",
    "symbol",
    "strict",
    "seqstrict",
    "bracket",
    "token",
    "anywhere",
)

USED_SUPPLIED_FILES = {
    "syntax.k",
    "core.k",
    "iter.k",
    "str.k",
    "list.k",
    "methods.k",
    "controls.k",
    "functions.k",
    "operators.k",
    "call.k",
    "tuple.k",
}
WARNING_DECLARATIONS = {
    ("builtins.k", 134): "mapStrVS compiler non-exhaustiveness warning",
    ("float.k", 73): "floorFI compiler non-exhaustiveness warning",
    ("float.k", 86): "toF compiler non-exhaustiveness warning",
    ("float.k", 93): "ceilF compiler non-exhaustiveness warning",
    ("methods.k", 27): "joinCodes compiler non-exhaustiveness warning",
    ("subscript.k", 11): "valSeqAt compiler non-exhaustiveness warning",
}
CANDIDATE_DISPOSITIONS = {
    7: "ACCEPTED: finite valid-note data syntax.",
    15: "REJECTED: opaque result-bearing input constructor has no concrete-code equations.",
    19: "CONDITIONAL: abstract iterator is truthful only if connected to fixed split execution.",
    20: "ACCEPTED: empty iterator equation.",
    21: "ACCEPTED: whole-note iterator equation.",
    23: "ACCEPTED: half-note iterator equation.",
    25: "ACCEPTED: quarter-note iterator equation.",
    28: "REJECTED_UNSOUND: split bridge omits fixed allocation; valid input o witnesses heapLoc 2 versus proved 1.",
    33: "ACCEPTED: total constructor-complete descending musicAcc declaration.",
    34: "ACCEPTED: musicAcc empty equation.",
    35: "ACCEPTED: musicAcc whole equation.",
    37: "ACCEPTED: musicAcc half equation.",
    39: "ACCEPTED: musicAcc quarter equation.",
    43: "ACCEPTED: total constructor-complete descending musicLast declaration.",
    44: "ACCEPTED: musicLast empty equation.",
    45: "ACCEPTED: musicLast whole equation.",
    47: "ACCEPTED: musicLast half equation.",
    49: "ACCEPTED: musicLast quarter equation.",
    54: "ACCEPTED: loop-body macro declaration.",
    55: "ACCEPTED: exact loop-body macro expansion.",
    62: "ACCEPTED: function-body macro declaration.",
    63: "ACCEPTED: exact function-body macro expansion.",
    71: "ACCEPTED: closure macro declaration.",
    72: "ACCEPTED: exact closure macro expansion.",
    75: "ACCEPTED: program macro declaration.",
    76: "ACCEPTED: exact submitted-program macro expansion.",
    89: "EVIDENCE_GAP: separately proved exact loop summary is applied under arbitrary continuation; no false witness found.",
}


def compact(lines: list[str]) -> str:
    return " ".join(" ".join(line.strip().split()) for line in lines if line.strip())


rows: list[dict[str, str | int]] = []
for path in SOURCES:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    starts.append(len(lines))
    for position, start in enumerate(starts[:-1]):
        line = lines[start]
        match = START.match(line)
        assert match is not None
        raw_kind = match.group(1)
        if raw_kind not in {"configuration", "syntax", "context", "rule", "claim"}:
            continue
        end = starts[position + 1]
        block = lines[start:end]
        while len(block) > 1 and (
            not block[-1].strip() or block[-1].lstrip().startswith("//")
        ):
            block.pop()
        text = compact(block)
        attributes = ",".join(
            attribute.strip()
            for attribute_group in ATTR.findall(text)
            for attribute in attribute_group.split(",")
            if any(
                marker in attribute.strip()
                for marker in KNOWN_ATTRIBUTE_MARKERS
            )
        )

        if raw_kind == "syntax":
            if "macro-rec" in attributes:
                kind = "syntax-macro-rec"
            elif "macro" in attributes:
                kind = "syntax-macro"
            elif "function" in attributes:
                kind = "syntax-function"
            else:
                kind = "syntax"
            if "symbol(" in text or "no-evaluators" in text or "musicCodes(" in text:
                kind += "-opaque"
        elif raw_kind == "rule":
            if "simplification" in attributes:
                kind = "rule-simplification"
            elif "priority(" in attributes:
                kind = "rule-priority"
            elif "concrete" in attributes:
                kind = "rule-concrete"
            elif "owise" in attributes:
                kind = "rule-owise"
            else:
                kind = "rule-ordinary"
        else:
            kind = raw_kind

        source_class = (
            "candidate-proof"
            if path.parts[:2] == ("/", "candidate")
            else "trusted-supplied-semantics"
        )
        if source_class == "candidate-proof":
            if path.name == "spec.k":
                if start + 1 == 9:
                    reachability_scope = "candidate auxiliary claim"
                    review_disposition = "ACCEPTED_LOCALLY: satisfiable and freshly closes; constrains note and output list."
                else:
                    reachability_scope = "candidate entry claim"
                    review_disposition = "REJECTED_AS_REAL_PROGRAM_PROOF: closes only with rejected split bridge and false allocator state."
            else:
                reachability_scope = "candidate proof extension"
                review_disposition = CANDIDATE_DISPOSITIONS[start + 1]
        else:
            warning = WARNING_DECLARATIONS.get((path.name, start + 1))
            if warning is not None:
                reachability_scope = "supplied semantics, unreachable from submitted program"
                review_disposition = f"EVIDENCE_GAP_UNUSED: {warning}; cannot influence either claim."
            elif "opaque" in kind:
                reachability_scope = "supplied trust boundary, unreachable from submitted program"
                review_disposition = "ACCEPTED_UNUSED_BOUNDARY: opaque supplied symbol cannot influence this program or its proof helpers."
            elif path.name in USED_SUPPLIED_FILES:
                reachability_scope = "supplied semantics on or imported by used execution path"
                review_disposition = "ACCEPTED_SUPPLIED_USED_PATH: exact trusted baseline; checked for relevant overlap/state effects; no false witness found."
            else:
                reachability_scope = "supplied semantics for an unused construct"
                review_disposition = "ACCEPTED_NONCONTRIBUTING: exact trusted baseline and no submitted/proof term can invoke this entry."
        rows.append(
            {
                "id": len(rows) + 1,
                "source_class": source_class,
                "file": str(path),
                "start_line": start + 1,
                "end_line": start + len(block),
                "kind": kind,
                "attributes": attributes,
                "reachability_scope": reachability_scope,
                "review_disposition": review_disposition,
                "text": text,
            }
        )

with OUTPUT.open("w", encoding="utf-8", newline="") as stream:
    writer = csv.DictWriter(
        stream,
        fieldnames=[
            "id",
            "source_class",
            "file",
            "start_line",
            "end_line",
            "kind",
            "attributes",
            "reachability_scope",
            "review_disposition",
            "text",
        ],
        dialect="excel-tab",
    )
    writer.writeheader()
    writer.writerows(rows)

kind_counts = Counter(str(row["kind"]) for row in rows)
source_counts = Counter(str(row["source_class"]) for row in rows)
attribute_counts = Counter()
for row in rows:
    for attribute in str(row["attributes"]).split(","):
        if attribute:
            attribute_counts[attribute] += 1

summary_lines = [
    f"source files: {len(SOURCES)}",
    f"inventory entries: {len(rows)}",
    "",
    "by source class:",
    *(f"  {key}: {value}" for key, value in sorted(source_counts.items())),
    "",
    "by kind:",
    *(f"  {key}: {value}" for key, value in sorted(kind_counts.items())),
    "",
    "selected attributes:",
    *(
        f"  {key}: {value}"
        for key, value in sorted(attribute_counts.items())
        if any(
            marker in key
            for marker in (
                "function",
                "functional",
                "total",
                "simplification",
                "priority",
                "concrete",
                "owise",
                "macro",
                "no-evaluators",
                "symbol",
            )
        )
    ),
]
SUMMARY.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")
print("\n".join(summary_lines))
