#!/usr/bin/env python3
"""Emit an exhaustive source-level inventory of K declarations and rules."""

from __future__ import annotations

import pathlib
import re
from collections import Counter


SCRATCH = pathlib.Path("/tmp/audit-work/33-sort-third")
paths = sorted((SCRATCH / "reference-semantics").rglob("*.k")) + [
    SCRATCH / "verification.k",
    SCRATCH / "spec.k",
]
start_re = re.compile(r"^\s*(configuration|context|syntax|rule|claim)\b")
boundary_re = re.compile(
    r"^\s*(configuration|context|syntax|rule|claim|module|endmodule|requires|imports)\b"
)


def blocks(path: pathlib.Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [index for index, line in enumerate(lines) if start_re.match(line)]
    for position, start in enumerate(starts):
        stop = starts[position + 1] if position + 1 < len(starts) else len(lines)
        # Do not absorb module terminators or declarations that are not inventoried.
        for index in range(start + 1, stop):
            if boundary_re.match(lines[index]) and not lines[index].lstrip().startswith(
                ("requires ", "[")
            ):
                stop = index
                break
        while stop > start + 1 and not lines[stop - 1].strip():
            stop -= 1
        yield start + 1, lines[start:stop]


overall: Counter[str] = Counter()
output: list[str] = []
for path in paths:
    relative = path.relative_to(SCRATCH)
    entries = list(blocks(path))
    counts: Counter[str] = Counter()
    for _, block in entries:
        kind = start_re.match(block[0]).group(1)  # type: ignore[union-attr]
        counts[kind] += 1
        overall[kind] += 1
    output.append(
        f"FILE {relative} "
        + " ".join(f"{kind}={counts[kind]}" for kind in sorted(counts))
    )
    for line_number, block in entries:
        kind = start_re.match(block[0]).group(1)  # type: ignore[union-attr]
        attributes = sorted(
            {
                attribute
                for line in block
                for attribute in re.findall(
                    r"\b(functional|function|total|simplification|priority|"
                    r"owise|macro-rec|macro|concrete|no-evaluators|symbol)\b",
                    line,
                )
            }
        )
        flattened = " ".join(line.strip() for line in block)
        output.append(
            f"  {kind.upper()} line={line_number} "
            f"attrs={','.join(attributes) if attributes else '-'} :: {flattened}"
        )
output.append(
    "TOTAL " + " ".join(f"{kind}={overall[kind]}" for kind in sorted(overall))
)
destination = pathlib.Path("/audit-output/evidence/static_inventory.txt")
destination.write_text("\n".join(output) + "\n", encoding="utf-8")
print(f"files={len(paths)}")
print(f"output={destination}")
print(
    "totals=" + ",".join(f"{kind}:{overall[kind]}" for kind in sorted(overall))
)
print(f"output_lines={len(output)}")
