#!/usr/bin/env python3
"""Emit a line-anchored inventory of all local K declarations and rules."""

from __future__ import annotations

import re
from pathlib import Path


FILES = [
    Path("/tmp/audit-work/candidate-src/semantic.k"),
    Path("/tmp/audit-work/candidate-src/verification.k"),
    Path("/tmp/audit-work/candidate-src/spec.k"),
]


def blocks(lines: list[str], starter: re.Pattern[str]) -> list[tuple[int, int, str]]:
    starts = [index for index, line in enumerate(lines) if starter.match(line)]
    result = []
    for position, start in enumerate(starts):
        limit = starts[position + 1] if position + 1 < len(starts) else len(lines)
        # Stop a rule/claim/declaration before endmodule or the next declaration.
        end = start + 1
        while end < limit and not re.match(
            r"^\s*(?:rule|claim|syntax|configuration|module|endmodule)\b",
            lines[end],
        ):
            end += 1
        text = " ".join(line.strip() for line in lines[start:end] if line.strip())
        result.append((start + 1, end, text))
    return result


def main() -> None:
    for path in FILES:
        lines = path.read_text().splitlines()
        print(f"FILE {path}")
        print("MODULE/IMPORT INVENTORY")
        for number, line in enumerate(lines, 1):
            if re.match(r"^\s*(requires|module|imports|endmodule)\b", line):
                print(f"{number}: {line.strip()}")
        print("SYNTAX DECLARATIONS")
        for start, end, text in blocks(lines, re.compile(r"^\s*syntax\b")):
            print(f"{start}-{end}: {text}")
        print("CONFIGURATIONS")
        for start, end, text in blocks(lines, re.compile(r"^\s*configuration\b")):
            print(f"{start}-{end}: {text}")
        print("RULES")
        for index, (start, end, text) in enumerate(
            blocks(lines, re.compile(r"^\s*rule\b")), 1
        ):
            print(f"{index:02d} lines {start}-{end}: {text}")
        print("CLAIMS")
        for index, (start, end, text) in enumerate(
            blocks(lines, re.compile(r"^\s*claim\b")), 1
        ):
            print(f"{index:02d} lines {start}-{end}: {text}")
        print()

    combined = "\n".join(path.read_text() for path in FILES)
    attributes = [
        "function",
        "total",
        "functional",
        "simplification",
        "concrete",
        "priority",
        "owise",
        "macro",
        "alias",
        "trusted",
        "opaque",
        "strict",
        "seqstrict",
    ]
    print("ATTRIBUTE COUNTS")
    for attribute in attributes:
        count = len(re.findall(rf"\b{re.escape(attribute)}\b", combined))
        print(f"{attribute}={count}")

    solution = Path("/tmp/audit-work/candidate-src/solution.mpy").read_text()
    constructors = sorted(set(re.findall(r"\b([A-Z][A-Za-z0-9]*)\(", solution)))
    print("SOLUTION CONSTRUCTORS")
    print(",".join(constructors))
    print("SOLUTION OPERATORS")
    for operator in ("+", "-", "*", "%", "<", ">", "=="):
        print(f"{operator}={solution.count(chr(34) + operator + chr(34))}")
    print("INVENTORY_COMPLETE")


if __name__ == "__main__":
    main()
