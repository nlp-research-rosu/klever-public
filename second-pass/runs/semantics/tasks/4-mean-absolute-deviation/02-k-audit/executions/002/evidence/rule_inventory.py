#!/usr/bin/env python3
"""Mechanical inventory of K declarations and rules, with complete rule blocks."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/candidate")
FILES = [
    ROOT / "reference-semantics" / "semantics.k",
    *sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]

START = re.compile(
    r"^\s*(module|endmodule|imports|requires|configuration|syntax|context|"
    r"rule|claim|alias)\b"
)
RULE_START = re.compile(r"^\s*(rule|claim)\b")
TOP_LEVEL = re.compile(
    r"^\s*(module|endmodule|imports|requires|configuration|syntax|context|"
    r"rule|claim|alias)\b"
)


def main() -> None:
    declaration_count = 0
    rule_count = 0
    claim_count = 0
    for path in FILES:
        lines = path.read_text().splitlines()
        print(f"\n=== {path.relative_to(ROOT)} ({len(lines)} lines) ===")
        index = 0
        while index < len(lines):
            line = lines[index]
            if not START.match(line):
                index += 1
                continue
            start = index
            kind_match = re.match(r"^\s*(\w+)", line)
            kind = kind_match.group(1) if kind_match else "unknown"
            if RULE_START.match(line):
                index += 1
                while index < len(lines) and not TOP_LEVEL.match(lines[index]):
                    index += 1
            else:
                # Syntax/configuration declarations often continue on indented lines.
                index += 1
                while (
                    index < len(lines)
                    and lines[index].strip()
                    and not TOP_LEVEL.match(lines[index])
                ):
                    index += 1
            block = lines[start:index]
            print(f"{path.relative_to(ROOT)}:{start + 1}: [{kind}]")
            for block_line in block:
                print(f"  {block_line}")
            declaration_count += 1
            rule_count += kind == "rule"
            claim_count += kind == "claim"
    print(
        f"\nTOTAL declaration_blocks={declaration_count} "
        f"rules={rule_count} claims={claim_count}"
    )


if __name__ == "__main__":
    main()
