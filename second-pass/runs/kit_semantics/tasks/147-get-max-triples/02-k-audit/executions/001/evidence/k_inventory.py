#!/usr/bin/env python3
"""Emit a source-location inventory of K declarations and rules."""

from __future__ import annotations

import argparse
import collections
import re
from pathlib import Path


START = re.compile(
    r"^(?P<indent> *)(?P<kind>requires|module|endmodule|imports|syntax|"
    r"configuration|rule|context|claim|alias|macro)\b"
)
ATTRS = (
    "function",
    "functional",
    "total",
    "simplification",
    "concrete",
    "owise",
    "priority",
    "macro",
    "symbol",
    "no-evaluators",
)


def without_line_comments(text: str) -> str:
    cleaned = []
    for line in text.splitlines():
        in_string = False
        escaped = False
        index = 0
        while index < len(line):
            char = line[index]
            if escaped:
                escaped = False
            elif char == "\\" and in_string:
                escaped = True
            elif char == '"':
                in_string = not in_string
            elif (
                char == "/"
                and not in_string
                and index + 1 < len(line)
                and line[index + 1] == "/"
            ):
                line = line[:index]
                break
            index += 1
        cleaned.append(line)
    return "\n".join(cleaned)


def records(path: Path):
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match is not None and len(match.group("indent")) <= 2:
            starts.append((index, match.group("kind")))
    for number, (start, kind) in enumerate(starts):
        end = starts[number + 1][0] if number + 1 < len(starts) else len(lines)
        text = "\n".join(lines[start:end]).strip()
        if kind in {"module", "endmodule", "imports", "requires"}:
            continue
        yield start + 1, end, kind, text


parser = argparse.ArgumentParser()
parser.add_argument("root", type=Path)
parser.add_argument("--summary", action="store_true")
args = parser.parse_args()

paths = sorted(args.root.rglob("*.k"))
counts: collections.Counter[tuple[str, str]] = collections.Counter()
attr_counts: collections.Counter[tuple[str, str]] = collections.Counter()
all_records = []
for path in paths:
    relative = path.relative_to(args.root).as_posix()
    for start, end, kind, body in records(path):
        counts[(relative, kind)] += 1
        code = without_line_comments(body)
        attributes = " ".join(re.findall(r"\[([^\]]+)\]", code))
        for attr in ATTRS:
            if re.search(rf"\b{re.escape(attr)}\b", attributes):
                attr_counts[(relative, attr)] += 1
        all_records.append((relative, start, end, kind, body))

if args.summary:
    for path in paths:
        relative = path.relative_to(args.root).as_posix()
        kind_text = " ".join(
            f"{kind}={counts[(relative, kind)]}"
            for kind in (
                "syntax",
                "configuration",
                "context",
                "rule",
                "claim",
                "alias",
                "macro",
            )
            if counts[(relative, kind)]
        )
        attr_text = " ".join(
            f"{attr}={attr_counts[(relative, attr)]}"
            for attr in ATTRS
            if attr_counts[(relative, attr)]
        )
        print(f"{relative}: {kind_text or 'no local declarations'}; {attr_text or 'no attributes'}")
    totals = collections.Counter()
    total_attrs = collections.Counter()
    for (_, kind), count in counts.items():
        totals[kind] += count
    for (_, attr), count in attr_counts.items():
        total_attrs[attr] += count
    print("TOTAL KINDS:", " ".join(f"{key}={totals[key]}" for key in sorted(totals)))
    print(
        "TOTAL ATTRIBUTES:",
        " ".join(f"{key}={total_attrs[key]}" for key in sorted(total_attrs)),
    )
else:
    for relative, start, end, kind, body in all_records:
        flattened = " ".join(
            line.strip() for line in body.splitlines() if line.strip()
        )
        print(f"{relative}:{start}-{end} [{kind}] {flattened}")
