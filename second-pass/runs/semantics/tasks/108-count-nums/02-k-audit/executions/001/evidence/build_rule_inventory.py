#!/usr/bin/env python3
"""Build a complete declaration/rule index for every K source in the audit."""

from __future__ import annotations

import collections
import re
from pathlib import Path


SOURCE_ROOT = Path("/tmp/audit-work/audit-108/source")
SEMANTICS_ROOT = SOURCE_ROOT / "reference-semantics"
OUTPUT = Path("/audit-output/evidence/rule_inventory.md")

files = [SEMANTICS_ROOT / "semantics.k"]
files.extend(sorted((SEMANTICS_ROOT / "semantics").glob("*.k")))
files.extend([SOURCE_ROOT / "verification.k", SOURCE_ROOT / "spec.k"])

start_re = re.compile(
    r"^\s*(configuration|syntax|rule|claim|context(?:\s+alias)?|alias)\b"
)
boundary_re = re.compile(
    r"^\s*(?:configuration|syntax|rule|claim|context(?:\s+alias)?|alias|"
    r"module|endmodule|imports?)\b"
)

records = []
for path in files:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [
        index
        for index, line in enumerate(lines)
        if start_re.match(line) is not None
    ]
    for position, index in enumerate(starts):
        next_index = len(lines)
        for probe in range(index + 1, len(lines)):
            if boundary_re.match(lines[probe]):
                next_index = probe
                break
        block_lines = lines[index:next_index]
        while block_lines and (
            not block_lines[-1].strip()
            or block_lines[-1].lstrip().startswith("//")
        ):
            block_lines.pop()
        block = "\n".join(block_lines)
        match = start_re.match(lines[index])
        assert match is not None
        kind = match.group(1).replace(" ", "-")
        relative = path.relative_to(SOURCE_ROOT)

        bracket_text = " ".join(re.findall(r"\[([^\]]+)\]", block))
        attrs = []
        for attr in [
            "function",
            "functional",
            "total",
            "symbol",
            "no-evaluators",
            "priority",
            "simplification",
            "concrete",
            "macro",
            "macro-rec",
            "owise",
            "strict",
            "seqstrict",
        ]:
            if re.search(rf"\b{re.escape(attr)}\b", bracket_text):
                attrs.append(attr)

        if relative == Path("verification.k"):
            if index + 1 >= 140:
                review_class = "proof-local operational bridge"
            else:
                review_class = "proof-local definition or exact-syntax macro"
        elif relative == Path("spec.k"):
            review_class = "target reachability claim"
        else:
            review_class = "integrity-checked supplied-semantics baseline"

        first_line = " ".join(lines[index].strip().split())
        records.append(
            {
                "path": str(relative),
                "line": index + 1,
                "kind": kind,
                "attrs": ", ".join(attrs) if attrs else "—",
                "review_class": review_class,
                "first_line": first_line.replace("|", "\\|"),
                "block": block,
            }
        )

counts = collections.Counter(record["kind"] for record in records)
classes = collections.Counter(record["review_class"] for record in records)

with OUTPUT.open("w", encoding="utf-8") as stream:
    stream.write("# Exhaustive K declaration and rule inventory\n\n")
    stream.write(
        "Generated from the fresh scratch copy. Each row is one K declaration, "
        "configuration, context, rule, or claim start; multiline bodies retain "
        "their source location and are available in the byte-checked source tree.\n\n"
    )
    stream.write(f"Total records: {len(records)}.\n\n")
    stream.write("Kinds: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())) + ".\n\n")
    stream.write(
        "Review classes: "
        + ", ".join(f"{k}={v}" for k, v in sorted(classes.items()))
        + ".\n\n"
    )
    stream.write("| # | Location | Kind | Attributes | Audit class | Declaration start |\n")
    stream.write("|---:|---|---|---|---|---|\n")
    for number, record in enumerate(records, 1):
        stream.write(
            f"| {number} | `{record['path']}:{record['line']}` | "
            f"{record['kind']} | {record['attrs']} | "
            f"{record['review_class']} | `{record['first_line']}` |\n"
        )

    opaque = [
        record
        for record in records
        if "symbol" in record["attrs"] or "no-evaluators" in record["attrs"]
    ]
    stream.write("\n## Opaque/symbol declarations\n\n")
    if not opaque:
        stream.write("None.\n")
    else:
        for record in opaque:
            stream.write(
                f"- `{record['path']}:{record['line']}`: "
                f"`{record['first_line'].replace(chr(92) + '|', '|')}`\n"
            )

    simplifications = [
        record for record in records if "simplification" in record["attrs"]
    ]
    stream.write("\n## Simplification declarations/rules\n\n")
    if simplifications:
        for record in simplifications:
            stream.write(f"- `{record['path']}:{record['line']}`\n")
    else:
        stream.write("None.\n")

print(f"output={OUTPUT}")
print(f"total_records={len(records)}")
for kind, count in sorted(counts.items()):
    print(f"{kind}={count}")
for review_class, count in sorted(classes.items()):
    print(f"class[{review_class}]={count}")
print(f"opaque_or_symbol_records={len(opaque)}")
print(f"simplification_records={len(simplifications)}")
