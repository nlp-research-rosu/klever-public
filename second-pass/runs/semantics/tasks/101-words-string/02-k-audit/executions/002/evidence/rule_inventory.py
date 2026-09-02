#!/usr/bin/env python3
"""Produce a source-derived inventory of every local K declaration and rule."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/101-words-string-independent-audit")
FILES = [
    ROOT / "reference-semantics/semantics.k",
    *sorted((ROOT / "reference-semantics/semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]
START = re.compile(
    r"^\s*(requires|module|imports|configuration|syntax|context|rule|claim|endmodule)\b"
)


def logical_blocks(lines: list[str]):
    starts = [i for i, line in enumerate(lines) if START.match(line)]
    for pos, start in enumerate(starts):
        kind = START.match(lines[start]).group(1)
        if kind in {"requires", "module", "imports", "endmodule"}:
            end = start + 1
        else:
            next_start = starts[pos + 1] if pos + 1 < len(starts) else len(lines)
            end = next_start
            while end > start + 1 and (
                not lines[end - 1].strip() or lines[end - 1].lstrip().startswith("//")
            ):
                end -= 1
        text = " ".join(
            part.strip()
            for part in lines[start:end]
            if part.strip() and not part.lstrip().startswith("//")
        )
        yield kind, start + 1, end, text


grand = Counter()
print("# Exhaustive K declaration and rule inventory")
print()
print("Generated from the clean trusted-semantics scratch copy and candidate proof sources.")
print("Each source-starting declaration is listed exactly once; multiline bodies, guards, cells,")
print("attributes, and right-hand sides are collapsed onto one line.")
print()

for path in FILES:
    rel = path.relative_to(ROOT)
    lines = path.read_text().splitlines()
    blocks = list(logical_blocks(lines))
    counts = Counter(kind for kind, *_ in blocks)
    for kind, _, _, text in blocks:
        grand[kind] += 1
        if kind == "syntax":
            for attr in ("function", "total", "macro", "strict", "seqstrict"):
                if re.search(rf"\b{attr}\b", text):
                    counts[f"syntax:{attr}"] += 1
                    grand[f"syntax:{attr}"] += 1
        if kind == "rule":
            for attr in ("priority", "owise", "concrete", "simplification"):
                if re.search(rf"\b{attr}\b", text):
                    counts[f"rule:{attr}"] += 1
                    grand[f"rule:{attr}"] += 1

    print(f"## {rel}")
    print()
    summary = ", ".join(f"{key}={value}" for key, value in sorted(counts.items()))
    print(f"Counts: {summary}")
    print()
    for kind, start, end, text in blocks:
        span = str(start) if start == end else f"{start}-{end}"
        print(f"- `{kind}` L{span}: `{text}`")
    print()

print("## Grand totals")
print()
for key, value in sorted(grand.items()):
    print(f"- {key}: {value}")
