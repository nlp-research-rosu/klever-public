#!/usr/bin/env python3
"""Mechanical inventory of every K declaration/rule in the audited sources."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path("/tmp/audit-work/62-derivative")
SOURCES = [
    ROOT / "reference-semantics" / "semantics.k",
    *sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]
START = re.compile(
    r"^\s*(configuration|syntax|rule|context|claim|macro|alias)\b"
)
BOUNDARY = re.compile(
    r"^\s*(module|endmodule|imports|configuration|syntax|rule|context|claim|macro|alias)\b"
)


def tag(path: Path, kind: str, text: str) -> str:
    relative = path.relative_to(ROOT).as_posix()
    if relative == "verification.k":
        return "PROOF_LOCAL_REVIEW_REQUIRED"
    if relative == "spec.k":
        return "CLAIM_ADEQUACY_REVIEW_REQUIRED"
    if kind in {"rule", "context", "configuration"}:
        return "SUPPLIED_FIXED_RULE"
    return "SUPPLIED_FIXED_DECLARATION"


def one_line(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip()).replace("\t", " ")


def main() -> int:
    rows: list[tuple[str, int, int, str, str, str, str]] = []
    counters: dict[str, int] = {}
    for path in SOURCES:
        lines = path.read_text().splitlines()
        starts = [
            index
            for index, line in enumerate(lines)
            if START.match(line)
        ]
        for position, start in enumerate(starts):
            end_limit = starts[position + 1] if position + 1 < len(starts) else len(lines)
            end = end_limit
            for candidate in range(start + 1, end_limit):
                if BOUNDARY.match(lines[candidate]) and not START.match(lines[candidate]):
                    end = candidate
                    break
            # Drop trailing blank/comment lines before the next declaration.
            while end > start + 1 and (
                not lines[end - 1].strip() or lines[end - 1].lstrip().startswith("//")
            ):
                end -= 1
            text = "\n".join(lines[start:end])
            match = START.match(lines[start])
            assert match
            kind = match.group(1)
            counters[kind] = counters.get(kind, 0) + 1
            attributes = []
            for attribute in [
                "function",
                "total",
                "functional",
                "simplification",
                "concrete",
                "owise",
                "priority",
                "macro",
                "no-evaluators",
                "symbol",
            ]:
                if re.search(rf"\b{re.escape(attribute)}\b", text):
                    attributes.append(attribute)
            rows.append(
                (
                    path.relative_to(ROOT).as_posix(),
                    start + 1,
                    end,
                    kind,
                    ",".join(attributes) or "-",
                    tag(path, kind, text),
                    one_line(text),
                )
            )

    print("source\tstart_line\tend_line\tkind\tattributes\taudit_class\tdeclaration")
    for row in rows:
        print("\t".join(map(str, row)))
    print(f"# TOTAL={len(rows)} COUNTS={dict(sorted(counters.items()))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
