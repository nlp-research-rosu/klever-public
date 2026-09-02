#!/usr/bin/env python3
"""Exhaustive declaration/rule inventory for the fixed and proof-local K sources."""

from __future__ import annotations

import collections
import re
import sys
from pathlib import Path


ROOT = Path("/tmp/audit-work/86-anti-shuffle")
FIXED_ROOT = ROOT / "reference-semantics"
FILES = sorted(FIXED_ROOT.rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "spec.k",
]
START = re.compile(
    r"^\s*(requires|module|endmodule|imports|syntax|configuration|context|"
    r"rule|claim|alias)\b"
)
ATTR_NAMES = (
    "function",
    "functional",
    "total",
    "macro",
    "priority",
    "simplification",
    "concrete",
    "owise",
    "strict",
    "seqstrict",
    "symbol",
    "no-evaluators",
)


def records(path: Path) -> list[tuple[int, str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1)))
    output: list[tuple[int, str, str]] = []
    for pos, (start, kind) in enumerate(starts):
        stop = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
        body_lines = lines[start:stop]
        while body_lines and (
            not body_lines[-1].strip() or body_lines[-1].lstrip().startswith("//")
        ):
            body_lines.pop()
        flattened = " ".join(
            line.strip()
            for line in body_lines
            if line.strip() and not line.lstrip().startswith("//")
        )
        output.append((start + 1, kind, flattened))
    return output


def main() -> int:
    if any(not path.is_file() for path in FILES):
        missing = [str(path) for path in FILES if not path.is_file()]
        print(f"ERROR missing files={missing}")
        return 1
    total_counts: collections.Counter[str] = collections.Counter()
    attribute_counts: collections.Counter[str] = collections.Counter()
    opaque: list[str] = []
    priority: list[str] = []
    simplification: list[str] = []
    for path in FILES:
        rel = path.relative_to(ROOT)
        file_records = records(path)
        counts: collections.Counter[str] = collections.Counter(
            kind for _, kind, _ in file_records
        )
        total_counts.update(counts)
        print(f"FILE {rel} RECORDS={len(file_records)} COUNTS={dict(counts)}")
        for line, kind, text in file_records:
            identifier = f"{rel}:{line}"
            print(f"  {identifier} [{kind}] {text}")
            for attribute in ATTR_NAMES:
                if re.search(rf"\b{re.escape(attribute)}\b", text):
                    attribute_counts[attribute] += 1
            if "no-evaluators" in text:
                opaque.append(f"{identifier} {text}")
            if "priority" in text:
                priority.append(f"{identifier} {text}")
            if "simplification" in text:
                simplification.append(f"{identifier} {text}")
    print(f"TOTAL_FILES={len(FILES)}")
    print(f"TOTAL_RECORDS={sum(total_counts.values())}")
    print(f"TOTAL_COUNTS={dict(sorted(total_counts.items()))}")
    print(f"ATTRIBUTE_COUNTS={dict(sorted(attribute_counts.items()))}")
    print(f"OPAQUE_COUNT={len(opaque)}")
    for item in opaque:
        print(f"OPAQUE {item}")
    print(f"PRIORITY_COUNT={len(priority)}")
    for item in priority:
        print(f"PRIORITY {item}")
    print(f"SIMPLIFICATION_COUNT={len(simplification)}")
    for item in simplification:
        print(f"SIMPLIFICATION {item}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
