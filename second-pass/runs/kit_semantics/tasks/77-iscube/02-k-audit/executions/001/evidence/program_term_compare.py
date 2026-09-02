#!/usr/bin/env python3
"""Mechanical constructor comparison between solution.mpy and IDENTITY's input."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction/candidate")


def remove_comments(text: str) -> str:
    return re.sub(r"//[^\n]*", "", text)


def compact(text: str) -> str:
    # The translator prints an empty Stmts production as an omitted argument;
    # the K claim spells the same unit as `.Stmts`.
    return re.sub(r"\s+", "", remove_comments(text)).replace(".Stmts", "")


def balanced_call(text: str, marker: str) -> str:
    start = text.index(marker) + len(marker)
    depth = 1
    quoted = False
    escaped = False
    for index in range(start, len(text)):
        character = text[index]
        if quoted:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                quoted = False
            continue
        if character == '"':
            quoted = True
        elif character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
            if depth == 0:
                return text[start:index]
    raise ValueError(f"unbalanced call after {marker!r}")


def main() -> None:
    solution_text = (ROOT / "solution.mpy").read_text()
    identity_text = remove_comments((ROOT / "identity-spec.k").read_text())
    identity_module = balanced_call(identity_text, "#loadAll(")
    expected = compact(solution_text)
    actual = compact(identity_module)
    print(f"solution_compact_length={len(expected)}")
    print(f"identity_input_compact_length={len(actual)}")
    print(f"constructor_term_equal={actual == expected}")
    if actual != expected:
        mismatch = next(
            (
                index
                for index, pair in enumerate(zip(actual, expected))
                if pair[0] != pair[1]
            ),
            min(len(actual), len(expected)),
        )
        print(f"first_mismatch_offset={mismatch}")
        print(f"solution_context={expected[mismatch:mismatch + 160]}")
        print(f"identity_context={actual[mismatch:mismatch + 160]}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
