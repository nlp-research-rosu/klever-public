#!/usr/bin/env python3
"""Source-level K declaration/rule inventory for the audit.

This deliberately inventories source statements rather than trusting a
candidate-built definition.  It records every module/import, configuration,
syntax declaration, context, rule, alias, and claim start, plus the complete
source block through its guards/attributes.
"""

from collections import Counter
from pathlib import Path
import re


ROOTS = [
    Path("/reference/reference-semantics/semantics.k"),
    *sorted(Path("/reference/reference-semantics/semantics").glob("*.k")),
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
]

START = re.compile(
    r'^\s*(requires(?=\s+")|module|endmodule|imports|configuration|syntax|context|rule|claim|alias)\b'
)
BLOCK_KINDS = {"configuration", "syntax", "context", "rule", "claim", "alias"}
ATTRIBUTES = [
    "function",
    "total",
    "functional",
    "symbol",
    "no-evaluators",
    "concrete",
    "simplification",
    "simplify",
    "priority",
    "owise",
    "anywhere",
    "macro",
]


def blocks(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))
    for position, (index, kind) in enumerate(starts):
        if kind not in BLOCK_KINDS:
            yield index + 1, kind, lines[index].strip()
            continue
        next_index = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        end = next_index
        while end > index + 1 and not lines[end - 1].strip():
            end -= 1
        text = "\n".join(line.rstrip() for line in lines[index:end]).strip()
        yield index + 1, kind, text


grand = Counter()
attribute_counts = Counter()
print("# Exhaustive source inventory")
print()
print("Inputs: trusted `/reference/reference-semantics/**/*.k`, candidate")
print("`verification.k`, and candidate `spec.k`.")
print()
for path in ROOTS:
    entries = list(blocks(path))
    counts = Counter(kind for _, kind, _ in entries)
    grand.update(counts)
    print(f"## {path}")
    print()
    print("Counts: " + ", ".join(f"{key}={counts[key]}" for key in sorted(counts)))
    print()
    for line_no, kind, text in entries:
        uncommented = "\n".join(part.split("//", 1)[0] for part in text.splitlines())
        brackets = " ".join(re.findall(r"\[([^\]]*)\]", uncommented))
        attrs = [name for name in ATTRIBUTES if re.search(rf"\b{re.escape(name)}\b", brackets)]
        for attr in attrs:
            attribute_counts[attr] += 1
        classification = ""
        if kind == "rule":
            if "simplification" in attrs or "simplify" in attrs:
                classification = "simplification-rule"
            elif "concrete" in attrs:
                classification = "concrete-only-rule"
            elif "priority" in attrs:
                classification = "priority-rule"
            elif "owise" in attrs:
                classification = "owise-rule"
            else:
                classification = "ordinary-rule"
        suffix = f" [{classification}]" if classification else ""
        if attrs:
            suffix += " attrs=" + ",".join(attrs)
        print(f"- L{line_no} `{kind}`{suffix}")
        if kind in BLOCK_KINDS:
            print()
            print("  ```k")
            for source_line in text.splitlines():
                print("  " + source_line)
            print("  ```")
        else:
            print(f"  `{text}`")
    print()

print("# Totals")
print()
for key in sorted(grand):
    print(f"- {key}: {grand[key]}")
print()
print("# Attribute-bearing statement counts")
print()
for key in ATTRIBUTES:
    print(f"- {key}: {attribute_counts[key]}")
