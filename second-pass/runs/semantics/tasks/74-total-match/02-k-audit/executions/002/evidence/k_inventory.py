#!/usr/bin/env python3
"""Exhaustive source-level inventory of supplied semantics and proof extensions."""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/74-total-match")
FILES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "spec.k",
]
START = re.compile(
    r"^\s*(requires\b|module\b|endmodule\b|imports\b|configuration\b|"
    r"syntax\b|rule\b|context\b|claim\b|alias\b|macro\b)"
)


def records(path: Path):
    lines = path.read_text().splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        block_lines = lines[start:end]
        while block_lines and (
            not block_lines[-1].strip() or block_lines[-1].lstrip().startswith("//")
        ):
            block_lines.pop()
        text = " ".join(line.strip() for line in block_lines if line.strip())
        kind_match = START.match(lines[start])
        assert kind_match
        yield start + 1, end, kind_match.group(1), text


def main() -> None:
    counts = collections.Counter()
    attribute_counts = collections.Counter()
    print(f"INVENTORY_FILE_COUNT {len(FILES)}")
    for path in FILES:
        relative = path.relative_to(ROOT)
        file_records = list(records(path))
        print(f"\nFILE {relative} RECORDS {len(file_records)}")
        for start, end, kind, text in file_records:
            counts[kind] += 1
            attrs = []
            for attr in [
                "function",
                "total",
                "functional",
                "no-evaluators",
                "priority",
                "simplification",
                "concrete",
                "owise",
                "macro",
                "strict",
                "seqstrict",
                "hook",
                "symbol",
                "constructor",
                "anywhere",
            ]:
                if re.search(rf"\b{re.escape(attr)}\b", text):
                    attrs.append(attr)
                    attribute_counts[attr] += 1
            attribute_text = ",".join(attrs) if attrs else "-"
            print(
                f"{relative}:{start}-{end} KIND={kind} ATTRS={attribute_text} "
                f"TEXT={text}"
            )
    print(f"\nTOTAL_RECORDS {sum(counts.values())}")
    print(f"KIND_COUNTS {dict(sorted(counts.items()))}")
    print(f"ATTRIBUTE_RECORD_COUNTS {dict(sorted(attribute_counts.items()))}")


if __name__ == "__main__":
    main()
