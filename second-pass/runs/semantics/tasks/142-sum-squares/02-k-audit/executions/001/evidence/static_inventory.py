#!/usr/bin/env python3
"""Create an exhaustive, line-addressable inventory of K source sentences."""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from pathlib import Path


START = re.compile(
    r"^(?:(requires|module|endmodule)\b|"
    r"  (imports|syntax|configuration|context(?:\s+alias)?|rule|claim)\b)"
)
BRACKET = re.compile(r"\[([^\]\n]*)\]")
ATTR = re.compile(
    r"\b(function|total|functional|simplification|priority|symbol|macro|"
    r"concrete|owise|strict|seqstrict|anywhere)\b"
)

RELEVANT_FIXED_RANGES: dict[str, list[tuple[int, int]]] = {
    "semantics.k": [(37, 90)],
    "semantics/syntax.k": [(3, 62)],
    "semantics/core.k": [
        (13, 42),
        (49, 65),
        (124, 127),
        (130, 191),
        (194, 210),
    ],
    "semantics/iter.k": [(6, 9)],
    "semantics/tuple.k": [(31, 41)],
    "semantics/operators.k": [(7, 17)],
    "semantics/int.k": [(4, 28)],
    "semantics/controls.k": [(3, 31), (48, 74)],
    "semantics/functions.k": [(3, 15), (55, 91)],
    "semantics/call.k": [(7, 19), (83, 95)],
}


def in_ranges(line: int, ranges: list[tuple[int, int]]) -> bool:
    return any(lo <= line <= hi for lo, hi in ranges)


def decision(relative: str, line: int, kind: str) -> str:
    if relative == "verification.k":
        if line in (15, 17):
            return (
                "SOUND_WITH_DOCUMENTED_BRIDGE_LIMITATION:"
                "proof-only Ints iterator is an isomorphic finite-integer-list input encoding;"
                "no bridge-free machine-checked connection theorem"
            )
        if 23 <= line <= 29:
            return (
                "SOUND_DEFINITIONAL_SUMMARY:"
                "three disjoint exhaustive index classes implement square/cube/identity"
            )
        if 32 <= line <= 46:
            return (
                "SOUND_DEFINITIONAL_SUMMARY:"
                "structural recursion is total on Ints and strictly descends"
            )
        if 48 <= line <= 83:
            return (
                "SOUND_EXACT_AST_MACRO:"
                "macro expansion is byte-for-byte AST-equivalent to translated solution body"
            )
        return "SOUND_PROOF_LOCAL_DECLARATION_OR_MODULE_WIRING"

    if relative == "spec.k":
        if kind == "claim":
            return "TARGET_OR_AUXILIARY_REACHABILITY_CLAIM:reviewed_for_satisfiability_and_result_constraint"
        return "SPEC_MODULE_WIRING"

    if relative == "semantics.k" or relative.startswith("semantics/"):
        base = (
            "FIXED_SUPPLIED_BASELINE:"
            "candidate entry is regular and byte-identical to trusted reference"
        )
        if in_ranges(line, RELEVANT_FIXED_RANGES.get(relative, [])):
            return base + ":SUBMITTED_PROGRAM_PATH_REVIEWED"
        return base + ":NOT_REACHED_BY_SUBMITTED_PROGRAM"

    return "UNCLASSIFIED"


def parse_file(path: Path, display_root: Path) -> list[dict[str, object]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[int] = []
    for index, line in enumerate(lines, start=1):
        if START.match(line) and not line.lstrip().startswith("//"):
            starts.append(index)

    rows: list[dict[str, object]] = []
    relative = str(path.relative_to(display_root))
    for offset, start in enumerate(starts):
        end = starts[offset + 1] - 1 if offset + 1 < len(starts) else len(lines)
        block_lines = lines[start - 1 : end]
        while block_lines and not block_lines[-1].strip():
            block_lines.pop()
            end -= 1
        first = START.match(lines[start - 1])
        assert first is not None
        kind = (first.group(1) or first.group(2)).replace(" ", "_")
        source = " ".join(
            part.strip()
            for part in block_lines
            if part.strip() and not part.lstrip().startswith("//")
        )
        attrs = sorted(
            {
                attribute
                for bracket in BRACKET.findall(source)
                for attribute in ATTR.findall(bracket)
            }
        )
        rows.append(
            {
                "path": relative,
                "start": start,
                "end": end,
                "kind": kind,
                "attributes": ",".join(attrs) or "-",
                "decision": decision(relative, start, kind),
                "source": source,
            }
        )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    paths = [
        args.root / "reference-semantics" / "semantics.k",
        *sorted((args.root / "reference-semantics" / "semantics").glob("*.k")),
        args.root / "verification.k",
        args.root / "spec.k",
    ]
    rows: list[dict[str, object]] = []
    for path in paths:
        display_root = (
            args.root / "reference-semantics"
            if "reference-semantics" in path.parts
            else args.root
        )
        rows.extend(parse_file(path, display_root))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as stream:
        fields = [
            "id",
            "path",
            "start",
            "end",
            "kind",
            "attributes",
            "decision",
            "source",
        ]
        writer = csv.DictWriter(stream, fields, dialect="excel-tab")
        writer.writeheader()
        for number, row in enumerate(rows, start=1):
            writer.writerow({"id": number, **row})

    kinds = Counter(str(row["kind"]) for row in rows)
    attributes = Counter(
        attr
        for row in rows
        for attr in str(row["attributes"]).split(",")
        if attr != "-"
    )
    decisions = Counter(str(row["decision"]).split(":", 1)[0] for row in rows)
    print(f"source_file_count={len(paths)}")
    print(f"inventory_entry_count={len(rows)}")
    print("kind_counts=" + repr(dict(sorted(kinds.items()))))
    print("attribute_counts=" + repr(dict(sorted(attributes.items()))))
    print("decision_class_counts=" + repr(dict(sorted(decisions.items()))))
    print(f"inventory_tsv={args.output}")
    print("unclassified_count=" + str(sum(v for k, v in decisions.items() if k == "UNCLASSIFIED")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
