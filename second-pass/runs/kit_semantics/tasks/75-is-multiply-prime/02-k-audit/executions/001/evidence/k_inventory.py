#!/usr/bin/env python3
"""Create a complete line-addressed inventory of local K declarations/rules."""

from __future__ import annotations

import collections
import re
import sys
from pathlib import Path


START = re.compile(r"^(syntax|configuration|rule|claim|context|alias)\b")
ATTR_NAMES = (
    "function", "functional", "total", "symbol", "no-evaluators",
    "priority", "owise", "concrete", "simplification", "macro", "macro-rec",
    "strict", "seqstrict", "anywhere",
)


def strip_line_comment(line: str) -> str:
    """Remove // comments while preserving // inside quoted K strings."""
    in_string = False
    escaped = False
    index = 0
    while index < len(line):
        char = line[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
        elif char == "/" and index + 1 < len(line) and line[index + 1] == "/":
            return line[:index]
        index += 1
    return line


def items(path: Path):
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for number, line in enumerate(lines, 1):
        stripped = strip_line_comment(line).strip()
        match = START.match(stripped)
        if match:
            starts.append((number, match.group(1)))

    for index, (number, kind) in enumerate(starts):
        stop = starts[index + 1][0] - 1 if index + 1 < len(starts) else len(lines)
        block_lines = lines[number - 1:stop]
        while block_lines and (
            not block_lines[-1].strip()
            or block_lines[-1].lstrip().startswith("//")
            or block_lines[-1].strip() == "endmodule"
        ):
            block_lines.pop()
        text = " ".join(
            strip_line_comment(part).strip()
            for part in block_lines
            if strip_line_comment(part).strip()
        )
        text = re.sub(r"\s+", " ", text)
        attribute_text = " ".join(re.findall(r"\[[^\]]*\]", text))
        attrs = [
            name
            for name in ATTR_NAMES
            if re.search(rf"\b{re.escape(name)}\b", attribute_text)
        ]
        yield number, kind, attrs, text


def main() -> int:
    if len(sys.argv) < 2:
        raise SystemExit("usage: k_inventory.py FILE...")

    print("# Complete K source inventory")
    print()
    print("Generated from source. Each row identifies one local declaration, "
          "configuration, context, rule, or claim by file and starting line.")
    print()

    grand = collections.Counter()
    for raw in sys.argv[1:]:
        path = Path(raw)
        found = list(items(path))
        counts = collections.Counter(kind for _, kind, _, _ in found)
        attr_counts = collections.Counter(attr for _, _, attrs, _ in found for attr in attrs)
        grand.update(counts)
        grand.update({f"attr:{key}": value for key, value in attr_counts.items()})

        print(f"## {path}")
        print()
        print("Counts: " + ", ".join(
            [f"{key}={counts[key]}" for key in sorted(counts)]
            + [f"{key}={attr_counts[key]}" for key in sorted(attr_counts)]
        ))
        print()
        print("| Line | Kind | Attributes | Source item |")
        print("|---:|---|---|---|")
        for number, kind, attrs, text in found:
            safe = text.replace("|", "&#124;")
            print(f"| {number} | {kind} | {', '.join(attrs) or '—'} | `{safe}` |")
        print()

    print("## Grand totals")
    print()
    print(", ".join(f"{key}={grand[key]}" for key in sorted(grand)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
