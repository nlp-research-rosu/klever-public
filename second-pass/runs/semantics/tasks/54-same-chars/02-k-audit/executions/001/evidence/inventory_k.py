#!/usr/bin/env python3
"""Emit a source-anchored inventory of every local K declaration and rule."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/candidate-source")
FILES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "spec.k",
]
ANCHOR = re.compile(
    r"^\s*(module|endmodule|imports|configuration|syntax|context|rule|claim)\b"
)


def declaration_blocks(lines: list[str]):
    anchors = [
        index
        for index, line in enumerate(lines)
        if ANCHOR.match(line) and not line.lstrip().startswith("//")
    ]
    for position, start in enumerate(anchors):
        end = anchors[position + 1] if position + 1 < len(anchors) else len(lines)
        yield start, lines[start:end]


global_counts: Counter[str] = Counter()
print("K SOURCE INVENTORY")
print("ROOT=/tmp/audit-work/candidate-source")
print(f"FILE_COUNT={len(FILES)}")

for path in FILES:
    lines = path.read_text(encoding="utf-8").splitlines()
    relative = path.relative_to(ROOT)
    local_counts: Counter[str] = Counter()
    print(f"\n===== FILE {relative} =====")
    for start, block_lines in declaration_blocks(lines):
        first = block_lines[0]
        kind_match = ANCHOR.match(first)
        assert kind_match is not None
        kind = kind_match.group(1).upper()
        block = "\n".join(block_lines)

        if kind == "SYNTAX":
            flags = ["SYNTAX"]
            if "[function" in block or "functional" in block:
                flags.append("FUNCTIONAL")
            if "total" in block:
                flags.append("TOTAL")
            if "symbol(" in block or "no-evaluators" in block:
                flags.append("OPAQUE_OR_SYMBOL")
        elif kind == "RULE":
            flags = ["RULE"]
            flags.append(
                "SIMPLIFICATION" if "simplification" in block else "ORDINARY"
            )
            if "priority(" in block:
                flags.append("PRIORITY")
            if "[owise]" in block:
                flags.append("OWISE")
            if "[concrete]" in block:
                flags.append("CONCRETE_ONLY_ATTRIBUTE")
        else:
            flags = [kind]

        for flag in flags:
            local_counts[flag] += 1
            global_counts[flag] += 1

        # The first source line is the stable enumeration anchor. Attribute
        # lines are included so priority/owise/concrete classification can be
        # checked directly without relying only on the generated flags.
        print(f"{relative}:{start + 1}: [{','.join(flags)}] {first.strip()}")
        for offset, continuation in enumerate(block_lines[1:], start + 2):
            stripped = continuation.strip()
            if (
                stripped.startswith("requires ")
                or stripped.startswith("[")
                or "priority(" in stripped
                or "simplification" in stripped
                or "no-evaluators" in stripped
                or "[concrete]" in stripped
            ):
                print(f"  {relative}:{offset}: {stripped}")

    print(
        "FILE_COUNTS "
        + " ".join(f"{key}={local_counts[key]}" for key in sorted(local_counts))
    )

print("\n===== GLOBAL COUNTS =====")
for key in sorted(global_counts):
    print(f"{key}={global_counts[key]}")
