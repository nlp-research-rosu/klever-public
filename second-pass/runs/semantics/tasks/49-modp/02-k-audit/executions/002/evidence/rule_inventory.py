#!/usr/bin/env python3
"""Produce an exhaustive source-located K declaration/rule inventory."""

from __future__ import annotations

import re
from pathlib import Path


WORK = Path("/tmp/audit-work/49-modp")
FILES = sorted((WORK / "reference-semantics").rglob("*.k")) + [
    WORK / "verification.k",
    WORK / "spec.k",
]
START = re.compile(r"^\s*(configuration|syntax|rule|context|claim)\b")
END_MODULE = re.compile(r"^\s*endmodule\b")


def records(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [i for i, line in enumerate(lines) if START.match(line)]
    for offset, start in enumerate(starts):
        following = starts[offset + 1] if offset + 1 < len(starts) else len(lines)
        for index in range(start + 1, following):
            if END_MODULE.match(lines[index]):
                following = index
                break
        statement = "\n".join(lines[start:following]).rstrip()
        keyword = START.match(lines[start]).group(1)
        yield start + 1, keyword, statement


def classify(keyword: str, statement: str) -> list[str]:
    tags = [keyword]
    if keyword == "syntax":
        tags.append("function" if re.search(r"\bfunction\b", statement)
                    else "constructor")
        for attribute in (
            "total", "functional", "no-evaluators", "hook", "token",
            "klabel", "symbol", "assoc", "comm", "unit", "subsort",
        ):
            if re.search(rf"\b{re.escape(attribute)}\b", statement):
                tags.append(attribute)
    elif keyword == "rule":
        tags.append("operational" if re.search(r"<[A-Za-z][^>]*>", statement)
                    else "equational")
        for attribute in (
            "simplification", "owise", "priority", "concrete",
            "anywhere", "macro", "alias", "preserves-definedness",
        ):
            if re.search(rf"\b{re.escape(attribute)}\b", statement):
                tags.append(attribute)
        if "requires" in statement:
            tags.append("guarded")
    return tags


def main() -> None:
    total = 0
    counts: dict[str, int] = {}
    for path in FILES:
        relative = path.relative_to(WORK)
        print(f"FILE {relative}")
        file_total = 0
        for line, keyword, statement in records(path):
            total += 1
            file_total += 1
            tags = classify(keyword, statement)
            for tag in tags:
                counts[tag] = counts.get(tag, 0) + 1
            rendered = statement.replace("\n", "\\n")
            print(f"{relative}:{line}\t{','.join(tags)}\t{rendered}")
        print(f"FILE_COUNT {relative} {file_total}")
    print(f"TOTAL_RECORDS {total}")
    for tag, count in sorted(counts.items()):
        print(f"TAG_COUNT {tag} {count}")


if __name__ == "__main__":
    main()
