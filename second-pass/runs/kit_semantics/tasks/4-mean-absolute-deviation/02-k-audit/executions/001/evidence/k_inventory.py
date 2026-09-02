#!/usr/bin/env python3
"""Mechanical source inventory for every supplied and proof-local K declaration."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import re


ROOT = Path("/tmp/audit-work/reconstruct")
FILES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "spec.k",
]

STARTERS = (
    "requires ",
    "module ",
    "imports ",
    "syntax ",
    "configuration",
    "rule ",
    "claim ",
    "context ",
    "context alias ",
    "endmodule",
)


def strip_comments(lines: list[str]) -> list[str]:
    result: list[str] = []
    in_block = False
    for line in lines:
        output = []
        index = 0
        while index < len(line):
            if in_block:
                end = line.find("*/", index)
                if end == -1:
                    index = len(line)
                else:
                    in_block = False
                    index = end + 2
            else:
                block = line.find("/*", index)
                single = line.find("//", index)
                candidates = [value for value in (block, single) if value != -1]
                if not candidates:
                    output.append(line[index:])
                    break
                nearest = min(candidates)
                output.append(line[index:nearest])
                if nearest == single:
                    break
                in_block = True
                index = nearest + 2
        result.append("".join(output))
    return result


def category(text: str) -> str:
    stripped = text.lstrip()
    for value in (
        "requires",
        "module",
        "imports",
        "syntax",
        "configuration",
        "rule",
        "claim",
        "context alias",
        "context",
        "endmodule",
    ):
        if stripped == value or stripped.startswith(value + " "):
            return value
    return "continuation"


def records(path: Path) -> list[tuple[int, str, str]]:
    raw_lines = path.read_text(encoding="utf-8").splitlines()
    lines = strip_comments(raw_lines)
    result: list[tuple[int, str, str]] = []
    active_line = 0
    active_category = ""
    active_parts: list[str] = []
    for line_number, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped:
            continue
        starts_record = any(
            stripped == starter.strip() or stripped.startswith(starter)
            for starter in STARTERS
        )
        if starts_record:
            if active_parts:
                result.append(
                    (
                        active_line,
                        active_category,
                        " ".join(active_parts),
                    )
                )
            active_line = line_number
            active_category = category(stripped)
            active_parts = [stripped]
        elif active_parts:
            active_parts.append(stripped)
        else:
            result.append((line_number, "orphan", stripped))
    if active_parts:
        result.append((active_line, active_category, " ".join(active_parts)))
    return result


def attributes(statement: str) -> list[str]:
    found: list[str] = []
    for raw in re.findall(r"\[([^\]]+)\]", statement):
        found.extend(part.strip() for part in raw.split(","))
    return found


def main() -> None:
    print("COMMAND: python3 /audit-output/evidence/k_inventory.py")
    print(f"k_source_files={len(FILES)}")
    total_categories: Counter[str] = Counter()
    total_attributes: Counter[str] = Counter()
    for path in FILES:
        path_records = records(path)
        relative = path.relative_to(ROOT).as_posix()
        counts = Counter(record_category for _, record_category, _ in path_records)
        for _, record_category, statement in path_records:
            total_categories[record_category] += 1
            total_attributes.update(attributes(statement))
        print(f"\n### FILE {relative}")
        print(f"RECORD_COUNTS {dict(sorted(counts.items()))}")
        for line_number, record_category, statement in path_records:
            print(
                f"{relative}:{line_number}: [{record_category}] {statement}"
            )
    print("\n### TOTALS")
    print(f"CATEGORY_COUNTS {dict(sorted(total_categories.items()))}")
    print(f"ATTRIBUTE_COUNTS {dict(sorted(total_attributes.items()))}")
    print("STATUS: ALL K SOURCE FILES INVENTORIED")


if __name__ == "__main__":
    main()
