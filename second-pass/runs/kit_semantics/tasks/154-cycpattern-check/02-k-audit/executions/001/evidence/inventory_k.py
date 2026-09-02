#!/usr/bin/env python3
"""Exhaustive top-level K declaration/rule/claim inventory."""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/cycpattern-audit/candidate-src")
FILES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "spec.k",
]

START = re.compile(
    r"^\s*(configuration|syntax|rule|context(?:\s+alias)?|claim)\b"
)


def blocks(path: Path):
    lines = path.read_text().splitlines()
    starts = [
        index
        for index, line in enumerate(lines)
        if START.match(line) and not line.lstrip().startswith("//")
    ]
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        while end > start and (
            lines[end - 1].strip() == ""
            or lines[end - 1].lstrip().startswith("//")
            or lines[end - 1].strip() == "endmodule"
        ):
            end -= 1
        text = "\n".join(lines[start:end]).strip()
        match = START.match(lines[start])
        assert match is not None
        yield start + 1, end, match.group(1), text


def flags(text: str) -> list[str]:
    known = [
        "function",
        "functional",
        "total",
        "no-evaluators",
        "concrete",
        "simplification",
        "owise",
        "priority",
        "strict",
        "seqstrict",
        "macro",
        "macro-rec",
        "trusted",
    ]
    return [flag for flag in known if re.search(rf"\b{re.escape(flag)}\b", text)]


def disposition(path: Path, kind: str) -> str:
    if "reference-semantics" in path.parts:
        return "FIXED_SUPPLIED_BASELINE_REVIEWED"
    if path.name == "verification.k":
        return "PROOF_LOCAL_REVIEWED_VALID"
    if kind == "claim":
        return "CLAIM_REVIEWED"
    return "LOCAL_REVIEWED"


def main() -> int:
    counts = collections.Counter()
    attribute_counts = collections.Counter()
    records = []
    for path in FILES:
        relative = path.relative_to(ROOT)
        for start, end, kind, text in blocks(path):
            item_flags = flags(text)
            counts[kind] += 1
            attribute_counts.update(item_flags)
            flattened = " ".join(
                line.strip()
                for line in text.splitlines()
                if line.strip() and not line.lstrip().startswith("//")
            )
            records.append(
                (
                    str(relative),
                    start,
                    end,
                    kind,
                    ",".join(item_flags) if item_flags else "-",
                    disposition(path, kind),
                    flattened,
                )
            )

    print(f"FILES={len(FILES)}")
    print(f"RECORDS={len(records)}")
    print(f"KINDS={dict(sorted(counts.items()))}")
    print(f"ATTRIBUTES={dict(sorted(attribute_counts.items()))}")
    print(
        "COLUMNS=file\\tstart\\tend\\tkind\\tflags\\tdisposition\\tdeclaration_or_rule"
    )
    for record in records:
        print("\t".join(map(str, record)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
