#!/usr/bin/env python3
"""Create a line-addressed inventory of K declarations and proof claims."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


TRUSTED = Path("/reference/reference-semantics")
CANDIDATE = Path("/candidate")
OUTPUT = Path("/audit-output/evidence/rule-inventory.md")

candidate_files = [
    CANDIDATE / "verification-base.k",
    CANDIDATE / "verification.k",
    CANDIDATE / "spec.k",
    CANDIDATE / "branch-connection.k",
    CANDIDATE / "branch-connection-spec.k",
    CANDIDATE / "loop-connection.k",
    CANDIDATE / "loop-connection-spec.k",
]
files = sorted(TRUSTED.rglob("*.k")) + candidate_files

start_re = re.compile(
    r"^\s*(configuration|syntax|rule|claim|context|alias)\b"
)
module_end_re = re.compile(r"^\s*endmodule\b")


def strip_line_comment(line: str) -> str:
    quoted = False
    escaped = False
    for index, char in enumerate(line):
        if escaped:
            escaped = False
            continue
        if char == "\\" and quoted:
            escaped = True
            continue
        if char == '"':
            quoted = not quoted
            continue
        if (
            char == "/"
            and not quoted
            and index + 1 < len(line)
            and line[index + 1] == "/"
        ):
            return line[:index]
    return line


def normalized(lines: list[str]) -> str:
    pieces: list[str] = []
    for line in lines:
        line = strip_line_comment(line).strip()
        if line:
            pieces.append(line)
    return " ".join(pieces)


records: list[dict[str, object]] = []
for path in files:
    lines = path.read_text().splitlines()
    starts = [
        index
        for index, line in enumerate(lines)
        if start_re.match(line)
    ]
    for position, start in enumerate(starts):
        later = starts[position + 1] if position + 1 < len(starts) else len(lines)
        for index in range(start + 1, later):
            if module_end_re.match(lines[index]):
                later = index
                break
        text = normalized(lines[start:later])
        match = start_re.match(lines[start])
        assert match is not None
        kind = match.group(1)
        attrs = sorted(
            {
                attr
                for bracket in re.findall(r"\[([^\]]+)\]", text)
                for attr in re.findall(
                    r"\b(?:function|functional|total|macro|simplification|"
                    r"concrete|owise|strict|seqstrict|symbol|priority)"
                    r"(?:\([^)]*\))?",
                    bracket,
                )
            }
        )
        records.append(
            {
                "path": str(path),
                "start": start + 1,
                "end": later,
                "kind": kind,
                "attrs": attrs,
                "text": text,
            }
        )

counts = Counter(str(record["kind"]) for record in records)
attribute_counts: Counter[str] = Counter()
for record in records:
    for attr in record["attrs"]:
        attribute_counts[str(attr)] += 1

with OUTPUT.open("w", encoding="utf-8") as stream:
    stream.write("# Exhaustive K declaration/rule inventory\n\n")
    stream.write(
        "Generated from the trusted supplied-semantics tree and all "
        "proof-local source modules that contribute declarations or claims. "
        "Every source line beginning with `configuration`, `syntax`, `rule`, "
        "`claim`, `context`, or `alias` starts one inventoried block; "
        "continuation lines are retained through the next declaration.\n\n"
    )
    stream.write(f"- Files: {len(files)}\n")
    stream.write(f"- Inventory records: {len(records)}\n")
    stream.write(
        "- Kinds: "
        + ", ".join(f"{kind}={count}" for kind, count in sorted(counts.items()))
        + "\n"
    )
    stream.write(
        "- Attributes: "
        + ", ".join(
            f"{attr}={count}" for attr, count in sorted(attribute_counts.items())
        )
        + "\n\n"
    )

    current_path = None
    sequence = 0
    for record_index, record in enumerate(records):
        path = str(record["path"])
        if path != current_path:
            stream.write(f"## {path}\n\n")
            stream.write("| ID | Lines | Kind | Attributes | Declaration / rule |\n")
            stream.write("|---:|:---|:---|:---|:---|\n")
            current_path = path
        sequence += 1
        text = str(record["text"]).replace("|", r"\|").replace("`", r"\`")
        attr_text = ", ".join(str(attr) for attr in record["attrs"])
        stream.write(
            f"| {sequence} | {record['start']}-{record['end']} | "
            f"{record['kind']} | {attr_text or 'ordinary'} | `{text}` |\n"
        )
        next_index = record_index + 1
        if next_index == len(records) or str(records[next_index]["path"]) != path:
            stream.write("\n")

print(f"files={len(files)}")
print(f"records={len(records)}")
print("kinds=" + ",".join(f"{k}:{v}" for k, v in sorted(counts.items())))
print(
    "attributes="
    + ",".join(f"{k}:{v}" for k, v in sorted(attribute_counts.items()))
)
print(f"output={OUTPUT}")
