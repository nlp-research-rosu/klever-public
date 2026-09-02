#!/usr/bin/env python3
"""Produce a line-addressed inventory of supplied and proof-local K declarations."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path


START = re.compile(
    r"^\s*(?P<kind>syntax|rule|claim|configuration|context)\b"
)
STOP = re.compile(r"^\s*(?:module|endmodule|imports|requires)\b")
ATTR = re.compile(r"\[([^\]]+)\]")


def collapse(lines: list[str]) -> str:
    return re.sub(r"\s+", " ", " ".join(line.strip() for line in lines)).strip()


def declarations(path: Path):
    lines = path.read_text().splitlines()
    starts = [
        index
        for index, line in enumerate(lines)
        if START.match(line)
    ]
    for ordinal, start in enumerate(starts):
        end = starts[ordinal + 1] if ordinal + 1 < len(starts) else len(lines)
        for probe in range(start + 1, end):
            if STOP.match(lines[probe]):
                end = probe
                break
        statement = collapse(lines[start:end])
        match = START.match(lines[start])
        assert match is not None
        kind = match.group("kind")
        attrs = ",".join(ATTR.findall(statement))
        yield start + 1, kind, attrs, statement


def classification(path: Path, kind: str, attrs: str, statement: str) -> str:
    if path.name == "verification.k":
        if "#checkIfLastChar" in statement:
            return "PROOF_LOCAL_ENTRY_ADAPTER"
        if "simplification" in attrs:
            return "PROOF_LOCAL_DERIVED_LEMMA"
        return "PROOF_LOCAL_DECLARATION"
    if kind == "rule":
        return "SUPPLIED_FIXED_SEMANTICS_RULE"
    if kind == "syntax" and (
        "function" in attrs or "functional" in attrs
    ):
        if "symbol(" in attrs or "no-evaluators" in attrs:
            return "SUPPLIED_OPAQUE_OR_EXTERNAL_FUNCTION"
        return "SUPPLIED_FIXED_FUNCTION_DECLARATION"
    return "SUPPLIED_FIXED_DECLARATION"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    args = parser.parse_args()

    paths = sorted(
        [
            args.root / "reference-semantics" / "semantics.k",
            *(args.root / "reference-semantics" / "semantics").glob("*.k"),
            args.root / "verification.k",
        ],
        key=lambda item: str(item),
    )
    counts: Counter[tuple[str, str]] = Counter()
    print("id\tfile\tline\tkind\tattributes\tclassification\tstatement")
    item_id = 0
    for path in paths:
        for line, kind, attrs, statement in declarations(path):
            item_id += 1
            rel = path.relative_to(args.root)
            category = classification(path, kind, attrs, statement)
            counts[(kind, category)] += 1
            escaped = statement.replace("\t", " ").replace("\n", " ")
            print(
                f"K{item_id:04d}\t{rel}\t{line}\t{kind}\t{attrs}\t"
                f"{category}\t{escaped}"
            )

    print(f"# total={item_id}")
    for (kind, category), count in sorted(counts.items()):
        print(f"# count kind={kind} classification={category} value={count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
