#!/usr/bin/env python3
"""Emit a line-addressable inventory of all K declarations and rules in scope."""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/109-move-one-ball/candidate")
PATHS = (
    [ROOT / "reference-semantics" / "semantics.k"]
    + sorted((ROOT / "reference-semantics" / "semantics").glob("*.k"))
    + [ROOT / "verification.k", ROOT / "spec.k"]
)
START = re.compile(r"^\s*(configuration|syntax|context|rule|claim)\b")


def compact(lines: list[str]) -> str:
    parts = []
    in_block_comment = False
    for raw in lines:
        line = raw.strip()
        if in_block_comment:
            if "*/" in line:
                line = line.split("*/", 1)[1].strip()
                in_block_comment = False
            else:
                continue
        while "/*" in line:
            before, after = line.split("/*", 1)
            if "*/" in after:
                after = after.split("*/", 1)[1]
                line = (before + " " + after).strip()
            else:
                line = before.strip()
                in_block_comment = True
                break
        if "//" in line:
            line = line.split("//", 1)[0].rstrip()
        if line:
            parts.append(line)
    return " ".join(parts)


entries: list[dict[str, object]] = []
module_rows = []
for path in PATHS:
    lines = path.read_text().splitlines()
    rel = path.relative_to(ROOT)
    module_names = [
        match.group(1)
        for line in lines
        if (match := re.match(r"^\s*module\s+(\S+)", line))
    ]
    module_rows.append((str(rel), ", ".join(module_names)))

    starts = [
        (index, match.group(1))
        for index, line in enumerate(lines)
        if (match := START.match(line))
    ]
    for position, (index, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        # Do not absorb the closing module into the preceding declaration.
        for cursor in range(index + 1, end):
            if re.match(r"^\s*endmodule\b", lines[cursor]):
                end = cursor
                break
        statement = compact(lines[index:end])
        attrs = []
        for attr in (
            "function",
            "total",
            "functional",
            "simplification",
            "concrete",
            "priority",
            "owise",
            "symbol",
            "no-evaluators",
            "strict",
            "seqstrict",
        ):
            if re.search(rf"\b{re.escape(attr)}\b", statement):
                attrs.append(attr)
        if rel == Path("verification.k"):
            source_class = "proof-local"
        elif rel == Path("spec.k"):
            source_class = "proof-claim"
        else:
            source_class = "supplied fixed semantics"
        entries.append(
            {
                "file": str(rel),
                "start": index + 1,
                "end": end,
                "kind": kind,
                "attrs": ", ".join(attrs) or "none",
                "source_class": source_class,
                "statement": statement,
            }
        )

print("# Exhaustive K declaration and rule inventory")
print()
print(
    "Generated from the fresh scratch source tree. Every top-level `configuration`, "
    "`syntax`, `context`, `rule`, and `claim` declaration is listed once."
)
print()
print("## Module manifest")
print()
print("| File | Modules |")
print("|---|---|")
for file_name, modules in module_rows:
    print(f"| `{file_name}` | `{modules}` |")

print()
print("## Counts")
print()
counts = collections.Counter((entry["file"], entry["kind"]) for entry in entries)
print("| File | Configuration | Syntax | Context | Rule | Claim | Total |")
print("|---|---:|---:|---:|---:|---:|---:|")
for path in PATHS:
    file_name = str(path.relative_to(ROOT))
    values = [counts[(file_name, kind)] for kind in ("configuration", "syntax", "context", "rule", "claim")]
    print(
        f"| `{file_name}` | {values[0]} | {values[1]} | {values[2]} | "
        f"{values[3]} | {values[4]} | {sum(values)} |"
    )
totals = [sum(counts[(str(path.relative_to(ROOT)), kind)] for path in PATHS) for kind in ("configuration", "syntax", "context", "rule", "claim")]
print(f"| **TOTAL** | {totals[0]} | {totals[1]} | {totals[2]} | {totals[3]} | {totals[4]} | {sum(totals)} |")

print()
print("## Entries")
print()
print("| # | Source class | Location | Kind | Attributes | Declaration / rule |")
print("|---:|---|---|---|---|---|")
for number, entry in enumerate(entries, 1):
    statement = str(entry["statement"]).replace("|", r"\|").replace("`", r"\`")
    location = f"{entry['file']}:{entry['start']}-{entry['end']}"
    print(
        f"| {number} | {entry['source_class']} | `{location}` | {entry['kind']} | "
        f"{entry['attrs']} | `{statement}` |"
    )
