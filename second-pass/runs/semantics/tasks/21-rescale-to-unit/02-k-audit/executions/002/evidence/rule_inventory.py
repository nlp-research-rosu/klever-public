#!/usr/bin/env python3
"""Lexically inventory every K declaration in the clean source tree."""

from __future__ import annotations

import re
from pathlib import Path


scratch = Path("/tmp/audit-work/21-rescale-to-unit-audit")
files = sorted((scratch / "reference-semantics").rglob("*.k")) + [
    scratch / "verification.k",
    scratch / "spec.k",
]
start_re = re.compile(
    r"^\s*(requires|module|endmodule|imports|configuration|syntax|rule|claim|context|alias)\b"
)
interesting = {
    "configuration",
    "syntax",
    "rule",
    "claim",
    "context",
    "alias",
}

records: list[dict[str, object]] = []
for path in files:
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = start_re.match(line)
        if match:
            starts.append((index, match.group(1)))
    for position, (index, kind) in enumerate(starts):
        if kind not in interesting:
            continue
        next_index = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        block_lines = lines[index:next_index]
        while block_lines and (
            not block_lines[-1].strip()
            or block_lines[-1].lstrip().startswith("//")
        ):
            block_lines.pop()
        block = "\n".join(block_lines).rstrip()
        attrs = [
            attr
            for attr in [
                "function",
                "total",
                "functional",
                "symbol",
                "no-evaluators",
                "concrete",
                "simplification",
                "priority",
                "owise",
                "macro",
                "strict",
                "seqstrict",
                "assoc",
                "comm",
                "unit",
                "hook",
            ]
            if re.search(rf"\b{re.escape(attr)}\b", block)
        ]
        records.append(
            {
                "file": str(path.relative_to(scratch)),
                "line": index + 1,
                "kind": kind,
                "attrs": attrs,
                "block": block,
            }
        )

output = Path("/audit-output/evidence/rule_inventory.md")
with output.open("w") as stream:
    stream.write("# Exhaustive lexical K declaration inventory\n\n")
    stream.write(
        "Generated from the clean trusted supplied-semantics copy plus "
        "`verification.k` and `spec.k`. Each record includes the complete "
        "source block through the next top-level K declaration.\n\n"
    )
    current = None
    for record in records:
        if record["file"] != current:
            current = record["file"]
            stream.write(f"## `{current}`\n\n")
        attrs = ", ".join(record["attrs"]) or "none"
        stream.write(
            f"### {record['kind']} at line {record['line']} "
            f"(attributes: {attrs})\n\n"
        )
        stream.write("```k\n")
        stream.write(str(record["block"]))
        stream.write("\n```\n\n")

print(f"inventory={output}")
print(f"files={len(files)} records={len(records)}")
for kind in sorted({str(record['kind']) for record in records}):
    print(f"{kind}={sum(record['kind'] == kind for record in records)}")
for attr in [
    "function",
    "total",
    "functional",
    "symbol",
    "no-evaluators",
    "concrete",
    "simplification",
    "priority",
    "owise",
    "macro",
]:
    print(f"attribute[{attr}]={sum(attr in record['attrs'] for record in records)}")
