#!/usr/bin/env python3
"""Extract the complete #loadAll argument from the entry claim for K parsing."""

from pathlib import Path


SPEC = Path("/tmp/audit-work/candidate/spec.k")
RAW_OUTPUT = Path("/audit-output/evidence/claimed_program_from_spec.kterm")
OUTPUT = Path("/audit-output/evidence/claimed_program_from_spec.mpy")


def main() -> None:
    text = SPEC.read_text()
    marker = "#loadAll("
    if text.count(marker) != 1:
        raise SystemExit(f"expected one {marker!r}, found {text.count(marker)}")
    start = text.index(marker) + len(marker)
    while text[start].isspace():
        start += 1
    if not text.startswith("Module(", start):
        raise SystemExit("entry claim #loadAll argument does not begin with Module(")

    depth = 0
    in_string = False
    escaped = False
    end = None
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
                end = index + 1
                break
            if depth < 0:
                raise SystemExit("unbalanced closing parenthesis")
    if end is None:
        raise SystemExit("unterminated Module term")
    claimed_program = text[start:end] + "\n"
    RAW_OUTPUT.write_text(claimed_program)
    # .Stmts and .Exprs are the explicit K unit constructors accepted in a
    # claim term. The MPY program parser spells the same units by omission.
    parser_form = claimed_program.replace(".Stmts", "").replace(".Exprs", "")
    OUTPUT.write_text(parser_form)
    print(f"source={SPEC}")
    print(f"raw_output={RAW_OUTPUT}")
    print(f"output={OUTPUT}")
    print(f"raw_chars={len(claimed_program)}")
    print(f"parser_chars={len(parser_form)}")
    print("normalization=remove explicit .Stmts/.Exprs unit spellings")
    print("EXTRACTION=PASS")


if __name__ == "__main__":
    main()
