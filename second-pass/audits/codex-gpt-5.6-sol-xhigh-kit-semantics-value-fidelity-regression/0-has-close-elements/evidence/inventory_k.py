#!/usr/bin/env python3
"""Produce an exhaustive sentence-level inventory of the audited K sources."""

from __future__ import annotations

import collections
import csv
import re
from pathlib import Path


WORK = Path("/tmp/audit-work/reconstruction")
OUTPUT = Path("/audit-output/evidence")
SOURCE_ROOTS = [
    WORK / "reference-semantics",
    WORK / "verification.k",
    WORK / "spec.k",
]
START = re.compile(
    r"^\s*(module|imports|syntax|configuration|rule|context|claim|endmodule)\b"
)
ATTRIBUTE_NAMES = [
    "function",
    "functional",
    "total",
    "simplification",
    "priority",
    "concrete",
    "anywhere",
    "owise",
    "no-evaluators",
    "macro",
    "macro-rec",
    "symbol",
    "strict",
    "seqstrict",
]


def source_files() -> list[Path]:
    files: list[Path] = []
    for root in SOURCE_ROOTS:
        if root.is_file():
            files.append(root)
        else:
            files.extend(sorted(root.rglob("*.k")))
    return sorted(files, key=lambda path: path.relative_to(WORK).as_posix())


def compact(lines: list[str]) -> str:
    relevant: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("//") or not stripped:
            continue
        if "//" in stripped:
            stripped = stripped.split("//", 1)[0].rstrip()
        if stripped:
            relevant.append(stripped)
    return " ".join(" ".join(relevant).split())


def tags_for(kind: str, text: str) -> list[str]:
    tags = [name for name in ATTRIBUTE_NAMES if re.search(rf"\b{re.escape(name)}\b", text)]
    if kind == "rule" and not any(
        tag in tags for tag in ["simplification", "concrete", "anywhere", "owise"]
    ):
        tags.append("ordinary")
    if kind == "syntax" and "no-evaluators" in tags:
        tags.append("opaque-symbol")
    return tags


def inventory() -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    identifier = 0
    for path in source_files():
        lines = path.read_text().splitlines()
        starts: list[tuple[int, str]] = []
        for index, line in enumerate(lines):
            match = START.match(line)
            if match and not line.lstrip().startswith("//"):
                starts.append((index, match.group(1)))

        current_module = ""
        for position, (index, kind) in enumerate(starts):
            end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
            sentence_lines = lines[index:end]
            text = compact(sentence_lines)
            if kind == "module":
                words = text.split()
                current_module = words[1] if len(words) > 1 else ""
            sentence_module = current_module
            if kind == "endmodule":
                current_module = ""
            if kind in {"imports", "module", "endmodule"}:
                continue
            identifier += 1
            tags = tags_for(kind, text)
            records.append(
                {
                    "id": f"K{identifier:04d}",
                    "file": path.relative_to(WORK).as_posix(),
                    "line": index + 1,
                    "end_line": end,
                    "module": sentence_module,
                    "kind": kind,
                    "tags": ",".join(tags),
                    "text": text,
                }
            )
    return records


def main() -> int:
    records = inventory()
    tsv_path = OUTPUT / "rule-inventory.tsv"
    with tsv_path.open("w", newline="") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=[
                "id",
                "file",
                "line",
                "end_line",
                "module",
                "kind",
                "tags",
                "text",
            ],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(records)

    kind_counts = collections.Counter(str(record["kind"]) for record in records)
    tag_counts: collections.Counter[str] = collections.Counter()
    file_counts: collections.Counter[str] = collections.Counter()
    for record in records:
        file_counts[str(record["file"])] += 1
        for tag in str(record["tags"]).split(","):
            if tag:
                tag_counts[tag] += 1

    summary_path = OUTPUT / "rule-inventory-summary.md"
    lines = [
        "# Exhaustive K sentence inventory summary",
        "",
        "Source scope: the fresh scratch copy of trusted `reference-semantics/**/*.k` "
        "and candidate `verification.k`. The complete sentence text, location, "
        "module, kind, and attributes are in `rule-inventory.tsv`.",
        "",
        f"Total inventoried sentences: {len(records)}.",
        "",
        "## Counts by kind",
        "",
    ]
    lines.extend(f"- `{name}`: {count}" for name, count in sorted(kind_counts.items()))
    lines.extend(["", "## Counts by classification/attribute", ""])
    lines.extend(f"- `{name}`: {count}" for name, count in sorted(tag_counts.items()))
    lines.extend(["", "## Counts by source file", ""])
    lines.extend(f"- `{name}`: {count}" for name, count in sorted(file_counts.items()))
    summary_path.write_text("\n".join(lines) + "\n")

    print(f"source_file_count={len(source_files())}")
    print(f"inventory_records={len(records)}")
    print(f"kind_counts={dict(sorted(kind_counts.items()))}")
    print(f"tag_counts={dict(sorted(tag_counts.items()))}")
    print(f"tsv={tsv_path} bytes={tsv_path.stat().st_size}")
    print(f"summary={summary_path} bytes={summary_path.stat().st_size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
