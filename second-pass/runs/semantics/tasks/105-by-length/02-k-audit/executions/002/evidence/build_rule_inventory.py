#!/usr/bin/env python3
"""Create a complete declaration/rule inventory for the audited K sources."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import re


SCRATCH = Path("/tmp/audit-work/105-by-length/recon")
OUTPUT = Path("/audit-output/evidence/RULE-INVENTORY.md")
ENTRY = re.compile(r"^\s*(configuration|syntax|context|rule|claim)\b")
ATTRIBUTES = (
    "function",
    "functional",
    "total",
    "no-evaluators",
    "symbol",
    "priority",
    "simplification",
    "concrete",
    "owise",
    "macro",
    "strict",
    "seqstrict",
    "anywhere",
)


def disposition(source: str, kind: str, line: int, text: str) -> str:
    if source == "proof-local":
        if kind == "rule" and line in {98, 126}:
            return (
                "REJECT—unsound operational bridge; arbitrary-continuation "
                "integer-list counterexample is machine-checked in "
                "04-bridge-witnesses.log"
            )
        if kind == "syntax" and (
            "filterDigits(ValSeq)" in text or "tableNames(ValSeq)" in text
        ):
            return (
                "LIMITATION—[total] domain is broader than the constructor "
                "equations; uses reached by the target are integer-only"
            )
        return (
            "ACCEPTED LOCALLY—truthful constructor definition, guarded "
            "mathematical equation, or post-execution observation"
        )
    if source == "target-spec":
        return "TARGET OBLIGATION—adequacy and non-vacuity reviewed separately"
    if "no-evaluators" in text:
        if "sortVS(ValSeq)" in text:
            return (
                "ACCEPTED SUPPLIED TRUST BOUNDARY—opaque ascending sort; "
                "material to this theorem and accounted explicitly"
            )
        return (
            "ACCEPTED SUPPLIED TRUST BOUNDARY—opaque fixed-semantics primitive; "
            "not reached by this integer-list program"
        )
    return (
        "ACCEPTED FIXED BASELINE—candidate copy is byte-identical; no "
        "task-specific conclusion and no adverse interaction found"
    )


files = [SCRATCH / "reference-semantics" / "semantics.k"]
files += sorted((SCRATCH / "reference-semantics" / "semantics").glob("*.k"))
files += [SCRATCH / "verification.k", SCRATCH / "spec.k"]

records: list[dict[str, object]] = []
for path in files:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [
        (index, ENTRY.match(line).group(1))
        for index, line in enumerate(lines)
        if ENTRY.match(line)
    ]
    for position, (start, kind) in enumerate(starts):
        stop = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        while stop > start + 1 and not lines[stop - 1].strip():
            stop -= 1
        text = "\n".join(lines[start:stop])
        if path.name == "verification.k":
            source = "proof-local"
        elif path.name == "spec.k":
            source = "target-spec"
        else:
            source = "supplied-fixed"
        attributes = [
            attribute
            for attribute in ATTRIBUTES
            if re.search(rf"\b{re.escape(attribute)}\b", text)
        ]
        records.append(
            {
                "path": path.relative_to(SCRATCH).as_posix(),
                "source": source,
                "kind": kind,
                "start": start + 1,
                "stop": stop,
                "text": text,
                "attributes": attributes,
                "disposition": disposition(source, kind, start + 1, text),
            }
        )

kind_counts = Counter(str(record["kind"]) for record in records)
source_counts = Counter(str(record["source"]) for record in records)
attribute_counts = Counter(
    attribute
    for record in records
    for attribute in record["attributes"]  # type: ignore[union-attr]
)
for attribute in ATTRIBUTES:
    attribute_counts[attribute] += 0

with OUTPUT.open("w", encoding="utf-8") as stream:
    stream.write("# Exhaustive K declaration and rule inventory\n\n")
    stream.write(
        "Generated from the clean scratch copies of every supplied semantics "
        "file plus `verification.k` and `spec.k`. Each top-level "
        "`configuration`, `syntax`, `context`, `rule`, and `claim` entry is "
        "listed exactly once. “Accepted fixed baseline” means the declaration "
        "belongs to the launcher-supplied semantics tree, whose candidate copy "
        "is byte-identical; it does not turn opaque primitives into proved "
        "Python facts.\n\n"
    )
    stream.write(f"- Total entries: {len(records)}\n")
    stream.write(f"- Kinds: {dict(sorted(kind_counts.items()))}\n")
    stream.write(f"- Sources: {dict(sorted(source_counts.items()))}\n")
    stream.write(f"- Attribute flags: {dict(sorted(attribute_counts.items()))}\n\n")
    for number, record in enumerate(records, 1):
        stream.write(f"## K-{number:04d}\n\n")
        stream.write(
            f"- Location: `{record['path']}:{record['start']}`"
            f"–`{record['stop']}`\n"
        )
        stream.write(f"- Source class: {record['source']}\n")
        stream.write(f"- Entry kind: {record['kind']}\n")
        stream.write(
            f"- Attribute flags: {', '.join(record['attributes']) or 'none'}\n"
        )
        stream.write(f"- Audit disposition: {record['disposition']}\n\n")
        stream.write("```k\n")
        stream.write(str(record["text"]))
        stream.write("\n```\n\n")

print(f"WROTE: {OUTPUT}")
print(f"TOTAL_ENTRIES: {len(records)}")
print(f"KIND_COUNTS: {dict(sorted(kind_counts.items()))}")
print(f"SOURCE_COUNTS: {dict(sorted(source_counts.items()))}")
print(f"ATTRIBUTE_COUNTS: {dict(sorted(attribute_counts.items()))}")
