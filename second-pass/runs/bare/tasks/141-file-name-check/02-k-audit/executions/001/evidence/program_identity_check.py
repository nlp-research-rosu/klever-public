#!/usr/bin/env python3
"""Check that verification.k's solutionProgram literal is solution.mpy's AST."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def balanced_term(text: str, start: int) -> str:
    depth = 0
    in_string = False
    escaped = False
    seen_open = False
    for index in range(start, len(text)):
        ch = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == "(":
            depth += 1
            seen_open = True
        elif ch == ")":
            depth -= 1
            if seen_open and depth == 0:
                return text[start : index + 1]
    raise ValueError("unbalanced solutionProgram term")


def normalize(text: str) -> str:
    # The translator renders an empty Stmts list as an empty argument; K source
    # writes the same list explicitly as .Stmts.
    return re.sub(r"\s+", "", text.replace(".Stmts", ""))


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit("usage: program_identity_check.py verification.k solution.mpy")
    verification_text = Path(sys.argv[1]).read_text(encoding="utf-8")
    solution_text = Path(sys.argv[2]).read_text(encoding="utf-8")
    marker = re.search(r"rule\s+solutionProgram\s*=>\s*Module\s*\(", verification_text)
    if marker is None:
        print("IDENTITY_MATCH=False")
        print("ERROR=solutionProgram rule not found")
        return 1
    module_start = verification_text.index("Module", marker.start())
    literal = balanced_term(verification_text, module_start)
    lhs = normalize(literal)
    rhs = normalize(solution_text)
    print(f"VERIFICATION_LITERAL_NORMALIZED_LENGTH={len(lhs)}")
    print(f"SOLUTION_MPY_NORMALIZED_LENGTH={len(rhs)}")
    print(f"IDENTITY_MATCH={lhs == rhs}")
    if lhs != rhs:
        for index, (left, right) in enumerate(zip(lhs, rhs)):
            if left != right:
                print(f"FIRST_DIFFERENCE_INDEX={index}")
                print(f"VERIFICATION_CONTEXT={lhs[max(0, index-40):index+40]!r}")
                print(f"SOLUTION_CONTEXT={rhs[max(0, index-40):index+40]!r}")
                break
        else:
            print("FIRST_DIFFERENCE_INDEX=length-only")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
