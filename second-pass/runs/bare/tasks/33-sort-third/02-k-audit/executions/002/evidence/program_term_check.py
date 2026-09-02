#!/usr/bin/env python3
"""Constructor-level comparison of solution.mpy with every spec entry term."""

from __future__ import annotations

import argparse
from pathlib import Path


def strip_layout(text: str) -> str:
    out: list[str] = []
    quoted = False
    escaped = False
    for char in text:
        if quoted:
            out.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
            out.append(char)
        elif not char.isspace():
            out.append(char)
    return "".join(out)


def module_terms(text: str) -> list[str]:
    terms: list[str] = []
    start = 0
    while True:
        start = text.find("Module(", start)
        if start < 0:
            return terms
        depth = 0
        quoted = False
        escaped = False
        for index in range(start, len(text)):
            char = text[index]
            if quoted:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    quoted = False
                continue
            if char == '"':
                quoted = True
            elif char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0:
                    terms.append(text[start : index + 1])
                    start = index + 1
                    break
        else:
            raise ValueError("unterminated Module(...) term")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("program", type=Path)
    parser.add_argument("spec", type=Path)
    args = parser.parse_args()

    program = strip_layout(args.program.read_text(encoding="utf-8"))
    entries = [strip_layout(term) for term in module_terms(
        args.spec.read_text(encoding="utf-8")
    )]
    matches = [entry == program for entry in entries]
    print(f"entry_terms={len(entries)}")
    print(f"constructor_matches={matches}")
    print(f"all_match={bool(entries) and all(matches)}")
    if not entries or not all(matches):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
