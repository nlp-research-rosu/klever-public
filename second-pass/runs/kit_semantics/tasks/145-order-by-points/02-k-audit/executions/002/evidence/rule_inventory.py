#!/usr/bin/env python3
"""Emit an exhaustive declaration/rule inventory for the audited K sources."""

import re
from collections import Counter
from pathlib import Path


SEMANTICS_ROOT = Path("/reference/reference-semantics")
FILES = sorted(SEMANTICS_ROOT.rglob("*.k")) + [
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
]

START = re.compile(
    r"^\s*(module|endmodule|imports|configuration|syntax|context(?:\s+alias)?|"
    r"rule|claim)\b"
)
TOP_REQUIRES = re.compile(r'^requires\s+"')
ATTR_NAMES = [
    "function",
    "total",
    "functional",
    "symbol",
    "no-evaluators",
    "priority",
    "simplification",
    "concrete",
    "owise",
    "macro",
    "macro-rec",
    "strict",
    "seqstrict",
]


def item_kind(line: str) -> str:
    if TOP_REQUIRES.match(line):
        return "file-requires"
    match = START.match(line)
    assert match
    return match.group(1).replace(" ", "-")


inventory = []
file_counts = {}
for path in FILES:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [
        index
        for index, line in enumerate(lines)
        if START.match(line) or TOP_REQUIRES.match(line)
    ]
    blocks = []
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        block_lines = lines[start:end]
        while block_lines and not block_lines[-1].strip():
            block_lines.pop()
        block = "\n".join(block_lines)
        code_only = "\n".join(
            re.sub(r"//.*$", "", block_line) for block_line in block_lines
        )
        bracket_groups = []
        for bracket_match in re.finditer(r"\[([^\]]*)\]", code_only):
            suffix = code_only[bracket_match.end():]
            if re.match(r"\s*:", suffix):
                continue
            bracket_groups.append(bracket_match.group(1))
        bracket_attributes = " ".join(bracket_groups)
        kind = item_kind(lines[start])
        attributes = [
            attribute
            for attribute in ATTR_NAMES
            if re.search(
                rf"\b{re.escape(attribute)}\b",
                bracket_attributes,
            )
        ]
        blocks.append((start + 1, kind, attributes, block))
        inventory.append((path, start + 1, kind, attributes, block))
    file_counts[str(path)] = Counter(kind for _, kind, _, _ in blocks)

global_counts = Counter(kind for _, _, kind, _, _ in inventory)
attribute_counts = Counter()
for _, _, _, attributes, _ in inventory:
    attribute_counts.update(attributes)

print("K STATIC INVENTORY")
print(f"files={len(FILES)} items={len(inventory)}")
print(f"kind_counts={dict(sorted(global_counts.items()))}")
print(f"attribute_counts={dict(sorted(attribute_counts.items()))}")
print("FILE COUNTS")
for path in FILES:
    print(f"{path}: {dict(sorted(file_counts[str(path)].items()))}")

opaque = [
    (path, line, block.splitlines()[0])
    for path, line, kind, attributes, block in inventory
    if kind == "syntax" and "no-evaluators" in attributes
]
print("OPAQUE DECLARATIONS")
for path, line, first in opaque:
    print(f"{path}:{line}: {first.strip()}")

print("PRIORITY RULES")
for path, line, kind, attributes, block in inventory:
    if kind == "rule" and "priority" in attributes:
        code_only = "\n".join(
            re.sub(r"//.*$", "", block_line) for block_line in block.splitlines()
        )
        priority = re.findall(r"priority\([^]]+\)", code_only)
        print(f"{path}:{line}: {priority}: {block.splitlines()[0].strip()}")

print("SIMPLIFICATION RULES")
simplifications = 0
for path, line, kind, attributes, block in inventory:
    if kind == "rule" and "simplification" in attributes:
        simplifications += 1
        print(f"{path}:{line}: {block.splitlines()[0].strip()}")
if simplifications == 0:
    print("NONE")

print("FUNCTIONAL DECLARATIONS")
functionals = 0
for path, line, kind, attributes, block in inventory:
    if kind == "syntax" and "functional" in attributes:
        functionals += 1
        print(f"{path}:{line}: {block.splitlines()[0].strip()}")
if functionals == 0:
    print("NONE")

print("EXHAUSTIVE ITEMS")
for number, (path, line, kind, attributes, block) in enumerate(inventory, 1):
    print(
        f"ITEM {number:04d} {path}:{line} "
        f"KIND={kind} ATTRS={','.join(attributes) or '-'}"
    )
    print(block)
    print("END ITEM")
