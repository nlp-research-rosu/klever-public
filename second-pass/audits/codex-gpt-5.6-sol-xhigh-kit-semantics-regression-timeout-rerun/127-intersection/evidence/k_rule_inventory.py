#!/usr/bin/env python3
"""Enumerate every local K declaration/rule in the audited source closure."""

import collections
import hashlib
import re
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/scratch")
OUTPUT = Path("/audit-output/evidence/rule-inventory.tsv")
SUMMARY = Path("/audit-output/evidence/rule-inventory-summary.txt")

KEYWORD = re.compile(
    r"^\s*(configuration|syntax|rule|claim|context|alias)\b"
)
ATTRIBUTES = (
    "function",
    "functional",
    "total",
    "opaque",
    "symbol",
    "no-evaluators",
    "priority",
    "simplification",
    "owise",
    "concrete",
)


def classify(keyword, text):
    attrs = []
    for attribute in ATTRIBUTES:
        if attribute == "no-evaluators":
            present = attribute in text
        elif attribute == "symbol":
            present = re.search(r"\bsymbol(?:\(|\b)", text) is not None
        else:
            present = re.search(rf"\b{re.escape(attribute)}\b", text) is not None
        if present:
            attrs.append(attribute)
    if keyword == "syntax":
        kind = "SYNTAX"
        if "function" in attrs:
            kind += "_FUNCTION"
        if "functional" in attrs:
            kind += "_FUNCTIONAL"
        if "total" in attrs:
            kind += "_TOTAL"
        if "opaque" in attrs or "no-evaluators" in attrs:
            kind += "_OPAQUE"
    elif keyword == "rule":
        if "simplification" in attrs:
            kind = "RULE_SIMPLIFICATION"
        elif "priority" in attrs:
            kind = "RULE_PRIORITY"
        else:
            kind = "RULE_ORDINARY"
    else:
        kind = keyword.upper()
    return kind, ",".join(attrs) if attrs else "-"


def source_role(path):
    if path.name == "verification.k":
        return "PROOF_LOCAL"
    if path.name == "spec.k":
        return "SPEC_CLAIM"
    return "FIXED_SUPPLIED_SEMANTICS"


def relative_name(path):
    return str(path.relative_to(SCRATCH))


def declarations(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    current = None
    for number, line in enumerate(lines, 1):
        match = KEYWORD.match(line)
        if match:
            if current is not None:
                yield current
            current = {
                "keyword": match.group(1),
                "line": number,
                "lines": [line.strip()],
            }
        elif current is not None:
            stripped = line.strip()
            if (
                stripped.startswith(("module ", "endmodule", "imports "))
                or line.startswith("requires ")
            ):
                yield current
                current = None
            elif stripped.startswith("//"):
                yield current
                current = None
            elif stripped:
                current["lines"].append(stripped)
            elif current["keyword"] == "configuration":
                yield current
                current = None
    if current is not None:
        yield current


def main():
    files = [
        SCRATCH / "reference-semantics" / "semantics.k",
        *sorted((SCRATCH / "reference-semantics" / "semantics").glob("*.k")),
        SCRATCH / "verification.k",
        SCRATCH / "spec.k",
    ]

    rows = []
    counts = collections.Counter()
    file_counts = collections.Counter()
    for path in files:
        for index, declaration in enumerate(declarations(path), 1):
            text = " ".join(declaration["lines"])
            text = re.sub(r"\s+", " ", text)
            kind, attrs = classify(declaration["keyword"], text)
            role = source_role(path)
            decision = {
                "FIXED_SUPPLIED_SEMANTICS": (
                    "DEFINES_SELECTED_BASELINE; integrity-verified; "
                    "used-path rules separately audited"
                ),
                "PROOF_LOCAL": "REQUIRES_MANUAL_RULE_JUDGMENT",
                "SPEC_CLAIM": "REQUIRES_ADEQUACY_AND_RECONSTRUCTION_CHECK",
            }[role]
            digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
            rows.append(
                (
                    f"K{len(rows) + 1:04d}",
                    relative_name(path),
                    str(declaration["line"]),
                    kind,
                    attrs,
                    role,
                    decision,
                    digest,
                    text,
                )
            )
            counts[kind] += 1
            file_counts[relative_name(path)] += 1

    header = (
        "id",
        "file",
        "line",
        "kind",
        "attributes",
        "source_role",
        "decision",
        "sha256_16",
        "normalized_declaration",
    )
    with OUTPUT.open("w", encoding="utf-8") as stream:
        stream.write("\t".join(header) + "\n")
        for row in rows:
            stream.write("\t".join(row) + "\n")

    with SUMMARY.open("w", encoding="utf-8") as stream:
        stream.write(f"TOTAL_INVENTORY_ENTRIES={len(rows)}\n")
        stream.write("COUNTS_BY_KIND\n")
        for kind, count in sorted(counts.items()):
            stream.write(f"{kind}\t{count}\n")
        stream.write("COUNTS_BY_FILE\n")
        for file_name, count in sorted(file_counts.items()):
            stream.write(f"{file_name}\t{count}\n")
        stream.write(f"INVENTORY_SHA256={hashlib.sha256(OUTPUT.read_bytes()).hexdigest()}\n")

    print(f"inventory={OUTPUT}")
    print(f"summary={SUMMARY}")
    print(f"entries={len(rows)}")


if __name__ == "__main__":
    main()
