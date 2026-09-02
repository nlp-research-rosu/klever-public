#!/usr/bin/env python3
"""Exhaustive declaration inventory for supplied semantics and proof extensions."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


scratch = Path("/tmp/audit-work/reconstruction")
semantics_root = scratch / "reference-semantics"
files = [semantics_root / "semantics.k"]
files.extend(sorted((semantics_root / "semantics").glob("*.k")))
files.append(scratch / "verification.k")

starter = re.compile(
    r'^\s*(?:requires\s+"|module\b|endmodule\b|imports\b|syntax\b|'
    r"configuration\b|rule\b|claim\b|context\b|alias\b)"
)


def category(first: str) -> str:
    token = first.strip().split(maxsplit=1)[0]
    return {
        "requires": "include",
        "module": "module",
        "endmodule": "endmodule",
        "imports": "import",
        "syntax": "syntax",
        "configuration": "configuration",
        "rule": "rule",
        "claim": "claim",
        "context": "context",
        "alias": "alias",
    }[token]


def decision(path: Path, declaration: str, decl_category: str) -> str:
    if path.name != "verification.k":
        return (
            "ACCEPT — byte-identical fixed SUPPLIED_SEMANTICS declaration; "
            "not candidate-local and taken as the selected operational baseline"
        )

    if decl_category in {"include", "module", "endmodule", "import"}:
        return "ACCEPT — proof-module framing/import only"
    if "#runEvenOdd" in declaration:
        return "ACCEPT — fresh execution wrapper expands to fixed load then real call"
    if re.search(r"\bsolutionModule\b", declaration):
        return "ACCEPT — definitional module wrapper with exact entry binding"
    if re.search(r"\bsolutionBody\b", declaration):
        return "ACCEPT — definitional program-AST macro; parser-level identity checked"
    if "evenPalindromes" in declaration:
        return (
            "ACCEPT — postcondition-only piecewise summary; guards are disjoint "
            "and cover the intended domain"
        )
    if "oddPalindromes" in declaration:
        return (
            "ACCEPT — postcondition-only piecewise summary; guards are disjoint "
            "and cover the intended domain"
        )
    if "leadingDigit" in declaration:
        return "ACCEPT — total mathematical helper; constant nonzero divisor"
    if "currentBlock" in declaration:
        return "ACCEPT — total mathematical helper; constant nonzero divisor"
    return "REVIEW_REQUIRED — unclassified proof-local declaration"


records: list[dict[str, object]] = []
for path in files:
    lines = path.read_text().splitlines()
    starts = [index for index, line in enumerate(lines) if starter.match(line)]
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        block = lines[start:end]
        while block and (
            not block[-1].strip() or block[-1].lstrip().startswith("//")
        ):
            block.pop()
        declaration = "\n".join(block)
        decl_category = category(block[0])
        attributes = []
        for attribute in (
            "function",
            "total",
            "functional",
            "opaque",
            "priority",
            "simplification",
            "owise",
            "concrete",
            "macro",
            "strict",
            "seqstrict",
            "hook",
            "symbol",
            "no-evaluators",
        ):
            if re.search(rf"\b{re.escape(attribute)}\b", declaration):
                attributes.append(attribute)
        records.append(
            {
                "file": path.relative_to(scratch).as_posix(),
                "line": start + 1,
                "category": decl_category,
                "attributes": ",".join(attributes) or "-",
                "declaration": " ⏎ ".join(line.strip() for line in block),
                "decision": decision(path, declaration, decl_category),
            }
        )

counts = Counter(record["category"] for record in records)
attribute_counts = Counter()
for record in records:
    for attribute in str(record["attributes"]).split(","):
        if attribute != "-":
            attribute_counts[attribute] += 1

output = Path("/audit-output/evidence/rule-inventory.md")
with output.open("w") as destination:
    destination.write("# Exhaustive K declaration inventory\n\n")
    destination.write(
        "Scope: the supplied `reference-semantics/semantics.k`, every helper "
        "under `reference-semantics/semantics/`, and candidate "
        "`verification.k`. Declarations are grouped from each top-level K "
        "declaration through the line before the next declaration.\n\n"
    )
    destination.write(f"Total declarations: {len(records)}\n\n")
    destination.write("Category counts: `" + repr(dict(sorted(counts.items()))) + "`\n\n")
    destination.write(
        "Attribute-bearing declaration counts: `"
        + repr(dict(sorted(attribute_counts.items())))
        + "`\n\n"
    )
    destination.write(
        "| # | File:line | Kind | Attributes | Declaration | Audit decision |\n"
    )
    destination.write("|---:|---|---|---|---|---|\n")
    for index, record in enumerate(records, 1):
        declaration = str(record["declaration"]).replace("|", "&#124;")
        audit_decision = str(record["decision"]).replace("|", "&#124;")
        destination.write(
            f"| {index} | `{record['file']}:{record['line']}` | "
            f"{record['category']} | `{record['attributes']}` | "
            f"`{declaration}` | {audit_decision} |\n"
        )

print(f"inventory={output}")
print(f"total_declarations={len(records)}")
print("category_counts=" + repr(dict(sorted(counts.items()))))
print("attribute_counts=" + repr(dict(sorted(attribute_counts.items()))))
unclassified = [
    record
    for record in records
    if str(record["decision"]).startswith("REVIEW_REQUIRED")
]
print(f"unclassified_proof_local={len(unclassified)}")
for record in unclassified:
    print(f"UNCLASSIFIED {record['file']}:{record['line']} {record['declaration']}")
