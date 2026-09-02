#!/usr/bin/env python3
"""Create a complete source-level declaration/rule inventory for the audit."""

from __future__ import annotations

import argparse
import collections
import re
from pathlib import Path


START = re.compile(r"^\s*(configuration|syntax|rule|claim|context|alias)\b")
ATTRIBUTE_WORDS = (
    "function",
    "total",
    "functional",
    "simplification",
    "priority",
    "concrete",
    "owise",
    "macro",
    "symbol",
    "no-evaluators",
)

# Exact source locations that form the reachable strlen execution slice.
TARGET_RULE_LINES = {
    "semantics/core.k": {
        125, 126, 127, 131, 132, 145, 152, 158, 189, 190, 191, 227, 228, 229
    },
    "semantics/functions.k": {14, 63, 64, 68, 78, 80, 85},
    "semantics/call.k": {20, 21, 31, 69},
    "semantics/builtins.k": {21, 24},
}
TARGET_SYNTAX_FILES = {
    "semantics/syntax.k",
    "semantics/core.k",
    "semantics/functions.k",
    "semantics/call.k",
    "semantics/builtins.k",
}


def logical_items(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))
    for position, (start, kind) in enumerate(starts):
        next_start = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        end = next_start
        for index in range(start + 1, next_start):
            if re.match(r"^\s*endmodule\b", lines[index]):
                end = index
                break
        block = lines[start:end]
        while block and (not block[-1].strip() or block[-1].lstrip().startswith("//")):
            block.pop()
        yield start + 1, kind, "\n".join(block)


parser = argparse.ArgumentParser()
parser.add_argument("root")
args = parser.parse_args()
root = Path(args.root)
paths = [
    root / "reference-semantics/semantics.k",
    *sorted((root / "reference-semantics/semantics").glob("*.k")),
    root / "verification.k",
    root / "spec.k",
]

rows = []
kind_counts = collections.Counter()
attribute_counts = collections.Counter()
file_counts: dict[str, collections.Counter[str]] = {}
for path in paths:
    relative = path.relative_to(root).as_posix()
    file_counter: collections.Counter[str] = collections.Counter()
    for line, kind, text in logical_items(path):
        attributes = [word for word in ATTRIBUTE_WORDS if re.search(rf"\b{re.escape(word)}\b", text)]
        if "no-evaluators" in text and "opaque" not in attributes:
            attributes.append("opaque")
        if kind == "rule":
            target = line in TARGET_RULE_LINES.get(relative.replace("reference-semantics/", ""), set())
            assessment = (
                "fixed-supplied; reachable target rule; manually reviewed"
                if target
                else "fixed-supplied; target-unreachable from pinned strlen state"
            )
        elif kind == "syntax":
            target = relative.replace("reference-semantics/", "") in TARGET_SYNTAX_FILES
            assessment = (
                "declaration; target syntax/helper file; manually mapped"
                if target
                else "declaration; target-unreachable construct/helper"
            )
        elif kind == "configuration":
            target = True
            assessment = "fixed-supplied initial configuration; manually reviewed"
        elif kind == "claim":
            target = relative == "spec.k"
            assessment = "positive target reachability claim; manually reviewed"
        else:
            target = False
            assessment = "fixed-supplied declaration; target-unreachable"
        normalized = " ".join(part.strip() for part in text.splitlines() if part.strip())
        rows.append((relative, line, kind, ",".join(attributes) or "-", target, assessment, normalized))
        kind_counts[kind] += 1
        file_counter[kind] += 1
        for attribute in attributes:
            attribute_counts[attribute] += 1
    file_counts[relative] = file_counter

print("# Exhaustive K source inventory")
print()
print("The table includes every source statement beginning with `configuration`,")
print("`syntax`, `rule`, `claim`, `context`, or `alias` in the supplied semantics,")
print("the candidate verification module, and the positive spec. Multiline statements")
print("are normalized onto one row. `target-reachable` is a conservative static slice")
print("for the exact pinned `strlen` execution; all other supplied rules remain fixed")
print("trusted semantics but cannot be reached from that pinned state.")
print()
print("## Summary")
print()
print(f"- Inventoried statements: {len(rows)}")
for kind, count in sorted(kind_counts.items()):
    print(f"- `{kind}`: {count}")
for attribute, count in sorted(attribute_counts.items()):
    print(f"- attribute `{attribute}`: {count}")
print()
print("### Per-file counts")
print()
print("| File | Counts |")
print("|---|---|")
for relative, counts in file_counts.items():
    formatted = ", ".join(f"{kind}={count}" for kind, count in sorted(counts.items())) or "none"
    print(f"| `{relative}` | {formatted} |")
print()
print("## Itemized inventory")
print()
print("| ID | Source | Kind | Attributes/classes | Target-reachable | Assessment | Normalized source |")
print("|---:|---|---|---|---|---|---|")
for identifier, (relative, line, kind, attributes, target, assessment, normalized) in enumerate(rows, 1):
    escaped = normalized.replace("|", "&#124;").replace("`", "&#96;")
    print(
        f"| {identifier} | `{relative}:{line}` | `{kind}` | `{attributes}` | "
        f"{'yes' if target else 'no'} | {assessment} | {escaped} |"
    )
