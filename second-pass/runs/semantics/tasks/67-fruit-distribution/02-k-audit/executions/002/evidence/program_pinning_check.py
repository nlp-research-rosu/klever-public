#!/usr/bin/env python3
"""Compare the regenerated MPY constructor tree with solutionModule's RHS."""

from __future__ import annotations

from pathlib import Path
import re
import sys


def balanced_term(text: str, marker: str) -> str:
    start = text.index(marker) + len(marker)
    start = text.index("Module(", start)
    depth = 0
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
                return text[start : index + 1]
    raise ValueError("unbalanced Module term")


def normalize(term: str) -> str:
    # The translator pretty-printer omits the empty Exprs unit; K accepts both
    # the omitted optional list and the explicit `.Exprs` used in verification.k.
    term = term.replace(".Exprs", "")
    term = re.sub(r"\s+", "", term)
    # Explicit list tails leave a surface trailing comma after the unit is
    # erased; the translator's optional-list form omits that comma.
    return term.replace(",)", ")")


def main() -> int:
    regenerated_text = Path(
        "/tmp/audit-work/reconstruction/regenerated.mpy"
    ).read_text()
    verification_text = Path(
        "/tmp/audit-work/reconstruction/verification.k"
    ).read_text()
    regenerated = balanced_term(regenerated_text, "")
    proof_rhs = balanced_term(verification_text, "rule solutionModule =>")
    same = normalize(regenerated) == normalize(proof_rhs)
    print(f"regenerated_constructor_chars={len(normalize(regenerated))}")
    print(f"solutionModule_constructor_chars={len(normalize(proof_rhs))}")
    print(
        "normalization=ASCII whitespace plus explicit optional .Exprs "
        "units/trailing surface commas only"
    )
    print(f"constructor_identity={same}")
    if not same:
        print(f"regenerated={normalize(regenerated)}")
        print(f"solutionModule={normalize(proof_rhs)}")
    return 0 if same else 1


if __name__ == "__main__":
    sys.exit(main())
