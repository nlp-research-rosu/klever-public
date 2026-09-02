#!/usr/bin/env python3
"""Produce a bounded, exhaustive declaration/rule inventory for the audit."""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/38-decode-cyclic/candidate")
FILES = (
    [ROOT / "reference-semantics/semantics.k"]
    + sorted((ROOT / "reference-semantics/semantics").glob("*.k"))
    + [ROOT / "verification.k", ROOT / "spec.k"]
)
START = re.compile(r"^\s*(configuration|syntax|context|rule|claim)\b")


def target_relevant(path: Path, line: int) -> bool:
    name = path.name
    ranges = {
        "syntax.k": [(9, 61)],
        "core.k": [
            (13, 60),
            (123, 191),
            (193, 205),
            (208, 210),
            (227, 229),
        ],
        "int.k": [(6, 28)],
        "str.k": [(13, 26)],
        "subscript.k": [(16, 23), (25, 69), (71, 121)],
        "builtins.k": [(17, 26)],
        "call.k": [(15, 32), (69, 75)],
        "functions.k": [(8, 20), (62, 90)],
        "controls.k": [(46, 54)],
        "operators.k": [(10, 17)],
    }
    return any(lo <= line <= hi for lo, hi in ranges.get(name, []))


records = []
for path in FILES:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [
        (index, START.match(text).group(1))
        for index, text in enumerate(lines)
        if START.match(text)
    ]
    for position, (index, kind) in enumerate(starts):
        next_index = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        block_lines = lines[index:next_index]
        # Stop at endmodule, so the final record does not absorb later prose.
        for offset, text in enumerate(block_lines):
            if text.strip() == "endmodule":
                block_lines = block_lines[:offset]
                break
        flat = " ".join(
            text.strip()
            for text in block_lines
            if text.strip() and not text.lstrip().startswith("//")
        )
        flat = re.sub(r"\s+", " ", flat)
        attrs = []
        attribute_text = " ".join(re.findall(r"\[[^\]]*\]", flat))
        for marker in [
            "function",
            "functional",
            "total",
            "symbol",
            "no-evaluators",
            "priority",
            "priorities",
            "simplification",
            "owise",
            "concrete",
            "macro-rec",
            "macro",
            "strict",
            "seqstrict",
        ]:
            if re.search(rf"\b{re.escape(marker)}\b", attribute_text):
                attrs.append(marker)

        if "reference-semantics" in path.parts:
            source_class = "trusted-supplied-semantics"
            if "no-evaluators" in attrs:
                decision = "ACCEPT_TRUSTED_PRIMITIVE_UNUSED_BY_TARGET"
            elif target_relevant(path, index + 1):
                decision = "ACCEPT_TARGET_RELEVANT_FIXED_RULE"
            else:
                decision = "ACCEPT_FIXED_RULE_UNUSED_BY_TARGET"
        elif path.name == "verification.k":
            source_class = "candidate-proof-local"
            decision = "ACCEPT_PROOF_LOCAL_RULE"
        else:
            source_class = "candidate-positive-claims"
            decision = "ACCEPT_REACHABILITY_CLAIM"

        records.append(
            {
                "path": str(path.relative_to(ROOT)),
                "line": index + 1,
                "kind": kind,
                "attrs": ",".join(attrs) if attrs else "-",
                "source_class": source_class,
                "decision": decision,
                "statement": flat[:320],
            }
        )

print("INVENTORY_SCOPE:")
for path in FILES:
    print(f"  {path.relative_to(ROOT)}")
print(f"TOTAL_RECORDS: {len(records)}")
print("COUNTS_BY_KIND:")
for key, value in sorted(collections.Counter(r["kind"] for r in records).items()):
    print(f"  {key}: {value}")
print("COUNTS_BY_SOURCE_CLASS:")
for key, value in sorted(
    collections.Counter(r["source_class"] for r in records).items()
):
    print(f"  {key}: {value}")
print("COUNTS_BY_DECISION:")
for key, value in sorted(collections.Counter(r["decision"] for r in records).items()):
    print(f"  {key}: {value}")
print("COUNTS_BY_ATTRIBUTE:")
attribute_counter = collections.Counter()
for record in records:
    if record["attrs"] != "-":
        attribute_counter.update(record["attrs"].split(","))
for key, value in sorted(attribute_counter.items()):
    print(f"  {key}: {value}")
print("COUNTS_BY_FILE:")
for key, value in sorted(collections.Counter(r["path"] for r in records).items()):
    print(f"  {key}: {value}")
print()
print("id\tpath\tline\tkind\tattributes\tsource_class\tstatic_decision\tstatement")
for number, record in enumerate(records, 1):
    print(
        f"K{number:04d}\t{record['path']}\t{record['line']}\t"
        f"{record['kind']}\t{record['attrs']}\t{record['source_class']}\t"
        f"{record['decision']}\t{record['statement']}"
    )
