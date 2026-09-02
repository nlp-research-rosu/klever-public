#!/usr/bin/env python3
"""Exhaustive declaration/rule index for the fixed and proof-local K sources."""

from __future__ import annotations

import collections
import re
from pathlib import Path


SEMANTICS = Path("/tmp/audit-work/111-histogram/reference-semantics")
FILES = [SEMANTICS / "semantics.k", *sorted((SEMANTICS / "semantics").glob("*.k"))]
FILES.append(Path("/tmp/audit-work/111-histogram/verification.k"))
START = re.compile(r"^\s*(syntax|rule|configuration|context|claim|alias)\b")


def tags(kind: str, body: str) -> list[str]:
    result: list[str] = []
    if kind == "syntax":
        for marker in (
            "function",
            "total",
            "functional",
            "constructor",
            "macro",
            "macro-rec",
            "strict",
            "seqstrict",
            "symbol",
            "no-evaluators",
        ):
            if re.search(rf"\b{re.escape(marker)}\b", body):
                result.append(marker)
    if kind == "rule":
        result.append("simplification" if "simplification" in body else "ordinary")
        if "priority(" in body:
            result.append("priority")
        if "[owise]" in body:
            result.append("owise")
        if "[concrete]" in body:
            result.append("concrete")
    return result


counts: collections.Counter[str] = collections.Counter()
entry_count = 0
for path in FILES:
    lines = path.read_text().splitlines()
    starts = [(idx, START.match(line)) for idx, line in enumerate(lines)]
    starts = [(idx, match) for idx, match in starts if match is not None]
    print(f"===== FILE {path}")
    for position, (start, match) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        body_lines = lines[start:end]
        while body_lines and (
            body_lines[-1].strip() in ("", "endmodule")
            or body_lines[-1].lstrip().startswith("//")
        ):
            body_lines.pop()
        body = "\n".join(body_lines)
        kind = match.group(1)
        entry_count += 1
        counts[kind] += 1
        entry_tags = tags(kind, body)
        for tag in entry_tags:
            counts[f"{kind}:{tag}"] += 1
        print(
            f"ENTRY {entry_count:04d} {path}:{start + 1} "
            f"KIND={kind} TAGS={','.join(entry_tags) if entry_tags else '-'}"
        )
        print(body)
        print("-----")

expected = 0
for path in FILES:
    expected += sum(1 for line in path.read_text().splitlines() if START.match(line))

print("===== INVENTORY SUMMARY")
print(f"FILE_COUNT={len(FILES)}")
print(f"ENTRY_COUNT={entry_count}")
print(f"REGEX_EXPECTED_ENTRY_COUNT={expected}")
for key in sorted(counts):
    print(f"{key}={counts[key]}")
if entry_count != expected:
    raise SystemExit(1)
