#!/usr/bin/env python3
"""Emit a line-numbered exhaustive K declaration/rule inventory.

Every source line is retained, while declaration headlines are separately
indexed and classified so multi-line rules and attributes remain auditable.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path("/tmp/audit-work/142-sum-squares")
SOURCES = [
    ROOT / "reference-semantics" / "semantics.k",
    *sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]
HEAD = re.compile(
    r"^\s*(requires|module|endmodule|imports|configuration|syntax|context|rule|claim)\b"
)


def tags(text: str) -> str:
    found = []
    for tag in (
        "function",
        "total",
        "functional",
        "simplification",
        "concrete",
        "priority",
        "owise",
        "anywhere",
        "macro",
        "macro-rec",
        "symbol",
        "no-evaluators",
        "strict",
        "seqstrict",
    ):
        if re.search(rf"\b{re.escape(tag)}\b", text):
            found.append(tag)
    if "rule" in text and "<k>" in text:
        found.append("operational")
    elif "rule" in text:
        found.append("equational")
    return ",".join(found) or "-"


def main() -> None:
    totals: dict[str, int] = {}
    print("EXHAUSTIVE K SOURCE INVENTORY")
    print(f"ROOT={ROOT}")
    for source in SOURCES:
        rel = source.relative_to(ROOT)
        lines = source.read_text(encoding="utf-8").splitlines()
        print(f"\n===== {rel} ({len(lines)} lines) =====")
        declarations = []
        for lineno, line in enumerate(lines, 1):
            match = HEAD.match(line)
            if match:
                kind = match.group(1)
                totals[kind] = totals.get(kind, 0) + 1
                declarations.append((lineno, kind, tags(line), line.strip()))
        print("DECLARATION INDEX")
        for lineno, kind, attrs, line in declarations:
            print(f"{lineno:04d} {kind:13s} [{attrs}] {line}")
        print("COMPLETE NUMBERED SOURCE")
        for lineno, line in enumerate(lines, 1):
            print(f"{lineno:04d}: {line}")
    print("\n===== GLOBAL HEADLINE COUNTS =====")
    for kind in sorted(totals):
        print(f"{kind}={totals[kind]}")


if __name__ == "__main__":
    main()
