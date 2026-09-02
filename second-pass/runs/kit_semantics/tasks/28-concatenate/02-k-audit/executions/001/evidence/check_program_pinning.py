#!/usr/bin/env python3
"""Constructor-level comparison of translated solution.mpy and SPEC entry term."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


SOLUTION = Path("/tmp/audit-work/reconstruction/regenerated-solution.mpy")
SPEC = Path("/tmp/audit-work/reconstruction/spec.k")


def balanced_argument(text: str, call: str) -> str:
    start = text.index(call) + len(call)
    depth = 1
    in_string = False
    escaped = False
    for index in range(start, len(text)):
        char = text[index]
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
                return text[start:index]
    raise ValueError(f"unterminated {call}")


def lexical_normalize(text: str) -> str:
    # Whitespace outside K String tokens is syntactically inert here.
    out: list[str] = []
    in_string = False
    escaped = False
    for char in text:
        if in_string:
            out.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
            out.append(char)
        elif not char.isspace():
            out.append(char)
    return "".join(out)


def main() -> int:
    translated = lexical_normalize(SOLUTION.read_text())
    entry_region = SPEC.read_text().split("claim [concatenate]:", 1)[1]
    claimed = lexical_normalize(balanced_argument(entry_region, "#loadAll("))
    equal = translated == claimed
    print(f"translated_sha256={hashlib.sha256(translated.encode()).hexdigest()}")
    print(f"claimed_module_sha256={hashlib.sha256(claimed.encode()).hexdigest()}")
    print(f"constructor_level_equal={equal}")
    print(f"translated_prefix={translated[:120]}")
    print(f"claimed_prefix={claimed[:120]}")
    if re.search(r"\b(Call|For|AugAssign|Return)\b", claimed) is None:
        print("ERROR: material constructors unexpectedly absent")
        return 1
    return 0 if equal else 1


if __name__ == "__main__":
    raise SystemExit(main())
