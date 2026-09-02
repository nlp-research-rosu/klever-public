#!/usr/bin/env python3
"""Check that every spec entry term is the exact submitted translated program."""

from __future__ import annotations

import hashlib
from pathlib import Path


WORK = Path("/tmp/audit-work")


def extract_balanced_modules(text: str) -> list[str]:
    results: list[str] = []
    offset = 0
    while True:
        start = text.find("Module(", offset)
        if start < 0:
            break
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
                    results.append(text[start : index + 1])
                    offset = index + 1
                    break
        else:
            raise ValueError("unbalanced Module term")
    return results


def normalize(text: str) -> str:
    output: list[str] = []
    quoted = False
    escaped = False
    for char in text:
        if quoted:
            output.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
            output.append(char)
        elif not char.isspace():
            output.append(char)
    return "".join(output)


def main() -> int:
    submitted = (WORK / "submitted-solution.mpy").read_text(encoding="utf-8")
    spec = (WORK / "build-proof" / "spec.k").read_text(encoding="utf-8")
    expected = normalize(submitted)
    terms = extract_balanced_modules(spec)
    print(f"submitted normalized AST={expected}")
    print(f"submitted normalized sha256={hashlib.sha256(expected.encode()).hexdigest()}")
    print(f"entry Module terms found={len(terms)}")
    mismatches = 0
    for index, term in enumerate(terms, 1):
        normalized = normalize(term)
        same = normalized == expected
        print(
            f"claim={index} same_as_submitted={same} "
            f"sha256={hashlib.sha256(normalized.encode()).hexdigest()}"
        )
        if not same:
            mismatches += 1
    print(f"pinning mismatches={mismatches}")
    return 1 if len(terms) != 5 or mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
