#!/usr/bin/env python3
"""Exhaustive source-level inventory of K declarations used by the audit."""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/129-minPath")
FILES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "spec.k",
]
START = re.compile(
    r"^(?:  )?(syntax|rule|claim|configuration|context|module|endmodule|imports|requires)\b"
)
ATTRIBUTE_WORDS = (
    "function",
    "functional",
    "total",
    "simplification",
    "concrete",
    "priority",
    "owise",
    "macro",
    "macro-rec",
    "symbol",
    "no-evaluators",
    "strict",
    "seqstrict",
)


def records(path: Path):
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))
    for ordinal, (index, kind) in enumerate(starts):
        end = starts[ordinal + 1][0] if ordinal + 1 < len(starts) else len(lines)
        block = "\n".join(lines[index:end]).rstrip()
        yield index + 1, kind, block


counts: collections.Counter[str] = collections.Counter()
attribute_counts: collections.Counter[str] = collections.Counter()
all_records: list[tuple[Path, int, str, str, list[str], str]] = []

for path in FILES:
    for line_number, kind, block in records(path):
        counts[kind] += 1
        uncommented = "\n".join(line.split("//", 1)[0] for line in block.splitlines())
        bracket_text = " ".join(re.findall(r"\[([^\]]*)\]", uncommented))
        attributes = [
            attribute
            for attribute in ATTRIBUTE_WORDS
            if re.search(rf"\b{re.escape(attribute)}\b", bracket_text)
        ]
        for attribute in attributes:
            attribute_counts[attribute] += 1
        if path.is_relative_to(ROOT / "reference-semantics"):
            disposition = (
                "TRUSTED_SUPPLIED_BASELINE; byte-identical candidate/reference; "
                "not a proof-local extension"
            )
        elif path.name == "verification.k":
            disposition = "CANDIDATE_PROOF_MODULE"
        elif kind == "claim":
            disposition = "TARGET_CLAIM; not an extension used to prove another claim"
        else:
            disposition = "SPEC_SCAFFOLD"
        all_records.append(
            (path, line_number, kind, block, attributes, disposition)
        )

print(f"FILES={len(FILES)}")
for path in FILES:
    print(f"FILE {path.relative_to(ROOT)}")
print(f"RECORD_COUNTS={dict(sorted(counts.items()))}")
print(f"ATTRIBUTE_RECORD_COUNTS={dict(sorted(attribute_counts.items()))}")
print(
    "OPAQUE_DECLARATIONS="
    + str(
        sum(
            kind == "syntax"
            and ("symbol" in attributes or "no-evaluators" in attributes)
            for _, _, kind, _, attributes, _ in all_records
        )
    )
)
print(
    "PROOF_LOCAL_RULES="
    + str(
        sum(
            path.name == "verification.k" and kind == "rule"
            for path, _, kind, _, _, _ in all_records
        )
    )
)
print(
    "PROOF_LOCAL_SYNTAX="
    + str(
        sum(
            path.name == "verification.k" and kind == "syntax"
            for path, _, kind, _, _, _ in all_records
        )
    )
)

for number, (path, line_number, kind, block, attributes, disposition) in enumerate(
    all_records, 1
):
    relative = path.relative_to(ROOT)
    print()
    print(
        f"RECORD {number:04d} source={relative}:{line_number} kind={kind} "
        f"attributes={attributes} disposition={disposition}"
    )
    print(block)
