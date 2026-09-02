#!/usr/bin/env python3
"""Extract the Module argument executed by the entry claim's #loadAll."""

from __future__ import annotations

import sys
from pathlib import Path


def extract_load_all_argument(spec_text: str) -> str:
    marker = "#loadAll("
    marker_index = spec_text.index(marker)
    start = marker_index + len(marker)
    depth = 1
    in_string = False
    escaped = False
    for index in range(start, len(spec_text)):
        char = spec_text[index]
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
                extracted = spec_text[start:index].strip()
                assert extracted.startswith("Module(")
                return extracted + "\n"
    raise ValueError("unterminated #loadAll argument")


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {sys.argv[0]} SPEC.K")
    print(extract_load_all_argument(Path(sys.argv[1]).read_text()), end="")


if __name__ == "__main__":
    main()
