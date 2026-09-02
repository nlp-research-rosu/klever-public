#!/usr/bin/env python3
"""Emit a line-addressable inventory of all supplied and proof-local K items."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

ROOT = Path("/tmp/audit-work/fresh")
paths = sorted((ROOT / "reference-semantics").rglob("*.k"))
paths += [
    ROOT / "verification.k",
    ROOT / "verification-with-loop.k",
    ROOT / "spec.k",
]

start_re = re.compile(
    r"^\s*(syntax|rule|claim|configuration|context|alias|macro)\b"
)
stop_re = re.compile(
    r"^\s*(?:syntax|rule|claim|configuration|context|alias|macro|"
    r"module|endmodule|imports\b|requires\s+\")"
)
attribute_names = (
    "function",
    "total",
    "functional",
    "simplification",
    "priority",
    "opaque",
    "no-evaluators",
    "concrete",
    "owise",
    "strict",
    "seqstrict",
    "macro",
)

counts: Counter[tuple[str, str]] = Counter()
attribute_counts: Counter[tuple[str, str]] = Counter()

for path in paths:
    relative = path.relative_to(ROOT)
    if str(relative).startswith("reference-semantics/"):
        source_class = "SUPPLIED_BASELINE"
    elif relative.name == "verification.k":
        source_class = "PROOF_LOCAL"
    elif relative.name == "verification-with-loop.k":
        source_class = "OPERATIONAL_BRIDGE"
    else:
        source_class = "TARGET_CLAIM"

    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [index for index, line in enumerate(lines) if start_re.match(line)]
    for ordinal, index in enumerate(starts):
        match = start_re.match(lines[index])
        assert match is not None
        kind = match.group(1)
        end = len(lines)
        for probe in range(index + 1, len(lines)):
            if stop_re.match(lines[probe]):
                end = probe
                break
        block = "\n".join(lines[index:end])
        attribute_text = " ".join(re.findall(r"\[[^\]]*\]", block))
        attributes = [
            name
            for name in attribute_names
            if re.search(rf"\b{re.escape(name)}\b", attribute_text)
        ]
        preview = re.sub(r"\s+", " ", block).strip()
        counts[(source_class, kind)] += 1
        for attribute in attributes:
            attribute_counts[(source_class, attribute)] += 1
        print(
            f"{source_class}\t{relative}:{index + 1}\t{kind}\t"
            f"attrs={','.join(attributes) or '-'}\t{preview}"
        )

print("COUNTS")
for (source_class, kind), count in sorted(counts.items()):
    print(f"{source_class}\t{kind}\t{count}")
print("ATTRIBUTE_COUNTS")
for (source_class, attribute), count in sorted(attribute_counts.items()):
    print(f"{source_class}\t{attribute}\t{count}")
