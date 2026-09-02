#!/usr/bin/env python3
"""Extract the Module argument executed by the entry claim's #loadAll term."""

from pathlib import Path


def main() -> None:
    text = Path("/tmp/audit-work/reconstruction/spec.k").read_text()
    marker = "#loadAll("
    marker_at = text.index(marker)
    start = marker_at + len(marker)
    depth = 1
    in_string = False
    escaped = False
    end = -1
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
                end = index
                break
    if end < 0:
        raise RuntimeError("unbalanced #loadAll argument")
    argument = text[start:end].strip()
    if not argument.startswith("Module("):
        raise RuntimeError(f"unexpected #loadAll argument: {argument[:80]!r}")
    # The spec parser permits explicit associative-list identities in a rule term,
    # while the program parser expects them to be omitted. Removing `.Stmts`
    # changes no constructor list: it is the Stmts unit.
    print(argument.replace(".Stmts", ""))


if __name__ == "__main__":
    main()
