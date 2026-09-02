#!/usr/bin/env python3
import collections
import re
from pathlib import Path


roots = [
    Path("/tmp/audit-work/work/reference-semantics"),
]
files = []
for root in roots:
    files.extend(sorted(root.rglob("*.k")))
files.extend(
    [
        Path("/tmp/audit-work/work/verification.k"),
        Path("/tmp/audit-work/work/spec.k"),
    ]
)

start_re = re.compile(
    r"^(?P<indent> {0,2})(?P<kind>requires|module|imports|syntax|configuration|rule|claim|context|endmodule)\b"
)
counts = collections.Counter()
attribute_counts = collections.Counter()
records = []

for path in files:
    lines = path.read_text().splitlines()
    starts = []
    for index, line in enumerate(lines):
        match = start_re.match(line)
        if match:
            starts.append((index, match.group("kind")))
    for pos, (start, kind) in enumerate(starts):
        end = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
        block = "\n".join(lines[start:end]).rstrip()
        counts[kind] += 1
        attrs = []
        if "[function" in block:
            attrs.append("function")
        if re.search(r"\btotal\b", block):
            attrs.append("total")
        if re.search(r"\bfunctional\b", block):
            attrs.append("functional")
        if "no-evaluators" in block:
            attrs.append("opaque/no-evaluators")
        if re.search(r"\bmacro(?:-rec)?\b", block):
            attrs.append("macro")
        if "simplification" in block or "simplifier" in block:
            attrs.append("simplification")
        if "[owise]" in block:
            attrs.append("owise")
        priorities = re.findall(r"priority\((\d+)\)", block)
        attrs.extend(f"priority({value})" for value in priorities)
        if kind == "rule":
            attrs.append("operational-k-rule" if "<k>" in block else "equational-rule")
        for attr in attrs:
            attribute_counts[attr] += 1
        records.append(
            {
                "path": str(path),
                "line": start + 1,
                "end": end,
                "kind": kind,
                "attrs": attrs,
                "block": block,
            }
        )

out = Path("/audit-output/evidence/rule-inventory.md")
with out.open("w", encoding="utf-8") as stream:
    stream.write("# Exhaustive K declaration and rule inventory\n\n")
    stream.write(
        "Generated from every `.k` source in the freshly copied supplied-semantics "
        "tree plus candidate `verification.k` and `spec.k`. Blocks begin at every "
        "top-level K directive and retain the complete multiline declaration/rule.\n\n"
    )
    stream.write(f"Files: {len(files)}\n\n")
    stream.write(f"Directive counts: `{dict(sorted(counts.items()))}`\n\n")
    stream.write(f"Attribute/class counts: `{dict(sorted(attribute_counts.items()))}`\n\n")
    current = None
    ordinal = 0
    for record in records:
        if record["path"] != current:
            current = record["path"]
            stream.write(f"## `{current}`\n\n")
        ordinal += 1
        attrs = ", ".join(record["attrs"]) if record["attrs"] else "none"
        stream.write(
            f"### {ordinal}. {record['kind']} at lines "
            f"{record['line']}-{record['end']} (attributes/classes: {attrs})\n\n"
        )
        stream.write("```k\n")
        stream.write(record["block"])
        stream.write("\n```\n\n")

print("FILES:", len(files))
print("DIRECTIVE_COUNTS:", dict(sorted(counts.items())))
print("ATTRIBUTE_CLASS_COUNTS:", dict(sorted(attribute_counts.items())))
print("RECORDS:", len(records))
print("OUTPUT:", out)
