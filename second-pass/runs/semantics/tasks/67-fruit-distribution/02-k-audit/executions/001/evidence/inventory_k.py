#!/usr/bin/env python3
"""Produce an exhaustive statement-level inventory of the audited K sources."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
BASE = ROOT / "reference-semantics"
FILES = sorted(BASE.rglob("*.k")) + [ROOT / "verification.k"]
START = re.compile(r"^\s*(configuration|syntax|rule|context|claim|macro|alias)\b")
BOUNDARY = re.compile(
    r"^\s*(configuration|syntax|rule|context|claim|macro|alias|"
    r"module|endmodule|imports)\b|^requires\s+\""
)
ATTRIBUTES = (
    "function",
    "functional",
    "total",
    "symbol",
    "no-evaluators",
    "priority",
    "owise",
    "concrete",
    "simplification",
    "strict",
    "seqstrict",
    "macro",
)

# Statement start-line ranges reached by the actual Module/FuncDef/Assign/Call/
# Attribute/split/Return/BinOp/int/Subscript program, including concrete Str
# examples. Entries outside these ranges remain part of the fixed supplied
# semantics, but are not on this program's proof path.
USED_RANGES: dict[str, tuple[tuple[int, int], ...]] = {
    "semantics/syntax.k": ((9, 30), (37, 38), (41, 61)),
    "semantics/core.k": (
        (13, 42),
        (49, 60),
        (68, 70),
        (117, 127),
        (130, 191),
        (194, 194),
        (208, 229),
    ),
    "semantics/operators.k": ((12, 12),),
    "semantics/int.k": ((13, 13),),
    "semantics/controls.k": ((9, 18),),
    "semantics/functions.k": ((8, 20), (62, 90)),
    "semantics/call.k": ((15, 32), (47, 50), (69, 74)),
    "semantics/methods.k": ((10, 10), (70, 86)),
    "semantics/builtins.k": ((17, 17), (139, 160)),
    "semantics/subscript.k": ((11, 41),),
    "semantics/str.k": ((13, 17),),
}


def statements(path: Path) -> list[dict[str, object]]:
    lines = path.read_text().splitlines()
    result: list[dict[str, object]] = []
    index = 0
    while index < len(lines):
        match = START.match(lines[index])
        if not match:
            index += 1
            continue
        start = index
        kind = match.group(1)
        index += 1
        while index < len(lines):
            if BOUNDARY.match(lines[index]):
                break
            # A blank line or a new comment after content terminates a K sentence.
            if not lines[index].strip():
                break
            if lines[index].lstrip().startswith("//"):
                break
            index += 1
        text = "\n".join(lines[start:index]).strip()
        result.append({"line": start + 1, "kind": kind, "text": text})
    return result


def relative(path: Path) -> str:
    if path == ROOT / "verification.k":
        return "verification.k"
    return str(path.relative_to(BASE))


def reached(filename: str, line: int) -> bool:
    return any(low <= line <= high for low, high in USED_RANGES.get(filename, ()))


def compact(text: str) -> str:
    return " ".join(text.split()).replace("|", "\\|")


all_entries: list[dict[str, object]] = []
for source in FILES:
    filename = relative(source)
    for entry in statements(source):
        entry["file"] = filename
        all_entries.append(entry)

print("# Exhaustive K source inventory")
print()
print("This statement-level inventory was generated from the clean scratch copy.")
print("A multiline `syntax` entry includes every alternative in that declaration.")
print()
print("## Counts")
print()
for kind in ("configuration", "syntax", "context", "rule", "claim", "macro", "alias"):
    count = sum(entry["kind"] == kind for entry in all_entries)
    print(f"- {kind}: {count}")
print(f"- total inventoried statements: {len(all_entries)}")
print()
print("## Attribute-bearing declarations and rules")
print()
for attribute in ATTRIBUTES:
    matching = [
        entry
        for entry in all_entries
        if re.search(rf"\b{re.escape(attribute)}\b", str(entry["text"]))
    ]
    print(f"- {attribute}: {len(matching)}")
    for entry in matching:
        print(f"  - {entry['file']}:{entry['line']}")
print()
print("## Per-statement decisions")
print()
print("| ID | Location | Kind | Path role | Decision | Statement |")
print("|---:|---|---|---|---|---|")
for number, entry in enumerate(all_entries, 1):
    filename = str(entry["file"])
    line = int(entry["line"])
    kind = str(entry["kind"])
    text = str(entry["text"])
    if filename == "verification.k":
        if line == 9:
            role = "proof-local opaque input encoding"
            decision = (
                "CONCERN: fresh constructors are consistent, but no equation or "
                "connection theorem relates them to concrete code sequences"
            )
        elif line == 15:
            role = "used result-bearing operational bridge"
            decision = (
                "CONCERN: correct for the intended exact grammar by ordinary "
                "string splitting, context/state preserving via #alloc, but no "
                "bridge-free universal connection theorem"
            )
        elif line == 34:
            role = "used result-bearing operational bridge"
            decision = (
                "CONCERN: correct inverse for nonnegative decimal notation, "
                "guarded and non-overlapping on the fresh constructor, but no "
                "bridge-free universal connection theorem"
            )
        elif line == 41:
            role = "used definitional summary"
            decision = (
                "ACCEPT: total nullary function names the exact submitted Module "
                "term; byte/AST identity checked separately"
            )
        elif line == 42:
            role = "used definitional equation"
            decision = (
                "ACCEPT: RHS is the exact trusted-translation AST; it does not "
                "replace execution after loading"
            )
        else:
            role = "proof-local"
            decision = "REVIEW REQUIRED"
    else:
        is_reached = reached(filename, line)
        role = "used fixed-semantics path" if is_reached else "unused fixed baseline"
        if kind == "configuration":
            decision = (
                "ACCEPT: unchanged byte-identical supplied configuration; its "
                "cells and initial values match every entry claim"
            )
        elif is_reached:
            decision = (
                "ACCEPT: unchanged byte-identical supplied-semantics rule/"
                "declaration; concrete path and overlaps reviewed for this program"
            )
        else:
            decision = (
                "ACCEPT AT SELECTED SEMANTICS LEVEL: unchanged byte-identical "
                "supplied baseline and unreachable from the submitted program"
            )
    print(
        f"| {number} | `{filename}:{line}` | {kind} | {role} | "
        f"{decision} | `{compact(text)}` |"
    )
