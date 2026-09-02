#!/usr/bin/env python3
"""Create a line-addressable inventory of every local K declaration/rule."""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path


SEM_ROOT = Path("/tmp/audit-work/46-fib4-audit/candidate-src/reference-semantics")
LOCAL_FILES = [SEM_ROOT / "semantics.k", *sorted((SEM_ROOT / "semantics").glob("*.k"))]
LOCAL_FILES += [
    Path("/tmp/audit-work/46-fib4-audit/candidate-src/verification.k"),
    Path("/tmp/audit-work/46-fib4-audit/candidate-src/spec.k"),
]

USED_MODULE_FILES = {
    "semantics.k",
    "semantics/syntax.k",
    "semantics/core.k",
    "semantics/functions.k",
    "semantics/controls.k",
    "semantics/call.k",
    "semantics/operators.k",
    "semantics/int.k",
    "semantics/assert.k",
}

start_re = re.compile(
    r"^\s*(module|endmodule|imports|configuration|syntax|context|rule|claim)\b"
)


def rel(path: Path) -> str:
    if path.is_relative_to(SEM_ROOT):
        return str(path.relative_to(SEM_ROOT))
    return path.name


records: list[dict[str, object]] = []
for path in LOCAL_FILES:
    lines = path.read_text().splitlines()
    starts = [(i, start_re.match(line).group(1)) for i, line in enumerate(lines) if start_re.match(line)]
    for pos, (start, kind) in enumerate(starts):
        end = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
        code_lines = []
        for raw in lines[start:end]:
            code = raw.split("//", 1)[0].strip()
            if code:
                code_lines.append(code)
        text = " ".join(code_lines)
        attrs = []
        for attr in (
            "function",
            "functional",
            "total",
            "simplification",
            "owise",
            "no-evaluators",
        ):
            if re.search(rf"\b{re.escape(attr)}\b", text):
                attrs.append(attr)
        priority = re.search(r"priority\(([^)]+)\)", text)
        if priority:
            attrs.append(f"priority({priority.group(1)})")

        source = rel(path)
        if source == "spec.k":
            disposition = "CLAIM_REVIEWED_IN_STAGES_4_AND_6"
        elif source == "verification.k":
            disposition = "NO_PROOF_EXTENSION_IMPORT_ONLY"
        elif source in USED_MODULE_FILES:
            disposition = "ACCEPTED_FIXED_SEMANTICS_USED_PATH"
        else:
            disposition = "ACCEPTED_FIXED_SEMANTICS_DISJOINT_OR_UNUSED_PATH"

        records.append(
            {
                "source": source,
                "line": start + 1,
                "kind": kind,
                "attrs": ",".join(attrs) if attrs else "-",
                "disposition": disposition,
                "text": text.replace("|", "\\|"),
            }
        )

counts = Counter(str(row["kind"]) for row in records)
attribute_counts: Counter[str] = Counter()
for row in records:
    for attr in str(row["attrs"]).split(","):
        if attr != "-":
            attribute_counts[attr] += 1
per_file: dict[str, Counter[str]] = defaultdict(Counter)
for row in records:
    per_file[str(row["source"])][str(row["kind"])] += 1

print("# Exhaustive local K inventory")
print()
print("Scope: the trusted supplied-semantics scratch copy plus candidate `verification.k` and `spec.k`.")
print("Imported K standard-library modules are outside this local-source inventory.")
print()
print("## Totals")
print()
print("| kind | count |")
print("|---|---:|")
for kind in sorted(counts):
    print(f"| {kind} | {counts[kind]} |")
print()
print("## Attribute/classifier totals")
print()
print("| attribute/classifier | count |")
print("|---|---:|")
for attr in sorted(attribute_counts):
    print(f"| {attr} | {attribute_counts[attr]} |")
if not attribute_counts:
    print("| (none) | 0 |")
print()
print("## Counts by file")
print()
print("| file | syntax | rule | claim | context | configuration | other directives |")
print("|---|---:|---:|---:|---:|---:|---:|")
for source in sorted(per_file):
    c = per_file[source]
    other = sum(c[k] for k in ("module", "endmodule", "imports"))
    print(
        f"| {source} | {c['syntax']} | {c['rule']} | {c['claim']} | "
        f"{c['context']} | {c['configuration']} | {other} |"
    )
print()
print("## Every declaration, rule, and claim")
print()
print("| file:line | kind | attributes/classifiers | disposition | normalized source record |")
print("|---|---|---|---|---|")
for row in records:
    print(
        f"| {row['source']}:{row['line']} | {row['kind']} | {row['attrs']} | "
        f"{row['disposition']} | {row['text']} |"
    )
