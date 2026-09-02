#!/usr/bin/env python3
"""Emit an exhaustive line-addressed K declaration and rule inventory."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/candidate")
sources = [ROOT / "reference-semantics/semantics.k"]
sources += sorted((ROOT / "reference-semantics/semantics").glob("*.k"))
sources += [ROOT / "verification.k", ROOT / "spec.k"]

start_re = re.compile(
    r"^\s*(module|imports|configuration|syntax|context|rule|claim|endmodule)\b"
)

print("id\tlocation\tmodule\tkind\tattributes\tdeclaration")
identifier = 0
for path in sources:
    lines = path.read_text().splitlines()
    module = ""
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        if line.startswith("requires "):
            starts.append((index, "requires"))
            continue
        match = start_re.match(line)
        if match:
            starts.append((index, match.group(1)))
    for ordinal, (index, kind) in enumerate(starts):
        end = starts[ordinal + 1][0] if ordinal + 1 < len(starts) else len(lines)
        block = "\n".join(lines[index:end])
        first = " ".join(block.split())
        if kind == "module":
            parts = lines[index].split()
            module = parts[1] if len(parts) > 1 else ""
        uncommented = "\n".join(part.split("//", 1)[0] for part in block.splitlines())
        bracket_items = re.findall(r"\[([^\]]+)\]", uncommented)
        attr_marker = re.compile(
            r"(?:^|,\s*)(?:(?:function|total|functional|simplification|"
            r"simplifier|owise|concrete|anywhere|macro(?:-rec)?|no-evaluators)"
            r"(?:\s*,|$)|priority\(|symbol\(|strict(?:\(|(?:\s*,|$))|"
            r"seqstrict\(|hook\()"
        )
        attrs = sorted({item for item in bracket_items if attr_marker.search(item)})
        identifier += 1
        rel = path.relative_to(ROOT)
        print(
            f"{identifier}\t{rel}:{index + 1}\t{module}\t{kind}\t"
            f"{','.join(attrs)}\t{first}"
        )
