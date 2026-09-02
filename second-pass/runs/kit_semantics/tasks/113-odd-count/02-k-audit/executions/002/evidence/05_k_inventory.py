#!/usr/bin/env python3
"""Line-preserving inventory of supplied and candidate K declarations."""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOTS = [
    Path("/reference/reference-semantics/semantics.k"),
    *sorted(Path("/reference/reference-semantics/semantics").glob("*.k")),
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
]

START = re.compile(
    r'^(?:requires\s+"|module\s+|endmodule\b|  (?:imports\b|configuration\b|syntax\b|context\b|rule\b|claim\b|priority\b))'
)


def kind_of(first: str, block: str) -> str:
    stripped = first.strip()
    if stripped.startswith("syntax "):
        tags = ["syntax"]
        for attribute in (
            "function",
            "functional",
            "total",
            "macro",
            "macro-rec",
            "symbol",
            "no-evaluators",
        ):
            if re.search(rf"\b{re.escape(attribute)}\b", block):
                tags.append(attribute)
        if "symbol" in tags and "no-evaluators" in tags:
            tags.append("opaque")
        return "+".join(tags)
    if stripped.startswith("rule "):
        tags = ["rule"]
        for attribute in (
            "simplification",
            "priority",
            "owise",
            "concrete",
            "macro",
            "macro-rec",
        ):
            if re.search(rf"\b{re.escape(attribute)}\b", block):
                tags.append(attribute)
        if len(tags) == 1:
            tags.append("ordinary")
        return "+".join(tags)
    return stripped.split(maxsplit=1)[0] if stripped else "blank"


grand: collections.Counter[str] = collections.Counter()
for path in ROOTS:
    lines = path.read_text().splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    starts.append(len(lines))
    file_counts: collections.Counter[str] = collections.Counter()
    print(f"FILE {path} lines={len(lines)}")
    for left, right in zip(starts, starts[1:]):
        first = lines[left]
        block_lines = lines[left:right]
        while block_lines and (
            not block_lines[-1].strip() or block_lines[-1].lstrip().startswith("//")
        ):
            block_lines.pop()
        block = "\n".join(block_lines)
        kind = kind_of(first, block)
        file_counts[kind] += 1
        grand[kind] += 1
        print(f"DECL line={left + 1} end={left + len(block_lines)} kind={kind}")
        for line in block_lines:
            print(f"  {line}")
    print("FILE_COUNTS " + " ".join(f"{key}={value}" for key, value in sorted(file_counts.items())))

print("GRAND_COUNTS " + " ".join(f"{key}={value}" for key, value in sorted(grand.items())))
