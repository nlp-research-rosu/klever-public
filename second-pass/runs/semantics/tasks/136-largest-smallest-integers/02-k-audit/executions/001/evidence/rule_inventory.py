#!/usr/bin/env python3
"""Enumerate top-level K declarations/rules for the supplied semantics and proof."""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
PATHS = [
    ROOT / "reference-semantics" / "semantics.k",
    *sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]
START = re.compile(
    r"^(?P<indent> {0,2})(?P<kind>requires|module|endmodule|imports|configuration|syntax|context|rule|claim)\b"
)


def normalized(lines: list[str]) -> str:
    meaningful = []
    for line in lines:
        text = line.strip()
        if not text or text.startswith("//"):
            continue
        meaningful.append(text)
    return " ".join(" ".join(meaningful).split())


all_records = []
for path in PATHS:
    lines = path.read_text().splitlines()
    starts = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group("kind")))
    for position, (index, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        block = normalized(lines[index:end])
        bracket_text = " ".join(re.findall(r"\[[^\]]+\]", block))
        attrs = []
        for attr in (
            "function",
            "functional",
            "total",
            "simplification",
            "priority",
            "owise",
            "concrete",
            "no-evaluators",
            "symbol",
            "macro",
            "macro-rec",
            "strict",
            "seqstrict",
        ):
            if re.search(rf"\b{re.escape(attr)}(?:\b|\()", bracket_text):
                attrs.append(attr)
        all_records.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "line": index + 1,
                "kind": kind,
                "attrs": attrs,
                "block": block,
            }
        )

print("COMMAND: python3 /audit-output/evidence/rule_inventory.py")
print(f"source_files={len(PATHS)}")
for path in PATHS:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    print(
        f"SOURCE {path.relative_to(ROOT).as_posix()} "
        f"lines={len(path.read_text().splitlines())} sha256={digest}"
    )

kind_counts = Counter(record["kind"] for record in all_records)
print("COUNTS " + " ".join(f"{kind}={kind_counts[kind]}" for kind in sorted(kind_counts)))

for attr in (
    "function",
    "functional",
    "total",
    "simplification",
    "priority",
    "owise",
    "concrete",
    "no-evaluators",
    "symbol",
    "macro",
    "macro-rec",
    "strict",
    "seqstrict",
):
    count = sum(attr in record["attrs"] for record in all_records)
    print(f"ATTRIBUTE {attr}={count}")

print("INVENTORY")
for number, record in enumerate(all_records, 1):
    attrs = ",".join(record["attrs"]) if record["attrs"] else "-"
    print(
        f"{number:04d} {record['path']}:{record['line']} "
        f"kind={record['kind']} attrs={attrs} :: {record['block']}"
    )
