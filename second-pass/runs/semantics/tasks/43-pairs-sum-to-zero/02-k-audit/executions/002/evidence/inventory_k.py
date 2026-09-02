#!/usr/bin/env python3
"""Emit a complete declaration/rule/claim inventory for the audited K sources."""

from __future__ import annotations

from pathlib import Path
import re

ROOT = Path("/tmp/audit-work")
paths = sorted((ROOT / "reference-semantics").rglob("*.k"))
paths += [ROOT / "verification.k", ROOT / "spec.k"]

start_re = re.compile(
    r"^(?:(requires|module|endmodule)\b|"
    r"  (imports|configuration|syntax(?:\s+priority)?|context|rule|claim)\b)"
)
module_re = re.compile(r"^\s*module\s+(\S+)")

records: list[dict[str, object]] = []


def finish_record(current: dict[str, object] | None) -> None:
    if current is not None:
        text = "\n".join(current["lines"]).rstrip()
        current["text"] = text
        records.append(current)


for path in paths:
    lines = path.read_text().splitlines()
    module = "(outside-module)"
    current: dict[str, object] | None = None

    for line_number, line in enumerate(lines, 1):
        match = start_re.match(line)
        if match:
            finish_record(current)
            current = None
            kind = match.group(1) or match.group(2)
            module_match = module_re.match(line)
            if module_match:
                module = module_match.group(1)
            current = {
                "path": path.relative_to(ROOT).as_posix(),
                "line": line_number,
                "module": module,
                "kind": kind,
                "lines": [line],
            }
            if kind == "endmodule":
                finish_record(current)
                current = None
                module = "(outside-module)"
        elif current is not None:
            stripped = line.strip()
            if stripped and not stripped.startswith("//"):
                current["lines"].append(line)
    finish_record(current)

for index, record in enumerate(records, 1):
    text = str(record["text"])
    flags = []
    for flag in (
        "function",
        "total",
        "functional",
        "symbol",
        "opaque",
        "priority",
        "owise",
        "simplification",
        "concrete",
        "strict",
        "seqstrict",
        "macro",
    ):
        if re.search(rf"\b{re.escape(flag)}\b", text):
            flags.append(flag)
    compact = " ".join(part.strip() for part in text.splitlines())
    print(
        f"{index:04d}\t{record['path']}:{record['line']}\t"
        f"{record['module']}\t{record['kind']}\t"
        f"flags={','.join(flags) if flags else '-'}\t{compact}"
    )

kinds: dict[str, int] = {}
for record in records:
    kinds[str(record["kind"])] = kinds.get(str(record["kind"]), 0) + 1
print(f"SUMMARY total_records={len(records)} kinds={dict(sorted(kinds.items()))}")
