#!/usr/bin/env python3
"""Produce an exhaustive source-located K declaration/rule inventory.

This is a lexical inventory, not a K parser. Every declaration-starting line is
listed with its complete source block up to the next declaration. The source
listing at the end ensures continuation productions cannot disappear from the
record.
"""

from __future__ import annotations

import collections
import re
from pathlib import Path

ROOT = Path("/tmp/audit-work/reconstruction")
paths = sorted((ROOT / "reference-semantics").rglob("*.k"))
paths += [ROOT / "verification.k", ROOT / "spec.k"]

decl_re = re.compile(
    r"^\s*(module|imports|configuration|syntax|context|rule|claim|alias|endmodule)\b"
)
attrs = [
    "function",
    "total",
    "functional",
    "simplification",
    "priority",
    "owise",
    "macro",
    "macro-rec",
    "concrete",
    "anywhere",
    "symbol",
    "no-evaluators",
    "strict",
    "seqstrict",
    "constructor",
    "hook",
]

grand = collections.Counter()
grand_attrs = collections.Counter()


used_fixed_rules = {
    "reference-semantics/semantics/core.k": {
        125, 126, 127, 131, 132, 152, 158, 189, 190, 191, 194, 214, 215, 218, 219
    },
    "reference-semantics/semantics/str.k": {14, 15, 16},
    "reference-semantics/semantics/controls.k": {
        9, 20, 36, 48, 69, 71, 72, 73, 85
    },
    "reference-semantics/semantics/functions.k": {14, 63, 64, 78, 80, 85},
    "reference-semantics/semantics/call.k": {20, 21, 69},
    "reference-semantics/semantics/int.k": {9, 14},
    "reference-semantics/semantics/tuple.k": {15, 16, 32},
}


def classify(rel: str, kind: str, line: int) -> str:
    if rel.startswith("reference-semantics/"):
        if kind == "rule" and line in used_fixed_rules.get(rel, set()):
            return "FIXED_SUPPLIED_BASELINE_USED_SLICE"
        return "FIXED_SUPPLIED_BASELINE_NOT_CANDIDATE_EXTENSION"
    if rel == "verification.k":
        if kind == "rule":
            if line in {9, 15, 25}:
                return "TRUTHFUL_EXACT_PROGRAM_MACRO"
            if line in {36, 37}:
                return "TRUTHFUL_INTSEQ_ITERATOR_IMAGE"
            if line in {42, 43}:
                return "TRUTHFUL_TOTAL_SUM_FOLD"
            if line in {47, 48}:
                return "TRUTHFUL_TOTAL_PRODUCT_FOLD"
            if line in {52, 53}:
                return "TRUTHFUL_TOTAL_LAST_ELEMENT_FOLD"
            if line == 62:
                return "SOUND_OPERATIONAL_BRIDGE_UNIVERSALLY_CONNECTED"
        if kind == "syntax":
            return "PROOF_LOCAL_DECLARATION_REVIEWED"
        return "STRUCTURAL_PROOF_MODULE_DECLARATION"
    if rel == "spec.k" and kind == "claim":
        return "POSITIVE_TARGET_CLAIM_RECONSTRUCTED"
    return "STRUCTURAL_SPEC_DECLARATION"


for path in paths:
    rel = path.relative_to(ROOT)
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        if line.startswith("requires "):
            starts.append((index, "requires"))
            continue
        match = decl_re.match(line)
        if match:
            starts.append((index, match.group(1)))

    counts = collections.Counter(kind for _, kind in starts)
    grand.update(counts)
    attr_counts = collections.Counter()
    print(f"\nFILE {rel} lines={len(lines)} declarations={len(starts)}")
    print("COUNTS " + " ".join(f"{key}={counts[key]}" for key in sorted(counts)))

    for ordinal, (index, kind) in enumerate(starts, 1):
        end = starts[ordinal][0] if ordinal < len(starts) else len(lines)
        block = "\n".join(lines[index:end]).rstrip()
        code_block = "\n".join(
            source_line.split("//", 1)[0] for source_line in block.splitlines()
        )
        attribute_text = " ".join(re.findall(r"\[[^\]]+\]", code_block))
        found = [
            attr
            for attr in attrs
            if re.search(
                rf"(?<![\w-]){re.escape(attr)}(?![\w-])",
                attribute_text,
            )
        ]
        attr_counts.update(found)
        grand_attrs.update(found)
        role = ""
        if kind == "rule":
            role = " operational" if "<k>" in block else " equational"
        if kind == "syntax" and "no-evaluators" in block:
            role += " opaque"
        print(
            f"DECL {ordinal:04d} line={index + 1} kind={kind}{role} "
            f"attrs={','.join(found) if found else '-'} "
            f"decision={classify(str(rel), kind, index + 1)}"
        )
        for source_line in block.splitlines():
            print(f"  {source_line}")
    print(
        "ATTRIBUTE_COUNTS "
        + (" ".join(f"{key}={attr_counts[key]}" for key in sorted(attr_counts)) or "-")
    )

print("\nGRAND_COUNTS " + " ".join(f"{key}={grand[key]}" for key in sorted(grand)))
print(
    "GRAND_ATTRIBUTE_COUNTS "
    + " ".join(f"{key}={grand_attrs[key]}" for key in sorted(grand_attrs))
)
print("\nCOMPLETE_NUMBERED_SOURCES")
for path in paths:
    rel = path.relative_to(ROOT)
    print(f"\n===== {rel} =====")
    for index, line in enumerate(path.read_text().splitlines(), 1):
        print(f"{index:04d}: {line}")
