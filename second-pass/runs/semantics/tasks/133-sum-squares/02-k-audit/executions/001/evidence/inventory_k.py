#!/usr/bin/env python3
"""Emit an exhaustive, line-addressable inventory of K declarations."""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path("/tmp/audit-work/133-sum-squares-audit")
FILES = [
    ROOT / "reference-semantics" / "semantics.k",
    *sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]
START = re.compile(
    r"^\s*(requires|module|endmodule|imports|configuration|syntax|rule|claim|"
    r"context(?:\s+alias)?|alias|macro)\b"
)


def kind_of(line: str) -> str:
    match = START.match(line)
    if match is None:
        raise ValueError(line)
    return match.group(1).replace(" ", "_")


def source_class(path: Path) -> str:
    if "reference-semantics" in path.parts:
        return "FIXED_SUPPLIED_SEMANTICS"
    if path.name == "verification.k":
        return "CANDIDATE_PROOF_EXTENSION"
    return "CANDIDATE_CLAIM"


def main() -> int:
    overall: Counter[str] = Counter()
    by_file: dict[str, Counter[str]] = defaultdict(Counter)
    serial = 0
    for path in FILES:
        lines = path.read_text().splitlines()
        starts = [index for index, line in enumerate(lines) if START.match(line)]
        rel = path.relative_to(ROOT).as_posix()
        print(f"===== FILE {rel} class={source_class(path)} lines={len(lines)} =====")
        for offset, start in enumerate(starts):
            end = (starts[offset + 1] - 1) if offset + 1 < len(starts) else len(lines) - 1
            while end > start and not lines[end].strip():
                end -= 1
            serial += 1
            kind = kind_of(lines[start])
            overall[kind] += 1
            by_file[rel][kind] += 1
            block = "\n".join(line.rstrip() for line in lines[start : end + 1]).strip()
            attrs = sorted(
                set(
                    re.findall(
                        r"\b(?:function|functional|total|simplification|concrete|owise|"
                        r"priority(?:\(\d+\))?|macro(?:-rec)?|symbol(?:\([^)]*\))?|"
                        r"no-evaluators|strict(?:\([^)]*\))?|seqstrict(?:\([^)]*\))?)\b",
                        block,
                    )
                )
            )
            opaque = "yes" if "no-evaluators" in block else "no"
            print(
                f"ITEM {serial:04d} kind={kind} lines={start + 1}-{end + 1} "
                f"opaque={opaque} attrs={','.join(attrs) if attrs else '-'}"
            )
            for source_line in block.splitlines():
                print(f"  {source_line}")
        print(
            "FILE_COUNTS "
            + " ".join(f"{kind}={count}" for kind, count in sorted(by_file[rel].items()))
        )
    print(f"TOTAL_ITEMS {serial}")
    print("TOTAL_COUNTS " + " ".join(f"{kind}={count}" for kind, count in sorted(overall.items())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
