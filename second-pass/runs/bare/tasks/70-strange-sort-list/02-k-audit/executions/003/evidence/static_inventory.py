#!/usr/bin/env python3
"""Mechanical inventory of every local declaration and rule."""

from __future__ import annotations

import re
from pathlib import Path


def inventory(path: Path) -> None:
    lines = path.read_text().splitlines()
    print(f"FILE {path}")
    for line_number, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("syntax "):
            declaration = stripped
            cursor = line_number
            while cursor < len(lines):
                following = lines[cursor].strip()
                if not following.startswith("|"):
                    break
                declaration += " " + following
                cursor += 1
            attrs = re.findall(r"\[([^\]]+)\]", declaration)
            print(
                f"SYNTAX line={line_number} attrs={attrs or ['none']} "
                f"text={declaration}"
            )
        elif stripped == "configuration":
            print(f"CONFIGURATION line={line_number}")
        elif stripped.startswith("rule "):
            rule_text = stripped
            cursor = line_number
            while cursor < len(lines):
                following = lines[cursor]
                following_stripped = following.strip()
                if (
                    not following_stripped
                    or following_stripped.startswith("//")
                    or re.match(
                        r"(syntax|rule|claim|configuration|module|endmodule|imports|requires)\b",
                        following_stripped,
                    )
                ):
                    break
                rule_text += " " + following_stripped
                cursor += 1
            attrs = re.findall(r"\[([^\]]+)\]", rule_text)
            print(
                f"RULE line={line_number} attrs={attrs or ['none']} "
                f"text={rule_text}"
            )
    print()


for source in (
    Path("/candidate/semantic.k"),
    Path("/candidate/verification.k"),
):
    inventory(source)

combined = (
    Path("/candidate/semantic.k").read_text()
    + Path("/candidate/verification.k").read_text()
)
for attribute in (
    "total",
    "functional",
    "simplification",
    "concrete",
    "owise",
    "priority",
    "priorities",
    "opaque",
):
    print(f"ATTRIBUTE {attribute} count={combined.count(attribute)}")

mpy = Path("/candidate/solution.mpy").read_text()
constructors = sorted(set(re.findall(r"\b([A-Z][A-Za-z0-9]*)\s*\(", mpy)))
print(f"SOLUTION CONSTRUCTORS {constructors}")
rule_pattern = re.compile(r"(?m)^\s*rule\b")
semantic_rule_count = len(
    rule_pattern.findall(Path("/candidate/semantic.k").read_text())
)
verification_rule_count = len(
    rule_pattern.findall(Path("/candidate/verification.k").read_text())
)
print(f"SEMANTIC RULE COUNT {semantic_rule_count}")
print(f"VERIFICATION RULE COUNT {verification_rule_count}")
