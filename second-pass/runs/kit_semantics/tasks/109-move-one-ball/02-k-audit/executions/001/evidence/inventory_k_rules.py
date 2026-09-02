#!/usr/bin/env python3
"""Enumerate every declaration and rule/claim in the audited K source files."""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/problem-109-independent")
FILES = [ROOT / "reference-semantics" / "semantics.k"]
FILES += sorted((ROOT / "reference-semantics" / "semantics").glob("*.k"))
FILES += [ROOT / "verification.k", ROOT / "spec.k"]

START = re.compile(
    r"^\s*(module|endmodule|imports|configuration|context|syntax|rule|claim)\b"
)
DECL = re.compile(r"^\s*(syntax|configuration|context)\b")
RULE = re.compile(r"^\s*(rule|claim)\b")
ATTRS = (
    "function",
    "total",
    "functional",
    "simplification",
    "priority",
    "owise",
    "macro",
    "macro-rec",
    "symbol",
    "no-evaluators",
    "concrete",
    "anywhere",
)

totals: collections.Counter[str] = collections.Counter()
declared_function_candidates: list[tuple[str, int, str]] = []
all_rule_text = "\n".join(path.read_text(encoding="utf-8") for path in FILES)

for path in FILES:
    lines = path.read_text(encoding="utf-8").splitlines()
    rel = path.relative_to(ROOT)
    print(f"\n## FILE {rel} ({len(lines)} lines)")
    blocks: list[tuple[int, int, str]] = []
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    for position, index in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        first = lines[index].lstrip()
        kind = first.split(maxsplit=1)[0]
        if kind not in ("syntax", "configuration", "context", "rule", "claim"):
            continue
        # Keep guard and attribute continuation lines, while trimming comments and blanks.
        raw_block = lines[index:end]
        while raw_block and (not raw_block[-1].strip() or raw_block[-1].lstrip().startswith("//")):
            raw_block.pop()
        block = "\n".join(piece.rstrip() for piece in raw_block)
        blocks.append((index + 1, index + len(raw_block), block))

    print(f"declaration_or_rule_blocks={len(blocks)}")
    for start, end, block in blocks:
        first = block.lstrip()
        kind = first.split(maxsplit=1)[0]
        totals[kind] += 1
        code_without_comments = "\n".join(piece.split("//", 1)[0] for piece in block.splitlines())
        bracket_text = " ".join(re.findall(r"\[([^\]]*)\]", code_without_comments))
        attributes = []
        for attr in ATTRS:
            if attr == "priority":
                present = bool(re.search(r"(?:^|[,\s])priority(?:\(|[,\s]|$)", bracket_text))
            elif attr == "symbol":
                present = bool(re.search(r"(?:^|[,\s])symbol(?:\(|[,\s]|$)", bracket_text))
            else:
                present = attr in {item.strip() for item in bracket_text.split(",")}
            if present:
                attributes.append(attr)
        for attr in attributes:
            totals[f"attr:{attr}"] += 1
        if kind == "rule":
            category = "simplification-rule" if "simplification" in attributes else "ordinary-rule"
            if "priority" in attributes:
                category = "priority-rule"
            totals[category] += 1
        elif kind == "claim":
            category = "claim"
        else:
            category = "declaration"
        print(
            f"\n[{rel}:{start}-{end}] kind={kind} category={category} "
            f"attrs={','.join(attributes) if attributes else '-'}"
        )
        print(block)

    # Function-like declarations are checked globally because extensible functions
    # (applyUn/applyBin/applyCmp) receive equations in imported domain modules.
    for number, line in enumerate(lines, 1):
        code = line.split("//", 1)[0]
        if line.lstrip().startswith(("syntax ", "|")) and re.search(
            r"\[(?:[^\]]*\b(?:function|functional|symbol)\b[^\]]*)\]", code
        ):
            for name in re.findall(r"(?:(?:::=)|(?:\|))\s*([A-Za-z#][A-Za-z0-9#-]*)\s*\(", code):
                declared_function_candidates.append((str(rel), number, name))

print("\n## GLOBAL COUNTS")
for key, value in sorted(totals.items()):
    print(f"{key}={value}")
print("function_candidates_without_any_textual_rule_head=")
for rel, number, name in declared_function_candidates:
    if not re.search(rf"^\s*rule\s+{re.escape(name)}\s*\(", all_rule_text, flags=re.MULTILINE):
        print(f"{rel}:{number}:{name}")
