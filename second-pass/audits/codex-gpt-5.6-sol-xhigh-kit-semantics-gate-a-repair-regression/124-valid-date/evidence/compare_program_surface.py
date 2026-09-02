#!/usr/bin/env python3
"""Compare submitted MPY text with the embedded K RHS at token level.

The program parser permits omitted empty list tails, while K rules spell those
tails as `.Stmts` or `.Exprs`. This comparator removes only those two explicit
empty-tail tokens and requires all remaining tokens to be identical.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


TOKEN = re.compile(
    r'"(?:\\.|[^"\\])*"'          # quoted K string token
    r"|(?:\.Stmts|\.Exprs)"       # only explicit empty tails we may erase
    r"|(?:[A-Za-z_][A-Za-z_0-9]*)"
    r"|(?:-?[0-9]+)"
    r"|(?:\S)"
)


def tokens(text: str) -> list[str]:
    return TOKEN.findall(text)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("submitted", type=Path)
    parser.add_argument("embedded", type=Path)
    args = parser.parse_args()

    submitted_tokens = tokens(args.submitted.read_text(encoding="utf-8"))
    embedded_tokens_raw = tokens(args.embedded.read_text(encoding="utf-8"))
    erased = [token for token in embedded_tokens_raw if token in (".Stmts", ".Exprs")]
    embedded_tokens = [
        token for token in embedded_tokens_raw if token not in (".Stmts", ".Exprs")
    ]

    equal = submitted_tokens == embedded_tokens
    print(f"submitted_tokens={len(submitted_tokens)}")
    print(f"embedded_tokens_before_empty_tail_erasure={len(embedded_tokens_raw)}")
    print(f"erased_explicit_empty_tails={len(erased)}")
    print(f"erased_Stmts={erased.count('.Stmts')}")
    print(f"erased_Exprs={erased.count('.Exprs')}")
    print(f"remaining_tokens_identical={str(equal).lower()}")
    if not equal:
        mismatch = next(
            (
                index
                for index, pair in enumerate(zip(submitted_tokens, embedded_tokens))
                if pair[0] != pair[1]
            ),
            min(len(submitted_tokens), len(embedded_tokens)),
        )
        print(f"first_mismatch_index={mismatch}")
        print(f"submitted_context={submitted_tokens[max(0, mismatch-12):mismatch+12]}")
        print(f"embedded_context={embedded_tokens[max(0, mismatch-12):mismatch+12]}")
    return 0 if equal else 1


if __name__ == "__main__":
    raise SystemExit(main())
