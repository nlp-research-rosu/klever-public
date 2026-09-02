#!/usr/bin/env python3
"""Produce a deterministic, line-addressed inventory of K declarations/rules."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


DECL = re.compile(r"^\s*(configuration|syntax|rule|claim|context)\b")
BOUNDARY = re.compile(
    r"^\s*(module|endmodule|configuration|syntax|rule|claim|context)\b"
)
ATTRS = (
    "function",
    "total",
    "functional",
    "simplification",
    "priority",
    "concrete",
    "macro",
    "owise",
    "anywhere",
    "strict",
    "seqstrict",
    "token",
    "hook",
)


def records(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [i for i, line in enumerate(lines) if BOUNDARY.match(line)]
    for offset, start in enumerate(starts):
        first = lines[start]
        if not DECL.match(first):
            continue
        end = starts[offset + 1] if offset + 1 < len(starts) else len(lines)
        block = "\n".join(lines[start:end]).rstrip()
        kind = DECL.match(first).group(1)
        attribute_text = " ".join(re.findall(r"\[([^\]]*)\]", block))
        attrs = [
            attribute
            for attribute in ATTRS
            if re.search(
                rf"(?<![A-Za-z0-9_-]){re.escape(attribute)}(?![A-Za-z0-9_-])",
                attribute_text,
            )
        ]
        if kind == "rule":
            if "simplification" in attrs:
                cls = "simplification-rule"
            elif "macro" in attrs:
                cls = "macro-rule"
            else:
                cls = "ordinary-rule"
        elif kind == "syntax":
            if "function" in attrs or "functional" in attrs:
                cls = "function-declaration"
            else:
                cls = "syntax-declaration"
        else:
            cls = kind
        summary = " ".join(part.strip() for part in block.splitlines())
        yield start + 1, cls, ",".join(attrs) or "-", summary


def opaque_functions(paths: list[Path]):
    all_records = [
        (path, record)
        for path in paths
        for record in records(path)
    ]
    rule_left_sides = []
    for _, (_, cls, _, summary) in all_records:
        if cls not in {"ordinary-rule", "simplification-rule", "macro-rule"}:
            continue
        rule_left_sides.append(summary.split("=>", 1)[0])
    seen: set[tuple[Path, int, str]] = set()
    for path, (line, cls, attrs, summary) in all_records:
        if cls != "function-declaration":
            continue
        declaration = summary.split("rule ", 1)[0]
        match = re.search(r"::=\s*([A-Za-z#][A-Za-z0-9#_-]*)\s*\(", declaration)
        if not match:
            continue
        symbol = match.group(1)
        lhs_count = sum(
            1
            for left_side in rule_left_sides
            if re.search(rf"\b{re.escape(symbol)}\s*\(", left_side)
        )
        if lhs_count == 0:
            key = (path, line, symbol)
            if key not in seen:
                seen.add(key)
                yield path, line, symbol, attrs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()
    totals: dict[str, int] = {}
    paths = sorted(args.paths, key=lambda item: str(item))
    for path in paths:
        print(f"FILE {path}")
        count = 0
        for line, cls, attrs, summary in records(path):
            count += 1
            totals[cls] = totals.get(cls, 0) + 1
            print(f"{line:04d}\t{cls}\tattrs={attrs}\t{summary}")
        print(f"FILE-RECORDS {count}")
    print("GLOBAL-OPAQUE-FUNCTIONS")
    for path, line, symbol, attrs in opaque_functions(paths):
        print(
            f"OPAQUE-FUNCTION\tfile={path}\tline={line}"
            f"\tsymbol={symbol}\tattrs={attrs}"
        )
    print("TOTALS")
    for cls in sorted(totals):
        print(f"{cls}\t{totals[cls]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
