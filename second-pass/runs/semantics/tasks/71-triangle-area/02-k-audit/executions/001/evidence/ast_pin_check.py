#!/usr/bin/env python3
"""Mechanically compose the verification constants and compare to solution.mpy."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


def normalized(text: str) -> str:
    # The MPY surface used here has no whitespace-bearing string literals.
    compact = re.sub(r"\s+", "", text)
    # K's List{Stmt,""} parser accepts both an omitted final empty element and
    # the explicit identity `.Stmts`; these are the same parsed AST.
    return compact.replace(",.Stmts)", ",)")


def extract(pattern: str, text: str, label: str) -> str:
    match = re.search(pattern, text, re.DOTALL)
    if match is None:
        raise RuntimeError(f"could not extract {label}")
    return match.group(1).strip()


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: ast_pin_check.py SOLUTION_MPY VERIFICATION_K", file=sys.stderr)
        return 64
    solution = Path(sys.argv[1]).read_text(encoding="utf-8")
    verification = Path(sys.argv[2]).read_text(encoding="utf-8")

    body = extract(
        r"rule triangleAreaBody\s*=>\s*(.*?)\n\s*syntax Val ::= \"triangleAreaClosure\"",
        verification,
        "triangleAreaBody",
    )
    module = extract(
        r"rule triangleAreaModule\s*=>\s*(.*?)\n\s*// The exact proof-domain",
        verification,
        "triangleAreaModule",
    )
    closure = extract(
        r"rule triangleAreaClosure\s*=>\s*(.*?)\n\s*syntax Module",
        verification,
        "triangleAreaClosure",
    )

    if module.count("triangleAreaBody") != 1:
        raise RuntimeError("triangleAreaModule does not contain exactly one body placeholder")
    composed = module.replace("triangleAreaBody", body)
    left = normalized(solution)
    right = normalized(composed)

    expected_closure = 'closureVal(("a","b","c"),triangleAreaBody,0)'
    closure_matches = normalized(closure) == normalized(expected_closure)
    module_matches = left == right
    print(f"SOLUTION_NORMALIZED_SHA256={hashlib.sha256(left.encode()).hexdigest()}")
    print(f"COMPOSED_NORMALIZED_SHA256={hashlib.sha256(right.encode()).hexdigest()}")
    print(f"MODULE_AST_MATCH={module_matches}")
    print(f"CLOSURE_SHAPE_MATCH={closure_matches}")
    if not module_matches:
        first = next(
            (index for index, pair in enumerate(zip(left, right)) if pair[0] != pair[1]),
            min(len(left), len(right)),
        )
        print(f"FIRST_MISMATCH_OFFSET={first}")
        print(f"SOLUTION_CONTEXT={left[max(0, first - 80):first + 120]}")
        print(f"COMPOSED_CONTEXT={right[max(0, first - 80):first + 120]}")
        print(f"SOLUTION_LENGTH={len(left)} COMPOSED_LENGTH={len(right)}")
    return 0 if module_matches and closure_matches else 1


if __name__ == "__main__":
    raise SystemExit(main())
