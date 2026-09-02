#!/usr/bin/env python3
"""Emit an exhaustive, line-addressed inventory of K declarations and rules."""

import re
from pathlib import Path


ROOTS = [
    Path("/tmp/audit-work/reconstruction/reference-semantics/semantics.k"),
    *sorted(Path("/tmp/audit-work/reconstruction/reference-semantics/semantics").glob("*.k")),
    Path("/tmp/audit-work/reconstruction/verification.k"),
    Path("/tmp/audit-work/reconstruction/spec.k"),
]

START = re.compile(
    r"^(?:requires\b|\s*(?:module\b|endmodule\b|imports\b|configuration\b|"
    r"syntax\b|rule\b|claim\b|context(?:\s+alias)?\b))"
)
DECL_KIND = re.compile(
    r"^\s*(requires|module|endmodule|imports|configuration|syntax|rule|claim|context(?:\s+alias)?)\b"
)


def classify(text: str):
    first = DECL_KIND.match(text)
    kind = first.group(1) if first else "unknown"
    attr_text = " ".join(re.findall(r"\[([^\]]*)\]", text, flags=re.DOTALL))
    attrs = []
    for attribute in (
        "function",
        "total",
        "functional",
        "simplification",
        "concrete",
        "priority",
        "owise",
        "strict",
        "seqstrict",
        "macro",
        "symbol",
        "token",
        "bracket",
        "assoc",
        "comm",
        "unit",
        "idempotent",
    ):
        if re.search(rf"\b{re.escape(attribute)}\b", attr_text):
            attrs.append(attribute)
    return kind, attrs


grand_total = 0
kind_totals = {}
for path in ROOTS:
    lines = path.read_text().splitlines()
    starts = [i for i, line in enumerate(lines) if START.match(line)]
    print(f"FILE {path}")
    file_count = 0
    file_kind_totals = {}
    for offset, start in enumerate(starts):
        end = starts[offset + 1] if offset + 1 < len(starts) else len(lines)
        block = lines[start:end]
        while block and (not block[-1].strip() or block[-1].lstrip().startswith("//")):
            block.pop()
        text = "\n".join(block)
        kind, attrs = classify(text)
        kind_totals[kind] = kind_totals.get(kind, 0) + 1
        file_kind_totals[kind] = file_kind_totals.get(kind, 0) + 1
        grand_total += 1
        file_count += 1
        line_end = start + len(block)
        print(
            f"DECL {path}:{start + 1}-{line_end} kind={kind} "
            f"attrs={','.join(attrs) if attrs else '-'}"
        )
        for line_number, line in enumerate(block, start + 1):
            print(f"  {line_number:04d}: {line}")
    print(
        f"FILE_DECLARATION_COUNT {file_count} "
        + " ".join(f"{k}={v}" for k, v in sorted(file_kind_totals.items()))
    )
print("KIND_TOTALS", " ".join(f"{k}={v}" for k, v in sorted(kind_totals.items())))
print("GRAND_TOTAL", grand_total)
