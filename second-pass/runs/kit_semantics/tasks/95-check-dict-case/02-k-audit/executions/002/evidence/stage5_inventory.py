#!/usr/bin/env python3
"""Inventory every top-level K declaration in fixed and proof-local sources."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import re


roots = [
    Path("/tmp/audit-work/case95/candidate-src/reference-semantics/semantics.k"),
    *sorted(
        Path(
            "/tmp/audit-work/case95/candidate-src/reference-semantics/semantics"
        ).glob("*.k")
    ),
    Path("/tmp/audit-work/case95/candidate-src/proof-theory.k"),
    Path("/tmp/audit-work/case95/candidate-src/verification.k"),
    Path("/tmp/audit-work/case95/candidate-src/connection.k"),
    Path("/tmp/audit-work/case95/candidate-src/connection-spec.k"),
    Path("/tmp/audit-work/case95/candidate-src/spec.k"),
]

start_re = re.compile(
    r"^\s*(requires|module|endmodule|imports|configuration|syntax|context|rule|claim)\b"
)
kind_re = re.compile(
    r"^\s*(requires|module|endmodule|imports|configuration|syntax|context|rule|claim)\b"
)
attribute_names = [
    "function",
    "functional",
    "total",
    "symbol",
    "no-evaluators",
    "priority",
    "simplification",
    "concrete",
    "owise",
    "macro",
    "strict",
    "seqstrict",
]

global_kinds: Counter[str] = Counter()
global_attributes: Counter[str] = Counter()
grand_total = 0

for path in roots:
    lines = path.read_text().splitlines()
    starts = [index for index, line in enumerate(lines) if start_re.match(line)]
    records = []
    for position, start in enumerate(starts):
        stop = starts[position + 1] if position + 1 < len(starts) else len(lines)
        block = "\n".join(lines[start:stop])
        match = kind_re.match(lines[start])
        if match is None:
            continue
        kind = match.group(1)
        compact = " ".join(
            line.strip()
            for line in block.splitlines()
            if line.strip() and not line.lstrip().startswith("//")
        )
        records.append((start + 1, kind, compact))

    counts = Counter(kind for _, kind, _ in records)
    attributes: Counter[str] = Counter()
    for _, _, compact in records:
        for name in attribute_names:
            if re.search(rf"(?<![A-Za-z-]){re.escape(name)}(?![A-Za-z-])", compact):
                attributes[name] += 1

    print(f"FILE {path}")
    print(
        "COUNTS "
        + " ".join(f"{name}={counts[name]}" for name in sorted(counts))
    )
    print(
        "ATTRIBUTES "
        + " ".join(
            f"{name}={attributes[name]}"
            for name in attribute_names
            if attributes[name]
        )
    )
    for line_number, kind, compact in records:
        print(f"DECL line={line_number} kind={kind} text={compact}")
    print("END_FILE")

    global_kinds.update(counts)
    global_attributes.update(attributes)
    grand_total += len(records)

print(f"GLOBAL_RECORDS {grand_total}")
print(
    "GLOBAL_KINDS "
    + " ".join(f"{name}={global_kinds[name]}" for name in sorted(global_kinds))
)
print(
    "GLOBAL_ATTRIBUTES "
    + " ".join(
        f"{name}={global_attributes[name]}"
        for name in attribute_names
        if global_attributes[name]
    )
)
