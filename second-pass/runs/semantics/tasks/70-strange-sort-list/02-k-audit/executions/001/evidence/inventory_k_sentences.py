#!/usr/bin/env python3
"""Source-level inventory of every relevant K sentence in the audited theory."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/recon")
FILES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "spec.k",
]

START = re.compile(
    r"^\s*(configuration|context(?:\s+alias)?|syntax(?:\s+(?:priority|associativity|lexical))?|"
    r"rule|claim|alias)\b"
)
BOUNDARY = re.compile(
    r"^\s*(?:configuration|context(?:\s+alias)?|syntax(?:\s+(?:priority|associativity|lexical))?|"
    r"rule|claim|alias|module|endmodule)\b"
)
MODULE = re.compile(r"^\s*module\s+([A-Za-z0-9_-]+)")

USED_MODULES = {
    "MPY-SYNTAX",
    "MPY-CORE",
    "MPY-OPERATORS",
    "MPY-INT",
    "MPY-LIST",
    "MPY-SUBSCRIPT",
    "MPY-CONTROLS",
    "MPY-FUNCTIONS",
    "MPY-BUILTINS",
    "MPY-CALL",
    "MPY-SORT",
    # Attribute evaluation passes through the generic bound-method dispatcher;
    # the append-specific priority rule preempts MPY-METHODS, so its overlap was
    # checked even though none of its named pure methods is invoked.
    "MPY-METHODS",
}


def normalized(lines: list[str]) -> str:
    pieces = []
    for line in lines:
        text = line.strip()
        if not text or text.startswith("//"):
            continue
        pieces.append(text)
    return " ".join(pieces)


records: list[dict[str, object]] = []
for path in FILES:
    lines = path.read_text().splitlines()
    current_module = "(assembly)"
    i = 0
    while i < len(lines):
        module_match = MODULE.match(lines[i])
        if module_match:
            current_module = module_match.group(1)
        start_match = START.match(lines[i])
        if not start_match:
            i += 1
            continue
        start = i
        j = i + 1
        while j < len(lines) and not BOUNDARY.match(lines[j]):
            j += 1
        block = normalized(lines[start:j])
        kind = start_match.group(1).replace(" ", "-")
        attrs = []
        for name in (
            "function",
            "total",
            "functional",
            "symbol",
            "no-evaluators",
            "priority",
            "simplification",
            "concrete",
            "owise",
            "macro",
            "strict",
            "seqstrict",
        ):
            if re.search(rf"\b{re.escape(name)}\b", block):
                attrs.append(name)

        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith("reference-semantics/"):
            origin = "FIXED_SUPPLIED_SEMANTICS"
            relevance = (
                "MODULE_AUDITED_FOR_REACHABILITY_AND_OVERLAP"
                if current_module in USED_MODULES
                else "INERT_FOR_SUBMITTED_PROGRAM"
            )
        elif rel == "verification.k":
            origin = "CANDIDATE_PROOF_EXTENSION"
            relevance = "AUDITED_LOCALLY"
        else:
            origin = "CANDIDATE_CLAIM"
            relevance = "AUDITED_LOCALLY"

        records.append(
            {
                "file": rel,
                "start": start + 1,
                "end": j,
                "module": current_module,
                "kind": kind,
                "attrs": ",".join(attrs) or "-",
                "origin": origin,
                "relevance": relevance,
                "sentence": block,
            }
        )
        i = j

print(
    "file\tlines\tmodule\tkind\tattributes\torigin\trelevance\tnormalized_sentence"
)
for record in records:
    print(
        f"{record['file']}\t{record['start']}-{record['end']}\t"
        f"{record['module']}\t{record['kind']}\t{record['attrs']}\t"
        f"{record['origin']}\t{record['relevance']}\t{record['sentence']}"
    )

print("\nSUMMARY")
print(f"files={len(FILES)}")
print(f"sentences={len(records)}")
for (origin, kind), count in sorted(
    Counter((str(r["origin"]), str(r["kind"])) for r in records).items()
):
    print(f"{origin}\t{kind}\t{count}")
for attr, count in sorted(
    Counter(
        attr
        for record in records
        for attr in str(record["attrs"]).split(",")
        if attr != "-"
    ).items()
):
    print(f"ATTRIBUTE\t{attr}\t{count}")
