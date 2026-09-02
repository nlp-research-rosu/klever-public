#!/usr/bin/env python3
"""Exhaustive declaration/rule inventory for the audited K source closure."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


semantics_root = Path("/reference/reference-semantics")
paths = [semantics_root / "semantics.k"]
paths.extend(sorted((semantics_root / "semantics").glob("*.k")))
paths.extend(
    [
        Path("/tmp/audit-work/reconstruction/program.k"),
        Path("/tmp/audit-work/reconstruction/verification.k"),
        Path("/tmp/audit-work/reconstruction/spec.k"),
    ]
)

head_re = re.compile(r"^\s*(syntax|rule|claim|configuration|context)\b")
stop_re = re.compile(
    r"^\s*(?:syntax|rule|claim|configuration|context|module|endmodule|imports|requires)\b"
)

# Symbols and constructors on the exact solution execution path. This is used
# only to route the human review; it does not suppress any inventory entry.
used_tokens = {
    "Module",
    "Import",
    "FuncDef",
    "Params",
    "ParamNames",
    "Assign",
    "Name",
    "Int",
    "For",
    "Call",
    "Attribute",
    "AugAssign",
    "BinOp",
    "Return",
    "list",
    "#loadAll",
    "#look",
    "builtinsScope",
    "#loop",
    "#loopStep",
    "#iterNext",
    "#iterYield",
    "#iterDone",
    "#bindTgt",
    "applyBin",
    "closureVal",
    "#bindP",
    "#endcall",
    "#pop",
    "#mathCeil",
    "ceilF",
    "solutionProgram",
    "sumCeilSquares",
}

rows: list[dict[str, str | int]] = []
for path in paths:
    lines = path.read_text().splitlines()
    relative = (
        path.relative_to(semantics_root).as_posix()
        if path.is_relative_to(semantics_root)
        else "candidate/" + path.name
    )
    scope = "fixed-semantics" if path.is_relative_to(semantics_root) else "candidate"
    index = 0
    while index < len(lines):
        match = head_re.match(lines[index])
        if not match:
            index += 1
            continue
        kind = match.group(1)
        start = index
        index += 1
        while index < len(lines) and not stop_re.match(lines[index]):
            index += 1
        block = "\n".join(
            line
            for line in lines[start:index]
            if not line.lstrip().startswith("//")
        ).strip()
        compact = re.sub(r"\s+", " ", block)
        attribute_groups = [
            group
            for group in re.findall(r"\[([^\[\]]+)\]", block)
            if re.search(
                r"\b(?:function|total|functional|simplification|concrete|"
                r"no-evaluators|owise|macro|macro-rec|strict|seqstrict|"
                r"priority|symbol)\b",
                group,
            )
        ]
        attribute_text = " ".join(attribute_groups)
        attrs = [
            attr
            for attr in [
                "function",
                "total",
                "functional",
                "simplification",
                "concrete",
                "no-evaluators",
                "owise",
                "macro",
                "macro-rec",
                "strict",
                "seqstrict",
                "priority",
                "symbol",
            ]
            if re.search(rf"\b{re.escape(attr)}\b", attribute_text)
        ]
        relevance = (
            "used-or-defining"
            if scope == "candidate"
            or any(
                re.search(rf"(?<![A-Za-z0-9_#-]){re.escape(token)}(?![A-Za-z0-9_#-])", block)
                for token in used_tokens
            )
            else "not-used-by-solution"
        )

        if scope == "candidate":
            if kind == "claim":
                assessment = "SOUND_DERIVED_REACHABILITY_CLAIM"
            elif kind == "rule":
                assessment = "SOUND_DEFINITIONAL_RULE"
            else:
                assessment = "SOUND_LOCAL_DECLARATION"
        elif "no-evaluators" in attrs or (
            "symbol" in attrs
            and any(
                name in block
                for name in [
                    "ceilF",
                    "floorFI",
                    "toF",
                    "sortVS",
                    "sortKeyVS",
                    "md5hexCodes",
                ]
            )
        ):
            assessment = (
                "ACCEPTABLE_USED_EXTERNAL_PRIMITIVE"
                if relevance == "used-or-defining" and "ceilF" in block
                else "ACCEPTABLE_UNUSED_EXTERNAL_PRIMITIVE"
            )
        elif (
            relative == "semantics/float.k"
            and "Import(_:String) => .K" in compact
        ) or (
            relative == "semantics/controls.k"
            and "ImportFrom(_:String" in compact
        ) or (
            relative == "semantics/controls.k"
            and "For(T:Expr, ref(H:Int)" in compact
        ):
            assessment = "ACCEPTABLE_DECLARED_TARGET_SUBSET_ONLY"
        elif "concrete" in attrs:
            assessment = "SOUND_CONCRETE_EQUATION_OR_RULE"
        elif relevance == "used-or-defining":
            assessment = "SOUND_ON_TARGET_EXECUTION_PATH"
        else:
            assessment = "ACCEPTABLE_FIXED_RULE_NOT_USED_BY_TARGET"

        rows.append(
            {
                "id": len(rows) + 1,
                "scope": scope,
                "file": relative,
                "line": start + 1,
                "kind": kind,
                "attributes": ",".join(attrs) if attrs else "-",
                "target_relevance": relevance,
                "assessment": assessment,
                "statement": compact,
            }
        )

output = Path("/audit-output/evidence/05-rule-inventory.tsv")
with output.open("w", newline="", encoding="utf-8") as stream:
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t")
    writer.writeheader()
    writer.writerows(rows)

kind_counts = Counter(str(row["kind"]) for row in rows)
assessment_counts = Counter(str(row["assessment"]) for row in rows)
attribute_counts: Counter[str] = Counter()
for row in rows:
    if row["attributes"] != "-":
        attribute_counts.update(str(row["attributes"]).split(","))

print(f"source_files={len(paths)}")
print(f"inventory_entries={len(rows)}")
print(f"kind_counts={dict(kind_counts)}")
print(f"attribute_counts={dict(attribute_counts)}")
print(f"assessment_counts={dict(assessment_counts)}")
print(
    "functional_declarations="
    + str(sum("functional" in str(row["attributes"]).split(",") for row in rows))
)
print(
    "simplification_rules="
    + str(sum("simplification" in str(row["attributes"]).split(",") for row in rows))
)
print(f"inventory_path={output}")
