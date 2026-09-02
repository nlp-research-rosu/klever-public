#!/usr/bin/env python3
"""Produce a line-addressable inventory of all submitted and supplied K records."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/20-find-closest-elements")
OUTPUT = Path("/audit-output/evidence/rule_inventory.md")
START = re.compile(
    r"^(?P<indent>[ \t]*)(?P<kind>requires|module|endmodule|syntax|"
    r"configuration|context|rule|claim)\b"
)


def classification(kind: str, text: str, supplied: bool) -> str:
    labels: list[str] = ["supplied" if supplied else "proof-local"]
    if kind == "syntax":
        if "function" in text:
            labels.append("function")
        if re.search(r"\btotal\b", text):
            labels.append("total")
        if re.search(r"\bfunctional\b", text):
            labels.append("functional")
        if "no-evaluators" in text:
            labels.append("opaque/no-evaluators")
        if "macro" in text:
            labels.append("macro")
    elif kind == "rule":
        if "simplification" in text:
            labels.append("simplification")
        elif "concrete" in text:
            labels.append("concrete")
        else:
            labels.append("ordinary")
        priority = re.search(r"priority\((\d+)\)", text)
        if priority:
            labels.append(f"priority({priority.group(1)})")
        if "owise" in text:
            labels.append("owise")
    elif kind == "claim":
        labels.append("reachability-claim")
    elif kind == "context":
        labels.append("evaluation-context")
    return ", ".join(labels)


paths = sorted((SCRATCH / "reference-semantics").rglob("*.k"))
paths += sorted(
    path
    for path in SCRATCH.glob("*.k")
    if not path.name.endswith("-mutated.k") and not path.name.startswith("audit-")
)

records: list[tuple[Path, int, str, str, str]] = []
for path in paths:
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match and len(match.group("indent").expandtabs()) <= 2:
            starts.append((index, match.group("kind")))
    for position, (index, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        block = " ".join(part.strip() for part in lines[index:end] if part.strip())
        block = re.sub(r"\s+", " ", block)
        supplied = "reference-semantics" in path.parts
        records.append(
            (
                path.relative_to(SCRATCH),
                index + 1,
                kind,
                classification(kind, block, supplied),
                block,
            )
        )

counts = Counter((str(path), kind) for path, _line, kind, _class, _text in records)
kind_counts = Counter(kind for _path, _line, kind, _class, _text in records)
class_counts = Counter(
    label.strip()
    for _path, _line, _kind, labels, _text in records
    for label in labels.split(",")
)

with OUTPUT.open("w") as stream:
    stream.write("# Exhaustive K-source inventory\n\n")
    stream.write(
        "Generated from the fresh scratch sources. The supplied tree is "
        "byte-identical to `/reference/reference-semantics`; proof-local means "
        "a candidate-authored K source outside that trusted tree.\n\n"
    )
    stream.write(f"Total records: {len(records)}. Kind counts: `{dict(kind_counts)}`.\n\n")
    stream.write(f"Classification counts: `{dict(class_counts)}`.\n\n")
    stream.write("## Counts by file\n\n")
    stream.write("| File | Kind | Count |\n|---|---:|---:|\n")
    for (path, kind), count in sorted(counts.items()):
        stream.write(f"| `{path}` | {kind} | {count} |\n")
    stream.write("\n## Every record\n\n")
    stream.write("| ID | Location | Kind/class | Source record |\n")
    stream.write("|---:|---|---|---|\n")
    for record_id, (path, line, kind, labels, text) in enumerate(records, 1):
        escaped = text.replace("|", "\\|").replace("`", "\\`")
        stream.write(
            f"| {record_id} | `{path}:{line}` | {kind}; {labels} | `{escaped}` |\n"
        )

print(f"output={OUTPUT}")
print(f"records={len(records)}")
print(f"kind_counts={dict(kind_counts)}")
print(f"classification_counts={dict(class_counts)}")
