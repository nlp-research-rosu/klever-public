#!/usr/bin/env python3
"""Produce an exhaustive source-level K declaration and rule inventory."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


START = re.compile(
    r"^\s*(configuration|syntax|rule|claim|context(?:\s+alias)?|alias|macro)\b"
)


def normalized(lines: list[str]) -> str:
    return " ".join(" ".join(line.strip().split()) for line in lines).strip()


def attributes(kind: str, text: str) -> list[str]:
    found: list[str] = []
    checks = [
        ("function", r"\bfunction\b"),
        ("total", r"\btotal\b"),
        ("functional", r"\bfunctional\b"),
        ("symbol", r"\bsymbol\s*\("),
        ("no-evaluators", r"\bno-evaluators\b"),
        ("simplification", r"\bsimplification\b"),
        ("concrete", r"\bconcrete\b"),
        ("owise", r"\bowise\b"),
        ("priority", r"\bpriority\s*\("),
        ("strict", r"\b(?:seqstrict|strict)\b"),
        ("macro", r"\bmacro\b"),
        ("token", r"\btoken\b"),
        ("bracket", r"\bbracket\b"),
    ]
    for name, pattern in checks:
        if re.search(pattern, text):
            found.append(name)
    if kind == "rule" and not set(found) & {
        "simplification",
        "concrete",
        "owise",
        "priority",
    }:
        found.append("ordinary")
    return found


def inventory_file(path: Path) -> list[dict[str, object]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match and not line.lstrip().startswith("//"):
            starts.append((index, match.group(1)))
    records: list[dict[str, object]] = []
    for position, (start, raw_kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        entry_lines = lines[start:end]
        # Exclude trailing module terminators and comments belonging to the next
        # section while retaining every declaration/rule token.
        while entry_lines and (
            entry_lines[-1].strip() == "endmodule"
            or entry_lines[-1].lstrip().startswith("//")
            or entry_lines[-1].strip() == ""
        ):
            entry_lines.pop()
        text = normalized(entry_lines)
        kind = "context" if raw_kind.startswith("context") else raw_kind
        records.append(
            {
                "file": str(path),
                "line": start + 1,
                "kind": kind,
                "attributes": attributes(kind, text),
                "text": text,
            }
        )
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output_markdown")
    parser.add_argument("output_json")
    parser.add_argument("paths", nargs="+")
    arguments = parser.parse_args()

    source_files: list[Path] = []
    for supplied in arguments.paths:
        path = Path(supplied)
        if path.is_dir():
            source_files.extend(sorted(path.rglob("*.k")))
        else:
            source_files.append(path)
    source_files = sorted(dict.fromkeys(source_files))

    all_records: list[dict[str, object]] = []
    summaries: dict[str, dict[str, int]] = {}
    for path in source_files:
        records = inventory_file(path)
        all_records.extend(records)
        counter: Counter[str] = Counter()
        for record in records:
            counter[str(record["kind"])] += 1
            for attribute in record["attributes"]:  # type: ignore[union-attr]
                counter[f"attr:{attribute}"] += 1
        summaries[str(path)] = dict(sorted(counter.items()))

    markdown_lines = [
        "# Exhaustive K source inventory",
        "",
        "Generated lexically from the trusted supplied semantics tree and the "
        "candidate proof extension. Each record gives the complete normalized "
        "source declaration beginning at the cited line.",
        "",
    ]
    for path in source_files:
        markdown_lines.extend([f"## {path}", ""])
        for record in [item for item in all_records if item["file"] == str(path)]:
            attrs = ",".join(record["attributes"]) or "-"
            markdown_lines.append(
                f"- L{record['line']} `{record['kind']}` [{attrs}]: "
                f"`{str(record['text']).replace('`', chr(39))}`"
            )
        markdown_lines.append("")
    Path(arguments.output_markdown).write_text(
        "\n".join(markdown_lines), encoding="utf-8"
    )
    Path(arguments.output_json).write_text(
        json.dumps(
            {
                "source_files": [str(path) for path in source_files],
                "record_count": len(all_records),
                "summaries": summaries,
                "records": all_records,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"SOURCE_FILES={len(source_files)}")
    print(f"RECORDS={len(all_records)}")
    print(f"MARKDOWN={arguments.output_markdown}")
    print(f"JSON={arguments.output_json}")
    for path in source_files:
        print(path, json.dumps(summaries[str(path)], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
