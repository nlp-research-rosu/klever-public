#!/usr/bin/env python3
"""Emit a complete line-addressed declaration/rule inventory for the audit."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import re


roots = [
    Path("/reference/reference-semantics/semantics.k"),
    *sorted(Path("/reference/reference-semantics/semantics").glob("*.k")),
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
]

start_re = re.compile(
    r"^\s*(requires|module|imports|syntax|configuration|context|rule|claim|endmodule)\b"
)

records: list[dict[str, object]] = []
for path in roots:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [index for index, line in enumerate(lines) if start_re.match(line)]
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        block_lines = lines[start:end]
        first = block_lines[0].strip()
        kind = start_re.match(block_lines[0]).group(1)  # type: ignore[union-attr]
        if kind not in {"syntax", "configuration", "context", "rule", "claim"}:
            continue
        block = "\n".join(block_lines).strip()
        attrs: list[str] = []
        if "[function" in block or re.search(r"\bfunction\b", block):
            attrs.append("function")
        for attr in (
            "total",
            "functional",
            "symbol",
            "no-evaluators",
            "macro",
            "macro-rec",
            "strict",
            "seqstrict",
            "owise",
            "concrete",
            "simplification",
        ):
            if re.search(rf"\b{re.escape(attr)}\b", block):
                attrs.append(attr)
        priorities = re.findall(r"priority\(([^)]+)\)", block)
        if priorities:
            attrs.extend(f"priority({value})" for value in priorities)
        records.append(
            {
                "path": path,
                "line": start + 1,
                "end": end,
                "kind": kind,
                "attrs": attrs,
                "first": first,
                "block": block,
            }
        )

counts = Counter(str(record["kind"]) for record in records)
attr_counts = Counter(
    attr for record in records for attr in record["attrs"]  # type: ignore[index]
)

print("# Exhaustive K declaration and rule inventory")
print()
print(
    "Source scope: trusted supplied `semantics.k` and every helper under "
    "`semantics/`, plus candidate `verification.k` and `spec.k`."
)
print()
print("## Counts")
print()
for kind in ("syntax", "configuration", "context", "rule", "claim"):
    print(f"- {kind}: {counts[kind]}")
for attr in (
    "function",
    "total",
    "functional",
    "symbol",
    "no-evaluators",
    "macro",
    "macro-rec",
    "strict",
    "seqstrict",
    "owise",
    "concrete",
    "simplification",
):
    print(f"- attribute `{attr}`: {attr_counts[attr]}")
print(
    f"- priority-bearing declarations/rules: "
    f"{sum(value for key, value in attr_counts.items() if key.startswith('priority('))}"
)
print()

current_path: Path | None = None
ordinal = 0
for record in records:
    path = record["path"]
    if path != current_path:
        current_path = path  # type: ignore[assignment]
        print(f"## `{path}`")
        print()
    ordinal += 1
    attrs = ", ".join(record["attrs"]) if record["attrs"] else "none"  # type: ignore[arg-type]
    first = str(record["first"]).replace("|", "\\|")
    print(
        f"- `INV-{ordinal:04d}` `{record['kind']}` "
        f"lines {record['line']}-{record['end']}; attrs: {attrs}; `{first}`"
    )
