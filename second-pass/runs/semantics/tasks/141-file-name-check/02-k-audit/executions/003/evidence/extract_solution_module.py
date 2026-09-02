#!/usr/bin/env python3
"""Extract the balanced Module(...) RHS of solutionModule for K parsing."""

from pathlib import Path


SOURCE = Path("/tmp/audit-work/reconstruction/verification.k")
OUTPUT = Path("/tmp/audit-work/reconstruction/solutionModule.term")
PROGRAM_OUTPUT = Path("/tmp/audit-work/reconstruction/solutionModule.program.term")


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    anchor = "rule solutionModule =>"
    anchor_at = text.index(anchor)
    start = text.index("Module(", anchor_at + len(anchor))
    depth = 0
    in_string = False
    escaped = False
    end = None
    for index in range(start, len(text)):
        character = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
            continue
        if character == '"':
            in_string = True
        elif character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
            if depth == 0:
                end = index + 1
                break
    if end is None:
        raise RuntimeError("unbalanced solutionModule RHS")
    term = text[start:end]
    OUTPUT.write_text(term + "\n", encoding="utf-8")
    # `.Stmts` is the explicit K unit used in a definition rule.  The MPY
    # program parser spells the same variadic-list unit as an omitted trailing
    # argument, i.e. `..., )`, exactly as the trusted translator does.
    unit_count = term.count(".Stmts")
    program_term = term.replace(".Stmts", "")
    PROGRAM_OUTPUT.write_text(program_term + "\n", encoding="utf-8")
    print(f"source={SOURCE}")
    print(f"output={OUTPUT}")
    print(f"program_parser_output={PROGRAM_OUTPUT}")
    print(f"term_bytes={len(term.encode('utf-8'))}")
    print(f"explicit_stmts_units_normalized={unit_count}")


if __name__ == "__main__":
    main()
