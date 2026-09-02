#!/usr/bin/env python3
"""Emit an exhaustive source-level K declaration and rule inventory."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

ROOT = Path("/tmp/audit-work/proof")
files = [
    ROOT / "reference-semantics/semantics.k",
    *sorted((ROOT / "reference-semantics/semantics").glob("*.k")),
    ROOT / "verification.k",
]

start_re = re.compile(
    r"^(?P<indent> *)(?P<kind>"
    r"requires|module|endmodule|imports|syntax|configuration|context alias|"
    r"context|rule|claim"
    r")\b"
)

counts: Counter[str] = Counter()
attribute_counts: Counter[str] = Counter()
inventory = []

for path in files:
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = start_re.match(line)
        if not match:
            continue
        # Declarations/rules inside a module use two spaces.  Indented
        # `requires` clauses on rules are not top-level entries.
        if len(match.group("indent")) > 2:
            continue
        starts.append((index, match.group("kind")))
    for position, (index, kind) in enumerate(starts):
        stop = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        block = "\n".join(lines[index:stop]).strip()
        # Exclude comments/blank lines immediately before the next declaration.
        body_lines = block.splitlines()
        while body_lines and (
            not body_lines[-1].strip() or body_lines[-1].lstrip().startswith("//")
        ):
            body_lines.pop()
        block = "\n".join(body_lines)
        relative = path.relative_to(ROOT).as_posix()
        if relative == "verification.k":
            if kind in {"rule", "syntax"} and index + 1 <= 46:
                decision = "CANDIDATE_EXACT_PROGRAM_MACRO"
            elif kind in {"rule", "syntax"} and index + 1 <= 63:
                decision = "CANDIDATE_INDUCTIVE_CARRIER_OR_ITERATOR"
            elif kind in {"rule", "syntax"} and index + 1 <= 96:
                decision = "CANDIDATE_DEFINITIONAL_SUMMARY"
            elif kind == "rule":
                decision = "CANDIDATE_OPERATIONAL_BRIDGE"
            else:
                decision = "CANDIDATE_MODULE_STRUCTURE"
        else:
            decision = "SELECTED_TRUSTED_FIXED_SEMANTICS"
        bracket_text = " ".join(re.findall(r"\[[^\]]*\]", block))
        tags = sorted(
            set(
                re.findall(
                    r"\b(functional|function|total|macro-rec|macro|priority|"
                    r"simplification|concrete|symbol|no-evaluators|owise|hook)\b",
                    bracket_text,
                )
            )
        )
        counts[kind] += 1
        attribute_counts.update(tags)
        inventory.append(
            (relative, index + 1, kind, decision, ",".join(tags) or "-", block)
        )

print("INVENTORY_SUMMARY")
for key in sorted(counts):
    print(f"{key}: {counts[key]}")
print("ATTRIBUTE_SUMMARY")
for key in sorted(attribute_counts):
    print(f"{key}: {attribute_counts[key]}")
print(f"TOTAL_ENTRIES: {len(inventory)}")
print()

for number, (relative, line, kind, decision, tags, block) in enumerate(inventory, 1):
    one_line = " ".join(part.strip() for part in block.splitlines() if part.strip())
    print(
        f"{number:04d}\t{relative}:{line}\t{kind}\t{decision}\t"
        f"attributes={tags}\t{one_line}"
    )
