#!/usr/bin/env python3
"""Emit a source-location inventory of K declarations and sentence starts."""

from __future__ import annotations

import re
from pathlib import Path


ROOTS = [
    Path("/reference/reference-semantics/semantics.k"),
    *sorted(Path("/reference/reference-semantics/semantics").glob("*.k")),
    Path("/tmp/audit-work/reconstruction/verification.k"),
    Path("/tmp/audit-work/reconstruction/spec.k"),
]
START = re.compile(
    r"^\s*(requires|module|endmodule|imports|configuration|syntax|context|"
    r"rule|claim|priority)\b"
)


def main() -> int:
    counts: dict[str, int] = {}
    item = 0
    for path in ROOTS:
        relative = (
            str(path).removeprefix("/reference/reference-semantics/")
            .removeprefix("/tmp/audit-work/reconstruction/")
        )
        for line_number, line in enumerate(path.read_text().splitlines(), 1):
            match = START.match(line)
            if not match:
                continue
            item += 1
            kind = match.group(1)
            counts[kind] = counts.get(kind, 0) + 1
            attrs = ",".join(
                attribute
                for attribute in (
                    "function",
                    "total",
                    "functional",
                    "macro",
                    "simplification",
                    "concrete",
                    "owise",
                    "priority",
                    "symbol",
                    "no-evaluators",
                )
                if attribute in line
            )
            text = " ".join(line.split())
            print(f"K{item:04d}\t{relative}:{line_number}\t{kind}\t{attrs}\t{text}")
    print("COUNTS")
    for kind, count in sorted(counts.items()):
        print(f"{kind}\t{count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
