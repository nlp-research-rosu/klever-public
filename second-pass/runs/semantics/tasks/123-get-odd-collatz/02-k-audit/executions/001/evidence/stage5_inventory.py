#!/usr/bin/env python3
"""Emit a source-complete inventory of K declarations and rule/claim blocks."""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path("/tmp/audit-work/123-get-odd-collatz/proof-src")
SOURCES = sorted((ROOT / "reference-semantics").rglob("*.k"))
SOURCES.extend([ROOT / "verification.k", ROOT / "spec.k"])
START = re.compile(
    r"^\s*(module|imports|configuration|syntax|context|rule|claim|priority)\b"
)
FILE_REQUIRE = re.compile(r'^requires\s+"')
ENDMODULE = re.compile(r"^\s*endmodule\b")


def flags(kind: str, block: str) -> list[str]:
    found: list[str] = []
    for name, pattern in [
        ("function", r"\bfunction\b"),
        ("functional", r"\bfunctional\b"),
        ("total", r"\btotal\b"),
        ("opaque-no-evaluators", r"\bno-evaluators\b"),
        ("symbol", r"\bsymbol(?:\(|\b)"),
        ("macro", r"\bmacro(?:-rec)?\b"),
        ("strict", r"\b(?:seq)?strict(?:\(|\b)"),
        ("priority", r"\bpriority\("),
        ("owise", r"\bowise\b"),
        ("simplification", r"\bsimplification\b"),
        ("concrete", r"\bconcrete\b"),
        ("hook", r"\bhook\("),
    ]:
        if re.search(pattern, block):
            found.append(name)
    if kind == "rule":
        found.append("operational" if "<k>" in block else "equational")
    return found


records: list[dict[str, object]] = []
for source in SOURCES:
    lines = source.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        if FILE_REQUIRE.match(line):
            starts.append((index, "requires"))
            continue
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))
        elif ENDMODULE.match(line):
            starts.append((index, "endmodule"))
    for position, (index, kind) in enumerate(starts):
        if kind == "endmodule":
            continue
        next_index = (
            starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        )
        block_lines = lines[index:next_index]
        while block_lines and (
            not block_lines[-1].strip()
            or block_lines[-1].lstrip().startswith("//")
        ):
            block_lines.pop()
        block = "\n".join(block_lines)
        relative = str(source.relative_to(ROOT))
        records.append(
            {
                "id": len(records) + 1,
                "file": relative,
                "line": index + 1,
                "kind": kind,
                "flags": flags(kind, block),
                "text": block,
            }
        )

print("id\tfile\tline\tkind\tflags\ttext")
for record in records:
    escaped = str(record["text"]).replace("\\", "\\\\").replace("\t", "\\t").replace(
        "\n", "\\n"
    )
    print(
        f'{record["id"]}\t{record["file"]}\t{record["line"]}\t'
        f'{record["kind"]}\t{",".join(record["flags"])}\t{escaped}'
    )

kind_counts = Counter(str(record["kind"]) for record in records)
flag_counts = Counter(
    flag for record in records for flag in record["flags"]  # type: ignore[union-attr]
)
file_counts: dict[str, Counter[str]] = defaultdict(Counter)
for record in records:
    file_counts[str(record["file"])][str(record["kind"])] += 1

summary = {
    "source_files": [str(source.relative_to(ROOT)) for source in SOURCES],
    "record_count": len(records),
    "kind_counts": dict(sorted(kind_counts.items())),
    "flag_counts": dict(sorted(flag_counts.items())),
    "file_kind_counts": {
        file: dict(sorted(counts.items())) for file, counts in sorted(file_counts.items())
    },
}
Path("/audit-output/evidence/stage5_inventory_summary.json").write_text(
    json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
