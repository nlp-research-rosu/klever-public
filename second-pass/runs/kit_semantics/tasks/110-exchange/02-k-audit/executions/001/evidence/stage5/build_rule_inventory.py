#!/usr/bin/env python3
"""Mechanical declaration inventory for supplied and proof-local K sources."""

from __future__ import annotations

import csv
import re
from pathlib import Path


WORK = Path("/tmp/audit-work/scratch/proof")
OUTPUT = Path("/audit-output/evidence/stage5/rule-inventory.tsv")
DECLARATION = re.compile(
    r"^(requires(?=\s+\")| {0,2}(?:module|endmodule|imports|configuration|syntax|rule|context|claim))\b"
)
MODULE = re.compile(r"^\s*module\s+([A-Za-z0-9_-]+)")


def normalized(lines: list[str]) -> str:
    return " ".join(" ".join(lines).split())


def parse(path: Path, provenance: str):
    text = path.read_text()
    raw_lines = text.splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(raw_lines):
        match = DECLARATION.match(line)
        if match:
            kind = match.group(1).strip().split()[0]
            starts.append((index, kind))

    current_module = ""
    start_index = 0
    records = []
    for position, (index, kind) in enumerate(starts):
        if index < start_index:
            continue
        end = starts[position + 1][0] if position + 1 < len(starts) else len(raw_lines)
        block_lines = raw_lines[index:end]
        block = normalized(block_lines)
        if kind == "module":
            match = MODULE.match(raw_lines[index])
            current_module = match.group(1) if match else ""
        module_for_record = current_module
        if kind == "endmodule":
            current_module = ""

        if kind == "rule":
            declaration_class = (
                "simplification-rule"
                if "simplification" in block
                else "ordinary-rule"
            )
        elif kind == "syntax":
            declaration_class = "syntax-declaration"
        elif kind == "context":
            declaration_class = "evaluation-context"
        elif kind == "configuration":
            declaration_class = "configuration"
        elif kind == "claim":
            declaration_class = "reachability-claim"
        else:
            declaration_class = kind

        records.append(
            {
                "provenance": provenance,
                "file": path.relative_to(WORK).as_posix(),
                "line": index + 1,
                "module": module_for_record,
                "kind": kind,
                "class": declaration_class,
                "function": "function" in block,
                "total": re.search(r"\btotal\b", block) is not None,
                "functional": re.search(r"\bfunctional\b", block) is not None,
                "symbol": re.search(r"\bsymbol(?:\(|\b)", block) is not None,
                "opaque_no_evaluators": "no-evaluators" in block,
                "priority": "priority(" in block,
                "simplification": "simplification" in block,
                "concrete": re.search(r"\bconcrete\b", block) is not None,
                "owise": re.search(r"\bowise\b", block) is not None,
                "macro": re.search(r"\bmacro\b", block) is not None,
                "text": block,
            }
        )
    return records


def main() -> None:
    sources = [
        (WORK / "reference-semantics" / "semantics.k", "SUPPLIED_FIXED"),
        *[
            (path, "SUPPLIED_FIXED")
            for path in sorted((WORK / "reference-semantics" / "semantics").glob("*.k"))
        ],
        (WORK / "verification.k", "PROOF_LOCAL"),
        (WORK / "connection-spec.k", "PROOF_CLAIM"),
        (WORK / "spec.k", "TARGET_CLAIM"),
    ]
    records = []
    for path, provenance in sources:
        records.extend(parse(path, provenance))
    fieldnames = [
        "id",
        "provenance",
        "file",
        "line",
        "module",
        "kind",
        "class",
        "function",
        "total",
        "functional",
        "symbol",
        "opaque_no_evaluators",
        "priority",
        "simplification",
        "concrete",
        "owise",
        "macro",
        "text",
    ]
    with OUTPUT.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for identifier, record in enumerate(records, 1):
            writer.writerow({"id": identifier, **record})

    print(f"output={OUTPUT}")
    print(f"declarations={len(records)}")
    for provenance in sorted({record["provenance"] for record in records}):
        subset = [record for record in records if record["provenance"] == provenance]
        print(f"{provenance}={len(subset)}")
        for declaration_class in sorted({record["class"] for record in subset}):
            count = sum(record["class"] == declaration_class for record in subset)
            print(f"  {declaration_class}={count}")
    for attribute in [
        "function",
        "total",
        "functional",
        "symbol",
        "opaque_no_evaluators",
        "priority",
        "simplification",
        "concrete",
        "owise",
        "macro",
    ]:
        count = sum(bool(record[attribute]) for record in records)
        print(f"attribute_{attribute}={count}")


if __name__ == "__main__":
    main()
