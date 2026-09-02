#!/usr/bin/env python3
"""Enumerate every declaration in the supplied MPY semantics and proof module."""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path("/tmp/audit-work/66-digitsum.dlRQYF/candidate")
OUTPUT = Path("/audit-output/evidence/k-rule-inventory.json")
SEMANTICS = ROOT / "reference-semantics"
FILES = sorted(SEMANTICS.rglob("*.k")) + [ROOT / "verification.k"]

START = re.compile(
    r"^\s*(?P<kind>"
    r"configuration|syntax|rule|claim|context(?:\s+alias)?|alias"
    r")\b"
)
MODULE = re.compile(r"^\s*(module|endmodule|imports|requires)\b")
KNOWN_ATTRIBUTES = (
    "function",
    "total",
    "functional",
    "macro",
    "macro-rec",
    "symbol",
    "no-evaluators",
    "priority",
    "simplification",
    "simplifier",
    "concrete",
    "owise",
    "strict",
    "seqstrict",
    "heat",
    "cool",
)


def source_group(path: Path) -> str:
    return "proof-extension" if path.name == "verification.k" else "trusted-supplied-semantics"


entries: list[dict[str, object]] = []
module_directives: list[dict[str, object]] = []

for path in FILES:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [
        index
        for index, line in enumerate(lines)
        if START.match(line)
    ]
    boundaries = starts + [len(lines)]
    for index, start in enumerate(starts):
        match = START.match(lines[start])
        assert match is not None
        next_start = boundaries[index + 1]
        end = next_start
        for possible_end in range(start + 1, next_start):
            if lines[possible_end].lstrip().startswith("endmodule"):
                end = possible_end
                break
        block_lines = lines[start:end]
        while block_lines and (
            not block_lines[-1].strip()
            or block_lines[-1].lstrip().startswith("//")
        ):
            block_lines.pop()
        text = "\n".join(block_lines)
        attributes = [
            attribute
            for attribute in KNOWN_ATTRIBUTES
            if re.search(rf"\b{re.escape(attribute)}\b", text)
        ]
        kind = match.group("kind")
        if kind == "rule":
            if "priority" in attributes:
                classification = "priority-rule"
            elif "simplification" in attributes or "simplifier" in attributes:
                classification = "simplification-rule"
            elif "concrete" in attributes:
                classification = "concrete-only-rule"
            elif "owise" in attributes:
                classification = "owise-rule"
            else:
                classification = "ordinary-rule"
        elif kind == "syntax":
            if "function" in attributes or "functional" in attributes:
                classification = "function-or-functional-declaration"
            elif "macro" in attributes or "macro-rec" in attributes:
                classification = "macro-syntax-declaration"
            else:
                classification = "syntax-declaration"
        else:
            classification = kind

        group = source_group(path)
        if group == "trusted-supplied-semantics":
            review_decision = (
                "ACCEPTED_AT_SELECTED_SEMANTICS_LEVEL: byte-identical entry in "
                "the trusted supplied-semantics tree; it defines the fixed MPY "
                "execution model rather than extending this candidate's proof."
            )
        else:
            review_decision = "REVIEWED_IN_STAGE_5_PROOF_EXTENSION_TABLE"

        entries.append(
            {
                "id": len(entries) + 1,
                "source_group": group,
                "file": str(path.relative_to(ROOT)),
                "line": start + 1,
                "kind": kind,
                "classification": classification,
                "attributes": attributes,
                "opaque_in_symbolic_backend": "no-evaluators" in attributes,
                "review_decision": review_decision,
                "text": text,
            }
        )

    for line_number, line in enumerate(lines, 1):
        if MODULE.match(line):
            module_directives.append(
                {
                    "file": str(path.relative_to(ROOT)),
                    "line": line_number,
                    "text": line.strip(),
                }
            )

counts = Counter(entry["classification"] for entry in entries)
attribute_counts = Counter(
    attribute
    for entry in entries
    for attribute in entry["attributes"]
)
per_file: dict[str, Counter[str]] = defaultdict(Counter)
for entry in entries:
    per_file[str(entry["file"])][str(entry["classification"])] += 1

document = {
    "scope": {
        "files": [str(path.relative_to(ROOT)) for path in FILES],
        "note": (
            "Every source declaration beginning with configuration, syntax, "
            "rule, claim, context/context alias, or alias is included. Module, "
            "import, require, and endmodule directives are separately listed."
        ),
    },
    "counts": dict(sorted(counts.items())),
    "attribute_counts": dict(sorted(attribute_counts.items())),
    "counts_by_file": {
        filename: dict(sorted(file_counts.items()))
        for filename, file_counts in sorted(per_file.items())
    },
    "module_directives": module_directives,
    "declarations": entries,
}

OUTPUT.write_text(
    json.dumps(document, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

print(f"files={len(FILES)}")
print(f"declarations={len(entries)}")
for classification, count in sorted(counts.items()):
    print(f"{classification}={count}")
print("attributes:")
for attribute, count in sorted(attribute_counts.items()):
    print(f"{attribute}={count}")
print("per-file:")
for filename, file_counts in sorted(per_file.items()):
    rendered = " ".join(
        f"{classification}={count}"
        for classification, count in sorted(file_counts.items())
    )
    print(f"{filename}: {rendered}")
print(f"inventory={OUTPUT}")
