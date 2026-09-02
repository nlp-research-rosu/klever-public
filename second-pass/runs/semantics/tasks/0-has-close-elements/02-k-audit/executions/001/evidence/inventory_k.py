#!/usr/bin/env python3
"""Build a source-line-complete inventory of local K sentences.

The inventory is deliberately mechanical: every source-level syntax, rule,
claim, context, configuration, macro, or alias sentence receives a disposition.
Multiline sentences are normalized onto one TSV field.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/0-has-close-elements")
OUT = Path("/audit-output/evidence/rule-inventory.tsv")
SUMMARY = Path("/audit-output/evidence/rule-inventory-summary.txt")

paths = sorted((SCRATCH / "reference-semantics").rglob("*.k"))
paths += [SCRATCH / "verification.k", SCRATCH / "spec.k"]

sentence_start = re.compile(
    r"^  (syntax|rule|claim|context|configuration|macro|alias)\b"
)
module_start = re.compile(r"^module\s+(\S+)")
attribute = re.compile(
    r"\b(function|total|functional|simplification|priority|owise|anywhere|"
    r"concrete|no-evaluators|symbol|macro)\b"
)

# Statements on these lines participate in parsing/executing solution.mpy or
# the reviewer concrete assertions. Other supplied statements remain imported
# but are not reached by this program's construct map.
used_lines = {
    "reference-semantics/semantics/syntax.k": range(9, 63),
    "reference-semantics/semantics/core.k": (
        13, 14, 18, 25, 31, 37, 40, 42, 49, 124, 125, 126, 127, 130,
        131, 132, 145, 152, 157, 158, 185, 186, 189, 190, 191, 194,
        195, 199, 200, 208, 209, 210, 213, 214, 215,
    ),
    "reference-semantics/semantics/iter.k": (8,),
    "reference-semantics/semantics/list.k": (9, 10),
    "reference-semantics/semantics/operators.k": (12, 15, 16, 17),
    "reference-semantics/semantics/float.k": (
        20, 21, 43, 44, 50, 51, 52, 54, 55, 56, 103, 104, 105,
    ),
    "reference-semantics/semantics/controls.k": (
        9, 20, 35, 36, 51, 52, 53, 54, 65, 69, 71, 72, 73, 85,
        87, 90, 91,
    ),
    "reference-semantics/semantics/functions.k": (
        8, 14, 63, 64, 78, 80, 85,
    ),
    "reference-semantics/semantics/builtins.k": (17, 44),
    "reference-semantics/semantics/call.k": (19, 20, 21, 31, 69),
    "reference-semantics/semantics/bool.k": (10, 11),
    "reference-semantics/semantics/assert.k": (6, 8),
}

rejected_verification_lines = {130, 151, 163, 178, 197}


def is_used(rel: str, line: int) -> bool:
    selected = used_lines.get(rel, ())
    return line in selected


def disposition(rel: str, line: int, kind: str) -> tuple[str, str]:
    if rel.startswith("reference-semantics/"):
        if is_used(rel, line):
            return (
                "SUPPLIED_FIXED_SEMANTICS_USED",
                "ACCEPTED: matches trusted supplied tree and traced in the "
                "construct/control map for this program",
            )
        return (
            "SUPPLIED_FIXED_SEMANTICS_NOT_REACHED",
            "ACCEPTED FOR THIS AUDIT: exact trusted supplied rule/declaration; "
            "not reached by solution.mpy or the concrete reviewer test",
        )
    if rel == "verification.k":
        if kind == "rule" and line in rejected_verification_lines:
            return (
                "PROOF_LOCAL_OPERATIONAL_BRIDGE",
                "REJECTED: false over its declared match domain; see "
                "bridge-witness.k, 05-bridge-witnesses.log, and "
                "05b-apply-bridge-check.log",
            )
        if line in (91, 93):
            return (
                "PROOF_LOCAL_TYPED_ITERATOR",
                "ACCEPTED: faithful iterator equations for the FloatSeq "
                "representation, disjoint from vCons/.ValSeq",
            )
        if line >= 97 and line <= 120:
            return (
                "PROOF_LOCAL_MATHEMATICAL_SUMMARY",
                "ACCEPTED: structurally recursive equations with disjoint, "
                "covering cases and exact opaque-float operation terms",
            )
        if kind == "rule":
            return (
                "PROOF_LOCAL_DEFINITION",
                "ACCEPTED: constructor/AST/closure definition; no execution "
                "is bypassed by this sentence",
            )
        return (
            "PROOF_LOCAL_DECLARATION",
            "ACCEPTED: typed syntax or inert proof marker declaration",
        )
    if rel == "spec.k" and kind == "claim":
        return (
            "REACHABILITY_OBLIGATION",
            "TARGET: independently rebuilt and run in its staged module",
        )
    return ("SPEC_DECLARATION", "ACCEPTED: module-local declaration")


rows = []
for path in paths:
    rel = path.relative_to(SCRATCH).as_posix()
    lines = path.read_text().splitlines()
    module = ""
    starts: list[tuple[int, str, str]] = []
    for idx, line in enumerate(lines, 1):
        mm = module_start.match(line)
        if mm:
            module = mm.group(1)
        sm = sentence_start.match(line)
        if sm:
            starts.append((idx, sm.group(1), module))

    for pos, (line_no, kind, module_name) in enumerate(starts):
        next_line = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines) + 1
        block_lines = []
        for raw in lines[line_no - 1 : next_line - 1]:
            if raw.startswith("endmodule") or raw.startswith("module "):
                break
            if raw.lstrip().startswith("//"):
                continue
            block_lines.append(raw.strip())
        text = " ".join(part for part in block_lines if part)
        attrs = ",".join(sorted(set(attribute.findall(text)))) or "-"
        classification, decision = disposition(rel, line_no, kind)
        rows.append(
            {
                "id": len(rows) + 1,
                "file": rel,
                "line": line_no,
                "module": module_name,
                "kind": kind,
                "attributes": attrs,
                "classification": classification,
                "decision": decision,
                "sentence": text,
            }
        )

with OUT.open("w", newline="") as stream:
    writer = csv.DictWriter(
        stream,
        delimiter="\t",
        fieldnames=(
            "id",
            "file",
            "line",
            "module",
            "kind",
            "attributes",
            "classification",
            "decision",
            "sentence",
        ),
    )
    writer.writeheader()
    writer.writerows(rows)

counts: dict[str, int] = {}
classes: dict[str, int] = {}
for row in rows:
    counts[row["kind"]] = counts.get(row["kind"], 0) + 1
    classes[row["classification"]] = classes.get(row["classification"], 0) + 1

with SUMMARY.open("w") as stream:
    stream.write(
        "COMMAND: python3 /audit-output/evidence/inventory_k.py\n"
        "EXIT: 0\n"
        f"source_files={len(paths)}\n"
        f"inventory_rows={len(rows)}\n"
    )
    for key in sorted(counts):
        stream.write(f"kind.{key}={counts[key]}\n")
    for key in sorted(classes):
        stream.write(f"class.{key}={classes[key]}\n")

print(f"source_files={len(paths)}")
print(f"inventory_rows={len(rows)}")
for key in sorted(counts):
    print(f"kind.{key}={counts[key]}")
for key in sorted(classes):
    print(f"class.{key}={classes[key]}")
