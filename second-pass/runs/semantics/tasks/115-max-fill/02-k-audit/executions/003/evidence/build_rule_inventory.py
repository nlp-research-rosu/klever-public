#!/usr/bin/env python3
"""Generate a complete declaration/rule/claim inventory for all audited K files."""

from __future__ import annotations

import html
import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/115-max-fill-audit")
FILES = [
    ROOT / "reference-semantics/semantics.k",
    *sorted((ROOT / "reference-semantics/semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]
OUTPUT = Path("/audit-output/evidence/rule_inventory.md")

START = re.compile(
    r"^\s*(configuration|context\s+alias|context|syntax|rule|claim|alias|priority)\b"
)
BOUNDARY = re.compile(
    r"^\s*(requires|module|endmodule|imports|configuration|context\s+alias|"
    r"context|syntax|rule|claim|alias|priority)\b"
)


def statement_blocks(path: Path):
    lines = path.read_text().splitlines()
    starts = [i for i, line in enumerate(lines) if START.match(line)]
    for number, start in enumerate(starts):
        next_start = starts[number + 1] if number + 1 < len(starts) else len(lines)
        # Stop before module/import/end markers that occur before the next declaration.
        end = next_start
        for i in range(start + 1, next_start):
            if BOUNDARY.match(lines[i]) and not lines[i].lstrip().startswith(
                ("requires ", "[")
            ):
                end = i
                break
        # Remove blank/comment tail while retaining multiline rule guards/attrs.
        block = lines[start:end]
        while block and (
            not block[-1].strip() or block[-1].lstrip().startswith("//")
        ):
            block.pop()
        match = START.match(lines[start])
        assert match
        kind = " ".join(match.group(1).split())
        yield start + 1, start + len(block), kind, "\n".join(block).strip()


rows = []
counts: Counter[str] = Counter()
attribute_counts: Counter[str] = Counter()
for path in FILES:
    relative = path.relative_to(ROOT).as_posix()
    for first, last, kind, text in statement_blocks(path):
        attrs = []
        for attr in [
            "function",
            "functional",
            "total",
            "macro",
            "priority",
            "simplification",
            "simplify",
            "concrete",
            "owise",
            "anywhere",
            "no-evaluators",
            "symbol",
            "strict",
            "seqstrict",
            "hook",
            "token",
        ]:
            if re.search(rf"\b{re.escape(attr)}\b", text):
                attrs.append(attr)
                attribute_counts[attr] += 1
        scope = "proof-local" if path.name in {"verification.k", "spec.k"} else "fixed"
        if scope == "fixed":
            assessment = (
                "Selected supplied semantics; inspected for contribution. "
                "Unused declarations/rules add no proof-local conclusion."
            )
        elif path.name == "spec.k":
            assessment = "Reachability claim; assessed individually in REVIEW.md."
        else:
            assessment = "Proof-local declaration/rule; assessed individually in REVIEW.md."
        rows.append(
            (relative, first, last, kind, ", ".join(attrs) or "none", text, assessment)
        )
        counts[kind] += 1

output = [
    "# Exhaustive K declaration and rule inventory",
    "",
    f"Files inventoried: {len(FILES)}",
    "",
    f"Inventory entries: {len(rows)}",
    "",
    f"Counts by kind: `{dict(sorted(counts.items()))}`",
    "",
    f"Attribute occurrences by entry: `{dict(sorted(attribute_counts.items()))}`",
    "",
    "The `fixed` scope is the byte-identical supplied-semantics baseline. "
    "Proof-local entries are not blessed by that baseline and receive explicit "
    "line-by-line grouped assessments in REVIEW.md.",
    "",
    "| # | File:lines | Scope | Kind | Attributes | Exact declaration/rule/claim | Assessment route |",
    "|---:|---|---|---|---|---|---|",
]
for index, (path, first, last, kind, attrs, text, assessment) in enumerate(rows, 1):
    escaped = html.escape(text).replace("\n", "<br>")
    lines = f"{first}" if first == last else f"{first}-{last}"
    scope = "proof-local" if path in {"verification.k", "spec.k"} else "fixed"
    output.append(
        f"| {index} | `{path}:{lines}` | {scope} | {kind} | {attrs} | "
        f"<code>{escaped}</code> | {assessment} |"
    )

OUTPUT.write_text("\n".join(output) + "\n")
print(f"output={OUTPUT}")
print(f"files={len(FILES)}")
print(f"entries={len(rows)}")
print(f"counts={dict(sorted(counts.items()))}")
print(f"attribute_entry_counts={dict(sorted(attribute_counts.items()))}")
