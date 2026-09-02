#!/usr/bin/env python3
"""Enumerate every K declaration/rule in the audited source set.

The output is a line-oriented inventory with source locations, attributes, and
the complete normalized declaration block. It intentionally does not infer
soundness; the review supplies that classification.
"""

from __future__ import annotations

import hashlib
import pathlib
import re
import sys
from collections import Counter


ROOT = pathlib.Path("/tmp/audit-work/proof")
PATHS = (
    [ROOT / "reference-semantics" / "semantics.k"]
    + sorted((ROOT / "reference-semantics" / "semantics").glob("*.k"))
    + [ROOT / "verification.k", ROOT / "spec.k"]
)
START = re.compile(
    r"^(?:"
    r"(requires)(?=\s+\")|"
    r"\s*(module|endmodule|imports|configuration|"
    r"syntax(?:\s+priority)?|rule|claim|context(?:\s+alias)?)\b"
    r")"
)
ATTR_NAMES = (
    "function",
    "total",
    "functional",
    "simplification",
    "macro",
    "priority",
    "owise",
    "symbol",
    "hook",
    "anywhere",
)


def normalized(block: list[str]) -> str:
    return "\\n".join(line.rstrip().replace("\t", "    ") for line in block)


def main() -> int:
    totals: Counter[str] = Counter()
    attr_totals: Counter[str] = Counter()
    entries: list[tuple[str, int, str, str, str]] = []

    for path in PATHS:
        raw = path.read_bytes()
        text = raw.decode("utf-8")
        rel = path.relative_to(ROOT).as_posix()
        print(
            "FILE"
            f"\t{rel}\tbytes={len(raw)}\tlines={len(text.splitlines())}"
            f"\tsha256={hashlib.sha256(raw).hexdigest()}"
        )
        lines = text.splitlines()
        starts: list[tuple[int, str]] = []
        for index, line in enumerate(lines):
            match = START.match(line)
            if match:
                starts.append((index, match.group(1) or match.group(2)))
        for position, (start, kind) in enumerate(starts):
            end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
            block = lines[start:end]
            # Strip comments/blank lines that belong before the next declaration
            # from the block tail without altering the inventoried source itself.
            while block and (not block[-1].strip() or block[-1].lstrip().startswith("//")):
                block = block[:-1]
            source = normalized(block)
            attrs = [name for name in ATTR_NAMES if re.search(rf"\b{name}\b", source)]
            totals[kind] += 1
            for attr in attrs:
                attr_totals[attr] += 1
            entries.append((rel, start + 1, kind, ",".join(attrs) or "-", source))

    print("\nSUMMARY")
    for kind in sorted(totals):
        print(f"kind={kind}\tcount={totals[kind]}")
    for attr in ATTR_NAMES:
        print(f"attribute={attr}\tcount={attr_totals[attr]}")
    print(f"inventory_entries={len(entries)}")

    print("\nENTRIES")
    for number, (path, line, kind, attrs, source) in enumerate(entries, 1):
        print(
            f"{number:04d}\t{path}:{line}\tkind={kind}\tattrs={attrs}"
            f"\tsource={source}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
