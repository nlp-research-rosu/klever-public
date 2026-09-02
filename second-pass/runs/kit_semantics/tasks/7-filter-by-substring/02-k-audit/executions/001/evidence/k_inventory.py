#!/usr/bin/env python3
"""Line-precise inventory of K declarations and rule starts."""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
FILES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "spec.k",
]
START = re.compile(
    r"^\s*(configuration|syntax|rule|claim|context\s+alias|context|"
    r"alias|macro|endmodule|module|imports|requires)\b"
)
RECOGNIZED_ATTRIBUTE = re.compile(
    r"\b(functional|function|total|owise|simplification|concrete|"
    r"no-evaluators|macro-rec|macro|strict|seqstrict|priority|symbol)"
    r"(?:\([^]]*\))?"
)


def main() -> int:
    counts: collections.Counter[str] = collections.Counter()
    attribute_counts: collections.Counter[str] = collections.Counter()
    print("file\tline\tkind\tattributes\ttext")
    for path in FILES:
        rel = path.relative_to(ROOT).as_posix()
        lines = path.read_text().splitlines()
        starts = [
            (index, match)
            for index, raw in enumerate(lines)
            if (match := START.match(raw)) is not None
        ]
        for position, (index, match) in enumerate(starts):
            next_index = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
            block_lines = lines[index:next_index]
            uncommented = "\n".join(line.split("//", 1)[0] for line in block_lines)
            attributes = []
            for bracket in re.findall(r"\[([^\]]*)\]", uncommented):
                for found in RECOGNIZED_ATTRIBUTE.finditer(bracket):
                    value = found.group(0)
                    attributes.append(value)
                    attribute_counts[found.group(1)] += 1
            kind = match.group(1).replace(" ", "_")
            counts[kind] += 1
            text = " ".join(
                line.strip()
                for line in block_lines
                if line.strip() and not line.lstrip().startswith("//")
            )
            print(
                f"{rel}\t{index + 1}\t{kind}\t{','.join(attributes)}\t{text}"
            )
    print("# COUNTS " + " ".join(f"{key}={counts[key]}" for key in sorted(counts)))
    print(
        "# ATTRIBUTE_COUNTS "
        + " ".join(
            f"{key}={attribute_counts[key]}" for key in sorted(attribute_counts)
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
