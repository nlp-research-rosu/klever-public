#!/usr/bin/env python3
"""Build a line-addressable exhaustive inventory of audited K sources."""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/candidate-src")
SEMANTICS = ROOT / "reference-semantics"
EXTRA = [ROOT / "verification.k", ROOT / "spec.k"]
START = re.compile(
    r"^\s*(configuration|syntax|rule|claim|context|context alias|alias)\b"
)


def classify(kind: str, block: str) -> list[str]:
    tags = [kind]
    attrs = {
        "function": r"\bfunction\b",
        "functional": r"\bfunctional\b",
        "total": r"\btotal\b",
        "simplification": r"\bsimplification\b",
        "priority": r"\bpriority\s*\(",
        "opaque": r"\bopaque\b",
        "macro": r"\bmacro\b",
        "strict": r"\bstrict\b",
        "seqstrict": r"\bseqstrict\b",
        "owise": r"\bowise\b",
        "anywhere": r"\banywhere\b",
    }
    for tag, pattern in attrs.items():
        if re.search(pattern, block):
            tags.append(tag)
    if kind == "rule" and "simplification" not in tags and "macro" not in tags:
        tags.append("ordinary-rule")
    return tags


def source_paths() -> list[Path]:
    return sorted(SEMANTICS.rglob("*.k")) + EXTRA


def entries(path: Path):
    lines = path.read_text().splitlines()
    starts = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))
    for position, (index, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        block_lines = lines[index:end]
        while block_lines and not block_lines[-1].strip():
            block_lines.pop()
        block = "\n".join(block_lines)
        yield index + 1, end, kind, block


def main() -> int:
    print("AUDITED SOURCE MANIFEST")
    for path in source_paths():
        data = path.read_bytes()
        print(
            f"{path.relative_to(ROOT)} bytes={len(data)} "
            f"sha256={hashlib.sha256(data).hexdigest()}"
        )

    totals = Counter()
    records = []
    for path in source_paths():
        for start, end, kind, block in entries(path):
            tags = classify(kind, block)
            totals.update(tags)
            records.append((path, start, end, tags, block))

    print("\nINVENTORY COUNTS")
    for key in sorted(totals):
        print(f"{key}={totals[key]}")
    print(f"records={len(records)}")

    print("\nEXHAUSTIVE DECLARATION AND RULE INVENTORY")
    for number, (path, start, end, tags, block) in enumerate(records, 1):
        relative = path.relative_to(ROOT)
        print(
            f"\nENTRY {number:04d} {relative}:{start}-{end} "
            f"tags={','.join(tags)}"
        )
        for offset, line in enumerate(block.splitlines(), start):
            print(f"{offset:5d} | {line}")

    print("\nOPAQUE TOKEN CHECK")
    opaque = []
    for path in source_paths():
        for line_number, line in enumerate(path.read_text().splitlines(), 1):
            if re.search(r"\bopaque\b", line):
                opaque.append((path.relative_to(ROOT), line_number, line))
    print(f"opaque_occurrences={len(opaque)}")
    for path, line_number, line in opaque:
        print(f"{path}:{line_number}: {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
