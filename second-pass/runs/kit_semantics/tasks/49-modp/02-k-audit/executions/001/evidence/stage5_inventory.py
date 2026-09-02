#!/usr/bin/env python3

"""Emit an exhaustive declaration/rule inventory for the audited K sources."""

from __future__ import annotations

import collections
import hashlib
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/49-modp")
sources = [ROOT / "reference-semantics" / "semantics.k"]
sources += sorted((ROOT / "reference-semantics" / "semantics").glob("*.k"))
sources += [ROOT / "verification.k", ROOT / "spec.k"]

start = re.compile(
    r"^\s*(configuration|syntax|context|rule|claim)\b"
)
attribute_names = (
    "function",
    "total",
    "functional",
    "symbol",
    "no-evaluators",
    "priority",
    "owise",
    "simplification",
    "concrete",
    "macro",
    "macro-rec",
    "strict",
    "seqstrict",
)

grand_counts: collections.Counter[str] = collections.Counter()
grand_attributes: collections.Counter[str] = collections.Counter()


def parse_records(text: str) -> list[tuple[int, str, str]]:
    records: list[tuple[int, str, str]] = []
    current_line: int | None = None
    current_kind: str | None = None
    current_parts: list[str] = []

    def flush() -> None:
        nonlocal current_line, current_kind, current_parts
        if current_line is not None and current_kind is not None:
            records.append((current_line, current_kind, " ".join(current_parts)))
        current_line = None
        current_kind = None
        current_parts = []

    for line_number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        found = start.match(line)
        if found:
            flush()
            current_line = line_number
            current_kind = found.group(1)
            current_parts = [stripped]
        elif stripped == "endmodule":
            flush()
        elif current_line is not None and stripped and not stripped.startswith("//"):
            current_parts.append(stripped)
    flush()
    return records


for path in sources:
    text = path.read_text()
    digest = hashlib.sha256(text.encode()).hexdigest()
    records = parse_records(text)

    counts = collections.Counter(kind for _, kind, _ in records)
    attrs = collections.Counter()
    for _, _, body in records:
        for attribute in attribute_names:
            if re.search(rf"\b{re.escape(attribute)}\b", body):
                attrs[attribute] += 1
    grand_counts.update(counts)
    grand_attributes.update(attrs)

    relative = path.relative_to(ROOT)
    print(f"FILE|{relative}|SHA256={digest}|LINES={len(text.splitlines())}")
    print(
        "COUNTS|"
        + "|".join(f"{kind}={counts[kind]}" for kind in sorted(counts))
        + "|"
        + "|".join(f"attr:{name}={attrs[name]}" for name in attribute_names)
    )
    for line_number, kind, body in records:
        print(f"ENTRY|{relative}:{line_number}|{kind.upper()}|{body}")

print(
    "GRAND_COUNTS|"
    + "|".join(f"{kind}={grand_counts[kind]}" for kind in sorted(grand_counts))
)
print(
    "GRAND_ATTRIBUTES|"
    + "|".join(f"{name}={grand_attributes[name]}" for name in attribute_names)
)
