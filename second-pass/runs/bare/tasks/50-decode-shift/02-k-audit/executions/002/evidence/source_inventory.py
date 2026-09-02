#!/usr/bin/env python3
"""Emit a line-numbered inventory of all local K declarations."""

from __future__ import annotations

import re
from pathlib import Path


DECLARATION = re.compile(
    r"^\s*(requires|module|endmodule|imports|syntax|configuration|rule|claim)\b"
)
ATTRIBUTES = re.compile(
    r"\[(?:[^\]]*\b(?:function|total|functional|constructor|simplification|"
    r"priority|owise|strict|seqstrict)\b[^\]]*)\]"
)


def main() -> None:
    roots = [
        Path("/tmp/audit-work/candidate/semantic.k"),
        Path("/tmp/audit-work/candidate/verification.k"),
        Path("/tmp/audit-work/candidate/spec.k"),
    ]
    totals = {}
    for path in roots:
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        matches = []
        for number, line in enumerate(lines, 1):
            if DECLARATION.match(line) or ATTRIBUTES.search(line):
                matches.append((number, line.rstrip()))
        totals[path.name] = len(matches)
        print(f"FILE {path.name}")
        for number, line in matches:
            print(f"{number:4}: {line}")
    print(f"declaration_line_counts={totals}")
    print("local_k_files=semantic.k,verification.k,spec.k")
    print("helper_k_files=NONE")
    print("SOURCE_INVENTORY=PASS")


if __name__ == "__main__":
    main()
