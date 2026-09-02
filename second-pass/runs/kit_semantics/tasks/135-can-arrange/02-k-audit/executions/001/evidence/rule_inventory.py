"""Emit an exhaustive declaration/rule inventory for the audited K sources."""

from __future__ import annotations

import re
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/135-can-arrange")
sources = sorted((SCRATCH / "reference-semantics").rglob("*.k"))
sources += [
    SCRATCH / "verification.k",
    SCRATCH / "spec.k",
    SCRATCH / "connection-spec.k",
]

start_pattern = re.compile(
    r"^\s*(module|endmodule|syntax|configuration|"
    r"rule|claim|context|alias)\b"
)
record_pattern = re.compile(
    r"^\s*(syntax|configuration|rule|claim|context|alias)\b"
)


def compact(lines):
    return " ".join(line.strip() for line in lines if line.strip())


counts = {}
records = []
for path in sources:
    lines = path.read_text().splitlines()
    starts = [
        index
        for index, line in enumerate(lines)
        if start_pattern.match(line) and record_pattern.match(line)
    ]
    for position, begin in enumerate(starts):
        end = len(lines)
        for later in range(begin + 1, len(lines)):
            if start_pattern.match(lines[later]):
                end = later
                break
        block = compact(lines[begin:end])
        code_only = compact(
            line.split("//", 1)[0] for line in lines[begin:end]
        )
        kind = record_pattern.match(lines[begin]).group(1)
        attrs = []
        for attr in (
            "function",
            "functional",
            "total",
            "no-evaluators",
            "symbol",
            "simplification",
            "concrete",
            "priority",
            "owise",
            "macro",
            "strict",
            "seqstrict",
        ):
            if re.search(rf"\b{re.escape(attr)}\b", code_only):
                attrs.append(attr)
        if str(path).startswith(str(SCRATCH / "reference-semantics")):
            decision = "FIXED_SUPPLIED_BASELINE"
        elif kind == "claim":
            decision = "PROOF_OBLIGATION"
        else:
            decision = "CANDIDATE_LOCAL_REVIEW_REQUIRED"
        records.append(
            (
                str(path.relative_to(SCRATCH)),
                begin + 1,
                kind,
                ",".join(attrs) if attrs else "-",
                decision,
                block,
            )
        )
        key = (str(path.relative_to(SCRATCH)), kind)
        counts[key] = counts.get(key, 0) + 1

print("INVENTORY_VERSION 1")
print("SOURCE_FILE_COUNT", len(sources))
print("RECORD_COUNT", len(records))
print()
print("COUNTS_BY_FILE_AND_KIND")
for (path, kind), count in sorted(counts.items()):
    print(f"{path}\t{kind}\t{count}")
print()
print("RECORDS")
for path, line, kind, attrs, decision, block in records:
    print(
        f"{path}:{line}\t{kind}\tattrs={attrs}\t"
        f"decision={decision}\t{block}"
    )
