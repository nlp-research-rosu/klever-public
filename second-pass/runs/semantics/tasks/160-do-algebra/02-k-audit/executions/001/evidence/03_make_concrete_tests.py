#!/usr/bin/env python3
"""Append independent concrete assertions to a translated Module(...) program."""

from __future__ import annotations

import argparse
from pathlib import Path


ASSERTIONS = [
    'Assert(Compare(Call(Name("do_algebra"), ListExpr(Str("+"), Str("*"), Str("-")), ListExpr(Int(2), Int(3), Int(4), Int(5))), CmpOp("==", Int(9))))',
    'Assert(Compare(Call(Name("do_algebra"), ListExpr(Str("+")), ListExpr(Int(0), Int(0))), CmpOp("==", Int(0))))',
    'Assert(Compare(Call(Name("do_algebra"), ListExpr(Str("-")), ListExpr(Int(0), Int(7))), CmpOp("==", Int(-7))))',
    'Assert(Compare(Call(Name("do_algebra"), ListExpr(Str("*")), ListExpr(Int(0), Int(9))), CmpOp("==", Int(0))))',
    'Assert(Compare(Call(Name("do_algebra"), ListExpr(Str("//")), ListExpr(Int(7), Int(3))), CmpOp("==", Int(2))))',
    'Assert(Compare(Call(Name("do_algebra"), ListExpr(Str("**")), ListExpr(Int(2), Int(5))), CmpOp("==", Int(32))))',
    'Assert(Compare(Call(Name("do_algebra"), ListExpr(Str("-"), Str("-")), ListExpr(Int(20), Int(5), Int(3))), CmpOp("==", Int(12))))',
    'Assert(Compare(Call(Name("do_algebra"), ListExpr(Str("//"), Str("//")), ListExpr(Int(20), Int(3), Int(2))), CmpOp("==", Int(3))))',
    'Assert(Compare(Call(Name("do_algebra"), ListExpr(Str("**"), Str("**")), ListExpr(Int(2), Int(3), Int(2))), CmpOp("==", Int(512))))',
    'Assert(Compare(Call(Name("do_algebra"), ListExpr(Str("+"), Str("*"), Str("**"), Str("//"), Str("-")), ListExpr(Int(4), Int(3), Int(2), Int(3), Int(5), Int(1))), CmpOp("==", Int(7))))',
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()

    source = args.source.read_text()
    if not source.endswith(")\n"):
        raise ValueError("expected translated Module to end in a single close-parenthesis line")
    body = source[:-2]
    appended = "".join(f"\n  {assertion}" for assertion in ASSERTIONS)
    args.destination.write_text(body + appended + "\n)\n")
    print(f"wrote {args.destination} with {len(ASSERTIONS)} assertions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
