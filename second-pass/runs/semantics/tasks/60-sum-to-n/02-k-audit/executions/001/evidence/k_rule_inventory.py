#!/usr/bin/env python3
"""Emit an exhaustive source-level inventory of K declarations and rules."""

from __future__ import annotations

import collections
import re
import sys
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
SOURCES = [
    ROOT / "reference-semantics" / "semantics.k",
    *sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]

START = re.compile(
    r"^(?:requires\b|module\b|endmodule\b|  imports\b|  "
    r"(?:syntax|configuration|context|rule|claim|alias)\b)"
)
KIND = re.compile(
    r"^\s*(requires|module|endmodule|imports|syntax|configuration|context|rule|claim|alias)\b"
)
ATTRS = (
    "function",
    "total",
    "functional",
    "simplification",
    "concrete",
    "priority",
    "owise",
    "macro",
    "macro-rec",
    "strict",
    "seqstrict",
    "symbol",
    "no-evaluators",
)


def blocks(path: Path):
    lines = path.read_text().splitlines()
    starts = [i for i, line in enumerate(lines) if START.match(line)]
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        block = lines[start:end]
        while block and (not block[-1].strip() or block[-1].lstrip().startswith("//")):
            block.pop()
        match = KIND.match(lines[start])
        if match is None:
            raise AssertionError((path, start + 1, lines[start]))
        yield start + 1, match.group(1), "\n".join(block)


def code(text: str) -> str:
    return "\n".join(f"    {line}" for line in text.splitlines())


def main() -> int:
    counts = collections.Counter()
    attr_counts = collections.Counter()
    opaque = []
    priority = []
    declarations = []

    for path in SOURCES:
        if not path.is_file():
            print(f"MISSING SOURCE: {path}", file=sys.stderr)
            return 1
        relative = path.relative_to(ROOT)
        file_blocks = list(blocks(path))
        declarations.append((relative, file_blocks))
        for line, kind, text in file_blocks:
            counts[kind] += 1
            for attr in ATTRS:
                if re.search(rf"(?<![A-Za-z0-9-]){re.escape(attr)}(?![A-Za-z0-9-])", text):
                    attr_counts[attr] += 1
            if "no-evaluators" in text:
                opaque.append((relative, line, text))
            if "priority(" in text:
                priority.append((relative, line, text))

    print("# Exhaustive K source inventory")
    print()
    print("Generated from fresh scratch sources. Every top-level `requires`, module/import,")
    print("syntax declaration, configuration, context, rule, claim, and alias is listed")
    print("verbatim with its source line. Multiline guards and attributes remain attached.")
    print()
    print("## Counts")
    print()
    for kind in (
        "requires",
        "module",
        "endmodule",
        "imports",
        "syntax",
        "configuration",
        "context",
        "rule",
        "claim",
        "alias",
    ):
        print(f"- {kind}: {counts[kind]}")
    print()
    print("Attribute-bearing declaration/rule block counts:")
    print()
    for attr in ATTRS:
        print(f"- {attr}: {attr_counts[attr]}")
    print()
    print("Per-file rule and declaration counts:")
    print()
    for path, file_blocks in declarations:
        file_counts = collections.Counter(kind for _, kind, _ in file_blocks)
        print(
            f"- `{path}`: syntax={file_counts['syntax']}, "
            f"configuration={file_counts['configuration']}, "
            f"context={file_counts['context']}, rule={file_counts['rule']}, "
            f"claim={file_counts['claim']}"
        )
    print()
    print("## Opaque/no-evaluator declarations")
    print()
    if not opaque:
        print("- None")
    for path, line, text in opaque:
        print(f"- `{path}:{line}`")
        print()
        print(code(text))
    print()
    print("## Priority-bearing rules")
    print()
    if not priority:
        print("- None")
    for path, line, text in priority:
        print(f"- `{path}:{line}`")
        print()
        print(code(text))
    print()
    print("## Complete declaration and rule listing")
    print()
    for path, file_blocks in declarations:
        print(f"### `{path}`")
        print()
        for line, kind, text in file_blocks:
            print(f"- Line {line}; `{kind}`")
            print()
            print(code(text))
            print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
