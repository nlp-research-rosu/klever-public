#!/usr/bin/env python3
"""Extract #loadAll's sole KORE argument from a compiled claim module."""

from __future__ import annotations

import sys
from pathlib import Path


LOAD_ALL_LABEL = (
    "Lbl'Hash'loadAll'LParUndsRParUnds'MPY-CORE'Unds'KItem'Unds'Module{}"
)


def extract_argument(kore: str) -> str:
    label_index = kore.index(LOAD_ALL_LABEL)
    open_index = kore.index("(", label_index + len(LOAD_ALL_LABEL))
    depth = 1
    in_string = False
    escaped = False
    for index in range(open_index + 1, len(kore)):
        char = kore[index]
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
                return kore[open_index + 1 : index].strip()
    raise ValueError("unterminated KORE #loadAll argument")


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {sys.argv[0]} SPEC.KORE")
    sys.stdout.write(extract_argument(Path(sys.argv[1]).read_text()))


if __name__ == "__main__":
    main()
