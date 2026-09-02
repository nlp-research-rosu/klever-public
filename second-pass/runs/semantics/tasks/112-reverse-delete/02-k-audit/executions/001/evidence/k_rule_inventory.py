#!/usr/bin/env python3
"""Create a line-addressed inventory of K declarations and rules.

This is intentionally a source inventory, not a K parser. K statements in the
audited files begin with one of the recognized words and extend through their
following indented conditions/attributes until the next statement, comment,
module boundary, or blank line.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


START = re.compile(r"^\s*(configuration|syntax|context|rule|claim|alias)\b")
BOUNDARY = re.compile(
    r"^\s*(configuration|syntax|context|rule|claim|alias|module|endmodule|imports)\b"
)


def spans(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    entries = []
    i = 0
    while i < len(lines):
        match = START.match(lines[i])
        if match is None:
            i += 1
            continue
        kind = match.group(1)
        start = i
        i += 1
        while i < len(lines):
            line = lines[i]
            if not line.strip() or line.lstrip().startswith("//"):
                break
            if BOUNDARY.match(line):
                break
            i += 1
        text = "\n".join(lines[start:i]).strip()
        attributes = sorted(
            {
                attr
                for attr in (
                    "function",
                    "functional",
                    "total",
                    "simplification",
                    "priority",
                    "owise",
                    "concrete",
                    "macro",
                    "macro-rec",
                    "anywhere",
                    "symbol",
                    "no-evaluators",
                    "strict",
                    "seqstrict",
                )
                if re.search(rf"\b{re.escape(attr)}\b", text)
            }
        )
        if kind == "syntax":
            classification = "syntax-declaration"
        elif kind == "configuration":
            classification = "configuration"
        elif kind == "context":
            classification = "evaluation-context"
        elif kind == "claim":
            classification = "reachability-claim"
        elif "simplification" in attributes:
            classification = "simplification-rule"
        elif "priority" in attributes:
            classification = "priority-rule"
        elif "macro" in attributes or "macro-rec" in attributes:
            classification = "macro-rule"
        else:
            classification = "ordinary-rule"

        entries.append(
            {
                "file": str(path),
                "start_line": start + 1,
                "end_line": i,
                "kind": kind,
                "classification": classification,
                "attributes": attributes,
                "opaque": "no-evaluators" in attributes,
                "text": " ".join(text.split()),
            }
        )
    return entries


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--semantics-root", type=Path, required=True)
    parser.add_argument("--verification", type=Path, required=True)
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--json-output", type=Path, required=True)
    parser.add_argument("--markdown-output", type=Path, required=True)
    args = parser.parse_args()

    files = sorted(
        [args.semantics_root / "semantics.k"]
        + list((args.semantics_root / "semantics").glob("*.k"))
        + [args.verification, args.spec],
        key=lambda p: str(p),
    )
    records = []
    file_hashes = {}
    for path in files:
        file_hashes[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
        records.extend(spans(path))

    counts = {}
    for record in records:
        counts[record["classification"]] = (
            counts.get(record["classification"], 0) + 1
        )

    args.json_output.write_text(
        json.dumps(
            {
                "files": file_hashes,
                "counts": counts,
                "entry_count": len(records),
                "entries": records,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    rows = [
        "# Exhaustive K source inventory",
        "",
        f"Entries: {len(records)}",
        "",
        "| # | File:line | Class | Attributes | Opaque | Source statement |",
        "|---:|---|---|---|---|---|",
    ]
    for number, record in enumerate(records, 1):
        source = record["text"].replace("|", "&#124;")
        if len(source) > 420:
            source = source[:417] + "..."
        rows.append(
            "| {number} | `{file}:{start}-{end}` | {classification} | "
            "{attributes} | {opaque} | `{source}` |".format(
                number=number,
                file=record["file"],
                start=record["start_line"],
                end=record["end_line"],
                classification=record["classification"],
                attributes=", ".join(record["attributes"]) or "—",
                opaque="yes" if record["opaque"] else "no",
                source=source.replace("`", "\\`"),
            )
        )
    args.markdown_output.write_text("\n".join(rows) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "files": len(files),
                "entry_count": len(records),
                "counts": counts,
                "opaque_entries": sum(record["opaque"] for record in records),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
