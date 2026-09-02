#!/usr/bin/env python3
"""Emit an exhaustive declaration/rule/claim inventory for the audit sources."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


TRUSTED = Path("/reference/reference-semantics")
CANDIDATE = Path("/candidate")

paths = sorted(TRUSTED.rglob("*.k")) + [
    CANDIDATE / "verification.k",
    CANDIDATE / "spec.k",
]

declaration = re.compile(
    r"^\s*(requires|module|endmodule|imports|configuration|syntax|context(?:\s+alias)?|"
    r"rule|claim|alias)\b"
)

# These source files contain the execution slice reached by solution.mpy. Some
# declarations within them are still unused; their complete text remains in
# the inventory so that the manual review can state that explicitly.
material_files = {
    "semantics.k",
    "semantics/syntax.k",
    "semantics/core.k",
    "semantics/iter.k",
    "semantics/list.k",
    "semantics/str.k",
    "semantics/operators.k",
    "semantics/controls.k",
    "semantics/functions.k",
    "semantics/call.k",
    "verification.k",
    "spec.k",
}

counts: Counter[str] = Counter()
attribute_counts: Counter[str] = Counter()
opaque_blocks: list[str] = []
priority_blocks: list[str] = []
simplification_blocks: list[str] = []
functional_blocks: list[str] = []

for path in paths:
    if path.is_relative_to(TRUSTED):
        rel = path.relative_to(TRUSTED).as_posix()
    else:
        rel = path.name
    lines = path.read_text().splitlines()
    starts = [i for i, line in enumerate(lines) if declaration.match(line)]
    print(f"\nFILE {rel} lines={len(lines)} material_execution_slice={'yes' if rel in material_files else 'no'}")
    for index, start in enumerate(starts):
        end = starts[index + 1] if index + 1 < len(starts) else len(lines)
        block_lines = lines[start:end]
        while block_lines and not block_lines[-1].strip():
            block_lines.pop()
        first = block_lines[0].strip()
        kind_match = declaration.match(block_lines[0])
        assert kind_match is not None
        kind = kind_match.group(1)
        counts[kind] += 1
        block = "\n".join(block_lines)
        attrs = re.findall(r"\[([^\]]+)\]", block)
        for attr_group in attrs:
            for attr in (piece.strip() for piece in attr_group.split(",")):
                attribute_counts[attr.split("(", 1)[0]] += 1
        tag = f"{rel}:{start + 1}"
        if "symbol(" in block or "no-evaluators" in block:
            opaque_blocks.append(tag)
        if "priority(" in block:
            priority_blocks.append(tag)
        if "simplification" in block:
            simplification_blocks.append(tag)
        if "functional" in block:
            functional_blocks.append(tag)
        print(f"DECL {tag} kind={kind}")
        for line in block_lines:
            print(f"  {line}")

print("\nSUMMARY")
print(f"files={len(paths)}")
print(f"declaration_counts={dict(sorted(counts.items()))}")
print(f"attribute_counts={dict(sorted(attribute_counts.items()))}")
print(f"opaque_or_no_evaluator_blocks={opaque_blocks}")
print(f"priority_blocks={priority_blocks}")
print(f"simplification_blocks={simplification_blocks}")
print(f"functional_blocks={functional_blocks}")
