#!/usr/bin/env python3
"""Emit a complete declaration-start inventory for all proof K sources."""

from __future__ import annotations

import collections
import hashlib
import re
from pathlib import Path


FILES = sorted(
    Path("/reference/reference-semantics").rglob("*.k"),
    key=lambda path: path.as_posix(),
) + [Path("/candidate/verification.k"), Path("/candidate/spec.k")]

START = re.compile(
    r"^\s*(configuration|syntax|context(?:\s+alias)?|rule|claim)\b"
)
BOUNDARY = re.compile(
    r"^\s*(?:configuration|syntax|context(?:\s+alias)?|rule|claim|"
    r"module|endmodule|imports|requires\s+\")\b"
)
ATTRIBUTES = [
    "function",
    "total",
    "functional",
    "simplification",
    "concrete",
    "owise",
    "macro",
    "token",
    "strict",
    "seqstrict",
    "bracket",
    "no-evaluators",
]


def normalize(lines: list[str]) -> str:
    text = " ".join(line.strip() for line in lines)
    return re.sub(r"\s+", " ", text).strip()


overall: collections.Counter[str] = collections.Counter()
print("# Complete K declaration inventory")
print(
    "# Each record identifies a declaration start, its complete source span "
    "up to the next declaration boundary, attributes, and normalized digest."
)

for path in FILES:
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1).replace(" ", "-")))

    counts: collections.Counter[str] = collections.Counter()
    records: list[tuple[int, int, str, list[str], str, str]] = []
    for position, (start, kind) in enumerate(starts):
        if position + 1 < len(starts):
            end = starts[position + 1][0]
        else:
            end = len(lines)
        # Module/import/end boundaries before the next declaration should not
        # be absorbed into the current declaration.
        for candidate in range(start + 1, end):
            if BOUNDARY.match(lines[candidate]):
                end = candidate
                break
        block = lines[start:end]
        text = normalize(block)
        attrs = [
            attr
            for attr in ATTRIBUTES
            if re.search(rf"(?<![A-Za-z-]){re.escape(attr)}(?![A-Za-z-])", text)
        ]
        priority = re.search(r"priority\(([-0-9]+)\)", text)
        if priority:
            attrs.append(f"priority({priority.group(1)})")
        if kind == "rule":
            if "<" in text.split("=>", 1)[0]:
                semantic_class = "operational-rule"
            elif "simplification" in attrs:
                semantic_class = "simplification-rule"
            else:
                semantic_class = "equation/ordinary-rule"
        elif kind == "syntax":
            semantic_class = "function-syntax" if "function" in attrs else "syntax"
        else:
            semantic_class = kind
        digest = hashlib.sha256(text.encode()).hexdigest()[:16]
        records.append(
            (start + 1, end, kind, attrs, semantic_class, digest + " " + text)
        )
        counts[kind] += 1
        overall[kind] += 1

    display = path.as_posix()
    print(f"\n## {display}")
    print(
        "counts "
        + " ".join(f"{kind}={counts[kind]}" for kind in sorted(counts))
    )
    for line_start, line_end, kind, attrs, semantic_class, payload in records:
        attr_text = ",".join(attrs) if attrs else "-"
        print(
            f"{line_start}-{line_end} | {kind} | {semantic_class} | "
            f"attrs={attr_text} | {payload}"
        )

print("\n# OVERALL")
print(" ".join(f"{kind}={overall[kind]}" for kind in sorted(overall)))
