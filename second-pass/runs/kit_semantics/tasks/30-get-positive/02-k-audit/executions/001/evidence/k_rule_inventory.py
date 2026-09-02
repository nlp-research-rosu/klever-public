#!/usr/bin/env python3
"""Exhaustive textual inventory of K declarations, contexts, rules, and claims."""

from __future__ import annotations

import re
from pathlib import Path


ROOTS = [
    Path("/reference/reference-semantics/semantics.k"),
    *sorted(Path("/reference/reference-semantics/semantics").glob("*.k")),
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
    Path("/candidate/spec-connection.k"),
]

START = re.compile(
    r"^(?:(requires|module|endmodule)\b|  (imports|configuration|syntax|context|rule|claim)\b)"
)


def category(first_line: str) -> str:
    match = START.match(first_line)
    if not match:
        return "unknown"
    return match.group(1) or match.group(2)


def main() -> int:
    totals: dict[str, int] = {}
    attribute_totals: dict[str, int] = {}
    for path in ROOTS:
        lines = path.read_text().splitlines()
        starts = [index for index, line in enumerate(lines) if START.match(line)]
        entries = []
        for position, start in enumerate(starts):
            end = starts[position + 1] if position + 1 < len(starts) else len(lines)
            kind = category(lines[start])
            if kind in {"requires", "module", "endmodule", "imports"}:
                end = start + 1
            text = "\n".join(lines[start:end]).rstrip()
            entries.append((start + 1, kind, text))
            totals[kind] = totals.get(kind, 0) + 1
            for attribute in (
                "function", "functional", "total", "no-evaluators",
                "concrete", "simplification", "priority", "owise", "macro",
                "strict", "seqstrict", "symbol",
            ):
                if re.search(rf"\b{re.escape(attribute)}\b", text):
                    attribute_totals[attribute] = attribute_totals.get(attribute, 0) + 1

        print(f"FILE {path} ENTRIES={len(entries)}")
        for line_number, kind, text in entries:
            flattened = " ".join(part.strip() for part in text.splitlines() if part.strip())
            print(f"{path}:{line_number}\t{kind}\t{flattened}")

    print(f"TOTALS={dict(sorted(totals.items()))}")
    print(f"ATTRIBUTE_ENTRY_TOTALS={dict(sorted(attribute_totals.items()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
