#!/usr/bin/env python3
"""Lexical inventory of every local K outer sentence.

This is intentionally source based: it inventories what the reviewer audited
without trusting a candidate-compiled definition.
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
FILES = ["semantic.k", "solution-program.k", "verification.k", "spec.k"]
OUTER = re.compile(
    r"^\s*(requires|module|endmodule|imports|syntax|configuration|rule|claim|context|alias)\b"
)


def sentences(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines, 1):
        match = OUTER.match(line)
        if match:
            starts.append((index, match.group(1)))
    for position, (start, keyword) in enumerate(starts):
        if keyword in {"module", "endmodule"}:
            end = start
        else:
            next_start = starts[position + 1][0] if position + 1 < len(starts) else len(lines) + 1
            end = next_start - 1
            while end >= start and not lines[end - 1].strip():
                end -= 1
        text = " ".join(line.strip() for line in lines[start - 1 : end] if line.strip())
        yield start, end, keyword, text


def main() -> int:
    global_counts: Counter[str] = Counter()
    for filename in FILES:
        path = ROOT / filename
        print(f"FILE {filename}")
        local_counts: Counter[str] = Counter()
        serials: Counter[str] = Counter()
        for start, end, keyword, text in sentences(path):
            local_counts[keyword] += 1
            global_counts[keyword] += 1
            serials[keyword] += 1
            identity = f"{keyword.upper()}-{serials[keyword]:02d}"
            attributes = re.findall(r"\[([^\]]+)\]", text)
            attribute_text = ";".join(attributes) if attributes else "-"
            print(
                f"{identity} lines={start}-{end} attributes={attribute_text} :: {text}"
            )
        print(f"COUNTS {dict(sorted(local_counts.items()))}")
    print(f"GLOBAL_COUNTS {dict(sorted(global_counts.items()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
