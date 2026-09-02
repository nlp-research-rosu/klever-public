#!/usr/bin/env python3
"""Produce a line-addressable inventory of all K declarations and claims."""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOTS = [
    Path("/reference/reference-semantics/semantics.k"),
    *sorted(Path("/reference/reference-semantics/semantics").glob("*.k")),
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
]

START = re.compile(
    r"^\s*(configuration|syntax|context|rule|claim|module|endmodule|imports)\b"
)
TOP_REQUIRE = re.compile(r'^requires\s+"')


def records(path: Path):
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))
        elif TOP_REQUIRE.match(line):
            starts.append((index, "requires"))
    for position, (start, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        block = lines[start:end]
        while block and (not block[-1].strip() or block[-1].lstrip().startswith("//")):
            block.pop()
        text = " ".join(piece.strip() for piece in block if piece.strip())
        attrs = ",".join(
            sorted(
                {
                    attr
                    for attr in (
                        "function",
                        "functional",
                        "total",
                        "simplification",
                        "priority",
                        "owise",
                        "anywhere",
                        "macro",
                        "macro-rec",
                        "concrete",
                        "symbol",
                        "no-evaluators",
                        "strict",
                        "seqstrict",
                    )
                    if re.search(rf"\b{re.escape(attr)}\b", text)
                }
            )
        )
        if kind == "rule":
            if "simplification" in attrs:
                subtype = "simplification-rule"
            elif "priority" in attrs:
                subtype = "priority-rule"
            elif "owise" in attrs:
                subtype = "owise-rule"
            elif "concrete" in attrs:
                subtype = "concrete-rule"
            else:
                subtype = "ordinary-rule"
        elif kind == "syntax" and "no-evaluators" in attrs:
            subtype = "opaque-symbol-declaration"
        elif kind == "syntax" and "function" in attrs:
            subtype = "function-declaration"
        else:
            subtype = kind
        yield start + 1, kind, subtype, attrs or "-", text


def main() -> None:
    print("record_id\tfile\tline\tkind\tsubtype\tattributes\tstatement")
    counts: collections.Counter[tuple[str, str]] = collections.Counter()
    total = 0
    for path in ROOTS:
        display = str(path)
        for line, kind, subtype, attrs, text in records(path):
            total += 1
            counts[(display, subtype)] += 1
            safe = text.replace("\t", " ")
            print(
                f"K{total:04d}\t{display}\t{line}\t{kind}\t{subtype}\t"
                f"{attrs}\t{safe}"
            )
    print(f"# TOTAL_RECORDS={total}")
    for (path, subtype), count in sorted(counts.items()):
        print(f"# COUNT\t{path}\t{subtype}\t{count}")


if __name__ == "__main__":
    main()
