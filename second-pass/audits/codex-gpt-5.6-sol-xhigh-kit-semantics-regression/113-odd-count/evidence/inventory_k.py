#!/usr/bin/env python3
"""Create a line-numbered inventory of top-level K declarations and rules."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


START = re.compile(
    r"^(?:(requires|module|endmodule)\b|  (imports|configuration|syntax|rule|"
    r"claim|context alias|context|alias)\b)"
)
ENTRY_KINDS = {
    "configuration",
    "syntax",
    "rule",
    "claim",
    "context",
    "context alias",
    "alias",
}


def blocks(path: Path) -> list[tuple[int, str, str]]:
    lines = path.read_text().splitlines()
    starts: list[int] = []
    for index, line in enumerate(lines):
        if START.match(line):
            starts.append(index)
    result: list[tuple[int, str, str]] = []
    for pos, start in enumerate(starts):
        match = START.match(lines[start])
        assert match
        kind = match.group(1) or match.group(2)
        if kind not in ENTRY_KINDS:
            continue
        end = starts[pos + 1] if pos + 1 < len(starts) else len(lines)
        text = "\n".join(lines[start:end]).rstrip()
        result.append((start + 1, kind, text))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()
    total = 0
    by_kind: dict[str, int] = {}
    for path in sorted(args.paths):
        entries = blocks(path)
        print(f"FILE {path} ENTRIES {len(entries)}")
        for ordinal, (line, kind, text) in enumerate(entries, start=1):
            total += 1
            by_kind[kind] = by_kind.get(kind, 0) + 1
            attributes = []
            for attr in [
                "function",
                "total",
                "functional",
                "simplification",
                "macro",
                "priority",
                "owise",
                "strict",
                "seqstrict",
                "symbol",
                "token",
                "bracket",
            ]:
                if re.search(rf"\b{re.escape(attr)}\b", text):
                    attributes.append(attr)
            one_line = " ".join(part.strip() for part in text.splitlines())
            print(
                f"{ordinal:04d} {path}:{line} KIND={kind} "
                f"ATTRS={','.join(attributes) or '-'} :: {one_line}"
            )
    print(f"TOTAL_ENTRIES {total}")
    print(
        "COUNTS "
        + " ".join(f"{kind}={count}" for kind, count in sorted(by_kind.items()))
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
