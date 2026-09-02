#!/usr/bin/env python3
"""Emit a source-derived inventory of every local K declaration."""

from __future__ import annotations

import re
from pathlib import Path


FILES = [
    Path("/candidate/semantic.k"),
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
]
START = re.compile(
    r'^\s*(requires\s+"|module\b|endmodule\b|imports\b|configuration\b|'
    r"syntax\b|rule\b|claim\b)"
)
ATTRIBUTES = (
    "function",
    "total",
    "functional",
    "simplification",
    "concrete",
    "priority",
    "owise",
    "trusted",
    "macro",
    "alias",
)


def declarations(path: Path) -> list[tuple[int, int, str]]:
    lines = path.read_text().splitlines()
    starts = [
        index
        for index, line in enumerate(lines)
        if START.match(line) and not line.lstrip().startswith("//")
    ]
    output = []
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        while end > start and not lines[end - 1].strip():
            end -= 1
        text = "\n".join(lines[start:end]).strip()
        output.append((start + 1, end, text))
    return output


def main() -> None:
    totals = {"syntax": 0, "configuration": 0, "rule": 0, "claim": 0}
    attribute_counts = {name: 0 for name in ATTRIBUTES}
    for path in FILES:
        print(f"FILE {path}")
        for number, (start, end, text) in enumerate(declarations(path), 1):
            first = text.splitlines()[0].lstrip()
            kind = first.split(maxsplit=1)[0]
            if kind in totals:
                totals[kind] += 1
            bracket_text = " ".join(re.findall(r"\[([^\]]*)\]", text))
            found = [
                name
                for name in ATTRIBUTES
                if re.search(rf"\b{name}\b", bracket_text)
            ]
            for name in ATTRIBUTES:
                attribute_counts[name] += len(
                    re.findall(rf"\b{name}\b", bracket_text)
                )
            flattened = " ".join(part.strip() for part in text.splitlines())
            print(
                f"DECL {number:02d} lines={start}-{end} kind={kind} "
                f"attrs={','.join(found) if found else '-'} :: {flattened}"
            )
        print()
    print("TOTALS " + " ".join(f"{key}={value}" for key, value in totals.items()))
    print(
        "ATTRIBUTE_DECLARATIONS "
        + " ".join(f"{key}={value}" for key, value in attribute_counts.items())
    )


if __name__ == "__main__":
    main()
