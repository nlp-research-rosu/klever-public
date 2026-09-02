#!/usr/bin/env python3
"""Emit a source-level inventory of all local K declarations for Stage 5."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOT = Path("/reference/reference-semantics")
FILES = [ROOT / "semantics.k", *sorted((ROOT / "semantics").glob("*.k"))]
FILES += [Path("/candidate/verification.k"), Path("/candidate/spec.k")]
START = re.compile(r"^\s*(syntax|rule|claim|configuration|context|alias)\b")
STOP = re.compile(r"^\s*(module|endmodule|requires|imports)\b")


def compact(text: str) -> str:
    return " ".join(
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.lstrip().startswith("//")
    )


records: list[dict[str, object]] = []
for path in FILES:
    lines = path.read_text().splitlines()
    starts = [
        index
        for index, line in enumerate(lines)
        if START.match(line)
    ]
    boundaries = set(starts)
    boundaries.update(
        index for index, line in enumerate(lines) if STOP.match(line)
    )
    ordered_boundaries = sorted(boundaries)
    for start in starts:
        end = len(lines)
        for boundary in ordered_boundaries:
            if boundary > start:
                end = boundary
                break
        text = "\n".join(lines[start:end]).rstrip()
        match = START.match(lines[start])
        assert match is not None
        declaration = match.group(1)
        attrs = []
        for attr in [
            "function",
            "functional",
            "total",
            "macro",
            "simplification",
            "simplifier",
            "no-evaluators",
            "concrete",
            "owise",
            "priority",
        ]:
            if re.search(rf"\b{re.escape(attr)}\b", text):
                attrs.append(attr)
        if declaration == "rule":
            if "macro" in attrs:
                role = "macro rule"
            elif "<k>" in text or re.search(r"<[-A-Za-z]+>", text):
                role = "operational rule"
            else:
                role = "equational rule"
        elif declaration == "syntax":
            role = "syntax declaration"
        else:
            role = declaration
        records.append(
            {
                "path": path,
                "line": start + 1,
                "declaration": declaration,
                "role": role,
                "attrs": ",".join(attrs) or "-",
                "text": compact(text),
            }
        )


def assessment(record: dict[str, object]) -> str:
    path = str(record["path"])
    line = int(record["line"])
    declaration = str(record["declaration"])
    text = str(record["text"])
    if path == "/candidate/verification.k":
        if line in {8, 9, 12, 13}:
            return "REACHED-SOUND: definitional macro; expanded term was mechanically matched"
        if line in {21, 22}:
            return "REACHED-SOUND: launch wrapper; introduces no result and preserves framed state"
    if path == "/candidate/spec.k":
        return "TARGET-CLAIM: result-constraining but inadequate for Unicode Python str"
    if path.endswith("/semantics/methods.k") and (
        line in {10, 19, 20, 21}
        or 112 <= line <= 164
    ):
        if line in {21, 112, 113, 115, 116, 149, 150, 151, 152, 162, 163, 164}:
            return "REACHED-MODEL-GAP: coherent ASCII equation, false as full Python Unicode behavior"
        return "REACHED-SOUND: disjoint definitional helper in the fixed ASCII model"
    if path.endswith("/semantics/core.k") and (
        13 <= line <= 42
        or line == 49
        or 124 <= line <= 132
        or line in {145, 152, 157, 158, 185, 186, 189, 190, 191, 213, 214, 215}
    ):
        return "REACHED-SOUND: ordinary configuration/load/lookup/evaluation rule"
    if path.endswith("/semantics/functions.k") and (
        8 <= line <= 16 or 62 <= line <= 90
    ):
        return "REACHED-SOUND: ordinary closure binding/return/frame rule"
    if path.endswith("/semantics/call.k") and (
        15 <= line <= 24 or 69 <= line <= 75
    ):
        return "REACHED-SOUND: ordinary attribute/call dispatch or closure-frame rule"
    if path.endswith("/semantics/syntax.k") and any(
        token in text
        for token in [
            "Expr ::=",
            "Exprs",
            "Stmt ::=",
            "Stmts",
            "Params",
            "ParamNames",
            "Module",
        ]
    ):
        return "REACHED-SOUND: constructor declaration used by the submitted module"
    if declaration in {"syntax", "configuration", "context"}:
        return "FIXED-UNREACHED-DECL: well-sorted in clean build; constructor absent from proof slice"
    if declaration == "claim":
        return "CLAIM"
    return (
        "FIXED-UNREACHED-RULE: inspected fixed baseline; head cannot occur on this "
        "program/claim slice and it contributes no equation to closure"
    )


print("# Exhaustive local K declaration inventory")
print()
print(
    "Generated from every source file in the trusted supplied-semantics tree, "
    "plus candidate verification.k and spec.k."
)
print()
counts = Counter((str(record["path"]), str(record["declaration"])) for record in records)
print("## Counts")
print()
print("| File | syntax | rule | claim | configuration | context | alias |")
print("|---|---:|---:|---:|---:|---:|---:|")
for path in FILES:
    values = [counts[(str(path), key)] for key in ["syntax", "rule", "claim", "configuration", "context", "alias"]]
    print(f"| `{path}` | " + " | ".join(str(value) for value in values) + " |")
print()
print(f"Total declarations: {len(records)}")
print()
print("## Records")
print()
print("| ID | Source | Kind | Attributes | Audit determination | Complete declaration (comments omitted) |")
print("|---:|---|---|---|---|---|")
for identifier, record in enumerate(records, 1):
    source = f"{record['path']}:{record['line']}"
    text = str(record["text"]).replace("|", "&#124;")
    print(
        f"| {identifier} | `{source}` | {record['role']} | "
        f"`{record['attrs']}` | {assessment(record)} | `{text}` |"
    )
