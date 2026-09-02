#!/usr/bin/env python3
"""Generate an exhaustive declaration/rule inventory for the audited K tree."""

from collections import Counter, defaultdict
from pathlib import Path
import re


ROOT = Path("/tmp/audit-work/46-fib4-review")
SEMANTICS = ROOT / "reference-semantics"
OUTPUT = Path("/audit-output/evidence/rule-inventory.md")

files = [SEMANTICS / "semantics.k"]
files.extend(sorted((SEMANTICS / "semantics").glob("*.k")))
files.extend([ROOT / "verification.k", ROOT / "spec.k"])

declaration = re.compile(
    r"^\s*(syntax|rule|context|configuration|claim)\b"
)
boundary = re.compile(
    r"^\s*(syntax|rule|context|configuration|claim|module|endmodule|imports|requires)\b"
)

records = []
for path in files:
    lines = path.read_text().splitlines()
    starts = [
        index
        for index, line in enumerate(lines)
        if declaration.match(line)
    ]
    for position, start in enumerate(starts):
        end = len(lines)
        for probe in range(start + 1, len(lines)):
            if boundary.match(lines[probe]):
                end = probe
                break
        chunk_lines = lines[start:end]
        while chunk_lines and not chunk_lines[-1].strip():
            chunk_lines.pop()
        chunk = "\n".join(chunk_lines)
        code_only = "\n".join(
            line.split("//", 1)[0] for line in chunk_lines
        )
        kind = declaration.match(lines[start]).group(1)
        attrs = []
        for attr in (
            "function",
            "total",
            "functional",
            "symbol",
            "no-evaluators",
            "concrete",
            "simplification",
            "priority",
            "owise",
            "macro",
            "macro-rec",
            "strict",
            "seqstrict",
        ):
            if re.search(rf"\b{re.escape(attr)}\b", code_only):
                attrs.append(attr)
        if kind == "rule":
            subtype = "operational" if "<k>" in chunk else "equational"
        elif kind == "syntax":
            subtype = "function-or-symbol" if "function" in attrs else "declaration"
        else:
            subtype = kind
        records.append(
            {
                "path": str(path.relative_to(ROOT)),
                "line": start + 1,
                "kind": kind,
                "subtype": subtype,
                "attrs": ",".join(attrs) if attrs else "-",
                "chunk": chunk,
            }
        )

counts = Counter(record["kind"] for record in records)
by_file = defaultdict(Counter)
for record in records:
    by_file[record["path"]][record["kind"]] += 1

out = [
    "# Exhaustive K declaration and rule inventory",
    "",
    "Generated from the clean scratch copy. Every declaration below is quoted "
    "with its source line; no candidate-provided inventory was reused.",
    "",
    f"Total records: {len(records)}",
    "",
    f"Counts: {dict(sorted(counts.items()))}",
    "",
    "No local declaration or rule exists in `verification.k`; it only imports "
    "the fixed `MPY` semantics. The two `spec.k` claims are included.",
    "",
    "## Counts by file",
    "",
]
for path in sorted(by_file):
    out.append(f"- `{path}`: {dict(sorted(by_file[path].items()))}")

out.extend(["", "## Inventory", ""])
for number, record in enumerate(records, 1):
    out.append(
        f"### K-{number:04d} — `{record['path']}:{record['line']}`"
    )
    out.append("")
    out.append(
        f"Kind: {record['kind']}; subtype: {record['subtype']}; "
        f"attributes: {record['attrs']}."
    )
    out.append("")
    out.append("```k")
    out.append(record["chunk"])
    out.append("```")
    out.append("")

OUTPUT.write_text("\n".join(out))
print(f"output={OUTPUT}")
print(f"records={len(records)}")
print(f"counts={dict(sorted(counts.items()))}")
for path in sorted(by_file):
    print(f"{path} {dict(sorted(by_file[path].items()))}")
