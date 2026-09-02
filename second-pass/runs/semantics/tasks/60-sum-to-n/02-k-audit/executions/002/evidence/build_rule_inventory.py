#!/usr/bin/env python3
"""Emit an exhaustive declaration/rule inventory for the audited K sources."""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
FILES = (
    [ROOT / "reference-semantics" / "semantics.k"]
    + sorted((ROOT / "reference-semantics" / "semantics").glob("*.k"))
    + [ROOT / "verification.k", ROOT / "spec.k"]
)

START = re.compile(
    r"^(?P<indent> *)(?P<kind>requires|module|imports|syntax|configuration|context|alias|rule|claim|endmodule)\b"
)


def entries(path: Path):
    lines = path.read_text().splitlines()
    starts = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match and len(match.group("indent")) <= 2:
            starts.append((index, match.group("kind")))
    for pos, (start, kind) in enumerate(starts):
        stop = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
        while stop > start + 1 and not lines[stop - 1].strip():
            stop -= 1
        yield start + 1, stop, kind, "\n".join(lines[start:stop])


counts = collections.Counter()
print("# Exhaustive K source inventory")
print()
print("Generated from fresh trusted-semantics scratch sources. Each top-level K declaration,")
print("configuration, context, rule, and claim is reproduced with its source line span.")
print()

for path in FILES:
    relative = path.relative_to(ROOT)
    print(f"## `{relative}`")
    print()
    for start, stop, kind, block in entries(path):
        counts[kind] += 1
        if kind in {"requires", "module", "imports", "endmodule"}:
            continue
        print(f"### {kind} at `{relative}:{start}` (through line {stop})")
        print()
        print("```k")
        print(block)
        print("```")
        print()

print("## Counts")
print()
for kind in sorted(counts):
    print(f"- {kind}: {counts[kind]}")
