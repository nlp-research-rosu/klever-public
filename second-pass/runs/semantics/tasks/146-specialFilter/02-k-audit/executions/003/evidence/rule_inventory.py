#!/usr/bin/env python3
"""Emit an exhaustive declaration/rule inventory for all audited K sources."""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOTS = [
    ("supplied", Path("/reference/reference-semantics")),
    ("candidate", Path("/candidate")),
]
START = re.compile(
    r"^\s*(module|endmodule|imports|configuration|syntax|context|rule|claim)\b"
)


def classification(text: str) -> str:
    first = START.match(text)
    kind = first.group(1) if first else "other"
    tags = [kind]
    attribute_tags = [
        "function",
        "functional",
        "total",
        "no-evaluators",
        "symbol",
        "macro",
        "simplification",
        "concrete",
        "owise",
        "priority",
        "anywhere",
        "strict",
        "seqstrict",
    ]
    for tag in attribute_tags:
        if re.search(rf"\b{re.escape(tag)}\b", text):
            tags.append(tag)
    if kind == "rule" and not any(
        tag in tags
        for tag in ["macro", "simplification", "concrete", "owise", "priority"]
    ):
        tags.append("ordinary")
    return ",".join(tags)


def blocks(path: Path):
    lines = path.read_text().splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    for ordinal, start in enumerate(starts):
        end = starts[ordinal + 1] if ordinal + 1 < len(starts) else len(lines)
        block = "\n".join(lines[start:end]).rstrip()
        yield start + 1, block


def main() -> int:
    counters: collections.Counter[tuple[str, str]] = collections.Counter()
    total = 0
    for origin, root in ROOTS:
        if origin == "candidate":
            paths = [root / "verification.k", root / "spec.k"]
        else:
            paths = sorted(root.rglob("*.k"))
        for path in paths:
            for line_number, block in blocks(path):
                total += 1
                klass = classification(block)
                primary = klass.split(",", 1)[0]
                counters[(origin, primary)] += 1
                relative = path.relative_to(root)
                indented = "\n".join("    " + line for line in block.splitlines())
                print(
                    f"ENTRY {total:04d} origin={origin} "
                    f"file={relative} line={line_number} class={klass}"
                )
                print(indented)
    print(f"TOTAL_ENTRIES={total}")
    for (origin, kind), count in sorted(counters.items()):
        print(f"COUNT origin={origin} kind={kind} value={count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
