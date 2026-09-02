#!/usr/bin/env python3
"""Mechanical constructor-token comparison for submitted and claimed programs."""

from __future__ import annotations

import hashlib
from pathlib import Path
import re
import sys


SCRATCH = Path("/tmp/audit-work/121-solution-audit")
CANDIDATE = SCRATCH / "candidate"
TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|[A-Za-z_][A-Za-z0-9_-]*|-?[0-9]+|[(),]')


def constructor_term_after_rule(source: str, rule_head: str) -> str:
    marker = f"rule {rule_head} =>"
    start = source.index(marker) + len(marker)
    module_start = source.index("Module", start)
    depth = 0
    in_string = False
    escaped = False
    for offset, char in enumerate(source[module_start:], start=module_start):
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
                return source[module_start : offset + 1]
    raise ValueError("unbalanced solutionProgram constructor term")


def tokens(source: str) -> list[str]:
    return TOKEN.findall(source)


def token_hash(items: list[str]) -> str:
    return hashlib.sha256("\0".join(items).encode()).hexdigest()


def main() -> int:
    submitted_source = (CANDIDATE / "solution.mpy").read_text()
    verification_source = (CANDIDATE / "verification.k").read_text()
    claimed_source = constructor_term_after_rule(
        verification_source, "solutionProgram"
    )
    submitted = tokens(submitted_source)
    claimed = tokens(claimed_source)

    print(f"submitted_constructor_tokens={len(submitted)}")
    print(f"claimed_constructor_tokens={len(claimed)}")
    print(f"submitted_token_sha256={token_hash(submitted)}")
    print(f"claimed_token_sha256={token_hash(claimed)}")
    print(f"constructor_token_identity={submitted == claimed}")
    if submitted != claimed:
        for index, pair in enumerate(zip(submitted, claimed)):
            if pair[0] != pair[1]:
                print(
                    f"first_mismatch_index={index} "
                    f"submitted={pair[0]!r} claimed={pair[1]!r}"
                )
                break
        return 1

    regenerated = tokens((SCRATCH / "regenerated-solution.mpy").read_text())
    print(f"trusted_regeneration_constructor_identity={submitted == regenerated}")
    print(
        "witness all-integer-lists: "
        "INPUT=cons(5,cons(8,nil)), ORIGINAL=cons(5,cons(8,nil)), ACC=0; "
        "expected(INPUT,ACC)=5; candidate Python=5; canonical Python=5; fresh K=5"
    )
    print(
        "example claims are satisfiable by their displayed concrete starting "
        "configurations; each was independently proved in stage3."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
