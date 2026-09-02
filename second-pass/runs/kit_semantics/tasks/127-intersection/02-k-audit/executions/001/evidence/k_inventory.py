#!/usr/bin/env python3
"""Emit an exhaustive declaration/rule inventory for the audited K sources."""

import collections
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/127-intersection")
sources = sorted((ROOT / "reference-semantics").rglob("*.k"))
sources += [ROOT / "solution-module.k", ROOT / "verification.k", ROOT / "spec.k"]

starter = re.compile(
    r"^(?:requires|module|endmodule)\b|^\s*(imports|configuration|syntax|context|rule|claim)\b"
)
inventoried = {"configuration", "syntax", "context", "rule", "claim"}
blocks = []

for path in sources:
    lines = path.read_text().splitlines()
    starts = []
    for index, line in enumerate(lines):
        match = starter.match(line)
        if match:
            stripped_kind = line.strip().split(maxsplit=1)[0]
            starts.append((index, match.group(1) or stripped_kind))
    for position, (start, kind) in enumerate(starts):
        if kind not in inventoried:
            continue
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        text = "\n".join(lines[start:end]).rstrip()
        blocks.append((path, start + 1, end, kind, text))

kind_counts = collections.Counter()
attribute_counts = collections.Counter()
file_counts = collections.Counter()

print("K RULE/DECLARATION INVENTORY")
print("scope=trusted supplied semantics + candidate solution-module.k + verification.k + spec.k")
for ordinal, (path, start, end, kind, text) in enumerate(blocks, 1):
    relative = path.relative_to(ROOT)
    kind_counts[kind] += 1
    file_counts[str(relative)] += 1
    attributes = []
    for attribute in (
        "function",
        "total",
        "functional",
        "symbol",
        "no-evaluators",
        "simplification",
        "concrete",
        "priority",
        "owise",
        "macro",
        "macro-rec",
        "strict",
        "seqstrict",
    ):
        if re.search(rf"\b{re.escape(attribute)}\b", text):
            attributes.append(attribute)
            attribute_counts[attribute] += 1
    if kind == "rule":
        classification = "ordinary-semantic-rule"
        if "simplification" in attributes:
            classification = "simplification-rule"
        elif "concrete" in attributes:
            classification = "concrete-rule"
        elif "owise" in attributes:
            classification = "owise-rule"
    elif kind == "syntax":
        if "macro" in attributes or "macro-rec" in attributes:
            classification = "syntax-macro"
        elif "function" in attributes:
            classification = "function-declaration"
        else:
            classification = "syntax-declaration"
    elif kind == "claim":
        classification = "reachability-claim"
    else:
        classification = kind
    attr_text = ",".join(attributes) if attributes else "-"
    print()
    print(
        f"ENTRY {ordinal:04d} file={relative} lines={start}-{end} "
        f"kind={kind} class={classification} attributes={attr_text}"
    )
    for offset, line in enumerate(text.splitlines(), start):
        print(f"{offset:04d}: {line}")

print()
print("SUMMARY")
print(f"files={len(sources)}")
print(f"entries={len(blocks)}")
for kind, count in sorted(kind_counts.items()):
    print(f"kind[{kind}]={count}")
for attribute, count in sorted(attribute_counts.items()):
    print(f"attribute[{attribute}]={count}")
for path, count in sorted(file_counts.items()):
    print(f"file_entries[{path}]={count}")
