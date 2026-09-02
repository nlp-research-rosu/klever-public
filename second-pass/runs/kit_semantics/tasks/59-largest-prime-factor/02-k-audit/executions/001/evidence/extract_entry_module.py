#!/usr/bin/env python3
"""Extract the Module(...) term executed by SPEC.entry for parser comparison."""

import argparse
from pathlib import Path


def balanced_constructor(text: str, start: int) -> str:
    open_paren = text.find("(", start)
    if open_paren < 0:
        raise ValueError("constructor has no opening parenthesis")
    depth = 0
    quoted = False
    escaped = False
    for i in range(open_paren, len(text)):
        ch = text[i]
        if quoted:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                quoted = False
            continue
        if ch == '"':
            quoted = True
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return text[start : i + 1]
    raise ValueError("unterminated constructor")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--strip-stmts-units",
        action="store_true",
        help="remove explicit .Stmts list units before standalone program parsing",
    )
    args = parser.parse_args()

    text = args.spec.read_text()
    entry = text.index("claim [entry]:")
    load = text.index("#loadAll(", entry)
    module = text.index("Module(", load)
    term = balanced_constructor(text, module)
    unit_count = term.count(".Stmts")
    if args.strip_stmts_units:
        term = term.replace(".Stmts", "")
    args.output.write_text(term + "\n")
    print(f"entry_claim_offset={entry}")
    print(f"module_offset={module}")
    print(f"module_bytes={len(term.encode())}")
    print(f"explicit_stmts_units={unit_count}")
    print(f"stripped_stmts_units={unit_count if args.strip_stmts_units else 0}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
