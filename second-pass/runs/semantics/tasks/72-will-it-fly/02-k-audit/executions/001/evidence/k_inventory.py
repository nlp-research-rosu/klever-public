#!/usr/bin/env python3
"""Produce a complete statement inventory for the audited K source tree."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


WORK = Path("/tmp/audit-work/72-will-it-fly")
OUT_TSV = Path("/audit-output/evidence/k-statement-inventory.tsv")
OUT_MD = Path("/audit-output/evidence/k-statement-inventory.md")
KINDS = ("syntax", "rule", "context", "configuration", "claim")
START_RE = re.compile(r"^\s*(syntax|rule|context|configuration|claim)\b")
BOUNDARY_RE = re.compile(
    r"^\s*(?:syntax|rule|context|configuration|claim|module|endmodule)\b"
)
ATTR_RE = re.compile(r"\[([^\]]+)\]")

# Lines that contribute to execution of this closed program or to its entry
# claims. The remaining fixed-semantics statements are unreachable from the
# submitted syntax and initial configurations.
RELEVANT_INTERVALS = {
    "reference-semantics/semantics/syntax.k": [(9, 61)],
    "reference-semantics/semantics/core.k": [
        (13, 42), (49, 60), (68, 70), (117, 127), (130, 181),
        (183, 225),
    ],
    "reference-semantics/semantics/iter.k": [(8, 8)],
    "reference-semantics/semantics/operators.k": [(10, 20), (34, 42)],
    "reference-semantics/semantics/int.k": [(7, 7), (22, 27)],
    "reference-semantics/semantics/bool.k": [(13, 25)],
    "reference-semantics/semantics/list.k": [(8, 10), (27, 28)],
    "reference-semantics/semantics/subscript.k": [(43, 114)],
    "reference-semantics/semantics/functions.k": [(8, 20), (62, 91)],
    "reference-semantics/semantics/builtins.k": [(17, 56)],
    "reference-semantics/semantics/call.k": [(18, 32), (34, 50), (69, 75)],
}


def relevant(path: str, start: int, end: int) -> bool:
    return any(
        start <= hi and end >= lo
        for lo, hi in RELEVANT_INTERVALS.get(path, [])
    )


def normalize(lines: list[str]) -> str:
    while lines and not lines[-1].strip():
        lines.pop()
    while lines and lines[-1].lstrip().startswith("//"):
        lines.pop()
        while lines and not lines[-1].strip():
            lines.pop()
    return " ".join(" ".join(lines).split())


def inventory_file(path: Path) -> list[dict[str, str | int]]:
    rel = path.relative_to(WORK).as_posix()
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [
        index for index, line in enumerate(lines)
        if START_RE.match(line)
    ]
    rows: list[dict[str, str | int]] = []

    for index in starts:
        match = START_RE.match(lines[index])
        assert match is not None
        end_index = index + 1
        while end_index < len(lines) and not BOUNDARY_RE.match(lines[end_index]):
            end_index += 1
        statement_lines = lines[index:end_index]
        statement = normalize(statement_lines)
        actual_end = index + max(1, len(statement_lines))
        attrs = "; ".join(ATTR_RE.findall(statement))

        if rel == "verification.k":
            disposition = "candidate proof extension; individually reviewed"
        elif rel == "spec.k":
            disposition = "candidate entry claim; adequacy reviewed"
        elif relevant(rel, index + 1, actual_end):
            disposition = "fixed supplied semantics; used/reachable"
        else:
            disposition = "fixed supplied semantics; unreachable from closed submitted program"

        opaque = (
            "yes" if "no-evaluators" in statement
            or ("symbol(" in statement and match.group(1) == "syntax")
            else "no"
        )
        rows.append(
            {
                "file": rel,
                "start": index + 1,
                "end": actual_end,
                "kind": match.group(1),
                "attributes": attrs,
                "opaque": opaque,
                "disposition": disposition,
                "statement": statement,
            }
        )
    return rows


def main() -> int:
    paths = sorted((WORK / "reference-semantics").rglob("*.k"))
    paths += [WORK / "verification.k", WORK / "spec.k"]
    rows = [row for path in paths for row in inventory_file(path)]

    fields = [
        "file", "start", "end", "kind", "attributes",
        "opaque", "disposition", "statement",
    ]
    with OUT_TSV.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, dialect="excel-tab")
        writer.writeheader()
        writer.writerows(rows)

    with OUT_MD.open("w", encoding="utf-8") as stream:
        stream.write("# Exhaustive K statement inventory\n\n")
        stream.write(
            "| # | File:line | Kind | Attributes | Opaque | Disposition | Statement |\n"
        )
        stream.write("|---:|---|---|---|---|---|---|\n")
        for number, row in enumerate(rows, 1):
            values = [
                str(number),
                f"{row['file']}:{row['start']}",
                str(row["kind"]),
                str(row["attributes"]) or "—",
                str(row["opaque"]),
                str(row["disposition"]),
                str(row["statement"]),
            ]
            escaped = [value.replace("|", r"\|") for value in values]
            stream.write("| " + " | ".join(escaped) + " |\n")

    counts = Counter(str(row["kind"]) for row in rows)
    dispositions = Counter(str(row["disposition"]) for row in rows)
    print(f"files={len(paths)}")
    print(f"statements={len(rows)}")
    for kind in KINDS:
        print(f"{kind}={counts[kind]}")
    for name, count in sorted(dispositions.items()):
        print(f"disposition[{name}]={count}")
    print(f"tsv={OUT_TSV}")
    print(f"markdown={OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
