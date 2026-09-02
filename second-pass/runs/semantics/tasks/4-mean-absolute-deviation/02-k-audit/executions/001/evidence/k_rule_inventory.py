#!/usr/bin/env python3
"""Emit a line-addressable exhaustive declaration/rule inventory for this audit."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/4mad-review/candidate-source")
FILES = [
    ROOT / "reference-semantics" / "semantics.k",
    *sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]
START = re.compile(
    r"^\s*(module|endmodule|imports|configuration|syntax|context alias|context|"
    r"rule|claim|alias)\b|^(requires)\b"
)
FLAGS = (
    "function",
    "functional",
    "total",
    "symbol",
    "no-evaluators",
    "priority",
    "simplification",
    "simplify",
    "concrete",
    "owise",
    "strict",
)


def records(path: Path) -> list[tuple[int, str, str]]:
    lines = path.read_text().splitlines()
    found: list[tuple[int, str, str]] = []
    index = 0
    while index < len(lines):
        match = START.match(lines[index])
        if match is None:
            index += 1
            continue
        kind = match.group(1) or match.group(2)
        start = index
        if kind in {"rule", "claim", "configuration", "syntax", "context", "context alias", "alias"}:
            index += 1
            while index < len(lines):
                next_match = START.match(lines[index])
                if next_match is not None:
                    break
                index += 1
        else:
            index += 1
        statement = " ".join(
            part.split("//", 1)[0].strip()
            for part in lines[start:index]
            if part.split("//", 1)[0].strip()
        )
        found.append((start + 1, kind, statement))
    return found


def classify(relative: str, kind: str, statement: str) -> tuple[str, str]:
    if relative == "verification.k":
        if kind == "syntax":
            return ("proof-local declaration", "REVIEWED")
        if kind == "rule" and "#applyK(toCall(builtinV(\"sum\"))" in statement:
            return ("operational bridge: sum", "SOUND_ON_GUARD_BUT_NO_CONNECTION_CLAIM")
        if kind == "rule" and "#loop(list(VS:ValSeq)" in statement:
            return ("operational bridge: loop", "UNSOUND_STATE_FOOTPRINT")
        if kind == "rule" and "#runMad" in statement:
            return ("entry execution harness", "EXACT_AST_ROUTE")
        if kind == "rule":
            return ("proof-local definition/equation", "REVIEWED")
    if relative == "spec.k" and kind == "claim":
        return ("target reachability claim", "RESULT_CONSTRAINING")
    if relative.startswith("reference-semantics/"):
        if kind == "rule" and "[concrete]" in statement:
            return ("supplied concrete primitive rule", "SELECTED_SEMANTICS_BOUNDARY")
        if kind == "rule" and "<k>" in statement:
            return ("supplied operational semantic rule", "SELECTED_SEMANTICS_BOUNDARY")
        if kind == "rule":
            return ("supplied equational semantic rule", "SELECTED_SEMANTICS_BOUNDARY")
        if kind == "syntax":
            return ("supplied syntax/declaration", "SELECTED_SEMANTICS_BOUNDARY")
        if kind == "configuration":
            return ("supplied configuration", "SELECTED_SEMANTICS_BOUNDARY")
        if kind in {"context", "context alias"}:
            return ("supplied evaluation context", "SELECTED_SEMANTICS_BOUNDARY")
    return ("module/import plumbing", "STRUCTURAL")


print(
    "\t".join(
        (
            "id",
            "file",
            "line",
            "kind",
            "flags",
            "classification",
            "disposition",
            "statement",
        )
    )
)
record_id = 0
for path in FILES:
    relative = str(path.relative_to(ROOT))
    for line, kind, statement in records(path):
        record_id += 1
        flags = ",".join(flag for flag in FLAGS if re.search(rf"\b{re.escape(flag)}\b", statement))
        classification, disposition = classify(relative, kind, statement)
        print(
            "\t".join(
                (
                    str(record_id),
                    relative,
                    str(line),
                    kind,
                    flags,
                    classification,
                    disposition,
                    statement.replace("\t", " "),
                )
            )
        )
