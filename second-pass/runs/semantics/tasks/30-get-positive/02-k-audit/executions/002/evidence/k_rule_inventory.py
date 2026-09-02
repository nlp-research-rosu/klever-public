#!/usr/bin/env python3
"""Exhaustive source-level inventory of supplied and proof-local K declarations."""

from __future__ import annotations

import csv
import hashlib
import re
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/30-get-positive")
FILES = [
    SCRATCH / "reference-semantics" / "semantics.k",
    *sorted((SCRATCH / "reference-semantics" / "semantics").glob("*.k")),
    SCRATCH / "verification.k",
    SCRATCH / "spec.k",
]
OUTPUT = Path("/audit-output/evidence/k-rule-inventory.tsv")

START = re.compile(
    r"^\s*(configuration|context|rule|claim|syntax|priority)\b"
)
BOUNDARY = re.compile(
    r"^\s*(module|endmodule|imports|requires|configuration|context|rule|claim|syntax|priority)\b"
)
ATTRIBUTE = re.compile(r"\[([^\]]+)\]")


def classify(kind: str, text: str, path: Path) -> tuple[str, str]:
    attrs = ",".join(ATTRIBUTE.findall(text)).replace("\n", " ")
    labels: list[str] = []
    if kind == "syntax":
        labels.append("syntax-declaration")
        if "function" in text:
            labels.append("function-declaration")
        if re.search(r"\btotal\b", text):
            labels.append("total-declaration")
        if re.search(r"\bfunctional\b", text):
            labels.append("functional-declaration")
        if "no-evaluators" in text or "symbol(" in text:
            labels.append("opaque-symbol")
        if "macro" in text:
            labels.append("macro")
        if "strict" in text:
            labels.append("evaluation-order-declaration")
    elif kind == "configuration":
        labels.append("configuration")
    elif kind == "context":
        labels.append("evaluation-context")
    elif kind == "claim":
        labels.append("reachability-claim")
    elif kind == "priority":
        labels.append("priority-declaration")
    elif kind == "rule":
        labels.append("semantic-rule")
        if "priority(" in text:
            labels.append("priority-rule")
        if "[owise]" in text:
            labels.append("owise-rule")
        if "[concrete]" in text:
            labels.append("concrete-only-rule")
        if "simplification" in text:
            labels.append("simplification-rule")
        if path.name == "verification.k":
            labels.append("proof-local-rule")
    return attrs, ",".join(labels)


def blocks(path: Path) -> list[tuple[int, str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    found: list[tuple[int, str, str]] = []
    index = 0
    while index < len(lines):
        match = START.match(lines[index])
        if not match:
            index += 1
            continue
        kind = match.group(1)
        start = index
        index += 1
        while index < len(lines):
            if BOUNDARY.match(lines[index]):
                break
            index += 1
        body = lines[start:index]
        while body and (
            not body[-1].strip() or body[-1].lstrip().startswith("//")
        ):
            body.pop()
        found.append((start + 1, kind, "\n".join(body)))
    return found


def main() -> None:
    rows: list[dict[str, str | int]] = []
    counts: dict[str, int] = {}
    for path in FILES:
        if not path.is_file() or path.is_symlink():
            raise AssertionError(f"invalid K source: {path}")
        relative = path.relative_to(SCRATCH).as_posix()
        for line, kind, text in blocks(path):
            attrs, classification = classify(kind, text, path)
            counts[kind] = counts.get(kind, 0) + 1
            rows.append(
                {
                    "id": len(rows) + 1,
                    "file": relative,
                    "line": line,
                    "kind": kind,
                    "attributes": attrs,
                    "classification": classification,
                    "text": text.replace("\t", "  ").replace("\n", "\\n"),
                }
            )

    with OUTPUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=(
                "id",
                "file",
                "line",
                "kind",
                "attributes",
                "classification",
                "text",
            ),
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(rows)

    by_file: dict[str, dict[str, int]] = {}
    for row in rows:
        file_counts = by_file.setdefault(str(row["file"]), {})
        kind = str(row["kind"])
        file_counts[kind] = file_counts.get(kind, 0) + 1

    print(f"OUTPUT {OUTPUT}")
    print(f"SHA256 {hashlib.sha256(OUTPUT.read_bytes()).hexdigest()}")
    print(f"TOTAL_ENTRIES {len(rows)}")
    print(f"KIND_COUNTS {counts}")
    for file, file_counts in by_file.items():
        print(f"FILE {file} {file_counts}")
    print(
        "OPAQUE_SYMBOL_DECLARATIONS "
        f"{sum('opaque-symbol' in str(row['classification']) for row in rows)}"
    )
    print(
        "TOTAL_DECLARATIONS "
        f"{sum('total-declaration' in str(row['classification']) for row in rows)}"
    )
    print(
        "FUNCTIONAL_DECLARATIONS "
        f"{sum('functional-declaration' in str(row['classification']) for row in rows)}"
    )
    print(
        "PRIORITY_RULES "
        f"{sum('priority-rule' in str(row['classification']) for row in rows)}"
    )
    print(
        "SIMPLIFICATION_RULES "
        f"{sum('simplification-rule' in str(row['classification']) for row in rows)}"
    )
    print("INVENTORY_OK")


if __name__ == "__main__":
    main()
