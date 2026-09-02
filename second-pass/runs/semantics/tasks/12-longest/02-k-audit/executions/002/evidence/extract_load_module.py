#!/usr/bin/env python3
"""Extract the Module(...) term executed by the load-solution claim."""

from __future__ import annotations

from pathlib import Path
import sys


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: extract_load_module.py SPEC.k", file=sys.stderr)
        return 2
    source = Path(sys.argv[1]).read_text(encoding="utf-8")
    marker = "#loadAll(Module("
    marker_offset = source.index(marker)
    start = marker_offset + len("#loadAll(")

    depth = 0
    in_string = False
    escaped = False
    for offset in range(start, len(source)):
        char = source[offset]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                sys.stdout.write(source[start : offset + 1] + "\n")
                return 0
    raise RuntimeError("unterminated Module term")


if __name__ == "__main__":
    raise SystemExit(main())
